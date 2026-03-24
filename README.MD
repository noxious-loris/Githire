# Githire 🚀

Githire is a modern platform that makes a custom resume based on a provided job description 


## 🌟 Features

- 🔍 **GitHub Profile Search:** Find developers by GitHub handle.
- 📊 **Intelligent Scoring:** Analyze contributions, languages, stars, and more.
- 🧠 **AI Summaries:** Auto-generate professional summaries based on GitHub activity.
- 💼 **Talent Dashboard:** A clean interface for recruiters to shortlist candidates.
- ⚡ **Streamlit UI:** Fast, responsive, and deployed as a web app.

## 📦 Tech Stack

- 🐍 Python
- 🔮 Streamlit
- 💡 Gemeni  (for profile summaries)
- 💻 GitHub API

## 🚀 Getting Started

### 1. Clone the Repo

```bash
    git clone https://github.com/your-username/githire.git
    cd githire

2. Create a Virtual Environment
    python -m venv env
    source env/bin/activate  # or .\env\Scripts\activate on Windows

3. Install Dependencies
    pip install -r requirements.txt

4. Add API Keys
    Create a .env file and add your keys:
        OPENAI_API_KEY=your_openai_key
        GITHUB_API_TOKEN=your_github_token
5. Run the App
    streamlit run app.py

🧠 How It Works

    User enters a GitHub username.

    Backend fetches GitHub data using the GitHub REST API.

    AI (OpenAI GPT) generates summaries and scores.

    Streamlit renders the results beautifully.

    Optional: Export or share profiles for hiring use cases.

📸 Screenshots
    

Coming soon...
🛠️ Roadmap

Add login for recruiters

API access for companies

Candidate comparison view

Email notifications

    Integration with LinkedIn

🤝 Contributing

Pull requests are welcome! 

MIT License 
