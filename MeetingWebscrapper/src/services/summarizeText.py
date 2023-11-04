# Import necessary libraries
import openai  # OpenAI's Python package for accessing the GPT models
# Package to load environment variables from .env file
from dotenv import load_dotenv
import os  # Python's standard library for interacting with the operating system
from common.decorators import *
from common.AI_Templates import templates
from multiprocessing import Pool, cpu_count
from queue import Queue
from common.utils import cleanup_temp_files
import threading

import glob
# Load environment variables from a .env file. This is useful for secrets management,
# allowing sensitive information (like API keys) to be kept out of the source code.
load_dotenv()

# Fetch OpenAI API key from the .env file. The os.getenv function retrieves
# the value of the environment variable named "OPENAI_API_KEY".
openai.api_key = os.getenv("OPENAI_API_KEY")

# # Use the decorator with the structured_summary function
# @handle_large_texts(max_tokens=3000) #uncomment to if txt files become too large

@timing_decorator
def get_summary(path, template_type='structured_summary'):
    """
    Use OpenAI's API to create a structured summary of the provided text.

    Parameters:
        path (str): The path to the file that contains the meeting transcript to be summarized.

    Returns:
        str: A structured summary of the meeting transcript.

    Usage:
        This function reads the meeting transcript from a file, sends it to OpenAI's GPT-3.5 Turbo model
        to generate a structured summary, and returns the summary. The output will have specific sections
        like Introduction, Key Points, Decisions Made, Action Items, and Conclusion.

        Coders looking to extend or modify this function can:
        1. Add or modify sections in the system message to get different structures in the summary.
        2. Adjust the OpenAI model or its parameters for different outcomes.
        3. Incorporate additional preprocessing or postprocessing of the text to further refine the summary.
    """

    # Ensure the chosen template exists
    if template_type not in templates:
        raise ValueError(f"Template '{template_type}' not found.")

    # Construct chat prompts for the GPT model using the chosen template
    system_prompt = templates[template_type]['system']

    # Read the content of the file specified by 'path'
    with open(path, 'r') as file:
        meeting_transcript = file.read()

    # Trim the meeting transcript if it's too long.
    # Assuming 4000 characters for simplicity.
    max_transcript_length = 4000 - len(system_prompt)
    if len(meeting_transcript) > max_transcript_length:
        meeting_transcript = meeting_transcript[:max_transcript_length] + "..."

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"Here's the meeting transcript:\n\n{meeting_transcript}"
        }
    ]

    # Get the model's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract and return the assistant's response
    assistant_reply = response.choices[0].message['content']
    return assistant_reply.strip()


def _summarize_chunk(chunk):
    """
    Helper function to summarize a given chunk.
    """
    with open('temp\\temp_chunk_{}.txt'.format(os.getpid()), 'w') as temp_file:  # unique temp file per process
        temp_file.write(chunk)
    return get_summary('temp\\temp_chunk_{}.txt'.format(os.getpid()), template_type="chunk_summary")

@timing_decorator
def chunkAndSummarize(path, template_type='structured_summary', chunk_size=3500):
    """
    Divides the text into meaningful chunks and summarizes each chunk individually using multiprocessing.
    Combines the individual summaries to produce a final summarized text.

    Parameters:
        path (str): Path to the file containing the text to be summarized.
        template_type (str): Type of summary template to be used.
        chunk_size (int): Size of each chunk in characters. Default is 3500.

    Returns:
        str: Summarized text.
    """

    current_working_directory = os.getcwd()
    print(current_working_directory)
    # Read the content of the file specified by 'path'
    with open(path, 'r') as file:
        content = file.read()

    # Split the content into chunks of specified size
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    
    num_processors = min(len(chunks), cpu_count())
    
    # Use multiprocessing to summarize each chunk concurrently
    with Pool(processes=num_processors) as pool:
        summarized_chunks = pool.map(_summarize_chunk, chunks)

    # Combine the summarized chunks into a single text
    combined_summaries = ' '.join(summarized_chunks)
    
    # Write the combined summaries to a temporary file
    with open('temp\\temp_combined_summaries.txt', 'w') as temp_file:
        temp_file.write(combined_summaries)
    
    # Use the get_summary function to summarize the combined summaries
    overall_summary = get_summary('temp\\temp_combined_summaries.txt', template_type)
    
    cleanup_temp_files()  # Call the cleanup function at the end
    
    return overall_summary

################# Using different approach with threads (TEST) ##########################

def _threaded_summarize_chunk(chunk, queue):
    with open('temp\\temp_window_{}.txt'.format(threading.get_ident()), 'w') as temp_file:
        temp_file.write(chunk)
    summarized_chunk = get_summary('temp\\temp_window_{}.txt'.format(threading.get_ident()), template_type="chunk_summary")
    queue.put(summarized_chunk)

@timing_decorator
def sliding_window_summarize_method(path, template_type='chunk_summary', window_size=3500, overlap=500, max_threads=4):
    current_working_directory = os.getcwd()
    print(current_working_directory)
    with open(path, 'r') as file:
        content = file.read()
    
    start_idx = 0
    end_idx = window_size
    summarized_windows = []
    queue = Queue()

    while start_idx < len(content):
        threads = []
        window_content = content[start_idx:end_idx]
        
        # Create and start threads
        if len(threads) < max_threads:
            t = threading.Thread(target=_threaded_summarize_chunk, args=(window_content, queue))
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # Slide the window
        start_idx = end_idx - overlap
        end_idx = start_idx + window_size
        
    # Collect all the results from the threads
    while not queue.empty():
        summarized_windows.append(queue.get())

    # Optional: Create a final summary from the merged summarized windows
    final_summary = ' '.join(summarized_windows)
    with open('temp\\temp_final_summary.txt', 'w') as temp_file:
        temp_file.write(final_summary)
    structured_summary = get_summary('temp\\temp_final_summary.txt', template_type)
    
    return structured_summary


# A few things to consider and keep in mind:

# 1. Length Limitations:
#    - The gpt-3.5-turbo model has a token limit of 4096 tokens. This means that very long texts
#      could receive truncated summaries, or the request could even fail.
#    - To handle large texts, there's a decorator (`handle_large_texts`) available. This can be applied
#      to the `structured_summary` function to manage longer transcripts. To use it, uncomment the
#      decorator line above the `structured_summary` function.

# 2. Iterative Refinement:
#    - Depending on the content and complexity of the input text, the model might not always produce
#      a perfect summary on the first try. It's a good practice to refine your instructions or try
#      multiple summaries to get the best result.
#    - Regularly testing and adjusting based on the type of content you deal with can improve results.

# 3. Explicitness:
#    - Providing explicit and clear instructions to the model can yield better results. For instance,
#      instead of simply requesting "Key Points", specifying the number, like "List the 5 most important
#      points discussed", can help in narrowing down the information.

# 4. Future Goals and Enhancements:
#    - Consider integrating more advanced preprocessing or post-processing steps to refine and polish
#      the returned summaries.
#    - As OpenAI releases new models or versions, it might be beneficial to test and migrate to them
#      for potentially better results.
#    - Expand the system message to include or adjust sections in the summary, tailoring it to specific
#      needs. For instance, you might want sections dedicated to "Questions Raised" or "Unresolved Topics".


# Handling large text inputs while maintaining the context of the entire content is challenging, especially 
# when the model has a token limit. However, there are several strategies you can employ:

# Chunking and Summarizing: Divide the text into meaningful chunks and summarize each chunk individually. 
# Afterwards, combine the individual summaries. This method can preserve most of the important details, but 
# there's a risk of losing the overarching narrative or context of the meeting.

# Hierarchical Summarization: Start by summarizing the entire text into a shorter version. Then, summarize the 
# shorter version again. This iterative summarization can provide a condensed version while aiming to maintain 
# the main context.

# Custom Model Training: While training a model specifically for your use case might sound like a good approach, 
# it requires a significant amount of data, resources, and expertise. If you have a collection of meeting transcripts 
# and their corresponding high-quality summaries, you could consider fine-tuning a model on this dataset. However, 
# keep in mind that fine-tuning models like GPT-3.5 is currently not supported by OpenAI's platform. You would need to 
# utilize platforms like HuggingFace's Transformers with models like GPT-2 or BERT for such endeavors.

# Sliding Window Approach: Use a sliding window to move through the text, always overlapping part of the previous chunk 
# with the current one. This way, some context is preserved from chunk to chunk. The summaries from each window can then be 
# stitched together. This can help in ensuring continuity but might lead to redundancy in the final summary.

# Enhanced Preprocessing: Before feeding the text to the model, use techniques to remove any irrelevant or repetitive content. 
# The cleaner and more concise the initial text, the less you have to cut out to fit within the model's token limit.

# Human-in-the-loop: Summarize in chunks using the model, then have a human editor stitch together and refine the summaries into a 
# coherent whole. This can often lead to higher-quality summaries as the human can ensure context is maintained and redundancy is removed.

# Use Different Models: Instead of relying solely on GPT-3.5 or similar models, you can explore other models or algorithms specifically 
# designed for text summarization. For instance, there are extractive summarization algorithms that pick out the most important sentences 
# from the text, or abstractive models that generate a completely new summary.

# If maintaining the context of the entire meeting is absolutely crucial, a hybrid approach combining machine-generated summaries with human 
# oversight might be the most effective. That said, always consider the trade-offs in terms of time, costs, and quality.


# Assuming you have the 'chunkAndSummarize' function and 'get_summary' function in the same file or they are imported appropriately.

  # Optional: Clean up temporary files
