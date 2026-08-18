import os
import requests
from clearml import Task
from clearml.datasets import Dataset

# 1. Initialize ClearML task tracking
task = Task.init(
    project_name="Nimesh-18-Aug", 
    task_name="Pipeline Step 2 - Inference Run"
)

print("--- Step 1: Fetching the dataset from ClearML ---")

# 2. Automatically download the dataset folder to this machine
dataset_folder = Dataset.get(
    dataset_project="Nimesh-18-Aug/Datasets", 
    dataset_name="Simple_LLM_Prompts"
).get_local_copy()

# Read the file from the downloaded dataset path
prompts_file_path = os.path.join(dataset_folder, "prompts.txt")
with open(prompts_file_path, "r") as f:
    prompts = [line.strip() for line in f if line.strip()]

print(f"Found {len(prompts)} prompts in the dataset.")

print("\n--- Step 2: Processing through Ollama ---")
logger = task.get_logger()

# 3. Loop through our dataset prompts
for i, prompt in enumerate(prompts):
    print(f"Running prompt {i+1}...")
    try:
        response = requests.post(
            "http://localhost:11434/api/generate", 
            json={
                "model": "gpt-oss:120b",  # Switch to your specific model name
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        output_text = response.json().get("response", "")
        
        # Log each answer clearly into your dashboard
        logger.report_text(f"Prompt {i+1}: {prompt}")
        logger.report_text(f"Ollama Answer {i+1}:\n{output_text}\n{'='*40}")
        
    except Exception as e:
        print(f"Error on prompt {i+1}: {e}")

task.close()
print("\nPipeline run complete! Check your main Tasks dashboard.")
