from agent_framework import Agent, Goal, Environment, AgentFunctionCallingActionLanguage, generate_response, register_tool, PythonActionRegistry
import random
from typing import List, Optional
import sys

goals = [
    Goal(priority=1, name="Select Meal", description="You are an agent that helps the user select a valid meal that respects their calory and time limits. "
                                                    "Every meal should contain a starter, a main course and a dessert, in that order. "
                                                    "You can use the select_random_starter, select_random_main_course and select_random_dessert actions to select each item of the meal. "
                                                    "Use the validate_meal action with the exact dish names (strings) for starter, main course, and dessert against the user's calorie and time limits. "
                                                    "You should change the choice of starter, main course or dessert until the total meal is valid and respects the limits (if any). "
                                                    "If the meal is over the calory limit, you can choose a lighter course using select_lighter_starter, select_lighter_main_course, or select_lighter_dessert; pass the current dish's exact name as a string. "
                                                    "If the meal is over the time limit, use select_faster_starter, select_faster_main_course, or select_faster_dessert with the current dish name as a string. "
                                                    "If the user does not specify either calories or time limits, ignore that parameter. "
                                                    "If validate_meal returns true, do not look for a better meal. "),
    Goal(priority=1, name="Terminate", description="Call the terminate action immediately when you have selected the meal and validate_meal returns true "
                                                    "and provide the content of the meal to the user in the terminate message. In that message, include "
                                                    "the starter, main course and dessert names in the message. also include preparation time and calories. "
                                                    "Finally say a little and short nice sentence to the user. ")
]

starters = [
    {"name": "Bruschetta al Pomodoro", "calories": 180, "prep_time_minutes": 15},
    {"name": "French Onion Soup", "calories": 350, "prep_time_minutes": 60},
    {"name": "Shrimp Cocktail", "calories": 150, "prep_time_minutes": 20},
    {"name": "Stuffed Mushrooms", "calories": 210, "prep_time_minutes": 30},
    {"name": "Caesar Salad", "calories": 290, "prep_time_minutes": 15},
    {"name": "Gazpacho", "calories": 120, "prep_time_minutes": 20},
    {"name": "Beef Carpaccio", "calories": 230, "prep_time_minutes": 25},
    {"name": "Spinach & Ricotta Arancini", "calories": 310, "prep_time_minutes": 45},
    {"name": "Smoked Salmon Blinis", "calories": 260, "prep_time_minutes": 30},
    {"name": "Caprese Salad", "calories": 200, "prep_time_minutes": 10},
]

main_courses = [
    {"name": "Beef Bourguignon", "calories": 650, "prep_time_minutes": 180},
    {"name": "Grilled Salmon with Lemon Butter", "calories": 480, "prep_time_minutes": 25},
    {"name": "Chicken Tikka Masala", "calories": 520, "prep_time_minutes": 50},
    {"name": "Spaghetti Carbonara", "calories": 610, "prep_time_minutes": 30},
    {"name": "Mushroom Risotto", "calories": 430, "prep_time_minutes": 45},
    {"name": "Roast Rack of Lamb", "calories": 720, "prep_time_minutes": 90},
    {"name": "Pad Thai", "calories": 550, "prep_time_minutes": 30},
    {"name": "Coq au Vin", "calories": 580, "prep_time_minutes": 120},
    {"name": "Vegetable Moussaka", "calories": 390, "prep_time_minutes": 75},
    {"name": "Pan-Seared Duck Breast", "calories": 490, "prep_time_minutes": 40},
]

desserts = [
    {"name": "Crème Brûlée", "calories": 340, "prep_time_minutes": 60},
    {"name": "New York Cheesecake", "calories": 490, "prep_time_minutes": 90},
    {"name": "Chocolate Lava Cake", "calories": 380, "prep_time_minutes": 25},
    {"name": "Tiramisu", "calories": 450, "prep_time_minutes": 30},
    {"name": "Lemon Tart", "calories": 320, "prep_time_minutes": 75},
    {"name": "Baklava", "calories": 430, "prep_time_minutes": 90},
    {"name": "Panna Cotta with Berry Coulis", "calories": 300, "prep_time_minutes": 20},
    {"name": "Apple Tarte Tatin", "calories": 410, "prep_time_minutes": 60},
    {"name": "Mango Sorbet", "calories": 160, "prep_time_minutes": 15},
    {"name": "Sticky Toffee Pudding", "calories": 520, "prep_time_minutes": 55},
]

def _find_by_name(items: List[dict], name: str) -> Optional[dict]:
    """Finds a dish by name in the list of dishes.

    Args:
        items: The list of dishes.
        name: The name of the dish to find.
    Returns:
        The dish if found, None otherwise.
    """
    if not name or not str(name).strip():
        return None
    key = str(name).strip().lower()
    for item in items:
        if item["name"].strip().lower() == key:
            return item
    return None

@register_tool(tags=["meal_selector", "initialize"])
def select_random_starter() -> dict:
    """Selects a random starter from the list of starters.

    Returns:
        A random starter from the list of starters.
    """
    return random.choice(starters)

@register_tool(tags=["meal_selector", "initialize"])
def select_random_main_course() -> dict:
    """Selects a random main course from the list of main courses.

    Returns:
        A random main course from the list of main courses.
    """
    return random.choice(main_courses)

@register_tool(tags=["meal_selector", "initialize"])
def select_random_dessert() -> dict:
    """Selects a random dessert from the list of desserts.

    Returns:
        A random dessert from the list of desserts.
    """
    return random.choice(desserts)

@register_tool(tags=["meal_selector", "improve"])
def select_lighter_starter(starter_name: str) -> dict:
    """Selects a random starter with fewer calories than the dish named by starter_name (exact menu string).

    Args:
        starter_name: The name of the starter to select.
    Returns:
        A random starter with fewer calories than the dish named by starter_name.
    """
    starter = _find_by_name(starters, starter_name)
    if not starter:
        raise ValueError(f"Unknown starter: {starter_name!r}")
    candidates = [x for x in starters if x["calories"] < starter["calories"]]
    if not candidates:
        raise ValueError("No starter has fewer calories than the given dish.")
    return random.choice(candidates)


@register_tool(tags=["meal_selector", "improve"])
def select_lighter_main_course(main_course_name: str) -> dict:
    """Selects a random main course with fewer calories than the dish named by main_course_name (exact menu string).

    Args:
        main_course_name: The name of the main course to select.
    Returns:
        A random main course with fewer calories than the dish named by main_course_name.
    """
    main_course = _find_by_name(main_courses, main_course_name)
    if not main_course:
        raise ValueError(f"Unknown main course: {main_course_name!r}")
    candidates = [x for x in main_courses if x["calories"] < main_course["calories"]]
    if not candidates:
        raise ValueError("No main course has fewer calories than the given dish.")
    return random.choice(candidates)


@register_tool(tags=["meal_selector", "improve"])
def select_lighter_dessert(dessert_name: str) -> dict:
    """Selects a random dessert with fewer calories than the dish named by dessert_name (exact menu string).

    Args:
        dessert_name: The name of the dessert to select.
    Returns:
        A random dessert with fewer calories than the dish named by dessert_name.
    """
    dessert = _find_by_name(desserts, dessert_name)
    if not dessert:
        raise ValueError(f"Unknown dessert: {dessert_name!r}")
    candidates = [x for x in desserts if x["calories"] < dessert["calories"]]
    if not candidates:
        raise ValueError("No dessert has fewer calories than the given dish.")
    return random.choice(candidates)


@register_tool(tags=["meal_selector", "improve"])
def select_faster_starter(starter_name: str) -> dict:
    """Selects a random starter with shorter prep time than the dish named by starter_name (exact menu string).

    Args:
        starter_name: The name of the starter to select.
    Returns:
        A random starter with shorter prep time than the dish named by starter_name.
    """
    starter = _find_by_name(starters, starter_name)
    if not starter:
        raise ValueError(f"Unknown starter: {starter_name!r}")
    candidates = [x for x in starters if x["prep_time_minutes"] < starter["prep_time_minutes"]]
    if not candidates:
        raise ValueError("No starter has shorter prep time than the given dish.")
    return random.choice(candidates)


@register_tool(tags=["meal_selector", "improve"])
def select_faster_main_course(main_course_name: str) -> dict:
    """Selects a random main course with shorter prep time than the dish named by main_course_name (exact menu string).

    Args:
        main_course_name: The name of the main course to select.
    Returns:
        A random main course with shorter prep time than the dish named by main_course_name.
    """
    main_course = _find_by_name(main_courses, main_course_name)
    if not main_course:
        raise ValueError(f"Unknown main course: {main_course_name!r}")
    candidates = [x for x in main_courses if x["prep_time_minutes"] < main_course["prep_time_minutes"]]
    if not candidates:
        raise ValueError("No main course has shorter prep time than the given dish.")
    return random.choice(candidates)


@register_tool(tags=["meal_selector", "improve"])
def select_faster_dessert(dessert_name: str) -> dict:
    """Selects a random dessert with shorter prep time than the dish named by dessert_name (exact menu string).

    Args:
        dessert_name: The name of the dessert to select.
    Returns:
        A random dessert with shorter prep time than the dish named by dessert_name.
    """
    dessert = _find_by_name(desserts, dessert_name)
    if not dessert:
        raise ValueError(f"Unknown dessert: {dessert_name!r}")
    candidates = [x for x in desserts if x["prep_time_minutes"] < dessert["prep_time_minutes"]]
    if not candidates:
        raise ValueError("No dessert has shorter prep time than the given dish.")
    return random.choice(candidates)


@register_tool(tags=["meal_selector", "validate"])
def validate_meal(
    starter_name: str,
    main_course_name: str,
    dessert_name: str,
    max_calories: int = sys.maxsize,
    max_prep_time_minutes: int = sys.maxsize,
) -> tuple[bool, str]:
    """Validates the meal using exact dish names from the menu (strings). Optionally pass max_calories and max_prep_time_minutes when the user specified limits.

    Args:
        starter_name: The name of the starter to validate.
        main_course_name: The name of the main course to validate.
        dessert_name: The name of the dessert to validate.
    Returns:
        A tuple containing a boolean indicating if the meal is valid and a string describing the meal.
    """
    if not starter_name or not main_course_name or not dessert_name:
        return False, "Error: starter_name, main_course_name, and dessert_name are required for validate_meal."

    starter = _find_by_name(starters, starter_name)
    main_course = _find_by_name(main_courses, main_course_name)
    dessert = _find_by_name(desserts, dessert_name)
    missing = []
    if not starter:
        missing.append("starter")
    if not main_course:
        missing.append("main_course")
    if not dessert:
        missing.append("dessert")
    if missing:
        return False, f"Error: Unknown dish name(s): {', '.join(missing)}."

    total_calories = starter["calories"] + main_course["calories"] + dessert["calories"]
    if total_calories > max_calories:
        return False, f"Error: The total calories of the meal ({total_calories}) are over the limit ({max_calories})"
    total_prep_time = starter["prep_time_minutes"] + main_course["prep_time_minutes"] + dessert["prep_time_minutes"]
    if total_prep_time > max_prep_time_minutes:
        return False, f"Error: The total preparation time of the meal ({total_prep_time}) are over the limit ({max_prep_time_minutes})"
    return True, f"The meal is valid: {total_calories} calories and {total_prep_time} minutes of preparation time"

@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the session and prints the meal content to the user in the terminate message

    Args:
        message: The message to print to the user.
    Returns:
        The message to print to the user.
    """
    return f"{message}"

agent = Agent(
    goals, 
    agent_language=AgentFunctionCallingActionLanguage(), 
    action_registry=PythonActionRegistry(tags=["meal_selector", "system"]), 
    generate_response=generate_response, 
    environment=Environment()
)

user_input = "Select a meal for me which has less than 1100 calories and that I can prepare in less than 60 minutes"
final_memory = agent.run(user_input)

print("--------------------------------")
print("Final Result:")
print(final_memory.get_memories()[-1].get("content"))