import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests
from utils.resume_builder_agent import build_resume
from utils.email_writer_agent import write_cold_email
from utils.latex_to_pdf import convert_to_pdf

def load_lottieurl(url: str, fallback_path: str = None):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"Error loading Lottie URL: {e}")
    
    # Fallback to a simple animation
    if fallback_path:
        try:
            with open(fallback_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading fallback Lottie: {e}")
    
    # If all else fails, return a simple animation as dict
    return {
        "v": "5.5.2",
        "fr": 30,
        "ip": 0,
        "op": 90,
        "w": 500,
        "h": 500,
        "nm": "Fallback Animation",
        "layers": [
            {
                "ddd": 0,
                "ind": 1,
                "ty": 4,
                "nm": "Layer 1",
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100},
                    "r": {"a": 1, "k": [{"i": {"x": [0.833], "y": [0.833]}, "o": {"x": [0.167], "y": [0.167]}, "t": 0, "s": [0]}, {"t": 90, "s": [360]}]},
                    "p": {"a": 0, "k": [250, 250, 0]},
                    "a": {"a": 0, "k": [0, 0, 0]},
                    "s": {"a": 0, "k": [100, 100, 100]}
                },
                "shapes": [
                    {
                        "ty": "el",
                        "p": {"a": 0, "k": [0, 0], "ix": 3},
                        "s": {"a": 0, "k": [100, 100], "ix": 5},
                        "nm": "Ellipse",
                        "mn": "ADBE Vector Shape - Ellipse",
                        "hd": False
                    },
                    {
                        "ty": "st",
                        "c": {"a": 0, "k": [0.1, 0.1, 0.1, 1], "ix": 3},
                        "o": {"a": 0, "k": 100, "ix": 4},
                        "w": {"a": 0, "k": 5, "ix": 5},
                        "lc": 1,
                        "lj": 1,
                        "ml": 4,
                        "bm": 0,
                        "nm": "Stroke 1",
                        "mn": "ADBE Vector Graphic - Stroke",
                        "hd": False
                    },
                    {
                        "ty": "tr",
                        "p": {"a": 0, "k": [0, 0], "ix": 2},
                        "a": {"a": 0, "k": [0, 0], "ix": 1},
                        "s": {"a": 0, "k": [100, 100], "ix": 3},
                        "r": {"a": 0, "k": 0, "ix": 6},
                        "o": {"a": 0, "k": 100, "ix": 7},
                        "sk": {"a": 0, "k": 0, "ix": 4},
                        "sa": {"a": 0, "k": 0, "ix": 5}
                    }
                ]
            }
        ],
        "markers": []
    }

# Page config
st.set_page_config(
    page_title="GitHire - AI Resume & Cover Letter Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
        /* Modern font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Hero section */
        .hero {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            padding: 6rem 2rem;
            border-radius: 0 0 1.5rem 1.5rem;
            color: white;
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .hero h1 {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
        }
        
        .hero p {
            font-size: 1.25rem;
            max-width: 700px;
            margin: 0 auto 2rem auto;
            opacity: 0.9;
        }
        
        /* Card styling */
        .card {
            background: white;
            border-radius: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            padding: 2rem;
            margin-bottom: 2rem;
        }
        
        /* Step indicator */
        .steps {
            display: flex;
            justify-content: space-between;
            margin: 3rem 0;
            position: relative;
        }
        
        .step {
            text-align: center;
            position: relative;
            z-index: 1;
            flex: 1;
        }
        
        .step-number {
            width: 40px;
            height: 40px;
            background: #e0e7ff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 0.5rem;
            font-weight: 700;
            color: #4f46e5;
        }
        
        .step.active .step-number {
            background: #4f46e5;
            color: white;
        }
        
        .step-line {
            position: absolute;
            top: 20px;
            left: 0;
            right: 0;
            height: 2px;
            background: #e0e7ff;
            z-index: 0;
        }
        
        /* Form elements */
        .stTextInput>div>div>input, 
        .stTextArea>div>textarea {
            border-radius: 0.5rem;
            border: 1px solid #e5e7eb;
            padding: 0.75rem 1rem;
        }
        
        /* Buttons */
        .stButton>button {
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            background: #4f46e5;
            color: white;
            border: none;
            width: 100%;
            transition: all 0.2s;
        }
        
        .stButton>button:hover {
            background: #4338ca;
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2.5rem;
            }
            
            .hero p {
                font-size: 1.1rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero">
        <h1>GitHire</h1>
        <p>Create ATS-optimized resumes and personalized cover letters in minutes. Showcase your GitHub projects and land your dream tech job.</p>
    </div>
""", unsafe_allow_html=True)

# Main container with max width for better readability
main_container = st.container()

# Steps indicator
st.markdown("""
    <div class="steps">
        <div class="step active" id="step1">
            <div class="step-number">1</div>
            <div>Enter Details</div>
        </div>
        <div class="step" id="step2">
            <div class="step-number">2</div>
            <div>Generate Resume</div>
        </div>
        <div class="step" id="step3">
            <div class="step-number">3</div>
            <div>Download & Send</div>
        </div>
        <div class="step-line"></div>
    </div>
""", unsafe_allow_html=True)

# Main content
with main_container:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        with st.form("resume_email_form"):
            st.markdown("### 🎯 Your Information")
            name = st.text_input("Full Name *", placeholder="John Doe")
            contact = st.text_input("Contact Info *", placeholder="email@example.com | (123) 456-7890")
            education = st.text_area("Education *", placeholder="Bachelor's in Computer Science, XYZ University, 2020-2024")
            skills = st.text_area("Skills (comma separated) *", placeholder="Python, Machine Learning, Data Analysis, Team Leadership")
            achievements = st.text_area("Achievements (comma separated)", placeholder="Led team of 5 developers, Increased sales by 30%, Published research paper on AI")
            github_username = st.text_input("GitHub Username (optional)", placeholder="johndoe")
            
            st.markdown("### 💼 Job Details")
            recruiter_name = st.text_input("Recruiter's Name (optional)", placeholder="Sarah Johnson")
            company_name = st.text_input("Company Name *", placeholder="Tech Innovations Inc.")
            job_title = st.text_input("Job Title *", placeholder="Senior Software Engineer")
            job_description = st.file_uploader("Upload Job Description (optional, .txt)", type=["txt"])
            
            submitted = st.form_submit_button("✨ Generate Resume & Email")
    
    with col2:
        st.markdown("### 📝 Preview")
        if not submitted:
            # Show preview placeholder with fallback
            lottie_animation = load_lottieurl(
                "https://assets5.lottiefiles.com/packages/lf20_3a8joebv.json",
                fallback_path="animation.json"
            )
            st_lottie(lottie_animation, height=300, key="preview")
            st.markdown("""
                <div style="text-align: center; color: #6b7280; margin-top: 1rem;">
                    <p>Your generated resume and email will appear here</p>
                </div>
            """, unsafe_allow_html=True)

if submitted:
    with st.spinner('Generating your ATS-optimized resume and cold email...'):
        jd_text = ""
        if job_description:
            jd_text = job_description.read().decode("utf-8")

        user_data = {
            "name": name,
            "contact": contact,
            "education": education,
            "skills": [s.strip() for s in skills.split(",") if s.strip()],
            "achievements": [a.strip() for a in achievements.split(",") if a.strip()]
        }

        with col2:
            # Generate Resume
            st.markdown("### 📄 Your Resume")
            latex_resume = build_resume(user_data, jd_text, github_username)
            
            # Show loading spinner while generating PDF
            with st.spinner('Generating PDF...'):
                pdf_file, error = convert_to_pdf(latex_resume)
                
                if error:
                    st.error("❌ Failed to generate PDF. Please check the LaTeX content and try again.")
                    st.code(latex_resume, language="latex")
                    st.error(f"Error details:\n{error}")
                    st.stop()  # Stop further execution of the script
                else:
                    # Generate Cold Email
                    email_text = write_cold_email(recruiter_name, company_name, job_title, "resume.pdf")
                    
                    # Show success message
                    st.success("✅ Resume generated successfully!")
                    
                    # Download buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "📥 Download Resume", 
                            open(pdf_file, "rb"), 
                            file_name="resume.pdf",
                            use_container_width=True,
                            type="primary"
                        )
                    with col2:
                        st.download_button(
                            "📧 Download Email", 
                            email_text, 
                            file_name="cold_email.txt",
                            use_container_width=True
                        )
            
            # Show email preview
            st.markdown("### ✉️ Cold Email Preview")
            st.text_area("Email Content", email_text, height=200, label_visibility="collapsed")
            
            # Show success message
            st.success("✅ Success! Your resume and email are ready to download.")
            
            # Update step indicators
            st.markdown(
                """
                <script>
                    document.getElementById('step1').classList.add('active');
                    document.getElementById('step2').classList.add('active');
                    document.getElementById('step3').classList.add('active');
                </script>
                """, 
                unsafe_allow_html=True
            )
