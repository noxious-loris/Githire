import google.generativeai as genai
import requests

genai.configure(api_key="GEmmeni_api_key")

def fetch_github_projects(username, max_projects=5):
    response = requests.get(f"https://api.github.com/users/{username}/repos")
    repos = response.json()
    return [{"name": r["name"], "description": r.get("description", "")} for r in repos[:max_projects]]

def build_resume(user_data, job_desc, github_username):
    projects = fetch_github_projects(github_username)
    project_summary = "\n".join([f"{p['name']}: {p['description']}" for p in projects])

    prompt = f"""
    Create a LaTeX resume with:
    Name: {user_data['name']}
    Contact: {user_data['contact']}
    Education: {user_data['education']}
    Skills: {', '.join(user_data['skills'])}
    Achievements: {', '.join(user_data['achievements'])}
    Projects:
    {project_summary}
    Job Description:
    {job_desc}
    Output pure LaTeX, ATS score 90+.
    """
    model = genai.GenerativeModel("gemini-2.5-pro")
    resume = model.generate_content(prompt)
    return resume.text
