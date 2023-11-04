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