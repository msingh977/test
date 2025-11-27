from google.cloud import storage
import os

def upload_to_gcp(local_file_path, bucket_name, remote_path):
    """Upload a file to GCP using the Python client library."""
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your service account JSON key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"./service-account.json"

    # Initialize a Cloud Storage client
    client = storage.Client()

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    # Create a blob (object) in the bucket
    blob = bucket.blob(remote_path)

    # Upload the file to GCP
    blob.upload_from_filename(local_file_path)
    print(f"File uploaded to {bucket_name}/{remote_path}")
