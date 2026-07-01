<!--START-->
Last run: `2026-07-01` — Verified
```py
import sys
s = 'import sys\ns = %r\nsys.stdout.write(s %% s)\n'
sys.stdout.write(s % s)
```
<details>
Output

```
import sys
s = 'import sys\ns = %r\nsys.stdout.write(s %% s)\n'
sys.stdout.write(s % s)
```
</details>
<!--END-->