import os
import anthropic
from dotenv import load_dotenv

load_dotenv()


def get_strategy(system_prompt, user_prompt):
    try:
        api_key = os.getenv("ANTHROPIC_AUTH_TOKEN")
        base_url = os.getenv("ANTHROPIC_BASE_URL")
        model = os.getenv("ANTHROPIC_MODEL")

        if not api_key:
            return "Error: ANTHROPIC_AUTH_TOKEN not set in .env"
        if not base_url:
            return "Error: ANTHROPIC_BASE_URL not set in .env"
        if not model:
            return "Error: ANTHROPIC_MODEL not set in .env"

        client = anthropic.Anthropic(api_key=api_key, base_url=base_url)

        response = client.messages.create(
            model=model,
            max_tokens=3000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        return response.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"
