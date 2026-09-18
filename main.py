import ollama
from ddgs import DDGS

company = input("Enter a company name: ")

# Research topics
queries = {
    "Company Overview": f"{company} company business overview official",
    "Products and Services": f"{company} products services official",
    "Customers and Industries": f"{company} customers industries official",
    "Competitors": f"{company} major competitors",
    "News and Risks": f"{company} latest news business risks"
}

all_research = ""
sources = []

# Web research
with DDGS() as ddgs:

    for topic, query in queries.items():

        print(f"\nResearching: {topic}...")

        results = list(ddgs.text(query, max_results=3))

        all_research += f"\n\n===== {topic} =====\n"

        for i, result in enumerate(results, start=1):

            all_research += f"""
Source {i}
Title: {result['title']}
Information: {result['body']}
URL: {result['href']}
"""

            sources.append(result)

# Ask Llama to analyze everything
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": f"""
You are a business research analyst.

Analyze the following research about {company}.

{all_research}

Create a SHORT business research report with these sections:

1. Company Overview
2. Products and Services
3. Target Customers
4. Industry
5. Major Competitors
   - Mention only 5 competitors.
6. Competitor Comparison
   - Compare {company} with the 5 competitors.
   - Use simple factors such as services, industries served and market positioning.
7. Opportunities
   - Give 3 opportunities.
8. Risks
   - Give 3 risks.
9. Business Screening

Give a score from 1 to 10 for:

- Market Opportunity
- Growth Potential
- Competitive Position
- Business Risk

For each score, give ONE short reason.

10. Key Takeaway
Rules:
- Use ONLY the information provided.
- Do not invent facts.
- Keep the report concise.
- Do not give numerical scores.
- Do not create very long lists.
"""
        }
    ]
)

# Display report
print("\n")
print("=" * 60)
print("AI BUSINESS RESEARCH REPORT")
print("=" * 60)

print(response["message"]["content"])

# Display sources
print("\n")
print("=" * 60)
print("SOURCES USED")
print("=" * 60)

seen_urls = set()
source_number = 1

for source in sources:

    url = source["href"]

    # Remove duplicate sources
    if url not in seen_urls:

        print(f"{source_number}. {source['title']}")
        print(f"   {url}")
        print()

        seen_urls.add(url)
        source_number += 1