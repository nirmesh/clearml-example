from clearml import Task
import requests

# 1. Initialize ClearML - this automatically tracks your experiment in the UI
task = Task.init(
    project_name="Nirmesh-18-Aug", 
    task_name="Ollama LLM Test Inference"
)

# 2. Set up your Ollama details (Update the IP if Ollama is running inside K8s or a specific node)
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate" 

config_params = {
    "model": "llama3",  # Change to your specific model name
    "prompt": "What are the first 3 steps to take after installing a Kubernetes cluster?",
    "temperature": 0.7
}
# Track hyperparameters automatically in the 'Hyperparameters' tab
task.connect(config_params)

# 3. Call Ollama
try:
    print(f"Sending prompt to Ollama: {config_params['prompt']}")
    response = requests.post(OLLAMA_ENDPOINT, json={
        "model": config_params["model"],
        "prompt": config_params["prompt"],
        "options": {"temperature": config_params["temperature"]},
        "stream": False
    })
    
    output_text = response.json().get("response", "")
    
    # 4. Log text outputs and results to ClearML 
    print("Inference completed successfully!")
    task.get_logger().report_text(f"Prompt sent: {config_params['prompt']}")
    task.get_logger().report_text(f"Ollama Output: {output_text}")
    
    # Save the output as an artifact file in ClearML
    task.upload_artifact("llm_response", artifact_object=output_text)

except Exception as e:
    print(f"Failed to connect to Ollama: {e}")

task.close()
