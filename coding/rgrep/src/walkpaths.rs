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

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashSet;
    use std::fs::{self, File};
    use std::path::{Path, PathBuf};
    use tempfile::tempdir;

    #[test]
    fn simple_walkpath() {
        let dir = tempdir().unwrap();
        let dir_path = dir.path();

        let file1_path = dir_path.join("file1");
        File::create(&file1_path).unwrap();

        let file2_path = dir_path.join("file2");
        let sub_dir_path = dir_path.join("dir");
        fs::create_dir_all(&sub_dir_path).unwrap();
        File::create(&file2_path).unwrap();

        let nested_dir_path = dir_path.join("some").join("nested").join("dir");
        fs::create_dir_all(&nested_dir_path).unwrap();
        let file3_path = sub_dir_path.join("file3");
        File::create(&file3_path).unwrap();

        let empty_dir_path = dir_path.join("some").join("empty").join("dir");
        fs::create_dir_all(&empty_dir_path).unwrap();

        let paths: HashSet<&Path> = [
            file1_path.as_ref(),
            file2_path.as_ref(),
            file3_path.as_ref(),
        ]
        .iter()
        .cloned()
        .collect();

        let mut walkpaths = WalkPaths::new(vec![&dir_path]);

        let result = walkpaths.next();
        assert!(result.is_some());
        let result = result.unwrap();
        assert!(paths.contains::<&Path>(&result.0.as_ref()));
        assert!(result.1.is_none());

        let result = walkpaths.next();
        assert!(result.is_some());
        let result = result.unwrap();
        assert!(paths.contains::<&Path>(&result.0.as_ref()));
        assert!(result.1.is_none());

        let result = walkpaths.next();
        assert!(result.is_some());
        let result = result.unwrap();
        assert!(paths.contains::<&Path>(&result.0.as_ref()));
        assert!(result.1.is_none());

        let result = walkpaths.next();
        assert!(result.is_none());
    }

    #[cfg(unix)]
    #[test]
    fn test_skip_special_devices() {
        let path = String::from("/dev/null");
        let paths = vec![&path];

        let mut walkpaths = WalkPaths::new(paths);

        let result = walkpaths.next();
        assert!(result.is_some());
        let result = result.unwrap();

        assert_eq!(result.0, PathBuf::from(path));
        assert!(result.1.is_some());
    }
}
