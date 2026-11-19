# Issues Found

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| Unsafe pickle import and `pickle.load` (B403/B301) | Security (Medium) | 2, 44, 49 | Unpickling a tampered backup file can execute arbitrary code | Replaced pickle with `json`, converting order ids back to int on restore |
| Bare `except: pass` (B110/E722/W0702) | Bug / Security (Low) | 24-25 | Errors in `update_order_status` were swallowed, so updating a nonexistent order (42) failed silently | Removed the try/except and raise `KeyError` for unknown ids |
| Mutable default argument `order_history=[]` (W0102) | Bug | 11 | The same list is shared across all calls to `create_order` | Default to `None` and create a new list inside the function |
| Broad `except Exception` (W0718) | Bad practice | 32 | Hides unrelated errors when loading the menu | Catch only `OSError` and `json.JSONDecodeError` |
| Files opened without `with` or encoding (R1732/W1514) | Resource leak | 30, 43, 49 | Handles may stay open if an error occurs | Use `with open(..., encoding="utf-8")` |
| Unknown dishes silently cost 99 | Logic bug (no tool flagged) | 15 | Order 2 ("sushi") was priced at 99 with no warning, giving a total of 249 | Raise `ValueError` for items not on the menu |
| Status never validated | Logic bug (no tool flagged) | 23 | "teleported" was accepted; `VALID_STATUSES` was never used | Check the status against `VALID_STATUSES` |
| Empty customer and items accepted | Logic bug (no tool flagged) | 11-19, 60 | Order 3 was created with no customer and no items | Reject such orders in `create_order` |
| `global` statements (W0603) | Design | 12, 28, 48 | Mutating module state through `global` | Update the dicts in place instead |
| `printQueue` naming and `%` formatting (C0103/C0209) | Style | 51-52 | Not snake_case; old-style string formatting | Renamed to `print_queue`, used an f-string |
| Missing docstrings (C0114/C0116) | Style | 1, all functions | No documentation | Added module and function docstrings |
| `main()` runs on import | Design | 70 | Importing the module runs the program | Added `if __name__ == "__main__":` guard |
| Final newline and whitespace (W292/W293/C0304) | Style | end of file | Formatting violations | Removed trailing whitespace, added a final newline |