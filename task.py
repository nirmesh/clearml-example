import os
from clearml import Task

print("--- Step 1: Checking environment variables ---")
print(f"API Server Target: {os.getenv('CLEARML_API_HOST')}")

# Add a strict connection timeout limit so it errors out instead of hanging forever
os.environ["CLEARML_API_DEFAULT_REQ_TIMEOUT"] = "5"

try:
    print("\n--- Step 2: Initializing ClearML Task ---")
    print("Connecting to server (Timeout set to 5 seconds)...")
    
    task = Task.init(
        project_name="Nirmesh-18-Aug", 
        task_name="Minimal Network Test"
    )
    
    print("\n--- Step 3: Connection Successful! ---")
    logger = task.get_logger()
    logger.report_text("Network verification test completed successfully.")
    
    task.close()
    print("Task closed properly.")

except Exception as e:
    print(f"\n[!] Connection Failed: {e}")
    print("Please verify your port-forwarding or host file entries.")
