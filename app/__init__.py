from flask import Flask
import os
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore  # <-- use Cloud SDK for named DBs

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "PASSWORD")

    # Path to Firebase service account key
    cred_path = os.path.join(os.path.dirname(__file__), 'firebase_key.json')

    # Initialize Firebase Admin once
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    # ✅ Use google.cloud.firestore.Client for named database
    app.firestore_client = firestore.Client(database="estimator")

    # Optionally register blueprints
    try:
        from app.routes import main
        app.register_blueprint(main)
    except ImportError:
        pass

    return app

# Example usage (for testing/running locally)
if __name__ == '__main__':
    # Make sure 'firebase_key.json' is present for this to run
    try:
        my_app = create_app()
        print("Flask app created successfully!")
        print(f"Firestore Client configured for database: {my_app.firestore_client.database}")
        # my_app.run(debug=True)
    except FileNotFoundError:
        print("ERROR: firebase_key.json not found. Cannot initialize Firebase.")
    except Exception as e:
        print(f"An error occurred during app creation: {e}")