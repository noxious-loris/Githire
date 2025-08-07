import google.generativeai as genai

genai.configure(api_key="AIzaSyD73vy59xoZUvhkNBf1inHEif8N_CK-Ma8")

def write_cold_email(recruiter_name, company, job_title, resume_filename):
    prompt = f"""
    Write a concise, personalized cold email to {recruiter_name} at {company}
    about the {job_title} role.
    - Mention attached resume named {resume_filename}
    - Professional, polite, 3 short paragraphs
    - Call to action for interview
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    email = model.generate_content(prompt)
    return email.text
