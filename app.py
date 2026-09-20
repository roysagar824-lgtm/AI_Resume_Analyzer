
import streamlit as st
import altair as alt
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

st.markdown(
    "<h1 style='text-align: center;'>📄 AI Resume Analyzer</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>"
    "Analyze your resume and match it with a job description."
    "</p>",
    unsafe_allow_html=True
)
# Resume Upload
resume = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "docx"]
)

# Job Description
job_description = st.text_area(
    "📋 Paste Job Description",
    height=200
)

if resume is not None:

    text = ""

    # Read PDF
    if resume.name.lower().endswith(".pdf"):
        reader = PdfReader(resume)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    # Read DOCX
    elif resume.name.lower().endswith(".docx"):
        document = Document(resume)

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

    st.success("Resume uploaded successfully! ✅")

    # Resume Text
    st.subheader("📄 Resume Text")

    st.text_area(
        "Extracted Text",
        text,
        height=250
    )

    st.subheader("ATS Checks")

    section_checks = {
        "Summary": any(
            keyword in text.lower()
            for keyword in [
                "summary",
                "professional summary",
                "profile",
                "about me"
            ]
        ),
        "Education": any(
            keyword in text.lower()
            for keyword in [
                "education",
                "educational qualification",
                "academics",
                "degree",
                "b.tech",
                "btech"
            ]
        ),
        "Skills": any(
            keyword in text.lower()
            for keyword in [
                "skills",
                "technical skills",
                "core competencies"
            ]
        ),
        "Projects": any(
            keyword in text.lower()
            for keyword in [
                "projects",
                "project"
            ]
        ),
        "Experience": any(
            keyword in text.lower()
            for keyword in [
                "experience",
                "work experience",
                "professional experience",
                "internship"
            ]
        ),
        "Certifications": any(
            keyword in text.lower()
            for keyword in [
                "certifications",
                "certification",
                "certified"
            ]
        )
    }

    for section_name, found in section_checks.items():
        if found:
            st.write("✅", section_name)
        else:
            st.write("❌", section_name)

    # Skills List
    skills = [
        "Python",
        "Java",
        "C++",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "Machine Learning",
        "Artificial Intelligence",
        "Data Science",
        "Excel",
        "Git",
        "GitHub",
        "Django",
        "Flask",
        "React",
        "Power BI",
        "TensorFlow"
    ]

    # Resume Skills
    resume_skills = []

    for skill in skills:
        if skill.lower() in text.lower():
            resume_skills.append(skill)

    st.subheader("🛠️ Skills Found in Resume")

    if resume_skills:
        for skill in resume_skills:
            st.write("✅", skill)
    else:
        st.write("No matching skills found.")

    # Resume Score
    # Professional Resume Score

    skills_score = min(len(resume_skills) * 3, 30)

    experience_score = 20 if any(
        word in text.lower()
        for word in ["experience", "internship", "work experience"]
    ) else 0

    education_score = 20 if any(
        word in text.lower()
        for word in ["education", "bachelor", "degree", "b.tech", "btech"]
    ) else 0

    projects_score = 20 if any(
        word in text.lower()
        for word in ["projects", "project"]
    ) else 0

    contact_score = 10 if any(
        word in text.lower()
        for word in ["email", "phone", "linkedin"]
    ) else 0

    score = (
        skills_score
        + experience_score
        + education_score
        + projects_score
        + contact_score
    )

    st.subheader("📊 Professional Resume Score")
    st.progress(score)

    st.metric("Resume Score", f"{score}/100")

    st.write("🛠️ Skills:", skills_score, "/30")
    st.write("💼 Experience:", experience_score, "/20")
    st.write("🎓 Education:", education_score, "/20")
    st.write("🚀 Projects:", projects_score, "/20")
    st.write("📞 Contact Details:", contact_score, "/10")
    # Job Matching
    if job_description:

        job_skills = []

        for skill in skills:
            if skill.lower() in job_description.lower():
                job_skills.append(skill)

        matching_skills = []

        for skill in job_skills:
            if skill in resume_skills:
                matching_skills.append(skill)

        missing_skills = []

        for skill in job_skills:
            if skill not in resume_skills:
                missing_skills.append(skill)

        # Match percentage
        if len(job_skills) > 0:
            match_percentage = int(
                len(matching_skills) / len(job_skills) * 100
            )
        else:
            match_percentage = 0

        st.subheader("🎯 Job Match")

        st.progress(match_percentage)

        st.metric("Job Match %", f"{match_percentage}%")

        # Matching Skills
        st.subheader("✅ Matching Skills")

        if matching_skills:
            for skill in matching_skills:
                st.write("✅", skill)
        else:
            st.write("No matching skills found.")

        # Missing Skills
        st.subheader("❌ Missing Skills")

        if missing_skills:
            for skill in missing_skills:
                st.write("❌", skill)
        else:
            st.write("No major missing skills found.")

        st.subheader("📈 Skills Count")
        skills_count_df = pd.DataFrame(
            {
                "Category": ["Matching Skills", "Missing Skills"],
                "Count": [len(matching_skills), len(missing_skills)]
            }
        )

        skills_count_chart = (
            alt.Chart(skills_count_df)
            .mark_bar()
            .encode(
                x=alt.X("Category:N", title="Skills"),
                y=alt.Y("Count:Q", title="Count"),
                color=alt.condition(
                    alt.datum.Category == "Matching Skills",
                    alt.value("#2ecc71"),
                    alt.value("#e74c3c")
                )
            )
            .properties(height=250)
        )
        st.altair_chart(skills_count_chart, width='stretch')

        # Suggestions
        st.subheader("💡 Suggestions")

        if missing_skills:
            st.write(
                "Consider learning or highlighting these "
                "job-related skills:"
            )

            for skill in missing_skills:
                st.write("•", skill)

        else:
            st.write(
                "Your resume contains the skills detected "
                "in the job description."
            )

        st.subheader("🤖 Resume Analysis")

        analysis = []

        if resume_skills:
            analysis.append(
                f"Your resume contains {len(resume_skills)} relevant skills."
            )
        else:
            analysis.append(
                "Your resume should include more technical skills."
            )

        if score >= 70:
            analysis.append("Your resume has a good range of detected skills.")
        elif score >= 40:
            analysis.append("Your resume has some relevant skills, but more can be added.")
        else:
            analysis.append("Try adding more relevant technical skills.")

        if job_description:
            if matching_skills:
                analysis.append(
                    "Your resume matches some of the skills mentioned in the job description."
                )

            if missing_skills:
                analysis.append(
                    "Consider learning or highlighting the missing job-related skills."
                )

        for point in analysis:
            st.write("🔹", point)

        report = f"""Resume Score: {score}/100
Job Match %: {match_percentage}%

Matching Skills:
{', '.join(matching_skills) if matching_skills else 'None'}

Missing Skills:
{', '.join(missing_skills) if missing_skills else 'None'}

ATS Checks:
"""

        report += "\n".join(
            f"{section_name}: {'Passed' if found else 'Failed'}"
            for section_name, found in section_checks.items()
        )

        st.download_button(
            "Download TXT Report",
            report,
            file_name="resume_analysis_report.txt",
            mime="text/plain"
        )
