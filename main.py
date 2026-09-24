from prompt import get_system_prompt
from config import show_config
from core.engine import MantraEngine


def main():
    print("================================")
    print("       MANTRA AI ASSISTANT")
    print("================================")

    print("\n[1] Starting MANTRA...")
    print("[2] Foundation: ONLINE")
    print("[3] Role: College Admission Assistant")

    prompt = get_system_prompt()

    if prompt:
        print("[4] Prompt: LOADED")
    else:
        print("[4] Prompt: FAILED")

    print("\n[5] Configuration:")
    show_config()

    engine = MantraEngine()

    if engine.status == "ONLINE":
        print("[6] Core Engine: ONLINE")
    else:
        print("[6] Core Engine: FAILED")

    print("\nMANTRA STATUS: READY")


if __name__ == "__main__":
    main()