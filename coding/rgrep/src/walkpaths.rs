use std::fs;
use std::io;
use std::path::{Path, PathBuf};

pub struct WalkPaths {
    stack: Vec<PathBuf>,
}

impl WalkPaths {
    pub fn new<T>(paths: T) -> Self
    where
        T: IntoIterator,
        T::Item: AsRef<Path>,
    {
        WalkPaths {
            stack: paths
                .into_iter()
                .map(|p| p.as_ref().to_path_buf())
                .collect(),
        }
    }

    fn walkdir(&mut self, dir: PathBuf) -> io::Result<()> {
        // depth first path traversal
        for entry in fs::read_dir(dir)? {
            let entry = entry?;
            self.stack.push(entry.path());
        }
        Ok(())
    }
}

impl Iterator for WalkPaths {
    type Item = io::Result<PathBuf>;

    fn next(&mut self) -> Option<Self::Item> {
        loop {
            match self.stack.pop() {
                Some(path) => {
                    if path.is_dir() {
                        match self.walkdir(path) {
                            Ok(_) => continue,
                            Err(e) => break Some(Err(e)),
                        }
                    } else {
                        break Some(Ok(path));
                    }
                }
                None => break None,
            }
        }
    }
}