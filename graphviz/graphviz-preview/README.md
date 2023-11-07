# Graphviz Previewer
## Description
Preview a graphviz file you're working on by rendering an automatically updating webpage with the rendered image embeded. Also shows error messages!

## Dependencies
- Python3
- Flask
- Waitress
- Graphviz

## Usage
To execute, run:
```
$ python3 ./app.py
```

To view, access the following in your browser, where engine is one of dot, neato, twopi, circo, fdp, sfdp, patchwork, or osage, type is the graphviz format (eg. svg or png) and file is the graphviz file name in the same or deeper directory:
```
http://localhost:8080/ENGINE/TYPE/FILE
```
