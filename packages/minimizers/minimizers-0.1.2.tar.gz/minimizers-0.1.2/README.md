# minimizers

A Python package for extracting minimizers from sequence data.

## Requirements

The package requires Python 3 and there are no constraints on the type of operating system.

It also requires the [biopython](https://pypi.org/project/biopython/) package.

## Install

It can be installed with `pip` by typing the following command in your terminal:

```
pip install minimizers
```

## How to use it

Run `minimizers --help` for a list of available arguments:

```
usage: minimizers [-h] [-a] -i INPUT [-o OUTPUT] [-t {list,fasta}] -s SIZE -w
                  WINDOW [--report-counts] [--top-perc TOP_PERC]
                  [--top-num TOP_NUM] [-n NPROC] [--verbose] [-v]

Extract the set of minimizers from a sequence file

optional arguments:
  -h, --help            show this help message and exit
  -a, --aggregate       Aggregate record results (default: False)
  -i INPUT, --input INPUT
                        Path to the input sequence file in fasta format. It
                        can be Gzip compressed (default: None)
  -o OUTPUT, --output OUTPUT
                        Path to the output file with minimizers. Results are
                        printed on the stdout if no output is provided
                        (default: None)
  -t {list,fasta}, --output-type {list,fasta}
                        The output can be formatted as a list of kmers or as a
                        fasta file (default: list)
  -s SIZE, --size SIZE  Length of the minimizers (default: None)
  -w WINDOW, --window WINDOW
                        Size of the sliding window. It must be greater than
                        the minimizer size (default: None)
  --report-counts       Report the frequencies of the minimizers. This is
                        compatible with "--output-type list" only (default:
                        False)
  --top-perc TOP_PERC   Report the top percentage of minimizers based on their
                        frequency (default: None)
  --top-num TOP_NUM     Report the top number of minimizers based on their
                        frequency (default: None)
  -n NPROC, --nproc NPROC
                        Make it parallel (default: 1)
  --verbose             Print messages on the stdout (default: False)
  -v, --version         Print the "minimizers" version and exit
```

Copyright © 2022 [Fabio Cumbo](https://github.com/cumbof). See [LICENSE](https://github.com/cumbof/minimizers/blob/main/LICENSE) for additional details.
