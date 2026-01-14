import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3"

def summarize_articles(query: str, articles: list[dict]) -> str:
    context = "\n\n".join(
        f"- {a['title']}: {a['content'][:300]}" for a in articles
    )

    prompt = f"""
You are a crypto finance analyst.

User query:
{query}

Articles:
{context}

Summarize the following news in **4 short bullet points**.
Each bullet must be **one sentence only**.
Total length must be **under 120 words**.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )
    response.raise_for_status()

    response = response.json()["response"]
    summary = response.strip()
    return summary

