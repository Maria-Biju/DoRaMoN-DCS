references:copilot,chatgpt,stackoverfow
## 2026-02-16 — Initial exploration (problem understanding)
### Prompt / Query
help me built a decision companion system that helpes user make better decision

### Source
AI assistant output and stack overflow(generic blueprint)

### What I took
- Use transparent MCDA (weighted sum) as default.
- Keep criteria user-defined (generic).
- Provide explanations + sensitivity.

### What I rejected / modified
- Rejected “cloud-native microservices / Kubernetes” scope as unnecessary for take-home.
- Rejected heavy ML/SHAP/LIME: adds black-box feel; not required.
- Modified architecture to: FastAPI + minimal JS UI + pure-python engine.

---

## 2026-02-16 — Clarifying scope (generic vs scenario-specific)
### Prompt / Query
the system should assist a user in evaluating options for a real world decision of their choice

### What I concluded
- Build a generic engine + demo with example scenarios.
- Ensure system is not hard-coded to laptops/travel etc.

---

## 2026-02-16 — Generic system plan
### Prompt / Query
generic

### What I took
- Dynamic criteria schema: {name, direction, weight, type}.
- Options store values keyed by criterion id.
- Provide contribution table & sensitivity.

## 2026-02-16 — Copilot brainstorming (web app architecture)
### Source
GitHub Copilot suggestion

### What I accepted
- Web app with frontend + backend separation
- Weighted scoring as the core evaluation method
- AI (if used) should be optional and not the decision-maker

### What I rejected (and why)
- External API data fetching: increases scope and reduces reliability; not required by assignment
- Database + auth: not required for MVP; adds time with little evaluation benefit
- Heavy AI summarization: can reduce explainability and needs citation/provenance


->prompts
1)I am building a generic Decision Companion System as a FastAPI web app. 
Help me divide the entire project into clear development parts based on system architecture 
(schemas, decision engine, API, UI, and documentation), so that I can implement and commit each stage incrementally.
