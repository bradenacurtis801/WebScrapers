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
