import os 
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

groq_APIs = [
    os.environ.get("API1"),
    os.environ.get("API2"),
    os.environ.get("API3"),
    os.environ.get("API4"),
    os.environ.get("API5"),
    os.environ.get("API6"),
]

# Remove empty or None keys from the list
groq_APIs = [api for api in groq_APIs if api]

def switch_API(current_api):
    """Switches to the next API in the list, excluding empty ones."""
    if current_api not in groq_APIs:
        print("Current API is not valid.")
        return None  # Or handle the case of an invalid current API gracefully
    current_api_index = groq_APIs.index(current_api)
    next_api_index = (current_api_index + 1) % len(groq_APIs)
    new_api = groq_APIs[next_api_index]
    return new_api