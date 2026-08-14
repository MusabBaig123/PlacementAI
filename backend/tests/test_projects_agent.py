from app.agents.projects_agent import extract_projects


test_cv = """
MUSAB BAIG

PROJECTS

BioTrace Sustainability Platform
Developed frontend and backend features using React and Spring Boot.

Tunnel Vision
Built a Java program using the SwiftBot camera to measure tunnel distances.

Card Game Pontoon
Implemented a terminal-based Java card game.

Python Calculator Project
Developed a calculator using Python.
"""

projects = extract_projects(test_cv)

print(projects)