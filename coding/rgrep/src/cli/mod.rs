use std::convert::TryFrom;
use std::env;
use std::error;
use std::io;

use crate::search;
use crate::walkpaths;

mod args;
pub use args::ArgError;
pub use args::Args;
mod options;
pub use options::Options;
mod print;

use crate::search::Options as SearchOptions;

pub fn run() -> Result<bool, Box<dyn error::Error>> {
    let args: Args = Args::try_from(env::args())?;

    let search_options = SearchOptions::from(&args.options);

    if args.options.read_from_stdin {
        let results = search::search_file(&args.pattern, io::stdin(), &search_options);
        let path = "<stdin>".as_ref();
        Ok(print::print_matches(path, results, &args.options))
    } else {
        let walkpaths = walkpaths::WalkPaths::new(args.paths);
        let results = search::search_paths(&args.pattern, walkpaths, &search_options);
        Ok(print::print_results(results, &args.options))
    }
}
