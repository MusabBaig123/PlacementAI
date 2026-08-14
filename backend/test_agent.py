from app.agents.cv_agent import analyse_cv


test_cv = """
Musab Baig

BSc Computer Science student.

Skills:
Java
Python
React
Spring Boot

Projects:
BioTrace Sustainability Platform
PlacementAI
"""


result = analyse_cv(test_cv)

print(result)