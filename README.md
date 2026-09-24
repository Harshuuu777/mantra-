# MANTRA
## Smart College Admission Assistant

MANTRA is a voice-enabled college admission assistant designed to help students with admission-related information in a simple and friendly way.

---

## 🎯 Project Objective

The main objective of MANTRA is to provide students with quick and easy access to college admission information through natural conversation.

MANTRA can understand student queries, identify the required topic, maintain conversation context, and provide relevant admission information.

---

## ✨ Key Features

### 🎤 Voice Interaction
MANTRA can listen to the student's voice and convert speech into text.

### 🔊 Text-to-Speech
MANTRA can speak its responses using the system's text-to-speech engine.

### 💤 Wake Word
MANTRA can remain on standby and activate when the user says:

> "Mantra"

### 🧠 Smart Intent Detection
MANTRA identifies different types of student queries, including:

- Greeting
- Course information
- Fees
- Documents
- Eligibility
- Admission process
- Scholarship
- Admission queries
- Thank you
- Goodbye

### 🎓 Course Information
MANTRA can provide information about available courses such as:

- BCA
- B.Tech
- Computer Engineering
- Mechanical Engineering
- Civil Engineering
- Electrical Engineering
- Information Technology
- ENTC
- AI
- Data Science
- AI & ML
- Cyber Security

### 📚 Document Information
MANTRA can provide required admission documents.

### ✅ Eligibility Information
MANTRA provides course-specific eligibility information stored in its database.

### 📋 Admission Process
MANTRA can explain the admission process step-by-step.

### 👤 Student Profile
MANTRA can recognize the student's name and maintain basic conversation information such as:

- Student name
- Selected course
- Last intent
- Current topic
- Conversation turn

### 🧩 Conversation Context
MANTRA understands follow-up questions such as:

- "Aur fees?"
- "Aur documents?"
- "Aur eligibility?"
- "Aur process?"

without requiring the student to repeat the course name.

### 🗄️ Database
MANTRA uses SQLite to store and retrieve college admission information.

---

## 🛠️ Technologies Used

- Python
- SQLite
- Speech Recognition
- pyttsx3
- JSON
- Regular Expressions
- Python Modules

---

## 📁 Project Structure

```text
Mantra/
│
├── brain/
│   └── response_engine.py
│
├── database/
│   ├── db.py
│   ├── manager.py
│   └── seed.py
│
├── data/
│   └── college_data.json
│
├── voice/
│   ├── speech.py
│   ├── wake_word.py
│   └── voice_assistant.py
│
├── tests/
│
├── chat.py
├── config.py
├── prompt.py
├── main.py
└── README.md