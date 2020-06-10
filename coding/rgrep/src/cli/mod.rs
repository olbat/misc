use std::convert::TryFrom;
use std::env;
use std::error;

use crate::search;
use crate::walkpaths;

mod args;
pub use args::ArgError;
pub use args::Args;
mod print;

pub fn run() -> Result<bool, Box<dyn error::Error>> {
    let args: Args = Args::try_from(env::args())?;

    let walkpaths = walkpaths::WalkPaths::new(args.paths);

    let results = search::search_paths(&args.pattern, walkpaths, &args.options);

    Ok(print::print_results(results, &args.options))
}
