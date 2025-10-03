import os
import sys
import django

# Add project directory to the Python path
sys.path.append(r'D:\FaceMatch\facemash')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facemash.settings')
django.setup()

from comparison.models import Image
from django.core.files import File

def truncate_filename(filename, max_length=150):
    """
    Truncate filename to fit within the max_length limit.
    """
    root, ext = os.path.splitext(filename)
    if len(root) > max_length:
        root = root[:max_length]
    return root + ext

def upload_images_from_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'rb') as f:
                # Truncate filename
                truncated_filename = truncate_filename(filename)
                # Create a new Image instance
                new_image = Image(image=File(f, name=truncated_filename))
                new_image.save()
                print(f'Saved {filename} to the database.')

if __name__ == "__main__":
    images_directory = r'D:\FaceMatch\Photos'
    upload_images_from_directory(images_directory)
