#!/usr/bin/python3
import os
import sys
import re

# Constant Variables
TORRENT_PATH = sys.argv[1]
OUTPUT_PATH = "PATH for generated files"
SFTP_HOST = "SFTP host"
SFTP_PORT = "SFP port"
SFTP_USER = "SFTP user"
SSH_KEY_PATH = "PATH for the ssh-key"

# Config variables
THREAD_NUMBER = 20
ALLOWED_TAGS = ['Movie', 'Serie', 'Tv-show']
TAG = 'Other'  # Default TAG

# TAG can be 'anything'
if len(sys.argv) >= 3:
    TAG = sys.argv[2]
elif TAG not in ALLOWED_TAGS:
    TAG = 'Other'

# Sanitize function
def sanitize(variable):
    # Remove all non-alphanumeric characters using regular expressions
    filename = re.sub(r'\W+', '', variable)

    # Replace spaces with underscores and add extension
    filename = filename.replace(' ', '_')
    filename = filename + ".lftp"

    return filename

# Get the basename from the TORRENT_PATH
torrent_name = os.path.basename(TORRENT_PATH)
# Get the filename
filename = sanitize(torrent_name)
# Set output file
output_path = os.path.join(OUTPUT_PATH, filename)

# Create the lftp command based on the file or directory
if os.path.isdir(TORRENT_PATH):
    # Directory case
    lftp_command_torrent = '\n'.join([
        f'''lcd /Incoming/{TAG}''',
        f'''mirror -c --use-pget-n={THREAD_NUMBER} "{torrent_name}"''',
        f'''local chmod -R 777 "{torrent_name}"'''
    ])

else:
    # File case
    lftp_command_torrent = '\n'.join([
        f'''lcd /Incoming/{TAG}''',
        f'''pget -c -n {THREAD_NUMBER} "{torrent_name}"''',
        f'''local chmod 777 "{torrent_name}"'''
    ])

lftp_command = '\n'.join([
    f'''set sftp:auto-confirm yes''',
    f'''set sftp:connect-program "ssh -a -x -i {SSH_KEY_PATH} -o StrictHostKeyChecking=no"''',
    f'''open -u {SFTP_USER}, sftp://{SFTP_HOST}:{SFTP_PORT}''',
    f'''cd download''',
    lftp_command_torrent
])

# Write the command to the file named CMD_FILE
with open(output_path, 'w') as file:
    file.write(lftp_command)
