# Braille Generator

A configurable OpenJSCAD script for creating Braille text from strings. Can be used for printing dots only on surfaces or creating braille labels (with a backplate).

# Usage

You can render this script in following ways:
* Use the OpenJsCad parser, provided by https://joostn.github.io/OpenJsCad/processfile.html
* Use the adapted frontend (in German) for easier use: https://benjaminaigner.github.io/braillegenerator/index.html 

## Parameters

* enable backplate: If set, a 2mm sheet will be created, on which the braille dots are located
* enable support: If set, 2 additional small cubes are created, to stabilize the backplate while printing
* text: Enter a text. New lines can be created by entering `\n`. A backslash must be escaped: `\\`
