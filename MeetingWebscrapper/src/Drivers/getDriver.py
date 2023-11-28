import platform
import requests
from bs4 import BeautifulSoup
import os
import zipfile
import re
import shutil
import traceback


def get_chromedriver_url(URL):
    html_content = requests.get(URL).text
    soup = BeautifulSoup(html_content, "html.parser")

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
    pattern = re.compile(f"https.*{os_key}.*chromedriver.*\.zip")
    # Find the <code> tag containing the URL
    url_code_tag = section.find("code", string=pattern)

    if url_code_tag:
        return url_code_tag.text
    raise ValueError("Driver URL not found for the architecture")


def download_chromedriver(
    url, download_path="src/Drivers/chromedriver.zip", extract_path="src/Drivers/"
):
    response = requests.get(url)
    with open(download_path, "wb") as file:
        file.write(response.content)
    try:
        with zipfile.ZipFile(download_path, "r") as zip_ref:
            extracted_file_names = zip_ref.namelist()
            zip_ref.extractall(extract_path)
    except PermissionError:
        print(
            "Permission error while extracting. Please ensure you have the necessary permissions."
        )
        traceback.print_exc()

    os.remove(download_path)  # Remove the zip file after extraction
    # Return the full path to the extracted chromedriver
    exeFolder = extracted_file_names[1].split("/")[0]
    return os.path.abspath(os.path.join(extract_path, exeFolder))
