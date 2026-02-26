

references:copilot,chatgpt,stackoverfow

This log contains the AI prompts, searches, and references I used while building the Decision Companion System.
I intentionally kept prompts as-is (including spelling/grammar) for transparency.

---

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

---

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

---

## 2026-02-16 — Old prompts used in the initial stage (not included at first)
### Prompts / Queries
-> did they mean a decision making companion which can be used evrywhere not just one scenario

-> so does it mean to be a decision making companion the user will provide their options and weights and systen need to find which one is better rather than finding even better choices or gather more information from that

-> dynamic criteria

-> but choosing a tech stack for a startup and picking an investment strategy needs real world data also to make it more efficient 

->can we do it as parts so that i cam commit with meaningfull messages can we complte this in 10 parts or more

->explain part1 in detail

->explain the problem and the decision companion system and explain the parts we did till part 2 and explain the remaining works

### What I took / concluded
- Keep MVP as a generic “decision engine” that works for any scenario with user inputs.
- Make the build incremental so commit history shows progress and design evolution.

---

## 2026-02-16 to 2026-02-21 — Prompts (uptodate)
### 1) Prompt
"I am building a generic Decision Companion System as a FastAPI web app. 
Help me divide the entire project into clear development parts based on system architecture 
(schemas, decision engine, API, UI, and documentation), so that I can implement and commit each stage incrementally."

### What I took
- Break project into parts (schema → engine → API → explainability → docs → UI) with meaningful commits.

---

### 2) Prompt
"**role**you are a senior software engineer 
**task**you are assigned to built a decision companion system which help users make better real world decisions 
**instructions**the system should should assist a user in evaluating options for a real world decision of their choice.The system should work without relying completely on ai, the system must accept multiple options, accept criteria which may have different weights, provide a ranked recommendation, process and evaluate options against criteria, explain why a particulat recommendation was made, make it a web app use python as the leadind language
**data**example cases are choosing a laptop under budget,selecting a best candidate for a job role, deciding where to travel within constrains, picking an investment plan, choosing a tech stack for a startup"

### What I took
- Use python + FastAPI.
- Keep algorithm explainable and deterministic.
- Generic scenario support with example cases for demo/testing.

---

### 3) Prompt
"explain the different algorithms  like MCDA for decision making based on criteria and weights and explain why MCDA is better"

### What I took
- MCDA is suitable for explainable scoring + ranking.
- Keep WSM as MVP because it is transparent.

---

### 4) Prompt
"explain how normalization actually works and why cost vs benefit criteria need inversion and implement MCDA-WSM algorithm "

### What I took
- Min-max normalization to compare different scales.
- Invert cost criteria during normalization.
- Weighted sum scoring: sum(weight × normalized value).

---

## 2026-02-21 — Algorithm discussion / improvement thoughts
### Prompt / Query
->but i think combining AHP and TOPSIS will give better accuracy than this

### What I concluded
- AHP + TOPSIS can be explored later as alternate engines.
- For MVP, WSM kept because it is simpler to explain and aligns with assignment requirement (not black-box).

---

## 2026-02-21 — Testing & Swagger usage
### Prompt / Query
->give the test cases to check to evaluate inside swagger

### What I took
- Prepared multiple sample inputs (laptop/hiring/travel) and edge cases to validate scoring + explanations.

---

## 2026-02-21 — Part 7 validation & error handling
### Prompt / Query
->give part 7 where the errors are handled properly and also checks duplicate criterion errors ,nr=egatice weights or missing fields values are given by user and also the test cases to check in swagger

### What I took
- Add validation for:
  - duplicate criterion ids
  - negative weights
  - missing option values
- Return clean HTTP 400 errors (instead of raw exceptions).
- Add negative test payloads for Swagger.

---

## 2026-02-21 — Code walkthrough / understanding
### Prompt / Query
->before moving to next session explain the code in deatil

### What I took
- Documented the flow of WSM:
  - validate → normalize weights → normalize values → contributions → score → sort → explain.

---

## 2026-02-21 — Debugging / implementation issues (small searches)
### Notes (what I searched / faced)
- Uvicorn ASGI error: "Attribute 'main' not found in module 'app'"
- Pylance import issue: "Import 'app.api.routes' could not be resolved"
- Git issue: "fatal: pathspec 'BUILD_PROCESS.md' did not match any files" (file name mismatch)
- GitHub Mermaid issue: "Unable to render rich display" / parse error in mermaid flowchart

### What I changed
- Used correct uvicorn target format (`module:app`) for running server.
- Ensured package structure / imports are correct (init files and correct module paths).
- Fixed file naming mismatch (BUILD_PROCESS.md vs BUILT_PROCESS.md).
- Updated Mermaid labels to GitHub-safe format (quotes and `<br/>` instead of `\n`).