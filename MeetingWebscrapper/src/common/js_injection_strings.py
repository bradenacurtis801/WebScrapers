from common.constants import *
import json

# Using json.dumps in Python to Safely Generate JavaScript Snippet
# ---------------------------------------------------------------
# This Python script generates a JavaScript (JS) snippet that is intended
# to be executed in the context of a web page, within the web browser.
# The script uses `json.dumps` for the following reasons:
#
# 1. Correct Quotation:
#    The `json.dumps` function is used to safely encode Python strings
#    as valid JSON/JavaScript string literals. It ensures that any special
#    characters, particularly quotation marks, are correctly escaped.
#    This is essential because the JavaScript code will be passed as a
#    string from Python to the Selenium driver, which then executes it
#    within the browser. `json.dumps` handles the proper insertion of
#    quotes within the JavaScript strings to prevent syntax errors.
#
# 2. String Literal Safety:
#    Using `json.dumps` prevents potential JS injection issues and syntax
#    errors that could arise from directly concatenating or formatting
#    strings within the JS code. It converts Python string values into
#    safe JS string literals, which can then be safely embedded within
#    the JS snippet.
#
# 3. Code Clarity:
#    By clearly delineating Python code from JavaScript code, `json.dumps`
#    allows for more readable and maintainable code. It clarifies the
#    intention to use a Python variable within the JS snippet, making the
#    code self-documenting.
#
# The generated JS snippet is used to query the DOM of a web page to extract
# participant names from a list and identify if any of them are marked as the
# host of the meeting. This script is typically used in the context of
# web automation using the Selenium WebDriver.

# JS snippet for getting participant names and checking for the host
EXTRACT_PARTICIPANTS = f"""
  var participantsList = document.querySelector({json.dumps(PARTICIPANTS_LIST_SELECTOR)});
  if (participantsList) {{
    let participants = Array.from(participantsList.querySelectorAll({json.dumps(PARTICIPANT_ITEM_SELECTOR)})).map(participant => {{
      // Find the name span
      let nameElement = participant.querySelector({json.dumps(PARTICIPANT_NAME_SELECTOR)});
      let nameText = nameElement ? nameElement.textContent.trim() : '';
  
      // Check if this participant has an additional descriptor indicating they are the host
      let additionalDescriptor = participant.querySelector({json.dumps(HOST_INDICATOR_SELECTOR)});
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
    var container = document.querySelector({json.dumps(CAPTION_CONTAINER_SELECTOR)});
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