import os
from clearml import StorageManager
from clearml.datasets import Dataset

# 1. Create a local folder and a file with our prompts
os.makedirs("my_local_prompts", exist_ok=True)
with open("my_local_prompts/prompts.txt", "w") as f:
    f.write("Explain Kubernetes in 1 short sentence.\n")
    f.write("What is ClearML used for?\n")
    f.write("Why do people use Ollama?\n")

print("--- Step 1: Creating a Versioned Dataset in ClearML ---")

# 2. Initialize a ClearML Dataset
dataset = Dataset.create(
    dataset_project="Nimesh-18-Aug/Datasets", 
    dataset_name="Simple_LLM_Prompts"
)

# 3. Add our local folder containing the file to the dataset tracking
dataset.add_files("my_local_prompts")

# 4. Upload and close
dataset.upload()
dataset.finalize()

print(f"Dataset successfully created! Version ID: {dataset.id}")
