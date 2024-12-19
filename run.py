from flask import Flask
from books import books_bp
from members import members_bp

app = Flask(__name__)

# blueprints Registeration
app.register_blueprint(books_bp)
app.register_blueprint(members_bp)

if __name__ == '__main__':
    app.run(debug=True)