import os 
from dotenv import load_dotenv

load_dotenv()

groq_APIs = [
    "API1", "API2", "API3",
    "API4", "API5", "API6",
]

def switch_API(current_api):
    """Switches to the next API in the list, excluding empty ones."""
    valid_APIs = []
    for api in groq_APIs:
        api_value = os.environ.get(api, None)
        if api_value != "":
            valid_APIs.append(api)
    current_api_index = valid_APIs.index(current_api)
    next_api_index = (current_api_index + 1) % len(valid_APIs)
    new_api = valid_APIs[next_api_index]
    print(f"API Changed! : {new_api}")
    return new_api