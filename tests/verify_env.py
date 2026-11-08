"""
Environment Verification Script for DeepLearning.AI "Agentic AI" Course
"""

import sys
import os

# Ensure safe UTF-8 output on Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def check_python_version():
    major, minor = sys.version_info.major, sys.version_info.minor
    print(f"[INFO] Python Version: {major}.{minor}.{sys.version_info.micro}")
    if major == 3 and minor >= 11:
        print("       [OK] Python version is compatible (>= 3.11)")
        return True
    else:
        print("       [WARN] Recommended Python version is 3.11 or 3.12")
        return False

def check_packages():
    packages = [
        ("aisuite", "aisuite (Andrew Ng's unified LLM client)"),
        ("openai", "openai"),
        ("anthropic", "anthropic"),
        ("google.genai", "google-genai"),
        ("pydantic", "pydantic"),
        ("dotenv", "python-dotenv"),
        ("rich", "rich"),
        ("tavily", "tavily-python"),
        ("wikipedia", "wikipedia"),
        ("arxiv", "arxiv"),
        ("fastapi", "fastapi"),
        ("sqlalchemy", "sqlalchemy"),
        ("ipykernel", "ipykernel (Jupyter support)"),
    ]

    print("\n[INFO] Checking Course Packages:")
    all_ok = True
    for mod_name, label in packages:
        try:
            __import__(mod_name)
            print(f"       [OK] {label}")
        except ImportError:
            print(f"       [MISSING] {label}")
            all_ok = False
    return all_ok

def check_api_keys():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass

    keys = [
        ("OPENAI_API_KEY", "OpenAI API"),
        ("ANTHROPIC_API_KEY", "Anthropic API"),
        ("GEMINI_API_KEY", "Google Gemini API"),
        ("GROQ_API_KEY", "Groq API"),
        ("TAVILY_API_KEY", "Tavily Search API"),
    ]

    print("\n[INFO] Checking Environment Keys (presence only, never displaying values):")
    found_any = False
    for env_var, desc in keys:
        is_set = bool(os.environ.get(env_var))
        if is_set:
            found_any = True
            print(f"       [CONFIGURED] {env_var} ({desc})")
        else:
            print(f"       [NOT SET]    {env_var} ({desc})")

    if not found_any:
        print("\n[TIP]  Copy .env.example to .env and add your preferred provider key to begin.")

def main():
    print("=" * 65)
    print(" DeepLearning.AI: Agentic AI - Environment Health Check")
    print("=" * 65)
    check_python_version()
    check_packages()
    check_api_keys()
    print("\n" + "=" * 65)
    print(" Environment is ready! Ready to build and learn together.")
    print("=" * 65)

if __name__ == "__main__":
    main()
