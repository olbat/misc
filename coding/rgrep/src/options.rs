#[derive(Default)]
pub struct Options {
    pub read_from_stdin: bool,
    pub quiet: bool,
}

impl Options {
    pub fn new() -> Self {
        Default::default()
    }
}
