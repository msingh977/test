from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import re
import os
from app.utils import upload_to_gcp
from datetime import datetime
import traceback

# Define the blueprint
main = Blueprint('main', __name__)

# ---------------- Main Route ----------------
@main.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# ---------------- Save to Firestore and GCP (Atomic) ----------------
@main.route('/', methods=['POST'])
def submit_info():
    """Submit user data and save to Firestore and GCP atomically"""
    try:
        # Collect form data
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        address = request.form['address'].strip()
        city = request.form['city'].strip()
        zipcode = request.form['zipcode'].strip()
        email = request.form['email'].strip()
        phone = request.form['phone'].strip()

        # Basic validation
        if not all([first_name, last_name, address, city, zipcode, email, phone]):
            flash("Please fill in all fields.", "error")
            return redirect(url_for('main.home'))

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            flash("Please enter a valid email address.", "error")
            return redirect(url_for('main.home'))

        phone_digits = re.sub(r"\D", "", phone)
        if not re.match(r"^\+?\d{10,15}$", phone_digits):
            flash("Please enter a valid phone number (10–15 digits).", "error")
            return redirect(url_for('main.home'))

        # Create text file for GCP upload
        info = (
            f"Name: {first_name} {last_name}\n"
            f"Address: {address}, {city}, {zipcode}\n"
            f"Email: {email}\n"
            f"Phone: {phone}"
        )

        safe_address = address.replace(" ", "_").replace(",", "")
        safe_zipcode = zipcode.replace(" ", "_").replace(",", "")
        date_str = datetime.now().strftime("%Y%m%d")
        local_file = "user_info.txt"
        remote_path = f"user_data_{date_str}/{safe_address}_{safe_zipcode}.txt"

        # Write data to local file
        with open(local_file, "w") as file:
            file.write(info)

        # Firestore document data
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "city": city,
            "zipcode": zipcode,
            "email": email,
            "phone": phone,
            "submitted_at": datetime.utcnow()
        }

        db = current_app.firestore_client
        print("✅ Firestore client obtained:", db)
        print("📦 Data being saved to Firestore:", data)

        # ---- Step 1: Save to Firestore ----
        doc_ref = db.collection('user_submissions').document()
        try:
            doc_ref.set(data)
            print("✅ Data saved to Firestore successfully")
        except Exception as db_err:
            print("❌ Firestore insertion failed:")
            traceback.print_exc()
            raise db_err  # Propagate to main except

        # ---- Step 2: Upload to GCP ----
        try:
            upload_to_gcp(local_file, "mowingestimation", remote_path)
            print("✅ File uploaded to GCP successfully")

        except Exception as upload_err:
            print("❌ GCP upload failed, rolling back Firestore document...")
            traceback.print_exc()
            try:
                doc_ref.delete()
                print("🗑️ Firestore document deleted due to failed GCP upload")
            except Exception as delete_err:
                print("⚠️ Rollback failed: could not delete Firestore document.")
                traceback.print_exc()
            raise upload_err  # Re-raise for unified error handling

        flash("✅ Your estimation has been submitted successfully!", "success")
        return render_template("submit.html")

    except Exception as e:
        print("❌ Error during submission process:")
        traceback.print_exc()

        flash(f"⚠️ Submission failed: {e}", "error")
        return redirect(url_for('main.home'))
