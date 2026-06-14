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
