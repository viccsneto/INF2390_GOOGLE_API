#!/bin/env -S python3

import google.generativeai as genai
import os
import argparse

# Configure your API key (replace with your actual key)
# genai.configure(api_key="AIzaSy************************XlsElsLOs")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to send the file(s) to Gemini and get the description
def get_description(file_paths, prompt, model_name):
    model = genai.GenerativeModel(model_name=model_name)  # Use the specified model name
    sample_files = []

    # Upload each file
    for file_path in file_paths:
        try:
            sample_file = genai.upload_file(path=file_path, display_name=os.path.basename(file_path))
            sample_files.append(sample_file)
        except Exception as e:
            return f"Error uploading file '{file_path}': {e}"

    try:
        # Send request to generate description
        response = model.generate_content([*sample_files, prompt])
        return response.text
    except Exception as e:
        return f"Error generating description: {e}"  # Handle potential errors

# Main function
def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(
        description="Upload one or more files to Google APIs and get a description or explanation. "
                    "Provide an optional prompt for the explanation, or use the default prompt."
    )

    # Required positional argument for files
    parser.add_argument(
        'files',
        metavar='file',
        type=str,
        nargs='+',
        help='One or more file paths to be uploaded and analyzed'
    )

    # Optional argument for the prompt
    parser.add_argument(
        '-p', '--prompt',
        type=str,
        default=None,
        help='Optional custom prompt to guide the explanation'
    )

    # Optional argument to use the gemini-1.5-flash model
    parser.add_argument(
        '--flash',
        action='store_true',
        help='Use the gemini-1.5-flash model instead of the default gemini-1.5-pro'
    )

    # Optional argument to use the gemini-1.5-flash-8b-exp-0827 model
    parser.add_argument(
        '--flashier',
        action='store_true',
        help='Use the gemini-1.5-flash-8b-exp-0827 model instead of the default or flash model'
    )

    # Optional argument to specify any model name
    parser.add_argument(
        '--model',
        type=str,
        default=None,
        help='Specify the exact model name to use (overrides --flash and --flashier if provided)'
    )

    # Optional argument for brief answer
    parser.add_argument(
        '--brief',
        action='store_true',
        help='If set, the response will be brief instead of detailed'
    )

    # Parse the arguments
    args = parser.parse_args()

    # Determine the model name
    if args.model:
        model_name = args.model
    elif args.flashier:
        model_name = "gemini-1.5-flash-8b-exp-0827"
    elif args.flash:
        model_name = "gemini-1.5-flash"
    else:
        model_name = "gemini-1.5-pro"

    # Adjust the prompt for a brief response if --brief is set
    if args.prompt:
        prompt = args.prompt
    else:
        if args.brief:
            prompt = "Provide a brief explanation of the uploaded content."
        else:
            prompt = "Provide a detailed explanation of the uploaded content."

    # Verify that all provided paths are valid files
    invalid_files = [file for file in args.files if not os.path.isfile(file)]
    if invalid_files:
        print(f"Error: The following file paths are invalid: {', '.join(invalid_files)}")
        parser.print_help()
        exit(1)

    # Get and print the description
    description = get_description(args.files, prompt, model_name)
    print("--------------------------------------------------------------------")
    print(f"Model Used: {model_name}")
    print(description)
    print("--------------------------------------------------------------------")

if __name__ == '__main__':
    main()
