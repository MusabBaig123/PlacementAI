from app.agents.name_agent import extract_name


test_cv = """
MUSAB BAIG

Second-year Computer Science student at Brunel University London.

Skills:
Java
Python
React
"""

name = extract_name(test_cv)

print(name)