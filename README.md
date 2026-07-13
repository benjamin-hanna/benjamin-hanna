```
Languages: Python | PHP | Javascript | SQL & NoSQL
CI/CD: GitLab CI/CD / Actions
IaC & Automation: Terraform | Bash 
Cloud & Infrastructure: AWS | Azure
Containers: Docker
Other Tools: Linux, OpenBSD
```

<!--START-->
Last run: `2026-07-13`. Verified.
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