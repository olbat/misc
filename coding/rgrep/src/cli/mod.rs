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

    search::search(&args.pattern, paths, &args.options)

    // TODO: finish implementation
    //if args.options.quiet {
    //} else {
    //    // TODO: use closure
    //    results::print_results(search::search(&args.pattern, paths, &args.options))
    //}
}
