import os
import requests
from clearml import Task

# Ensure strict connection timeouts for ClearML requests
os.environ["CLEARML_API_DEFAULT_REQ_TIMEOUT"] = "10"

print("--- Step 1: Initializing ClearML Task ---")
task = Task.init(
    project_name="Nirmesh-18-Aug", 
    task_name="Ollama LLM Tracked Inference"
)

# 1. Define your parameters (ClearML tracks this dictionary automatically)
config_params = {
    "ollama_endpoint": "http://100.71.85.134:11434/api/generate", # Change to host IP if Ollama is remote
    "model": "gpt-oss:120b",  # Switch to your specific downloaded model name
    "prompt": "Give me a quick 3-bullet point summary of why MLOps is useful.",
    "temperature": 0.7
}
task.connect(config_params)

print("\n--- Step 2: Querying local Ollama instance ---")
try:
    # Send a request to the Ollama API service
    response = requests.post(
        config_params["ollama_endpoint"], 
        json={
            "model": config_params["model"],
            "prompt": config_params["prompt"],
            "options": {"temperature": config_params["temperature"]},
            "stream": False
        },
        timeout=30  # Allow up to 30 seconds for the model to think/respond
    )
    
    # Parse out the string text response
    response_data = response.json()
    output_text = response_data.get("response", "")
    
    print("--- Step 3: Success! Logging results to ClearML Dashboard ---")
    logger = task.get_logger()
    
    # 2. Report data straight to the 'Console' text log view
    logger.report_text(f"Prompt Sent: {config_params['prompt']}")
    logger.report_text(f"Ollama Output Received:\n{output_text}")
    
    # 3. Save the response as an explicit file artifact in your dashboard
    task.upload_artifact("ollama_llm_response", artifact_object=output_text)
    print("Logged metrics and text sample artifacts cleanly.")

except Exception as e:
    print(f"\n[!] Failed to pull generation response from Ollama: {e}")
    print("Make sure your Ollama background app or container is running and exposed.")

task.close()
print("\nTask finished and connection closed successfully.")
