# rgrep

## About
Fast & simple Rust implementation of the grep utility with recursive directory search support.

Optionally uses SIMD optimizations via the `twoway` crate.

## Usage
```
$ cargo build --release
$ ./target/release/rgrep [OPTIONS] PATTERN [PATH...]
```
