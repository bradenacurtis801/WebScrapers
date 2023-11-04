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
    
    