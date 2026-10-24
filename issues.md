# Lab 5 Issues and Fixes

Name: R Suhaas  
SRN: PES2UG24CS389  
Section: G

File: `wildlife_sightings.py`

The original program ran, but Pylint, Bandit and Flake8 reported several issues. The line numbers below refer to the original file saved in the `original` folder.

## 1. Weak hash for the observer ID

Bandit B324 — Security, high severity — Line 15

The code used MD5 and kept only the first six characters. I changed it to SHA-256 and kept the full result. This removes the weak-hash warning and avoids limiting the ID to such a short value. The ID is still just a label; it is not used to log anyone in.

## 2. Unsafe SQL query

Bandit B608 — Security, medium severity — Line 9

The INSERT query used `.format()` to put values directly into SQL. A name with an apostrophe could break it, and other input could change the query. I used `?` placeholders and passed the values separately. The test with `Pallas's cat` and SQL-like text in the zone passed, with the text stored as data.

## 3. Mutable default argument

Pylint W0102 — Bug — Line 8

The default `extras={}` dictionary was shared between calls. I changed it to `None` and create a new dictionary when none is supplied. An explicitly passed dictionary still gets updated, so the sample can continue adding to the same totals.

## 4. Assert used for a check

Bandit B101 — Reliability, low severity — Line 36

The `assert` statement disappears when Python runs with `-O`. I replaced it with an `if` condition that raises `RuntimeError` if the number of species is wrong. The sample ran successfully in both normal and optimized mode.

## 5. Function naming

Pylint C0103 — Style — Lines 8, 14 and 18

I changed `logSighting`, `observerId` and `zoneSummary` to `log_sighting`, `observer_id` and `zone_summary`. Their calls were updated as well. This follows Python's snake_case naming style.

## 6. Missing docstrings

Pylint C0114 and C0116 — Maintainability — Lines 1, 8, 14, 18, 26 and 32

The file and functions had no descriptions. I added short docstrings explaining what they do, including what is returned for an empty database or a zone with no sightings.

## 7. Reusing the global connection name

Pylint W0621 — Maintainability — Lines 8, 18 and 26, referring to line 4

The function parameters used the same name as the global connection. I moved the connection into `main` and pass it to the functions. I also used `closing` so it is closed after the sample runs, even if an error occurs. The main guard stops the sample from running on import.

## 8. Unnecessary else

Pylint R1705 — Readability — Lines 20 to 23

The `if` branch already returned zero. I removed the `else` and left the normal return after the condition. The result stays the same.

## 9. Long lines

Pylint C0301 and Flake8 E501 — Style — Lines 5, 9, 19 and 27

I split the long database statements across lines. All lines in the fixed program now fit Flake8's default 79-character limit.

## 10. Unclear variable name and spacing

Flake8 E741 and E225 — Style — Line 28

The variable `l` was easy to confuse with the number 1. I renamed it to `rarest_sighting` and added spaces around the assignment operator.

## 11. String formatting suggestion

Pylint C0209 — Style — Line 9

Pylint suggested an f-string for the SQL statement. That would not solve the SQL injection issue, so I used query parameters instead. The same change fixed both warnings.

## Other fixes

While checking the code, I also handled an empty sightings list. Previously, `min()` would fail; now `rarest()` returns `None`. Species and zone must be non-empty strings, and count must be a positive integer. Boolean values are rejected as counts too. These were extra checks from reviewing the code, not findings reported by the tools.

## Results

Pylint improved from 3.46/10 to 10.00/10. All three Bandit findings and all six Flake8 findings were cleared. No warnings were suppressed. Ten tests passed, covering the sample output and cases such as shared defaults, quoted input, invalid counts and an empty database.
