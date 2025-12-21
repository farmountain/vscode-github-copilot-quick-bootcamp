# Session 2.3 — CLI Automation with GitHub Copilot CLI

**Duration:** Brief intro (integrated throughout Day 2)  
**Format:** Micro-exercises embedded in labs  
**Tools:** GitHub Copilot CLI (`gh copilot`)

---

## Learning Objectives

By the end of this session, learners will be able to:

1. **Use `gh copilot suggest`** to get command suggestions for common tasks
2. **Use `gh copilot explain`** to understand unfamiliar commands before running them
3. **Integrate Copilot CLI** into their development workflow (tests, git, file operations)
4. **Recognize** when CLI automation adds value vs. when manual commands are clearer

---

## What is GitHub Copilot CLI?

**GitHub Copilot CLI** is a command-line interface for Copilot that helps you:

- **Suggest commands** based on natural language descriptions
- **Explain commands** before you run them (safety first!)
- **Generate shell scripts** for repetitive tasks

**Installation:**
```bash
# Install GitHub CLI first (if not already installed)
# Windows: winget install GitHub.cli
# Mac: brew install gh
# Linux: see https://cli.github.com/

# Install Copilot CLI extension
gh extension install github/gh-copilot

# Verify installation
gh copilot --version
```

**Aliases (optional but recommended):**
```bash
# Add to your shell profile (.bashrc, .zshrc, or PowerShell profile)
alias ghcs='gh copilot suggest'
alias ghce='gh copilot explain'
```

---

## Core Commands

### 1. `gh copilot suggest` — Get Command Suggestions

**Syntax:**
```bash
gh copilot suggest [options] "<natural language query>"
```

**Options:**
- `-t shell` — suggest shell commands (default)
- `-t gh` — suggest GitHub CLI commands
- `-t git` — suggest git commands

**Example:**
```bash
gh copilot suggest "find all Python files modified in the last 24 hours"

# Copilot suggests:
find . -name "*.py" -mtime -1
```

**Workflow:**
1. Copilot suggests command
2. You review the suggestion
3. You choose: run it, revise it, or cancel

### 2. `gh copilot explain` — Understand Commands

**Syntax:**
```bash
gh copilot explain "<command to explain>"
```

**Example:**
```bash
gh copilot explain "pytest tests/ --cov=src --cov-report=html"

# Copilot explains:
# - pytest: runs Python tests
# - --cov=src: measures code coverage for src/ directory
# - --cov-report=html: generates HTML coverage report in htmlcov/
```

**Use this BEFORE running unfamiliar commands** (especially from Stack Overflow or docs).

---

## Day 2 CLI Exercises (Banking-Safe)

### Exercise 1: Find Files for Refactoring

**Task:** Find all Python files in the `src/day2/` directory that contain the word "TODO".

```bash
gh copilot suggest "find Python files in src/day2 that contain TODO"

# Expected suggestion:
grep -r "TODO" src/day2/ --include="*.py"
```

**Verification:**
- Review the command
- Run it: `grep -r "TODO" src/day2/ --include="*.py"`
- Check results

### Exercise 2: Run Tests for Specific Module

**Task:** Run pytest for only the AML rules tests with verbose output.

```bash
gh copilot suggest "run pytest on tests/day2/test_aml_rules.py with verbose output"

# Expected suggestion:
pytest tests/day2/test_aml_rules.py -v
```

**Before running, explain it:**
```bash
gh copilot explain "pytest tests/day2/test_aml_rules.py -v"
```

### Exercise 3: Check Git Diff Before Commit

**Task:** Show changes in staged files.

```bash
gh copilot suggest -t git "show changes in staged files"

# Expected suggestion:
git diff --staged
```

### Exercise 4: Count Lines of Code

**Task:** Count lines of code in the `src/day2/aml_triage/` module.

```bash
gh copilot suggest "count lines of Python code in src/day2/aml_triage"

# Expected suggestion (may vary by OS):
# Linux/Mac:
find src/day2/aml_triage -name "*.py" -exec wc -l {} + | tail -1

# Windows PowerShell:
(Get-ChildItem -Path src/day2/aml_triage -Filter *.py -Recurse | Get-Content).Count
```

### Exercise 5: Create Directory Structure

**Task:** Create output directories for Day 2 labs.

```bash
gh copilot suggest "create directories out/day2/lab3 and out/day2/lab4"

# Expected suggestion:
mkdir -p out/day2/lab3 out/day2/lab4
# Or Windows: New-Item -ItemType Directory -Path out/day2/lab3, out/day2/lab4 -Force
```

### Exercise 6: Compare Two JSON Files

**Task:** Check if two JSON output files are identical.

```bash
gh copilot suggest "compare two JSON files and show differences"

# Expected suggestion:
diff file1.json file2.json
# Or: jq -S . file1.json > sorted1.json && jq -S . file2.json > sorted2.json && diff sorted1.json sorted2.json
```

**Explain before running:**
```bash
gh copilot explain "jq -S . file1.json"
# jq: command-line JSON processor
# -S: sort keys
# .: output entire JSON
```

---

## Workflow Integration Examples

### Pattern 1: Test → Commit Workflow

**Scenario:** You've just made a code change. You want to test, review diff, and commit.

```bash
# Suggest test command
gh copilot suggest "run all pytest tests in tests/day2 with coverage"

# (Suggested: pytest tests/day2/ --cov=src.day2 --cov-report=term)
# Run it:
pytest tests/day2/ --cov=src.day2 --cov-report=term

# Tests pass! Now check what changed:
gh copilot suggest -t git "show changes not yet staged"
# (Suggested: git diff)
git diff

# Stage changes:
gh copilot suggest -t git "stage all changed Python files"
# (Suggested: git add *.py)
git add *.py

# Commit:
gh copilot suggest -t git "commit with message refactored aml triage rules"
# (Suggested: git commit -m "refactored aml triage rules")
git commit -m "refactored aml triage rules"
```

### Pattern 2: Find and Replace Across Files

**Scenario:** You need to rename a function across multiple files.

```bash
# Find occurrences first:
gh copilot suggest "find all files containing function name check_high_velocity"
# (Suggested: grep -r "check_high_velocity" .)
grep -r "check_high_velocity" .

# Explain sed command before using it:
gh copilot explain "sed -i 's/check_high_velocity/check_velocity_rule/g' src/day2/aml_triage/rules.py"

# If safe, run replacements:
# (Better to use your editor's find-and-replace, but Copilot can suggest)
```

### Pattern 3: Generate Test Data

**Scenario:** You need sample CSV data for testing.

```bash
gh copilot suggest "create a CSV file with 10 rows of sample transaction data"

# Copilot might suggest using Python or a shell script
# Review the suggestion carefully!
```

---

## Safety Guidelines

### ✅ Safe to Automate with Copilot CLI

- **Read operations:** `find`, `grep`, `cat`, `ls`, `git diff`, `git log`
- **Test execution:** `pytest`, `python -m unittest`
- **Output inspection:** `wc -l`, `head`, `tail`, `diff`
- **Explanations:** Always use `gh copilot explain` for unfamiliar commands

### ⚠️ Requires Careful Review

- **Staging/committing:** Review `git add`, `git commit` suggestions before running
- **File creation:** Check `mkdir`, `touch` suggestions for correct paths
- **Batch operations:** Be cautious with `find ... -exec` or `xargs`

### ❌ Never Automate Without Understanding

- **Destructive operations:** `rm`, `git reset --hard`, `git push -f`
- **Credential operations:** Anything involving passwords, tokens, secrets
- **System modifications:** `chmod`, `chown`, package installations
- **Database operations:** `DROP TABLE`, `DELETE FROM` (not in this training, but principle applies)

**Golden rule:** If you don't understand the command, use `gh copilot explain` first. If still unsure, don't run it.

---

## Micro-Exercise: Build a Test Script

**Task:** Use Copilot CLI to help you write a shell script that:
1. Runs Day 2 tests
2. If tests pass, runs the AML triage pipeline
3. Counts alerts in the output

```bash
# Start by asking for structure:
gh copilot suggest "create a bash script that runs pytest and then runs a python module if tests pass"

# Example suggestion:
#!/bin/bash
pytest tests/day2/ -v
if [ $? -eq 0 ]; then
    echo "Tests passed, running pipeline..."
    python -m src.day2.aml_triage.cli --input src/samples/sample_transactions.csv --outdir out/day2
else
    echo "Tests failed, skipping pipeline"
    exit 1
fi
```

**Explain the exit code check:**
```bash
gh copilot explain "if [ $? -eq 0 ]"
# $?: exit code of last command
# -eq 0: equals 0 (success)
```

**Save to file:**
```bash
# Create the script file
gh copilot suggest "save command output to a file named run_day2_pipeline.sh"
# Suggestion: echo "..." > run_day2_pipeline.sh

# Make executable (Linux/Mac):
chmod +x run_day2_pipeline.sh

# Run:
./run_day2_pipeline.sh
```

---

## Debugging with Copilot CLI

### Pattern: Understand Test Failures

**Scenario:** A pytest run shows a failure. You want to understand the error.

```bash
# Run single test with full traceback:
gh copilot suggest "run pytest on a single test with full error output"
# Suggested: pytest tests/day2/test_aml_rules.py::test_high_velocity -vv

# Explain pytest options:
gh copilot explain "pytest -vv"
# -vv: very verbose (shows full diffs and tracebacks)
```

### Pattern: Check Code Quality

```bash
# Run linter:
gh copilot suggest "run flake8 on src/day2 directory"
# Suggested: flake8 src/day2/

# Run type checker:
gh copilot suggest "run mypy type checking on src/day2"
# Suggested: mypy src/day2/
```

---

## Integration with VS Code Tasks

You can combine Copilot CLI with VS Code tasks for a unified workflow.

**Example `.vscode/tasks.json` entry:**
```json
{
    "label": "Day2: Suggest Test Command",
    "type": "shell",
    "command": "gh copilot suggest 'run pytest on day2 tests with coverage'",
    "problemMatcher": []
}
```

**Or** use Copilot CLI to generate the task definition itself:
```bash
gh copilot suggest "create a VS Code task.json entry that runs pytest on tests/day2"
```

---

## Reflexion: When to Use Copilot CLI vs. Manual Commands

### Use Copilot CLI when:
- You know what you want to do but not the exact syntax
- You're learning new tools (pytest, git, shell)
- You want to explore options (Copilot suggests parameters)
- You need to understand a complex command from docs

### Use manual commands when:
- You know the exact command (typing is faster)
- Command is simple and common (`cd`, `ls`, `git status`)
- You're in a tight feedback loop (test → edit → test)

**Copilot CLI is a learning accelerator, not a replacement for understanding.**

---

## Key Takeaways

1. **`gh copilot suggest`** generates commands from natural language (read operations are safest)
2. **`gh copilot explain`** helps you understand commands before running them
3. **Always review suggestions** before executing, especially destructive operations
4. **Integrate into workflow:** test automation, git operations, file searching
5. **Use it to learn:** Copilot CLI teaches you shell commands and tool options

---

## Practice Challenges

Try these safe exercises with Copilot CLI:

1. **Find all CSV files** in the repository
2. **Count how many times** "ReasonCode" appears in the codebase
3. **Show git history** for a specific file
4. **Run pytest** with JSON output format (research needed!)
5. **Generate a requirements.txt** from currently installed packages (hint: `pip freeze`)
6. **Compare two directories** to see which files differ

For each:
- Use `gh copilot suggest`
- Use `gh copilot explain` on the suggestion
- Run the command if safe
- Verify the result

---

## Next Steps

- Throughout Day 2 labs, try using `gh copilot suggest` for every command task
- Track which suggestions were helpful vs. which required editing
- In the Day 2 wrap session, share: "What's one command you learned via Copilot CLI?"

---

**Experiment now:**
```bash
gh copilot suggest "show me the 5 largest files in the src directory"
```
