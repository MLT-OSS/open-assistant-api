import pytest
import openai

@pytest.fixture(name="client")
def client_for_test():
    """
    a openai client connected to local server for test
    """
    return openai.OpenAI(base_url="http://localhost:8086/api/v1", api_key="ml-xxx")

