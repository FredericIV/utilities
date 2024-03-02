# Excel/LibreOffice Calc Barcode Generator
Utilizing a single cell, generate a code128c barcode with the help of the [Libre Barcode Font Project](https://graphicore.github.io/librebarcode/). Due to limitations of cell formulas and the design goal of using a single cell without special formatting, the length of the barcode must be hardcoded.

## Usage
```
usage: text.py [-h] [-t {code128c}] [-n NUMCHARS] [-p PADDING] [-d {left,right}] field

positional arguments:
  field                 Field to be evaluated for generating the barcode.

options:
  -h, --help            show this help message and exit
  -t {code128c}, --type {code128c}
                        Barcode symbology to generate. Only code128c is supported at the moment. Defaults to code128c.
  -n NUMCHARS, --numchars NUMCHARS
                        Number of characters in barcode. Code128c supports only even numbers. Defaults to 8.
  -p PADDING, --padding PADDING
                        Padding character. Ensure the character is supported by the symbology. Defaults to 0.
  -d {left,right}, --paddingDirection {left,right}
                        Direction to pad barcode. Defaults to left.
```
Warning: LibreOffice Calc seems to support a maximum barcode length of 24 due to the formula exceeding 8192 tokens.

Generally the field would look like `A2`, but it may also be a SharePoint column `[Barcode]`, an explicit value `200`, or a calculated value `A2+100000`. The latter is a convenient way to add a prefix.