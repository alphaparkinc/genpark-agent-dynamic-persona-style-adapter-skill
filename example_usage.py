"""Example usage for AgentDynamicPersonaStyleAdapter."""
import sys
import json
from client import AgentDynamicPersonaStyleAdapter

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Agent Dynamic Persona & Style Adapter Demo ===")
    adapter = AgentDynamicPersonaStyleAdapter()

    base_report = (
        "Good morning! Your Q3 Strategic Revenue Report was completed by WorkBuddy with 42% YoY growth. "
        "The presentation slides and Excel models have been verified with 100% cryptographic Merkle proofs "
        "and are waiting for your executive sign-off before the 2:00 PM board sync."
    )

    # 1. Smart Glasses Audio (Meta Ray-Ban / Muse)
    print("\n--- 1. Adapting for Ray-Ban Smart Glasses (Whisper Audio) ---")
    audio = adapter.adapt_message_style(base_report, channel="SMART_GLASSES_AUDIO", user_cognitive_load="HIGH")
    print(f"Adapted Text: '{audio['adapted_text']}' ({audio['adapted_word_count']} words)")

    # 2. Mobile Push Notification
    print("\n--- 2. Adapting for Lock-Screen Mobile Push ---")
    push = adapter.adapt_message_style(base_report, channel="MOBILE_PUSH", user_cognitive_load="MEDIUM")
    print(f"Adapted Text: '{push['adapted_text']}' ({push['adapted_word_count']} words)")

    # 3. Full Executive Email
    print("\n--- 3. Adapting for Executive Email Delivery ---")
    email = adapter.adapt_message_style(base_report, channel="EXECUTIVE_EMAIL", user_cognitive_load="LOW")
    print(f"Adapted Text: '{email['adapted_text']}' ({email['adapted_word_count']} words)")

if __name__ == "__main__":
    main()
