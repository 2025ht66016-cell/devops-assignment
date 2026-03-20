"""
Unit tests for ACEest Fitness & Gym v1.0 business logic.
Covers: programme catalogue, workout/diet retrieval, color codes, gym metrics.
"""

import pytest
from aceest_logic import (
    PROGRAMS,
    GYM_METRICS,
    get_program_names,
    get_program,
    get_workout,
    get_diet,
    get_color,
)

# ---------------------------------------------------------------------------
# Programme catalogue
# ---------------------------------------------------------------------------

class TestProgramCatalogue:
    def test_exactly_three_programs_exist(self):
        assert len(PROGRAMS) == 3

    def test_all_expected_programs_present(self):
        names = get_program_names()
        assert "Fat Loss (FL)" in names
        assert "Muscle Gain (MG)" in names
        assert "Beginner (BG)" in names

    def test_get_program_names_returns_list(self):
        assert isinstance(get_program_names(), list)

    def test_each_program_has_workout_key(self):
        for name, data in PROGRAMS.items():
            assert "workout" in data, f"Missing 'workout' in {name}"

    def test_each_program_has_diet_key(self):
        for name, data in PROGRAMS.items():
            assert "diet" in data, f"Missing 'diet' in {name}"

    def test_each_program_has_color_key(self):
        for name, data in PROGRAMS.items():
            assert "color" in data, f"Missing 'color' in {name}"


# ---------------------------------------------------------------------------
# get_program()
# ---------------------------------------------------------------------------

class TestGetProgram:
    def test_returns_dict_for_valid_name(self):
        result = get_program("Fat Loss (FL)")
        assert isinstance(result, dict)

    def test_returns_none_for_unknown_name(self):
        assert get_program("Unknown Program") is None

    def test_returns_none_for_empty_string(self):
        assert get_program("") is None

    def test_fat_loss_program_keys(self):
        result = get_program("Fat Loss (FL)")
        assert set(result.keys()) == {"workout", "diet", "color"}

    def test_muscle_gain_program_keys(self):
        result = get_program("Muscle Gain (MG)")
        assert set(result.keys()) == {"workout", "diet", "color"}

    def test_beginner_program_keys(self):
        result = get_program("Beginner (BG)")
        assert set(result.keys()) == {"workout", "diet", "color"}


# ---------------------------------------------------------------------------
# get_workout()
# ---------------------------------------------------------------------------

class TestGetWorkout:
    def test_fat_loss_workout_is_string(self):
        assert isinstance(get_workout("Fat Loss (FL)"), str)

    def test_fat_loss_workout_not_empty(self):
        assert len(get_workout("Fat Loss (FL)")) > 0

    def test_muscle_gain_workout_contains_squat(self):
        assert "Squat" in get_workout("Muscle Gain (MG)")

    def test_beginner_workout_contains_circuit(self):
        assert "Circuit" in get_workout("Beginner (BG)")

    def test_unknown_program_returns_none(self):
        assert get_workout("Unknown") is None


# ---------------------------------------------------------------------------
# get_diet()
# ---------------------------------------------------------------------------

class TestGetDiet:
    def test_fat_loss_diet_is_string(self):
        assert isinstance(get_diet("Fat Loss (FL)"), str)

    def test_fat_loss_diet_mentions_target_calories(self):
        assert "2,000 kcal" in get_diet("Fat Loss (FL)")

    def test_muscle_gain_diet_mentions_target_calories(self):
        assert "3,200 kcal" in get_diet("Muscle Gain (MG)")

    def test_beginner_diet_mentions_protein(self):
        assert "Protein" in get_diet("Beginner (BG)")

    def test_unknown_program_returns_none(self):
        assert get_diet("Unknown") is None


# ---------------------------------------------------------------------------
# get_color()
# ---------------------------------------------------------------------------

class TestGetColor:
    def test_fat_loss_color_is_red(self):
        assert get_color("Fat Loss (FL)") == "#e74c3c"

    def test_muscle_gain_color_is_green(self):
        assert get_color("Muscle Gain (MG)") == "#2ecc71"

    def test_beginner_color_is_blue(self):
        assert get_color("Beginner (BG)") == "#3498db"

    def test_all_colors_start_with_hash(self):
        for name in get_program_names():
            assert get_color(name).startswith("#")

    def test_unknown_program_returns_none(self):
        assert get_color("Unknown") is None


# ---------------------------------------------------------------------------
# Gym metrics
# ---------------------------------------------------------------------------

class TestGymMetrics:
    def test_capacity_is_150(self):
        assert GYM_METRICS["capacity"] == 150

    def test_area_is_10000_sqft(self):
        assert GYM_METRICS["area_sqft"] == 10000

    def test_breakeven_members_is_250(self):
        assert GYM_METRICS["breakeven_members"] == 250

