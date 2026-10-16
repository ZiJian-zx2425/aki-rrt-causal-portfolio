"""Pure timeline checks for a future clinical adapter; never reads patient files."""
import math


def validate_timeline(aki_hour, last_covariate_hour, rrt_hour=None, death_hour=None):
    values = [aki_hour, last_covariate_hour] + [v for v in [rrt_hour, death_hour] if v is not None]
    if not all(math.isfinite(v) for v in values):
        raise ValueError("Timeline requires finite offsets, not missing-date substitutions.")
    if last_covariate_hour > aki_hour:
        raise ValueError("Baseline covariate occurs after time zero.")
    if rrt_hour is not None and rrt_hour < aki_hour:
        raise ValueError("Prevalent treatment: do not move pre-baseline RRT to time zero.")
    if death_hour is not None and death_hour < aki_hour:
        raise ValueError("Death precedes eligibility.")
    if rrt_hour is not None and death_hour is not None and rrt_hour > death_hour:
        raise ValueError("Treatment occurs after death.")


def observed_early_label(rrt_offset_hours, window_hours=24):
    """Retrospective exposure description ONLY; not valid baseline randomization."""
    if window_hours <= 0 or not math.isfinite(window_hours):
        raise ValueError("Window must be finite and positive.")
    if rrt_offset_hours is None:
        return 0
    if not math.isfinite(rrt_offset_hours) or rrt_offset_hours < 0:
        raise ValueError("Treatment offset must be finite and non-negative.")
    return int(rrt_offset_hours <= window_hours)
