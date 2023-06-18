import os
import urllib.parse
import sys
import re

# Constant Variables
TORRENT_PATH = sys.argv[1]

# Config variables
URL = "Enter you URL here - with trailing /"
THREAD_NUMBER = 20
ALLOWED_TAGS = ['Movie', 'Serie', 'Tv-show']

# TAG can be 'anything'
if len(sys.argv) >= 3:
    TAG = sys.argv[2]
elif TAG not in allowed_tags:
    TAG = 'Other'
else:
    TAG = 'Other'

# Sanitize function
def sanitize_and_convert(variable):
    # Remove all non-alphanumeric characters using regular expressions
    filename = re.sub(r'\W+', '', variable)

    # Replace spaces with underscores and add extension
    filename = filename.replace(' ', '_')
    filename = filename + ".lftp"

    # Convert the variable to HTML/URL format
    url_name = urllib.parse.quote(variable)

    return filename, url_name

# Get the basename from the TORRENT_PATH
torrent_name = os.path.basename(TORRENT_PATH)

filename, url_name = sanitize_and_convert(torrent_name)

# Create the lftp command based on the file or directory
if os.path.isdir(TORRENT_PATH):
    # Directory case
    lftp_command = '\n'.join([
        f"!cd {TAG}",
        f"mirror --use-pget-n={THREAD_NUMBER} {URL}{url_name}"
    ])
else:
    # File case
    lftp_command = '\n'.join([
        f"!cd {TAG}",
        f"pget -n {THREAD_NUMBER} {URL}{url_name}"
    ])

# Write the command to the file named CMD_FILE
with open(filename, 'w') as file:
    file.write(lftp_command)
