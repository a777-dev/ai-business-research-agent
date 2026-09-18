import os
import streamlit as st
from google import genai
from ddgs import DDGS

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Business Research Agent",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📊 AI Business Research & Screening Agent")

st.write(
    "Research a company using web search and AI."
)

# --------------------------------------------------
# COMPANY INPUT
# --------------------------------------------------

company = st.text_input(
    "Enter a company name",
    placeholder="e.g., TCS"
)

# --------------------------------------------------
# RESEARCH BUTTON
# --------------------------------------------------

if st.button("🔍 Research Company"):

    if not company:
        st.warning("Please enter a company name.")
        st.stop()

    # --------------------------------------------------
    # SEARCH QUERIES
    # --------------------------------------------------

    queries = {
        "Company Overview": f"{company} company business overview official",
        "Products and Services": f"{company} products services official",
        "Customers and Industries": f"{company} customers industries official",
        "Competitors": f"{company} major competitors",
        "News and Risks": f"{company} latest news business risks"
    }

    all_research = ""
    sources = []

    # --------------------------------------------------
    # WEB RESEARCH
    # --------------------------------------------------

    with st.spinner("Researching the company..."):

        with DDGS() as ddgs:

            for topic, query in queries.items():

                all_research += f"\n\n===== {topic} =====\n"

                try:

                    results = list(
                        ddgs.text(
                            query,
                            max_results=3
                        )
                    )

                except Exception as e:

                    results = []

                # ------------------------------------------
                # ADD SEARCH RESULTS
                # ------------------------------------------

                for result in results:

                    title = result.get("title", "")
                    body = result.get("body", "")
                    url = result.get("href", "")

                    all_research += f"""
Title: {title}
Information: {body}
URL: {url}
"""

                    sources.append(result)

    # --------------------------------------------------
    # CHECK IF SEARCH FOUND ANYTHING
    # --------------------------------------------------

    if not all_research.strip():

        st.error(
            "Web search could not retrieve results right now. "
            "Please try again in a few minutes."
        )

        st.stop()

    # --------------------------------------------------
    # GEMINI AI ANALYSIS
    # --------------------------------------------------

    with st.spinner("AI is analyzing the research..."):

        try:

            api_key = os.environ.get("GEMINI_API_KEY")

            if not api_key:

                st.error(
                    "Gemini API key is not configured."
                )

                st.stop()

            client = genai.Client(
                api_key=api_key
            )

            response = client.models.generate_content(

                model="gemini-2.5-flash",

                contents=f"""
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
   - Give 3 opportunities.

8. Risks
   - Give 3 risks.

9. Business Screening

Score the company from 1 to 10 on:

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
- Clearly separate facts from analysis.
- Use simple business language.
"""
            )

        except Exception as e:

            st.error(
                "The AI analysis could not be completed right now."
            )

            st.stop()

    # --------------------------------------------------
    # DISPLAY REPORT
    # --------------------------------------------------

    st.success("Research completed!")

    st.markdown(
        "## 📋 Business Research Report"
    )

    st.write(
        response.text
    )

    # --------------------------------------------------
    # DISPLAY SOURCES
    # --------------------------------------------------

    st.markdown(
        "## 🔗 Sources Used"
    )

    seen_urls = set()

    for source in sources:

        url = source.get("href", "")
        title = source.get("title", "Source")

        if url and url not in seen_urls:

            st.markdown(
                f"- [{title}]({url})"
            )

            seen_urls.add(url)
