from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
)


def generate_answer(prompt):
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

    return response.choices[0].message.content.strip()


test_cases = [
    # Should return language names
    ("Teach me Python", "Python"),
    ("I want to learn Python", "Python"),
    ("I wanna learn python", "Python"),
    ("I want to learn programming and it's Python", "Python"),
    ("Can you teach me JavaScript?", "JavaScript"),
    ("I want to learn Go programming", "Go"),
    ("Help me learn Java", "Java"),
    ("Teach me Rust", "Rust"),
    ("I would like to study C++", "C++"),
    # Programming but no language specified
    (
        "I want to learn programming",
        "I get you want to learn programming but what programming language do you want to learn.",
    ),
    (
        "I want to start coding",
        "I get you want to learn programming but what programming language do you want to learn.",
    ),
    (
        "Teach me programming",
        "I get you want to learn programming but what programming language do you want to learn.",
    ),
    # Learning something unrelated to programming
    (
        "I want to learn cooking",
        "I cannot help with anything unrelated to programming.",
    ),
    (
        "Teach me guitar",
        "I cannot help with anything unrelated to programming.",
    ),
    (
        "I want to learn chess",
        "I cannot help with anything unrelated to programming.",
    ),
    # Not asking to learn anything
    (
        "What's the weather today?",
        "I cannot help with anything unrelated to programming.",
    ),
    (
        "Tell me a joke",
        "I cannot help with anything unrelated to programming.",
    ),
    (
        "Hello there",
        "I cannot help with anything unrelated to programming.",
    ),
    (
        "then just tell me how to learn python",
        "Python",
    ),
    (
        "I want to learn programming and its python then just tell me how to learn python",
        "Python",
    ),
]


passed = 0
failed = 0

print("=" * 80)
print("Running tests...")
print("=" * 80)

for i, (user_input, expected) in enumerate(test_cases, start=1):
    actual = generate_answer(user_input)

    if actual.lower() == expected.lower():
        print(f"✅ Test {i}: PASSED")
        passed += 1
    else:
        print(f"❌ Test {i}: FAILED")
        print(f"   Input:    {user_input}")
        print(f"   Expected: {expected}")
        print(f"   Actual:   {actual}")
        failed += 1

print("\n" + "=" * 80)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Accuracy: {(passed / len(test_cases)) * 100:.2f}%")
print("=" * 80)
