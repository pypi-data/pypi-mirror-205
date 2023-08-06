use std::fmt::Write;

use anyhow::Result;
use circuit_base::{
    all_children,
    opaque_iterative_matcher::{HasTerm, OpaqueIterativeMatcherVal},
    Circuit, CircuitNode, CircuitNodeSelfOnlyHash, CircuitRc,
};
use circuit_print::print::{CircuitToColorCode, PrintOptions};
use get_update_node::{new_traversal, IterativeMatcherRc, Matcher, MatcherData};
use itertools::izip;
use pyo3::prelude::*;
use rr_util::{
    clicolor,
    name::Name,
    print::{color, last_child_arrows, CliColor},
    util::HashBytes,
};
use rustc_hash::FxHashMap as HashMap;
use uuid::uuid;

#[pyfunction]
#[pyo3(signature=(
    circuit,
    hash_child_count = true,
    hash_child_shapes = false,
    hash_name = true
))]
pub fn compute_self_hash(
    circuit: CircuitRc,
    hash_child_count: bool,
    hash_child_shapes: bool,
    hash_name: bool,
) -> HashBytes {
    let mut m = blake3::Hasher::new();
    for l in &circuit.info().shape {
        m.update(&l.to_le_bytes());
    }
    m.update(uuid!("92814fb9-3aa0-489c-b016-0f936941535b").as_bytes());
    if hash_name {
        m.update(Name::str_maybe_empty(circuit.info().name).as_bytes());
    }
    m.update(uuid!("6261daa8-0085-46f7-9f38-b085601fa628").as_bytes());
    if hash_child_count {
        m.update(&circuit.num_children().to_le_bytes());
    }
    m.update(uuid!("c7034aef-2179-4afa-9b90-c9abfcd1405d").as_bytes());
    if hash_child_shapes {
        for x in circuit.children() {
            for l in x.shape() {
                m.update(&l.to_le_bytes());
            }
            m.update(uuid!("17519b66-2332-450e-bdb2-bf893f8ed699").as_bytes());
        }
    }
    m.update(uuid!("e95b4d23-0077-4f57-a993-224454cb8570").as_bytes());
    circuit.compute_self_only_hash(&mut m);
    m.finalize().into()
}

fn default_diff_options() -> PrintOptions {
    PrintOptions {
        arrows: true,
        bijection: false,
        traversal: Some(OpaqueIterativeMatcherVal::term()),
        ..Default::default()
    }
}

#[pyfunction]
#[pyo3(signature=(
    new,
    old,
    options = default_diff_options(),
    require_child_count_same = true,
    require_child_shapes_same = false,
    require_name_same = false,
    print_legend = true,
    same_self_color = clicolor!(Blue),
    new_color = clicolor!(Green),
    removed_color = clicolor!(Red),
))]
pub fn diff_circuits(
    new: CircuitRc,
    old: CircuitRc,
    options: PrintOptions,
    require_child_count_same: bool,
    require_child_shapes_same: bool,
    require_name_same: bool,
    print_legend: bool,
    same_self_color: CliColor,
    new_color: CliColor,
    removed_color: CliColor,
) -> Result<String> {
    struct DiffConfig {
        require_child_count_same: bool,
        require_child_shapes_same: bool,
        require_name_same: bool,
        same_self_color: CliColor,
        new_color: CliColor,
        removed_color: CliColor,
        options: PrintOptions,
        old_options: PrintOptions,
        new_options: PrintOptions,
        disallow_name_ident: Option<HashMap<Name, bool>>,
    }

    fn recurse(
        new: CircuitRc,
        old: CircuitRc,
        result: &mut String,
        prefix: &str,
        parent_info: Option<(&Circuit, usize)>,
        dc: &DiffConfig,
        traversal: IterativeMatcherRc,
        seen_diffs: &mut HashMap<(CircuitRc, CircuitRc), String>,
        seen_hashes: &mut HashMap<HashBytes, (String, String)>,
        running_serial_number: &mut usize,
        running_leaf_number: &mut usize,
    ) -> Result<()> {
        let diffkey = (new.clone(), old.clone());
        if let Some(id) = seen_diffs.get(&diffkey) {
            result.push_str(&id);
            result.push('\n');
            return Ok(());
        }
        let id = seen_diffs.len();

        if new == old {
            dc.options.repr_build_go(
                &**new,
                result,
                seen_hashes,
                running_serial_number,
                running_leaf_number,
                prefix,
                Some(traversal.as_opaque()),
                dc.disallow_name_ident.as_ref(),
                parent_info,
                vec![],
            )?;
            return Ok(());
        }
        if compute_self_hash(
            new.clone(),
            dc.require_child_count_same,
            dc.require_child_shapes_same,
            dc.require_name_same,
        ) == compute_self_hash(
            old.clone(),
            dc.require_child_count_same,
            dc.require_child_shapes_same,
            dc.require_name_same,
        ) {
            let line = color(
                &format!(
                    "{}{} # changed {id}{}",
                    new.info().name.map_or("", |x| x.str()),
                    dc.options.repr_line_info(new.clone())?,
                    if new.info().name != old.info().name {
                        color(
                            &format!(" old name: {}", old.info().name.map_or("", |x| x.str())),
                            dc.removed_color,
                        )
                    } else {
                        "".to_string()
                    }
                ),
                dc.same_self_color,
            );
            result.push_str(&line);
            seen_diffs.insert(
                diffkey.clone(),
                color(
                    &format!(
                        "{} # changed {id} (repeat)",
                        new.info().name.map_or("", |x| x.str())
                    ),
                    dc.same_self_color,
                ),
            );
            result.push('\n');

            assert_eq!(new.num_children(), old.num_children());
            for (i, (new_child, old_child, new_traversal)) in izip!(
                new.children(),
                old.children(),
                traversal.match_iterate_continue(new.clone())?.2,
            )
            .enumerate()
            {
                let new_prefix = last_child_arrows(
                    result,
                    prefix,
                    i == new.num_children() - 1,
                    dc.options.arrows,
                );
                recurse(
                    new_child,
                    old_child,
                    result,
                    &new_prefix,
                    Some((&*new, i)),
                    dc,
                    new_traversal,
                    seen_diffs,
                    seen_hashes,
                    running_serial_number,
                    running_leaf_number,
                )?;
            }
            return Ok(());
        }
        for (o, x, is_old) in [
            (&dc.old_options, &old, true),
            (&dc.new_options, &new, false),
        ] {
            let mut new_prefix = prefix.to_owned();
            new_prefix.pop();
            new_prefix.pop();
            if is_old {
                result.pop();
                result.pop();
                result.push_str(&color("- ", dc.removed_color));
                new_prefix.push_str(&color("- ", dc.removed_color));
            } else {
                new_prefix.push_str(&color("+ ", dc.new_color));
                result.push_str(&new_prefix);
            }
            o.repr_build_go(
                &**x,
                result,
                seen_hashes,
                running_serial_number,
                running_leaf_number,
                &new_prefix,
                Some(traversal.as_opaque()),
                dc.disallow_name_ident.as_ref(),
                parent_info,
                vec![],
            )?;
        }

        Ok(())
    }
    let old_circuits = all_children(old.clone());
    let new_circuits = all_children(new.clone());
    let old_circuits_2 = old_circuits.clone();
    let new_circuits_2 = new_circuits.clone();

    let traversal: IterativeMatcherRc =
        options
            .traversal
            .clone()
            .map_or(MatcherData::Always(true).into(), |t| {
                Python::with_gil(|py| {
                    new_traversal(
                        None,
                        None,
                        Matcher::new_func(Box::new(move |x| {
                            old_circuits.contains(&x) && new_circuits.contains(&x)
                        }))
                        .into(),
                    )
                    .or(t.to_object(py).extract(py).unwrap())
                    .into()
                })
            });

    let mut new_options = options.clone();
    let colorer = options.colorer.clone();
    new_options.colorer = Some(CircuitToColorCode::new_dyn(Box::new(move |x| {
        if old_circuits_2.contains(&x) {
            colorer.as_ref().map_or(Ok(CliColor::NONE), |f| f.call(x))
        } else {
            Ok(new_color)
        }
    })));

    let mut old_options = options.clone();
    let colorer = options.colorer.clone();
    old_options.colorer = Some(CircuitToColorCode::new_dyn(Box::new(move |x| {
        if new_circuits_2.contains(&x) {
            colorer.as_ref().map_or(Ok(CliColor::NONE), |f| f.call(x))
        } else {
            Ok(removed_color)
        }
    })));

    let mut result = "".to_owned();
    let mut seen_diffs: HashMap<(CircuitRc, CircuitRc), String> = HashMap::default();

    let mut seen_hashes: HashMap<HashBytes, (String, String)> = HashMap::default();
    let mut running_serial_number = 0;
    let mut running_leaf_number = 0;

    let dc = DiffConfig {
        require_child_count_same,
        require_child_shapes_same,
        require_name_same,
        same_self_color,
        new_color,
        removed_color,
        disallow_name_ident: options.disallow_name_ident(&[new.clone(), old.clone()]),
        options,
        new_options,
        old_options,
    };
    recurse(
        new,
        old,
        &mut result,
        "",
        None,
        &dc,
        traversal,
        &mut seen_diffs,
        &mut seen_hashes,
        &mut running_serial_number,
        &mut running_leaf_number,
    )?;
    if print_legend {
        if &result[result.len() - 1..] != "\n" {
            result.push('\n');
        }
        writeln!(
            result,
            "{} {} {}\n",
            color(
                &format!("{}: Children changed", same_self_color),
                same_self_color
            ),
            color(&format!("{}: Only in new", new_color), new_color),
            color(&format!("{}: Only in old", removed_color), removed_color)
        )
        .unwrap();
    }
    Ok(result)
}
