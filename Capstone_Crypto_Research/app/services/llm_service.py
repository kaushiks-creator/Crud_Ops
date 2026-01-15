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
Summarize the news below grouped by sentiment:

- Bullish signals
- Bearish risks
- Neutral context
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

    def clean_summary(text: str) -> str:
        lines = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.lower().startswith(("here are", "summary", "summarize")):
                continue
            lines.append(line)
        return "\n".join(lines)
    summary = clean_summary(summary)

    return summary

def stream_summary(prompt: str):
    with requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": True
        },
        stream=True,
        timeout=180
    ) as r:
        for line in r.iter_lines():
            if line:
                yield line.decode()
