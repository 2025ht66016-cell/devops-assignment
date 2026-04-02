PROGRAMS = {
    "FL": {
        "code": "FL",
        "name": "Fat Loss",
        "summary": "High-intensity conditioning and a calorie-controlled nutrition plan.",
        "workout": "Mon: 5x5 Back Squat + AMRAP\nTue: EMOM 20min Assault Bike\nWed: Bench Press + 21-15-9\nThu: 10RFT Deadlifts/Box Jumps\nFri: 30min Active Recovery",
        "diet": "B: 3 Egg Whites + Oats Idli\nL: Grilled Chicken + Brown Rice\nD: Fish Curry + Millet Roti\nTarget: 2,000 kcal",
        "color": "#e74c3c",
        "calorie_factor": 22,
    },
    "MG": {
        "code": "MG",
        "name": "Muscle Gain",
        "summary": "Progressive strength blocks with a calorie-surplus meal plan.",
        "workout": "Mon: Squat 5x5\nTue: Bench 5x5\nWed: Deadlift 4x6\nThu: Front Squat 4x8\nFri: Incline Press 4x10\nSat: Barbell Rows 4x10",
        "diet": "B: 4 Eggs + PB Oats\nL: Chicken Biryani (250g Chicken)\nD: Mutton Curry + Jeera Rice\nTarget: 3,200 kcal",
        "color": "#2ecc71",
        "calorie_factor": 35,
    },
    "BG": {
        "code": "BG",
        "name": "Beginner",
        "summary": "Foundational conditioning for new members focused on form and consistency.",
        "workout": "Circuit Training: Air Squats, Ring Rows, Push-ups.\nFocus: Technique Mastery & Form (90% Threshold)",
        "diet": "Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati.\nProtein: 120g/day",
        "color": "#3498db",
        "calorie_factor": 26,
    },
}


def get_program_by_code(program_code: str):
    return PROGRAMS.get(program_code.upper())


def get_programs_summary() -> list[dict[str, str]]:
    return [
        {
            "code": program["code"],
            "name": program["name"],
            "summary": program["summary"],
            "color": program["color"],
            "calorie_factor": program["calorie_factor"],
        }
        for program in PROGRAMS.values()
    ]


def calculate_calories(program_code: str, weight_kg: float) -> int | None:
    """Return estimated daily calories: weight_kg × calorie_factor, or None on bad input."""
    if not weight_kg or weight_kg <= 0:
        return None
    program = get_program_by_code(program_code)
    if program is None:
        return None
    return int(weight_kg * program["calorie_factor"])


# ── v1.1.2: in-memory client store ────────────────────────────────────────────

_CLIENTS: list[dict] = []


def add_client(name: str, age: int, weight_kg: float, program_code: str,
               adherence: int, notes: str = "") -> dict | None:
    """Add a client record. Returns the record or None if program is invalid."""
    if get_program_by_code(program_code) is None:
        return None
    record = {
        "name": name,
        "age": age,
        "weight_kg": weight_kg,
        "program_code": program_code.upper(),
        "adherence": max(0, min(100, adherence)),
        "notes": notes,
    }
    _CLIENTS.append(record)
    return record


def get_clients() -> list[dict]:
    return list(_CLIENTS)


def get_clients_csv() -> str:
    """Return all clients as a CSV string."""
    import csv
    import io
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["name", "age", "weight_kg", "program_code",
                                              "adherence", "notes"])
    writer.writeheader()
    writer.writerows(_CLIENTS)
    return buf.getvalue()


def clear_clients() -> None:
    """Clear all clients (used in tests)."""
    _CLIENTS.clear()