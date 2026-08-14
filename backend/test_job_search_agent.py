from app.agents.job_search_agent import build_search_query

query = build_search_query()

print("\n========== JOB SEARCH QUERY ==========\n")

for key, value in query.items():
    print(f"{key}: {value}")