import re
import json

def extract_json_from_response(text: str) -> dict or list:
    """
    Extracts a JSON object or list from a string, even if it's wrapped
    in markdown code blocks.
    """
    if not isinstance(text, str):
        return text # Return as-is if already parsed

    # Pattern to find JSON within ```json ... ``` blocks
    match = re.search(r'```(json)?\s*([\s\S]*?)\s*```', text)
    if match:
        text_to_parse = match.group(2)
    else:
        text_to_parse = text

    # Sanitize the string to remove invalid escape sequences
    text_to_parse = text_to_parse.replace("\\'", "'")

    try:
        # Attempt to parse the cleaned text
        return json.loads(text_to_parse.strip())
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        # As a last resort, try to find the first '{' and last '}'
        try:
            start = text_to_parse.find('{')
            end = text_to_parse.rfind('}') + 1
            if start != -1 and end != 0:
                return json.loads(text_to_parse[start:end])
        except json.JSONDecodeError:
            # If all parsing fails, raise the error to be handled by the agent
            raise ValueError(f"Could not parse JSON from response: {text}")
    
    raise ValueError(f"Could not find valid JSON in response: {text}")
