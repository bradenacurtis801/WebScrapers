from services.summarizeText import get_summary
import openai  # OpenAI's Python package for accessing the GPT models

def _test(file_path):
    """
    This is a test feature that may or may not be implemented -- just an idea.
    
    The function processes a meeting transcript to:
    1. Identify interactions directed towards "Scribe" (e.g., "Scribe, do something").
    2. Use the GPT model to generate corresponding responses to these interactions.
    3. Produce a structured summary of the entire transcript.
    4. Append the interactions with "Scribe" and the GPT model's responses to the end of the summary.
    
    The goal is to provide an enhanced summary that includes not just the main points of the meeting, 
    but also specific interactions with the virtual scribe.

    Args:
        file_path (str): Path to the meeting transcript file.

    Returns:
        str: A structured summary with integrated "Scribe" interactions and responses.
    """
    # Parse the transcript for mentions of "Scribe"
    scribe_interactions = parse_transcript_for_scribe_commands(file_path)

    # Generate the structured summary
    structured_summary_text = get_summary(file_path)

    # Add the interactions with Scribe to the end of the summary
    for speaker, command, response in scribe_interactions:
        structured_summary_text += f"\nResponse to {speaker}'s question '{command}':\n- {response}\n"

    return structured_summary_text


def get_response(command):
    # Create a prompt for the GPT model
    prompt = f"Question: {command}\nAnswer:"
    
    # Get the model's response
    response = get_gpt_response(prompt, max_tokens=150)

    return response


def parse_transcript_for_scribe_commands(file_path):
    with open(file_path, 'r') as file:
        transcript = file.readlines()

    interactions = []

    for line in transcript:
        if "Scribe," in line:
            # Extract the speaker's name
            speaker = line.split(":")[0].strip()

            # Extract the command/question after "Scribe,"
            command = line.split("Scribe,")[1].strip()

            # Get a response for the command
            response = get_response(command)
            interactions.append((speaker, command, response))

    return interactions


def get_gpt_response(prompt_or_messages, max_tokens=None):
    if isinstance(prompt_or_messages, str):
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt_or_messages,
            max_tokens=max_tokens
        )
        return response.choices[0].text
    elif isinstance(prompt_or_messages, list):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt_or_messages
        )
        return response.choices[0].message['content']

    raise ValueError("Invalid input to get_gpt_response.")