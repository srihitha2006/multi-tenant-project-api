## Tool Results

### Lint (flake8)
- Issues found: 68
  - .\app\api\organization.py:14:1: E302 expected 2 blank lines, found 1
  - .\app\api\organization.py:14:80: E501 line too long (103 > 79 characters)
  - .\app\api\organization.py:15:80: E501 line too long (91 > 79 characters)
  - .\app\api\organization.py:23:80: E501 line too long (87 > 79 characters)
  - .\app\api\organization.py:28:1: E302 expected 2 blank lines, found 1
  - .\app\api\overdue.py:12:1: E302 expected 2 blank lines, found 1
  - .\app\api\overdue.py:18:27: E711 comparison to None should be 'if cond is not None:'
  - .\app\api\overdue.py:20:28: E712 comparison to False should be 'if cond is False:' or 'if not cond:'
  - .\app\api\project.py:16:80: E501 line too long (109 > 79 characters)
  - .\app\api\project.py:23:5: F841 local variable 'org_id' is assigned to but never used
  - .\app\api\project.py:26:5: E122 continuation line missing indentation or outdented
  - .\app\api\project.py:27:5: E122 continuation line missing indentation or outdented
  - .\app\api\project.py:36:1: E303 too many blank lines (3)
  - .\app\api\project.py:58:80: E501 line too long (97 > 79 characters)
  - .\app\api\project.py:65:1: E303 too many blank lines (3)
  - .\app\api\project.py:73:80: E501 line too long (90 > 79 characters)
  - .\app\api\project.py:81:80: E501 line too long (120 > 79 characters)
  - .\app\api\project.py:89:80: E501 line too long (90 > 79 characters)
  - .\app\api\task.py:27:5: E122 continuation line missing indentation or outdented
  - .\app\api\task.py:28:5: E122 continuation line missing indentation or outdented

### Security (bandit)
- Findings: 1
  - Possible hardcoded password: 'SUPER_SECRET_KEY_CHANGE_THIS' | .\app\core\security.py:5 | severity=LOW

### Tests (pytest)
- Tests failed ❌
  - no tests ran in 0.01s