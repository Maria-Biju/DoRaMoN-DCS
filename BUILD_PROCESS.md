# BUILD_PROCESS

## How I Started

I began by researching what a real-world Decision Companion System should include.  
Initial research was done using Stack Overflow, Copilot, ChatGPT, and technical articles to understand:

- What features a decision-making companion should provide
- Which algorithms are commonly used for multi-criteria decisions
- How to keep the system explainable rather than AI-driven

Initially, I considered building an AI agent or using web scraping to collect real-world data automatically.  
However, after reviewing the assignment requirements, I decided to avoid heavy AI dependence because:

- The problem explicitly emphasizes transparency and explainability.
- AI-based decisions could become black-box outputs.
- A deterministic algorithmic approach would better demonstrate system design thinking.

Because of this, I shifted towards algorithm-based decision logic that could later be extended with AI if needed.

---

## How My Thinking Evolved

During the early design phase, I researched different decision-making techniques such as:

- MCDA (Multi-Criteria Decision Analysis)
- AHP (Analytic Hierarchy Process)
- TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)

After experimentation and comparison, I chose a **normalized weighted scoring model (WSM under MCDA)** because it provides:

- Transparent logic
- Easy explanation to users
- Direct mapping between weights and results
- Reusable architecture

The system evolved step-by-step:

1. Started with a simple ranking engine.
2. Added normalization to handle cost vs benefit criteria.
3. Extended the engine to provide contribution-based explanations.
4. Added strengths/weaknesses and template-based reasoning.
5. Introduced validation and constraint filtering to better match real-world decision flows.
6. Designed diagrams to visualize architecture and logic.

---

## Alternative Approaches Considered

During the design phase, multiple alternatives were evaluated:

### AHP
- Provides structured weight calculation through pairwise comparisons.
- Rejected for MVP because it introduces UI complexity and additional mathematical steps that reduce explainability for non-technical users.

### TOPSIS
- Provides distance-based ranking.
- Considered as a future extension.
- Deferred because explanation of “distance from ideal solution” is harder compared to weighted contributions.

### AI-based Decision System
- Initially considered using AI agents or external data retrieval.
- Rejected for the core engine because the assignment requires explainable logic and not a black-box system.

### Rule-based scoring
- Rejected because hardcoded rules reduce flexibility and scalability.

Future versions may support pluggable engines such as AHP or TOPSIS while keeping the current MCDA engine as default.

---

## Refactoring Decisions

Several structural refactoring decisions were made during development:

- Separated API layer from decision engine so that the logic remains reusable.
- Introduced Pydantic schemas early to enforce structured inputs.
- Moved normalization and weight handling into utility functions to reduce duplication.
- Added a constraints module instead of embedding constraint logic inside scoring to keep responsibilities clear.
- Upgraded response models to include explanations instead of only rankings.

These refactors improved maintainability and made future extensions easier.

---

## Mistakes and Corrections

Some issues encountered during development:

- Incorrect ASGI import path caused the FastAPI app not to load properly.
  - Fixed by running `uvicorn app.main:app --reload` from the project root.
- Early versions returned only ranked option names, which made explanations difficult.
  - Refactored the engine to return contribution data per criterion.
- Initial diagrams did not include constraint filtering.
  - Updated diagrams after introducing Part 8 constraints feature.

These corrections improved both usability and system clarity.

---

## What Changed During Development and Why

The project evolved incrementally:

- **Part 1–2:** Built basic API structure and schemas to support dynamic decision scenarios.
- **Part 3:** Implemented MCDA weighted scoring to produce deterministic rankings.
- **Part 4:** Connected engine to FastAPI endpoint for testing.
- **Part 5:** Added contribution tracking to explain why an option ranks higher.
- **Part 6:** Introduced human-readable explanations (strengths, weaknesses, why message).
- **Part 7:** Added validation and structured error handling for robustness.
- **Part 8:** Implemented constraint filtering to reflect real-world decision requirements.
- **Part 9:** Added architectural and decision diagrams to visualize system design.

Each step was implemented as a small incremental improvement to keep the build process transparent and traceable.

## Refactoring decisions
- Initially, the evaluation function returned only the ranked list. Later I refactored it to return a richer response:
  - `details` (ranked options with scores + per-criterion contributions)
  - `filtered_out` (options removed due to constraints)
  - `companion_insight` (winner vs closest competitor + gap + short summary)
  - `sensitivity` (simple what-if: increase each criterion weight by 10% and observe winner changes)
- This refactor was done to satisfy the requirement: “Explain why the recommendation was made” and to make the system more transparent beyond just a score.

## Mistakes and corrections
- **Return unpacking mismatch (“too many values to unpack”)**
  - Mistake: After extending `evaluate_wsm()` to return 4 values, the API route still unpacked only 2.
  - Fix: Updated the route to unpack all 4 values and return them in `EvaluationResult`.
- **Insights not showing in UI**
  - Mistake: Insights were generated only when `insight_mode` was provided, but the UI payload did not send it.
  - Fix: Removed the gating (always compute insights for MVP) so UI always gets `companion_insight` and `sensitivity`.

## What changed during development and why
- I started with a minimal WSM scoring engine to keep decision logic explainable.
- As the project grew, I added explanation layers:
  - contributions per criterion
  - strengths/weaknesses and a short “why” template
  - competitor gap summary
  - sensitivity checks
- I kept the algorithm simple but made the output richer because the assignment evaluates clarity, transparency, and how I evolved the design.