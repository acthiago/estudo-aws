from app import app, db
from app.utils import populate_db

with app.app_context():
    db.create_all()
    populate_db()

if __name__ == "__main__":
    app.run(debug=True)
