from ddgs import DDGS

query = "TCS latest company news"

with DDGS() as ddgs:
    results = list(ddgs.text(query, max_results=5))

for result in results:
    print(result["title"])
    print(result["body"])
    print(result["href"])
    print("-" * 50)