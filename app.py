from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, ContactMessage
from flask_migrate import Migrate




app = Flask(__name__)
app.config.from_object(Config)

# Init extensions
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

# Routes
@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'error': 'All fields are required'}), 400

    new_msg = ContactMessage(name=name, email=email, message=message)
    db.session.add(new_msg)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Message received'}), 200

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
