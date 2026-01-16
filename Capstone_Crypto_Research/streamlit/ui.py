import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF
import base64
from io import BytesIO

# PDF Generation Function (defined at the top)
def generate_pdf_report(query, data):
    """Generate a PDF report from search results"""
    
    def clean_text(text):
        """Clean text for PDF encoding - replace special characters"""
        # Replace common unicode characters with ASCII equivalents
        replacements = {
            '\u2022': '-',  # Bullet point
            '\u2013': '-',  # En dash
            '\u2014': '--', # Em dash
            '\u2018': "'",  # Left single quote
            '\u2019': "'",  # Right single quote
            '\u201c': '"',  # Left double quote
            '\u201d': '"',  # Right double quote
            '\u2026': '...', # Ellipsis
            '\u00a0': ' ',  # Non-breaking space
        }
        for unicode_char, ascii_char in replacements.items():
            text = text.replace(unicode_char, ascii_char)
        
        # Remove any remaining non-latin-1 characters
        return text.encode('latin-1', 'ignore').decode('latin-1')
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "Crypto Research Report", ln=True, align="C")
    
    # Date and Query
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}", ln=True, align="C")
    pdf.cell(0, 8, f"Query: {clean_text(query)}", ln=True, align="C")
    pdf.ln(10)
    
    # Summary with markdown parsing
    if "summary" in data:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "AI Summary", ln=True)
        
        # Parse and render markdown
        summary_text = data["summary"]
        lines = summary_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                pdf.ln(3)
                continue
            
            # Handle bold headers (e.g., **Bullish Signals:**)
            if line.startswith('**') and line.endswith('**'):
                pdf.set_font("Arial", "B", 12)
                clean_line = clean_text(line.replace('**', ''))
                pdf.multi_cell(0, 6, clean_line)
                pdf.set_font("Arial", "", 11)
            # Handle bullet points (• or *)
            elif line.startswith('*') or line.startswith('•'):
                pdf.set_font("Arial", "", 11)
                clean_line = clean_text(line.lstrip('*•').strip())
                pdf.cell(10, 6, '')  # Indent
                pdf.multi_cell(0, 6, f"- {clean_line}")
            # Regular text with inline bold
            else:
                pdf.set_font("Arial", "", 11)
                # Handle inline bold text
                parts = line.split('**')
                
                for i, part in enumerate(parts):
                    if part:
                        if i % 2 == 1:  # Odd indices are bold
                            pdf.set_font("Arial", "B", 11)
                        else:
                            pdf.set_font("Arial", "", 11)
                        
                        part_clean = clean_text(part)
                        pdf.multi_cell(0, 6, part_clean)
        
        pdf.ln(8)
    
    # Results
    results = data.get("sources", data.get("results", []))
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Top {len(results)} Results", ln=True)
    
    for idx, r in enumerate(results, 1):
        pdf.set_font("Arial", "B", 12)
        title = clean_text(r.get('title', 'No title'))
        pdf.multi_cell(0, 6, f"{idx}. {title}")
        
        pdf.set_font("Arial", "", 10)
        content = clean_text(r.get('content', '')[:300])
        pdf.multi_cell(0, 5, content + "...")
        
        pdf.set_font("Arial", "I", 9)
        pdf.cell(0, 5, f"Source: {clean_text(r.get('source', 'Unknown'))} | Sentiment: {r.get('sentiment', 'N/A')} | Score: {round(r.get('score', 0), 4)}", ln=True)
        pdf.ln(5)
    
    # Return PDF as bytes
    return pdf.output(dest='S').encode('latin-1')

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #0a0f1c 0%, #1a1f3a 100%);
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(90deg, #00f6ff, #ff00cc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem !important;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: #00f6ff;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Result Cards */
    .result-card {
        background: linear-gradient(135deg, #1e2746 0%, #2d3561 100%);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        border-left: 4px solid;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateX(8px);
        box-shadow: 0 12px 48px rgba(0, 246, 255, 0.2);
    }
    
    /* Summary Box */
    .summary-container {
        background: linear-gradient(135deg, #0b1020 0%, #1a1f3a 100%);
        border-left: 5px solid #00f6ff;
        border-radius: 16px;
        padding: 28px;
        margin: 24px 0;
        box-shadow: 0 8px 32px rgba(0, 246, 255, 0.15);
        color: #e6e6e6;
        line-height: 1.8;
    }
    
    .summary-container strong {
        color: #00f6ff;
        font-size: 1.1em;
    }
    
    .summary-container ul {
        margin-left: 20px;
        margin-top: 10px;
    }
    
    .summary-container li {
        margin-bottom: 8px;
        color: #d0d0d0;
    }
    
    /* Sentiment Badges */
    .sentiment-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-right: 8px;
    }
    
    /* Stats Box */
    .stats-box {
        background: rgba(0, 246, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        border: 1px solid rgba(0, 246, 255, 0.3);
    }
    
    /* Progress Info */
    .progress-info {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        border-left: 3px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

API_BASE = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="Crypto Researcher",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🧠 Crypto Researcher")
    st.caption("Semantic search over real-time crypto & finance news")

with col2:
    st.markdown(f"**{datetime.now().strftime('%B %d, %Y')}**")
    st.caption("Powered by AI")

st.divider()

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    top_k = st.slider("Number of results", 3, 10, 5)
    use_summary = st.checkbox("Generate AI summary", value=True)
    
    st.divider()
    
    st.subheader("📊 Quick Stats")
    st.metric("Results to Show", top_k)
    st.metric("AI Summary", "Enabled" if use_summary else "Disabled")
    
    st.divider()
    st.caption("💡 Tip: Use specific queries for best results")

# Main content
tab1, tab2 = st.tabs(["🔍 Search", "🔄 Refresh Data"])

with tab2:
    st.subheader("Update News Database")
    st.info("Fetch the latest crypto and finance news from various sources")
    
    if st.button("🔄 Refresh Crypto News", use_container_width=True):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.markdown('<div class="progress-info">📡 Connecting to news sources...</div>', unsafe_allow_html=True)
            progress_bar.progress(20)
            
            status_text.markdown('<div class="progress-info">📰 Fetching latest articles...</div>', unsafe_allow_html=True)
            progress_bar.progress(40)
            
            resp = requests.post(f"{API_BASE}/ingest/news", timeout=180)
            
            status_text.markdown('<div class="progress-info">🔍 Indexing content...</div>', unsafe_allow_html=True)
            progress_bar.progress(70)
            
            status_text.markdown('<div class="progress-info">✅ Finalizing...</div>', unsafe_allow_html=True)
            progress_bar.progress(100)
            
            if resp.status_code == 200:
                st.success("✅ News refreshed and indexed successfully!")
            else:
                st.error(f"❌ Failed to refresh news (Status: {resp.status_code})")
                with st.expander("View Error Details"):
                    st.code(resp.text)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        finally:
            progress_bar.empty()
            status_text.empty()

with tab1:
    st.subheader("Search Crypto News")
    
    # Search query input
    query = st.text_input(
        "Enter your search query",
        placeholder="e.g., Bitcoin ETF inflows, Ethereum price prediction, DeFi trends",
        help="Try to be specific for better results"
    )
    
    # Number of results selector in main area
    col1, col2 = st.columns([3, 1])
    with col1:
        search_top_k = st.slider(
            "Number of results to retrieve",
            min_value=3,
            max_value=20,
            value=top_k,
            help="Select how many results you want to see"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Search", use_container_width=True, type="primary")
    
    if search_btn and query:
        endpoint = "/query/summarize" if use_summary else "/query/search"
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.markdown('<div class="progress-info">🔍 Searching database...</div>', unsafe_allow_html=True)
            progress_bar.progress(30)
            
            if use_summary:
                status_text.markdown('<div class="progress-info">🤖 Generating AI summary...</div>', unsafe_allow_html=True)
            
            progress_bar.progress(60)
            
            response = requests.post(
                f"{API_BASE}{endpoint}",
                json={"query": query, "top_k": search_top_k},
                timeout=180
            )
            
            progress_bar.progress(90)
            status_text.markdown('<div class="progress-info">📊 Formatting results...</div>', unsafe_allow_html=True)
            
            if response.status_code != 200:
                st.error(f"❌ Backend error {response.status_code}")
                with st.expander("View Error Details"):
                    st.code(response.text)
                st.stop()
            
            data = response.json()
            progress_bar.progress(100)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            st.divider()
            
            # Summary section
            if use_summary and "summary" in data:
                st.subheader("🧠 AI-Generated Summary")
                
                # Render markdown properly using st.markdown
                st.markdown(
                    f"""
                    <div class="summary-container">
                    """,
                    unsafe_allow_html=True
                )
                
                # Use st.markdown to render the actual markdown content
                st.markdown(data["summary"])
                
                st.markdown(
                    """
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # PDF Download button
                col1, col2 = st.columns([3, 1])
                with col2:
                    try:
                        pdf_data = generate_pdf_report(query, data)
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=pdf_data,
                            file_name=f"crypto_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"PDF generation failed: {str(e)}")
                
                results = data.get("sources", [])
            else:
                results = data.get("results", [])
            
            # Results section
            if not results:
                st.warning("⚠️ No results found. Try a different query.")
            else:
                st.subheader(f"📰 Top {len(results)} Results")
                
                for idx, r in enumerate(results, 1):
                    sentiment = r.get("sentiment", "neutral")
                    color_map = {
                        "bullish": "#00ff9c",
                        "bearish": "#ff4d4d",
                        "neutral": "#ffaa00"
                    }
                    color = color_map.get(sentiment, "#888")
                    
                    st.markdown(
                        f"""
                        <div class="result-card" style="border-left-color: {color};">
                            <h3 style="margin-top: 0; color: #00f6ff;">
                                #{idx} {r.get('title', 'No title')}
                            </h3>
                            <p style="color: #b0b0b0; line-height: 1.7;">
                                {r.get('content', '')[:400]}...
                            </p>
                            <div style="margin-top: 16px;">
                                <span class="sentiment-badge" style="background: {color}; color: #000;">
                                    {sentiment.upper()}
                                </span>
                                <span style="color: #888; margin-right: 16px;">
                                    📰 {r.get('source', 'Unknown')}
                                </span>
                                <span style="color: #888;">
                                    🎯 Score: {round(r.get('score', 0), 4)}
                                </span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            progress_bar.empty()
            status_text.empty()

st.divider()
st.caption("Built with ❤️ using Streamlit | © 2026 Crypto Researcher")