import os
import tkinter as tk
from tkinter import messagebox
from app import create_app  # Assuming you have a Flask app

# Add your Flask-related logic here if needed.
app = create_app()

def submit_info():
    # Your function logic here
    pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

