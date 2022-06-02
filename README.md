# Just Another Music Generator

This software generates algorithmic music based on cellular automata.

## Platform
This software was developed using Python 3.9 on MacOS Monterey 12.3.1.
It probably works on other platforms and/or versions, but this cannot be guaranteed.

## Installation
* Setup a virtual environment (if you don't know what this is, please google it)

* Run the following within virtual environment:
```commandline
python setup.py install
```

## CLI usage
On command line, type
```commandline
just-another-music-generator
```

to generate an audio sequence and store it as a numpy file. 
The file can be found at `/tmp/tmp.npy`.
```commandline
just-another-music-generator --help
```
to discover how to use the CLI.

## To develop
Install dependencies:

```commandline
pip install -r requirements.txt
```
