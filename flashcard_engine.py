import ollama

def generate_flashcards(text):

    prompt = f"""
Create 6 flashcards.

Format EXACTLY like:

Q: question
A: answer

Material:
{text}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user","content":prompt}]
    )

    lines = response["message"]["content"].split("\n")

    cards = []
    q = None

    for line in lines:

        if line.startswith("Q:"):
            q = line[2:].strip()

        if line.startswith("A:") and q:
            a = line[2:].strip()
            cards.append((q,a))
            q=None

    return cards