# Lab 5: Static Code Analysis - Issues

Program: `pharmacy_system.py` (Pharmacy Prescription & Stock Tracker)

Tools: Pylint, Flake8, Bandit, plus manual testing. Line numbers refer to the original starter file. Ordered High, then Medium, then Low.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (High) | Security (Bandit B608) | 21 | Query built with `%` string formatting from user input. Typing `x' OR '1'='1` returns every patient. | Use a parameterized query with a `?` placeholder. |
| Dispensing more than in stock (High) | Logic bug (manual test) | 35 | No stock check. Amoxicillin has 20 units, 30 are dispensed, stock becomes -10 and it returns True. | Check stock >= units before subtracting. |
| Allergy check is case-sensitive (High) | Logic / safety bug | 32 | `drug in patient[1]` is a case-sensitive substring test, so "Ibuprofen" bypasses Meena's "ibuprofen" allergy. | Compare with `casefold()` for equality. |
| Negative stock accepted (High) | Logic bug (manual test) | 72, 25 | `add_stock("Ibuprofen", -15, ...)` is accepted with no validation. | Raise `ValueError` when units < 0. |
| Expired medicine stocked and dispensed (Medium) | Logic bug (manual test) | 70, 35 | Amoxicillin expiry 2025-12-31 is in the past, yet it is stocked and dispensed. | Check expiry before dispensing and fix the sample date. |
| Bare except in dispense (Medium) | Error handling (Pylint W0702, Flake8 E722) | 38-39 | Hides IndexError, KeyError and real bugs behind a silent `False`. | Remove it and validate patient, drug, units and stock explicitly. |
| Bare except: pass in load_stock (Medium) | Security / error handling (Bandit B110) | 58-59 | Missing file, bad JSON and permission errors are silently ignored. | Catch specific exceptions and print clear messages. |
| Drug name case mismatch (Medium) | Logic bug | 35 | "ibuprofen" does not match key "Ibuprofen", so a KeyError is hidden by the bare except. | Match stock names case-insensitively. |
| Mutable default argument (Medium) | Bug (Pylint W0102) | 24 | `batch_log=[]` is shared across calls, so the count keeps growing. | Default to `None` and create the list inside the function. |
| Restock overwrites expiry (Medium) | Logic bug | 25 | New batch replaces the existing expiry date, even if older units expire sooner. | Keep the earlier expiry date. |
| Files opened without `with` or encoding (Low) | Code quality (Pylint R1732, W1514) | 50-52, 57 | File may not close on error and no encoding is set. | Use `with open(..., encoding="utf-8")` and `json.dump`. |
| Global statement (Low) | Code quality (Pylint W0603) | 55 | `global stock` rebinds module state. | Use `stock.clear()` and `stock.update()`. |
| `main()` runs on import (Low) | Design | 83 | Importing the file runs the whole program. | Add `if __name__ == "__main__":`. |
| Unused import `os` (Low) | Code quality (Pylint W0611, Flake8 F401) | 3 | `os` is never used. | Remove the import. |
| `printStock` not snake_case (Low) | Style (Pylint C0103) | 61, 81 | Breaks PEP 8 naming. | Rename to `print_stock`. |
| Missing docstrings (Low) | Documentation (Pylint C0114, C0116) | 1, 11, 19, 24, 29, 41, 49, 54, 61, 66 | Module and functions have no docstrings. | Add docstrings. |
| Lines too long (Low) | Style (Pylint C0301, Flake8 E501) | 25, 36 | Lines are 90 and 112 characters. | Split across lines. |
| Missing blank lines (Low) | Style (Flake8 E302, E305) | 11, 19, 24, 29, 41, 49, 54, 61, 66, 83 | PEP 8 needs two blank lines around top-level definitions. | Add blank lines. |
| Old-style string formatting (Low) | Style (Pylint C0209) | 21 | `%` formatting instead of an f-string. | Gone once the query is parameterized. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.90/10 | 10.00/10 |
| Flake8 | 15 warnings | 0 |
| Bandit | 2 issues (1 Medium, 1 Low) | No issues |
