#!/usr/bin/env python3

import datetime
import subprocess
import sys
import tempfile
import os

README_PATH = "README.md"
START_MARKER = "<!--START-->"
END_MARKER = "<!--END-->"

def make_quine():
    s = "import sys\ns = %r\nsys.stdout.write(s %% s)\n"
    return s % s

QUINES = [("py", make_quine(), ["python3", "{path}"])]

def time():
    time = datetime.date.today().timetuple().tm_yday
    return QUINES[time % len(QUINES)]

def run(ext, source, cmd_template):
    with tempfile.NamedTemporaryFile(mode="w", suffix=f".{ext}", delete=False) as f:
        f.write(source)
        path = f.name

    cmd = [part.format(path=path) for part in cmd_template]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        output = result.stdout

    finally:
        os.unlink(path)

    verified = output == source
    return output, verified

def build(source, output, verified, ext):
    time = datetime.date.today().isoformat()
    status = "Verified:" if verified else "Error. Mismatch."

    lines = [
        START_MARKER,
        f"Last run: `{time}`. {status}",
        f"```{ext}",
        source.rstrip(),
        "```",
        "Output:",
        "",
        "```",
        output.rstrip(),
        "```",
        END_MARKER,
    ]

    return "\n".join(lines)

def main():
    ext, source, cmd_template = time()
    output, verified = run(ext, source, cmd_template)
    new_section = build(source, output, verified, ext)

    with open(README_PATH, "r") as f:
        content = f.read()

    if START_MARKER not in content or END_MARKER not in content:
        print("Markers not found in README.md. Aborting.", file=sys.stderr)
        sys.exit(1)

    before = content.split(START_MARKER)[0]
    after = content.split(END_MARKER)[1]
    new_content = before + new_section + after

    with open(README_PATH, "w") as f:
        f.write(new_content)
    print(f"Updated README. Verified: {verified}")

if __name__ == "__main__":
    main()