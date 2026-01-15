def build_summary_prompt(query: str, articles: list[dict]) -> str:
    bullish = []
    bearish = []
    neutral = []

    for a in articles:
        text = f"{a['title']}: {a['content'][:300]}"
        if a.get("sentiment") == "bullish":
            bullish.append(text)
        elif a.get("sentiment") == "bearish":
            bearish.append(text)
        else:
            neutral.append(text)

    def block(title, items):
        if not items:
            return f"{title}:\nNone\n"
        joined = "\n".join(f"- {i}" for i in items[:3])
        return f"{title}:\n{joined}\n"

    prompt = f"""
You are a professional crypto market analyst.

User query:
{query}

Summarize the following news in **4 concise bullet points total**.
Each bullet must be **one sentence**.
Maximum total length: **120 words**.

Focus on:
- Market-moving information
- Institutional signals
- Risks and opportunities

{block("Bullish signals", bullish)}
{block("Bearish risks", bearish)}
{block("Neutral context", neutral)}
"""

    return prompt.strip()
