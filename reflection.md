# Lab 5 Reflection

Name: R Suhaas  
SRN: PES2UG24CS389  
Section: G

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The spacing and naming issues were the easiest to fix. The reports gave the line numbers, so these were small changes. The SQL query took more thought because changing it to an f-string would still leave the same security problem. It needed placeholders instead. The default dictionary was also less obvious. The sample ran fine, but separate calls without a dictionary would share their totals.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

I did not find a clear false positive. The MD5 warning did need a closer look because the hash was only being used as an observer ID, not as a password. So the warning sounded more serious than its use in this program. I still replaced MD5 with SHA-256 and kept the full hash instead of six characters. This also gives the IDs a much larger range of possible values.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would run Pylint and Flake8 before committing code and use Bandit to check for security issues. For a group project, these checks could run automatically on each pull request. I would fix the more serious warnings first, then deal with formatting. I would also run tests after making changes, since a clean report does not tell me whether the output is correct.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The Pylint score went from 3.46 to 10.00, and the Bandit and Flake8 warnings were cleared. The code now handles species names with apostrophes, rejects invalid counts, and returns None instead of crashing when there are no sightings. Calls without an extras dictionary also get separate totals. The sample still returns 25 for North and Leopard as the rarest species. The observer ID is different because the hashing method changed. All ten tests passed.
