use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

use crate::Options;

pub type Match = (usize, String);

// TODO: find a way to simplify the return type to make it easy to re-use
pub fn search<'a, P: AsRef<Path> + 'a>(
    pattern: &'a str,
    paths: impl Iterator<Item = P>,
    opts: &'a Options,
) -> impl Iterator<Item = (P, Result<impl Iterator<Item = Match> + 'a, Box<dyn Error>>)> {
    // TODO: search different files in parallel
    // TODO: allow searching in directories (use a stack to avoid too many nested recursive calls?)
    paths.into_iter().map(move |p| {
        let results = search_file(pattern, &p, &opts);
        (p, results)
    })
}

// TODO: make pattern a std::str::Pattern & change path to be a std::io::Reader?
pub fn search_file<'a, P: AsRef<Path> + 'a>(
    pattern: &'a str,
    path: &P,
    _opts: &'a Options,
) -> Result<impl Iterator<Item = Match> + 'a, Box<dyn Error>> {
    // TODO: re-use the same buffer for the whole process instead of creating a new one every time
    let f = File::open(path.as_ref())?;
    let f = BufReader::new(f);

    Ok(f.lines()
        .map(|l| l.unwrap()) // FIXME: return an error on Err
        .enumerate()
        .filter(move |(_, l)| l.contains(pattern)))
}
