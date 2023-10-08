import os
import uuid
from django.core.files.storage import default_storage


def generate_unique_filename(filename):
    file_extension = os.path.splitext(filename)[-1]
    unique_id = uuid.uuid4().hex

    new_filename = f"{unique_id}{file_extension}"

    return new_filename


def handle_uploaded_file(upload_file):
    original_filename = upload_file.name

    new_filename = generate_unique_filename(original_filename)

    path = default_storage.save(new_filename, upload_file)

    return path
