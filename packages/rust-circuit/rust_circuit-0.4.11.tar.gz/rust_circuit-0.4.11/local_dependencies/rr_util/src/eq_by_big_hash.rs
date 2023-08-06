use std::{collections::BTreeMap, mem};

use crate::util::HashBytes;

pub trait EqByBigHash {
    fn hash(&self) -> HashBytes;
    #[inline]
    fn first_u64_bytes(&self) -> [u8; mem::size_of::<u64>()] {
        self.hash()[..mem::size_of::<u64>()].try_into().unwrap()
    }
    #[inline]
    fn first_u64(&self) -> u64 {
        let a = unsafe { std::mem::transmute::<[u8; 32], [u64; 4]>(self.hash()) };
        a[0]
    }
    fn first_i64(&self) -> i64 {
        i64::from_le_bytes(self.first_u64_bytes())
    }
}

impl<K: EqByBigHash, V: EqByBigHash> EqByBigHash for BTreeMap<K, V> {
    fn hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        for (k, v) in self {
            hasher.update(&k.hash());
            hasher.update(&v.hash());
        }
        hasher.finalize().into()
    }
}

#[macro_export]
macro_rules! impl_eq_by_big_hash {
    ($t:ty) => {
        impl PartialEq for $t {
            #[inline]
            fn eq(&self, other: &Self) -> bool {
                let a = unsafe {
                    std::mem::transmute::<[u8; 32], [u64; 4]>(
                        $crate::eq_by_big_hash::EqByBigHash::hash(self),
                    )
                };
                let b = unsafe {
                    std::mem::transmute::<[u8; 32], [u64; 4]>(
                        $crate::eq_by_big_hash::EqByBigHash::hash(other),
                    )
                };
                (a[0] == b[0]) && (a[1] == b[1]) && (a[2] == b[2]) && (a[3] == b[3])
            }
        }
        impl Eq for $t {}
        impl ::std::hash::Hash for $t {
            #[inline]
            fn hash<H: ::std::hash::Hasher>(&self, state: &mut H) {
                state.write_u64($crate::eq_by_big_hash::EqByBigHash::first_u64(self));
            }
        }
    };
}

#[macro_export]
macro_rules! impl_ord_by_big_hash {
    ($t:ty) => {
        impl PartialOrd for $t {
            #[inline]
            fn partial_cmp(&self, other: &Self) -> Option<::std::cmp::Ordering> {
                Some(self.cmp(other))
            }
        }
        impl Ord for $t {
            #[inline]
            fn cmp(&self, other: &Self) -> ::std::cmp::Ordering {
                $crate::eq_by_big_hash::EqByBigHash::hash(self)
                    .cmp(&$crate::eq_by_big_hash::EqByBigHash::hash(other))
            }
        }
    };
}
#[macro_export]
macro_rules! impl_both_by_big_hash {
    ($t:ty) => {
        $crate::impl_eq_by_big_hash!($t);
        $crate::impl_ord_by_big_hash!($t);
    };
}
