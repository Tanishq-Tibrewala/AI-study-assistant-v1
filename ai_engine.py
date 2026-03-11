import ollama

def generate_notes(text):

    prompt = f"""
Create structured study notes from the material.

Include:

1. Summary
2. Key Points
3. Important Concepts

Material:
{text}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user","content":prompt}]
    )

    return response["message"]["content"]


def chat_with_notes(question, context):

    prompt = f"""
Use the study material to answer the question.

Material:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user","content":prompt}]
    )

    return response["message"]["content"]