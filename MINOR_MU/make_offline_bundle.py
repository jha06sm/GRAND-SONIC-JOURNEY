from huggingface_hub import snapshot_download
import os, shutil

MODELS = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "distilgpt2",
    "ai4bharat/indic-gpt"
]

def safe_copy(src, dst):
    if os.path.isdir(dst):
        return
    shutil.copytree(src, dst)

def main():
    os.makedirs("models", exist_ok=True)
    for name in MODELS:
        print(f"Downloading {name} ...")
        cache_dir = snapshot_download(repo_id=name)
        local_name = name.replace('/', '__')
        target = os.path.join("models", local_name)
        print(f"Copying to {target} ...")
        safe_copy(cache_dir, target)
    print("All models downloaded to ./models/")

if __name__ == '__main__':
    main()
