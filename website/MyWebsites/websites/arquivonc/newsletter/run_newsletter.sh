#!/bin/zsh

# Define the path to your Python script
SCRIPT_PATH="/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/newsletter/newsletter.py"

# Check if the Python script exists
if [[ ! -f "$SCRIPT_PATH" ]]; then
  echo "Error: $SCRIPT_PATH does not exist."
  exit 1
fi

# Run the Python script
python3 "$SCRIPT_PATH"

# Check if the script ran successfully
if [[ $? -ne 0 ]]; then
  echo "Error: Python script failed to run."
  exit 1
fi

echo "Python script ran successfully."
