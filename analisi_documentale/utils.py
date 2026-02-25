import shutil
from pathlib import Path
from transformers import AutoTokenizer
from urllib.parse import urlparse

def clean_directory(directory = "temp_downloads"):
    try:
        dir_path = Path(directory)
        if dir_path.exists() and dir_path.is_dir():
            shutil.rmtree(directory)
    except Exception as e:
        raise Exception(f"Errore durante la rimozione di '{directory}': {e}")

def is_colab():
    try:
        import google.colab
        return True
    except ImportError:
        return False

def count_tokens(text: str):
    try:
        tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.3-70B-Versatile")
        tokens = tokenizer(text)
        return len(tokens['input_ids'])
    except Exception as e:
        return len(text.split())

def is_url(s):
    parsed = urlparse(s)
    return bool(parsed.scheme and parsed.netloc)
