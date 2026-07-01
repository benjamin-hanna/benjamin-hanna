#!/usr/bin/env python3
import datetime
import subprocess
import sys
import tempfile
import os

README_PATH = "README.md"
START_MARKER = "<!--QUINE:START-->"
END_MARKER = "<!--QUINE:END-->"

def make_py_quine():
    s = "s = %r\nprint(s %% s)\n"
    return s % s

QUINES = [
    ("py", make_py_quine(), ["python3", "{path}"])
]

def pick_today():
    day_of_year = datetime.date.today().timetuple().tm_yday
    return QUINES[day_of_year % len(QUINES)]

def run_quine(ext, source, cmd_template):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=f".{ext}", delete=False
    ) as f:
        f.write(source)
        path = f.name
    cmd = [part.format(path=path) for part in cmd_template]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15
        )
        output = result.stdout
    finally:
        os.unlink(path)
    verified = output == source
    return output, verified

def build_section(source, output, verified, ext):
    today = datetime.date.today().isoformat()
    status = "Verified" if verified else "Error. Mismatch."
    lines = [
        START_MARKER,
        f"Last run: `{today}` — {status}",
        f"```{ext}",
        source.rstrip(),
        "```",
        "<details>",
        "<summary>Output</summary>",
        "",
        "```",
        output.rstrip(),
        "```",
        "</details>",
        END_MARKER,
    ]
    return "\n".join(lines)

def main():
    ext, source, cmd_template = pick_today()
    output, verified = run_quine(ext, source, cmd_template)
    new_section = build_section(source, output, verified, ext)
    with open(README_PATH, "r") as f:
        content = f.read()
    if START_MARKER not in content or END_MARKER not in content:
        print("Markers not found in README.md — aborting.", file=sys.stderr)
        sys.exit(1)
    before = content.split(START_MARKER)[0]
    after = content.split(END_MARKER)[1]
    new_content = before + new_section + after
    with open(README_PATH, "w") as f:
        f.write(new_content)
    print(f"Updated README. Verified: {verified}")

if __name__ == "__main__":
    main()