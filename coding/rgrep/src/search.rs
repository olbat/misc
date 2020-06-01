use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;
use std::path::Path;

use crate::Options;

// TODO; to be completed
//struct SearchResult;
//enum SearchError;

// TODO: use a closure to return matched entries one by one (result or error)
//       (result entry: Path, line & pattern position, /!\ overlapping results)
pub fn search<P: AsRef<Path>>(
    pattern: &str,
    paths: impl IntoIterator<Item = P>,
    opts: &Options,
) -> Result<bool, Box<dyn Error>> {
    let mut found = false;

    // TODO: search different files in parallel
    for path in paths.into_iter() {
        let path = path.as_ref();
        if path.is_dir() {
            // TODO: allow searching in directories (use a stack to avoid too many nested recursive calls?)
        } else {
            found = found || search_file(pattern, path, opts)?;
        }
    }

    Ok(found)
}

// TODO: make pattern a std::str::Pattern
pub fn search_file(pattern: &str, path: &Path, _opts: &Options) -> Result<bool, Box<dyn Error>> {
    // TODO: re-use the same buffer for the whole process instead of creating a new one every time
    let f = File::open(path)?;
    let f = BufReader::new(f);

    // TODO: use a closure
    Ok(f.lines().any(|l| l.unwrap().contains(pattern)))
}
