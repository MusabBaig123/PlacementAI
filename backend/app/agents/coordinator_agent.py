from app.agents.education_agent import extract_education
from app.agents.experience_agent import extract_experience
from app.agents.name_agent import extract_name
from app.agents.projects_agent import extract_projects
from app.agents.role_agent import suggest_roles
from app.agents.skills_agent import extract_skills
from app.services.cv_section_service import extract_cv_sections


def process_cv(cv_text: str) -> dict:
    """
    Coordinates the complete CV analysis workflow.

    It first separates the CV into sections and then delegates
    each section to the relevant specialist agent.
    """

    sections = extract_cv_sections(cv_text)

    name = extract_name(cv_text)

    skills = extract_skills(
        sections["technical_skills"]
    )

    education = extract_education(
        sections["education"]
    )

    projects = extract_projects(cv_text)

    experience = extract_experience(cv_text)

    candidate_summary = f"""
Name:
{name}

Education:
{education}

Technical skills:
{", ".join(skills)}

Projects:
{", ".join(projects)}

Experience:
{experience}
"""

    suitable_roles = suggest_roles(candidate_summary)

    return {
        "name": name,
        "education": education,
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "suitable_roles": suitable_roles,
    }