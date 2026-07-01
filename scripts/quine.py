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
        "Python",
        "py",
        's = \'s = %r\\nprint(s%%s)\'\nprint(s%s)\n',
        ["python3", "{path}"]
    )
]
def pick_today():
    day_of_year = datetime.date.today().timetuple().tm_yday
    return QUINES[day_of_year % len(QUINES)]
def run_quine(name, ext, source, cmd_template):
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
def build_section(name, source, output, verified, ext):
    today = datetime.date.today().isoformat()
    status = "Verified" if verified else "Error. Mismatch."
    return f"""{START_MARKER}
### {name}
Last run: `{today}` — {status}

```{ext}
{source.rstrip()}
```
<details>
<summary>Actual output from running it today</summary>
```
{output.rstrip()}
```
</details>
{END_MARKER}"""
def main():
    name, ext, source, cmd_template = pick_today()
    output, verified = run_quine(name, ext, source, cmd_template)
    new_section = build_section(name, source, output, verified, ext)
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
    print(f"Updated README with {name} quine. Verified: {verified}")
if __name__ == "__main__":
    main()