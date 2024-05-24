from app import app
from app.utils import populate_db

with app.app_context():
    populate_db()

if __name__ == "__main__":
    app.run(debug=True)
