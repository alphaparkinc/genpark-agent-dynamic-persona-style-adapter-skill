"""MCP Server for Agent Dynamic Persona Style Adapter."""
import sys
import json
import time
from client import AgentDynamicPersonaStyleAdapter

adapter = AgentDynamicPersonaStyleAdapter()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "adapt_agent_communication_style":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "adapt_message_style")
    if action == "adapt_message_style":
        return adapter.adapt_message_style(
            raw_message=args.get("raw_message", "Hello!"),
            channel=args.get("channel", "SLACK_CHAT"),
            user_cognitive_load=args.get("user_cognitive_load", "MEDIUM"),
            target_persona=args.get("target_persona")
        )
    elif action == "classify_channel_constraints":
        return adapter.classify_channel_constraints(args.get("channel", "SLACK_CHAT"))
    elif action == "get_persona_profiles":
        return adapter.get_persona_profiles()
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        long_msg = "Hey! We just processed the transaction for $45.99 at Whole Foods and the delivery ETA is 2:30 PM today. Let me know if you need any adjustments!"
        res = adapter.adapt_message_style(long_msg, channel="SMART_GLASSES_AUDIO", user_cognitive_load="HIGH")
        assert res["adapted_word_count"] <= 20
        assert res["compression_ratio"] < 1.0
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "AgentDynamicPersonaStyleAdapter", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "adapt_agent_communication_style",
                            "description": "Adapt communication persona: adjust brevity, formality, and technical depth according to channel type, user cognitive load, and feedback sentiment.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["adapt_message_style", "classify_channel_constraints", "get_persona_profiles"]},
                                    "raw_message": {"type": "string"},
                                    "channel": {"type": "string"},
                                    "user_cognitive_load": {"type": "string"},
                                    "target_persona": {"type": "string"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
