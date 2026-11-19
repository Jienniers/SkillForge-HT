"""HTTP endpoints consumed by the React client."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from skillforge.api.schemas import (
    CompletionRequest,
    EvaluationRequest,
    EvaluationResponse,
    HintRequest,
    LevelRequest,
    PracticeRequest,
    RoadmapPdfRequest,
    RoadmapRequest,
)
from skillforge.exceptions import ConfigurationError, GenerationError
from skillforge.services.learning import (
    completion_reward_for,
    evaluate,
    generate_hint_for,
    generate_practice_for,
    generate_roadmap_for,
    level_for_experience,
)
from skillforge.services.pdf import generate_roadmap_pdf
from skillforge.services.validation import validate_roadmap

router = APIRouter(prefix="/api")


@router.post("/roadmap")
def roadmap(request: RoadmapRequest) -> dict[str, list[str]]:
    return _run(generate_roadmap_for, request.language, request.provider)


@router.post("/practice")
def practice(request: PracticeRequest) -> dict[str, dict[str, list[str]]]:
    return _run(generate_practice_for, request.language, request.roadmap, request.provider)


@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate_answer(request: EvaluationRequest) -> EvaluationResponse:
    feedback, correct, xp_awarded = _run(
        evaluate, request.question, request.code, request.language, request.provider
    )
    return EvaluationResponse(feedback=feedback, correct=correct, xp_awarded=xp_awarded)


@router.post("/hint")
def hint(request: HintRequest) -> dict[str, str | int]:
    content, xp_cost = _run(
        generate_hint_for,
        request.question,
        request.language,
        request.level,
        request.xp,
        request.already_charged,
        request.provider,
    )
    return {"hint": content, "xp_cost": xp_cost}


@router.post("/gamification/completion")
def completion(request: CompletionRequest) -> dict[str, int | str | None]:
    reward = _run(
        completion_reward_for,
        request.day_number,
        request.completed_day_count,
        request.first_bonus_given,
    )
    return {"xp": reward.xp, "achievement": reward.achievement}


@router.post("/gamification/level")
def experience_level(request: LevelRequest) -> dict[str, str]:
    return {"level": _run(level_for_experience, request.xp)}


@router.post("/roadmap/pdf")
def roadmap_pdf(request: RoadmapPdfRequest) -> Response:
    plan = _run(validate_roadmap, request.roadmap)
    return Response(
        content=generate_roadmap_pdf(plan),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="SkillForge_Roadmap.pdf"'},
    )


def _run(operation, *args):
    try:
        return operation(*args)
    except ConfigurationError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except GenerationError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
