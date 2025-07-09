# 🎓 College Events Management System

A **simple, beginner-friendly project** to manage college events and student registrations, built with:

- ⚙️ **FastAPI** (Python backend)
- 🗄️ **MySQL** database (with SQLAlchemy)
- 💻 **HTML + CSS + JavaScript** frontend

---

## 📌 Features

✅ **Students can:**
- View available events
- Register for an event

✅ **Admins can:**
- Add new events via a simple form

✅ **Backend:**
- FastAPI provides a RESTful API for frontend interaction
- SQLAlchemy ORM for database operations

✅ **Frontend:**
- HTML/CSS for layout and styling
- JavaScript for making API calls and dynamic updates
---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

git clone https://github.com/YOUR-USERNAME/college_events.git
cd college_events


### 2️⃣ Create & Activate Virtual Environment
python -m venv venv

- For Windows:
.\venv\Scripts\activate

- For macOS/Linux:
source venv/bin/activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Run the FastAPI Server
uvicorn backend.main:app --reload
- Your API will be available at http://127.0.0.1:8000

### 5️⃣ Open the Frontend
Open frontend/index.html in your browser and try:

- Registering for events

- Creating new events

# 📌 API Endpoints

- GET / - API health check
- POST /events - Create a new event
- GET /events - Get all events
- POST /register - Register for an event
- GET /registrations - Get all registrations
