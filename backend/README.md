# Yearly Rewind for LOL

## Get Started
1. Clone repo & install dependencies
```
git clone <repo-url>
cd backend
conda create -n league_rewind python=3.12
conda activate league_rewind
pip install -r requirements.txt
```
2. Environment variables
Create a .env file:
```
DATABASE_URL=sqlite:///league.db
RIOT_API_KEY=RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```
3. Run the app
```
python app.py
```
The API will be available at: http://127.0.0.1:5000

## Database & Migrations
We use Flask-Migrate to manage schema changes.

### First-time setup
```
flask db init
flask db migrate -m "initial tables"
flask db upgrade
```

### After modifying models (models/schema.py)
1. Edit your model (e.g., add a column to Player).
2. Run:
    ```
    flask db migrate -m "describe change here"
    flask db upgrade
    ```
3. Check your SQLite DB



## Project Structure
```
backend/
│── app.py                  # App factory, register routes
│── config.py               # Config (env variables, API key, DB URL)
│── extensions.py            # db, migrate instances
│── models/
│    └── schema.py          # SQLAlchemy models: Player, Match, Participant
│── routes/
│    └── player_routes.py   # Player endpoints
│── services/
│    └── player_service.py  # Business logic (DB + Riot API calls)
│── migrations/             # Auto-generated migration scripts
│── league.db               # SQLite database
│── .env                    # Environment variables
│── requirements.txt
│── README.md
```