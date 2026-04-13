# snip — url shortener

![Snip UI](static/snip.png)

A minimal URL shortening app built with Flask and MySQL. Shorten long URLs, track click counts, update destinations, and delete links.

## Stack

| Layer | Technology |
|---|---|
| Backend | Flask, Flask-SQLAlchemy, Flask-Migrate |
| Database | MySQL (via PyMySQL) |
| Frontend | Vanilla HTML + CSS + JS (no build step) |

## Getting Started

**1. Clone and create a virtual environment**

```bash
git clone <repo-url>
cd url-shortener
python -m venv venv
source venv/bin/activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` and fill in your MySQL credentials:

```
DATABASE_URL=mysql+pymysql://user:password@localhost/snip
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

**4. Run database migrations**

```bash
flask --app run db init
flask --app run db migrate -m "initial"
flask --app run db upgrade
```

**5. Start the server**

```bash
python run.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/shorten` | Create a short URL — body: `{"url": "..."}` |
| `GET` | `/shorten/<code>` | Fetch record and increment click counter |
| `PUT` | `/shorten/<code>` | Update destination — body: `{"url": "..."}` |
| `DELETE` | `/shorten/<code>` | Delete the short URL |
| `GET` | `/shorten/<code>/stats` | Fetch record without incrementing counter |
| `GET` | `/<code>` | Redirect to the original URL |

## Project Structure

```
url-shortener/
├── app/
│   ├── __init__.py     # app factory
│   ├── models.py       # Url database model
│   ├── routes.py       # Blueprint with all endpoints
│   ├── services.py     # CRUD business logic
│   └── utils.py
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── config.py
├── run.py
└── requirements.txt
```
