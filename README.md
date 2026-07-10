# CampusConnect

A campus Q&A forum web app built with Django. Students can register, ask questions, answer others, and discover trending topics — all in one place.

---

## Features

- User registration with OTP email verification
- Login / logout with session management
- Ask questions with tags
- Answer questions from the community
- Dashboard with personal stats and unanswered questions
- Search questions by keyword
- Edit profile and change password
- Responsive UI with Bootstrap 5 and Bootstrap Icons

---

## Tech Stack

| Layer      | Tech                          |
|------------|-------------------------------|
| Backend    | Django 5.2                    |
| Database   | SQLite (dev) / PostgreSQL (prod) |
| Frontend   | Bootstrap 5.3, Bootstrap Icons |
| Forms      | django-crispy-forms            |
| Config     | python-decouple               |
| Server     | Gunicorn                      |

---

## Project Structure

```
campusconnect/
├── campusconnect/        # Project settings, URLs
├── users/                # Auth, profiles, OTP verification
├── forum/                # Questions, answers, tags, search
├── templates/            # Base template
├── static/               # CSS and JS
│   ├── css/main.css
│   └── js/main.js
├── manage.py
├── requirements.txt
└── .env                  # Not committed — see below
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/campusconnect.git
cd campusconnect
```

### 2. Create and activate a virtual environment

```bash
python -m venv myenv
# Windows
myenv\Scripts\activate
# macOS/Linux
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the `campusconnect/` directory:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ALLOWED_HOSTS=127.0.0.1,localhost
```

> For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) rather than your account password.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## Environment Variables

| Variable            | Description                        |
|---------------------|------------------------------------|
| `EMAIL_HOST_USER`   | Gmail address used to send OTPs    |
| `EMAIL_HOST_PASSWORD` | Gmail App Password               |
| `ALLOWED_HOSTS`     | Comma-separated list of hosts      |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feature/your-feature`
5. Open a pull request

---

## License

This project is open source and available under the [MIT License](LICENSE).
