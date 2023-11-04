Google Meet Transcription Bot

Overview
This project provides a script that automates the login process into a Google account and joins a Google Meet meeting to transcribe the ongoing dialogue. It's useful for students or professionals who want to capture and review the main talking points of a meeting without taking notes in real-time.

Prerequisites
Python: Ensure Python is installed. This script was developed using Python 3.11.6

Selenium: The automation is achieved using the Selenium package. You can install it using pip:

pip install selenium

Google Chrome & ChromeDriver: The script uses ChromeDriver to interface with the Chrome browser. Ensure you have both installed and that ChromeDriver is in your system's PATH.

Make sure you install a googledriver version that is the closest to the version of the google browser you will be using. See Images below:
URL: https://googlechromelabs.github.io/chrome-for-testing/#stable


Environment Variables: Store your dummy Google account's email and password as environment variables (DUMMY_EMAIL and DUMMY_PASSWORD respectively) for security reasons.

Setup
Clone the Repository:

bash

git clone [your-repository-url]
cd [repository-name]
Set Up a Virtual Environment (optional but recommended):

bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Dependencies:


pip install -r requirements.txt
Set Environment Variables:
For Windows (PowerShell):

css

[System.Environment]::SetEnvironmentVariable("DUMMY_EMAIL", "your-email@gmail.com", "User")
[System.Environment]::SetEnvironmentVariable("DUMMY_PASSWORD", "your-password", "User")
For Linux/macOS:

bash
export DUMMY_EMAIL="your-email@gmail.com"
export DUMMY_PASSWORD="your-password"
Run the Script:


python script_name.py
Follow the on-screen prompts to input the Google Meet URL.

Notes
The script will continuously transcribe dialogue until manually interrupted.
Transcriptions will be saved in the specified directory as a .txt file, organized by class name and date.
For security reasons, do not hard-code your Google account credentials directly into the script.

Future Enhancements
Extend support for other browsers.
Implement a GUI for a more user-friendly experience.
Add error handling for invalid Google Meet URLs.
Add time signiture for when meeting started, when each dialog chat was spoken, when meeting has ended. 
Handle If call has disconnected and then rejoined 

Implementing new file structure:
TeamsWebscraper/
│
├── .vscode/
│
├── assets/
│
├── src/  # A directory for source files
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── meet_scraper.py
│   │   └── utils.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── summarizeText.py
│   │
│   └── common/
│       ├── __init__.py
│       └── decorators.py
│
├── venv/
│
├── __pycache__/
│
├── .env
│
├── README.md
│
└── requirements.txt

Explanation:

src/: This directory is introduced to hold all source code files.

scraper/: Dedicated to the web scraping functionality.

services/: Dedicated to services that the project might utilize, e.g., text summarization.

common/: General-purpose or shared functionality, e.g., decorators, that aren't specific to scraping or services.

assets/: For static files, such as images or other resources.

.vscode/: Configuration for the VS Code editor.

venv/: The virtual environment.

pycache/: Python cache files. Remember, you might want to add this to a .gitignore file if you're using version control.

.env: Environment variables.

README.md: Instructions, explanations, or other relevant project info.

requirements.txt: List of Python packages required for the project.

Moving files around to match the above structure will also mean updating import paths in the scripts. Ensure all your modules can still find and import each other properly after the restructuring.

This is just a suggested structure and can be further adjusted to fit the unique requirements of your project. The main idea is to keep related files together in directories and separate distinct functionalities into different modules and packages. This makes the project more modular and easier to manage.