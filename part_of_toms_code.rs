use crate::{is_sorted, Word, FDTS};
use itertools::Itertools;

#[derive(Debug, Clone, Eq, PartialEq)]
pub struct MappedFDTS<'a> {
    pub fdts: &'a FDTS,
    pub map: Vec<usize>,
    pub back: Vec<Option<usize>>,
}

impl<'a> MappedFDTS<'a> {
    pub fn new(fdts: &'a FDTS, map: &[usize], range: usize) -> Self {
        assert!(map.len() == fdts.n());
        let mut back = vec![None; range];
        for (i, &m) in map.iter().enumerate() {
            back[m] = Some(i);
        }
        assert!(is_sorted(map));
        assert!(is_sorted(&back.iter().filter_map(|&x| x).collect_vec()));
        Self {
            fdts,
            map: map.into(),
            back,
        }
    }

    pub fn iterate_words(&'a self) -> impl Iterator<Item = Word> + 'a {
        self.fdts
            .dice
            .iter()
            .map(move |d| d.word.iter().map(|x| self.map[*x as usize] as u8).collect::<Word>())
    }

    pub fn iterate_words_subset(&'a self, subset: &[usize]) -> impl Iterator<Item = Word> + 'a {
        // Which internal indices to keep
        let keep: Vec<bool> = (0..self.map.len()).map(|i| subset.contains(&self.map[i])).collect();
        self.fdts.dice.iter().map(move |d| {
            d.word
                .iter()
                .filter(|&&x| keep[x as usize])
                .map(|&x| self.map[x as usize] as u8)
                .collect::<Word>()
        })
    }

    pub fn subset_word_in_prefixes(&self, word: &[u8]) -> bool {
        let bword: Word = word.iter().filter_map(|&d| self.back[d as usize]).map(|x| x as u8).collect();
        self.fdts.prefixes.contains(&bword)
    }

    pub fn sizes_string(&self) -> String {
        format!(
            "[{}]",
            self.back
                .iter()
                .map(|b| {
                    if let Some(i) = *b {
                        self.fdts.sizes[i].to_string()
                    } else {
                        "_".into()
                    }
                })
                .join(",")
        )
    }

    pub fn is_compatible_with(&self, other: &MappedFDTS) -> bool {
        if self.back.len() != other.back.len() {
            return false;
        }
        for (&b1, &b2) in self.back.iter().zip(other.back.iter()) {
            if b1.is_some() && b2.is_some() {
                if self.fdts.sizes[b1.unwrap()] != other.fdts.sizes[b2.unwrap()] {
                    return false;
                }
            }
        }
        true
    }
}

#[cfg(test)]
mod test {
    use crate::{DiceTuple, Word};
    use crate::{MappedFDTS, FDTS};

    #[test]
    fn test_mapped() {
        let mut f = FDTS::new_empty(&[2, 2, 3]);
        f.insert_dice_tuple(DiceTuple::from_word(&f, &[1, 2, 0, 2, 1, 0, 2]));

        let mf: MappedFDTS = MappedFDTS::new(&f, &[0, 2, 3], 4);
        assert_eq!(mf.iterate_words().collect::<Vec<_>>(), &[Word::from_slice(&[2, 3, 0, 3, 2, 0, 3])]);
        assert_eq!(mf.iterate_words_subset(&[3]).collect::<Vec<_>>(), &[Word::from_slice(&[3, 3, 3])]);
        assert_eq!(mf.iterate_words_subset(&[1]).collect::<Vec<_>>(), &[Word::from_slice(&[])]);
        assert_eq!(
            mf.iterate_words_subset(&[0, 1, 2]).collect::<Vec<_>>(),
            &[Word::from_slice(&[2, 0, 2, 0])]
        );

        let mf2 = f.mapped_as(&[0, -1, 1, 2]);
        assert_eq!(mf2.iterate_words().collect::<Vec<_>>(), &[Word::from_slice(&[2, 3, 0, 3, 2, 0, 3])]);
    }
}