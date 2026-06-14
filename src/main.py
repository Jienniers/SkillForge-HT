from openai import OpenAI
import json

answerDone = False
jsonRoadmapFile = "roadmap.json"


def roadmapExtract(language):
    with open(jsonRoadmapFile, "r", encoding="utf-8") as f:
        data = json.load(f)

    steps = data["roadmaps"][language]["steps"]
    for step in steps:
        print(step)


while answerDone == False:
    user_input = input("What do you want to learn and plan today? ")

    def generate_answer(prompt):
        client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

        response = client.chat.completions.create(
            model="qwen2.5-coder-7b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict programming language extractor.\n"
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
                        "User: I want python and javascript -> Python\n"
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response.choices[0].message.content

    answer = generate_answer(user_input)

    language = answer.strip()

    if language.lower() == "python":
        roadmapExtract(language.lower())
        answerDone = True
    elif language.lower() == "javascript":
        roadmapExtract(language.lower())
        answerDone = True
    elif language.lower() == "java":
        roadmapExtract(language.lower())
        answerDone = True
    elif language.lower() == "c++":
        roadmapExtract(language.lower())
        answerDone = True
    elif language.lower() == "go":
        roadmapExtract(language.lower())
        answerDone = True
    else:
        print(answer)
