from app.agents.experience_agent import extract_experience


test_cv = """
MUSAB BAIG

EXPERIENCE

Worked within Agile-style development teams using GitHub,
participating in sprint planning, iterative development, project
reviews, and continuous improvement activities.

During the BioTrace project, I took on the role of project leader
for a group of 10 students, coordinating frontend and backend
responsibilities, setting deadlines, monitoring progress, and
collaborating with fellow project leaders to ensure successful
delivery of project objectives.
"""

experience = extract_experience(test_cv)

print(experience)