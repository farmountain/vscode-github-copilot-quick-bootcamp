# Session 1.1: Introduction to Agentic Development

**Duration**: 90 minutes (09:00–10:30)  
**Format**: Instructor-led with micro-exercises

## Learning Objectives

By the end of this session, you will be able to:

* Explain the evolution from code autocomplete to agentic AI development
* Apply mental models for effective human-AI collaboration
* Identify safety and compliance risks in banking contexts
* Use GitHub Copilot Chat for basic coding assistance
* Apply critical thinking frameworks to AI-assisted development

## Agenda

| Time | Topic | Format |
|------|-------|--------|
| 09:00–09:15 | Welcome & mental models | Lecture |
| 09:15–09:30 | From autocomplete to agentic dev | Lecture + demo |
| 09:30–09:50 | Banking safety & compliance mindset | Discussion |
| 09:50–10:10 | Micro-exercises: Copilot Chat basics | Hands-on |
| 10:10–10:25 | Inversion thinking: failure modes | Group activity |
| 10:25–10:30 | Reflexion & Q&A | Discussion |

---

## Part 1: Mental Models for AI-Assisted Development

### Feynman Explanation (Simple Analogy)

**Imagine you're leading a team at a bank:**

* **Traditional coding** = You write every line yourself, like preparing a regulatory report by hand
* **Code autocomplete** = Someone suggests the next word as you type, like auto-fill in forms
* **AI pair programmer** = A junior teammate who reads your comments and drafts code sections
* **Agentic AI** = A capable teammate who can take a task description, read multiple files, write code across several files, and run verification steps—but **you're still the team lead who reviews and approves everything**

**The key shift**: You move from "writing code" to "defining requirements, reviewing outputs, and ensuring quality."

### Technical Definition

**Agentic AI Development** refers to AI systems that can:

1. **Understand context**: Read your codebase, understand file relationships, parse requirements
2. **Plan**: Break down a task into steps
3. **Execute**: Generate or modify code across multiple files
4. **Verify**: Run tests, check syntax, iterate on failures
5. **Explain**: Describe what was done and why

**GitHub Copilot Agent Mode** is an implementation of this in VS Code, where Copilot can:
* Edit multiple files based on a prompt
* Create new files and directory structures
* Run terminal commands (with your approval)
* Iterate based on test results

### Why This Matters in Banking

* **Accelerated development**: Routine tasks (boilerplate, tests, documentation) can be generated quickly
* **Consistency**: AI can apply patterns uniformly across a codebase
* **Knowledge transfer**: Junior developers can learn faster by seeing how AI applies best practices
* **Risk**: If used carelessly, AI can introduce subtle bugs, compliance violations, or security issues

---

## Part 2: The Evolution from Autocomplete to Agentic AI

### Timeline of Capabilities

| Era | Capability | Example | Banking Impact |
|-----|------------|---------|----------------|
| **2010s** | Autocomplete | IntelliSense suggests method names | Minor productivity gain |
| **2021** | Line/block completion | Copilot suggests next few lines | Moderate speed-up on boilerplate |
| **2023** | Chat-based assistance | Ask questions, get code snippets | Knowledge at your fingertips |
| **2024+** | Agentic workflows | "Migrate this API to use async" → multi-file changes | Dramatic acceleration, but requires strong review |

### What Changed?

1. **Context windows expanded**: Early models saw ~2K tokens; modern models see 100K+ tokens (entire codebases)
2. **Tool use**: Models can now call functions (read files, run tests, search documentation)
3. **Iteration**: Models can see their mistakes and retry

### GitHub Copilot Features (Day 1 Focus)

* **Copilot Autocomplete**: Inline suggestions as you type (classic Copilot)
* **Copilot Chat**: Conversational interface in VS Code sidebar
  - Ask questions about code
  - Generate functions or classes
  - Explain existing code
  - Fix errors
* **Agent Mode** (in Chat): Give a high-level task, Copilot proposes a plan and executes it
* **Copilot CLI**: Command-line interface for shell command suggestions and explanations

---

## Part 3: Banking Safety & Compliance Mindset

### Core Principle: "Trust, but Verify"

In banking, we operate under rigorous regulatory frameworks (SOX, Basel III, GDPR, etc.). AI-generated code must meet the same standards as human-written code.

### Paul-Elder Critical Thinking Checklist (for Every AI Task)

**Before you run any AI prompt**, consider:

| Element | Banking Question |
|---------|------------------|
| **Purpose** | What business outcome does this serve? |
| **Question** | What specifically are we asking the AI to do? |
| **Information** | What data/files will it access? Is any of it sensitive? |
| **Assumptions** | What does the AI assume about our environment, dependencies, or data? |
| **Implications** | If this code fails or leaks data, what's the regulatory impact? |
| **Point of View** | Have we considered this from developer, auditor, and compliance perspectives? |

### Example Application

**Task**: "Generate a function to validate customer credit scores"

**Paul-Elder Analysis**:
* **Purpose**: Ensure data quality before risk modeling
* **Question**: Do we want validation rules, error handling, logging?
* **Information**: Will use synthetic data for training; production version needs PII controls
* **Assumptions**: AI might assume we store scores in plain text; we actually encrypt at rest
* **Implications**: If validation is wrong, we might approve bad loans (credit risk) or reject good customers (reputational risk)
* **Point of View**: Developer wants speed; auditor wants evidence trail; compliance wants data privacy

**Result**: You craft a much better prompt that specifies synthetic data, includes audit logging, and excludes PII.

---

## Part 4: Inversion Thinking – How Projects Fail

**Inversion** = Instead of asking "How do we succeed?", ask "How do we fail?" Then avoid those failure modes.

### Top 5 Failure Modes in AI-Assisted Banking Development

| Failure Mode | Description | Prevention |
|--------------|-------------|------------|
| **1. Vague prompts** | "Make it better" → AI guesses wrong | Use specific acceptance criteria: "Add input validation for ISO-8601 dates" |
| **2. No tests** | AI generates code that looks good but has edge-case bugs | Always request tests; run them before merge |
| **3. Blind trust** | Assuming AI-generated code is correct | Mandate human review; use diff tools |
| **4. Data leakage** | Copy-pasting real customer data into prompts | Use synthetic data only; redact before sharing |
| **5. No audit trail** | Can't prove to regulators how a decision was made | Log all inputs/outputs; version control everything |

### Micro-Exercise (5 min): Identify the Failure

**Scenario**: A developer prompts Copilot: *"Write a function to calculate interest"*

**AI generates**:
```python
def calculate_interest(principal, rate):
    return principal * rate
```

**Questions**:
1. What's missing? (time period, compounding logic, input validation, currency)
2. What could go wrong in production? (negative principal, rate > 100%, no audit trail)
3. How would you improve the prompt?

**Better prompt**:
> "Write a Python function `calculate_simple_interest(principal: Decimal, annual_rate: Decimal, days: int) -> Decimal` that calculates simple interest for a given number of days. Include input validation (principal > 0, 0 <= rate <= 1, days > 0). Raise ValueError for invalid inputs. Use Decimal for precision. Add docstring with examples."

---

## Part 5: Hands-On Micro-Exercises (Copilot Chat)

### Setup

1. Open VS Code in this training repository
2. Open Copilot Chat (sidebar icon or `Ctrl+Shift+I` / `Cmd+Shift+I`)
3. Ensure you're signed into GitHub Copilot

### Exercise 1: Simple Code Generation (5 min)

**Task**: Ask Copilot to generate a Python dataclass for a bank transaction.

**Prompt** (paste into Copilot Chat):
```
Create a Python dataclass called Transaction with these fields:
- txn_id: str
- account_id: str
- amount: Decimal
- currency: str (3-letter code)
- txn_ts: datetime
- description: str

Use the dataclasses module and typing for type hints. Import Decimal from decimal.
```

**Observe**:
* How complete is the code?
* Did it include imports?
* Did it add any extra features (like validation)?

**Reflexion**: What would you need to add for production use? (Validation, serialization, audit fields?)

### Exercise 2: Explain Existing Code (5 min)

**Task**: Ask Copilot to explain a piece of code.

**Prompt**:
```
Explain this Python code in simple terms suitable for a business analyst:

def validate_transaction(txn):
    if txn.amount <= 0:
        return False, "Amount must be positive"
    if len(txn.currency) != 3:
        return False, "Currency must be 3-letter code"
    return True, "Valid"
```

**Reflexion**: Did Copilot's explanation make sense? What context did it miss?

### Exercise 3: Add Tests (5 min)

**Task**: Ask Copilot to generate tests for the validation function.

**Prompt**:
```
Write pytest unit tests for the validate_transaction function. Include test cases for:
- Valid transaction
- Negative amount
- Zero amount
- Invalid currency (too short, too long, empty)
- Edge case: very large amount

Use descriptive test names and AAA pattern (Arrange, Act, Assert).
```

**Reflexion**: Are the tests comprehensive? What edge cases might be missing?

### Exercise 4: Improve with Constraints (5 min)

**Task**: Ask Copilot to refactor code with specific banking constraints.

**Prompt**:
```
Refactor this function to use Pydantic for validation instead of manual checks. Ensure:
- All fields are required
- Amount must be a positive Decimal
- Currency must be exactly 3 uppercase letters
- Add a validator to ensure txn_ts is not in the future
- Include clear error messages for each validation failure

def validate_transaction(txn):
    if txn.amount <= 0:
        return False, "Amount must be positive"
    if len(txn.currency) != 3:
        return False, "Currency must be 3-letter code"
    return True, "Valid"
```

**Reflexion**: Did Copilot understand all constraints? Did it generate idiomatic Pydantic code?

---

## Part 6: Reflexion Framework for AI Outputs

After every AI interaction, ask yourself:

### Reflexion Checklist

| Question | Why It Matters |
|----------|----------------|
| **Did the AI understand the task?** | Misunderstandings lead to wrong implementations |
| **Is the code idiomatic and readable?** | Non-standard code is hard to maintain |
| **Are edge cases handled?** | Banking requires robustness |
| **Are there security or compliance issues?** | Regulatory violations can be costly |
| **Can I explain this code to an auditor?** | You own the code, not the AI |
| **What would break if inputs change?** | Anticipate future issues |

### Traffic Light System

Use this simple heuristic:

* 🟢 **Green**: Code looks good, tests pass, no obvious issues → Proceed
* 🟡 **Yellow**: Code works but needs refinement (comments, edge cases, performance) → Iterate
* 🔴 **Red**: Code has bugs, security issues, or doesn't meet requirements → Reject and re-prompt

**Rule**: Never merge red or yellow code without fixing issues first.

---

## Part 7: Key Takeaways

### What We Learned

1. **Agentic AI ≠ Autopilot**: You're still the lead; AI is the assistant
2. **Mental model**: AI is a capable teammate who needs clear instructions and review
3. **Paul-Elder framework**: Apply critical thinking to every prompt
4. **Inversion**: Avoid failure modes by thinking about what could go wrong
5. **Reflexion**: Always evaluate AI outputs systematically

### Banking-Specific Principles

* **Synthetic data only**: Never use real customer data in training or prompts
* **Test everything**: AI code is not automatically correct
* **Audit trail**: Keep diffs, logs, and test results for compliance
* **Human accountability**: You own the code, not the AI
* **Deterministic behavior**: Banking systems must be reproducible

### What's Next

* **Session 1.2**: Learn advanced prompting techniques for VS Code and Copilot CLI
* **Lab 1**: Build a real data quality rules engine with AI assistance

---

## Additional Resources

* [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
* [Paul-Elder Critical Thinking Framework](https://www.criticalthinking.org/pages/universal-intellectual-standards/527)
* [Inversion Thinking (Farnam Street)](https://fs.blog/inversion/)

---

## Micro-Homework (Optional)

Before Session 1.2, try this:

1. Find a simple function in your codebase (or write one)
2. Ask Copilot Chat to explain it
3. Ask Copilot Chat to generate tests for it
4. Ask Copilot Chat to suggest improvements
5. Evaluate each response using the Reflexion Checklist

**Note**: Use only non-sensitive code or synthetic examples.

---

**Next**: [Session 1.2: Prompting in VS Code](session1_2_prompting_in_vscode.md)
