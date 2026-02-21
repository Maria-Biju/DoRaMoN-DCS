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


-->old prompts used in the initial stage  which not included at first


-> did they mean a decision making companion which can be used evrywhere not just one scenario

-> so does it mean to be a decision making companion the user will provide their options and weights and systen need to find which one is better rather than finding even better choices or gather more information from that

-> dynamic criteria

-> but choosing a tech stack for a startup and picking an investment strategy needs real world data also to make it more efficient 

->can we do it as parts so that i cam commit with meaningfull messages can we complte this in 10 parts or more

->explain part1 in detail
->explain the problem and the decision companion system and explain the parts we did till part 2 and explain the remaining works


->            prompts uptodate

1)"I am building a generic Decision Companion System as a FastAPI web app. 
Help me divide the entire project into clear development parts based on system architecture 
(schemas, decision engine, API, UI, and documentation), so that I can implement and commit each stage incrementally."

2)"**role**you are a senior software engineer 
**task**you are assigned to built a decision companion system which help users make better real world decisions 
**instructions**the system should should assist a user in evaluating options for a real world decision of their choice.The system should work without relying completely on ai, the system must accept multiple options, accept criteria which may have different weights, provide a ranked recommendation, process and evaluate options against criteria, explain why a particulat recommendation was made, make it a web app use python as the leadind language
**data**example cases are choosing a laptop under budget,selecting a best candidate for a job role, deciding where to travel within constrains, picking an investment plan, choosing a tech stack for a startup"

3)"explain the different algorithms  like MCDA for decision making based on criteria and weights and explain why MCDA is better"

4)"explain how normalization actually works and why cost vs benefit criteria need inversion and implement MCDA-WSM algorithm "
       