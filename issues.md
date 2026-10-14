# Lab 5: Static Code Analysis

## Issue Documentation Table

*Note: Line numbers refer to the original `pharmacy_system.py` before
modifications.*

  ---------------------------------------------------------------------------------
  Issue         Type           Original line(s) Description      Fix approach
  ------------- ------------- ----------------- ---------------- ------------------
  SQL injection Security                     21 SQL query        Used a
  risk                                          constructed      parameterized SQL
                                                using string     query with a `?`
                                                formatting with  placeholder.
                                                user input.      

  Silent        Security /               58--59 A bare exception Added specific
  exception     Error                           was caught and   exception handling
  handling      handling                        ignored using    and error
                                                `pass`.          messages.

  Mutable       Bug                          26 `batch_log=[]`   Changed the
  default                                       could share a    default to `None`
  argument                                      list between     and initialized
                                                function calls.  the list inside
                                                                 the function.

  Missing       Code quality                  1 The module       Added a
  module                                        lacked a         module-level
  docstring                                     descriptive      docstring.
                                                docstring.       

  Missing       Code quality           Multiple Functions lacked Added docstrings
  function                                      documentation    to the functions.
  docstrings                                    describing their 
                                                purpose.         

  Bare          Error                        40 A bare `except`  Removed broad
  exception     handling                        could catch      exception handling
                                                unexpected       and added explicit
                                                exceptions.      validation.

  Unsafe file   Code quality             52--53 The file was     Used `with open()`
  handling                                      opened without   and specified
                                                explicit         UTF-8 encoding.
                                                encoding or a    
                                                context manager. 

  Global        Code quality                 59 The function     Updated the
  statement                                     reassigned the   existing
                                                global stock     dictionary using
                                                dictionary.      `clear()` and
                                                                 `update()`.

  Invalid       Code style                   71 `printStock()`   Renamed it to
  function                                      did not follow   `print_stock()`.
  naming                                        Python's         
                                                snake_case       
                                                convention.      

  Unused import Code style                    3 The `os` module  Removed the unused
                                                was imported but import.
                                                never used.      

  Formatting    Code style             Multiple Missing blank    Corrected spacing
  violations                                    lines and lines  and split long
                                                exceeding the    statements across
                                                recommended      multiple lines.
                                                length.          

  Negative      Logic /                      82 The original     Added validation
  stock         Validation                      demonstration    to reject negative
  quantities                                    added a negative stock additions
                                                stock quantity.  and corrected the
                                                                 demonstration
                                                                 quantity.
  ---------------------------------------------------------------------------------

## Results After Fixes

-   **Pylint:** Improved from 6.90/10 initially to 10.00/10 after the
    changes.
-   **Bandit:** No issues identified in the final scan.
-   **Flake8:** No formatting violations reported in the final scan.

## Conclusion

Static code analysis helped identify security risks, programming errors,
and style violations in the pharmacy stock and prescription tracking
program. Fixing these issues improved code readability, maintainability,
error handling, and security. Running the tools again confirmed that the
reported findings had been addressed.
