<!--QUINE:START-->
Last run: `2026-07-01` — Error. Mismatch.
```py
s = 's = %r\nprint(s %% s)\n'
print(s % s)
```
<details>
<summary>Output</summary>

```
s = 's = %r\nprint(s %% s)\n'
print(s % s)
```
</details>
<!--QUINE:END-->