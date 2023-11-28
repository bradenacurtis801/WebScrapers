import time
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from common.js_injection_strings import *
from common.decorators import *
import datetime
import glob
import os
import shutil
import stat


@deprecated
def safe_action(driver, func=None, by=None, value=None, action=None, element=None, args=None, timeout=60, sleep_interval=2, exceptions=(ElementNotInteractableException, NoSuchElementException), single_try=False):
    """
    Attempts to perform a given action multiple times until successful or a timeout is reached.

    Parameters:
    - driver: The selenium webdriver instance.
    - func: A specific function or method to be executed (e.g., WebElement.send_keys).
    - by: The selenium locator strategy (e.g., By.XPATH).
    - value: The value for the selenium locator strategy (e.g., "//div[@class='some_class']").
    - action: A specific string action if wanting to dynamically call a WebElement method (e.g., 'click').
    - element: A specific WebElement instance.
    - args: Additional arguments for the function or method specified by 'func'.
    - timeout: Maximum time (in seconds) to retry the action.
    - sleep_interval: Time (in seconds) to wait between retries.
    - exceptions: Exceptions to catch.

    Returns:
    - WebElement if a locator strategy was provided and element was found. None otherwise.

    This function is useful to ensure resilience against transient issues when interacting with web elements, such as dynamically loaded content.
    """
    end_time = time.time() + timeout
    last_exception = None

    while time.time() < end_time:
        try:
            if by and value:
                element = driver.find_element(by, value)
                if action:
                    getattr(element, action)()
                return element
            elif element and func:
                if args:
                    func(*args)
                else:
                    func()
                return
        except exceptions as e:
            last_exception = e
            print(f"Error encountered: {e}. Retrying...")
            if single_try:
                break  # Exit the loop immediately if single_try is True
            time.sleep(sleep_interval)

    # After the loop is done and if no action was successful
    print(
        f"Failed to execute action after {timeout} seconds due to: {last_exception}")
    raise last_exception


def get_meeting_url(driver, timeout=5):
    """
    Injects a custom input field on the current webpage for the user to manually input a meeting URL.

    Parameters:
    - driver: The selenium webdriver instance.
    - timeout: Time (in seconds) to check if the page has refreshed before injecting the input.

    Returns:
    - The URL string entered by the user.

    Useful when the meeting URL cannot be obtained programmatically and requires user intervention.
    """

    # Wait for a specific element that signifies the page has loaded
    # Replace with the actual locator
    expected_element_locator = (By.CSS_SELECTOR, HOME_PAGE_LOADED)
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(expected_element_locator)
    )

    driver.execute_script(GET_MEETING_URL_SCRIPT)

    # Wait for the user to input a URL and submit it
    WebDriverWait(driver, 300).until(lambda d: d.execute_script(
        'return typeof window.meetingURL !== "undefined";'))

    # Fetch the URL entered by the user directly from the JavaScript variable
    meeting_url = driver.execute_script('return window.meetingURL;')

    return meeting_url


def _write_to_file(path, content, mode):
    with open(path, mode) as file:
        file.write(content)


def sessionStart_write(path):
    # Write the header to the file before entering the scraping loop
    now = datetime.datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    content = f"\n\n=====================================\nCaptured at: {formatted_date_time}\n\n"
    _write_to_file(path, content, mode='a')


def sessionEnd_write(path):
    # Write the header to the file before entering the scraping loop
    now = datetime.datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    content = f"\n\n=====================================\nSession ended at: {formatted_date_time}\n\n"
    _write_to_file(path, content, mode='a')


def write_summary_to_file(filepath, summary_text):
    content = "Meeting Summary:\n================\n" + summary_text
    _write_to_file(filepath, content, mode='w')


def cleanup_temp_files():
    """
    Cleans up temporary files generated during the summarization process.
    NOTE: This assumes that temp files are stored in ./temp/
    """
    if os.path.exists('temp\\temp_combined_summaries.txt'):
        os.remove('temp\\temp_combined_summaries.txt')
    for chunk_file in glob.glob('temp\\temp_chunk_*.txt'):
        os.remove(chunk_file)


def delete_folder(folder_path):
    """
    Delete the specified folder and its contents.

    Args:
    - folder_path (str): Path to the folder to be deleted.

    Raises:
    - FileNotFoundError: If the specified folder does not exist.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"'{folder_path}' does not exist.")

    shutil.rmtree(folder_path)


def force_delete_folder(folder_path):
    # Function to override permissions and delete a file
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(folder_path, onerror=remove_readonly)


def add_to_path(folder_path):
    """
    Add the specified folder path to the system's PATH variable.

    Args:
    - folder_path (str): Path to the folder to be added to PATH.
    """
    # Get the current PATH
    current_path = os.environ.get('PATH', '')

    # Add folder_path to the PATH if it's not already present
    if folder_path not in current_path:
        os.environ['PATH'] = folder_path + os.pathsep + current_path


def remove_from_path(folder_path):
    """
    Remove the specified folder path from the system's PATH variable.

    Args:
    - folder_path (str): Path to the folder to be removed from PATH.
    """
    # Get the current PATH
    current_path = os.environ.get('PATH', '')

    # Remove folder_path from the PATH
    os.environ['PATH'] = os.pathsep.join(
        [path for path in current_path.split(os.pathsep) if path != folder_path])


def log_participant_updates(filepath, participants, action):
    for participant in participants:
        _log_participant_event(filepath, participant, action)


def _log_participant_event(filepath, participant, event):
    """
    Helper Funciton
    Log the event of a participant joining or leaving.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    event_message = f"{participant} {event} at {timestamp}\n"
    print(event_message)  # Print to console
    with open(filepath, 'a') as file:  # Append to the file
        file.write(event_message)


def save_transcription_to_file(filepath, speaker_name, caption_text):
    with open(filepath, 'a') as file:
        file.write(f"{speaker_name}: {caption_text}\n")


def create_directory(directory_path):
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        return True
    except Exception:
        return False


def save_summary_to_file(filepath, summary):
    with open(filepath, 'w') as file:
        file.write(summary)


def check_participants_changes(current_participants, previous_participants):
    """Check for any new participants who joined or existing ones who left, and return the changes."""
    joined = current_participants - previous_participants
    left = previous_participants - current_participants

    return joined, left
