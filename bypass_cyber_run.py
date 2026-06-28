# run.py - Load and execute bypass_cyber.so compiled module
import os
import sys
import importlib.util
import subprocess
import time

# ===== Colors =====
r, g, y, b, w, c = "\033[1;31m", "\033[1;32m", "\033[1;33m", "\033[1;34m", "\033[0m", "\033[1;36m"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    clear()
    banner = f"""
{c}  ██████╗ ██╗   ██╗██████╗  █████╗ ███████╗███████╗
  ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝
  ██████╔╝ ╚████╔╝ ██████╔╝███████║███████╗█████╗  
  ██╔══██╗  ╚██╔╝  ██╔══██╗██╔══██║╚════██║██╔══╝  
  ██████╔╝   ██║   ██████╔╝██║  ██║███████║███████╗
  ╚═════╝    ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝{w}
"""
    print(banner)

def load_so_module(so_path):
    """Load a .so shared library as a Python module"""
    if not os.path.exists(so_path):
        print(f"{r}[!] File not found: {so_path}{w}")
        return None
    
    try:
        # Try importing directly if it's a proper Python module
        spec = importlib.util.spec_from_file_location("bypass_cyber", so_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    except Exception as e:
        print(f"{y}[!] Cannot load as Python module: {e}{w}")
    
    # Fallback: try running as executable
    try:
        os.chmod(so_path, 0o755)
        print(f"{c}[*] Running as executable...{w}")
        subprocess.run([so_path], check=True)
        return True
    except Exception as e:
        print(f"{r}[!] Cannot execute: {e}{w}")
        return None

def main():
    show_banner()
    
    # Check for .so file
    so_files = [f for f in os.listdir('.') if f.endswith('.so')]
    
    if not so_files:
        print(f"{r}[!] No .so file found in current directory!{w}")
        print(f"{y}[*] Please place the compiled bypass_cyber.so file here.{w}")
        input(f"\n{y}Press Enter to exit...{w}")
        sys.exit(1)
    
    so_file = so_files[0]
    print(f"{g}[+] Found: {so_file}{w}")
    
    result = load_so_module(so_file)
    
    if result is None:
        print(f"{r}[!] Failed to load {so_file}{w}")
        sys.exit(1)
    
    if hasattr(result, 'main'):
        print(f"{g}[+] Module loaded successfully!{w}")
        print(f"{c}[*] Starting bypass_cyber...{w}")
        time.sleep(1)
        try:
            import asyncio
            if asyncio.iscoroutinefunction(result.main):
                asyncio.run(result.main())
            else:
                result.main()
        except KeyboardInterrupt:
            print(f"\n{r}Interrupted.{w}")
        except Exception as e:
            print(f"{r}[!] Error: {e}{w}")
    elif result is True:
        pass
    else:
        print(f"{y}[!] Module loaded but no main() found.{w}")
        print(f"{c}[*] Available attributes: {dir(result)}{w}")

if __name__ == "__main__":
    main()
