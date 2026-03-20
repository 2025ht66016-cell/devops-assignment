"""
ACEest Fitness & Gym — v1.0 Business Logic
Pure functions extracted from src/aceest_v1.py.
No tkinter dependency — safe to import in tests and CI.
"""

PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": (
            "Mon: 5x5 Back Squat + AMRAP\n"
            "Tue: EMOM 20min Assault Bike\n"
            "Wed: Bench Press + 21-15-9\n"
            "Thu: 10RFT Deadlifts/Box Jumps\n"
            "Fri: 30min Active Recovery"
        ),
        "diet": (
            "B: 3 Egg Whites + Oats Idli\n"
            "L: Grilled Chicken + Brown Rice\n"
            "D: Fish Curry + Millet Roti\n"
            "Target: 2,000 kcal"
        ),
        "color": "#e74c3c",
    },
    "Muscle Gain (MG)": {
        "workout": (
            "Mon: Squat 5x5\n"
            "Tue: Bench 5x5\n"
            "Wed: Deadlift 4x6\n"
            "Thu: Front Squat 4x8\n"
            "Fri: Incline Press 4x10\n"
            "Sat: Barbell Rows 4x10"
        ),
        "diet": (
            "B: 4 Eggs + PB Oats\n"
            "L: Chicken Biryani (250g Chicken)\n"
            "D: Mutton Curry + Jeera Rice\n"
            "Target: 3,200 kcal"
        ),
        "color": "#2ecc71",
    },
    "Beginner (BG)": {
        "workout": (
            "Circuit Training: Air Squats, Ring Rows, Push-ups.\n"
            "Focus: Technique Mastery & Form (90% Threshold)"
        ),
        "diet": (
            "Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati.\n"
            "Protein: 120g/day"
        ),
        "color": "#3498db",
    },
}

GYM_METRICS = {
    "capacity": 150,
    "area_sqft": 10000,
    "breakeven_members": 250,
}


def get_program_names():
    """Return a list of all available programme names."""
    return list(PROGRAMS.keys())


def get_program(name):
    """Return the programme dict for *name*, or None if not found."""
    return PROGRAMS.get(name)


def get_workout(name):
    """Return the workout string for *name*, or None if not found."""
    program = get_program(name)
    return program["workout"] if program else None


def get_diet(name):
    """Return the diet string for *name*, or None if not found."""
    program = get_program(name)
    return program["diet"] if program else None


def get_color(name):
    """Return the UI color hex string for *name*, or None if not found."""
    program = get_program(name)
    return program["color"] if program else None

