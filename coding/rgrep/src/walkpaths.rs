use std::fs;
use std::io;
#[cfg(unix)]
use std::os::unix::fs::FileTypeExt;
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

    fn walkdir(&mut self, dir: &Path) -> io::Result<()> {
        // depth first path traversal
        for entry in fs::read_dir(dir)? {
            let entry = entry?;
            self.stack.push(entry.path());
        }
        Ok(())
    }

    #[inline]
    fn check_path(&self, path: &PathBuf) -> Option<io::Error> {
        if cfg!(unix) {
            match path.metadata() {
                Ok(metadata) => {
                    let file_type = metadata.file_type();
                    if file_type.is_char_device() {
                        Some(io::Error::new(
                            io::ErrorKind::InvalidData,
                            "cannot process char device",
                        ))
                    } else if file_type.is_block_device() {
                        Some(io::Error::new(
                            io::ErrorKind::InvalidData,
                            "cannot process block device",
                        ))
                    } else if file_type.is_fifo() {
                        Some(io::Error::new(
                            io::ErrorKind::InvalidData,
                            "cannot process fifo",
                        ))
                    } else if file_type.is_socket() {
                        Some(io::Error::new(
                            io::ErrorKind::InvalidData,
                            "cannot process socket",
                        ))
                    } else {
                        None
                    }
                }
                Err(e) => Some(e),
            }
        } else {
            None
        }
    }
}

impl Iterator for WalkPaths {
    type Item = (PathBuf, Option<io::Error>);

    fn next(&mut self) -> Option<Self::Item> {
        loop {
            match self.stack.pop() {
                Some(path) => {
                    if path.is_dir() {
                        match self.walkdir(&path) {
                            Ok(_) => continue,
                            Err(err) => break Some((path, Some(err))),
                        }
                    } else {
                        let err = self.check_path(&path);
                        break Some((path, err));
                    }
                }
                None => break None,
            }
        }
    }
}
