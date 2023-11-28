

# === src\common\AI_Templates.py ===

# Define a dictionary of templates
templates = {
    'structured_summary': {
        'system': ("You are a helpful assistant. "
                   "Produce a structured summary of the text with the following sections: "
                   "Introduction, Key Points, Decisions Made, Action Items, and Conclusion."),
    },
    'brief_summary': {
        'system': ("You are a helpful assistant. "
                   "Provide a brief summary of the text highlighting the main ideas.")
    },
    'chunk_summary': {
        'system': ("You are a helpful assistant. Summarize this chunk of content for me.")
    }
    # ... add more templates as needed
}

# === src\common\constants.py ===

CHROME_DRIVER_URLS = "https://googlechromelabs.github.io/chrome-for-testing/"
CHROME_SIGNIN_URL = "https://accounts.google.com/signin"
JOIN_BTN = [
    "//button/span[text()='Ask to join']",
    "//button/span[text()='Join now']"
]

EMAIL_LOGIN = "identifierId"
PASSWORD_LOGIN = "input[type='password'][jsname='YPqjbf']"

# Constants for after login
HOME_PAGE_LOADED = "h1.XY0ASe"


# Constants for selectors
PARTICIPANT_ITEM_SELECTOR = 'div[role="listitem"]'
PARTICIPANT_NAME_SELECTOR = 'span.zWGUib'
HOST_INDICATOR_SELECTOR = 'div.d93U2d'
CAPTION_CONTAINER_SELECTOR = 'div[jsname="tgaKEf"]'

# Google Meet UI button selectors
CONTINUE_WITHOUT_MIC_BUTTON_XPATH = "//button[span[text()='Continue without microphone']]"
ASK_TO_JOIN_BUTTON_XPATH = "//button/span[text()='Ask to join']"
JOIN_NOW_BUTTON_XPATH = "//button/span[text()='Join now']"
TURN_ON_CAPTIONS_BUTTON_XPATH = "//button[@aria-label='Turn on captions (c)']"
SHOW_EVERYONE_BUTTON_XPATH = "//button[@aria-label='Show everyone']"

# Google Meet specific selectors
PARTICIPANTS_LIST_SELECTOR = "div[jsname='jrQDbd']"
LEAVE_MEETING_BUTTON_CSS_SELECTOR = "button[jsname='CQylAd']"
SPEAKER_NAME_CSS_SELECTOR = ".zs7s8d.jxFHg"
CAPTIONS_TEXT_CSS_SELECTOR = "div[jsname='tgaKEf'] span[id^='customID_']"

# === src\common\decorators.py ===

import time
import warnings
import functools
from colorama import init, Fore

# Initialize Colorama
init()

def timing_decorator(func):
    """
    A decorator that prints the time a function takes to execute in different colors.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Start the timer
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.perf_counter()  # End the timer
        execution_time = end_time - start_time

        # Define time thresholds for different colors
        thresholds = {
            'red': 5,     # Red for more than 5 seconds
            'yellow': 1,  # Yellow for more than 1 second and less than or equal to 5 seconds
            'green': 0    # Green for 1 second or less
        }

        # Choose the color
        if execution_time > thresholds['red']:
            color = Fore.RED
        elif execution_time > thresholds['yellow']:
            color = Fore.YELLOW
        else:
            color = Fore.GREEN

        # Print the formatted message with the selected color
        print(color + f"{func.__name__} executed in {execution_time:.2f} seconds" + Fore.RESET)
        return result
    return wrapper

def deprecated(func):
    """This is a decorator which can be used to mark functions as deprecated."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn(Fore.YELLOW + f"Call to deprecated function {func.__name__}." + Fore.RESET,
                      category=DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    return new_func

def decorator_record_algorithm_type(func):
    """
    A decorator that records the algorithm or function type used.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Perform the recording here, e.g., by printing or logging
        label = f"Algorithm/Function used: {func.__name__}\n\n"
        print(label)
        # Call the original function
        result = label + func(*args, **kwargs)
        return result
    return wrapper

# === src\common\js_injection_strings.py ===

from common.constants import *


# JS snippet for getting participant names and checking for the host
EXTRACT_PARTICIPANTS = f"""
  var participantsList = document.querySelector('{PARTICIPANTS_LIST_SELECTOR}');
  if (participantsList) {{
    let participants = Array.from(participantsList.querySelectorAll('{PARTICIPANT_ITEM_SELECTOR}')).map(participant => {{
      // Find the name span
      let nameElement = participant.querySelector('{PARTICIPANT_NAME_SELECTOR}');
      let nameText = nameElement ? nameElement.textContent.trim() : '';
  
      // Check if this participant has an additional descriptor indicating they are the host
      let additionalDescriptor = participant.querySelector('{HOST_INDICATOR_SELECTOR}');
      if (additionalDescriptor && additionalDescriptor.textContent.includes('Meeting host')) {{
        nameText += ' (Host)';
      }}
  
      return nameText;
    }}).filter(name => name !== ''); // Filter out any empty names
    return participants;
  }} else {{
    // If the container is not found, return an empty array
    return [];
  }}
"""

GET_MEETING_URL_SCRIPT = """
    if (!document.getElementById('customUrlInput')) {
        var backdrop = document.createElement("div");
        backdrop.style.position = "fixed";
        backdrop.style.top = "0";
        backdrop.style.left = "0";
        backdrop.style.width = "100%";
        backdrop.style.height = "100%";
        backdrop.style.backgroundColor = "rgba(0,0,0,0.7)";
        backdrop.style.zIndex = "9999";
        
        var input = document.createElement("input");
        input.type = "text";
        input.id = "customUrlInput";
        input.placeholder = "Please paste the meeting URL and press Enter";
        
        // Style the input for better visibility
        input.style.position = "fixed";
        input.style.top = "40%";
        input.style.left = "25%";
        input.style.width = "50%";
        input.style.fontSize = "20px";
        input.style.padding = "10px";
        input.style.border = "2px solid black";
        input.style.backgroundColor = "white";
        input.style.zIndex = "10000";

        // Append elements
        document.body.appendChild(backdrop);
        backdrop.appendChild(input);
        input.focus();

        // Blur background
        var bodyChildren = document.body.children;
        for (var i = 0; i < bodyChildren.length; i++) {
            if (bodyChildren[i] != backdrop) {
                bodyChildren[i].style.filter = "blur(5px)";
            }
        }

        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                window.meetingURL = input.value;
                input.style.display = "none";
                backdrop.remove();
                for (var i = 0; i < bodyChildren.length; i++) {
                    bodyChildren[i].style.filter = "";
                }
            }
        });
    }
    """


def js_inject_ids_script(last_id):
    # Note: Make sure you correctly handle the string conversion of last_id.
    return f"""
    var container = document.querySelector('{CAPTION_CONTAINER_SELECTOR}');
    if (container) {{
        var lastID = {last_id};
        var spans = container.querySelectorAll("span");
        for (var i = 0; i < spans.length; i++) {{
            if (!spans[i].id) {{
                lastID++;
                spans[i].id = "customID_" + lastID;
            }}
        }}
    }}
    """


# === src\common\utils.py ===

import time
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from services.summarizeText import *
from common.js_injection_strings import *
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
    """Log the event of a participant joining or leaving."""
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


def generate_summary(filepath):
    # Assuming get_summary() is a function that generates a summary from the file
    return get_summary(filepath, template_type='structured_summary')


def save_summary_to_file(filepath, summary):
    with open(filepath, 'w') as file:
        file.write(summary)


def check_participants_changes(current_participants, previous_participants):
    """Check for any new participants who joined or existing ones who left, and return the changes."""
    joined = current_participants - previous_participants
    left = previous_participants - current_participants

    return joined, left


# === src\common\__init__.py ===



# === src\Drivers\getDriver.py ===

import platform
import requests
from bs4 import BeautifulSoup
import os
import zipfile
import re
import shutil

def get_chromedriver_url(URL):
    html_content = requests.get(URL).text 
    soup = BeautifulSoup(html_content, 'html.parser')
    
    os_name = platform.system().lower()
    arch = platform.architecture()[0]
    
    if os_name == "windows":
        if arch == "64bit":
            os_key = "win64"
        else:
            os_key = "win32"
    elif os_name == "darwin":  # macOS
        if platform.machine() == "arm64":
            os_key = "mac-arm64"
        else:
            os_key = "mac-x64"
    elif os_name == "linux":
        os_key = "linux64"  # assuming no support for 32-bit Linux
    else:
        raise ValueError("Unsupported OS")
    
    # Find the section with id="Stable"
    section = soup.find("section", id="stable")
    
    # Define a regex pattern to find the desired URL
    pattern = re.compile(f'https.*{os_key}.*chromedriver.*\.zip')
    # Find the <code> tag containing the URL
    url_code_tag = section.find("code", string=pattern)
    
    if url_code_tag:
        return url_code_tag.text
    raise ValueError("Driver URL not found for the architecture")
def download_chromedriver(url, download_path="src/Drivers/chromedriver.zip", extract_path="src/Drivers/"):
    response = requests.get(url)
    with open(download_path, 'wb') as file:
        file.write(response.content)
    try:
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            extracted_file_names = zip_ref.namelist()
            zip_ref.extractall(extract_path)
    except PermissionError:
        print("Permission error while extracting. Please ensure you have the necessary permissions.")
    
    os.remove(download_path)  # Remove the zip file after extraction
    # Return the full path to the extracted chromedriver
    exeFolder = extracted_file_names[1].split('/')[0]
    return os.path.abspath(os.path.join(extract_path, exeFolder))

# === src\Drivers\__init__.py ===



# === src\exceptions\base_exceptions.py ===



# === src\exceptions\scraper_exceptions.py ===

class FailedInitializationError(Exception):
    """Raised when there's a problem during the initialization process."""

class LoginError(Exception):
    """Raised during login failures."""

class BrowserWindowError(Exception):
    """Raised when there's an issue with the browser window."""
    
class NavigationError(Exception):
    """Raised when navigation to a specific URL fails."""

class LoginFieldNotFoundError(Exception):
    """Raised when login fields cannot be located."""

class LoginActionError(Exception):
    """Raised when an action during the login sequence fails."""


# === src\exceptions\__init__.py ===



# === src\main.py ===

# from scraper.meet_scraper_revised import GoogleMeetScraper
from scraper.meet_scraper import GoogleMeetScraper
from services.summarizeText import *
import os

DUMMY_EMAIL = os.environ.get('DUMMY_EMAIL')
DUMMY_PASSWORD = os.environ.get('DUMMY_PASSWORD')  # Assuming you've set this
def app():
    # Enable all deprecation warnings.
    warnings.simplefilter('default', DeprecationWarning)
    classname = "PrasadsClass"
    base_directory = "C:\\Users\\Braden\\OneDrive - Utah Valley University\\Desktop\\PrasadsClass\\LectureNotes"
    driver = GoogleMeetScraper(DUMMY_EMAIL,DUMMY_PASSWORD)
    driver.initialize_driver()
    driver.run_scraper(base_directory,classname)

def main():
    # normal startup (with webscrapping)
    app()
    
    # ######################## Testing AI API functionality with large text files. Currently trying different approaches i.e. chunk summary and window sliding techinque #################################
    # # Path to your text file
    # file_path = "C:/Users/Braden/OneDrive - Utah Valley University/Desktop/PrasadsClass/LectureNotes/PrasadsClass_2023-11-04/PrasadsClass_2023-11-04.txt"

    # # Call the function
    # summarized_text = chunkAndSummarize(file_path, template_type='structured_summary')

    # # Print the summarized text
    # print(summarized_text)
    
    # myInstance = GoogleMeetScraper(DUMMY_EMAIL,DUMMY_PASSWORD)
    
if __name__ == '__main__':
    main()

# === src\scraper\meet_scraper.py ===

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, WebDriverException, TimeoutException
from selenium import webdriver
from services.summarizeText import get_summary
import time
from time import sleep
import os
import sys
import datetime
from common.utils import *
from common.js_injection_strings import *
from common.constants import *
from Drivers.getDriver import get_chromedriver_url, download_chromedriver
from exceptions.scraper_exceptions import FailedInitializationError, NavigationError, LoginFieldNotFoundError, LoginActionError


class GoogleMeetScraper:

    def __init__(self, email, password):
        self.chromedriver_url = get_chromedriver_url(CHROME_DRIVER_URLS)
        # This will download and extract the chromedriver binary
        self.exePath = download_chromedriver(self.chromedriver_url)

        self.chrome_options = webdriver.ChromeOptions()
        # Mute audio for the entire browser session
        self.chrome_options.add_argument("--mute-audio")
        # self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.driver = None
        self.last_captured_id = 0
        self.email = email
        self.password = password

    def initialize_driver(self):
        self.setup_webdriver()
        self.navigate_to_google_login()
        self.perform_login()

    def setup_webdriver(self):
        try:
            add_to_path(self.exePath)
            self.driver = webdriver.Chrome(options=self.chrome_options)
        except Exception as e:
            raise FailedInitializationError(f"Failed to initialize WebDriver: {e}")

    def navigate_to_google_login(self):
        try:
            self.driver.get(CHROME_SIGNIN_URL)
        except Exception as e:
            raise NavigationError(f"Navigation to login page failed: {e}")

    def perform_login(self):
        try:
            self.enter_email()
            self.enter_password()
        except NoSuchElementException:
            raise LoginFieldNotFoundError("Input field not found.")
        except NoSuchWindowException:
            print("Browser window was closed or not found. Exiting program")
            sys.exit()
        except Exception as e:
            raise LoginActionError(f"Error during login sequence: {e}")

    def enter_email(self):
        email_field = WebDriverWait(self.driver, 20).until(
        EC.presence_of_element_located((By.ID, EMAIL_LOGIN))
    )
        email_field.send_keys(self.email)
        email_field.send_keys(Keys.RETURN)

    def enter_password(self):
        password_field = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PASSWORD_LOGIN))
        )
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)

    def navigate_to_meeting(self, meeting_url):
        self.attempt_navigate_to_url(meeting_url)
        self.interact_with_meeting_ui()

    def attempt_navigate_to_url(self, meeting_url):
        success = False
        while not success:
            try:
                self.driver.get(meeting_url)
                success = True
            except WebDriverException as e:
                print(f"Error navigating to the meeting URL: {e}")
                if input("Failed to navigate to the meeting URL. Try again? (yes/no): ").lower() != 'yes':
                    break

    def interact_with_meeting_ui(self):
        # Wait for and click the 'Continue without microphone' button
        continue_without_mic_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, CONTINUE_WITHOUT_MIC_BUTTON_XPATH))
        )
        continue_without_mic_button.click()
        
        # Attempt to click either 'Ask to join' or 'Join now'
        self.attempt_join_meeting()
        
        # Turn on captions
        turn_on_captions_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, TURN_ON_CAPTIONS_BUTTON_XPATH))
        )
        turn_on_captions_button.click()
        
        # Show participants
        show_everyone_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, SHOW_EVERYONE_BUTTON_XPATH))
        )
        show_everyone_button.click()

        # Wait for the participants' list to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PARTICIPANTS_LIST_SELECTOR))
        )

    def attempt_join_meeting(self):
        # Define the buttons to try clicking
        possible_buttons_xpaths = [
            ASK_TO_JOIN_BUTTON_XPATH,
            JOIN_NOW_BUTTON_XPATH
        ]
        
        # Try each button until one works
        for button_xpath in possible_buttons_xpaths:
            try:
                join_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                )
                join_button.click()
                # Break after successfully clicking a button
                break
            except TimeoutException:
                # If the button wasn't found or wasn't clickable, continue to the next
                continue
        
    def transcribe_meeting(self, filepath):
        sessionStart_write(filepath)
        try:
            while not self.meeting_ended():
                self.inject_caption_ids()
                self.update_and_check_participants(filepath)
                self.update_transcript(filepath)
                time.sleep(2)  # Consider a more dynamic wait condition
        except Exception as e:
            print(f"Error during transcription: {e}")
        finally:
            sessionEnd_write(filepath)
            
    def meeting_ended(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, LEAVE_MEETING_BUTTON_CSS_SELECTOR)
            return False
        except NoSuchElementException:
            return True

    def inject_caption_ids(self):
        # Assuming you already have self.last_captured_id defined
        self.driver.execute_script(js_inject_ids_script(self.last_captured_id))

    def update_and_check_participants(self, filepath):
        current_participants = self.get_current_participants()
        joined, left = check_participants_changes(current_participants)
        log_participant_updates(filepath, joined, 'joined')
        log_participant_updates(filepath, left, 'left')
        self.participants = current_participants  # Update the participants list for the next check
                
    def run_scraper(self, save_directory, classname):
        try:
            self.setup_paths_and_directory(save_directory, classname)
            self.navigate_and_transcribe()
            self.generate_and_save_summary()
        except KeyboardInterrupt:
            print("Interrupted by user. Exiting...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.cleanup()

    def setup_paths_and_directory(self, save_directory, classname):
        # Create folder and file paths
        self.folder_name = f"{classname}_{datetime.datetime.now().strftime('%Y-%m-%d')}"
        self.full_folder_path = os.path.join(save_directory, self.folder_name)
        self.full_file_path = os.path.join(self.full_folder_path, f"{self.folder_name}.txt")
        self.summary_file_path = os.path.join(self.full_folder_path, 'Summary.txt')
        create_directory(self.full_folder_path)

    def navigate_and_transcribe(self):
        # Get the meeting URL, navigate to it, and start transcribing
        meeting_url = get_meeting_url(self.driver)
        self.navigate_to_meeting(meeting_url)
        self.transcribe_meeting(self.full_file_path)

    def generate_and_save_summary(self):
        # Generate a summary of the meeting and save it
        summary = chunkAndSummarize(self.full_file_path, template_type='structured_summary')
        save_summary_to_file(self.summary_file_path, summary)

    def cleanup(self):
        # Perform cleanup, including closing the driver
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            print(f"An error occurred during cleanup: {e}")
                
    def update_transcript(self, filepath):
        speaker_name = self.driver.find_element(By.CSS_SELECTOR, SPEAKER_NAME_CSS_SELECTOR).text
        captions = self.driver.find_elements(By.CSS_SELECTOR, CAPTIONS_TEXT_CSS_SELECTOR)
        for caption in captions:
            current_id = int(caption.get_attribute("id").replace("customID_", ""))
            if current_id > self.last_captured_id:
                print(f"{speaker_name}: {caption.text}")
                save_transcription_to_file(filepath, speaker_name, caption.text)
                self.last_captured_id = current_id
                
    def get_current_participants(self):
        participants = set()
        try:
            participants = set(self.driver.execute_script(EXTRACT_PARTICIPANTS))
        except Exception as e:
            print(f"Error retrieving participants: {e}")

        return participants


######################################################################################################################

# A few considerations:

# Page Variability: Google's interface might change over time, affecting the XPath, CSS selectors, or attributes used in this script. Regularly test and update the script to ensure compatibility.

# Conditional Checks: Instead of relying on just one criterion to confirm if you've successfully joined a meeting, consider adding multiple checks. This can be useful to handle different scenarios or changes in the user interface.

# Error Handling: Be prepared for unexpected situations. For example, Google Meet may introduce CAPTCHAs or other mechanisms that might interfere with automated logins. Plan to handle these edge cases if they arise.

# Responsiveness: As the script is running and scraping data in real-time, ensure your system remains responsive and is not overloaded with other tasks.

# Dependencies: Ensure all libraries and dependencies are up-to-date and compatible with the version of the browser driver in use.

# API Calls: If the meeting transcription is substantial, remember that the 'summarize_text' function is making an API call which may have rate limits or costs associated with it. Always monitor and manage your API usage.


# === src\scraper\old.py ===

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from services.summarizeText import get_summary
import time
from time import sleep
import os
import datetime
from common.utils import *

chrome_options = webdriver.ChromeOptions()

# Mute audio for the entire browser session
chrome_options.add_argument("--mute-audio")

# Initialize the Chrome driver with the options
driver = webdriver.Chrome(options=chrome_options)

# Retrieve credentials
DUMMY_EMAIL = os.environ.get('DUMMY_EMAIL')
DUMMY_PASSWORD = os.environ.get('DUMMY_PASSWORD')  # Assuming you've set this

timeout = time.time() + 60  # Set a timeout for 60 seconds to prevent an infinite loop

# Navigate to Google Login
driver.get("https://accounts.google.com/signin")

# Find the email and password input fields and enter credentials
# Locate the email input field and enter the email
email_field = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "identifierId"))
)

# Login sequence with safe actions
safe_action(driver, func=email_field.send_keys, element=email_field, args=[DUMMY_EMAIL])
safe_action(driver, func=email_field.send_keys, element=email_field, args=[Keys.RETURN])

# Locate the password input field and enter the password
password_field = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, "Passwd"))
)

safe_action(driver, func=password_field.send_keys, element=password_field, args=[DUMMY_PASSWORD])
safe_action(driver, func=password_field.send_keys, element=password_field, args=[Keys.RETURN])




# A few notes:

# Ensure that the aria-label attribute value matches the one provided; it may change depending on the Google Meet localization (language).

# If there's another better and more stable identifier or criteria you can use to check if the account is inside the meeting (e.g., a specific 
# element that appears only when in the meeting), then you should use that for confirmation.

# You may also need to handle scenarios where the captions are already on, in which case you won't need to click the button again. Checking the 
# aria-pressed attribute of the button might be one way to determine the current state of captions (on or off).


success = False  # A flag to determine if the URL navigation is successful


while not success:
        try:
            # After logging in successfully
            meeting_url = get_meeting_url(driver=driver)
            driver.get(meeting_url)
            success = True  # If the above lines run without an exception, set the flag to True

        except Exception as e:
            print(f"Error navigating to the meeting URL: {e}")
            response = input("Failed to navigate to the meeting URL. Would you like to try again? (yes/no): ")

            # If the user's response isn't affirmative, break out of the loop
            if response.lower() != 'yes':
                break


safe_action(driver, by=By.XPATH, value="//button[span[text()='Continue without microphone']]", action='click')

possible_buttons = [
    "//button/span[text()='Ask to join']",
    "//button/span[text()='Join now']"
]
time.sleep(2)

for button_xpath in possible_buttons:
    try:
        safe_action(driver, by=By.XPATH, value=button_xpath, action='click', single_try=True)
        break  # Exit the loop if the action was successful
    except (ElementNotInteractableException, NoSuchElementException):
        # If an exception occurs, the loop continues to the next button_xpath
        time.sleep(2)
        continue


safe_action(driver, by=By.XPATH, value="//button[@aria-label='Turn on captions (c)']", action='click')

classname = "PrasadsClass"

# Generate the filename for this session.
base_directory = "C:\\Users\\Braden\\OneDrive - Utah Valley University\\Desktop\\PrasadsClass\\LectureNotes"
folder_name = f"{classname}_{datetime.datetime.now().strftime('%Y-%m-%d')}"
filename = f"{folder_name}.txt"
full_folder_path = os.path.join(base_directory, folder_name)
full_file_path = os.path.join(full_folder_path, filename)

# Create directory if it doesn't exist
if not os.path.exists(full_folder_path):
    os.makedirs(full_folder_path)

last_captured_id = 0  # Initialize the last captured ID to 0

# The JavaScript to assign unique IDs will be slightly modified
def js_inject_ids_script(last_id):
    return """
    var container = document.querySelector("div[jsname='tgaKEf']");
    if (container) {
        var lastID = """ + str(last_id) + """;  // Using the last ID passed to the script
        var spans = container.querySelectorAll("span");
        for (var i = 0; i < spans.length; i++) {
            if (!spans[i].id) {
                lastID++;  // Increment the last ID
                spans[i].id = "customID_" + lastID;  // Assigning the new unique ID to the span
            }
        }
    }
    """

# Write the header to the file before entering the scraping loop
with open(full_file_path, 'a') as file:
    now = datetime.datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    file.write("\n\n=====================================\n")  # Separator
    file.write(f"Captured at: {formatted_date_time}\n\n")  # Date-Time header

meeting_ended = False  # Add a flag for meeting status

try:
    while True:
        if meeting_ended:
            break  # Break out of the loop if the meeting ended
        try:

            # Inject the JavaScript to assign IDs
            driver.execute_script(js_inject_ids_script(last_captured_id))
            
            # Check if "Leave call" button is present
            try:
                leave_call_button = driver.find_element(By.CSS_SELECTOR, "button[jsname='CQylAd']")
            except NoSuchElementException:
                print("Meeting ended or left")
                meeting_ended = True  # Set the flag
                continue  # Skip the current iteration of the loop

            # Get speaker's name and caption
            speaker_name = driver.find_element(By.CSS_SELECTOR, ".zs7s8d.jxFHg").text
            # Get all span tags with the custom ID prefix
            captions = driver.find_elements(By.CSS_SELECTOR, "div[jsname='tgaKEf'] span[id^='customID_']")

            # Iterate over the captions and process only the new ones based on the custom ID
            for caption in captions:
                current_id = int(caption.get_attribute("id").replace("customID_", ""))
                if current_id > last_captured_id:
                    print(f"{speaker_name}: {caption.text}")

                    # Save the scraped data to the file without additional headers
                    with open(full_file_path, 'a') as file:
                        file.write(f"{speaker_name}: {caption.text}\n")  

                    # Update the last captured ID
                    last_captured_id = current_id

            # Pause for a few seconds before checking again
            time.sleep(2)
        except Exception as e:
            print(f"Error scraping: {e}")
            time.sleep(2)
except (KeyboardInterrupt, Exception) as e:
    print(f"Exiting gracefully due to: {e}")
finally: # Using finally to ensure this block always runs
    driver.close()
    
    summary = get_summary(full_file_path, template_type='structured_summary')  # Get the summary
    summary_file_path = os.path.join(full_folder_path, 'Summary.txt')
    write_summary_to_file(summary_file_path, summary)
    
    

# === src\scraper\__init__.py ===



# === src\services\summarizeText.py ===

# Import necessary libraries
import openai  # OpenAI's Python package for accessing the GPT models
# Package to load environment variables from .env file
from dotenv import load_dotenv
import os  # Python's standard library for interacting with the operating system
from common.decorators import *
from common.AI_Templates import templates
from multiprocessing import Pool, cpu_count
from queue import Queue
from common.utils import cleanup_temp_files
import threading

import glob
# Load environment variables from a .env file. This is useful for secrets management,
# allowing sensitive information (like API keys) to be kept out of the source code.
load_dotenv()

# Fetch OpenAI API key from the .env file. The os.getenv function retrieves
# the value of the environment variable named "OPENAI_API_KEY".
openai.api_key = os.getenv("OPENAI_API_KEY")

# # Use the decorator with the structured_summary function
# @handle_large_texts(max_tokens=3000) #uncomment to if txt files become too large

@timing_decorator
def get_summary(path, template_type='structured_summary'):
    """
    Use OpenAI's API to create a structured summary of the provided text.

    Parameters:
        path (str): The path to the file that contains the meeting transcript to be summarized.

    Returns:
        str: A structured summary of the meeting transcript.

    Usage:
        This function reads the meeting transcript from a file, sends it to OpenAI's GPT-3.5 Turbo model
        to generate a structured summary, and returns the summary. The output will have specific sections
        like Introduction, Key Points, Decisions Made, Action Items, and Conclusion.

        Coders looking to extend or modify this function can:
        1. Add or modify sections in the system message to get different structures in the summary.
        2. Adjust the OpenAI model or its parameters for different outcomes.
        3. Incorporate additional preprocessing or postprocessing of the text to further refine the summary.
    """

    # Ensure the chosen template exists
    if template_type not in templates:
        raise ValueError(f"Template '{template_type}' not found.")

    # Construct chat prompts for the GPT model using the chosen template
    system_prompt = templates[template_type]['system']

    # Read the content of the file specified by 'path'
    with open(path, 'r') as file:
        meeting_transcript = file.read()

    # Trim the meeting transcript if it's too long.
    # Assuming 4000 characters for simplicity.
    max_transcript_length = 4000 - len(system_prompt)
    if len(meeting_transcript) > max_transcript_length:
        meeting_transcript = meeting_transcript[:max_transcript_length] + "..."

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"Here's the meeting transcript:\n\n{meeting_transcript}"
        }
    ]

    # Get the model's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract and return the assistant's response
    assistant_reply = response.choices[0].message['content']
    return assistant_reply.strip()


def _summarize_chunk(chunk):
    """
    Helper function to summarize a given chunk.
    """
    with open('temp\\temp_chunk_{}.txt'.format(os.getpid()), 'w') as temp_file:  # unique temp file per process
        temp_file.write(chunk)
    return get_summary('temp\\temp_chunk_{}.txt'.format(os.getpid()), template_type="chunk_summary")

@timing_decorator
@decorator_record_algorithm_type
def chunkAndSummarize(path, template_type='structured_summary', chunk_size=3500):
    """
    Divides the text into meaningful chunks and summarizes each chunk individually using multiprocessing.
    Combines the individual summaries to produce a final summarized text.

    Parameters:
        path (str): Path to the file containing the text to be summarized.
        template_type (str): Type of summary template to be used.
        chunk_size (int): Size of each chunk in characters. Default is 3500.

    Returns:
        str: Summarized text.
    """

    current_working_directory = os.getcwd()
    print(current_working_directory)
    # Read the content of the file specified by 'path'
    with open(path, 'r') as file:
        content = file.read()

    # Split the content into chunks of specified size
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    
    num_processors = min(len(chunks), cpu_count())
    
    # Use multiprocessing to summarize each chunk concurrently
    with Pool(processes=num_processors) as pool:
        summarized_chunks = pool.map(_summarize_chunk, chunks)

    # Combine the summarized chunks into a single text
    combined_summaries = ' '.join(summarized_chunks)
    
    # Write the combined summaries to a temporary file
    with open('temp\\temp_combined_summaries.txt', 'w') as temp_file:
        temp_file.write(combined_summaries)
    
    # Use the get_summary function to summarize the combined summaries
    overall_summary = get_summary('temp\\temp_combined_summaries.txt', template_type)
    
    cleanup_temp_files()  # Call the cleanup function at the end
    
    return overall_summary

################# Using different approach with threads (TEST) ##########################

def _threaded_summarize_chunk(chunk, queue):
    with open('temp\\temp_window_{}.txt'.format(threading.get_ident()), 'w') as temp_file:
        temp_file.write(chunk)
    summarized_chunk = get_summary('temp\\temp_window_{}.txt'.format(threading.get_ident()), template_type="chunk_summary")
    queue.put(summarized_chunk)

@timing_decorator
@decorator_record_algorithm_type
def sliding_window_summarize_method(path, template_type='chunk_summary', window_size=3500, overlap=500, max_threads=4):
    current_working_directory = os.getcwd()
    print(current_working_directory)
    with open(path, 'r') as file:
        content = file.read()
    
    start_idx = 0
    end_idx = window_size
    summarized_windows = []
    queue = Queue()

    while start_idx < len(content):
        threads = []
        window_content = content[start_idx:end_idx]
        
        # Create and start threads
        if len(threads) < max_threads:
            t = threading.Thread(target=_threaded_summarize_chunk, args=(window_content, queue))
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # Slide the window
        start_idx = end_idx - overlap
        end_idx = start_idx + window_size
        
    # Collect all the results from the threads
    while not queue.empty():
        summarized_windows.append(queue.get())

    # Optional: Create a final summary from the merged summarized windows
    final_summary = ' '.join(summarized_windows)
    with open('temp\\temp_final_summary.txt', 'w') as temp_file:
        temp_file.write(final_summary)
    structured_summary = get_summary('temp\\temp_final_summary.txt', template_type)
    
    return structured_summary


# A few things to consider and keep in mind:

# 1. Length Limitations:
#    - The gpt-3.5-turbo model has a token limit of 4096 tokens. This means that very long texts
#      could receive truncated summaries, or the request could even fail.
#    - To handle large texts, there's a decorator (`handle_large_texts`) available. This can be applied
#      to the `structured_summary` function to manage longer transcripts. To use it, uncomment the
#      decorator line above the `structured_summary` function.

# 2. Iterative Refinement:
#    - Depending on the content and complexity of the input text, the model might not always produce
#      a perfect summary on the first try. It's a good practice to refine your instructions or try
#      multiple summaries to get the best result.
#    - Regularly testing and adjusting based on the type of content you deal with can improve results.

# 3. Explicitness:
#    - Providing explicit and clear instructions to the model can yield better results. For instance,
#      instead of simply requesting "Key Points", specifying the number, like "List the 5 most important
#      points discussed", can help in narrowing down the information.

# 4. Future Goals and Enhancements:
#    - Consider integrating more advanced preprocessing or post-processing steps to refine and polish
#      the returned summaries.
#    - As OpenAI releases new models or versions, it might be beneficial to test and migrate to them
#      for potentially better results.
#    - Expand the system message to include or adjust sections in the summary, tailoring it to specific
#      needs. For instance, you might want sections dedicated to "Questions Raised" or "Unresolved Topics".


# Handling large text inputs while maintaining the context of the entire content is challenging, especially 
# when the model has a token limit. However, there are several strategies you can employ:

# Chunking and Summarizing: Divide the text into meaningful chunks and summarize each chunk individually. 
# Afterwards, combine the individual summaries. This method can preserve most of the important details, but 
# there's a risk of losing the overarching narrative or context of the meeting.

# Hierarchical Summarization: Start by summarizing the entire text into a shorter version. Then, summarize the 
# shorter version again. This iterative summarization can provide a condensed version while aiming to maintain 
# the main context.

# Custom Model Training: While training a model specifically for your use case might sound like a good approach, 
# it requires a significant amount of data, resources, and expertise. If you have a collection of meeting transcripts 
# and their corresponding high-quality summaries, you could consider fine-tuning a model on this dataset. However, 
# keep in mind that fine-tuning models like GPT-3.5 is currently not supported by OpenAI's platform. You would need to 
# utilize platforms like HuggingFace's Transformers with models like GPT-2 or BERT for such endeavors.

# Sliding Window Approach: Use a sliding window to move through the text, always overlapping part of the previous chunk 
# with the current one. This way, some context is preserved from chunk to chunk. The summaries from each window can then be 
# stitched together. This can help in ensuring continuity but might lead to redundancy in the final summary.

# Enhanced Preprocessing: Before feeding the text to the model, use techniques to remove any irrelevant or repetitive content. 
# The cleaner and more concise the initial text, the less you have to cut out to fit within the model's token limit.

# Human-in-the-loop: Summarize in chunks using the model, then have a human editor stitch together and refine the summaries into a 
# coherent whole. This can often lead to higher-quality summaries as the human can ensure context is maintained and redundancy is removed.

# Use Different Models: Instead of relying solely on GPT-3.5 or similar models, you can explore other models or algorithms specifically 
# designed for text summarization. For instance, there are extractive summarization algorithms that pick out the most important sentences 
# from the text, or abstractive models that generate a completely new summary.

# If maintaining the context of the entire meeting is absolutely crucial, a hybrid approach combining machine-generated summaries with human 
# oversight might be the most effective. That said, always consider the trade-offs in terms of time, costs, and quality.


# Assuming you have the 'chunkAndSummarize' function and 'get_summary' function in the same file or they are imported appropriately.

  # Optional: Clean up temporary files


# === src\services\whatsapp_notifier.py ===

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



# === src\services\__init__.py ===



# === testFeatures\testFeatures.py ===

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