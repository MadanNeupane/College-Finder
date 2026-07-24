# College Finder

![walkthrough](walkthrough.gif)
![Predicting Chances + Dark Mode](chance_prediction.gif)

> **Live:** [https://college-finder-m534.onrender.com](https://college-finder-m534.onrender.com/)

A platform for graduate college aspirants to discover universities, compare options, predict admission chances, and manage their shortlist.

## Features

- Beautiful interactive dashboard with data visualisation
- 1,500+ universities
- Admission chance prediction (Machine Learning — Logistic Regression)
- Side-by-side college comparison
- Blogging system with tagging
- Bookmark / shortlist management
- Google & Facebook social login
- Dark mode
- Fully responsive (mobile-first)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.x (Python 3.11+) |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Static files | WhiteNoise 6.x (compressed + hashed) |
| Auth | django-allauth + social-auth-app-django |
| ML | scikit-learn, numpy, scipy |
| Deployment | Render (free tier) / Docker |

---

## Getting Started

### Option A — Local (virtualenv)

#### 1. Clone

```bash
git clone https://github.com/MadanNeupane/College-Finder.git
cd College-Finder
```

#### 2. Create & activate a virtual environment

```bash
# Create
python -m venv env

# Activate — Windows
env\Scripts\activate

# Activate — Linux / macOS
source env/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set up environment variables

```bash
# Copy the template
cp .env.example .env

# Then edit .env and fill in your values
```

Key variables (see `.env.example` for the full list):

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `SECRET_KEY` | ✅ | — | Django secret key |
| `DEBUG` | | `False` | Enable debug mode |
| `DATABASE_URL` | | *(empty → SQLite)* | PostgreSQL connection URL |
| `ALLOWED_HOSTS` | | `localhost,127.0.0.1` | Comma-separated hostnames |
| `USE_WHITENOISE_MANIFEST` | | `False` in dev | Compressed static files |
| `SERVE_MEDIA_IN_PRODUCTION` | | `True` | Django serves `/media/` |
| `EMAIL_HOST_USER` | | *(console backend)* | SMTP email address |

#### 5. Run migrations

```bash
python manage.py migrate
```

#### 6. (Optional) Create a superuser

```bash
python manage.py createsuperuser
```

Or set `DJANGO_SUPERUSER_*` vars in `.env` and run:

```bash
python create_superuser.py
```

#### 7. Start the development server

```bash
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000)

---

### Option B — Docker (recommended for consistent environments)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/).

#### SQLite (quickest — no extra services)

```bash
# Copy env template and set at least SECRET_KEY
cp .env.example .env

docker compose up --build
```

Open [http://localhost:8000](http://localhost:8000)

#### PostgreSQL (mirrors production)

```bash
cp .env.example .env
# In .env, set:
#   DATABASE_URL=postgresql://college_finder_user:changeme_in_dotenv@db:5432/college_finder
#   DB_SSL_REQUIRE=False
#   POSTGRES_PASSWORD=changeme_in_dotenv

docker compose --profile postgres up --build
```

#### Useful Docker commands

```bash
# Run a management command inside the container
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py shell

# Stop all services
docker compose down

# Wipe the database volume and start fresh
docker compose down -v
```

#### Build arguments

```bash
# Use a different Python version
PYTHON_VERSION=3.12-slim docker compose up --build

# Use a different port
PORT=9000 docker compose up
```

---

## Switching Databases

The database backend is controlled entirely by the `DATABASE_URL` env var:

```bash
# SQLite (default — no DATABASE_URL needed)
# DATABASE_URL=

# PostgreSQL
DATABASE_URL=postgresql://user:password@hostname:5432/dbname

# PostgreSQL with SSL (Render / Railway / Heroku)
DATABASE_URL=postgresql://user:password@hostname:5432/dbname
DB_SSL_REQUIRE=True
```

No code changes required — just update `.env`.

---

## Static & Media Files

| Setting | Dev | Production |
|---|---|---|
| Static files | WhiteNoise serves plain files | WhiteNoise serves compressed + hashed files |
| Media files | Django dev server | Django serves via `/media/` (controlled by `SERVE_MEDIA_IN_PRODUCTION`) |
| `USE_WHITENOISE_MANIFEST` | `False` | `True` |

> **Note on free-tier hosting:** Media uploads are ephemeral on Render's free tier — files are lost on each redeploy. For persistence, set up an S3-compatible bucket and configure `django-storages`.

---

## Deployment (Render)

The project ships with a [`render.yaml`](render.yaml) and [`build.sh`](build.sh).

1. Fork / connect the repo on [Render](https://render.com)
2. Add environment variables in the Render dashboard (see `.env.example`)
3. Set `DEBUG=False` and `ALLOWED_HOSTS=your-app.onrender.com`
4. Set `CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com`
5. Render runs `./build.sh` automatically on each deploy

---

## Project Structure

```
College-Finder/
├── college_finder_app/   # Django project config (settings, urls, wsgi)
├── users/                # Auth, registration, profile
├── dashboard/            # Main dashboard
├── universities/         # University listings
├── college_comparison/   # Side-by-side comparison
├── bookmarks/            # Bookmark / shortlist
├── blogs/                # Blog system
├── faqs/                 # FAQ pages
├── components/
│   ├── static/           # CSS, JS, images
│   ├── templates/        # Shared HTML templates
│   └── media/            # User-uploaded files (gitignored)
├── fixtures/             # Initial data fixtures
├── Dockerfile            # Multi-stage Docker build
├── docker-compose.yml    # Local dev orchestration
├── docker-entrypoint.sh  # Migrate + start gunicorn
├── build.sh              # Render build script
├── render.yaml           # Render IaC config
├── requirements.txt      # Python dependencies (>= loose pins)
├── .env.example          # Environment variable template
└── manage.py
```

---

## Security Notes

- `SECRET_KEY` is required at startup — the app will refuse to start without it
- `DEBUG=True` is for local development only; never deploy with it enabled
- HTTPS-only cookies, HSTS, `X-Frame-Options: DENY`, and `SECURE_CONTENT_TYPE_NOSNIFF` are enforced when `DEBUG=False`
- `.env` is git-ignored; `.env.example` is the safe-to-commit template
- The Docker image runs as a non-root user (`appuser`)

---

## License

Restricted to the University of Wolverhampton for assessment purposes.

© Madan Neupane, 2021 – 2026
