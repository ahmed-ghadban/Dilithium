import subprocess

def run_python_script(script_path, *args):
    try:
        result = subprocess.run(['python', script_path, *args], capture_output=True, text=True, check=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"Error: Script not found at {script_path}")
        return None
    except Exception as e: 
        print(f"An unexpected error occurred: {e}")
        return None


script_path = "dilithium_py/main.py"  
arguments = ["arg1", "arg2"]  

result = run_python_script(script_path, *arguments)

if result:  
    print("Program executed successfully.")
    print("Stdout:", result.stdout)
    print("Stderr:", result.stderr)
    print("Return code:", result.returncode)
else:
    print("Program execution failed.")

result = run_python_script(script_path)
if result:
  pass