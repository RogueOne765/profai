import shutil
from transformers import AutoTokenizer

def clean_directory(directory="temp_downloads"):
    shutil.rmtree(directory)

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
