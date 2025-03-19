#!/bin/env -S python3

import google.generativeai as genai
import os
import argparse
import sys
import mimetypes  # Import the mimetypes library

# Configure your API key (replace with your actual key)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to send the file(s) to Gemini and get the description
def get_description(file_paths, prompt, model_name):
    model = genai.GenerativeModel(model_name=model_name)
    sample_files = []

    # Upload each file
    for file_path in file_paths:
        try:
            # Get MIME type, handling potential None
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                print(f"Warning: Could not determine MIME type for '{file_path}'.  Using 'application/octet-stream'.", file=sys.stderr)
                mime_type = 'application/octet-stream'

            # Upload the file WITH the determined (or default) MIME type.
            sample_file = genai.upload_file(path=file_path, display_name=os.path.basename(file_path), mime_type=mime_type)
            sample_files.append(sample_file)

        except Exception as e:
            print(f"Error uploading file '{file_path}': {e}", file=sys.stderr)  # Error to stderr
            return None  # Return None on upload error.

    try:
        # Send request to generate description
        response = model.generate_content([*sample_files, prompt])
        return response.text
    except Exception as e:
        print(f"Error generating description: {e}", file=sys.stderr)
        return None

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

    # Model arguments
    model_group = parser.add_argument_group('Model Selection')
    model_group.add_argument('--flash', action='store_true', help='Use gemini-1.5-flash')
    model_group.add_argument('--flash8b', action='store_true', help='Use gemini-1.5-flash-8b')
    model_group.add_argument('--pro', action='store_true', help='Use gemini-1.5-pro')
    model_group.add_argument('--flash2', action='store_true', help='Use gemini-2.0-flash')
    model_group.add_argument('--flash2lite', action='store_true', help='Use gemini-2.0-flash-lite')
    model_group.add_argument('--pro2exp', action='store_true', help='Use gemini-2.0-pro-exp-02-05')
    model_group.add_argument('--embedding', action='store_true', help='Use gemini-embedding-exp')
    model_group.add_argument('--model', type=str, default=None, help='Specify exact model name')

    # Optional argument for brief answer
    parser.add_argument(
        '--brief',
        action='store_true',
        help='If set, the response will be brief'
    )

    args = parser.parse_args()

    # Determine the model name (prioritized)
    if args.model:
        model_name = args.model
    elif args.flash:
        model_name = "gemini-1.5-flash"
    elif args.flash8b:
        model_name = "gemini-1.5-flash-8b"
    elif args.pro:
        model_name = "gemini-1.5-pro"
    elif args.flash2:
        model_name = "gemini-2.0-flash"
    elif args.flash2lite:
        model_name = "gemini-2.0-flash-lite"
    elif args.pro2exp:
        model_name = "gemini-2.0-pro-exp-02-05"
    elif args.embedding:
        model_name = "gemini-embedding-exp"
    else:
        model_name = "gemini-1.5-pro"  # Default

    if args.prompt:
        prompt = args.prompt
    else:
        prompt = "Provide a brief explanation." if args.brief else "Provide a detailed explanation."

    invalid_files = [file for file in args.files if not os.path.isfile(file)]
    if invalid_files:
        print(f"Error: Invalid file paths: {', '.join(invalid_files)}", file=sys.stderr)
        parser.print_help(file=sys.stderr)
        exit(1)

    description = get_description(args.files, prompt, model_name)
    print("-" * 60, file=sys.stderr)
    print(f"Model Used: {model_name}", file=sys.stderr)
    if description:
        description_clean = description
        for delimiter in ["```json", "```"]:
            if delimiter in description_clean:
                print(delimiter, file=sys.stderr)
                description_clean = description_clean.replace(delimiter, "")
        print(description_clean)
    print("-" * 60, file=sys.stderr)

if __name__ == '__main__':
    main()