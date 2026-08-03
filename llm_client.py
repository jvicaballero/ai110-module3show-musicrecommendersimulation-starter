import os


class MockClient:
    """
    Offline stand-in for an LLM client.
    Lets the app run without an API key, and lets tests/demos exercise the
    retry/guardrail path deterministically (this response is intentionally
    not valid JSON).
    """

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        return "Sure! Here are some great K-pop songs for you."


class GeminiClient:
    """
    Minimal Gemini API wrapper with added error resilience.

    Requirements:
    - google-genai installed
    - GEMINI_API_KEY set in environment (or loaded via python-dotenv)
    """

    def __init__(self, model_name: str = "gemini-flash-lite-latest", temperature: float = 0.4):
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                "Missing GEMINI_API_KEY. Create a .env file and set GEMINI_API_KEY=..."
            )

        # Import here so offline/Mock mode never requires the dependency.
        from google import genai
        from google.genai import types

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.temperature = float(temperature)
        self._config_types = types

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """
        Sends a single request to Gemini.

        If an error occurs, returns an empty string, which the caller's
        validation logic treats as a failed attempt and retries.
        """
        try:
            merged_prompt = f"{system_prompt}\n\n{user_prompt}".strip()
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=merged_prompt,
                # Temperature controls sampling randomness: near 0 the model keeps
                # picking the single most-likely (most "obvious"/famous) answer for
                # a given prompt, so identical prompts return near-identical songs;
                # higher values let it sample less-dominant but still plausible
                # answers, trading some consistency/validity for variety.
                config=self._config_types.GenerateContentConfig(temperature=self.temperature),
            )
            # Defensive: response.text can be None if blocked by safety filters.
            return response.text or ""
        except Exception:
            return ""
