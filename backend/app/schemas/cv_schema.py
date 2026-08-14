from pydantic import BaseModel
from typing import List


class Project(BaseModel):
    title: str
    description: str
    development_tools: List[str]
    technologies: List[str]


class Experience(BaseModel):
    title: str
    company: str
    description: str
    development_tools: List[str]
    technologies: List[str]


class CVAnalysis(BaseModel):
    name: str
    education: str
    skills: List[str]
    projects: List[Project]
    experience: List[Experience]
    suitable_roles: List[str]