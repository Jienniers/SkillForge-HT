from openai import OpenAI

answerDone = False

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
                        "You are a strict programming intent classifier.\n"
                        "You MUST follow the rules in order. If multiple rules apply, choose ONLY the first matching rule.\n\n"
                        "RULE 1: If the user is NOT asking to learn anything related to programming (or is asking about anything unrelated like cooking, music, jokes, general questions, greetings), respond EXACTLY:\n"
                        "I cannot help with anything unrelated to programming.\n\n"
                        "RULE 2: If the user IS asking to learn something, but it is NOT related to programming, respond EXACTLY:\n"
                        "I cannot help with anything unrelated to programming.\n\n"
                        "RULE 3: If the user IS asking to learn programming BUT does NOT specify a programming language, respond EXACTLY:\n"
                        "I get you want to learn programming but what programming language do you want to learn.\n\n"
                        "IMPORTANT FOR RULE 3:\n"
                        "- 'Teach me programming', 'I want to learn programming', 'Help me learn programming' ALL count as missing language.\n\n"
                        "RULE 4: If the user clearly specifies a programming language, respond with ONLY the language name.\n"
                        "No punctuation, no explanation, no extra words.\n\n"
                        "Examples:\n"
                        "User: hello -> I cannot help with anything unrelated to programming.\n"
                        "User: I want to learn cooking -> I cannot help with anything unrelated to programming.\n"
                        "User: teach me guitar -> I cannot help with anything unrelated to programming.\n"
                        "User: I want to learn programming -> I get you want to learn programming but what programming language do you want to learn.\n"
                        "User: Teach me Python -> Python\n"
                        "User: I want to learn JavaScript -> JavaScript\n"
                        "User: I want to learn Go programming -> Go\n"
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
        print("Ok lets start with learning python")
        answerDone = True
    elif language.lower() == "javascript":
        print("Ok lets start with learning JavaScript")
        answerDone = True
    elif language.lower() == "java":
        print("Ok lets start with learning Java")
        answerDone = True
    elif language.lower() == "c++":
        print("Ok lets start with learning C++")
        answerDone = True
    elif language.lower() == "go":
        print("Ok lets start with learning Go")
        answerDone = True
    else:
        print(language)

