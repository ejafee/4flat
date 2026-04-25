import os
import anthropic
from dotenv import load_dotenv

load_dotenv()


def _get_client_and_model():
    api_key = os.getenv("ANTHROPIC_AUTH_TOKEN")
    base_url = os.getenv("ANTHROPIC_BASE_URL")
    model = os.getenv("ANTHROPIC_MODEL")

    if not api_key:
        return None, None, "Error: ANTHROPIC_AUTH_TOKEN not set in .env"
    if not base_url:
        return None, None, "Error: ANTHROPIC_BASE_URL not set in .env"
    if not model:
        return None, None, "Error: ANTHROPIC_MODEL not set in .env"

    client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
    return client, model, None


def get_strategy(system_prompt, user_prompt):
    try:
        client, model, err = _get_client_and_model()
        if err:
            return err

        response = client.messages.create(
            model=model,
            max_tokens=3000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        return response.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"


def stream_strategy(system_prompt, user_prompt):
    try:
        client, model, err = _get_client_and_model()
        if err:
            yield err
            return

        with client.messages.stream(
            model=model,
            max_tokens=3000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        ) as stream:
            for text in stream.text_stream:
                yield text
    except Exception as e:
        yield f"\n\nError: {str(e)}"
