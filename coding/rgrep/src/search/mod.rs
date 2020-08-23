#[cfg(feature = "simd")]
extern crate twoway;

use std::fs::File;
use std::io::{self, BufRead, BufReader, Read};
use std::path::Path;

mod options;
pub use options::Options;

pub type Match = (usize, io::Result<String>);

pub fn search<'a, P: AsRef<Path> + 'a>(
    pattern: &'a str,
    paths: impl Iterator<Item = P> + 'a,
    opts: &'a Options,
) -> impl Iterator<Item = (P, io::Result<impl Iterator<Item = Match> + 'a>)> {
    search_paths(pattern, paths.map(|p| (p, None)), opts)
}

// TODO: find a way to simplify the return type to make it easy to re-use
pub fn search_paths<'a, P: AsRef<Path> + 'a>(
    pattern: &'a str,
    paths: impl Iterator<Item = (P, Option<io::Error>)>,
    opts: &'a Options,
) -> impl Iterator<Item = (P, io::Result<impl Iterator<Item = Match> + 'a>)> {
    // TODO: search different files in parallel
    paths.map(move |(p, e)| {
        if let Some(err) = e {
            (p, io::Result::Err(err))
        } else {
            let file = File::open(p.as_ref());
            match file {
                Ok(f) => (p, io::Result::Ok(search_file(pattern, f, &opts))),
                Err(e) => (p, io::Result::Err(e)),
            }
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
            Ok(line) => search_string(&line, &pattern),
            Err(_) => true,
        })
        .enumerate()
        .map(|(n, l)| (n + 1, l))
}

#[cfg(feature = "simd")]
#[inline]
fn search_string(string: &str, pattern: &str) -> bool {
    twoway::find_str(&string, pattern).is_some()
}

#[cfg(not(feature = "simd"))]
#[inline]
fn search_string(string: &str, pattern: &str) -> bool {
    string.contains(pattern)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs::{self, File};
    use std::io::Write;
    use std::io::{Seek, SeekFrom};
    use tempfile::tempdir;
    use tempfile::tempfile;

    #[test]
    fn simple_search_string() {
        let string = "some simple string";

        assert_eq!(search_string(string, "simple"), true);
        assert_eq!(search_string(string, "complex"), false);
    }

    #[test]
    fn simple_search_file() {
        let mut file = tempfile().unwrap();
        writeln!(file, "first simple string");
        writeln!(file, "other string");
        writeln!(file, "some other string");
        writeln!(file);
        writeln!(file, "second simple string");
        writeln!(file, "a last string");
        file.seek(SeekFrom::Start(0)).unwrap();

        let options = Options::new();
        let mut results = search_file("simple", file, &options);

        let result = results.next();
        assert!(result.is_some());
        let result = result.unwrap();
        assert_eq!(result.0, 1);
        assert!(result.1.is_ok());
        assert_eq!(result.1.unwrap(), "first simple string");

        let result = results.next();
        assert!(result.is_some());
        let result = result.unwrap();
        assert_eq!(result.0, 5);
        assert!(result.1.is_ok());
        assert_eq!(result.1.unwrap(), "second simple string");

        let result = results.next();
        assert!(result.is_none());
    }

    #[test]
    fn simple_search_paths() {
        let dir = tempdir().unwrap();
        let dir_path = dir.path();

        let file1_path = dir_path.join("file1");
        let mut file1 = File::create(&file1_path).unwrap();
        writeln!(file1);
        writeln!(file1, "first simple string");
        writeln!(file1, "other string");
        writeln!(file1);
        writeln!(file1);
        writeln!(file1, "second simple string");

        let file2_path = dir_path.join("file2");
        let mut file2 = File::create(&file2_path).unwrap();
        writeln!(file2, "nothing");
        writeln!(file2, "matching");
        writeln!(file2, "here");

        let subdir_path = dir_path.join("some").join("sub").join("dir");
        fs::create_dir_all(&subdir_path).unwrap();

        let file3_path = subdir_path.join("file3");
        let mut file3 = File::create(&file3_path).unwrap();
        writeln!(file3, "third simple string");
        writeln!(file3, "third simple string");
        writeln!(file3, "third simple string");

        let paths = vec![&file1_path, &file2_path, &file3_path];
        let options = Options::new();

        let mut paths_results = search_paths("simple", paths.iter().map(|p| (p, None)), &options);

        let paths_result = paths_results.next();
        assert!(paths_result.is_some());
        let paths_result = paths_result.unwrap();
        assert_eq!(*paths_result.0, &file1_path);
        assert!(paths_result.1.is_ok());

        // file1
        let mut path_results = paths_result.1.unwrap();
        let results = path_results.next();
        assert!(results.is_some());
        let result = results.unwrap();
        assert_eq!(result.0, 2);
        assert!(result.1.is_ok());
        assert_eq!(result.1.unwrap(), "first simple string");

        let results = path_results.next();
        assert!(results.is_some());
        let result = results.unwrap();
        assert_eq!(result.0, 6);
        assert!(result.1.is_ok());
        assert_eq!(result.1.unwrap(), "second simple string");

        let results = path_results.next();
        assert!(results.is_none());

        // file2
        let path_result = paths_results.next();
        assert!(path_result.is_some());
        let path_result = path_result.unwrap();
        assert_eq!(*path_result.0, &file2_path);
        assert!(path_result.1.is_ok());

        let mut path_results = path_result.1.unwrap();
        let results = path_results.next();
        assert!(results.is_none());

        // file3
        let path_result = paths_results.next();
        assert!(path_result.is_some());
        let path_result = path_result.unwrap();
        assert_eq!(*path_result.0, &file3_path);
        assert!(path_result.1.is_ok());

        let mut path_results = path_result.1.unwrap();
        let results = path_results.next();
        assert!(results.is_some());
        let result = results.unwrap();
        assert_eq!(result.0, 1);
        assert!(result.1.is_ok());
        assert_eq!(result.1.unwrap(), "third simple string");

        let results = path_results.next();
        assert!(results.is_some());
        let result = results.unwrap();
        assert_eq!(result.0, 2);
        assert!(result.1.is_ok());
        assert_eq!(result.1.unwrap(), "third simple string");

        let results = path_results.next();
        assert!(results.is_some());
        let result = results.unwrap();
        assert_eq!(result.0, 3);
        assert!(result.1.is_ok());
        assert_eq!(result.1.unwrap(), "third simple string");

        let results = path_results.next();
        assert!(results.is_none());
    }

    #[test]
    fn search_path_with_error() {}
}
