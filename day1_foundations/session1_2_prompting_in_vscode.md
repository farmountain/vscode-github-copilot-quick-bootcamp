# Session 1.2: Prompting in VS Code (Context, Constraints, Acceptance Criteria)

**Duration**: 90 minutes (10:45–12:15)  
**Format**: Instructor-led with hands-on exercises

## Learning Objectives

By the end of this session, you will be able to:

* Craft effective prompts using the 3C framework (Context, Constraints, Criteria)
* Use GitHub Copilot Chat features for code generation, explanation, and refactoring
* Use GitHub Copilot Agent Mode to execute multi-file tasks
* Use GitHub Copilot CLI for command-line productivity
* Apply the Paul-Elder framework to structure complex prompts
* Identify and fix common prompting mistakes

## Agenda

| Time | Topic | Format |
|------|-------|--------|
| 10:45–11:00 | The anatomy of a good prompt | Lecture |
| 11:00–11:20 | 3C Framework: Context, Constraints, Criteria | Lecture + examples |
| 11:20–11:40 | GitHub Copilot Chat features deep-dive | Demo + hands-on |
| 11:40–12:00 | GitHub Copilot Agent Mode walkthrough | Demo + hands-on |
| 12:00–12:10 | GitHub Copilot CLI essentials | Demo + hands-on |
| 12:10–12:15 | Reflexion & Q&A | Discussion |

---

## Part 1: The Anatomy of a Good Prompt

### Feynman Explanation (Simple Analogy)

**Bad prompt** = "Build me a house"  
→ You might get a doghouse, a treehouse, or a mansion. Who knows?

**Good prompt** = "Build me a 3-bedroom, 2-bath single-family home with a kitchen, living room, and garage. Budget: $300K. Must meet local building codes. Include blueprint and materials list."  
→ Now the builder knows exactly what to deliver.

**In coding**: A vague prompt ("add validation") gets you vague code. A precise prompt gets you production-ready code.

### The Problem with Vague Prompts

**Example of a vague prompt**:
> "Write a function to process payments"

**What AI doesn't know**:
* What payment methods? (card, ACH, wire, crypto?)
* What validations? (amount limits, fraud checks?)
* What outputs? (success/failure, receipts, logs?)
* What error handling? (retry logic, dead-letter queue?)
* What data format? (JSON, XML, protobuf?)

**Result**: AI makes assumptions, generates something generic, and you waste time refactoring.

### The Solution: Structured Prompts

Use the **3C Framework**:

1. **Context**: What's the situation? What files/code exist? What's the business goal?
2. **Constraints**: What must we respect? (languages, libraries, patterns, data privacy)
3. **Criteria**: What does success look like? (acceptance criteria, test cases)

---

## Part 2: The 3C Framework (Context, Constraints, Criteria)

### Structure of an Effective Prompt

```
[Context]
We have a banking transaction processing system. Currently, transactions are validated manually.
We need to automate validation before they hit the ledger.

[Constraints]
- Use Python 3.9+
- Use Pydantic for data models
- No external API calls (all logic must be local)
- Must be deterministic (same input → same output)
- No PII logging (transaction IDs only)
- Must work with existing Transaction dataclass (in models.py)

[Criteria]
Generate a validate_transaction function that:
1. Returns a tuple: (is_valid: bool, errors: list[str])
2. Checks:
   - amount > 0 and amount < 1_000_000
   - currency is a valid ISO-4217 code (use a small hardcoded list: USD, EUR, GBP)
   - account_id matches pattern "ACC\d{8}"
   - txn_ts is not in the future (use UTC)
3. Include type hints
4. Include a docstring with examples
5. Include pytest unit tests in a separate test_validation.py file

Success criteria:
- All tests pass
- Code follows PEP 8
- No exceptions for valid inputs
```

### Why This Works

* **Context**: AI understands we're in a banking domain, not e-commerce
* **Constraints**: AI won't suggest libraries we don't use or patterns we don't want
* **Criteria**: AI knows exactly what "done" looks like

### Exercise 1: Improve a Vague Prompt (10 min)

**Vague prompt**:
> "Create a database model for customers"

**Your task**: Rewrite using 3C framework.

**Hint**: Consider:
* Context: What kind of system? What do we do with customer data?
* Constraints: What database (SQL/NoSQL)? What ORM? What privacy rules?
* Criteria: What fields? What relationships? What validations?

**Sample improved prompt**:
```
[Context]
We're building a credit application system. We need to store applicant information for risk scoring.
This is a backend service using PostgreSQL.

[Constraints]
- Use SQLAlchemy ORM with declarative base
- No PII in logs (encrypt SSN, redact in debug output)
- All timestamps in UTC
- Use UUIDs for primary keys

[Criteria]
Create a Customer model with fields:
- id (UUID, primary key)
- application_id (str, unique, indexed)
- full_name (str, required, max 200 chars)
- annual_income (Decimal, required, >= 0)
- employment_years (int, required, >= 0)
- created_at (timestamp with tz, default now)
- updated_at (timestamp with tz, auto-update)

Include:
- __repr__ method that doesn't expose PII
- Alembic migration file
- Basic pytest fixtures for testing
```

---

## Part 3: GitHub Copilot Chat Features Deep-Dive

### Overview of Copilot Chat

**Location**: VS Code sidebar (chat icon) or inline (`Ctrl+I` / `Cmd+I`)

**Key features**:
* Conversational code generation
* Code explanations
* Bug fixes
* Refactoring suggestions
* Test generation
* Documentation generation

### Feature 1: Slash Commands

Slash commands provide quick shortcuts for common tasks:

| Command | Purpose | Example |
|---------|---------|---------|
| `/explain` | Explain selected code | Select a function, type `/explain` |
| `/fix` | Fix errors in selected code | Select buggy code, type `/fix` |
| `/tests` | Generate unit tests | Select a function, type `/tests` |
| `/doc` | Generate documentation | Select a function, type `/doc` |
| `/simplify` | Simplify complex code | Select convoluted logic, type `/simplify` |

### Feature 2: Context References

Use `#` to reference context:

| Reference | Meaning | Example |
|-----------|---------|---------|
| `#file:path/to/file.py` | Include a specific file | `#file:models.py` |
| `#selection` | Include current selection | Select code, then `#selection` |
| `#editor` | Include active file | `#editor` |
| `#codebase` | Search entire codebase | `#codebase transaction validation` |

**Example prompt with context**:
```
Using the Transaction model in #file:models.py, generate a validation function that checks all required fields are present. Include type hints and return a ValidationResult dataclass.
```

### Feature 3: Multi-turn Conversations

You can have back-and-forth conversations to refine code:

**Turn 1**: "Generate a function to parse CSV files"  
**Turn 2**: "Add error handling for malformed rows"  
**Turn 3**: "Add logging for each error"  
**Turn 4**: "Write tests for the error cases"

**Tip**: Each turn maintains context from previous turns in the same chat session.

### Exercise 2: Use Slash Commands (10 min)

**Task**: Create a simple function and use Copilot Chat slash commands.

1. Create a new file: `example_function.py`
2. Paste this code:
```python
def calculate_monthly_payment(principal, annual_rate, years):
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    return principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
```

3. Select the function
4. In Copilot Chat, type: `/explain`
5. Then type: `/tests`
6. Then type: `/doc`

**Reflexion**: Did Copilot generate useful tests? Is the documentation clear?

---

## Part 4: GitHub Copilot Agent Mode

### What is Agent Mode?

**Agent Mode** = Copilot can execute multi-step plans:
* Read multiple files
* Generate or edit multiple files
* Run terminal commands (with approval)
* Iterate based on test results

**When to use Agent Mode**:
* Multi-file refactoring
* Generating boilerplate for a new feature
* Setting up a new module with tests and docs
* Migrating code patterns across files

**When NOT to use Agent Mode**:
* Simple single-file edits (use Chat instead)
* Exploratory questions (use Chat instead)
* When you want fine-grained control over each edit

### How to Use Agent Mode

1. Open Copilot Chat
2. Type `@workspace` to enable workspace-wide context
3. Provide a detailed prompt with 3C framework
4. Review the proposed plan
5. Approve or adjust
6. Review each file change in the diff view
7. Run tests and verify

### Example Agent Mode Prompt

```
@workspace
Create a new module for transaction categorization.

[Context]
We have a Transaction model in src/models.py with fields: txn_id, amount, currency, description.
We need to categorize transactions (e.g., "GROCERIES", "UTILITIES", "ENTERTAINMENT") based on description keywords.

[Constraints]
- Create new folder: src/categorization/
- Use Python 3.9+
- Use simple keyword matching (no ML)
- Must be deterministic
- Include comprehensive tests
- Follow existing project structure (see src/data_quality/)

[Criteria]
Create:
1. src/categorization/__init__.py
2. src/categorization/categorizer.py with:
   - categorize_transaction(description: str) -> str function
   - Keyword map for 5 categories (GROCERIES, UTILITIES, ENTERTAINMENT, TRANSPORT, OTHER)
   - Return "OTHER" for unmatched descriptions
3. src/categorization/categories.py with:
   - Category enum
   - Keyword mappings (dict)
4. tests/test_categorization.py with:
   - Test cases for each category
   - Test for "OTHER" default
   - Test for case-insensitivity
5. src/categorization/README.md with usage examples

Success criteria:
- All tests pass (pytest)
- Code is documented
- README has copy-paste examples
```

### Exercise 3: Agent Mode Practice (15 min)

**Task**: Use Agent Mode to create a simple utility module.

**Prompt**:
```
@workspace
Create a currency conversion utility module.

[Context]
We need to convert transaction amounts between currencies for reporting.
This is for internal use only, using fixed exchange rates (not real-time).

[Constraints]
- Create in src/day1/utils/currency_converter.py
- Support only USD, EUR, GBP
- Use hardcoded rates: 1 USD = 0.85 EUR = 0.73 GBP
- No external API calls
- Use Decimal for precision

[Criteria]
Create:
1. convert(amount: Decimal, from_currency: str, to_currency: str) -> Decimal
2. get_rate(from_currency: str, to_currency: str) -> Decimal
3. Raise ValueError for unsupported currencies
4. Include docstrings
5. Include tests in tests/day1/test_currency_converter.py

Success: Tests pass, conversions are accurate to 2 decimal places.
```

**Steps**:
1. Paste prompt into Copilot Chat
2. Review proposed plan
3. Approve
4. Review diffs
5. Run tests: `pytest tests/day1/test_currency_converter.py -v`

**Reflexion**: Did Agent Mode generate correct code? What did you need to fix?

---

## Part 5: GitHub Copilot CLI Essentials

### What is GitHub Copilot CLI?

**GitHub Copilot CLI** = Command-line interface for Copilot that helps with shell commands.

**Use cases**:
* Get suggestions for complex commands
* Explain unfamiliar commands
* Generate one-liners for common tasks

### Installation

```bash
# Install GitHub CLI (if not already installed)
# https://cli.github.com/

# Install Copilot CLI extension
gh extension install github/gh-copilot

# Verify installation
gh copilot --version
```

### Core Commands

#### 1. `gh copilot suggest` - Get command suggestions

**Syntax**: `gh copilot suggest [description]`

**Examples**:

```bash
# Get suggestion for finding files
gh copilot suggest "find all python files modified in the last 7 days"

# Get suggestion for git operations
gh copilot suggest "show git commits from last week by author"

# Get suggestion for system tasks
gh copilot suggest "list processes using port 8080"
```

**Interactive mode** (no description):
```bash
gh copilot suggest
# Then describe what you want
```

#### 2. `gh copilot explain` - Explain a command

**Syntax**: `gh copilot explain [command]`

**Examples**:

```bash
# Explain a complex command
gh copilot explain "find . -name '*.py' -mtime -7 -exec grep -l 'TODO' {} \;"

# Explain git command
gh copilot explain "git log --oneline --graph --all --decorate"

# Explain docker command
gh copilot explain "docker run -d -p 8080:80 -v $(pwd):/app nginx"
```

#### 3. `--target` flag - Specify shell type

```bash
# Target PowerShell
gh copilot suggest --target shell "list all files sorted by size"

# Target Git
gh copilot suggest --target git "undo last commit but keep changes"

# Target GitHub CLI
gh copilot suggest --target gh "create a pull request from current branch"
```

### Banking-Safe CLI Usage Rules

✅ **DO**:
* Use for learning commands
* Use for generating test data scripts
* Use for documentation tasks
* Use for local development workflows

❌ **DON'T**:
* Never include sensitive data in prompts (account numbers, credentials, PII)
* Never run suggested commands without reviewing them first
* Never use for production system commands without approval
* Never share command outputs that contain sensitive info

### Exercise 4: Copilot CLI Practice (10 min)

Try these exercises (adapt for your OS):

#### Exercise 4a: Find files
```bash
gh copilot suggest "find all markdown files in this repository"
```
**Review the suggestion, then run it.**

#### Exercise 4b: Explain a test command
```bash
gh copilot explain "pytest -v --cov=src --cov-report=html tests/"
```
**Read the explanation. Does it make sense?**

#### Exercise 4c: Git workflow
```bash
gh copilot suggest --target git "show files changed in last commit"
```
**Review and run.**

#### Exercise 4d: Generate a script suggestion
```bash
gh copilot suggest "python script to generate 100 synthetic transaction records in CSV format"
```
**Review the suggestion. Would you trust it? What would you verify?**

### Common CLI Patterns for Day 1 Labs

```bash
# Running tests
gh copilot suggest "run python tests in tests/ directory with verbose output"

# Finding and counting files
gh copilot suggest "count number of python files in src/"

# Checking code quality
gh copilot suggest "run python linter on all files in src/"

# Viewing logs
gh copilot suggest "show last 50 lines of application.log and follow new entries"

# Git diffs
gh copilot suggest "show diff of unstaged changes in python files only"
```

---

## Part 6: Paul-Elder Framework Applied to Prompting

### Mapping Paul-Elder to the 3C Framework

| Paul-Elder Element | Maps to | Prompt Section |
|-------------------|---------|----------------|
| **Purpose** | Criteria | What outcome do we want? |
| **Question** | Context | What are we building? |
| **Information** | Context | What files/data are relevant? |
| **Assumptions** | Constraints | What can we assume? What must we avoid? |
| **Implications** | Constraints | What could go wrong? What compliance risks? |
| **Point of View** | All sections | Developer, auditor, user perspectives |

### Advanced Prompt Template (Banking-Grade)

```
[Business Context]
<What business problem are we solving? Why does this matter?>

[Technical Context]
<What code/files exist? What patterns do we follow? What's the current state?>

[Constraints - Technical]
- Language/framework: <specific versions>
- Libraries: <allowed/required libraries>
- Patterns: <architectural patterns to follow>
- Performance: <any performance requirements>

[Constraints - Banking/Compliance]
- Data privacy: <what data can/cannot be used>
- Audit requirements: <what logging/tracking is needed>
- Determinism: <must be reproducible?>
- Error handling: <fail-safe or fail-fast?>

[Acceptance Criteria]
Must have:
1. <specific requirement 1>
2. <specific requirement 2>
...

Should have:
1. <nice-to-have 1>
...

Success metrics:
- <how do we know it works?>
- <what tests must pass?>

[Output Format]
<what files to create/modify? what documentation? what tests?>

[Verification Steps]
1. <how to run/test the code>
2. <what output to expect>

[Auditor's Lens]
<What evidence would an auditor need to see that this code is correct and compliant?>
```

### Exercise 5: Write a Banking-Grade Prompt (15 min)

**Scenario**: Your team needs to implement a daily transaction reconciliation report.

**Your task**: Write a complete prompt using the advanced template above.

**Requirements**:
* Report should aggregate transaction counts and sums by currency
* Should handle missing/invalid data gracefully
* Should output to JSON and CSV
* Should include audit timestamp and report ID
* Should use synthetic data for testing

**Hint**: Think about:
* What constraints matter for a bank report? (determinism, auditability, no data loss)
* What acceptance criteria would an auditor require?
* What verification steps prove it works correctly?

---

## Part 7: Common Prompting Mistakes and Fixes

### Mistake 1: Too Generic

❌ **Bad**: "Write a validator"  
✅ **Good**: "Write a Pydantic validator for the Transaction model that ensures amount > 0, currency is 3 letters, and account_id matches pattern ACC\\d{8}"

### Mistake 2: No Error Handling Specified

❌ **Bad**: "Create a CSV parser"  
✅ **Good**: "Create a CSV parser that yields Transaction objects. Handle malformed rows by logging the error (with row number) and skipping. Raise ValueError if file not found. Include retry logic for file locks (max 3 attempts)."

### Mistake 3: Ambiguous Success Criteria

❌ **Bad**: "Make it faster"  
✅ **Good**: "Optimize the validation loop to process 10,000 transactions in under 1 second on a standard laptop (target: <0.1ms per transaction). Profile before and after. Document optimization techniques used."

### Mistake 4: No Testing Requirements

❌ **Bad**: "Generate a scoring function"  
✅ **Good**: "Generate a credit scoring function with pytest tests covering: valid input, boundary cases (score = 0, score = 100), invalid input types, and a property test that score is always 0-100."

### Mistake 5: Ignoring Existing Code

❌ **Bad**: "Create a Transaction class"  
✅ **Good**: "Using the existing Transaction dataclass in #file:models.py, create a validator function that checks..."

---

## Part 8: Reflexion Checklist for Prompts

After crafting a prompt, ask:

### Pre-Flight Checklist

- [ ] Does the prompt specify **what** to build?
- [ ] Does it specify **constraints** (language, libraries, patterns)?
- [ ] Does it specify **acceptance criteria** (what "done" looks like)?
- [ ] Does it reference relevant **context** (files, existing code)?
- [ ] Does it address **banking/compliance concerns**?
- [ ] Does it specify **test requirements**?
- [ ] Does it specify **error handling** approach?
- [ ] Could an experienced developer execute this prompt without guessing?

### Post-Generation Checklist

- [ ] Did Copilot generate code that meets all criteria?
- [ ] Are there any security or compliance red flags?
- [ ] Do the tests actually test the requirements?
- [ ] Is the code maintainable and documented?
- [ ] Would this pass code review?

---

## Part 9: Key Takeaways

### What We Learned

1. **3C Framework**: Context, Constraints, Criteria structure effective prompts
2. **Copilot Chat**: Use slash commands and context references for efficiency
3. **Agent Mode**: Use for multi-file tasks with clear requirements
4. **Copilot CLI**: Use for command-line productivity (safely)
5. **Paul-Elder**: Apply critical thinking to every prompt
6. **Specificity wins**: Detailed prompts get better code

### Prompting Best Practices

* **Be specific**: Vague prompts → vague code
* **Provide context**: Reference files, explain the situation
* **State constraints**: What must/must not be done
* **Define success**: Explicit acceptance criteria
* **Request tests**: Always ask for tests alongside code
* **Iterate**: Multi-turn conversations refine outputs
* **Review**: Never blindly accept generated code

### What's Next

* **Session 1.3**: Verification and testing mindset
* **Lab 1**: Apply these prompting techniques to build a data quality rules engine

---

## Additional Resources

* [GitHub Copilot Chat Documentation](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide)
* [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
* [Prompt Engineering Guide](https://www.promptingguide.ai/)

---

## Homework (Optional)

Before the afternoon labs:

1. Install and configure GitHub Copilot CLI
2. Practice the 3C framework with a function from your own codebase (use synthetic data)
3. Try Agent Mode to refactor a small module
4. Document one prompting mistake you made and how you fixed it

---

**Next**: [Session 1.3: Verification and Tests](session1_3_verification_and_tests.md)
