"""Lab 01 check: confirm .env is readable without printing the full API key."""

from lab02_desk import load_dotenv


values = load_dotenv()
api_key = values.get("API_KEY", "")
user_agent = values.get("SEC_USER_AGENT", "")

if not api_key or not user_agent:
    raise SystemExit("Missing API_KEY or SEC_USER_AGENT in .env")

print(f"{api_key[:4]}...")
print(user_agent)
