# SheLearn Web Application

SheLearn is a web-based e-learning platform designed to support women entering the tech industry. It offers two structured learning tracks — **Data Science & Analysis** and **Software Development** — with role-based access for students, facilitators, and administrators.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [User Roles](#user-roles)
- [Pages & Routes](#pages--routes)
- [API Endpoints](#api-endpoints)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Environment Variables](#environment-variables)
- [Running the App](#running-the-app)
- [Seeding the Database](#seeding-the-database)
- [Deployment Notes](#deployment-notes)

---

## Features

- User registration and login with hashed passwords
- Role-based dashboards: Student, Facilitator, Admin
- Two learning tracks with module and lesson pages
- Facilitator mode — edit lesson content directly on the page and save it to the database
- Knowledge quiz with server-side scoring
- Progress tracking — students can mark lessons as complete
- Admin panel — view all users, add new users, delete users
- Bootstrap 5 carousel on the landing page
- Flash messages for user feedback (errors, success, info)
- Fully local static assets — no external image dependencies

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, Flask 3.0 |
| **Database** | SQLite (via Flask-SQLAlchemy 3.1) |
| **Authentication** | Werkzeug password hashing (pbkdf2:sha256) |
| **Templating** | Jinja2 (built into Flask) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **UI Framework** | Bootstrap 5 (CDN) |
| **Environment** | python-dotenv |
| **CORS** | Flask-CORS |

---

## Project Structure

```
SheLearn_WebApp/
│
├── Backend/
│   ├── app.py                  # Main Flask application — all routes and API endpoints
│   ├── db.py                   # SQLAlchemy models (User, Progress, LessonContent)
│   ├── seed.py                 # Script to populate the database with sample users
│   ├── reset_passwords.py      # Utility to reset user passwords
│   ├── shelearn.db             # SQLite database (auto-created, not committed to git)
│   ├── .env                    # Secret environment variables (not committed to git)
│   ├── .env.example            # Template showing required environment variables
│   ├── requirements.txt        # Pinned Python dependencies
│   │
│   ├── routes/
│   │   ├── auth.py             # Auth blueprint (logout)
│   │   └── user.py             # User blueprint (progress tracking)
│   │
│   ├── static/
│   │   ├── styles.css          # Global styles and flash message styling
│   │   ├── landing-sections.css# Landing page and carousel styles
│   │   ├── script.js           # Frontend JavaScript (admin modals, fetch calls)
│   │   ├── hero-bg.jpeg        # Landing page hero background
│   │   ├── ladder.jpeg         # Carousel "What We Do" slide background
│   │   ├── dev.jpeg            # Software Development student dashboard card image
│   │   └── data_sc.jpeg        # Data Science student dashboard card image
│   │
│   └── templates/
│       ├── landing.html        # Public landing page with carousel
│       ├── login.html          # Login page
│       ├── SignUp.html         # Registration page
│       ├── student.html        # Data Science student dashboard
│       ├── dev_student.html    # Software Development student dashboard
│       ├── course-modules.html # Data Science modules list
│       ├── dev_modules.html    # Software Development modules list
│       ├── lesson.html         # APIs & Web Scraping lesson
│       ├── ai-intro.html       # Introduction to AI lesson
│       ├── srs.html            # SRS Document lesson
│       ├── uml.html            # Software Design & UML lesson
│       ├── knowledge-test.html # Quiz page
│       ├── facilitator.html    # Facilitator dashboard (student progress overview)
│       └── admin.html          # Admin dashboard (user management)
│
├── Frontend/                   # Static HTML prototypes (design reference only)
│
├── .gitignore
└── README.md
```

---

## Database Models

### `User`
| Column | Type | Description |
|---|---|---|
| `id` | Integer | Primary key |
| `name` | String(100) | Full name |
| `email` | String(120) | Unique email address |
| `password_hash` | String(256) | Hashed password (Werkzeug) |
| `role` | String(20) | `student`, `facilitator`, or `admin` |
| `track` | String(60) | `software-development` or `data-science` |

### `Progress`
| Column | Type | Description |
|---|---|---|
| `id` | Integer | Primary key |
| `user_id` | Integer | Foreign key → `users.id` |
| `lesson_name` | String(120) | Name of the completed lesson |
| `completed_at` | DateTime | Timestamp of completion |

### `LessonContent`
| Column | Type | Description |
|---|---|---|
| `id` | Integer | Primary key |
| `slug` | String(80) | Unique URL identifier (e.g. `apis-web-scraping`) |
| `title` | String(200) | Lesson title (editable by facilitator) |
| `description` | Text | Lesson description (editable by facilitator) |
| `paragraphs_json` | Text | JSON array of paragraph strings |
| `updated_at` | DateTime | Last updated timestamp |

---

## User Roles

| Role | Access |
|---|---|
| **Student** | Dashboard, module list, lesson pages, knowledge quiz, progress tracking |
| **Facilitator** | Everything students see + edit lesson content inline + view all student progress |
| **Admin** | Admin dashboard — view, add, and delete users |

---

## Pages & Routes

| Route | Method | Description |
|---|---|---|
| `/` or `/landing` | GET | Public landing page |
| `/login` | GET, POST | Login form |
| `/SignUp` | GET, POST | Registration form |
| `/logout` | GET | Clears session and redirects to login |
| `/dashboard` | GET | Redirects to the correct student dashboard |
| `/student/<name>` | GET | Data Science student dashboard |
| `/dev_student` | GET | Software Development student dashboard |
| `/course-modules` | GET | Data Science module list with progress |
| `/dev_modules` | GET | Software Development module list with progress |
| `/lesson` | GET | APIs & Web Scraping lesson |
| `/ai-intro` | GET | Introduction to AI lesson |
| `/srs` | GET | SRS Document lesson |
| `/uml` | GET | Software Design & UML lesson |
| `/knowledge-test` | GET | Quiz page |
| `/facilitator` | GET | Facilitator dashboard (protected) |
| `/admin` | GET | Admin dashboard (protected) |

---

## API Endpoints

| Endpoint | Method | Role Required | Description |
|---|---|---|---|
| `/api/quiz/submit` | POST | Student | Submit quiz answers, returns score and percentage |
| `/api/lessons/update` | POST | Facilitator | Save edited lesson content to the database |
| `/api/admin/add-user` | POST | Admin | Create a new user account |
| `/api/admin/delete-user` | POST | Admin | Delete a user and their progress records |
| `/api/user/progress` | POST | Student | Mark a lesson as complete |
| `/api/auth/logout` | GET/POST | Any | Log out and clear session |

---

## Prerequisites

Before setting up the project, make sure you have the following installed:

- **Python 3.10 or higher** — [python.org](https://www.python.org/downloads/)
- **pip** — comes with Python
- **Git** — [git-scm.com](https://git-scm.com/)

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/SheLearn_WebApp.git
cd SheLearn_WebApp
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r Backend/requirements.txt
```

### 4. Set up environment variables

Copy the example file and fill in your values:

```bash
cp Backend/.env.example Backend/.env
```

Then open `Backend/.env` and set a real secret key:

```
SECRET_KEY=replace_this_with_a_long_random_string
```

To generate a strong secret key, run this in your terminal:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | A long random string used to sign session cookies. Never share this. |

The app will refuse to start if `SECRET_KEY` is not set.

---

## Running the App

```bash
cd Backend
python app.py
```

The server starts on **http://localhost:3000**

The SQLite database (`shelearn.db`) is created automatically on first run — no migration steps needed.

---

## Seeding the Database

To populate the database with sample users for testing:

```bash
cd Backend
python seed.py
```

To reset all user passwords (useful if hashes become outdated):

```bash
cd Backend
python reset_passwords.py
```

---

## How to Use the App

### As a Student
1. Go to `/SignUp` and create an account — choose your track (Data Science or Software Development).
2. You will be taken to your dashboard automatically.
3. Navigate to **Course Modules** to see your available lessons.
4. Open a lesson, read through it, and click **Mark as Complete** when done.
5. Your progress percentage will update on the modules page.
6. Take the **Knowledge Test** at any time to check your understanding.

### As a Facilitator
1. Log in with a facilitator account (created by the admin).
2. Navigate to any lesson page — an **Edit** button will appear.
3. Click **Edit**, modify the title, description, or content directly on the page.
4. Click **Save** — changes are stored in the database and shown to all students immediately.
5. Visit the **Facilitator Dashboard** to see all student progress records.

### As an Admin
1. Log in with the admin account.
2. The **Admin Dashboard** shows total student and facilitator counts.
3. Use the **Add User** button to create a new student or facilitator account.
4. Use the **Delete User** button to remove a user by their email address.

---

## Deployment Notes

- **Never commit `.env`** — it is listed in `.gitignore`.
- **Never commit `shelearn.db`** — it is also gitignored. On your deployment server, the database is created fresh on first run.
- Set `SECRET_KEY` as an environment variable on your hosting platform (e.g. Render, Railway, Heroku) — do not put it in source code.
- Set `debug=False` in `app.run()` before deploying to production.
- For production, consider replacing SQLite with PostgreSQL and using a proper WSGI server like **Gunicorn**.

---

## License

This project was built for the SheLearn programme. All rights reserved.
