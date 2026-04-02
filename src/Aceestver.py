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


# ── v2.0.1: SQLite-backed client store ────────────────────────────────────────

import csv
import io
import os
import sqlite3

_DB_PATH = os.environ.get("DB_PATH", "aceest_fitness.db")


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str | None = None) -> None:
    """Create the clients table if it does not exist."""
    path = db_path or _DB_PATH
    with sqlite3.connect(path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                age         INTEGER NOT NULL,
                weight_kg   REAL    NOT NULL,
                program_code TEXT   NOT NULL,
                adherence   INTEGER NOT NULL,
                notes       TEXT    DEFAULT ''
            )
        """)
        conn.commit()


def add_client(name: str, age: int, weight_kg: float, program_code: str,
               adherence: int, notes: str = "") -> dict | None:
    """Insert a client row. Returns the record dict or None if program is invalid."""
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
    with _get_conn() as conn:
        conn.execute(
            "INSERT INTO clients (name, age, weight_kg, program_code, adherence, notes) "
            "VALUES (:name, :age, :weight_kg, :program_code, :adherence, :notes)",
            record,
        )
        conn.commit()
    return record


def get_clients() -> list[dict]:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT name, age, weight_kg, program_code, adherence, notes FROM clients"
        ).fetchall()
    return [dict(row) for row in rows]


def get_clients_csv() -> str:
    """Return all clients as a CSV string."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["name", "age", "weight_kg", "program_code",
                                              "adherence", "notes"])
    writer.writeheader()
    writer.writerows(get_clients())
    return buf.getvalue()


def clear_clients() -> None:
    """Delete all client rows (used in tests)."""
    with _get_conn() as conn:
        conn.execute("DELETE FROM clients")
        conn.commit()