import shutil

def clean_directory(directory="temp_downloads"):
    shutil.rmtree(directory)

def is_colab():
    try:
        import google.colab
        return True
    except ImportError:
        return False

