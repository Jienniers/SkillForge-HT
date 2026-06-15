from openai import OpenAI
import json

jsonRoadmapFile = "./roadmap.json"

USE_BREAKS = True

languages = {"1": "Python", "2": "JavaScript", "3": "Java"}


def generate_answer(prompt, promptStructure):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    response = client.chat.completions.create(
        model="qwen2.5-coder-7b-instruct",
        messages=[
            {"role": "system", "content": promptStructure},
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.choices[0].message.content


def roadmapExtract(language):
    with open(jsonRoadmapFile, "r", encoding="utf-8") as f:
        data = json.load(f)

    steps = data["roadmaps"][language]["steps"]
    return steps


def createPlan(roadmap, USE_BREAKS):
    roadmap_text = json.dumps(roadmap)

    PLAN = f"""
    You are an expert programming curriculum designer.

    Your task is to convert a list of learning roadmap steps into a structured 30-day learning plan.

    INPUT:
    You will receive an array of learning topics (roadmap steps).

    GLOBAL FLAG:
    USE_BREAKS = {USE_BREAKS}

    CRITICAL PACING RULE (MOST IMPORTANT):
    You MUST NOT speedrun the curriculum.
    You MUST spread learning evenly across all 30 days.
    Each concept should be learned slowly with proper spacing and reinforcement.

    STRICT LEARNING SPEED RULES:
    - Maximum 1 core concept per day (very important)
    - If a topic is large (e.g., OOP, Web Dev), split it across multiple days
    - NEVER combine more than 1 major concept in a single day
    - You MUST revisit earlier concepts implicitly through progression (do not skip ahead)

    LEARNING FLOW RULE:
    - One concept must be fully introduced before moving to the next
    - No jumping from basics directly to frameworks
    - No clustering multiple advanced topics early

    LEARNING ORDER PRIORITY:
    1. Syntax, variables, data types
    2. Control flow (if/else, loops)
    3. Functions
    4. Data structures (lists, dicts, sets, tuples)
    5. OOP (must be spread across multiple days)
    6. File handling & error handling
    7. Libraries (requests, numpy, pandas) (must be separated across days)
    8. Web frameworks (Flask/Django) (must take multiple days)
    9. Projects & practice days

    BREAK RULE (VERY IMPORTANT):
    - If USE_BREAKS is true:
        - Include exactly 1 rest day every 5–7 learning days
        - Rest days MUST be spread out across the plan
        - NEVER place all rest days at the end
        - Rest days must be between learning days (natural spacing)
        - Rest day format: ["rest"]

    - If USE_BREAKS is false:
        - No rest days allowed

    ANTI-SPEEDRUN RULE:
    - Do NOT compress multiple topics just to finish early
    - Do NOT complete the roadmap before day 30
    - You MUST stretch learning across the full 30 days evenly

    TASK:
    1. Break topics into small teachable steps
    2. Spread them evenly across 30 days
    3. Ensure proper prerequisite order
    4. Ensure no day is overloaded
    5. Ensure slow progressive learning

    OUTPUT FORMAT (STRICT JSON ONLY):
    {{
    "day_1": ["topic"],
    "day_2": ["topic"],
    ...
    "day_30": ["topic"]
    }}

    RULES:
    - Do NOT include explanations
    - Do NOT include markdown
    - Do NOT add extra text
    - Always return exactly 30 days
    - Keep learning slow, spaced, and realistic for beginners

    Now generate the 30-day plan.
    """

    answer = generate_answer(roadmap_text, PLAN)
    print(f"Your 30-days Plan is following:\n{answer}")


def userChoice():
    choice = ""

    while choice not in ["1", "2", "3"]:
        print("Please select the programming language you want to learn:")
        print("1. Python")
        print("2. JavaScript")
        print("3. Java")

        choice = input("Enter your choice (1, 2, or 3): ")

    # Ask about breaks
    breaks = ""
    while breaks not in ["y", "n"]:
        breaks = input("Do you want rest days in your 30-day plan? (y/n): ").lower()

    return choice, breaks


choice, breaks = userChoice()

USE_BREAKS = breaks == "y"

roadmap = roadmapExtract(languages[choice].lower())

createPlan(roadmap, USE_BREAKS)
