# Lab 5: Static Code Analysis

## Reflection

### 1. What is static code analysis, and why is it useful?

Static code analysis means checking the source code without running the
program. It helps find possible errors, security problems and
coding-style issues before the software is used. It is useful because
fixing these issues early can make the code safer and easier to
maintain.

### 2. What is the difference between Pylint, Bandit and Flake8?

Pylint checks the overall quality of Python code, including naming,
documentation and possible programming mistakes. Bandit checks for
common security problems, such as unsafe ways of building SQL queries.
Flake8 checks formatting and style rules, including spacing and line
length. Using all three gave me a better idea of different types of
problems in the same program.

### 3. What issues did you find and fix in the program?

The original program had a possible SQL injection issue, a mutable
default argument, broad exception handling, and file handling that did
not specify an encoding or use a context manager. It also had missing
docstrings, an unused import, a function name that did not follow
`snake_case`, and formatting issues. I used parameterized SQL, changed
the default argument to `None`, handled specific exceptions, improved
file handling, added docstrings and corrected the naming and formatting.

### 4. How did the tools help improve the program?

The tools gave specific warnings and line numbers, which made it easier
to locate problems. After making the changes, I ran the tools again to
check the results. Pylint improved from 6.90/10 in the original report
to 10.00/10, Bandit reported no issues, and Flake8 produced no
violations.

### 5. What did you learn from this lab?

I learned that a program can run and still contain security risks or
code-quality problems. Each tool checks a different area, so using them
together is more useful than relying on only one. I also learned that it
is important to rerun the tools after making changes instead of assuming
that the fixes worked.
