import subprocess
import sys

app_path = "./HOME.py"  # Replace with the correct path to your app.py

# Run the Streamlit app using subprocess
try:
    print("Opening Streamlit app...")
    input("Press Enter To Continue...")  # Pausing to allow user to continue
    result = subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], 
                            check=True, capture_output=True, text=True)
    # If the subprocess completes without error, print the standard output
    print(result.stdout)

except subprocess.CalledProcessError as e:
    # In case of an error, capture stderr and print it
    print("Error encountered while running Streamlit app:")
    print(e.stderr)
