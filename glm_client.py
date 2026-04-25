import os
import httpx
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

    # Use a custom httpx client with a long timeout to handle slow proxy responses
    http_client = httpx.Client(
        timeout=httpx.Timeout(
            connect=10.0,
            read=180.0,    # 3 minutes read timeout — handles slow GLM responses
            write=10.0,
            pool=10.0,
        )
    )

    client = anthropic.Anthropic(
        api_key=api_key,
        base_url=base_url,
        http_client=http_client,
    )
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
    """Streaming kept as fallback but not used by default."""
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