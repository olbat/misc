use std::error::Error;
use std::path::Path;

use crate::options;
use crate::search;

pub fn print_results<'a>(
    filepath: &'a Path,
    results: Result<impl Iterator<Item = search::Match>, Box<dyn Error>>,
    opts: &'a options::Options,
) -> bool {
    let mut any_match = false;

    match results {
        Ok(matches) => {
            for (line_no, line) in matches {
                any_match |= true;
                print_result(filepath, line_no, line, opts);
            }
        }
        Err(e) => print_error(filepath, e),
    }

    any_match
}

#[inline]
fn print_result<'a>(filepath: &'a Path, line_no: usize, line: String, opts: &'a options::Options) {
    if !opts.quiet {
        println!("{}:{}: {}", filepath.display(), line_no, line);
    }
}

#[inline]
fn print_error<'a>(filepath: &'a Path, err: Box<dyn Error>) {
    eprintln!("{}: error, {}", filepath.display(), err);
}
