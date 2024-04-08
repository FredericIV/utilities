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

## Example
`python3 app.py -t code128c -n 8 -p "0" -d left A2`
Which is equivalent to `python3 app.py A2`, the result of which is included as `example.txt`. The output can be copied into a cell, which will convert the value in `A2` to the output necessary to be rendered as a barcode when in the LibreBarcode Code128 font, padding left with zeros. The cell can be expanded/dragged to neighbors as with a normal formula.

## Implementation details
### Code128C
The formula operates in four parts:
1) Startcode C "Í"
2) 1) Pad the number
   2) Break the number into two digit segments
   3) Break into <25, <50, <75, and <100. This gets around the max choose length in LibreOffice of 30. Choose is used for backwards compatibility instead of using switch.
   4) Conduct lookup, e.g. 1 == !
3) 1) [Calculate checksum](https://www.barcodefaq.com/1d/code-128/#CalculationExamples)
   2) Conduct lookup (See 2.2 and 2.3)
4) Stopcode "Î"

## Special note for SharePoint
Due to internal limits of 2019 and 365 editions of Sharepoint, the formula needs to be split into pieces depending on the number of barcode characters. An example with eight characters is in example-sharepoint.txt using the fields `Barcode` for the string to convert, `BarcodeCalcA` for the first half, `BarcodeCalcB` for the second half, and `BarcodePrint` for the result.
