from app.agents.skills_agent import extract_skills


test_cv = """
MUSAB BAIG

TECHNICAL SKILLS

Languages: Python, Java, SQL, HTML, CSS, JavaScript
Frameworks: React, Spring Boot
Databases: H2
Tools: Visual Studio 2022, Git, GitHub, Eclipse IDE
Operating Systems: Windows, Linux
APIs: REST APIs, .NET 4.8
Methodologies: Agile, UML, Object-Oriented Programming
Network Protocols: TCP/IP, HTTP, SFTP
"""

skills = extract_skills(test_cv)

print(skills)