use std::io;
use std::path::Path;

use crate::options;
use crate::search;

pub fn print_results<'a, P: AsRef<Path> + 'a>(
    results: impl Iterator<Item = (P, io::Result<impl Iterator<Item = search::Match> + 'a>)>,
    opts: &'a options::Options,
) -> bool {
    let mut any_match = false;

    for (filepath, result) in results {
        let filepath = filepath.as_ref();
        match result {
            Ok(matches) => any_match |= print_matches(filepath, matches, opts),
            Err(error) => print_error(filepath, error),
        }
    }

    any_match
}

pub fn print_matches<'a>(
    filepath: &'a Path,
    matches: impl Iterator<Item = search::Match>,
    opts: &'a options::Options,
) -> bool {
    let mut any_match = false;

    for (line_no, lmatch) in matches {
        match lmatch {
            Ok(line) => {
                any_match |= true;
                print_match(filepath, line_no, line, opts);
            }
            Err(error) => print_error(filepath, error),
        }
    }

    any_match
}

#[inline]
fn print_match<'a>(filepath: &'a Path, line_no: usize, line: String, opts: &'a options::Options) {
    if !opts.quiet {
        println!("{}:{}:{}", filepath.display(), line_no, line);
    }
}

#[inline]
fn print_error<'a>(filepath: &'a Path, error: io::Error) {
    eprintln!("!{}: {}", filepath.display(), error);
}