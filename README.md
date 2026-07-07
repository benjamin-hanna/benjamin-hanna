<!--START-->
Last run: `2026-07-07`. Verified.
```py
import sys
s = 'import sys\ns = %r\nsys.stdout.write(s %% s)\n'
sys.stdout.write(s % s)
```
Output:

```
import sys
s = 'import sys\ns = %r\nsys.stdout.write(s %% s)\n'
sys.stdout.write(s % s)
```
<!--END-->