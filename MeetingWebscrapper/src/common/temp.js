  var participantsList = document.querySelector("{PARTICIPANTS_LIST_SELECTOR}");
  if (participantsList) {{
    let participants = Array.from(participantsList.querySelectorAll("{PARTICIPANT_ITEM_SELECTOR}")).map(function(participant) {{
      // Find the name span
      let nameElement = participant.querySelector("{PARTICIPANT_NAME_SELECTOR}");
      let nameText = nameElement ? nameElement.textContent.trim() : '';
  
      // Check if this participant has an additional descriptor indicating they are the host
      let additionalDescriptor = participant.querySelector("{HOST_INDICATOR_SELECTOR}");
      if (additionalDescriptor && additionalDescriptor.textContent.includes('Meeting host')) {{
        nameText += ' (Host)';
      }}
  
      return nameText;
    }}).filter(function(name) {{ return name !== ''; }}); // Filter out any empty names
    return participants;
  }} else {{
    // If the container is not found, return an empty array
    return [];
  }}