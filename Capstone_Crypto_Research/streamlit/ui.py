import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Crypto Researcher", layout="wide")

st.title("🧠 Crypto Researcher")
st.caption("Semantic search over real-time crypto & finance news")
st.divider()
if st.button("🔄 Refresh Crypto News (Fetch Latest)"):
    with st.spinner("Fetching and indexing latest news..."):
        resp = requests.post(
            f"{API_BASE}/ingest/news",
            timeout=180
        )

    if resp.status_code == 200:
        st.success("News refreshed and indexed successfully ✅")
    else:
        st.error(f"Failed to refresh news ({resp.status_code})")
        st.code(resp.text)


query = st.text_input("Search crypto news", placeholder="Bitcoin ETF inflows")

top_k = st.slider("Number of results", 3, 10, 5)
use_summary = st.checkbox("Generate AI summary")


if st.button("Search") and query:
    endpoint = "/query/summarize" if use_summary else "/query/search"

    with st.spinner("Processing..."):
        response = requests.post(
            f"{API_BASE}{endpoint}",
            json={"query": query, "top_k": top_k},
            timeout=180
        )
        if response.status_code != 200:
            st.error(f"Backend error {response.status_code}")
        st.code(response.text)
        st.stop()
        data = response.json()

    if use_summary:
        st.subheader("🧠 AI Summary")
        clean_summary = data["summary"].replace("\n", "<br>")
        st.markdown(
    f"""
    <div style="
        background-color:#f6f7f9;
        padding:16px;
        border-radius:8px;
        font-size:16px;
        line-height:1.5;
        max-height:260px;
        overflow:hidden;
    ">
    {clean_summary}
    </div>
    """,
    unsafe_allow_html=True
)

        results = data["sources"]
    else:
        results = data["results"]

    if not results:
        st.warning("No results found.")
    else:
        for r in results:
            st.markdown("### " + r.get("title", "No title"))
            st.write(r.get("content", "")[:500] + "...")
            st.write(f"**Source:** {r.get('source')}")
            st.write(f"**Score:** {round(r.get('score', 0), 4)}")
            st.markdown("---")
