architectures:
 Architectural diagram:
```mermaid
flowchart LR
    USER[User / Web UI / Swagger] --> API[FastAPI API Layer]
    API --> SCHEMA[Pydantic Schemas\n(Scenario, Criterion, Option)]
    API --> ENGINE[Decision Engine\n(MCDA - Weighted Sum Model)]
    ENGINE --> UTILS[Normalization + Weight Utilities]
    ENGINE --> API
    API --> RESPONSE[Ranked Recommendation Response]
```
decision logic flowchart:
```mermaid
flowchart TD
    START[Start Evaluation]
    --> CHECK[Check Criteria & Options Valid]

    CHECK --> WEIGHT[Normalize Weights]

    WEIGHT --> LOOP[For Each Criterion]

    LOOP --> GOAL{Goal Type?}
    GOAL -->|Benefit| NORM1[Min-Max Normalize]
    GOAL -->|Cost| NORM2[Invert + Normalize]

    NORM1 --> SCORE
    NORM2 --> SCORE

    SCORE[Compute Contribution\n(weight × normalized value)]
    --> TOTAL[Sum Contributions\nper Option]

    TOTAL --> SORT[Sort Scores Descending]
    SORT --> END[Return Ranked Options]
```
data flow diagram:

```mermaid
flowchart TD
    A[User provides Scenario\n(criteria + options + weights)]
    --> B[FastAPI Endpoint\nPOST /api/evaluate]

    B --> C[Pydantic Validation\nSchemas]

    C --> D[Decision Engine\nMCDA Evaluation]

    D --> E[Normalize Weights]
    E --> F[Normalize Criterion Values]
    F --> G[Calculate Weighted Scores]
    G --> H[Sort Options by Score]

    H --> I[Return Ranked Result JSON]
    I --> J[User receives Recommendation]
```