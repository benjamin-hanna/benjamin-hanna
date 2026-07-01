<!--START-->
Last run: `2026-06-30` — Verified
```py
import sys
s = 'import sys\ns = %r\nsys.stdout.write(s %% s)\n'
sys.stdout.write(s % s)
```
<details>
<summary>Output</summary>

```
import sys
s = 'import sys\ns = %r\nsys.stdout.write(s %% s)\n'
sys.stdout.write(s % s)
```
</details>
<!--END-->