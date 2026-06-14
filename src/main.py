from openai import OpenAI
import json

answerDone = False
jsonRoadmapFile = "roadmap.json"

STARTING_PROMPT = """ You are a strict programming language extractor.\n"
    "Your ONLY job is to detect and output a programming language if present.\n"
    "Do NOT interpret intent. Do NOT ask questions. Do NOT respond conversationally.\n"
    "Do NOT decide whether the user is 'asking to learn' or not.\n\n"
    "RULE 1: If ANY programming language is mentioned in the user message, respond with ONLY the language name.\n"
    "Ignore all other words in the message.\n\n"
    "RULE 2: If NO programming language is mentioned, respond EXACTLY:\n"
    "I get you want to learn programming but what programming language do you want to learn.\n\n"
    "RULE 3: If the message contains NO programming context at all (e.g. greetings, cooking, music, jokes), respond EXACTLY:\n"
    "I cannot help with anything unrelated to programming.\n\n"
    "IMPORTANT RULES:\n"
    "- Language detection ALWAYS has highest priority.\n"
    "- Even if the user says extra words like 'teach me', 'how to learn', 'just tell me', ignore them.\n"
    "- If a language appears anywhere, output ONLY that language.\n\n"
    "Examples:\n"
    "User: hello -> I cannot help with anything unrelated to programming.\n"
    "User: I want to learn cooking -> I cannot help with anything unrelated to programming.\n"
    "User: teach me guitar -> I cannot help with anything unrelated to programming.\n"
    "User: I want to learn programming -> I get you want to learn programming but what programming language do you want to learn.\n"
    "User: I want to learn Python -> Python\n"
    "User: Teach me Python -> Python\n"
    "User: then just tell me how to learn python -> Python\n"
    "User: I want python and javascript -> Python\n", """


PLAN = """ You are an expert programming curriculum designer.\n"
    "Your task is to convert a list of learning roadmap steps into a structured 30-day learning plan.\n\n"
    "INPUT:\n"
    "You will receive an array of topics (roadmap steps).\n\n"
    "TASK:\n"
    "1. Analyze all topics.\n"
    "2. Sort them from easiest to hardest based on typical beginner learning difficulty.\n"
    "3. Distribute them into a 30-day learning plan.\n"
    "4. Each day should contain 1–3 topics depending on difficulty.\n"
    "5. Ensure progressive learning (no advanced topic before basics).\n\n"
    "OUTPUT FORMAT (STRICT JSON ONLY):\n"
    "{\n"
    '  "day_1": ["topic1", "topic2"],\n'
    '  "day_2": ["topic3"],\n'
    "  ...\n"
    '  "day_30": ["topicN"]\n'
    "}\n\n"
    "RULES:\n"
    "- Do NOT include explanations.\n"
    "- Do NOT include markdown.\n"
    "- Do NOT add extra text.\n"
    "- Always return exactly 30 days (day_1 to day_30).\n"
    "- If topics are few, distribute them evenly across 30 days.\n"
    "- If topics are many, group related topics together.\n\n"
    "EXAMPLE INPUT:\n"
    "['variables', 'loops', 'functions', 'OOP', 'recursion']\n\n"
    "EXAMPLE OUTPUT:\n"
    "{\n"
    '  "day_1": ["variables"],\n'
    '  "day_2": ["loops"],\n'
    '  "day_3": ["functions"],\n'
    '  "day_4": ["OOP"],\n'
    '  "day_5": ["recursion"],\n'
    '  "day_6": [],\n'
    "  ...\n"
    '  "day_30": []\n'
    "}\n\n"
    "Now generate the 30-day plan from the provided roadmap."""


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


def createPlan(roadmap):
    roadmap_text = "\n".join(roadmap)

    answer = generate_answer(roadmap_text, PLAN)
    print(f"Your 30-days Plan is following:\n{answer}")


while answerDone == False:
    user_input = input("What do you want to learn and plan today? ")

    answer = generate_answer(user_input, STARTING_PROMPT)

    language = answer.strip()

    if len(answer) > 10:
        print(answer)
    else:
        roadmap = roadmapExtract(language.lower())
        createPlan(roadmap)
        answerDone = True
