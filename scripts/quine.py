#!/usr/bin/env python3
import datetime
import subprocess
import sys
import tempfile
import os

README_PATH = "README.md"
START_MARKER = "<!--QUINE:START-->"
END_MARKER = "<!--QUINE:END-->"

QUINES = [
    (
        "py",
        's = \'s = %r\\nprint(s%%s)\'\nprint(s%s)\n',
        ["python3", "{path}"]
    )
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
    return f"""{START_MARKER}
Last run: `{today}` — {status}
```{ext}
{source.rstrip()}
```
<details>
<summary>Output</summary>