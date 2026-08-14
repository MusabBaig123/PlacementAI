from app.services.cv_processing_service import extract_text
from app.services.cv_section_service import extract_cv_sections


cv_text = extract_text("uploads/Musab_Baig_CV.docx")
sections = extract_cv_sections(cv_text)

for section_name, section_text in sections.items():
    print(f"\n========== {section_name.upper()} ==========")
    print(section_text)