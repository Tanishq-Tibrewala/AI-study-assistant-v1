import ollama

def generate_plan(topic):

    prompt = f"""
    Create a 7 day study plan for learning:

    {topic}

    Include:
    - daily topics
    - revision
    - practice
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]