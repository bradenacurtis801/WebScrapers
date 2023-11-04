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
    # # #normal startup (with webscrapping)
    app()
    
    # ######################### Testing AI API functionality with large text files. Currently trying different approaches i.e. chunk summary and window sliding techinque #################################
    # # # Path to your text file
    # # file_path = "C:/Users/Braden/OneDrive - Utah Valley University/Desktop/PrasadsClass/LectureNotes/PrasadsClass_2023-11-01/PrasadsClass_2023-11-01.txt"

    # # # Call the function
    # # summarized_text = chunkAndSummarize(file_path, template_type='structured_summary')

    # # # Print the summarized text
    # # print(summarized_text)
    
    # myInstance = GoogleMeetScraper(DUMMY_EMAIL,DUMMY_PASSWORD)
    
if __name__ == '__main__':
    main()