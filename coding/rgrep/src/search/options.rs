use crate::cli::Options as CliOptions;

#[derive(Default)]
pub struct Options {}

impl Options {
    pub fn new() -> Self {
        Default::default()
    }
}

impl From<&CliOptions> for Options {
    fn from(_opts: &CliOptions) -> Self {
        Options::new()
    }
}
