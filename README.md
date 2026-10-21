1) Activate venv
 
2) pip install -r requirements.txt

3) python -m fastapi dev app/main.py

## Database migrations (Alembic)

All tables live in one shared Azure MySQL database, so structure changes go through Alembic migrations.
Needs a filled-in `.env` (copy `.env.example`, get the password from Mark) and your IP on the Azure firewall.

- Apply all pending migrations: `alembic upgrade head`
- See where the database is: `alembic current`
- Undo the last migration: `alembic downgrade -1`

Adding or changing a table:

1. Write the model in `app/models/` (a SQLModel class with `table=True`).
2. Import it in `app/db/base.py` so Alembic can see it.
3. `alembic revision --autogenerate -m "short description"`, then read the new file in `alembic/versions/` and check it does what you expect.
4. `alembic upgrade head`, then commit the model and the migration file together.

Team rules (one shared database, so migrations change everyone's data):

- Pull `main` before creating a migration.
- Merge your migration PR before running `upgrade` against the shared database, and let one person run it. Running it again is harmless.
- Never edit a migration that is already merged. Make a new one instead.
- If two migrations collide (Alembic reports multiple heads), fix it with `alembic merge heads`.
