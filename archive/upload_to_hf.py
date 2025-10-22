from huggingface_hub import HfApi, create_repo

username = "Ninja69"
dataset_name = "military-battles-100k"
repo_id = username + "/" + dataset_name

print("Creating dataset: " + repo_id)

try:
    create_repo(repo_id=repo_id, repo_type="dataset", exist_ok=True)
    print("Repository created!")
except Exception as e:
    print("Error: " + str(e))

api = HfApi()
print("Uploading 33MB file (this may take a few minutes)...")

api.upload_file(
    path_or_fileobj="military_battles_dataset_100k.csv",
    path_in_repo="data.csv",
    repo_id=repo_id,
    repo_type="dataset",
)

print("DONE!")
print("View at: https://huggingface.co/datasets/" + repo_id)
