from app.agents.role_agent import suggest_roles


test_cv = """
MUSAB BAIG

Second-year BSc Computer Science student seeking a 12-month
industrial placement.

Skills:
Python, Java, SQL, React, Spring Boot, Git, REST APIs, H2

Projects:
BioTrace Sustainability Platform
Tunnel Vision SwiftBot Project
Card Game Pontoon
Python Calculator

Experience:
Worked in Agile development teams.
Acted as project leader during the BioTrace project.
"""

roles = suggest_roles(test_cv)

print(roles)