"""
Dynamic Agent Persona & Communication Style Adapter (Zero External Dependencies)
Provides rule-based contextual message transformation for audio, push, chat, and email channels.
"""
import time
import math
import hashlib
import json
import re
from typing import Dict, Any, List, Optional

CHANNEL_PROFILES = {
    "SMART_GLASSES_AUDIO": {"max_words": 20, "speech_optimized": True, "bullet_allowed": False},
    "MOBILE_PUSH": {"max_words": 30, "speech_optimized": False, "bullet_allowed": False},
    "SLACK_CHAT": {"max_words": 100, "speech_optimized": False, "bullet_allowed": True},
    "EXECUTIVE_EMAIL": {"max_words": 300, "speech_optimized": False, "bullet_allowed": True}
}

class AgentDynamicPersonaStyleAdapter:
    def __init__(self):
        pass

    def adapt_message_style(
        self,
        raw_message: str,
        channel: str = "SLACK_CHAT",
        user_cognitive_load: str = "MEDIUM",
        target_persona: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Dynamically adjusts message verbosity, tone, and formatting.
        For high cognitive load or audio, compresses message to core actionable signal.
        """
        profile = CHANNEL_PROFILES.get(channel, CHANNEL_PROFILES["SLACK_CHAT"])
        max_words = profile["max_words"]

        # If user cognitive load is high, cut word budget in half
        if user_cognitive_load.upper() == "HIGH":
            max_words = max(10, int(max_words * 0.5))

        words = raw_message.split()
        original_word_count = len(words)

        adapted_text = raw_message

        # Compression if exceeding budget
        if len(words) > max_words:
            # Extract first sentence or core clause
            sentences = re.split(r"(?<=[.!?])\s+", raw_message)
            candidate = ""
            for s in sentences:
                if len((candidate + " " + s).split()) <= max_words:
                    candidate = (candidate + " " + s).strip()
                else:
                    break
            if not candidate:
                candidate = " ".join(words[:max_words]) + "..."
            adapted_text = candidate

        # Channel specific adjustments
        if channel == "SMART_GLASSES_AUDIO":
            # Strip markdown links and formatting for clean TTS speech
            adapted_text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", adapted_text)
            adapted_text = re.sub(r"[*_#`]", "", adapted_text)
        elif channel == "MOBILE_PUSH":
            # Ensure punchy action verb format
            if not adapted_text.endswith((".", "!", "?")):
                adapted_text += "."

        return {
            "channel": channel,
            "user_cognitive_load": user_cognitive_load,
            "target_persona": target_persona or "BALANCED_COPILOT",
            "original_word_count": original_word_count,
            "adapted_word_count": len(adapted_text.split()),
            "compression_ratio": round(len(adapted_text.split()) / max(1, original_word_count), 2),
            "adapted_text": adapted_text
        }

    def classify_channel_constraints(self, channel: str) -> Dict[str, Any]:
        return CHANNEL_PROFILES.get(channel, CHANNEL_PROFILES["SLACK_CHAT"])

    def get_persona_profiles(self) -> Dict[str, Any]:
        return {
            "channels": list(CHANNEL_PROFILES.keys()),
            "cognitive_load_states": ["HIGH", "MEDIUM", "LOW"]
        }
