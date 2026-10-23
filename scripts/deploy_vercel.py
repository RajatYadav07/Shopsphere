import os
import re
import subprocess
import sys

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_env_path = os.path.join(root_dir, "backend", ".env")
    
    if not os.path.exists(backend_env_path):
        print("Error: backend/.env not found")
        sys.exit(1)
        
    with open(backend_env_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    m = re.search(r"MONGODB_URI=(.*)", content)
    if not m:
        print("Error: MONGODB_URI not found in backend/.env")
        sys.exit(1)
    uri = m.group(1).strip()
    
    node_exe = r"C:\Program Files\nodejs\node.exe"
    vercel_js = r"C:\Users\rajat\AppData\Local\npm-cache\_npx\69f9afb961c37556\node_modules\vercel\dist\index.js"
    
    cmd = [
        node_exe,
        vercel_js,
        "deploy",
        "--temporary",
        "--yes",
        "--env",
        f"MONGODB_URI={uri}",
        "--env",
        "DATABASE_NAME=shopsphere_olist",
        "--env",
        "ENVIRONMENT=production"
    ]
    
    print("Starting Vercel direct node deployment...")
    env = os.environ.copy()
    extra_paths = [
        os.path.join(root_dir, "backend", "venv", "Scripts"),
        r"C:\Flutter-1\src\flutter\bin\mingit\cmd",
        r"C:\Users\rajat\AppData\Local\Microsoft\WinGet\Packages\GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe\bin"
    ]
    env["PATH"] = ";".join(extra_paths) + ";" + env.get("PATH", "")
    
    proc = subprocess.Popen(
        cmd,
        cwd=root_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env
    )
    
    for line in proc.stdout:
        if "mongodb+srv" in line:
            print("[DEPLOY] (sensitive env line hidden)")
        else:
            sys.stdout.write(line)
            sys.stdout.flush()
            
    proc.wait()
    print(f"Process exited with code {proc.returncode}")
    sys.exit(proc.returncode)

if __name__ == "__main__":
    main()
