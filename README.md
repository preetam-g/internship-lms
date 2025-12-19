# Internship Learning Management System (LMS)

A robust, full-stack Learning Management System designed for internship management. This application features a secure, multi-role architecture (RBAC) to handle different user permissions and real-world business logic.

## 🚀 Live Deployment

**[Insert Live Link Here - e.g., Vercel/Render/Railway]**

---

## 🛠 Tech Stack

* **Frontend:** React.js
* **Backend:** Django REST Framework (DRF)
* **Database:** PostgreSQL (via Supabase)
* **Authentication:** JWT (JSON Web Tokens)
* **State Management:** [e.g., Redux Toolkit or React Context API]

---

## 🔐 Key Features & RBAC Enforcement

The system implements a strict **Role-Based Access Control** system to ensure data integrity and security:

* **Admin:** Full access to manage users, internship tracks, and global settings.
* **Mentor:** Can create content, grade assignments, and track intern progress.
* **Intern:** Can view curriculum, submit tasks, and track their own performance.

> **Note:** Permissions are enforced at the API level using custom DRF permission classes and on the frontend via protected routes.

---

## 📁 Project Structure

```text
├── backend/            # Django Project & Apps
├── frontend/           # React Application
├── .env.example        # Environment variable templates
└── README.md

```

---

## ⚙️ Setup Instructions

### 1. Prerequisites

* Python 3.x
* Node.js & npm
* Supabase Account (PostgreSQL)

### 2. Backend Setup

1. Clone the repository: `git clone <repo-url>`
2. Navigate to backend: `cd backend`
3. Create a virtual environment: `python -m venv venv`
4. Activate venv: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Win)
5. Install dependencies: `pip install -r requirements.txt`
6. Configure `.env` with your **Supabase/PostgreSQL** credentials.
7. Run migrations: `python manage.py migrate`
8. Start server: `python manage.py runserver`

### 3. Frontend Setup

1. Navigate to frontend: `cd frontend`
2. Install dependencies: `npm install`
3. Configure `.env` with backend API URL.
4. Start development server: `npm start`

---

## 🧪 Test Report & Coverage

Detailed testing was performed to ensure RBAC integrity.

* **Unit Tests:** Handled via `pytest` / `unittest`.
* **Coverage Summary:** * Models: 100%
* RBAC Middleware/Permissions: 100%
* Total Coverage: **[Insert % here, e.g., 85%]**



---

## 🤖 AI Disclosure

In compliance with the project guidelines, AI was utilized for:

* Initial project scaffolding.
* Validation of complex Regex patterns.
* Drafting initial documentation.
* *All business logic, database schema design, and RBAC enforcement were reviewed, modified, and manually verified for accuracy.*

---

## 📸 Screenshots