from typing import Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field

# Criterion types supported in the MVP
CriterionType = Literal["number", "boolean", "category"]

# Whether higher values are better or worse
GoalType = Literal["benefit", "cost"]


class Criterion(BaseModel):
    """
    A criterion is a dimension used to evaluate options.
    Example: Price (cost), Battery (benefit), Risk (cost)
    """
    id: str = Field(..., min_length=1, description="Unique id used as key in option.values")
    name: str = Field(..., min_length=1, description="Human-friendly name shown in UI")
    weight: float = Field(..., ge=0, description="Relative importance; engine will normalize weights")
    goal: GoalType = Field(..., description="benefit = higher is better, cost = lower is better")
    ctype: CriterionType = Field(..., description="Data type of values entered for this criterion")

    # Only used when ctype == "category": map label -> score (0..1)
    scale: Optional[Dict[str, float]] = Field(
        default=None,
        description="For category criteria: mapping like {'High': 1, 'Medium': 0.6, 'Low': 0.2}"
    )


class Option(BaseModel):
    """
    An option is one candidate choice in the decision.
    values is keyed by criterion.id.
    """
    name: str = Field(..., min_length=1)
    values: Dict[str, Union[float, bool, str]] = Field(
        default_factory=dict,
        description="Keyed by criterion id; value can be number/bool/category label"
    )


class Scenario(BaseModel):
    """
    A Scenario bundles criteria + options for a decision.
    """
    title: str = Field(default="Untitled Decision")
    criteria: List[Criterion] = Field(default_factory=list)
    options: List[Option] = Field(default_factory=list)


# ---- Placeholder response model for the next parts ----
class OptionExplanation(BaseModel):
    name: str
    score: float
    contributions: Dict[str, float]
    strengths: List[str]=[]
    weaknesses: List[str]=[]
    why: str =""


class EvaluationResult(BaseModel):
    title: str
    ranked_option_names: List[str]
    details: List[OptionExplanation]
