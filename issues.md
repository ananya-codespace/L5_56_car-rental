# Lab 5: Static Code Analysis — Issues Identified

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Weak SHA-1 hash | Security — High | 47–48 | SHA-1 is a weak hashing algorithm and is unsuitable for security-sensitive uses. | Replace SHA-1 with a stronger hashing approach appropriate to the purpose. |
| Insecure file permissions | Security — High | 62–67 | Setting receipt permissions to `0o777` allows overly broad file access. | Remove the permissive permissions and use secure file permissions. |
| SQL injection in customer lookup | Security — Medium | 25–27 | The customer name is concatenated directly into an SQL query, allowing SQL injection. | Use parameterized SQL queries. |
| SQL injection in customer registration | Security — Medium | 22–23 | Customer details are inserted into SQL using string formatting. | Use parameterized SQL queries with placeholders. |
| Arbitrary code execution | Security — Medium | 50–54 | The `exec()` function executes a promo rule as Python code, which can be unsafe. | Replace `exec()` with a controlled calculation or an explicitly supported set of promo rules. |
| Insecure temporary file creation | Security — Medium | 62–64 | `tempfile.mktemp()` can introduce a race condition when creating receipt files. | Use a safer temporary-file creation method. |
| Dangerous mutable default argument | Code quality | 16 | The default `features=[]` list can be shared between function calls. | Use `None` as the default and create a new list inside the function. |
| Broad exception handling | Code quality | 36–42 | A bare `except` suppresses errors and makes debugging difficult. | Catch specific exceptions and handle them appropriately. |
| Unused import | Style | 2 | The `json` module is imported but never used. | Remove the unused import. |
| Incorrect Boolean comparison | Style | 78 | The code compares a Boolean value explicitly with `True`. | Use the Boolean value directly in the condition. |
| Missing documentation and naming conventions | Style | Multiple | Functions lack docstrings and use camelCase names instead of snake_case. | Add docstrings and use consistent snake_case naming. |