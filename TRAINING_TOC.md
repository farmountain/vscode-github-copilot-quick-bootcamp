# Training Table of Contents

**GitHub Copilot Quick Bootcamp**: Banking-Grade Agentic Development

---

## Quick Start

* [Main README](README.md) - Overview and getting started
* [Prerequisites](docs/prerequisites.md) - What you need before starting

---

## Day 1: Foundations (VS Code + Copilot Chat + Agent Mode + Copilot CLI)

**Goal**: Learn to reliably go from task → agent prompt → multi-file change → tests/verification → readable docs using synthetic data only.

### Day 1 Overview
* **[Day 1 README](day1_foundations/README.md)** - Complete Day 1 guide and schedule

### Sessions

1. **[Session 1.1: Introduction to Agentic Development](day1_foundations/session1_1_intro_to_agentic_dev.md)** (09:00–10:30)
   - From autocomplete to agentic AI
   - Mental models and safety considerations
   - Paul-Elder critical thinking framework
   - Inversion thinking and failure modes
   - Copilot Chat basics

2. **[Session 1.2: Prompting in VS Code](day1_foundations/session1_2_prompting_in_vscode.md)** (10:45–12:15)
   - 3C Framework: Context, Constraints, Criteria
   - GitHub Copilot Chat features (slash commands, context references)
   - GitHub Copilot Agent Mode walkthrough
   - GitHub Copilot CLI essentials
   - Advanced prompting techniques

3. **[Session 1.3: Verification and Testing](day1_foundations/session1_3_verification_and_tests.md)** (17:15–17:45)
   - Verification hierarchy (syntax → unit → integration → compliance)
   - Testing strategies for AI-generated code
   - Code review checklists
   - Reflexion framework
   - Creating audit-ready evidence

### Hands-On Labs

1. **[Lab 1: Data Quality Rules Engine](day1_foundations/labs/lab1_data_quality_rules_engine.md)** (13:30–15:30)
   - Build a transaction validation system
   - Implement deterministic validation rules
   - Create audit-ready reports
   - Generate synthetic test data
   - Write comprehensive tests

2. **[Lab 2: Simple Risk Scoring Service](day1_foundations/labs/lab2_simple_risk_scoring_service.md)** (15:45–17:15)
   - Build an explainable credit risk API (FastAPI)
   - Implement deterministic scoring with reason codes
   - Create audit logging
   - Write API tests
   - Generate synthetic credit applications

### Reference Materials

* **[Day 1 Prompts Playbook](day1_foundations/prompts/day1_prompts.md)** - All copy-paste prompts for labs
  - Prompt D1-1: Generate Lab 1 code
  - Prompt D1-2: Generate Lab 2 code
  - Prompt D1-3: Add VS Code tasks
  - Prompt D1-4: Add Copilot CLI mini-bootcamp
  - Quick prompts for common tasks
  - Troubleshooting guide

---

## Day 2: Advanced Patterns with Model Context Protocol (MCP)

**Goal**: Extend AI capabilities with MCP servers for banking-specific workflows.

### Day 2 Overview
* **Coming soon**: Day 2 materials (advanced MCP integration)

### Planned Topics

1. **Session 2.1: Introduction to Model Context Protocol**
   - What is MCP and why it matters
   - MCP architecture (client, server, transport)
   - Banking use cases for MCP

2. **Session 2.2: Working with MCP Servers**
   - Installing and configuring MCP servers
   - Using pre-built MCP servers
   - Integrating MCP with Copilot

3. **Session 2.3: Building Custom MCP Servers**
   - MCP server basics
   - Creating banking-specific MCP tools
   - Testing and deploying MCP servers

### Planned Labs

1. **Lab 3: Document Analysis with MCP**
   - Use MCP to analyze policy documents
   - Extract compliance requirements
   - Generate validation rules

2. **Lab 4: Custom MCP Server for Banking Workflows**
   - Build an MCP server for transaction enrichment
   - Integrate with existing systems
   - Add custom tools for banking operations

---

## Day 3: Real-World Banking Workflows

**Goal**: Apply AI-assisted development to realistic banking scenarios.

### Day 3 Overview
* **Coming soon**: Day 3 materials (real-world applications)

### Planned Topics

1. **Session 3.1: Code Migration and Refactoring**
   - Migrating legacy systems with AI assistance
   - Large-scale refactoring patterns
   - Maintaining compliance during migration

2. **Session 3.2: Integration Patterns**
   - Integrating AI-generated code with existing systems
   - API design and documentation
   - Error handling and resilience

3. **Session 3.3: Production Readiness**
   - Deployment strategies
   - Monitoring and observability
   - Compliance documentation

### Planned Labs

1. **Lab 5: Migrate a Legacy Service**
   - Modernize an old codebase
   - Maintain behavior while improving structure
   - Add tests and documentation

2. **Lab 6: Build a Complete Banking Feature**
   - End-to-end feature development
   - Multi-service integration
   - Production-ready documentation

---

## Reference Documentation

### Frameworks and Templates

* [Paul-Elder Critical Thinking Framework](docs/frameworks/paul_elder_framework.md)
* [Feynman Explanation Template](docs/frameworks/feynman_template.md)
* [Inversion Thinking Guide](docs/frameworks/inversion_thinking.md)
* [Reflexion Framework](docs/frameworks/reflexion_framework.md)

### Templates

* [Prompt Template (3C Framework)](docs/templates/prompt_template.md)
* [Test Suite Template](docs/templates/test_suite_template.md)
* [API Documentation Template](docs/templates/api_doc_template.md)
* [Code Review Checklist](docs/templates/code_review_checklist.md)

### Additional Resources

* [Banking Safety Guidelines](docs/banking_safety_guidelines.md)
* [Compliance Checklist](docs/compliance_checklist.md)
* [Troubleshooting Guide](docs/troubleshooting.md)
* [Glossary](docs/glossary.md)

---

## Quick Navigation

### By Role

**For Developers**:
* Start with [Day 1 README](day1_foundations/README.md)
* Use [Prompts Playbook](day1_foundations/prompts/day1_prompts.md) for quick reference
* Check [Troubleshooting Guide](docs/troubleshooting.md) when stuck

**For Instructors**:
* Review all session materials in order
* Use session timings and agendas for planning
* Adapt exercises based on learner pace

**For Auditors/Reviewers**:
* Focus on verification sections in each session
* Review [Banking Safety Guidelines](docs/banking_safety_guidelines.md)
* Check [Compliance Checklist](docs/compliance_checklist.md)

### By Task

**Setting up your environment**:
1. [Prerequisites](docs/prerequisites.md)
2. [Day 1 README - Quick Start](day1_foundations/README.md#quick-start-how-to-run-day-1)

**Learning to prompt effectively**:
1. [Session 1.2: Prompting in VS Code](day1_foundations/session1_2_prompting_in_vscode.md)
2. [Prompt Template (3C Framework)](docs/templates/prompt_template.md)
3. [Prompts Playbook](day1_foundations/prompts/day1_prompts.md)

**Building your first project**:
1. [Lab 1: Data Quality Rules Engine](day1_foundations/labs/lab1_data_quality_rules_engine.md)
2. [Lab 2: Risk Scoring Service](day1_foundations/labs/lab2_simple_risk_scoring_service.md)

**Testing and verification**:
1. [Session 1.3: Verification and Testing](day1_foundations/session1_3_verification_and_tests.md)
2. [Test Suite Template](docs/templates/test_suite_template.md)
3. [Code Review Checklist](docs/templates/code_review_checklist.md)

---

## Progress Tracking

Use this checklist to track your progress through the bootcamp:

### Day 1: Foundations
- [ ] Completed Session 1.1 (Intro to Agentic Dev)
- [ ] Completed Session 1.2 (Prompting in VS Code)
- [ ] Completed Lab 1 (Data Quality Rules Engine)
  - [ ] All code generated
  - [ ] All tests passing
  - [ ] Verified with sample data
- [ ] Completed Lab 2 (Risk Scoring Service)
  - [ ] API running
  - [ ] All tests passing
  - [ ] Audit log working
- [ ] Completed Session 1.3 (Verification and Testing)
- [ ] Day 1 Reflexion completed

### Day 2: Advanced Patterns (Coming Soon)
- [ ] Completed Session 2.1
- [ ] Completed Session 2.2
- [ ] Completed Session 2.3
- [ ] Completed Lab 3
- [ ] Completed Lab 4

### Day 3: Real-World Workflows (Coming Soon)
- [ ] Completed Session 3.1
- [ ] Completed Session 3.2
- [ ] Completed Session 3.3
- [ ] Completed Lab 5
- [ ] Completed Lab 6

---

## Success Criteria

By the end of this bootcamp, you should be able to:

### Day 1 Outcomes
- [x] Articulate the difference between autocomplete and agentic development
- [x] Write effective prompts using the 3C framework
- [x] Use GitHub Copilot Chat and Agent Mode effectively
- [x] Use GitHub Copilot CLI for command-line productivity
- [x] Write comprehensive tests for AI-generated code
- [x] Apply verification and reflexion techniques
- [x] Create audit-ready documentation and evidence

### Day 2 Outcomes (Coming Soon)
- [ ] Understand Model Context Protocol architecture
- [ ] Install and configure MCP servers
- [ ] Build custom MCP tools for banking workflows
- [ ] Integrate MCP with existing systems

### Day 3 Outcomes (Coming Soon)
- [ ] Migrate legacy code with AI assistance
- [ ] Build production-ready features end-to-end
- [ ] Apply AI-assisted development to real banking workflows
- [ ] Create complete compliance documentation

---

## Support

* **Questions during training**: Ask your instructor or use the dedicated Q&A sessions
* **Technical issues**: See [Troubleshooting Guide](docs/troubleshooting.md)
* **Feedback**: Share your experiences in the Day 1/2/3 Reflexion sessions

---

## Version History

* **v1.0.0** (2024-01-15): Initial Day 1 content release
  - Sessions 1.1, 1.2, 1.3
  - Labs 1 and 2
  - Prompts playbook
  - Core frameworks and templates

---

**Ready to start?** → [Day 1 README](day1_foundations/README.md)
