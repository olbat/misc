use std::process;

use rgrep::cli;

fn main() {
    process::exit(match cli::run() {
        Ok(true) => 0,
        Ok(false) => 1,
        Err(err) => {
            eprintln!("{}", err);
            match err.downcast_ref::<cli::ArgError>() {
                Some(cli::ArgError::Usage) => 0,
                Some(_) => 2, // Argument errors
                None => 3,    // Other type of errors
            }
        }
    })
}
