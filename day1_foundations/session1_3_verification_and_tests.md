# Session 1.3: Verification and Testing (Banking Compliance Mindset)

**Duration**: 30 minutes (17:15–17:45)  
**Format**: Instructor-led wrap-up with reflexion exercises

## Learning Objectives

By the end of this session, you will be able to:

* Apply a systematic verification approach to AI-generated code
* Write effective tests for AI-assisted development
* Use testing as a source of truth for code correctness
* Apply reflexion techniques to evaluate your own work
* Identify gaps in AI-generated code from a banking compliance perspective
* Create audit-ready evidence for code reviews

## Agenda

| Time | Topic | Format |
|------|-------|--------|
| 17:15–17:25 | Verification mindset for banking | Lecture |
| 17:25–17:35 | Testing strategies for AI code | Discussion + examples |
| 17:35–17:40 | Reflexion: Day 1 retro | Group activity |
| 17:40–17:45 | Q&A and Day 2 preview | Discussion |

---

## Part 1: The Verification Mindset

### Feynman Explanation (Simple Analogy)

**Traditional coding**:
* You write code → You test it → You know it works → You deploy

**AI-assisted coding**:
* AI writes code → **You don't know if it works** → You test it → You verify it matches requirements → You review for hidden issues → *Then* you know it works → You deploy

**Key difference**: With AI, you start from a place of **uncertainty**. Verification is not optional—it's the only way to establish truth.

### In Banking: Why Verification is Critical

In regulated industries, you must be able to prove:

1. **Correctness**: The code does what it claims to do
2. **Completeness**: All requirements are met
3. **Compliance**: No regulatory violations (data privacy, audit trails, etc.)
4. **Reproducibility**: Same inputs → same outputs (for audit reproduction)
5. **Auditability**: Clear evidence trail showing what was built and why

**Without verification**, you have:
* ❌ Code that looks right but might be wrong
* ❌ No proof for auditors
* ❌ No confidence for production deployment
* ❌ Potential regulatory violations

**With verification**, you have:
* ✅ Test results proving correctness
* ✅ Diffs showing exactly what changed
* ✅ Logs demonstrating compliance
* ✅ Documentation for reviewers and auditors

---

## Part 2: The Verification Hierarchy (Banking-Grade)

### Level 1: Syntax and Type Checking (Baseline)

**Goal**: Code compiles/parses and type hints are consistent.

**Tools**:
* Python: `mypy`, `pylint`, `flake8`
* IDE: VS Code's built-in linting

**Example**:
```bash
# Check types
mypy src/

# Check style
flake8 src/

# Check for common issues
pylint src/
```

**What it catches**:
* Type errors
* Undefined variables
* Import errors
* Code style violations

**What it misses**:
* Logic errors
* Business rule violations
* Edge cases

### Level 2: Unit Testing (Core)

**Goal**: Each function/class behaves correctly in isolation.

**Tools**:
* Python: `pytest`, `unittest`
* Coverage: `pytest-cov`

**What to test**:
* Happy path (valid inputs → expected outputs)
* Edge cases (boundary values, empty inputs, large inputs)
* Error cases (invalid inputs → expected exceptions/errors)
* Invariants (properties that must always hold)

**Example test structure**:
```python
import pytest
from decimal import Decimal
from src.models import Transaction
from src.validation import validate_transaction

class TestTransactionValidation:
    """Test suite for transaction validation logic."""
    
    def test_valid_transaction(self):
        """Test that valid transaction passes validation."""
        txn = Transaction(
            txn_id="TX001",
            account_id="ACC12345678",
            amount=Decimal("100.00"),
            currency="USD",
            txn_ts=datetime.now(UTC),
            description="Test"
        )
        is_valid, errors = validate_transaction(txn)
        assert is_valid is True
        assert len(errors) == 0
    
    def test_negative_amount_rejected(self):
        """Test that negative amount is rejected."""
        txn = Transaction(
            txn_id="TX002",
            account_id="ACC12345678",
            amount=Decimal("-50.00"),  # Invalid
            currency="USD",
            txn_ts=datetime.now(UTC),
            description="Test"
        )
        is_valid, errors = validate_transaction(txn)
        assert is_valid is False
        assert "amount must be positive" in str(errors).lower()
    
    def test_invalid_currency_rejected(self):
        """Test that invalid currency format is rejected."""
        txn = Transaction(
            txn_id="TX003",
            account_id="ACC12345678",
            amount=Decimal("100.00"),
            currency="US",  # Invalid (only 2 chars)
            txn_ts=datetime.now(UTC),
            description="Test"
        )
        is_valid, errors = validate_transaction(txn)
        assert is_valid is False
        assert "currency" in str(errors).lower()
    
    def test_future_timestamp_rejected(self):
        """Test that future timestamps are rejected."""
        future_ts = datetime.now(UTC) + timedelta(days=1)
        txn = Transaction(
            txn_id="TX004",
            account_id="ACC12345678",
            amount=Decimal("100.00"),
            currency="USD",
            txn_ts=future_ts,  # Invalid
            description="Test"
        )
        is_valid, errors = validate_transaction(txn)
        assert is_valid is False
        assert "future" in str(errors).lower()
```

**Coverage goal**: Aim for 80%+ line coverage, 100% on critical paths.

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html tests/

# View coverage report
open htmlcov/index.html  # or start htmlcov/index.html on Windows
```

### Level 3: Integration Testing (Realistic Scenarios)

**Goal**: Components work correctly together.

**What to test**:
* File I/O (read CSV, write JSON)
* API endpoints (request → response)
* Database operations (save, retrieve, update)
* Error propagation (errors from one component handled by another)

**Example**:
```python
def test_end_to_end_validation_workflow(tmp_path):
    """Test complete workflow: load CSV → validate → write report."""
    # Arrange: Create synthetic input file
    input_csv = tmp_path / "transactions.csv"
    input_csv.write_text(
        "txn_id,account_id,amount,currency,txn_ts,description\n"
        "TX001,ACC12345678,100.00,USD,2024-01-15T10:00:00Z,Purchase\n"
        "TX002,ACC12345678,-50.00,USD,2024-01-15T10:05:00Z,Refund\n"  # Invalid
    )
    
    output_json = tmp_path / "report.json"
    
    # Act: Run validation engine
    from src.data_quality.cli import run_validation
    run_validation(str(input_csv), str(output_json))
    
    # Assert: Check report structure and content
    import json
    report = json.loads(output_json.read_text())
    
    assert report["total_records"] == 2
    assert report["valid_records"] == 1
    assert report["invalid_records"] == 1
    assert len(report["findings"]) == 1
    assert "TX002" in report["findings"][0]["txn_id"]
```

### Level 4: Property-Based Testing (Advanced)

**Goal**: Verify properties that must always hold, across many random inputs.

**Tool**: `hypothesis` library

**Example**:
```python
from hypothesis import given, strategies as st
from decimal import Decimal

@given(
    amount=st.decimals(min_value=0, max_value=1000000, places=2),
    currency=st.sampled_from(["USD", "EUR", "GBP"])
)
def test_valid_transaction_always_accepted(amount, currency):
    """Property: any transaction with valid fields should pass validation."""
    txn = Transaction(
        txn_id="TX001",
        account_id="ACC12345678",
        amount=amount,
        currency=currency,
        txn_ts=datetime.now(UTC),
        description="Test"
    )
    is_valid, errors = validate_transaction(txn)
    assert is_valid is True, f"Valid transaction rejected: {errors}"
```

**What it catches**: Edge cases you didn't think to test manually.

### Level 5: Audit and Compliance Checks (Banking-Specific)

**Goal**: Ensure code meets regulatory requirements.

**What to verify**:
* No PII in logs or error messages
* Audit trails are complete (all decisions logged)
* Determinism (same input → same output, always)
* Data retention policies followed
* Access controls respected

**Example audit checklist**:
- [ ] All decision points logged (with timestamp, input hash, output)
- [ ] No sensitive data in logs (redact account numbers, PII)
- [ ] All exceptions caught and logged (no silent failures)
- [ ] All inputs validated before processing
- [ ] All outputs include traceability metadata (request ID, timestamp)

**Example audit log validation**:
```python
def test_audit_log_contains_required_fields():
    """Test that all audit log entries have required fields."""
    # Run a scoring request
    response = client.post("/score", json={...})
    
    # Read audit log
    with open("audit_log.jsonl") as f:
        entries = [json.loads(line) for line in f]
    
    # Verify last entry has required fields
    last_entry = entries[-1]
    assert "timestamp" in last_entry
    assert "request_id" in last_entry
    assert "score" in last_entry
    assert "reason_codes" in last_entry
    
    # Verify no PII leaked
    assert "ssn" not in str(last_entry).lower()
    assert "social_security" not in str(last_entry).lower()
```

---

## Part 3: Testing Strategies for AI-Generated Code

### Strategy 1: Test-First Approach

**Workflow**:
1. Write tests *before* asking AI to generate code
2. Run tests (they should fail initially)
3. Ask AI to implement code that passes the tests
4. Verify tests pass
5. Review code for quality

**Why it works**: Tests act as a specification. AI has a clear target.

**Example prompt**:
```
I have these failing tests in tests/test_validator.py:

[paste tests]

Implement the validate_transaction function in src/validation.py to make these tests pass.
Use Pydantic for validation. Include type hints and docstring.
```

### Strategy 2: Specification-by-Example

**Workflow**:
1. Provide examples of input → output in your prompt
2. Ask AI to generate code that matches the examples
3. Convert examples into test cases
4. Verify

**Example prompt**:
```
Create a categorize_transaction function that maps descriptions to categories:

Examples:
- "WHOLE FOODS MARKET" → "GROCERIES"
- "SHELL GAS STATION" → "TRANSPORT"
- "NETFLIX SUBSCRIPTION" → "ENTERTAINMENT"
- "ELECTRIC COMPANY" → "UTILITIES"
- "RANDOM STORE" → "OTHER"

Use keyword matching. Include tests for all examples.
```

### Strategy 3: Mutation Testing (Advanced)

**Goal**: Verify that tests actually catch bugs (test the tests).

**Tool**: `mutmut` (introduces bugs, checks if tests catch them)

```bash
# Run mutation testing
mutmut run --paths-to-mutate=src/

# See results
mutmut results

# Show a specific mutation
mutmut show <id>
```

**Interpretation**:
* If mutmut changes code and tests still pass → test is weak
* If mutmut changes code and tests fail → test is strong ✅

### Strategy 4: Regression Testing

**Goal**: Ensure new changes don't break existing functionality.

**Workflow**:
1. Before changing code, run full test suite (establish baseline)
2. Ask AI to make changes
3. Run full test suite again
4. Verify no previously passing tests now fail

**Command**:
```bash
# Run tests and save results
pytest tests/ -v > baseline_results.txt

# After AI changes
pytest tests/ -v > new_results.txt

# Compare
diff baseline_results.txt new_results.txt
```

---

## Part 4: Code Review Checklist (for AI-Generated Code)

### Functional Correctness

- [ ] Does the code do what it claims to do?
- [ ] Are all requirements met?
- [ ] Are edge cases handled?
- [ ] Do tests pass?
- [ ] Is behavior deterministic (if required)?

### Code Quality

- [ ] Is the code readable and maintainable?
- [ ] Are variable/function names descriptive?
- [ ] Is there appropriate documentation (docstrings, comments)?
- [ ] Is the code idiomatic for the language?
- [ ] Is there unnecessary complexity?

### Banking/Compliance

- [ ] No hardcoded credentials or secrets?
- [ ] No PII in logs or error messages?
- [ ] Are audit trails complete?
- [ ] Are errors handled gracefully (no silent failures)?
- [ ] Is input validation thorough?
- [ ] Is data sanitized before use?

### Security

- [ ] No SQL injection vulnerabilities?
- [ ] No command injection vulnerabilities?
- [ ] No path traversal vulnerabilities?
- [ ] Are dependencies up-to-date and secure?
- [ ] Is data encrypted at rest/in transit (where required)?

### Performance

- [ ] Are there obvious inefficiencies (N+1 queries, unnecessary loops)?
- [ ] Is memory usage reasonable?
- [ ] Are there potential bottlenecks?

---

## Part 5: Reflexion Framework (Day 1 Retro)

### Individual Reflexion (5 min)

Reflect on your Day 1 experience. Answer these questions:

#### What did AI do well?

* What code/tests/docs did AI generate that were immediately useful?
* Where did AI save you time?
* What patterns did AI apply correctly?

#### Where did AI struggle or hallucinate?

* What code did AI generate that was wrong or incomplete?
* What requirements did AI misunderstand?
* What context did AI miss?

#### What evidence do you have that your code works?

* What tests passed?
* What verification steps did you run?
* What outputs/logs did you review?

#### What guardrails did you use?

* How did you structure your prompts?
* What constraints did you specify?
* How did you review AI outputs?

#### What would you do differently next time?

* How would you improve your prompts?
* What additional tests would you write?
* What verification steps would you add?

### Group Discussion (5 min)

Share with the group:

* One thing AI did surprisingly well
* One thing you had to fix or re-prompt
* One lesson learned about prompting or verification

---

## Part 6: Banking-Grade Evidence Package

### What Auditors Need to See

When auditors review your code, they want:

1. **Requirements traceability**: How does code map to business requirements?
2. **Test evidence**: Proof that code was tested and passed
3. **Review evidence**: Who reviewed? What was found? What was fixed?
4. **Change history**: What changed, when, and why (git log)?
5. **Risk assessment**: What could go wrong? How is it mitigated?

### Artifact Checklist (for Each Feature)

- [ ] **Requirements document** or user story
- [ ] **Code** with clear comments and docstrings
- [ ] **Tests** with descriptive names and coverage report
- [ ] **Test results** (pytest output, all tests passing)
- [ ] **Code review notes** (GitHub PR comments or review checklist)
- [ ] **Git commit messages** explaining what and why
- [ ] **Audit logs** (if applicable) showing system behavior
- [ ] **Documentation** (README, API docs, etc.)

### Example Evidence Package Structure

```
feature-transaction-validation/
├── requirements.md                    # What we're building
├── src/validation.py                  # Implementation
├── tests/test_validation.py           # Tests
├── test_results.txt                   # pytest output (all passing)
├── coverage_report.html               # Coverage metrics
├── code_review_checklist.md           # Review checklist (completed)
├── git_log.txt                        # Commit history for this feature
└── demo_output/                       # Sample runs with synthetic data
    ├── sample_input.csv
    └── validation_report.json
```

---

## Part 7: Key Takeaways

### What We Learned Today

1. **Verification is not optional**: AI code must be tested like any other code
2. **Tests are the source of truth**: Passing tests give you confidence
3. **Multiple layers of verification**: Syntax → unit → integration → compliance
4. **Reflexion is a habit**: Always evaluate what worked and what didn't
5. **Evidence is king**: For banking, proof matters more than claims

### Day 1 Success Criteria (Check Yourself)

By now, you should be able to:

- [x] Explain the difference between autocomplete and agentic development
- [x] Write effective prompts using the 3C framework (Context, Constraints, Criteria)
- [x] Use GitHub Copilot Chat and Agent Mode
- [x] Use GitHub Copilot CLI for command-line tasks
- [x] Write tests for AI-generated code
- [x] Apply reflexion to evaluate AI outputs
- [x] Identify common pitfalls and how to avoid them

### Habits to Build

* **Always define acceptance criteria** before asking AI to code
* **Always request tests** alongside implementation
* **Always review diffs** before accepting AI changes
* **Always run tests** after AI generates code
* **Always ask**: "What would an auditor want to see?"

---

## Part 8: Looking Ahead to Day 2

### What's Next?

**Day 2** will cover:
* Model Context Protocol (MCP) for extended AI capabilities
* Connecting to external data sources and tools
* Advanced workflows (code migration, refactoring at scale)
* Building custom MCP servers for banking-specific tasks

### Homework (Optional, Before Day 2)

1. **Review your Day 1 labs**: Run all tests, ensure everything works
2. **Reflect on prompting**: What prompts worked best? Why?
3. **Read about MCP**: [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
4. **Prepare questions**: What workflows do you want to automate?

---

## Part 9: Final Reflexion Exercise

Take 5 minutes to complete this:

### Day 1 Reflexion Form

**What I learned today:**
1. _______________________________________________________________
2. _______________________________________________________________
3. _______________________________________________________________

**What I'm still unclear about:**
1. _______________________________________________________________
2. _______________________________________________________________

**One thing I'll do differently in my work:**
_______________________________________________________________

**One question for Day 2:**
_______________________________________________________________

**How confident do I feel about using AI-assisted development in banking? (1-5)**
[ ] 1 - Not confident  
[ ] 2 - Slightly confident  
[ ] 3 - Moderately confident  
[ ] 4 - Very confident  
[ ] 5 - Extremely confident  

---

## Resources

* [Pytest Documentation](https://docs.pytest.org/)
* [Property-Based Testing with Hypothesis](https://hypothesis.readthedocs.io/)
* [Mutation Testing with mutmut](https://mutmut.readthedocs.io/)
* [Code Coverage with pytest-cov](https://pytest-cov.readthedocs.io/)

---

**Thank you for participating in Day 1!** 

See you tomorrow for Day 2: Advanced Patterns with Model Context Protocol.

---

**Navigation**:
* [Back to Day 1 README](README.md)
* [Lab 1: Data Quality Rules Engine](labs/lab1_data_quality_rules_engine.md)
* [Lab 2: Risk Scoring Service](labs/lab2_simple_risk_scoring_service.md)
