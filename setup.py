import os
import subprocess
import sys

# Define the path to your cloned repository
repo_dir = "AI-WritingAssistant-API"  # Path to the cloned repository
env_dir = "venv"  # Virtual environment directory

# Step 1: Check if the repository exists (you manually cloned it)
if not os.path.exists(repo_dir):
    raise FileNotFoundError(f"The repository directory '{repo_dir}' does not exist. Please clone the repository manually.")

# Step 2: Create a virtual environment if it doesn't exist
if not os.path.exists(env_dir):
    print(f"Creating virtual environment in {env_dir}...")
    subprocess.check_call([sys.executable, "-m", "venv", env_dir])
else:
    print("Virtual environment already exists.")

# Step 3: Install the dependencies from requirements.txt
def install_requirements():
    print("Installing dependencies from requirements.txt...")
    requirements_path = os.path.join(repo_dir, "requirements.txt")
    if not os.path.exists(requirements_path):
        raise FileNotFoundError(f"requirements.txt not found in the repository. Please ensure it exists.")
    
    subprocess.check_call([os.path.join(env_dir, "bin", "pip"), "install", "-r", requirements_path])

install_requirements()

# Step 4: Run FastAPI app using Uvicorn with nohup to make it persistent
def run_fastapi_app():
    print("Running FastAPI app with Uvicorn (in the background)...")
    
    # Command to run FastAPI app using uvicorn (adjust if needed)
    command = [
        "nohup",
        os.path.join(env_dir, "bin", "uvicorn"),
        "main:app",  # Replace with your actual entry point
        "--host", "0.0.0.0",
        "--port", "8000",
        "&"
    ]
    
    # Run the FastAPI app in the background
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

run_fastapi_app()
