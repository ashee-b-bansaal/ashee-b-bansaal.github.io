"""Edit the portfolio in your browser.

    python3 src/editor.py

Opens the site with an edit mode: click any text to change it, then Save.
Changes are written straight into content.py (comments and layout kept) and the
site is rebuilt. Runs only on your own machine (127.0.0.1); the published site
never includes the editor.
"""
import ast
import base64
import io
import json
import os
import re
import shutil
import subprocess
import sys
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)  # repo root, where the built site lives
CONTENT = os.path.join(HERE, "content.py")
PHOTOS = os.path.join(SITE, "photos")
EDITABLE = {"NAME", "TAGLINE", "ABOUT_HEAD", "ABOUT", "SEEKING", "EPIGRAPHS", "TITLES",
            "EXPERIENCE", "PROJECTS", "HOBBIES", "SKILLS", "EDU"}
NEW_PROJECT = '''dict(
        name="New project",
        subtitle="One line about it",
        link="#",
        image="",
        fit="contain",
        text="What it is, what you built, and the result.",
        details=[("Tech Stack", "Python, React")],
        buttons=[("GitHub", "#")],
    )'''


# ── editing content.py through its syntax tree ──────────────────────────────

class Src:
    """content.py as bytes, with helpers to find and replace pieces of it."""

    def __init__(self):
        self.b = open(CONTENT, "rb").read()

    def tree(self):
        return ast.parse(self.b)

    def span(self, node):
        starts = [0]
        for line in self.b.splitlines(keepends=True):
            starts.append(starts[-1] + len(line))
        return (starts[node.lineno - 1] + node.col_offset,
                starts[node.end_lineno - 1] + node.end_col_offset)

    def splice(self, start, end, text):
        self.b = self.b[:start] + text.encode() + self.b[end:]

    def find(self, path):
        """Return (node, parent) for a path like ["PROJECTS", 2, "text"]. node is None if a dict key is missing."""
        if path[0] not in EDITABLE:
            raise ValueError(f"{path[0]} can't be edited here")
        node = next((n.value for n in self.tree().body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == path[0] for t in n.targets)), None)
        if node is None:
            raise ValueError(f"{path[0]} not found in content.py")
        parent = None
        for seg in path[1:]:
            parent = node
            if isinstance(node, (ast.List, ast.Tuple)):
                node = node.elts[int(seg)]
            elif isinstance(node, ast.Call):  # dict(key=...)
                node = next((k.value for k in node.keywords if k.arg == seg), None)
            elif isinstance(node, ast.Dict):
                node = next((v for k, v in zip(node.keys, node.values)
                             if isinstance(k, ast.Constant) and k.value == seg), None)
            else:
                raise ValueError(f"can't follow {'.'.join(map(str, path))}")
            if node is None:
                return None, parent
        return node, parent

    def set(self, path, value):
        node, parent = self.find(path)
        literal = json.dumps(value, ensure_ascii=False)  # a valid Python string literal
        if node is None:  # e.g. a project without "focus" yet: add the keyword
            if not isinstance(parent, ast.Call) or not parent.keywords:
                raise ValueError(f"can't add {'.'.join(map(str, path))}")
            _, end = self.span(parent.keywords[-1].value)
            self.splice(end, end, f",\n        {path[-1]}={literal}")
            return
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            raise ValueError(f"{'.'.join(map(str, path))} isn't text")
        self.splice(*self.span(node), literal)

    def projects(self):
        node, _ = self.find(["PROJECTS"])
        return node.elts

    def project_op(self, op, i):
        elts = self.projects()
        text = lambda n: self.b[slice(*self.span(n))].decode()
        if op in ("up", "down"):
            j = i - 1 if op == "up" else i + 1
            if not 0 <= j < len(elts):
                return
            a, b = sorted((i, j))
            ta, tb = text(elts[a]), text(elts[b])
            self.splice(*self.span(elts[b]), ta)  # later one first so offsets stay valid
            self.splice(*self.span(elts[a]), tb)
        elif op == "duplicate":
            _, end = self.span(elts[i])
            self.splice(end, end, ",\n    " + text(elts[i]))
        elif op == "new":
            _, end = self.span(elts[-1])
            self.splice(end, end, ",\n    " + NEW_PROJECT)
        elif op == "delete":
            if len(elts) == 1:
                raise ValueError("can't delete the only project")
            if i + 1 < len(elts):
                self.splice(self.span(elts[i])[0], self.span(elts[i + 1])[0], "")
            else:
                self.splice(self.span(elts[i - 1])[1], self.span(elts[i])[1], "")
        else:
            raise ValueError(f"unknown action {op}")


def save_image(i, name, data_url):
    """Store an uploaded image in photos/ (resized, metadata such as GPS removed)."""
    raw = base64.b64decode(data_url.split(",", 1)[1])
    stem = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(name)[0].lower()).strip("-")[:40] or f"project-{i}"
    os.makedirs(PHOTOS, exist_ok=True)
    try:
        from PIL import Image, ImageOps
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw)))
        im.thumbnail((1800, 1800))
        screenshot = im.mode in ("RGBA", "LA", "P") or name.lower().endswith(".png")
        ext = ".png" if screenshot else ".jpg"
        out = os.path.join(PHOTOS, stem + ext)
        if screenshot:
            im.save(out, "PNG", optimize=True)
        else:
            im.convert("RGB").save(out, "JPEG", quality=84, optimize=True, progressive=True)
    except ImportError:  # no Pillow: keep the file as-is
        ext = os.path.splitext(name)[1].lower() or ".jpg"
        out = os.path.join(PHOTOS, stem + ext)
        open(out, "wb").write(raw)
    return "photos/" + os.path.basename(out)


def parse_path(s):
    parts = s.split(".")
    if not all(re.fullmatch(r"[A-Za-z_]\w*|\d+", p) for p in parts):
        raise ValueError(f"bad path {s}")
    return [int(p) if p.isdigit() else p for p in parts]


def apply(payload):
    src = Src()
    for e in payload.get("edits", []):  # text first, while indices still match the page
        src.set(parse_path(e["path"]), e["value"])
    for op in payload.get("ops", []):
        i = int(op.get("i", 0))
        if op["op"] == "image":
            src.set(["PROJECTS", i, "image"], save_image(i, op["name"], op["data"]))
        else:
            src.project_op(op["op"], i)
    ast.parse(src.b)  # never write a broken file
    shutil.copyfile(CONTENT, CONTENT + ".bak")
    open(CONTENT, "wb").write(src.b)
    r = subprocess.run([sys.executable, os.path.join(HERE, "build.py")], capture_output=True, text=True)
    if r.returncode != 0:
        shutil.copyfile(CONTENT + ".bak", CONTENT)  # roll back
        raise ValueError("build failed: " + r.stderr.strip().splitlines()[-1])


# ── the local web server ────────────────────────────────────────────────────

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=SITE, **k)

    def local_only(self):
        host = (self.headers.get("Host") or "").split(":")[0]
        return host in ("localhost", "127.0.0.1")

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if not self.local_only():
            return self.send_error(403)
        path = self.path.split("?")[0]
        if path.startswith(("/src", "/.git", "/.")):  # only the site itself is served
            return self.send_error(404)
        if path.startswith("/_editor/"):
            name = os.path.basename(path)
            if name not in ("editor.js", "editor.css"):
                return self.send_error(404)
            return self.send(open(os.path.join(HERE, name), "rb").read(),
                             "text/javascript" if name.endswith(".js") else "text/css")
        if path in ("/", "/index.html"):
            html = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
            html = html.replace("</body>", '  <link rel="stylesheet" href="/_editor/editor.css">\n'
                                           '  <script src="/_editor/editor.js" defer></script>\n</body>')
            return self.send(html.encode(), "text/html; charset=utf-8")
        super().do_GET()

    def do_POST(self):
        # the custom header can't be sent cross-site without a preflight we never answer
        if not self.local_only() or self.headers.get("X-Portfolio-Editor") != "1" or self.path != "/_save":
            return self.send_error(403)
        try:
            payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            apply(payload)
            self.send(json.dumps({"ok": True}).encode(), "application/json")
        except Exception as e:  # report the problem to the page instead of crashing
            self.send(json.dumps({"ok": False, "error": str(e)}).encode(), "application/json", 400)

    def send(self, body, ctype, code=200):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        if self.command == "POST":
            sys.stderr.write("saved changes\n")


if __name__ == "__main__":
    subprocess.run([sys.executable, os.path.join(HERE, "build.py")], check=True)
    for port in range(8000, 8020):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
            break
        except OSError:
            continue
    url = f"http://localhost:{port}/"
    print(f"Edit mode running at {url}  (Ctrl+C to stop)", flush=True)
    if "--no-browser" not in sys.argv:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
