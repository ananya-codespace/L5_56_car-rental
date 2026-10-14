# Lab 5: Static Code Analysis — Reflection

### 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, and coding-style violations early in development, making software easier to maintain and improve.

### 2. What is the purpose of Pylint, Bandit, and Flake8?

Pylint checks code quality, naming conventions, documentation, and potential programming errors. Bandit identifies common security vulnerabilities and unsafe coding practices. Flake8 checks Python code for formatting and style violations according to PEP 8 guidelines.

### 3. What types of issues were identified and fixed in this lab?

The analysis identified issues such as SQL injection risks, unsafe code execution, weak hashing, insecure temporary-file handling, mutable default arguments, missing docstrings, inconsistent naming conventions, and formatting violations. These were addressed through safer implementations and improved coding practices.

### 4. How did static analysis improve the program?

Static analysis helped improve the program's security, readability, and maintainability. After making the changes, the final code achieved a Pylint score of 10.00/10, Bandit reported no issues, and Flake8 reported no violations. This demonstrated how automated analysis tools can help improve Python code quality.