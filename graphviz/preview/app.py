#!/usr/bin/env python3
from flask import Flask
import subprocess
import base64
app = Flask(__name__)

@app.route("/<string:type>/<path:name>")
def getMemberPath(type, name):
    dot = subprocess.run(["dot", "-T" + type, name], capture_output=True)
    errortext = ""
    if dot.stderr:
        errortext = '<p>' + dot.stderr.decode('utf-8') + '</p>'
    return f"<html><head><title>Graphviz</title><meta http-equiv=\"refresh\" content=\"10\"/></head><body><img src=\"data:image/{type if not type == 'svg' else 'svg+xml'};base64,{base64.b64encode(dot.stdout).decode('ascii')}\"/>{errortext}</body></html>"

if __name__ == "__main__":
    app.run()