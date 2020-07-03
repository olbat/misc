use super::Options;

use std::collections::VecDeque;
use std::convert::TryFrom;
use std::env;
use std::error;
use std::fmt;

pub const USAGE: &str = "usage: rgrep [options] <pattern> [<path1> <path2> ..]

options:
  -q, --quiet\t\tRun in quiet mode (do not display any results)
  -h, --help\t\tDisplay the help message
  - , --stdin\t\tRead from standard input
";

// TODO: switch to a struct where we could save the position of the argument?
#[derive(Debug, PartialEq)]
pub enum ArgError {
    UnknownOption,
    BothPathsAndStdin,
    MissingArgument,
    Usage, // technically not really an error but very convinient
}

impl fmt::Display for ArgError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut errmsg = String::new();
        if !matches!(self, ArgError::Usage) {
            let err = match self {
                ArgError::UnknownOption => "unknown option",
                ArgError::BothPathsAndStdin => "cannot search both paths and stdin",
                ArgError::MissingArgument => "missing argument",
                _ => panic!("unknown error type"),
            };
            errmsg.push_str(&format!("Argument error: {}\n\n", err));
        }
        write!(f, "{}{}", errmsg, USAGE)
    }
}

impl error::Error for ArgError {}

pub struct Args {
    pub pattern: String,
    pub paths: Vec<String>,
    pub options: Options,
}

impl TryFrom<env::Args> for Args {
    type Error = ArgError;

    fn try_from(args: env::Args) -> Result<Args, Self::Error> {
        let mut args: VecDeque<String> = args.collect();
        Ok(Args::parse_args(&mut args)?)
    }
}

impl Args {
    fn new(pattern: String, paths: Vec<String>, options: Option<Options>) -> Args {
        Args {
            pattern,
            paths,
            options: options.unwrap_or_else(Default::default),
        }
    }

    fn parse_args(args: &mut VecDeque<String>) -> Result<Args, ArgError> {
        args.pop_front(); // program name

        let (mut pos_args, mut opts) = Self::parse_opts(args)?;

        if pos_args.is_empty() {
            return Err(ArgError::MissingArgument);
        }

        let pattern = pos_args.pop_front().unwrap();
        let paths = Vec::from(pos_args);

        if paths.is_empty() {
            opts.read_from_stdin = true;
        } else if opts.read_from_stdin {
            return Err(ArgError::BothPathsAndStdin);
        }

        Ok(Self::new(pattern, paths, Some(opts)))
    }

    fn parse_opts(args: &mut VecDeque<String>) -> Result<(VecDeque<String>, Options), ArgError> {
        let mut pos_args: VecDeque<String> = VecDeque::new(); // positional argument
        let mut opts: Options = Options::new();

        // iterate on slice, pass iterator as argument to set_opt (use DeQue?)
        while let Some(arg) = args.pop_front() {
            let mut charsit = arg.chars();

            match charsit.next().unwrap_or_default() {
                // leading \: escape path name starting with an '-'
                '\\' => pos_args.push_back(charsit.collect::<String>()),

                // leading '-': options
                '-' => {
                    match charsit.next() {
                        // '-' alone: read from stdin
                        None => opts.read_from_stdin = true,

                        // double '-': long option
                        Some('-') => {
                            Self::set_long_opt(&mut opts, &charsit.collect::<String>(), args)?
                        }

                        // single '-': short option
                        Some(c) => Self::set_short_opt(&mut opts, c, args)?,
                    }
                }

                // empty string: nothing to do (should never happen)
                '\x00' => panic!("args contains an empty string"),

                // else: path name
                _ => pos_args.push_back(arg),
            }
        }

        Ok((pos_args, opts))
    }

    fn set_short_opt(
        opts: &mut Options,
        c: char,
        _args: &mut VecDeque<String>,
    ) -> Result<(), ArgError> {
        match c {
            'h' => Err(ArgError::Usage),
            'q' => {
                opts.quiet = true;
                Ok(())
            }
            _ => Err(ArgError::UnknownOption),
        }
    }

    fn set_long_opt(
        opts: &mut Options,
        s: &str,
        _args: &mut VecDeque<String>,
    ) -> Result<(), ArgError> {
        match s {
            "help" => Err(ArgError::Usage),
            "quiet" => {
                opts.quiet = true;
                Ok(())
            }
            "stdin" => {
                opts.read_from_stdin = true;
                Ok(())
            }
            _ => Err(ArgError::UnknownOption),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn call_parse_args(args: &[&str]) -> Result<Args, ArgError> {
        let mut args: VecDeque<String> = args.iter().map(|s| s.to_string()).collect();
        Args::parse_args(&mut args)
    }

    #[test]
    fn no_path_no_opt() {
        let args = ["rgrep", "pattern"];
        let res = call_parse_args(&args);

        assert!(res.is_ok());
        let args = res.unwrap();

        assert_eq!(args.pattern, "pattern");
        assert!(args.paths.is_empty());
        assert_eq!(args.options.read_from_stdin, true);
    }

    #[test]
    fn one_path_no_opt() {
        let args = ["rgrep", "pattern", "path"];
        let res = call_parse_args(&args);

        assert!(res.is_ok());
        let args = res.unwrap();

        assert_eq!(args.pattern, "pattern");
        assert_eq!(args.paths, vec!["path"]);
    }

    #[test]
    fn multiple_paths_no_opt() {
        let args = ["rgrep", "pattern", "path1", "path2", "path3"];
        let res = call_parse_args(&args);

        assert!(res.is_ok());
        let args = res.unwrap();

        assert_eq!(args.pattern, "pattern");
        assert_eq!(args.paths, vec!["path1", "path2", "path3"]);
    }

    #[test]
    fn parse_stdin_when_no_path() {
        let args = ["rgrep", "pattern"];
        let res = call_parse_args(&args);

        assert!(res.is_ok());
        let args = res.unwrap();

        assert_eq!(args.pattern, "pattern");
        assert!(args.paths.is_empty());
        assert_eq!(args.options.read_from_stdin, true);
    }

    #[test]
    fn parse_single_short_opt() {
        let args = ["rgrep", "pattern", "-q", "path"];
        let res = call_parse_args(&args);

        assert!(res.is_ok());
        let args = res.unwrap();

        assert_eq!(args.pattern, "pattern");
        assert_eq!(args.paths, vec!["path"]);
        assert_eq!(args.options.quiet, true);
    }

    #[test]
    fn parse_multi_short_opt() {
        // TODO: add another option in the test when there will be one available
        let args = ["rgrep", "-q", "pattern", "path"];
        let res = call_parse_args(&args);

        assert!(res.is_ok());
        let args = res.unwrap();

        assert_eq!(args.pattern, "pattern");
        assert_eq!(args.paths, vec!["path"]);
        assert_eq!(args.options.quiet, true);
    }

    #[test]
    fn parse_single_long_opt() {
        let args = ["rgrep", "pattern", "--quiet", "path"];
        let res = call_parse_args(&args);

        assert!(res.is_ok());
        let args = res.unwrap();

        assert_eq!(args.pattern, "pattern");
        assert_eq!(args.paths, vec!["path"]);
        assert_eq!(args.options.quiet, true);
    }

    #[test]
    fn parse_multi_long_opt() {
        // TODO: add another option in the test when there will be one available
        let args = ["rgrep", "--quiet", "pattern", "path"];
        let res = call_parse_args(&args);

        assert!(res.is_ok());
        let args = res.unwrap();

        assert_eq!(args.pattern, "pattern");
        assert_eq!(args.paths, vec!["path"]);
        assert_eq!(args.options.quiet, true);
    }

    #[test]
    fn parse_help_opt() {
        let args = ["rgrep", "--help", "pattern", "path"];
        let res = call_parse_args(&args);

        assert!(res.is_err());
        assert_eq!(res.err(), Some(ArgError::Usage));
    }

    #[test]
    fn parse_unknown_opt_err() {
        let args = ["rgrep", "--unknown-option", "pattern", "path"];
        let res = call_parse_args(&args);

        assert!(res.is_err());
        assert_eq!(res.err(), Some(ArgError::UnknownOption));
    }

    #[test]
    fn parse_missing_argument_err() {
        let args = ["rgrep"];
        let res = call_parse_args(&args);

        assert!(res.is_err());
        assert_eq!(res.err(), Some(ArgError::MissingArgument));
    }

    #[test]
    fn parse_both_path_and_stdin_err() {
        let args = ["rgrep", "pattern", "path", "-"];
        let res = call_parse_args(&args);

        assert!(res.is_err());
        assert_eq!(res.err(), Some(ArgError::BothPathsAndStdin));
    }
}
