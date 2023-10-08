import os
import uuid
from django.core.files.storage import default_storage


def generate_unique_filename(filename):
    # Get the file extension
    file_extension = os.path.splitext(filename)[-1]

    # Generate a unique identifier (you can use other methods too)
    unique_id = uuid.uuid4().hex

    # Combine the unique ID and file extension to create a new filename
    new_filename = f"{unique_id}{file_extension}"

    return new_filename


def handle_uploaded_file(upload_file):
    # Get the original filename
    original_filename = upload_file.name

    # Generate a unique filename
    new_filename = generate_unique_filename(original_filename)

    # Save the file with the new filename
    path = default_storage.save(new_filename, upload_file)

    # You can now use the 'path' variable to store the file path in your database
    return path
