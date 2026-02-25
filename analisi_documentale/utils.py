import shutil
from transformers import AutoTokenizer

def clean_directory(directory="temp_downloads"):
    try:
        shutil.rmtree(directory)
    except Exception as e:
        raise Exception(f"Error during removing depository {directory}, {e}")

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
