use std::convert::TryFrom;
use std::env;
use std::error;

use crate::search;

mod args;
pub use args::ArgError;
pub use args::Args;
mod results;

pub fn run() -> Result<bool, Box<dyn error::Error>> {
    let args: Args = Args::try_from(env::args())?;

    let paths = args.paths.iter().map(String::as_str);

    let results_by_file = search::search(&args.pattern, paths, &args.options);

    let mut any_match = false;

    for (filepath, results) in results_by_file {
        any_match |= results::print_results(filepath.as_ref(), results, &args.options);
    }

    Ok(any_match)
}
