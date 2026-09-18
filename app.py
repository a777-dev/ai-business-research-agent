import os
import streamlit as st
from google import genai
from ddgs import DDGS

st.set_page_config(
    page_title="AI Business Research Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Business Research & Screening Agent")
st.write("Research a company using web search + local AI.")

company = st.text_input(
    "Enter a company name",
    placeholder="e.g., TCS"
)

if st.button("🔍 Research Company"):

    if not company:
        st.warning("Please enter a company name.")
        st.stop()

    queries = {
        "Company Overview": f"{company} company business overview official",
        "Products and Services": f"{company} products services official",
        "Customers and Industries": f"{company} customers industries official",
        "Competitors": f"{company} major competitors",
        "News and Risks": f"{company} latest news business risks"
    }

    all_research = ""
    sources = []

    with st.spinner("Researching the company..."):

        with DDGS() as ddgs:

            for topic, query in queries.items():

                results = list(
                    ddgs.text(query, max_results=3)
                )

                all_research += f"\n\n===== {topic} =====\n"

                for result in results:

                    all_research += f"""
Title: {result['title']}
Information: {result['body']}
URL: {result['href']}
"""

                    sources.append(result)

    with st.spinner("AI is analyzing the research..."):

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": f"""
You are a business research analyst.

Analyze the following research about {company}.

{all_research}

Create a SHORT business research report with:

1. Company Overview
2. Products and Services
3. Target Customers
4. Industry
5. Major Competitors
   - Mention only 5.
6. Competitor Comparison
7. Opportunities
   - 3 opportunities.
8. Risks
   - 3 risks.
9. Business Screening

Score from 1 to 10:
- Market Opportunity
- Growth Potential
- Competitive Position
- Business Risk

Give one short reason for each score.

10. Key Takeaway

Rules:
- Use ONLY the research provided.
- Do not invent facts.
- Keep the report concise.
"""
                }
            ]
        )

    st.success("Research completed!")

    st.markdown("## 📋 Business Research Report")

    st.write(response["message"]["content"])

    st.markdown("## 🔗 Sources Used")

    seen_urls = set()

    for source in sources:

        url = source["href"]

        if url not in seen_urls:

            st.markdown(
                f"- [{source['title']}]({url})"
            )

        seen_urls.add(url)