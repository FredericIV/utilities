#!/usr/bin/env python3
from flask import Flask, request, render_template_string
import subprocess
import base64
import os
import xml.etree.ElementTree as ET
import mimetypes
import gzip

app = Flask(__name__)
datadir = os.environ.get('GRAPHVIZ_DATADIR', './')
page_template = '''<!doctype html>
<html>
    <head>
        <title>Graphviz</title>
        <meta http-equiv=\"refresh\" content=\"120\"/><meta http-equiv=\"cache-control\" content=\"no-cache\"/>
    </head>
    <body>
        {{embed|safe}}
        {{errortext|safe}}
    </body>
</html>
'''
welcome_embed = '''<h1>Graphviz web preview</h1>
<h3>Usage</h3>
<p>
    <code>http(s)://host/ENGINE/TYPE/FILE?ARG</code>
</p>
<ul>
    <li>Engine is one of dot, neato, twopi, circo, fdp, sfdp, patchwork, or osage.</li>
    <li>Type is generally png or svg for best results. See the <a href=\"https://graphviz.org/docs/outputs/\">docs</a> for more formats.</li>
    <li>File is the path to your file (current directory or lower).</li>
    <li>Arg is zero or more of raw=(true|false), embed=(true|false) separated by &</li>
</ul>'''

@app.route("/")
def welcome():
    return render_template_string(page_template, embed=welcome_embed)

@app.route("/favicon.ico")
def favicon_path():
    return app.response_class(
        response=base64.b64decode(gzip.decompress(base64.b64decode('H4sIAFDkMmUA/+1WQU+GMAz9QR56kcjFw4NNhMQAR88keDB+R5d8v562RGbmZ7LIJH5x79DspaOPdV03ABVg0VQvPLRoUbf1CDwIrcXgWcyTGPV/4HUbZfx18BYzSjGDWEMyJLePazwbo2/ky916l3mUvp+fEP5/rk1/Pdg/ynfn9XasnzsMcA7iK38M5of+tZST5F97Wq/x332Pu5ifwJ9w/xs9n6r3CUF+vvgPqT9db/t9/Out/6yf9f+V/u/dv9o/494fd4n1NV7U+yPjOBgiKsGGMLBxhu+uCbdys/czFc6c6GZCAZzQj+icebMN87NhPhebn0i4nx/wNR5Xlgv1cL8Ah4KBztQMAAA=')).decode('utf-8')),
        status=200,
        mimetype='image/vnd.microsoft.icon'
    )

@app.route("/robots.txt")
def robots_path():
    return "User-agent: *\nDisallow: /\n"

@app.errorhandler(404)
def errorhandler(e):
    return render_template_string(page_template, embed=welcome_embed, errortext=f"<p><b>Error 404<b></p>"), 404

@app.route("/<string:engine>/<string:imgtype>/<path:name>")
def getMemberPath(engine, imgtype, name):
    if engine not in ["dot", "neato", "twopi", "circo", "fdp", "sfdp", "patchwork", "osage"]:
        return render_template_string(page_template, embed=f"<p>Provide a valid engine (one of dot, neato, twopi, circo, fdp, sfdp, patchwork, or osage)</p>"), 400
    if imgtype not in ["canon", "cmap", "cmapx", "cmapx_np", "dot", "dot_json", "eps", "fig", "gv", "imap", "imap_np", "ismap", "json", "json0", "mp", "pdf", "pic", "plain", "plain-ext", "png", "pov", "ps", "ps2", "svg", "svgz", "tk", "vdx", "vml", "vmlz", "webp", "x11", "xdot", "xdot1.2", "xdot1.4", "xdot_json", "xlib"]:
        return render_template_string(page_template, embed=f"<p>Provide a valid filetype. The most common/well supported are svg and png.</p>"), 400
    dot = subprocess.run([engine, "-T" + imgtype, name], capture_output=True, cwd=datadir)
    errortext = ""
    if dot.stderr:
        errortext = '<p>' + dot.stderr.decode('utf-8') + '</p>'
        if not dot.stdout:
            return render_template_string(page_template, embed=errortext), 400
    match imgtype:
        case "pdf":
            if request.args.get('raw') == "true":
                return app.response_class(
                        response=dot.stdout,
                        status=200,
                        mimetype='application/pdf'
                       )
            else:
                image = base64.b64encode(dot.stdout).decode('utf-8')
                embed = f"<object data=\"data:application/pdf;base64,{image}\" type=\"{mimetypes.guess_type('test.'+imgtype, strict=False)[0]}\"><p>Unable to display PDF file. <a href=\"data:{mimetypes.guess_type('test.'+imgtype, strict=False)[0]};base64,{image}\">Download</a> instead.</p></object>"
        case "svg":
            if request.args.get('embed', default="true") == "false":
                svgstring = dot.stdout
            else:
                svgroot = ET.fromstring(dot.stdout)
                ns = {'svg': 'http://www.w3.org/2000/svg', 'xlink': 'http://www.w3.org/1999/xlink'}
                for image_element in svgroot.findall(".//svg:image", ns):
                    filepath = os.path.join(datadir, image_element.attrib["{http://www.w3.org/1999/xlink}href"])
                    if os.path.isfile(filepath):
                        with open(filepath, 'rb') as file:
                            image_element.set('{http://www.w3.org/1999/xlink}href', "data:"+ mimetypes.guess_type(filepath, strict=False)[0] + ";base64," + base64.b64encode(file.read()).decode('utf-8'))
                svgstring = ET.tostring(svgroot)
            if request.args.get('raw') == "true":
                return app.response_class(
                        response=svgstring,
                        status=200,
                        mimetype='image/svg+xml'
                    )
            else:
                image = base64.b64encode(svgstring).decode('utf-8')
                embed = f"<img src=\"data:image/svg+xml;base64,{image}\"/>"
        case "dot":
            if request.args.get('raw') == "true":
                return app.response_class(
                        response=dot.stdout,
                        status=200,
                        mimetype='text/plain'
                    )
            else:
                embed = f"<p>{dot.stdout.decode('utf-8')}</p>"
        case "json":
            if request.args.get('raw') == "true":
                return app.response_class(
                        response=dot.stdout,
                        status=200,
                        mimetype='application/json'
                    )
            else:
                embed = f"<p>{dot.stdout.decode('utf-8')}</p>"
        case _:
            if request.args.get('raw') == "true":
                return app.response_class(
                        response=dot.stdout,
                        status=200,
                        mimetype=mimetypes.guess_type('test.'+imgtype, strict=False)[0]
                    )
            else:
                image = base64.b64encode(dot.stdout).decode('utf-8')
                embed = f"<img src=\"data:{mimetypes.guess_type('test.'+imgtype, strict=False)[0]};base64,{image}\"/>"
    return render_template_string(page_template, embed=embed, errortext=errortext)

if __name__ == "__main__":
    from waitress import serve
    import logging
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO) # TODO: add request logging
    serve(app, listen=os.environ.get('GRAPHVIZ_HOST', '*')+":"+os.environ.get('GRAPHVIZ_PORT', '8080'))

