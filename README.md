# SmartHire Engine 🤖

**SmartHire Engine** is a Generative AI-based job recommendation and resume analysis system that helps job seekers understand how well their resume matches a target job description and discover relevant job opportunities.

The system combines **LLM-based information extraction, ATS-style resume matching, skill-gap analysis, and AI-powered job recommendations** into a single platform.

---

## 🚀 Key Features

### 📄 Resume & Job Description Analysis

* Upload resumes and job descriptions in PDF/image format.
* Extract relevant information such as:

  * Skills
  * Education
  * Experience
  * Domain
* Uses OCR and document parsing for extracting text from uploaded files.

### 📊 ATS-Based Resume Matching

SmartHire calculates an overall ATS-style score based on three major factors:

| Component  | Weightage |
| ---------- | --------: |
| Skills     |       50% |
| Experience |       30% |
| Education  |       20% |

The system compares the candidate's resume with the target job description and generates a matching score.

### 🔍 Skill Gap Analysis

The system identifies missing or insufficient skills by comparing the candidate's resume with the requirements of the selected job description.

This helps users understand what skills they may need to improve for a particular role.

### 📝 Resume Summary

SmartHire generates a concise summary of the candidate's profile based on the information extracted from their resume.

### 🎥 Learning Recommendations

Based on identified skill gaps and the user's domain, the system provides relevant YouTube learning resources to help candidates improve their skills.

### 💼 AI-Powered Job Recommendations

The system recommends relevant job opportunities based on:

* Candidate's skills
* Experience
* Domain
* Resume information

Job listings are retrieved using **JSearch API through RapidAPI**, while the recommendation process uses the extracted candidate information.

---

## 🏗️ System Workflow

```text
User Signup
     ↓
Select Pricing Plan
     ↓
Login
     ↓
Upload Resume + Job Description
     ↓
OCR / PDF Text Extraction
     ↓
LLM-Based Information Extraction
     ↓
Resume & JD → Structured JSON
     ↓
ATS Matching
     ↓
Skill Gap Analysis
     ↓
Resume Summary
     ↓
Learning Recommendations
     ↓
AI-Based Job Recommendations
```

---

## 🧠 Generative AI Components

SmartHire Engine uses Generative AI for structured extraction and intelligent processing of resume and job-description data.

The LLM processes extracted text and identifies important attributes such as:

```json
{
  "skills": [],
  "education": [],
  "experience": [],
  "domain": ""
}
```

This structured information is then used by the matching and recommendation modules.

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* SQLite

### Frontend

* HTML
* CSS
* JavaScript
* Jinja Templates

### AI / NLP

* OpenAI LLM
* Generative AI
* Prompt-based information extraction

### Document Processing

* Tesseract OCR
* PyResParser
* PDF text extraction

### APIs

* JSearch API
* RapidAPI
* YouTube search resources

### Payments

* Razorpay

---

## 💰 Pricing Plans

The application includes different subscription plans:

| Plan     | Price |
| -------- | ----: |
| Basic    |  ₹399 |
| Standard |  ₹599 |
| Premium  |  ₹899 |

Different features are unlocked depending on the selected plan.

---

## 📈 Experimental Evaluation

The system was evaluated using a dataset of **10 resumes** to examine the quality of resume matching and recommendations.

The evaluation showed that approximately **70% of the generated results were considered correct or satisfactory** during testing.

The testing also highlighted some limitations, including differences between SmartHire scores and scores from other systems, as well as job recommendations that sometimes favored international opportunities instead of local jobs.

These observations are considered areas for future improvement.

---

## 📁 Project Structure

```text
SmartHire-Engine/
│
├── app/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   └── services/
│
├── uploads/
│
├── database/
│
├── main.py
├── requirements.txt
├── README.md
└── .env
```

> The exact folder structure may vary depending on the current project version.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd SmartHire-Engine
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
RAPIDAPI_KEY=your_rapidapi_key
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

Do not upload your API keys or other credentials to GitHub.

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

---

## 🔐 Security

* API keys are stored using environment variables.
* Sensitive credentials should not be committed to the repository.
* User-uploaded resumes should be handled securely.
* Authentication and payment-related information should be protected appropriately.

---

## 🔮 Future Improvements

Possible improvements include:

* Better localization of job recommendations
* More accurate semantic resume-to-JD matching
* Improved job ranking and filtering
* Support for additional job APIs
* Better handling of different resume formats
* More advanced skill extraction
* Personalized learning paths
* Improved recommendation evaluation using larger datasets
* Deployment on a cloud platform

---

## 🎯 Objective

The main objective of SmartHire Engine is to simplify the job-search process by combining **resume analysis, ATS-style matching, skill-gap identification, learning resources, and AI-powered job recommendations** in one platform.

Instead of only showing whether a resume matches a job description, SmartHire aims to provide actionable information about **what the candidate is missing and which opportunities may be relevant to them**.

---

## 👩‍💻 Authors

**Sayli Thukral**
Department of Computer Engineering and Technology
Guru Nanak Dev University, Amritsar

**Shivani Thapar**
Department of Computer Engineering and Technology
Guru Nanak Dev University, Amritsar

---

## 📜 License

This project is developed for academic/research purposes.
