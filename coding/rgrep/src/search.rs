use std::fs::File;
use std::io::{self, BufRead, BufReader, Read};
use std::path::Path;

use crate::Options;

pub type Match = (usize, io::Result<String>);

// TODO: find a way to simplify the return type to make it easy to re-use
pub fn search<'a, P: AsRef<Path> + 'a>(
    pattern: &'a str,
    paths: impl Iterator<Item = P>,
    opts: &'a Options,
) -> impl Iterator<Item = (P, io::Result<impl Iterator<Item = Match> + 'a>)> {
    // TODO: search different files in parallel
    // TODO: allow searching in directories (use a stack to avoid too many nested recursive calls?)
    paths.into_iter().map(move |p| {
        let file = File::open(p.as_ref());
        match file {
            Ok(f) => (p, io::Result::Ok(search_file(pattern, f, &opts))),
            Err(e) => (p, io::Result::Err(e)),
        }
    })
}

// TODO: make pattern a std::str::Pattern
pub fn search_file<'a>(
    pattern: &'a str,
    file: impl Read + 'a,
    _opts: &'a Options,
) -> impl Iterator<Item = Match> + 'a {
    // TODO: re-use the same buffer for the whole process instead of creating a new one every time
    let f = BufReader::new(file);
    let mut had_error = false;

    f.lines()
        .take_while(move |res| match res {
            Ok(_) => !had_error,
            Err(_) => {
                // stop iterating after the first error
                let stop = !had_error;
                had_error = true;
                stop
            }
        })
        .filter(move |res| match res {
            Ok(line) => line.contains(pattern),
            Err(_) => true,
        })
        .enumerate()
        .map(|(n, l)| (n + 1, l))
}