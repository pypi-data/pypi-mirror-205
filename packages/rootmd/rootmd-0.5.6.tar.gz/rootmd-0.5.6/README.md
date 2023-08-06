
# RootMD 🩺 👩🏼‍⚕️

Scientific reports/literate programming tool for CERN ROOT and c++. RootMD is a markdown (and other format) processor for mark up with ROOT-flavored c++ code. RootMD can execute c++ code and inject the output (from stdout, stderr) and link or embed image outputs. Provides a format for producing code + result for better documentation / notes. This is by design not a jupyter notebook, e.g. not a REPL-like environment. If you like Jupyter notebooks then use that :). 

## Features
- execute c++ code blocks via ROOT REPL
- capture stdout, stderr and inject into output
- embed (base64) or link to any image files produced 
- output to HTML, Markdown (or obsidian flavored markdown), or as a presentation (via Marp)
- execute html, css, javascript code blocks (for html output) to customize output

## usage
```sh
usage: rootmd [-h] [--output OUTPUT]
              [--format {html,md,obsidian,json,terminal}] [--embed]
              [--asset-dir ASSET_DIR] [--verbosity VERBOSITY]
              [--watch WATCH] [--run RUN] [--clean] [--no-exec]
              input

Convert Markdown with inline c++ code to ROOT output.

positional arguments:
  input                 input Markdown file to execute and convert

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT       output filename default <input>.<ext> where <ext>
                        is determined by the chosen format, default html
  --format {html,md,obsidian,json,terminal}
                        output format
  --embed               embed images as base 64
  --asset-dir ASSET_DIR
                        specify asset output directory, paths are NOTE re-
                        written to support unless using obsidian format
  --verbosity VERBOSITY
                        specify log verbosity
  --watch WATCH         watch a file or directory for changes
  --run RUN             command to run after processing a file. The
                        filename can be substituted into the command string
                        with {{file}}. Example: --run="echo {{file}}"
  --clean               clean artifacts, caution - should only use with
                        embed or asset copy to <asset-dir>
  --no-exec             Do not execute any code blocks, just process file
                        (useful for viewing and testing conversion)

```


## TODO
- [x] make it a python package (so that it can be installed via pip)
  - [x] Look into poetry
  - [x] start versioning
- [x] support output verbosity levels 
  - & make output useful
- Add comment for input block identification upon processing
- [x] add watch functionality for reprocessing a file on change
  - [ ] Add some additional features
  - [ ] Handle watch of multiple files, and how output filename should be named
- [x] Add terminal output using rich pretty output package
  - consider iterm image support? [See here](https://iterm2.com/documentation-images.html)
  - [x] Basically, markdown output on the terminal : using rich
- [x] Add prismjs for inline code
- test some failure modes when root code has errors leading to hang
- [x] add mathjax to html output for inline mathematics
- [x] "import" source files into output? So that you can write code in separate file but sow it in the output?
  - add as a block option
- support for other "languages", e.g. shell
- support for ROOTJS in HTML output
  - embed histogram as JSON object in HTML
- [x] clean assets in embed mode or other output path
- download + embed external JS for fully contained, offline ready single file HTML output
- [x] Load HTML / CSS defaults from a file in the package
- [x] Better style HTML output (input / output cells more like Jupyter)
  - Consider adding JS for collapsing headings, output blocks etc.
- [ ] add format option to output a ROOT macro with markdown and output converted to comments
- [x] integrate usage of RNUplot for graphical output!
- [x] implement an auto-draw so that you dont have to "Print(...)" every block
- [ ] block option: run code block as a "macro" 
  - [x] You can already use .L, .x
- [ ] move ROOT executor into member not superclass
- [ ] auto-draw dont do it for cells without any drawing!
- [x] PDF support
- [ ] Better PDF embed (link to file) (for Firefox especially) using canvas : https://stackoverflow.com/questions/2104608/hiding-the-toolbars-surrounding-an-embedded-pdf
- [ ] Embed PDF base64 in object tag
## Feature wish list
- Cache blocks of code for faster rerun
- server for "sharing" of documents, from command line - use secret links
- Technique for RAW output? 
  - i.e. write out HTML Table or markup
- inline code replacement, e.g. "We ran `TString::Format("%d",tree->GetEntries())` events."

## Improve ROOT?
- Apply some default style options
- 

## Known issues
- watch isnt working, especially when input not given
- something is surely broken
### ROOT REPL issues
ROOT REPL struggles with multi-line code:
- function definitions with "{" on next line does not work since it doesn't understand
```cpp
void hello() {
  // this works
}

void world() 
{
  // this DOES NOT work
}
```



## Dependencies
RootMD itself is a pure python package which uses:
- [mistletoe](https://github.com/miyuchina/mistletoe) : python markdown parser and processor
- [rich](https://github.com/Textualize/rich) : Rich for pretty terminal output
- pyyaml : for parsing yaml front matter
- Dependencies for HTML output
  - [prismjs](https://prismjs.com/) for syntax highlighting in HTML output
  - [mathjax](https://www.mathjax.org/) for rendering mathematics
- [ROOT](https://root.cern.ch/) : installed on system and available on PATH



## Example : see [example_in.md](example_in.md) and [example.md](example.md)
This is a simple example of markdown processed by RootMD.
You can include any c++ code that ROOT can handle. For instance (using ROOT6)
this part of the file was processed with
```sh
rootmd example_in.md -f md -o example.md

```

```cpp
cout << "Hello from ROOT (stdout)" << endl;
cerr << "Hello from ROOT (stderr)" << endl;

```
```sh
# Block [0]
Hello from ROOT (stdout)
Hello from ROOT (stderr)

```

```cpp
TH1 * h1 = new TH1F( "hGaus", ";x;counts", 100, -5, 5 );
h1->FillRandom( "gaus", 10000 );
h1->Draw( "pe" );
h1->Draw( "same hist" );
gPad->Print( "h1.svg" );

```
```sh
# Block [1]
Info in <TCanvas::MakeDefCanvas>:  created default TCanvas with name c1
Info in <TCanvas::Print>: SVG file h1.svg has been created

```

![h1.svg](h1.svg)