use std::{fmt, iter::zip};

use anyhow::{anyhow, bail, Context, Result};
use macro_rules_attribute::apply;
use once_cell::sync::Lazy;
use pyo3::{
    exceptions::PyValueError,
    prelude::{PyAny, *},
    sync::{GILLazy, GILLazyPy},
    types::PyTuple,
};
use regex::Regex;
use rr_util::{
    eq_by_big_hash::EqByBigHash,
    impl_eq_by_big_hash,
    name::Name,
    py_types::{PySymShape, Tensor, PY_UTILS, SELF_MODULE},
    pycall, python_error_exception,
    shape::{broadcast_shapes_impl, shape_eq_if_known, shape_join_eq, shape_to_py, Shape, Size},
    simple_from, sv,
    tensor_util::{
        check_canon_idxs, upcast_tensor_device_dtypes, upcast_tensor_devices, MiscInputError,
        TorchDevice, TorchDeviceDtypeOp, TorchDtype,
    },
};
use rustc_hash::FxHashMap as HashMap;
use smallvec::ToSmallVec;
use thiserror::Error;
use uuid::{uuid, Uuid};

use crate::{
    auto_name::OperatorPriority,
    circuit_node_auto_impl, circuit_node_extra_impl,
    circuit_node_private::{CircuitNodeComputeInfoImpl, CircuitNodeHashItems},
    new_rc_unwrap,
    prelude::*,
    CachedCircuitInfo, HashBytes, PyCircuitBase,
};

macro_rules! gf_gen {
    ($(($name:ident, $($t:tt)*)),* $(,)?) => {
        pub const BASIC_SPEC_ITEMS: &'static [(&'static str, bool, u8, u8)] = &[
            $(
                gf_gen!(@item $name, $($t)*),
            )*
        ];

        $(
        #[pyfunction]
        pub fn $name(circuit: CircuitRc, name: Option<Name>) -> Result<GeneralFunction> {
            GeneralFunction::new_by_name(vec![circuit], stringify!($name).into(), name)
        }
        )*

        pub fn register(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
            $(
            m.add_function(wrap_pyfunction!($name, m)?)?;
            )*
            Ok(())
        }
    };
    (@item $name:ident, $p:expr, $non_b:expr, $rem:expr $(,)?) => {
        (stringify!($name), $p, $non_b, $rem)
    };
    (@item $name:ident, $p:expr, $non_b:expr $(,)?) => {
        (stringify!($name), $p, $non_b, 0)
    };
}

// tuples correspond to GeneralFunctionSimpleSpec fields (default removed_from_end = 0)
gf_gen!(
    (sin, true, 0),
    (cos, true, 0),
    (sigmoid, true, 0),
    (tanh, true, 0),
    (rsqrt, true, 0),
    (gelu, false, 0),
    (gelu_new, true, 0),
    (relu, false, 0),
    (step, false, 0),
    (reciprocal, true, 0),
    (log_exp_p_1, true, 0),
    (gaussian_pdf, true, 0),
    (gaussian_cdf, true, 0),
    (softmax, false, 1),
    (log_softmax, false, 1),
    // (q_from_qr, false, 2, 0), // TODO: this requires first dim > second dim!
    (min, false, 0, 1),
    (max, false, 0, 1),
    (last_dim_size, false, 0, 1),
    (abs, false, 0),
    (exp, true, 0),
    (log, true, 0),
    (logit, true, 0),
);

static SPECS: GILLazy<HashMap<String, GeneralFunctionSpec>> = GILLazy::new(|| {
    BASIC_SPEC_ITEMS
        .iter()
        .cloned()
        .map(
            |(name, promote_int_to_f32, num_non_batchable_output_dims, removed_from_end)| {
                (
                    name.to_owned(),
                    GeneralFunctionSpec::Simple(GeneralFunctionSimpleSpec {
                        name: name.into(),
                        promote_int_to_f32,
                        num_non_batchable_output_dims,
                        removed_from_end,
                    }),
                )
            },
        )
        .collect()
});

pub const OFFICIAL_GENERALFUNCTION_INVERSES: [(&str, &str); 1] = [("reciprocal", "reciprocal")];

/// GeneralFunctionSpec contains all needed info about function, and is the same on all instances with the same function
/// how batchability works: input_batchability is a mask indicating which inputs support batching. if none do, there is no batching.
/// the number of non batchable dims in output, starting from end, is num_non_batchable_output_dims.
pub trait SpecTrait: fmt::Debug + ToPyObject {
    fn compute_hash(&self) -> HashBytes;
    fn function(&self, tensors: &[Tensor]) -> Result<Tensor>;
    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo>;
    // fn expand()
    // fn has_jacobian(&self) -> Result<bool>;
    // fn get_jacobians(&self, func: &GeneralFunction) -> Result<Option<Vec<Circuit>>>;
    fn name(&self) -> &'static str;
    fn is_official(&self) -> bool {
        false
    }
    fn serialize(&self) -> Result<String>;
    // returning None means use normal device_dtype inheritance. if Some, then error if dtypes are incorrect and dtype if correct
    fn get_device_dtype_override(
        &self,
        _device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Result<Option<TorchDeviceDtypeOp>> {
        Ok(None)
    }
    // should this function be evaluated if possible during circuit optimization?
    fn should_const_fold(&self, self_circ: &GeneralFunction) -> bool {
        // if you change this then probably also update GeneralFunctionSpecBase & MultiOutputGeneralFunctionSpecBase to match
        self_circ.rank() == 0
            && self_circ.num_children() == 1
            && self_circ.children_sl()[0].rank() == 0
    }
}

#[pyclass]
#[derive(Debug, Clone, Eq, Hash, PartialEq)]
pub struct GeneralFunctionShapeInfo {
    #[pyo3(set)]
    pub shape: Shape,
    #[pyo3(get, set)]
    pub num_non_batchable_output_dims: u8,
    #[pyo3(get, set)]
    pub input_batchability: Vec<bool>,
}

#[pymethods]
impl GeneralFunctionShapeInfo {
    #[getter]
    fn shape(&self) -> PySymShape {
        PySymShape(self.shape.clone())
    }

    /// no checking done here, validation done in validate
    #[new]
    pub fn new(
        shape: Shape,
        num_non_batchable_output_dims: u8,
        input_batchability: Vec<bool>,
    ) -> Self {
        Self {
            shape,
            num_non_batchable_output_dims,
            input_batchability,
        }
    }
}

impl GeneralFunctionShapeInfo {
    pub fn validate(&self, shapes: &[Shape]) -> Result<()> {
        if shapes.len() != self.input_batchability.len() {
            bail!(GeneralFunctionShapeError::WrongNumShapes {
                got: shapes.len(),
                expected: self.input_batchability.len()
            })
        }

        if self.num_non_batchable_output_dims as usize > self.shape.len() {
            bail!("GeneralFunctionShapeInfo: too many num_non_batchable_output_dims! num_non_batchable_output_dims={:?} shape={:?}", self.num_non_batchable_output_dims, self.shape)
        }

        if self.input_batchability.iter().any(|b| *b) {
            let batch_dims = self.shape.len() - self.num_non_batchable_output_dims as usize;

            for (shape, &is_batch) in shapes.iter().zip(&self.input_batchability) {
                if is_batch && shape.len() < batch_dims {
                    bail!(
                "some batchable shape too short for batch, shape.len()={} batch_dims={batch_dims}",
                shape.len(),
            );
                }
            }

            let mut batch_shape = self.shape[..batch_dims].to_smallvec();
            let batches: Vec<&[Size]> = shapes
                .iter()
                .zip(&self.input_batchability)
                .filter(|(_, b)| **b)
                .map(|(s, _)| &s[..batch_dims])
                .collect();
            for x in &batches[..] {
                batch_shape = shape_join_eq(&batch_shape, x, || {
                    anyhow!(GeneralFunctionShapeError::BatchDimsNotEqual {
                        batches: batches.iter().map(|x| (*x).into()).collect(),
                        output_batch: self.shape[..batch_dims].into()
                    })
                })?
            }
        }

        Ok(())
    }

    pub fn batch_dims(&self) -> usize {
        self.shape.len() - self.num_non_batchable_output_dims as usize
    }

    pub fn batch_shape(&self) -> &[Size] {
        &self.shape[..self.batch_dims()]
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GeneralFunctionSimpleSpec {
    #[pyo3(get)]
    pub name: Name,
    #[pyo3(get)]
    pub promote_int_to_f32: bool,
    #[pyo3(get)]
    pub num_non_batchable_output_dims: u8,
    #[pyo3(get)]
    pub removed_from_end: u8,
}

simple_from!(|x: GeneralFunctionSimpleSpec| -> GeneralFunctionSpec {
    GeneralFunctionSpec::Simple(x)
});

impl ToPyObject for GeneralFunctionSimpleSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

#[pyfunction]
pub fn get_shape_info_simple(
    shapes: Vec<Shape>,
    promote_int_to_f32: Option<bool>,
    num_non_batchable_output_dims: Option<u8>,
    removed_from_end: Option<u8>,
) -> Result<GeneralFunctionShapeInfo> {
    GeneralFunctionSimpleSpec {
        name: "".into(),
        promote_int_to_f32: promote_int_to_f32.unwrap_or(false),
        num_non_batchable_output_dims: num_non_batchable_output_dims.unwrap_or(0),
        removed_from_end: removed_from_end.unwrap_or(0),
    }
    .get_shape_info(&shapes)
}

#[pymethods]
impl GeneralFunctionSimpleSpec {
    fn get_function(&self) -> PyObject {
        PY_UTILS.generalfunctions[&self.name.string()].clone()
    }
}

impl GeneralFunctionSimpleSpec {}

impl SpecTrait for GeneralFunctionSimpleSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(uuid!("f1f0bc63-f390-412b-9e98-74ce65911006").as_bytes()); // uuid for SimpleSpec
        hasher.update(self.name.as_bytes()); // names are unique
        *hasher.finalize().as_bytes()
    }

    fn function(&self, tensors: &[Tensor]) -> Result<Tensor> {
        let tensors = upcast_tensor_device_dtypes(tensors);
        Python::with_gil(|py| {
            Ok(self
                .get_function()
                .call(
                    py,
                    PyTuple::new(py, tensors.iter().map(|x| x.clone().into_py(py))),
                    None,
                )
                .context(format!("evaluate function {}", self.name))?
                .extract(py)?)
        })
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        if shapes.len() != 1 {
            bail!(GeneralFunctionShapeError::WrongNumShapes {
                got: shapes.len(),
                expected: 1
            });
        }
        if (shapes[0].len() as u8) < self.num_non_batchable_output_dims + self.removed_from_end {
            bail!(GeneralFunctionShapeError::NDimTooSmall {
                ndim: shapes[0].len(),
                num_non_batchable_output_dims: self.num_non_batchable_output_dims,
                removed_from_end: self.removed_from_end
            });
        }
        Ok(GeneralFunctionShapeInfo {
            shape: shapes[0][..shapes[0].len() - self.removed_from_end as usize]
                .iter()
                .cloned()
                .collect(),
            num_non_batchable_output_dims: self.num_non_batchable_output_dims,
            input_batchability: vec![true].into_iter().collect(),
        })
    }

    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Result<Option<TorchDeviceDtypeOp>> {
        if self.promote_int_to_f32
            && device_dtypes[0]
                .dtype
                .map_or(false, |x| !x.is_floating_point())
        {
            Ok(Some(TorchDeviceDtypeOp {
                device: device_dtypes[0].device,
                dtype: Some(TorchDtype::float32),
            }))
        } else {
            Ok(None)
        }
    }

    // fn has_jacobian(&self) -> Result<bool> {
    //     Ok(self.get_jacobians.is_some())
    // }
    // fn get_jacobians(&self, func: &GeneralFunction) -> Result<Option<Vec<Circuit>>> {}

    fn name(&self) -> &'static str {
        self.name.into()
    }
    fn is_official(&self) -> bool {
        true
    }
    fn serialize(&self) -> Result<String> {
        Ok(self.name().into())
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GeneralFunctionIndexSpec {
    #[pyo3(get)]
    pub index_dim: i64,
    #[pyo3(get)]
    pub batch_x: bool,
    #[pyo3(get)]
    pub batch_index: bool,
    #[pyo3(get)]
    pub check_index_ints: bool,
}

simple_from!(|x: GeneralFunctionIndexSpec| -> GeneralFunctionSpec {
    GeneralFunctionSpec::Index(x)
});

impl ToPyObject for GeneralFunctionIndexSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

fn index_get_device_dtype_override(
    device_dtypes: &[TorchDeviceDtypeOp],
) -> Result<Option<TorchDeviceDtypeOp>> {
    if let Some(dev1) = device_dtypes[0].device && let Some(dev2) = device_dtypes[1].device && dev1!=dev2{
            return Err(MiscInputError::ChildrenMultipleDevices { a: device_dtypes[0].device, b: device_dtypes[1].device}.into())
        }
    if let Some(dtype) = device_dtypes[1].dtype && dtype != TorchDtype::int64 {
            return Err(MiscInputError::IndexDtypeNotI64 {}.into());
        }
    Ok(Some(TorchDeviceDtypeOp {
        device: device_dtypes[0].device.or(device_dtypes[1].device),
        dtype: device_dtypes[0].dtype,
    }))
}

impl SpecTrait for GeneralFunctionIndexSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(uuid!("442fde55-a1b7-4a69-98ff-bd40d7030ef2").as_bytes()); // uuid for Index
        hasher.update(&self.index_dim.to_le_bytes());
        hasher.update(&[
            self.batch_x as u8,
            self.batch_index as u8,
            self.check_index_ints as u8,
        ]);
        *hasher.finalize().as_bytes()
    }

    fn function(&self, tensors: &[Tensor]) -> Result<Tensor> {
        let tensors = upcast_tensor_devices(tensors);
        Python::with_gil(|py| {
            Ok(PY_UTILS
                .gen_index_function
                .call(
                    py,
                    PyTuple::new(
                        py,
                        tensors
                            .iter()
                            .map(|x| x.clone().into_py(py))
                            .chain([
                                self.index_dim.into_py(py),
                                self.batch_x.into_py(py),
                                self.batch_index.into_py(py),
                                self.check_index_ints.into_py(py),
                            ])
                            .collect::<Vec<_>>(),
                    ),
                    None,
                )
                .context("evaluate gen index")?
                .extract(py)?)
        })
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        let (x_shape, index_shape) = if let [x_shape, index_shape] = shapes {
            (x_shape, index_shape)
        } else {
            bail!(GeneralFunctionShapeError::WrongNumShapes {
                got: shapes.len(),
                expected: 2
            });
        };

        // TODO: improve errors as needed
        let get_err = || GeneralFunctionShapeError::IndexShapeInvalid {
            x_shape: x_shape.clone(),
            index_shape: index_shape.clone(),
            batch_x: self.batch_x,
        };

        if self.batch_x && self.batch_index {
            let prefix_len = index_shape.len();
            if prefix_len >= x_shape.len() {
                // condition to ensure that suffix len >= 1
                bail!(get_err())
            }

            if !shape_eq_if_known(&x_shape[..prefix_len], &index_shape[..]) {
                bail!(get_err())
            }

            let suffix_len = x_shape.len() - prefix_len;
            assert!(suffix_len >= 1);
            let final_index_dim = check_canon_idxs(suffix_len, &[self.index_dim])
                .context("index dim out of bounds for 'suffix'")?[0]
                + prefix_len;

            Ok(GeneralFunctionShapeInfo {
                shape: x_shape[..final_index_dim]
                    .iter()
                    .chain(&x_shape[final_index_dim + 1..])
                    .cloned()
                    .collect(),
                num_non_batchable_output_dims: (suffix_len - 1) as u8, // sub 1 for indexed
                input_batchability: vec![true, true].into_iter().collect(),
            })
        } else if self.batch_index {
            let index_dim = check_canon_idxs(x_shape.len(), &[self.index_dim])
                .context("index dim out of bounds for x_shape")?[0];

            Ok(GeneralFunctionShapeInfo {
                shape: index_shape
                    .iter()
                    .chain(&x_shape[..index_dim])
                    .chain(&x_shape[index_dim + 1..])
                    .cloned()
                    .collect(),
                num_non_batchable_output_dims: (x_shape.len() - 1) as u8, // sub 1 for indexed
                input_batchability: vec![false, true].into_iter().collect(),
            })
        } else {
            if self.batch_x && self.index_dim >= 0 {
                bail!("index dim must be negative if you're only batching over x");
            }
            let index_dim = check_canon_idxs(x_shape.len(), &[self.index_dim])
                .context("index dim out of bounds for x_shape")?[0];

            let shape: Shape = x_shape[..index_dim]
                .iter()
                .chain(index_shape)
                .chain(&x_shape[index_dim + 1..])
                .cloned()
                .collect();
            let lenshape = shape.len();

            Ok(GeneralFunctionShapeInfo {
                shape,
                num_non_batchable_output_dims: if self.batch_x {
                    index_shape.len() + x_shape[index_dim + 1..].len()
                } else {
                    lenshape
                } as u8,
                input_batchability: vec![self.batch_x, false].into_iter().collect(),
            })
        }
    }

    // fn has_jacobian(&self) -> Result<bool> {
    //     Ok(self.get_jacobians.is_some())
    // }
    // fn get_jacobians(&self, func: &GeneralFunction) -> Result<Option<Vec<Circuit>>> {}
    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Result<Option<TorchDeviceDtypeOp>> {
        index_get_device_dtype_override(device_dtypes)
    }
    fn name(&self) -> &'static str {
        Name::new(&format!(
            "gen_index_at_{}{}{}{}",
            self.index_dim,
            if self.batch_x { "_batch_x" } else { "" },
            if !self.batch_index {
                "_no_batch_index"
            } else {
                ""
            },
            if self.check_index_ints { "_c" } else { "" }
        ))
        .into()
    }
    fn is_official(&self) -> bool {
        true
    }
    fn serialize(&self) -> Result<String> {
        Ok(self.name().into())
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GeneralFunctionExplicitIndexSpec {
    #[pyo3(get)]
    index_dim: i64,
    #[pyo3(get)]
    x_non_batch_dims: usize,
    #[pyo3(get)]
    check_index_ints: bool,
}

simple_from!(
    |x: GeneralFunctionExplicitIndexSpec| -> GeneralFunctionSpec {
        GeneralFunctionSpec::ExplicitIndex(x)
    }
);

impl ToPyObject for GeneralFunctionExplicitIndexSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

impl GeneralFunctionExplicitIndexSpec {
    fn canon_index_dim(&self) -> Result<usize> {
        check_canon_idxs(self.x_non_batch_dims, &[self.index_dim])
            .with_context(|| {
                format!(
                    "index_dim={} out of bounds for x_non_batch_dims={}",
                    self.index_dim, self.x_non_batch_dims
                )
            })
            .map(|x| x[0])
    }

    pub fn new(index_dim: i64, x_non_batch_dims: usize, check_index_ints: bool) -> Result<Self> {
        let out = Self {
            index_dim,
            x_non_batch_dims,
            check_index_ints,
        };

        out.canon_index_dim()?; // check error

        Ok(out)
    }
}

impl SpecTrait for GeneralFunctionExplicitIndexSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(uuid!("442fde55-a1b7-4a69-98ff-bd40d7030ef2").as_bytes()); // uuid for Index
        hasher.update(&self.index_dim.to_le_bytes());
        hasher.update(&self.x_non_batch_dims.to_le_bytes());
        hasher.update(&[self.check_index_ints as u8]);
        *hasher.finalize().as_bytes()
    }

    fn function(&self, tensors: &[Tensor]) -> Result<Tensor> {
        Python::with_gil(|py| {
            Ok(PY_UTILS
                .explicit_gen_index_function
                .call(
                    py,
                    PyTuple::new(
                        py,
                        tensors
                            .iter()
                            .map(|x| x.clone().into_py(py))
                            .chain([
                                self.index_dim.into_py(py),
                                self.x_non_batch_dims.into_py(py),
                                self.check_index_ints.into_py(py),
                            ])
                            .collect::<Vec<_>>(),
                    ),
                    None,
                )
                .context("evaluate explicit gen index")?
                .extract(py)?)
        })
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        let (x_shape, index_shape) = if let [x_shape, index_shape] = shapes {
            (x_shape, index_shape)
        } else {
            bail!(GeneralFunctionShapeError::WrongNumShapes {
                got: shapes.len(),
                expected: 2
            });
        };

        // TODO: improve errors as needed
        let get_err = || GeneralFunctionShapeError::ExplicitIndexShapeInvalid {
            x_shape: x_shape.clone(),
            index_shape: index_shape.clone(),
            index_dim: self.index_dim,
            x_non_batch_dims: self.x_non_batch_dims,
        };

        assert!(self.x_non_batch_dims >= 1);
        if x_shape.len() < self.x_non_batch_dims {
            // condition to ensure that x suffix len >= 1
            bail!(get_err())
        }

        let batch_len = x_shape.len() - self.x_non_batch_dims;

        if index_shape.len() < batch_len {
            bail!(get_err())
        }

        if !shape_eq_if_known(&x_shape[..batch_len], &index_shape[..batch_len]) {
            bail!(get_err())
        }

        let final_index_dim = self.canon_index_dim().unwrap() + batch_len;

        let shape: Shape = index_shape
            .iter()
            .chain(&x_shape[batch_len..final_index_dim])
            .chain(&x_shape[final_index_dim + 1..])
            .cloned()
            .collect();
        let non_batch = shape.len() - batch_len;
        Ok(GeneralFunctionShapeInfo {
            shape,
            num_non_batchable_output_dims: non_batch as u8,
            input_batchability: vec![true, true].into_iter().collect(),
        })
    }

    // fn has_jacobian(&self) -> Result<bool> {
    //     Ok(self.get_jacobians.is_some())
    // }
    // fn get_jacobians(&self, func: &GeneralFunction) -> Result<Option<Vec<Circuit>>> {}
    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Result<Option<TorchDeviceDtypeOp>> {
        index_get_device_dtype_override(device_dtypes)
    }
    fn name(&self) -> &'static str {
        Name::new(&format!(
            "explicit_index_at_{}_x_non_b_{}{}",
            self.index_dim,
            self.x_non_batch_dims,
            if self.check_index_ints { "_c" } else { "" }
        ))
        .into()
    }
    fn is_official(&self) -> bool {
        true
    }
    fn serialize(&self) -> Result<String> {
        Ok(self.name().into())
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GeneralFunctionSetDDSpec {
    #[pyo3(get)]
    input_required_compatibility: TorchDeviceDtypeOp,
    #[pyo3(get)]
    output: TorchDeviceDtypeOp,
}

simple_from!(|x: GeneralFunctionSetDDSpec| -> GeneralFunctionSpec {
    GeneralFunctionSpec::SetDD(x)
});

impl ToPyObject for GeneralFunctionSetDDSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

impl SpecTrait for GeneralFunctionSetDDSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        self.input_required_compatibility.hash(&mut hasher);
        self.output.hash(&mut hasher);
        *hasher.finalize().as_bytes()
    }

    fn function(&self, tensors: &[Tensor]) -> Result<Tensor> {
        pycall!(
            PY_UTILS.cast_tensor,
            (tensors[0].clone(), self.output),
            anyhow
        )
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        if shapes.len() != 1 {
            bail!(GeneralFunctionShapeError::WrongNumShapes {
                got: shapes.len(),
                expected: 1
            });
        }
        Ok(GeneralFunctionShapeInfo {
            shape: shapes[0].clone(),
            num_non_batchable_output_dims: 0,
            input_batchability: vec![true],
        })
    }
    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Result<Option<TorchDeviceDtypeOp>> {
        Ok(Some(
            self.input_required_compatibility
                .combine(device_dtypes[0])
                .map_err(|_e| {
                    anyhow!(MiscInputError::CastIncompatibleDeviceDtype {
                        required: self.input_required_compatibility,
                        actual: device_dtypes[0],
                    })
                })
                .map(|_| self.output.override_other(device_dtypes[0]))?,
        ))
    }

    // fn has_jacobian(&self) -> Result<bool> {
    //     Ok(self.get_jacobians.is_some())
    // }
    // fn get_jacobians(&self, func: &GeneralFunction) -> Result<Option<Vec<Circuit>>> {}

    fn name(&self) -> &'static str {
        Name::new(&format!(
            "cast_from_{:?}_to_{:?}",
            self.input_required_compatibility, self.output
        ))
        .into()
    }
    fn serialize(&self) -> Result<String> {
        Ok(self.name().to_owned())
    }
}

#[pyclass]
#[derive(Debug, Clone, Copy)]
pub enum PairwiseType {
    Pow,
    Minimum,
    Maximum,
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GeneralFunctionPairwiseSpec {
    pairwise_type: PairwiseType,
}

simple_from!(|x: GeneralFunctionPairwiseSpec| -> GeneralFunctionSpec {
    GeneralFunctionSpec::Pairwise(x)
});

/// NOTE: expanding/batching doesn't nicely handle this (in the way it nicely handles add)
/// More generally, we have poor general func support for expand/batch
#[pyfunction]
#[pyo3(signature=(shapes, special_case_ones = true))]
pub fn get_shape_info_broadcast(
    shapes: Vec<Shape>,
    special_case_ones: bool,
) -> Result<GeneralFunctionShapeInfo> {
    let shape = broadcast_shapes_impl(&shapes, special_case_ones)?;

    Ok(GeneralFunctionShapeInfo {
        num_non_batchable_output_dims: shapes
            .iter()
            .filter_map(|s| {
                // only check batching dims
                (s.len() == shape.len()).then(|| {
                    s.iter()
                        .zip(&shape)
                        .rev()
                        .enumerate()
                        .filter_map(|(i, (size, broadcast_size))| {
                            (size != broadcast_size).then_some(i + 1)
                        })
                        .max()
                        .unwrap_or(0)
                })
            })
            .max()
            .unwrap_or(0) as u8,
        input_batchability: shapes.iter().map(|s| s.len() == shape.len()).collect(),
        shape,
    })
}

impl ToPyObject for GeneralFunctionPairwiseSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

impl SpecTrait for GeneralFunctionPairwiseSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(uuid!("6b8f667c-7fa2-40e3-9822-c3b9797549bd").as_bytes()); // uuid for pairwise
        hasher.update(&[self.pairwise_type as u8]);
        *hasher.finalize().as_bytes()
    }

    fn function(&self, tensors: &[Tensor]) -> Result<Tensor> {
        Python::with_gil(|py| {
            let func = match self.pairwise_type {
                PairwiseType::Pow => &PY_UTILS.pow,
                PairwiseType::Minimum => &PY_UTILS.minimum,
                PairwiseType::Maximum => &PY_UTILS.maximum,
            };
            let out = func.call1(py, (tensors[0].clone(), tensors[1].clone()));
            Ok(out
                .context(format!("evaluate pairwise type={:?}", self.pairwise_type))?
                .extract(py)
                .unwrap())
        })
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        if shapes.len() != 2 {
            bail!(GeneralFunctionShapeError::WrongNumShapes {
                got: shapes.len(),
                expected: 2
            });
        }
        get_shape_info_broadcast(shapes.to_vec(), true)
    }

    fn name(&self) -> &'static str {
        match self.pairwise_type {
            PairwiseType::Pow => "pow",
            PairwiseType::Minimum => "minimum",
            PairwiseType::Maximum => "maximum",
        }
    }

    fn is_official(&self) -> bool {
        true
    }

    fn serialize(&self) -> Result<String> {
        Ok(self.name().to_owned())
    }
}

#[pyfunction]
pub fn pow(base: CircuitRc, exponent: CircuitRc, name: Option<Name>) -> Result<GeneralFunction> {
    GeneralFunction::try_new(
        vec![base, exponent],
        GeneralFunctionSpec::Pairwise(GeneralFunctionPairwiseSpec {
            pairwise_type: PairwiseType::Pow,
        }),
        name,
    )
}

#[pyfunction]
pub fn minimum(
    base: CircuitRc,
    exponent: CircuitRc,
    name: Option<Name>,
) -> Result<GeneralFunction> {
    GeneralFunction::try_new(
        vec![base, exponent],
        GeneralFunctionSpec::Pairwise(GeneralFunctionPairwiseSpec {
            pairwise_type: PairwiseType::Minimum,
        }),
        name,
    )
}

#[pyfunction]
pub fn maximum(
    base: CircuitRc,
    exponent: CircuitRc,
    name: Option<Name>,
) -> Result<GeneralFunction> {
    GeneralFunction::try_new(
        vec![base, exponent],
        GeneralFunctionSpec::Pairwise(GeneralFunctionPairwiseSpec {
            pairwise_type: PairwiseType::Maximum,
        }),
        name,
    )
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GeneralFunctionMultinomialSpec {
    #[pyo3(get)]
    replacement: bool,
    shape: Shape,
}

#[pymethods]
impl GeneralFunctionMultinomialSpec {
    #[getter]
    #[pyo3(name = "shape")]
    fn py_shape(&self) -> PySymShape {
        PySymShape(self.shape.clone())
    }
}

simple_from!(|x: GeneralFunctionMultinomialSpec| -> GeneralFunctionSpec {
    GeneralFunctionSpec::Multinomial(x)
});

impl ToPyObject for GeneralFunctionMultinomialSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

fn sample_multinomial(
    probs: Tensor,
    shape: Shape,
    replacement: bool,
    seed_tensor: Tensor,
) -> Result<Tensor, PyErr> {
    Python::with_gil(|py| {
        PY_UTILS
            .random_indices
            .call(py, (probs, shape.clone(), replacement, seed_tensor), None)?
            .extract::<Tensor>(py)
    })
}

impl SpecTrait for GeneralFunctionMultinomialSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(uuid!("1f39ec5e-d3f8-4706-b075-1612fd83eef8").as_bytes());
        hasher.update(&[self.replacement as u8]);
        for l in &self.shape {
            hasher.update(&l.to_le_bytes());
        }
        *hasher.finalize().as_bytes()
    }

    fn function(&self, tensors: &[Tensor]) -> Result<Tensor> {
        let tensors = upcast_tensor_devices(tensors);
        Ok(sample_multinomial(
            tensors[0].clone(),
            self.shape.clone(),
            self.replacement,
            tensors[1].clone(),
        )?)
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        if shapes.len() != 2 {
            bail!(GeneralFunctionShapeError::WrongNumShapes {
                got: shapes.len(),
                expected: 2
            });
        }

        let (probs_shape, seed_shape) = (&shapes[0], &shapes[1]);
        // TODO: improve
        if !seed_shape.is_empty() {
            bail!("seed input must be zero-dim (got shape={seed_shape:?})")
        }
        if probs_shape.is_empty() {
            bail!("probs must be >=1d")
        }

        Ok(GeneralFunctionShapeInfo {
            shape: probs_shape[..probs_shape.len() - 1]
                .iter()
                .chain(&self.shape)
                .cloned()
                .collect(),
            num_non_batchable_output_dims: self.shape.len() as u8,
            input_batchability: vec![false, false], /* note: batching over probs has right shape, but due to rng, doesn't keep values correctly */
        })
    }

    fn name(&self) -> &'static str {
        "multinomial"
    }

    fn is_official(&self) -> bool {
        true
    }

    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Result<Option<TorchDeviceDtypeOp>> {
        let (probs_dd, seed_dd) = (device_dtypes[0], device_dtypes[1]);
        if probs_dd
            .dtype
            .map(|dtype| !dtype.is_floating_point())
            .unwrap_or(false)
        {
            bail!("probs dtype not floating point")
        }
        if seed_dd
            .dtype
            .map(|dtype| dtype != TorchDtype::int64)
            .unwrap_or(false)
        {
            bail!("seed should be int64 (we could support other integers if we wanted)")
        }
        if seed_dd
            .device
            .map(|device| device != TorchDevice::Cpu)
            .unwrap_or(false)
        {
            bail!("seed should be on cpu (for now at least)")
        }

        Ok(Some(TorchDeviceDtypeOp {
            device: probs_dd.device,
            dtype: Some(TorchDtype::int64),
        }))
    }

    fn serialize(&self) -> Result<String> {
        Ok(format!(
            "multinomial{}_{:?}",
            if !self.replacement { "_no_replace" } else { "" },
            self.shape
        ))
    }
}

#[pyfunction]
#[pyo3(signature=(probs, seed, shape, replacement = true, name = None))]
pub fn multinomial(
    probs: CircuitRc,
    seed: CircuitRc,
    shape: Shape,
    replacement: bool,
    name: Option<Name>,
) -> Result<GeneralFunction> {
    GeneralFunction::try_new(
        vec![probs, seed],
        GeneralFunctionMultinomialSpec { replacement, shape }.into(),
        name,
    )
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GeneralFunctionAlreadySampledMultinomialSpec {
    shape: Shape,
}

#[pymethods]
impl GeneralFunctionAlreadySampledMultinomialSpec {
    #[getter]
    #[pyo3(name = "shape")]
    fn py_shape(&self) -> PySymShape {
        PySymShape(self.shape.clone())
    }
}

simple_from!(
    |x: GeneralFunctionAlreadySampledMultinomialSpec| -> GeneralFunctionSpec {
        GeneralFunctionSpec::AlreadySampledMultinomial(x)
    }
);

impl ToPyObject for GeneralFunctionAlreadySampledMultinomialSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

fn compute_already_sampled_multinomial(
    weights: Tensor,
    exponentially_distributed_vals: Tensor,
    shape: Shape,
) -> Result<Tensor, PyErr> {
    Python::with_gil(|py| {
        PY_UTILS
            .already_sampled_multinomial
            .call(
                py,
                (weights, exponentially_distributed_vals, shape.clone()),
                None,
            )?
            .extract::<Tensor>(py)
    })
}

impl SpecTrait for GeneralFunctionAlreadySampledMultinomialSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(uuid!("f1502696-ea6e-46ab-9f62-c1912684eabe").as_bytes());
        for l in &self.shape {
            hasher.update(&l.to_le_bytes());
        }
        *hasher.finalize().as_bytes()
    }

    fn function(&self, tensors: &[Tensor]) -> Result<Tensor> {
        Ok(compute_already_sampled_multinomial(
            tensors[0].clone(),
            tensors[1].clone(),
            self.shape.clone(),
        )?)
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        if shapes.len() != 2 {
            bail!(GeneralFunctionShapeError::WrongNumShapes {
                got: shapes.len(),
                expected: 2
            });
        }
        let info = get_shape_info_broadcast(shapes.to_vec(), true)
            .context("probs and exponential vals didn't broadcast")?;

        Ok(GeneralFunctionShapeInfo {
            shape: info.shape[..info.shape.len() - 1]
                .iter()
                .chain(&self.shape)
                .cloned()
                .collect(),
            num_non_batchable_output_dims: self.shape.len() as u8,
            input_batchability: vec![true, true],
        })
    }

    fn name(&self) -> &'static str {
        "a_samp_multinomial"
    }

    fn is_official(&self) -> bool {
        true
    }

    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Result<Option<TorchDeviceDtypeOp>> {
        let (probs_dd, exponential_dd) = (device_dtypes[0], device_dtypes[1]);
        if probs_dd
            .dtype
            .map(|dtype| !dtype.is_floating_point())
            .unwrap_or(false)
        {
            bail!("probs dtype not floating point");
        }
        if exponential_dd
            .dtype
            .map(|dtype| !dtype.is_floating_point())
            .unwrap_or(false)
        {
            bail!("exponential dtype not floating point");
        }

        if let Some(probs_dev) = probs_dd.device {
            if let Some(exponential_dev) = exponential_dd.device {
                if probs_dev != exponential_dev {
                    bail!("probs and exponential dtypes different");
                }
            }
        }

        Ok(Some(TorchDeviceDtypeOp {
            device: probs_dd.device.or(exponential_dd.device),
            dtype: Some(TorchDtype::int64),
        }))
    }

    fn serialize(&self) -> Result<String> {
        Ok(format!("a_samp_multinomial_{:?}", self.shape))
    }
}

#[pyfunction]
#[pyo3(signature=(probs, exponentially_distributed_vals, shape,  name = None))]
pub fn already_sampled_multinomial(
    probs: CircuitRc,
    exponentially_distributed_vals: CircuitRc,
    shape: Shape,
    name: Option<Name>,
) -> Result<GeneralFunction> {
    GeneralFunction::try_new(
        vec![probs, exponentially_distributed_vals],
        GeneralFunctionSpec::AlreadySampledMultinomial(
            GeneralFunctionAlreadySampledMultinomialSpec { shape },
        ),
        name,
    )
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GeneralFunctionTopKSpec {
    shape: Shape,
}

#[pymethods]
impl GeneralFunctionTopKSpec {
    #[getter]
    #[pyo3(name = "shape")]
    fn py_shape(&self) -> PySymShape {
        PySymShape(self.shape.clone())
    }
}

simple_from!(|x: GeneralFunctionTopKSpec| -> GeneralFunctionSpec { GeneralFunctionSpec::TopK(x) });

impl ToPyObject for GeneralFunctionTopKSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

fn compute_top_k(vals: Tensor, shape: Shape) -> Result<Tensor, PyErr> {
    Python::with_gil(|py| {
        PY_UTILS
            .top_k
            .call(py, (vals, shape.clone()), None)?
            .extract::<Tensor>(py)
    })
}

impl SpecTrait for GeneralFunctionTopKSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(uuid!("b2b7c45b-658a-4df0-9a8a-20650978c94e").as_bytes());
        for l in &self.shape {
            hasher.update(&l.to_le_bytes());
        }
        *hasher.finalize().as_bytes()
    }

    fn function(&self, tensors: &[Tensor]) -> Result<Tensor> {
        Ok(compute_top_k(tensors[0].clone(), self.shape.clone())?)
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        if shapes.len() != 1 {
            bail!(GeneralFunctionShapeError::WrongNumShapes {
                got: shapes.len(),
                expected: 1
            });
        }

        Ok(GeneralFunctionShapeInfo {
            shape: shapes[0][..shapes[0].len() - 1]
                .iter()
                .chain(&self.shape)
                .cloned()
                .collect(),
            num_non_batchable_output_dims: self.shape.len() as u8,
            input_batchability: vec![true],
        })
    }

    fn name(&self) -> &'static str {
        "top_k"
    }

    fn is_official(&self) -> bool {
        true
    }

    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Result<Option<TorchDeviceDtypeOp>> {
        Ok(Some(TorchDeviceDtypeOp {
            device: device_dtypes[0].device,
            dtype: Some(TorchDtype::int64),
        }))
    }

    fn serialize(&self) -> Result<String> {
        Ok(format!("top_k_{:?}", self.shape))
    }
}

#[pyfunction]
#[pyo3(signature=(values,  shape,  name = None))]
pub fn top_k(values: CircuitRc, shape: Shape, name: Option<Name>) -> Result<GeneralFunction> {
    GeneralFunction::try_new(
        vec![values],
        GeneralFunctionSpec::TopK(GeneralFunctionTopKSpec { shape }),
        name,
    )
}

#[pyclass]
#[derive(Debug, Clone)]
/// used internally to optimize & evaluate multiple circuits at once
pub struct GeneralFunctionOutputSpec();

simple_from!(|x: GeneralFunctionOutputSpec| -> GeneralFunctionSpec {
    GeneralFunctionSpec::Output(x)
});

impl SpecTrait for GeneralFunctionOutputSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(uuid!("b79f926e-431d-47dc-a571-182c01eda8c9").as_bytes());
        *hasher.finalize().as_bytes()
    }

    fn function(&self, _tensors: &[Tensor]) -> Result<Tensor> {
        bail!("Shouldn't happen: attempt to evaluate GeneralFunction Output")
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        Ok(GeneralFunctionShapeInfo {
            shape: sv![],
            num_non_batchable_output_dims: 0,
            input_batchability: shapes.iter().map(|_| false).collect(),
        })
    }

    fn name(&self) -> &'static str {
        "Output"
    }

    fn serialize(&self) -> Result<String> {
        Ok("Output".to_owned())
    }

    fn should_const_fold(&self, _self_circ: &GeneralFunction) -> bool {
        false
    }
}

impl ToPyObject for GeneralFunctionOutputSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

enum PyModuleLocator {
    Path(String),
    Module(String),
}

impl PyModuleLocator {
    fn parse(s: String) -> Self {
        if s.starts_with('/') && s.ends_with(".py") {
            PyModuleLocator::Path(s)
        } else {
            PyModuleLocator::Module(s)
        }
    }

    fn get_module<'py>(&self, py: Python<'py>) -> Result<&'py PyAny> {
        match self {
            PyModuleLocator::Path(path) => {
                let rrfs_dir = rr_util::rrfs::get_rrfs_dir();

                // adapted from https://stackoverflow.com/questions/67631/how-can-i-import-a-module-dynamically-given-the-full-path

                let importlib_util = py.import("importlib.util")?;
                let spec = importlib_util
                    .call_method1("spec_from_file_location", ("user_funcs", rrfs_dir + path))?;
                let function_spec_module =
                    importlib_util.call_method1("module_from_spec", (spec,))?;
                spec.getattr("loader")?
                    .call_method1("exec_module", (function_spec_module,))?;
                Ok(function_spec_module)
            }
            PyModuleLocator::Module(module) => Ok(py.import(&**module)?),
        }
    }
}

struct PyClassLocator {
    module: PyModuleLocator,
    name: String,
}

impl PyClassLocator {
    fn parse(s: &str) -> Result<Self> {
        (|| -> Result<Self> {
            let mut split = s.splitn(2, ':');
            let file_path_or_module = convert_op_str_to_format_err(split.next(), s)?;
            let spec_name = convert_op_str_to_format_err(split.next(), s)?;
            Ok(PyClassLocator {
                module: PyModuleLocator::parse(file_path_or_module),
                name: spec_name,
            })
        })().context(
            "Function locator must either be of the form module.to.import:MyCustomSpec or /dir/sub_dir/.../file.py:MyCustomSpec (path relative to rrfs)"
        )
    }

    fn get_class<'py>(&self, py: Python<'py>) -> Result<&'py PyAny> {
        Ok(self.module.get_module(py)?.getattr(&*self.name)?)
    }
}

#[derive(Clone)]
pub struct PyWrap {
    ob: PyObject,
    hash: HashBytes,
    name: Name, // only used for autonaming
    path: Name,
}

impl fmt::Debug for PyWrap {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("PyWrap")
            .field("ob", &self.ob)
            .field("name", &self.name)
            .field("path", &self.path)
            .finish_non_exhaustive()
    }
}

simple_from!(|x: PyWrap| -> GeneralFunctionSpec { GeneralFunctionSpec::Py(Box::new(x)) });

pub static PY_WRAP_BASE: GILLazyPy<PyObject> =
    GILLazyPy::new_py(|py| SELF_MODULE.getattr(py, "GeneralFunctionSpecBase").unwrap());

fn extract_py_generalfunction<'source>(
    base: &PyObject,
    base_uuid: Uuid,
    ob: &'source PyAny,
) -> PyResult<(Name, Name, PyObject, HashBytes)> {
    let ob: PyObject = ob.into();
    let mut hasher = blake3::Hasher::new();
    if !Python::with_gil(|py| ob.as_ref(py).is_instance(base.as_ref(py)))
        .context("calling isinstance failed")?
    {
        let err: anyhow::Error = ConstructError::GeneralFunctionPyNotInstance { ob }.into();
        return Err(err.into());
    }

    let name: String =
        Python::with_gil(|py| -> Result<_> { Ok(ob.getattr(py, "name")?.extract(py)?) })?;

    if name.contains(" at ") {
        return Err(anyhow!("Function names can't contain the substring ` at ` because it could interfere with parsing.").into());
    }

    let path: String =
        Python::with_gil(|py| -> Result<_> { Ok(ob.getattr(py, "path")?.extract(py)?) })?;

    PyClassLocator::parse(&path)?;

    let name: Name = name.into();
    let path: Name = path.into();

    hasher.update(base_uuid.as_bytes());
    hasher.update(&name.0.get().to_le_bytes());
    hasher.update(&path.0.get().to_le_bytes());
    let bytes: Vec<u8> = Python::with_gil(|py| -> Result<_> {
        Ok(ob.call_method0(py, "compute_hash_bytes")?.extract(py)?)
    })?;
    hasher.update(&bytes);

    Ok((name, path, ob, *hasher.finalize().as_bytes()))
}

impl<'source> pyo3::FromPyObject<'source> for Box<PyWrap> {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        let (name, path, ob, hash) = extract_py_generalfunction(
            &*PY_WRAP_BASE,
            uuid!("de3124ee-154c-4da8-bdb3-b7496ae6223c"),
            ob,
        )?;

        Ok(Box::new(PyWrap {
            name,
            path,
            ob,
            hash,
        }))
    }
}

impl ToPyObject for Box<PyWrap> {
    fn to_object(&self, _py: Python<'_>) -> PyObject {
        self.ob.clone()
    }
}

impl SpecTrait for Box<PyWrap> {
    fn compute_hash(&self) -> HashBytes {
        self.hash
    }

    fn function(&self, tensors: &[Tensor]) -> Result<Tensor> {
        Python::with_gil(|py| {
            Ok(self
                .ob
                .call_method1(
                    py,
                    "function",
                    PyTuple::new(py, tensors.iter().map(|x| x.clone().into_py(py))),
                )?
                .extract(py)?)
        })
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        Python::with_gil(|py| {
            Ok(self
                .ob
                .call_method1(
                    py,
                    "get_shape_info",
                    PyTuple::new(py, shapes.iter().map(|x| shape_to_py(x))),
                )?
                .extract(py)?)
        })
    }

    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Result<Option<TorchDeviceDtypeOp>> {
        Python::with_gil(|py| {
            let x = self.ob.call_method1(
                py,
                "get_device_dtype_override",
                PyTuple::new(py, device_dtypes.iter().map(|x| x.into_py(py))),
            )?;
            Ok(x.extract::<Option<TorchDeviceDtypeOp>>(py)?)
        })
    }
    fn name(&self) -> &'static str {
        self.name.into()
    }
    fn serialize(&self) -> Result<String> {
        let extra = Python::with_gil(|py| -> Result<_> {
            Ok(self
                .ob
                .call_method1(py, "serialize_data", ())?
                .extract::<Option<String>>(py)?)
        })?;
        match extra {
            Some(extra) => Ok(format!("{}({})", self.path, extra)),
            None => Ok(self.path.into()),
        }
    }
    fn should_const_fold(&self, self_circ: &GeneralFunction) -> bool {
        Python::with_gil(|py| {
            self.ob
                .call_method1(py, "should_const_fold", (self_circ.crc(),))?
                .extract::<bool>(py)
        })
        .with_context(|| {
            format!("python GeneralFunction should_const_fold failed for circuit {self_circ:?}")
        })
        .unwrap()
    }
}

#[derive(Clone)]
pub struct PyWrapMultiOutput {
    ob: PyObject,
    hash: HashBytes,
    name: Name,
    path: Name,
}

impl_eq_by_big_hash!(PyWrapMultiOutput);

impl EqByBigHash for PyWrapMultiOutput {
    fn hash(&self) -> [u8; 32] {
        self.hash
    }
}

impl fmt::Debug for PyWrapMultiOutput {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("PyWrapMultiOutput")
            .field("ob", &self.ob)
            .field("name", &self.name)
            .field("path", &self.path)
            .finish_non_exhaustive()
    }
}

pub static PY_WRAP_MULTI_OUTPUT_BASE: GILLazyPy<PyObject> = GILLazyPy::new_py(|py| {
    SELF_MODULE
        .getattr(py, "MultiOutputGeneralFunctionSpecBase")
        .unwrap()
});

impl<'source> pyo3::FromPyObject<'source> for PyWrapMultiOutput {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        let (name, path, ob, hash) = extract_py_generalfunction(
            &*PY_WRAP_MULTI_OUTPUT_BASE,
            uuid!("cbb32067-ca14-4e6e-a938-212dc2f3eced"),
            ob,
        )?;

        Ok(PyWrapMultiOutput {
            name,
            path,
            ob,
            hash,
        })
    }
}

impl ToPyObject for Box<PyWrapMultiOutput> {
    fn to_object(&self, _py: Python<'_>) -> PyObject {
        self.ob.clone()
    }
}

impl PyWrapMultiOutput {
    fn compute_hash(&self) -> HashBytes {
        self.hash
    }

    pub fn function(&self, tensors: &[Tensor]) -> Result<Vec<Tensor>> {
        Python::with_gil(|py| {
            Ok(self
                .ob
                .call_method1(
                    py,
                    "function",
                    PyTuple::new(py, tensors.iter().map(|x| x.clone().into_py(py))),
                )?
                .extract(py)?)
        })
    }

    pub fn get_shape_info(&self, shapes: &[Shape]) -> Result<Vec<GeneralFunctionShapeInfo>> {
        let si: Vec<GeneralFunctionShapeInfo> = Python::with_gil(|py| -> Result<_> {
            Ok(self
                .ob
                .call_method1(
                    py,
                    "get_shape_info",
                    PyTuple::new(py, shapes.iter().map(|x| shape_to_py(x))),
                )?
                .extract(py)?)
        })?;

        si.iter().try_for_each(|x| x.validate(&shapes).with_context(|| {
            format!(
                "invalid shape info in new with spec={:?} input_shapes={:?} (likely input shape error)",
                self,
                shapes,
            )
        }))?;

        let input_batchability = si[0].input_batchability.clone();
        for s in si.iter().skip(1) {
            if s.input_batchability != input_batchability {
                bail!("multi-output generalfunction: input_batchability must be the same across outputs")
            }
        }
        if input_batchability.iter().any(|x| *x) {
            let batch_shape = si[0].batch_shape();
            for s in si.iter().skip(1) {
                if s.batch_shape() != batch_shape {
                    bail!(
                        "multi-output generalfunction: shape[:-num_non_batchable_output_dims] must be the same across outputs"
                    )
                }
            }
        }

        Ok(si)
    }

    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Result<Option<Vec<Option<TorchDeviceDtypeOp>>>> {
        Python::with_gil(|py| {
            let x = self.ob.call_method1(
                py,
                "get_device_dtype_override",
                PyTuple::new(
                    py,
                    device_dtypes
                        .iter()
                        .map(|x| x.into_py(py))
                        .collect::<Vec<_>>(),
                ),
            )?;
            if x.is_none(py) {
                Ok(None)
            } else if let Ok(x) = x.extract::<Vec<Option<TorchDeviceDtypeOp>>>(py) {
                Ok(Some(x))
            } else if let Ok(x) = x.extract::<Option<TorchDeviceDtypeOp>>(py) {
                Ok(Some(vec![x]))
            } else {
                bail!("python GeneralFunction {} get_device_dtype_override must return None, a TorchDeviceDtypeOp, or a list of TorchDeviceDtypeOp but returned {x}", self.name)
            }
        })
    }
    pub fn name(&self) -> &'static str {
        self.name.into()
    }
    fn serialize(&self) -> Result<String> {
        let extra = Python::with_gil(|py| -> Result<_> {
            Ok(self
                .ob
                .call_method1(py, "serialize_data", ())?
                .extract::<Option<String>>(py)?)
        })?;
        match extra {
            Some(extra) => Ok(format!("{}({})", self.path, extra)),
            None => Ok(self.path.into()),
        }
    }
}

#[derive(Debug, Clone, FromPyObject)]
pub enum GeneralFunctionSpec {
    Simple(GeneralFunctionSimpleSpec),
    Index(GeneralFunctionIndexSpec),
    ExplicitIndex(GeneralFunctionExplicitIndexSpec),
    SetDD(GeneralFunctionSetDDSpec),
    Pairwise(GeneralFunctionPairwiseSpec),
    Multinomial(GeneralFunctionMultinomialSpec),
    AlreadySampledMultinomial(GeneralFunctionAlreadySampledMultinomialSpec),
    TopK(GeneralFunctionTopKSpec),
    Output(GeneralFunctionOutputSpec),
    Py(Box<PyWrap>), // boxed bc it was long pole for Circuit size
}

simple_from!(|x: GeneralFunctionSpec| -> GeneralFunctionSpecFull {
    GeneralFunctionSpecFull::SingleOutput(x)
});

#[derive(Debug, Clone)]
pub enum GeneralFunctionSpecFull {
    SingleOutput(GeneralFunctionSpec),
    MultiOutput(Box<PyWrapMultiOutput>, usize),
}

impl IntoPy<PyObject> for GeneralFunctionSpecFull {
    fn into_py(self, py: Python) -> PyObject {
        match self {
            Self::SingleOutput(x) => x.into_py(py),
            Self::MultiOutput(x, _) => x.ob,
        }
    }
}

impl GeneralFunctionSpecFull {
    pub fn name(&self) -> &'static str {
        match self {
            Self::SingleOutput(x) => x.name(),
            Self::MultiOutput(x, _) => x.name(),
        }
    }
    pub fn is_official(&self) -> bool {
        match self {
            Self::SingleOutput(x) => x.is_official(),
            Self::MultiOutput(..) => false,
        }
    }
    pub fn should_const_fold(&self, self_circ: &GeneralFunction) -> bool {
        match self {
            Self::SingleOutput(x) => x.should_const_fold(self_circ),
            Self::MultiOutput(spec, _) => Python::with_gil(|py| {
                spec.ob
                    .call_method1(py, "should_const_fold", (self_circ.crc(),))?
                    .extract::<bool>(py)
            })
            .with_context(|| {
                format!("python GeneralFunction should_const_fold failed for circuit {self_circ:?}")
            })
            .unwrap(),
        }
    }
    pub fn serialize(&self) -> Result<String> {
        match self {
            Self::SingleOutput(x) => Ok(x.serialize()?),
            Self::MultiOutput(x, n) => Ok(format!("output:{n} {}", x.serialize()?,)),
        }
    }
}

impl GeneralFunctionSpec {
    #[inline]
    fn as_trait_obj(&self) -> &dyn SpecTrait {
        match self {
            Self::Simple(x) => x,
            Self::Index(x) => x,
            Self::ExplicitIndex(x) => x,
            Self::SetDD(x) => x,
            Self::Pairwise(x) => x,
            Self::Multinomial(x) => x,
            Self::AlreadySampledMultinomial(x) => x,
            Self::TopK(x) => x,
            Self::Output(x) => x,
            Self::Py(x) => x,
        }
    }
}

impl EqByBigHash for GeneralFunctionSpec {
    fn hash(&self) -> HashBytes {
        self.as_trait_obj().compute_hash()
    }
}

impl_eq_by_big_hash!(GeneralFunctionSpec);

impl ToPyObject for GeneralFunctionSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.as_trait_obj().to_object(py)
    }
}
impl IntoPy<PyObject> for GeneralFunctionSpec {
    fn into_py(self, py: Python<'_>) -> PyObject {
        self.to_object(py)
    }
}

impl SpecTrait for GeneralFunctionSpec {
    fn compute_hash(&self) -> HashBytes {
        self.as_trait_obj().compute_hash()
    }
    fn function(&self, tensors: &[Tensor]) -> Result<Tensor> {
        self.as_trait_obj().function(tensors)
    }
    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        let si = self.as_trait_obj().get_shape_info(shapes)?;

        si.validate(&shapes).with_context(|| {
            format!(
                "invalid shape info in new with spec={:?} input_shapes={:?} (likely input shape error)",
                self,
                shapes
            )
        })?;

        Ok(si)
    }
    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Result<Option<TorchDeviceDtypeOp>> {
        self.as_trait_obj().get_device_dtype_override(device_dtypes)
    }
    // fn has_jacobian(&self) -> Result<bool>;
    // fn get_jacobians(&self, func: &GeneralFunction) -> Result<Option<Vec<Circuit>>>;
    fn name(&self) -> &'static str {
        self.as_trait_obj().name()
    }
    fn is_official(&self) -> bool {
        self.as_trait_obj().is_official()
    }
    fn serialize(&self) -> Result<String> {
        self.as_trait_obj().serialize()
    }
    fn should_const_fold(&self, self_circ: &GeneralFunction) -> bool {
        self.as_trait_obj().should_const_fold(self_circ)
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
#[repr(C)]
pub struct GeneralFunction {
    info: CachedCircuitInfo,
    #[pyo3(get)]
    pub spec: GeneralFunctionSpecFull,
    #[pyo3(get)]
    pub num_non_batchable_output_dims: u8,
    pub input_batchability: Vec<bool>,
    pub multi_output_shapes: Option<Box<Vec<Shape>>>,
}

impl GeneralFunction {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        nodes: Vec<CircuitRc>,
        spec: GeneralFunctionSpec,
        name: Option<Name>,
    ) -> Result<Self> {
        let shapes = nodes
            .iter()
            .map(|x| x.shape().clone())
            .collect::<Vec<Shape>>();

        let si = spec.get_shape_info(&shapes[..]).with_context(|| {
            format!(
                "failed to compute shape info in new with spec={:?} input_shapes={:?}",
                spec,
                nodes
                    .iter()
                    .map(|x| x.shape().clone())
                    .collect::<Vec<Shape>>()
            )
        })?;

        let ddto = spec.get_device_dtype_override(
            &nodes
                .iter()
                .map(|x| x.info().device_dtype)
                .collect::<Vec<_>>(),
        )?;

        Self::new_(nodes, spec.into(), name, si, ddto, None)
    }

    pub fn new_multi_output(
        nodes: Vec<CircuitRc>,
        spec: PyWrapMultiOutput,
        name: Option<Name>,
    ) -> Result<Vec<Self>> {
        let shapes = nodes
            .iter()
            .map(|x| x.shape().clone())
            .collect::<Vec<Shape>>();

        let si = spec.get_shape_info(&shapes[..]).with_context(|| {
            format!(
                "failed to compute shape info in new with spec={:?} input_shapes={:?}",
                spec,
                nodes
                    .iter()
                    .map(|x| x.shape().clone())
                    .collect::<Vec<Shape>>()
            )
        })?;

        let ddtos = spec.get_device_dtype_override(
            &nodes
                .iter()
                .map(|x| x.info().device_dtype)
                .collect::<Vec<_>>(),
        )?;

        let multi_output_shapes = Some(Box::new(si.iter().map(|x| x.shape.clone()).collect()));

        if ddtos.is_some() && ddtos.as_ref().unwrap().len() != si.len() {
            bail!("multi-output generalfunction: device_dtype_override must be None or have the same length as the number of outputs")
        }

        (0..si.len())
            .map(|n| {
                Self::new_(
                    nodes.clone(),
                    GeneralFunctionSpecFull::MultiOutput(Box::new(spec.clone()), n),
                    name,
                    si[n].clone(),
                    ddtos.as_ref().and_then(|x| x[n].clone()),
                    multi_output_shapes.clone(),
                )
            })
            .collect()
    }

    fn new_full(
        nodes: Vec<CircuitRc>,
        spec: GeneralFunctionSpecFull,
        name: Option<Name>,
    ) -> Result<Self> {
        match spec {
            GeneralFunctionSpecFull::SingleOutput(spec) => Self::try_new(nodes, spec, name),
            GeneralFunctionSpecFull::MultiOutput(spec, n) => {
                Ok(Self::new_multi_output(nodes, *spec, name)?[n].clone())
            }
        }
    }

    fn new_(
        nodes: Vec<CircuitRc>,
        spec: GeneralFunctionSpecFull,
        name: Option<Name>,
        shape_info: GeneralFunctionShapeInfo,
        device_dtype_override: Option<TorchDeviceDtypeOp>,
        multi_output_shapes: Option<Box<Vec<Shape>>>,
    ) -> Result<Self> {
        let GeneralFunctionShapeInfo {
            shape,
            num_non_batchable_output_dims,
            input_batchability,
        } = shape_info;

        let out = Self {
            spec,
            info: match device_dtype_override {
                Some(ddt) => CachedCircuitInfo::with_device_dtype(name, shape, nodes, ddt),
                None => CachedCircuitInfo::incomplete(name, shape, nodes)?,
            },
            num_non_batchable_output_dims,
            input_batchability,
            multi_output_shapes,
        };
        out.initial_init_info()
    }

    pub fn evolve(&self, nodes: Vec<CircuitRc>, name: Option<Name>) -> Result<Self> {
        Self::new_full(nodes, self.spec.clone(), name)
    }

    pub fn is_batchable(&self) -> bool {
        self.input_batchability.iter().any(|x| *x)
    }
}

circuit_node_extra_impl!(GeneralFunction, self_hash_default);

impl CircuitNodeComputeInfoImpl for GeneralFunction {}

impl CircuitNodeHashItems for GeneralFunction {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        match &self.spec {
            GeneralFunctionSpecFull::SingleOutput(x) => hasher.update(&x.compute_hash()),
            GeneralFunctionSpecFull::MultiOutput(x, o) => {
                hasher.update(&o.to_le_bytes());
                hasher.update(&x.compute_hash())
            }
        };
    }
}

impl CircuitNode for GeneralFunction {
    circuit_node_auto_impl!("3c655670-b352-4a5f-891c-0d7160609341");

    fn _replace_children(&self, children: Vec<CircuitRc>) -> Result<Self> {
        Self::new_full(children, self.spec.clone(), self.info().name)
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let num_batchable_axes = self.rank() as u8 - self.num_non_batchable_output_dims;
        zip(self.children(), &self.input_batchability)
            .map(|(child, batchable)| {
                if !batchable {
                    vec![None; child.rank()]
                } else {
                    (0..child.rank())
                        .map(|i| match i < num_batchable_axes as usize {
                            true => Some(i),
                            false => None,
                        })
                        .collect()
                }
            })
            .collect()
    }
}

impl CircuitNodeAutoName for GeneralFunction {
    const PRIORITY: OperatorPriority = OperatorPriority::Function {};

    fn auto_name(&self) -> Option<Name> {
        // Never any parenthesis, so we don't even care checking if we need to add some
        // but check out children_names_with_maybe_paren if you change the syntax of the general function
        if self.children().any(|x| x.info().name.is_none()) {
            None
        } else {
            Some(
                (self.spec.name().to_owned()
                    + "("
                    + &self
                        .children()
                        .map(|x| Self::shorten_child_name(x.info().name.unwrap().str()))
                        .collect::<Vec<String>>()
                        .join(", ")
                    + ")")
                    .into(),
            )
        }
    }
}

#[pymethods]
impl GeneralFunction {
    #[new]
    #[pyo3(signature=(*nodes, spec, name = None))]
    fn new_py(
        nodes: Vec<CircuitRc>,
        spec: GeneralFunctionSpec,
        name: Option<Name>,
    ) -> PyResult<PyClassInitializer<GeneralFunction>> {
        let out = GeneralFunction::try_new(nodes, spec, name)?;

        Ok(out.into_init())
    }

    #[getter]
    fn output(&self) -> Option<usize> {
        match &self.spec {
            GeneralFunctionSpecFull::SingleOutput(_) => None,
            GeneralFunctionSpecFull::MultiOutput(_, o) => Some(*o),
        }
    }

    #[staticmethod]
    #[pyo3(signature=(*nodes, spec, name = None), name="new_multi_output")]
    pub fn new_multi_output_py(
        nodes: Vec<CircuitRc>,
        spec: PyObject,
        name: Option<Name>,
    ) -> Result<Vec<Self>> {
        Python::with_gil(|py| {
            let spec: PyWrapMultiOutput = FromPyObject::extract(spec.as_ref(py))?;
            Self::new_multi_output(nodes, spec, name)
        })
    }

    #[staticmethod]
    #[pyo3(signature=(*nodes, parse_string, name = None))]
    pub fn new_from_parse(
        nodes: Vec<CircuitRc>,
        parse_string: String,
        name: Option<Name>,
    ) -> Result<Self> {
        static RE_PY: Lazy<Regex> = Lazy::new(|| {
            Regex::new(&format!(r"(?P<path>(?:(?:{ident}(?:\.{ident})*)|(?:/.+?\.py)):{ident})(?:\((?P<data>.*)\))?", ident="[_a-zA-Z][_a-zA-Z0-9]*")).unwrap()
        });
        if let Some(r) = Self::new_by_name_op(nodes.clone(), &parse_string, name)? {
            Ok(r)
        } else if let Some(inner) = parse_string.strip_prefix("output:") {
            let (num, rest) = inner
                .split_once(" ")
                .context("failed to split output: into num & spec")?;
            let num: usize = num.parse().context("failed to parse output num")?;
            let re_captures = RE_PY
                .captures(rest)
                .context("failed to parse multi-output spec")?;
            let path = re_captures.name("path").unwrap().as_str();
            Ok(if let Some(extra) = re_captures.name("data") {
                Self::new_multi_output_by_path(nodes, path, Some(extra.as_str().to_string()), name)?
                    [num]
                    .clone()
            } else {
                Self::new_multi_output_by_path(nodes, rest, None, name)?[num].clone()
            })
        } else if let Some(re_captures) = RE_PY.captures(&parse_string) {
            let path = re_captures.name("path").unwrap();
            if let Some(extra) = re_captures.name("data") {
                Self::new_by_path(nodes, path.as_str(), Some(extra.as_str().to_owned()), name)
            } else {
                Self::new_by_path(nodes, path.as_str(), None, name)
            }
        } else {
            bail!(ConstructError::UnknownGeneralFunction { parse_string })
        }
    }

    #[staticmethod]
    #[pyo3(signature=(*nodes, spec_name, name = None))]
    pub fn new_by_name(nodes: Vec<CircuitRc>, spec_name: Name, name: Option<Name>) -> Result<Self> {
        Self::new_by_name_op(nodes, &spec_name, name)?.ok_or(
            ConstructError::UnknownGeneralFunction {
                parse_string: spec_name.into(),
            }
            .into(),
        )
    }

    #[staticmethod]
    #[pyo3(signature=(*nodes, spec_name, name = None))]
    pub fn new_by_name_op(
        nodes: Vec<CircuitRc>,
        spec_name: &str,
        name: Option<Name>,
    ) -> Result<Option<Self>> {
        // parse case
        static RE_MULTINOMIAL: Lazy<Regex> = Lazy::new(|| {
            Regex::new(r"^multinomial(_no_replace)?_\[\s*((?:\d+\s*,\s*)*(?:\d+\s*)?)\]$").unwrap()
        });
        static RE_A_SAMP_MULTINOMIAL: Lazy<Regex> = Lazy::new(|| {
            Regex::new(r"^a_samp_multinomial_\[\s*((?:\d+\s*,\s*)*(?:\d+\s*)?)\]$").unwrap()
        });
        static RE_TOP_K: Lazy<Regex> =
            Lazy::new(|| Regex::new(r"^top_k_\[\s*((?:\d+\s*,\s*)*(?:\d+\s*)?)\]$").unwrap());
        static RE_GEN_INDEX: Lazy<Regex> = Lazy::new(|| {
            Regex::new(r"^gen_index_at_(-?\d+)(_batch_x)?(_no_batch_index)?(_c)?$").unwrap()
        });
        static RE_EXPLICIT_INDEX: Lazy<Regex> =
            Lazy::new(|| Regex::new(r"^explicit_index_at_(-?\d+)_x_non_b_(\d+)(_c)?$").unwrap());
        static RE_CAST: Lazy<Regex> = Lazy::new(|| {
            Regex::new(r"^cast_from_\{device:([a-zA-Z0-9:]+),dtype:([a-zA-Z0-9]+)\}_to_\{device:([a-zA-Z0-9:]+),dtype:([a-zA-Z0-9]+)\}$").unwrap()
        });
        let spec = if let Some(re_captures) = RE_GEN_INDEX.captures(&spec_name) {
            let index_dim = re_captures
                .get(1)
                .unwrap()
                .as_str()
                .parse()
                .context("failed to parse index_dim for gen_index_at")?;
            let batch_x = re_captures.get(2).is_some();
            let batch_index = re_captures.get(3).is_none();
            let check_index_ints = re_captures.get(4).is_some();
            GeneralFunctionIndexSpec {
                index_dim,
                batch_x,
                batch_index,
                check_index_ints,
            }
            .into()
        } else if let Some(re_captures) = RE_MULTINOMIAL.captures(&spec_name) {
            let mut axis_strs: Vec<_> = re_captures
                .get(2)
                .unwrap()
                .as_str()
                .split(',')
                .map(|z| z.trim())
                .collect();
            if axis_strs.last() == Some(&"") {
                // allow last axis to be empty due to trailing comma
                // (Regex guarantees that only last axis has this I think, but better to be clear)
                axis_strs.pop();
            }
            let shape = axis_strs.into_iter().map(|x| x.parse().unwrap()).collect();
            GeneralFunctionMultinomialSpec {
                replacement: re_captures.get(1).is_none(),
                shape,
            }
            .into()
        } else if let Some(re_captures) = RE_A_SAMP_MULTINOMIAL.captures(&spec_name) {
            let mut axis_strs: Vec<_> = re_captures
                .get(1)
                .unwrap()
                .as_str()
                .split(',')
                .map(|z| z.trim())
                .collect();
            if axis_strs.last() == Some(&"") {
                // allow last axis to be empty due to trailing comma
                // (Regex guarantees that only last axis has this I think, but better to be clear)
                axis_strs.pop();
            }
            let shape = axis_strs.into_iter().map(|x| x.parse().unwrap()).collect();
            GeneralFunctionAlreadySampledMultinomialSpec { shape }.into()
        } else if let Some(re_captures) = RE_TOP_K.captures(&spec_name) {
            let mut axis_strs: Vec<_> = re_captures
                .get(1)
                .unwrap()
                .as_str()
                .split(',')
                .map(|z| z.trim())
                .collect();
            if axis_strs.last() == Some(&"") {
                // allow last axis to be empty due to trailing comma
                // (Regex guarantees that only last axis has this I think, but better to be clear)
                axis_strs.pop();
            }
            let shape = axis_strs.into_iter().map(|x| x.parse().unwrap()).collect();
            GeneralFunctionTopKSpec { shape }.into()
        } else if let Some(re_captures) = RE_EXPLICIT_INDEX.captures(&spec_name) {
            let index_dim = re_captures
                .get(1)
                .unwrap()
                .as_str()
                .parse()
                .context("failed to parse index_dim for explicit_index_at")?;
            let x_non_batch_dims = re_captures
                .get(2)
                .unwrap()
                .as_str()
                .parse()
                .context("failed to parse x_non_batch_dims for explicit_index_at")?;
            let check_index_ints = re_captures.get(3).is_some();
            GeneralFunctionExplicitIndexSpec {
                index_dim,
                x_non_batch_dims,
                check_index_ints,
            }
            .into()
        } else if let Some(re_captures) = RE_CAST.captures(&spec_name) {
            let device_in = re_captures.get(1).unwrap().as_str();
            let dtype_in = re_captures.get(2).unwrap().as_str();
            let device_out = re_captures.get(3).unwrap().as_str();
            let dtype_out = re_captures.get(4).unwrap().as_str();
            GeneralFunctionSetDDSpec {
                output: TorchDeviceDtypeOp {
                    device: if device_out == "None" {
                        None
                    } else {
                        Some(device_out.to_owned().try_into().unwrap())
                    },
                    dtype: if dtype_out == "None" {
                        None
                    } else {
                        Some(dtype_out.to_owned().try_into().unwrap())
                    },
                },
                input_required_compatibility: TorchDeviceDtypeOp {
                    device: if device_in == "None" {
                        None
                    } else {
                        Some(device_in.to_owned().try_into().unwrap())
                    },
                    dtype: if dtype_in == "None" {
                        None
                    } else {
                        Some(dtype_in.to_owned().try_into().unwrap())
                    },
                },
            }
            .into()
        } else if spec_name == "pow" {
            GeneralFunctionPairwiseSpec {
                pairwise_type: PairwiseType::Pow,
            }
            .into()
        } else if spec_name == "minimum" {
            GeneralFunctionPairwiseSpec {
                pairwise_type: PairwiseType::Minimum,
            }
            .into()
        } else if spec_name == "maximum" {
            GeneralFunctionPairwiseSpec {
                pairwise_type: PairwiseType::Maximum,
            }
            .into()
        } else if spec_name == "Output" {
            GeneralFunctionOutputSpec {}.into()
        } else if let Some(spec) = SPECS.get(spec_name) {
            spec.clone().into()
        } else {
            return Ok(None);
        };

        GeneralFunction::try_new(nodes, spec, name).map(Some)
    }

    #[staticmethod]
    #[pyo3(signature=(*nodes, path, data = None, name = None))]
    pub fn new_by_path(
        nodes: Vec<CircuitRc>,
        path: &str,
        data: Option<String>,
        name: Option<Name>,
    ) -> Result<Self> {
        let locator = PyClassLocator::parse(path)?;

        let spec: GeneralFunctionSpec =
            Python::with_gil(|py| -> Result<GeneralFunctionSpec, pyo3::PyErr> {
                let spec_cls = locator.get_class(py)?;
                match data {
                    // TODO maybe assert serialize = parse & isinstance spec_cls? or check in init or spec tester
                    Some(data) => spec_cls.call_method1("parse_data", (data,))?.extract(),
                    None => spec_cls.call0()?.extract(),
                }
            })?;

        GeneralFunction::try_new(nodes, spec.into(), name)
    }

    #[staticmethod]
    #[pyo3(signature=(*nodes, path, data = None, name = None))]
    pub fn new_multi_output_by_path(
        nodes: Vec<CircuitRc>,
        path: &str,
        data: Option<String>,
        name: Option<Name>,
    ) -> Result<Vec<Self>> {
        let locator = PyClassLocator::parse(path)?;

        let spec = Python::with_gil(|py| -> Result<PyWrapMultiOutput, pyo3::PyErr> {
            let spec_cls = locator.get_class(py)?;
            match data {
                Some(data) => spec_cls.call_method1("parse_data", (data,))?.extract(),
                None => spec_cls.call0()?.extract(),
            }
        })?;

        GeneralFunction::new_multi_output(nodes, spec.into(), name)
    }

    #[staticmethod]
    #[pyo3(signature=(
        x,
        index,
        index_dim,
        batch_x = false,
        batch_index = true,
        check_index_ints = true,
        name = None
    ))]
    pub fn gen_index(
        x: CircuitRc,
        index: CircuitRc,
        index_dim: i64,
        batch_x: bool,
        batch_index: bool,
        check_index_ints: bool,
        name: Option<Name>,
    ) -> Result<Self> {
        let spec = GeneralFunctionIndexSpec {
            index_dim,
            batch_x,
            batch_index,
            check_index_ints,
        }
        .into();
        Self::try_new(vec![x, index], spec, name)
    }

    #[staticmethod]
    #[pyo3(signature=(x, index, index_dim, x_non_batch_dims, check_index_ints = true, name = None))]
    pub fn explicit_index(
        x: CircuitRc,
        index: CircuitRc,
        index_dim: i64,
        x_non_batch_dims: usize,
        check_index_ints: bool,
        name: Option<Name>,
    ) -> Result<Self> {
        let spec =
            GeneralFunctionExplicitIndexSpec::new(index_dim, x_non_batch_dims, check_index_ints)?
                .into();
        Self::try_new(vec![x, index], spec, name)
    }

    #[staticmethod]
    #[pyo3(signature=(
        x,
        input_required_compatibility = Default::default(),
        output = Default::default(),
        name = None
    ))]
    pub fn new_cast(
        x: CircuitRc,
        input_required_compatibility: TorchDeviceDtypeOp,
        output: TorchDeviceDtypeOp,
        name: Option<Name>,
    ) -> Result<Self> {
        let spec = GeneralFunctionSetDDSpec {
            input_required_compatibility,
            output,
        }
        .into();
        Self::try_new(vec![x], spec, name)
    }
}

fn convert_op_str_to_format_err(op_s: Option<&str>, path: &str) -> Result<String> {
    if let Some(s) = op_s {
        Ok(s.to_string())
    } else {
        Err(anyhow!(format!(
            "failed to parse general function from string: {}",
            path
        )))
    }
}

#[apply(python_error_exception)]
#[base_error_name(GeneralFunctionShape)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum GeneralFunctionShapeError {
    #[error("got={got} expected={expected} ({e_name})")]
    WrongNumShapes { got: usize, expected: usize },

    #[error("ndim={ndim} < num_non_batchable_output_dims={num_non_batchable_output_dims} + removed_from_end={removed_from_end} ({e_name})")]
    NDimTooSmall {
        ndim: usize,
        num_non_batchable_output_dims: u8,
        removed_from_end: u8,
    },

    #[error(
        "batch dims not equal for all inputs: batches={batches:?} output_batch={output_batch:?} ({e_name})"
    )]
    BatchDimsNotEqual {
        batches: Vec<Shape>,
        output_batch: Shape,
    },

    #[error("x_shape={x_shape:?} index_shape={index_shape:?} batch_x={batch_x} ({e_name})")]
    IndexShapeInvalid {
        x_shape: Shape,
        index_shape: Shape,
        batch_x: bool,
    },

    #[error("x_shape={x_shape:?} index_shape={index_shape:?} index_dim={index_dim} x_non_batch_dims={x_non_batch_dims} ({e_name})")]
    ExplicitIndexShapeInvalid {
        x_shape: Shape,
        index_shape: Shape,
        index_dim: i64,
        x_non_batch_dims: usize,
    },
}
