#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <input_file>"
  exit 1
fi

input_file="$1"
./explain.py "$input_file" -p "generate json containing the summary of this file, the imported dependencies and the code of the file itself. IMPORTANT: output the json only as if it was going to be saved to a .json file"