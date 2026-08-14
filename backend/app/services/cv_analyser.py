from app.agents.cv_agent import analyse_cv


def analyse_uploaded_cv(cv_text):
    analysis_result = analyse_cv(cv_text)
    return analysis_result