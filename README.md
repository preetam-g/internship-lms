# Internship Learning Management System (LMS)

A robust, full-stack Learning Management System designed for internship management. This application features a secure, multi-role architecture (RBAC) to handle different user permissions and real-world business logic.

---

## 🛠 Tech Stack

* **Frontend:** React.js
* **Backend:** Django REST Framework (DRF)
* **Database:** PostgreSQL (via Supabase)
* **Authentication:** JWT (JSON Web Tokens)
* **State Management:** React State and Context

---

## 🔐 Key Features & RBAC Enforcement

The system implements a strict **Role-Based Access Control** system to ensure data integrity and security:

* **Admin:** Full access to manage users and view all courses currently on the platform.
* **Mentor:** Can create courses and assign students to courses.
* **Intern:** Can view curriculum, complete chapters (one-by-one), and track their own progress in each course.

> **Note:** Permissions are enforced at the API level using custom DRF permission classes and on the frontend via protected routes.

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

## 🤖 AI Disclosure

In compliance with the project guidelines, AI was utilized for:

* Initial project scaffolding.
* Generating and upgrading code logic and performance.
* Drafting documentation.
* *All business logic, database schema design, and RBAC enforcement were reviewed, modified, and manually verified for accuracy.*

---

## 📸 Screenshots

<img width="1710" height="1073" alt="Screenshot 2025-12-20 at 00 10 08" src="https://github.com/user-attachments/assets/9ca387e9-0304-4b43-b190-bd199e82e9fc" />
<img width="1710" height="1073" alt="Screenshot 2025-12-20 at 00 10 32" src="https://github.com/user-attachments/assets/097d4a81-f774-4a99-8a16-6eb6b7783344" />
<img width="1710" height="1073" alt="Screenshot 2025-12-20 at 00 11 04" src="https://github.com/user-attachments/assets/bad818e9-dc3b-492e-ac9e-bb616b568670" />


