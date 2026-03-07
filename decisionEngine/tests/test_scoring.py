from decisionengine.core.scoring import ScoringInput, score_decision
from decisionengine.models.enums import Priority


def test_urgent_priority_scores_better_than_standard():
    base = dict(
        total_distance_km=10,
        total_time_min=20,
        wait_time_min=5,
    )

    standard = score_decision(
        ScoringInput(priority=Priority.STANDARD, **base)
    )

    urgent = score_decision(
        ScoringInput(priority=Priority.CRITICAL, **base)
    )

    assert urgent < standard


def test_wait_time_penalizes_score():
    fast = score_decision(
        ScoringInput(
            total_distance_km=10,
            total_time_min=20,
            wait_time_min=1,
            priority=Priority.STANDARD,
        )
    )

    slow = score_decision(
        ScoringInput(
            total_distance_km=10,
            total_time_min=20,
            wait_time_min=15,
            priority=Priority.STANDARD,
        )
    )

    assert slow > fast
