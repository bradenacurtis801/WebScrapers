CHROME_DRIVER_URLS = "https://googlechromelabs.github.io/chrome-for-testing/"
CHROME_SIGNIN_URL = "https://accounts.google.com/signin"

EMAIL_LOGIN = "identifierId"
PASSWORD_LOGIN = "input[type='password'][jsname='YPqjbf']"
HOME_PAGE_LOADED = "h1.XY0ASe"


# Use single quotes for JavaScript selectors
PARTICIPANT_ITEM_SELECTOR = "div[role='listitem']"
PARTICIPANT_NAME_SELECTOR = "span.zWGUib"
HOST_INDICATOR_SELECTOR = "div.d93U2d"
CAPTION_CONTAINER_SELECTOR = "div[jsname='tgaKEf']"

# Google Meet specific selectors
PARTICIPANTS_LIST_SELECTOR = "div[jsname='jrQDbd']"
LEAVE_MEETING_BUTTON_CSS_SELECTOR = "button[jsname='CQylAd']"
SPEAKER_NAME_CSS_SELECTOR = ".zs7s8d.jxFHg"
CAPTIONS_TEXT_CSS_SELECTOR = "div[jsname='tgaKEf'] span[id^='customID_']"

# Google Meet UI button selectors with XPath - can contain either single or double quotes
# If using single quotes, be consistent and escape them in f-strings if necessary
CONTINUE_WITHOUT_MIC_BUTTON_XPATH = "//button[span[text()='Continue without microphone']]"
ASK_TO_JOIN_BUTTON_XPATH = "//button/span[text()='Ask to join']"
JOIN_NOW_BUTTON_XPATH = "//button/span[text()='Join now']"
TURN_ON_CAPTIONS_BUTTON_XPATH = "//button[@aria-label='Turn on captions (c)']"
SHOW_EVERYONE_BUTTON_XPATH = "//button[@aria-label='Show everyone']"
