from app.agents.education_agent import extract_education


test_cv = """
MUSAB BAIG

EDUCATION

Herschel Grammar School:
11 GCSEs.

Slough and Eton Sixth Form:
A-Levels in Mathematics, Biology and Chemistry.

Brunel University, Uxbridge
BSc (Hons) Computer Science – Sep 2024 – Present.
Expected Classification: 2:1 or above.
"""

education = extract_education(test_cv)

print(education)