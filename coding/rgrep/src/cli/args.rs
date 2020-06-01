use crate::Options;

use std::collections::VecDeque;
use std::convert::TryFrom;
use std::env;
use std::error;
use std::fmt;

pub const USAGE: &str = "usage: rgrep [options] <pattern> [<path1> <path2> ..]

options:
  -q, --quiet\t\tRun in quiet mode (do not display any results)
  -h, --help\t\tDisplay the help message
";

// TODO: switch to a struct where we could save the position of the argument?
#[derive(Debug)]
pub enum ArgError {
    UnknownOption,
    MissingArgument,
    Usage, // technically not really an error but very convinient
}

impl fmt::Display for ArgError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut errmsg = String::new();
        if !matches!(self, ArgError::Usage) {
            let err = match self {
                ArgError::UnknownOption => "unknown option",
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

        let (mut pos_args, opts) = Self::parse_opts(args)?;

        if pos_args.is_empty() {
            return Err(ArgError::MissingArgument);
        }

        let pattern = pos_args.pop_front().unwrap();
        let paths = Vec::from(pos_args);

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
