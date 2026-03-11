import ollama

def generate_quiz(text):

    prompt = f"""
Generate 5 quiz questions.

Format EXACTLY:

Q: question
A: answer
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user","content":prompt + text}]
    )

    lines = response["message"]["content"].split("\n")

    questions=[]
    answers=[]
    q=None

    for line in lines:

        if line.startswith("Q:"):
            q=line[2:].strip()

        if line.startswith("A:") and q:
            a=line[2:].strip()
            questions.append(q)
            answers.append(a)
            q=None

    return questions,answers