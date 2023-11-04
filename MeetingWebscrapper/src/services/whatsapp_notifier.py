from twilio.rest import Client
import json

def _send_whatsapp_message(to, message):
    # Your Twilio account SID and Auth Token
    ACCOUNT_SID = 'YOUR_TWILIO_ACCOUNT_SID'
    AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
    
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # Replace 'whatsapp:+14155238886' with your sandbox number
    message = client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',  # Your sandbox number
        to=f'whatsapp:{to}'  # Recipient's phone number
    )

    return message.sid

def load_participants(file_path):
    """
    Load participants' data from a given JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Parsed data from the JSON file.
    """
    
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

import json

def _policy(file_path):
    """
    Validates the structure and content of a given JSON file against a predefined schema.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        bool: True if the JSON file adheres to the schema, False otherwise.
    """
    
    # Define the expected schema
    schema = {
        "participants": [
            {
                "id": str,
                "name": str,
                "email": str,
                "phone_number": str,
                "whatsapp_number": str,
                "organization": str,
                "position": str,
                "additional_info": dict
            }
        ]
    }
    
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

            # Check if 'participants' key exists and is a list
            if "participants" not in data or not isinstance(data["participants"], list):
                return False

            # Check each participant against the schema
            for participant in data["participants"]:
                if not all(key in participant and isinstance(participant[key], value) for key, value in schema["participants"][0].items()):
                    return False
                type(participant)

            return True

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return False
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False



# Example usage:
is_valid = _policy("participants.json")
if is_valid:
    print("JSON file adheres to the schema.")
else:
    print("JSON file does not adhere to the schema.")

