from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, WebDriverException, TimeoutException, StaleElementReferenceException
from selenium import webdriver
from services.summarizeText import chunkAndSummarize
import time
from time import sleep
import os
import sys
import traceback
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
            raise FailedInitializationError(
                f"Failed to initialize WebDriver: {e}")

    def navigate_to_google_login(self):
        try:
            self.driver.get(CHROME_SIGNIN_URL)
            # Wait for some element that signifies the page has loaded
        except TimeoutException:
            raise NavigationError(f"Timed out waiting for login page to load")
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
            EC.element_to_be_clickable((By.ID, EMAIL_LOGIN))
        )
        email_field.send_keys(self.email)
        email_field.send_keys(Keys.RETURN)

    def enter_password(self):
        password_field = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, PASSWORD_LOGIN))
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
            EC.element_to_be_clickable(
                (By.XPATH, CONTINUE_WITHOUT_MIC_BUTTON_XPATH))
        )
        continue_without_mic_button.click()

        # Attempt to click either 'Ask to join' or 'Join now'
        self.attempt_join_meeting()

        # Turn on captions
        turn_on_captions_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, TURN_ON_CAPTIONS_BUTTON_XPATH))
        )
        turn_on_captions_button.click()

        # Show participants
        show_everyone_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, SHOW_EVERYONE_BUTTON_XPATH))
        )
        show_everyone_button.click()

        # Wait for the participants' list to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, PARTICIPANTS_LIST_SELECTOR))
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
                print(
                    f"Timeout when waiting for button with XPath: {button_xpath}")
                continue
        else:
            # If none of the buttons worked, raise an exception or handle the error
            raise Exception("Failed to join meeting.")

    def transcribe_meeting(self, filepath):
        sessionStart_write(filepath)
        self.participants = set()
        try:
            while not self.meeting_ended():
                self.inject_caption_ids()
                self.update_and_check_participants(filepath)
                self.update_transcript(filepath)
                time.sleep(2)  # Consider a more dynamic wait condition
        except Exception as e:
            print(f"Error during transcription: {e}")
            traceback.print_exc()
            pass
        finally:
            sessionEnd_write(filepath)

    def meeting_ended(self):
        try:
            self.driver.find_element(
                By.CSS_SELECTOR, LEAVE_MEETING_BUTTON_CSS_SELECTOR)
            return False
        except NoSuchElementException:
            return True
        except Exception as e:
            print(f"Error during transcription: {e}")
            traceback.print_exc()
            pass

    def inject_caption_ids(self):
        # Assuming you already have self.last_captured_id defined
        self.driver.execute_script(js_inject_ids_script(self.last_captured_id))

    def update_and_check_participants(self, filepath):
        current_participants = self.get_current_participants()
        joined, left = check_participants_changes(
            current_participants, self.participants)
        log_participant_updates(filepath, joined, 'joined')
        log_participant_updates(filepath, left, 'left')
        # Update the participants list for the next check
        self.participants = current_participants

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
        self.full_file_path = os.path.join(
            self.full_folder_path, f"{self.folder_name}.txt")
        self.summary_file_path = os.path.join(
            self.full_folder_path, 'Summary.txt')
        create_directory(self.full_folder_path)

    def navigate_and_transcribe(self):
        # Get the meeting URL, navigate to it, and start transcribing
        meeting_url = get_meeting_url(self.driver)
        self.navigate_to_meeting(meeting_url)
        self.transcribe_meeting(self.full_file_path)

    def generate_and_save_summary(self):
        # Generate a summary of the meeting and save it
        summary = chunkAndSummarize(
            self.full_file_path, template_type='structured_summary')
        save_summary_to_file(self.summary_file_path, summary)

    def cleanup(self):
        # Perform cleanup, including closing the driver
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            print(f"An error occurred during cleanup: {e}")

    def update_transcript(self, filepath):
        try:
            speaker_name = self.driver.find_element(
                By.CSS_SELECTOR, SPEAKER_NAME_CSS_SELECTOR).text
            captions = self.driver.find_elements(
                By.CSS_SELECTOR, CAPTIONS_TEXT_CSS_SELECTOR)
            for caption in captions:
                current_id = int(caption.get_attribute(
                    "id").replace("customID_", ""))
                if current_id > self.last_captured_id:
                    print(f"{speaker_name}: {caption.text}")
                    save_transcription_to_file(
                        filepath, speaker_name, caption.text)
                    self.last_captured_id = current_id
        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            pass
        except Exception:
            print("unexpected error")
            traceback.print_exc()
            pass

    def get_current_participants(self):
        try:
            participants = set(
                self.driver.execute_script(EXTRACT_PARTICIPANTS))
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
