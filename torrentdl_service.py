import os
import paramiko
import time
import subprocess

host = os.environ.get('HOST')
port = os.environ.get('PORT')
username = os.environ.get('USERNAME')
private_key_path = os.environ.get('PRIVATE_KEY_PATH')
remote_dir = os.environ.get('REMOTE_DIR')

def process_lftp_file(file_path):
    # Run 'lftp -l file.lfp' command]
    command = ['lftp', '-f', file_path]
    try:
        print(f"Processing file: {file_path}")
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print(f"Failed to process file: {file_path}")
        print(e.output.decode())

def delete_remote_file(sftp, file_path):
    sftp.remove(file_path)
    print(f"Deleted remote file: {file_path}")

def download_and_process_files(host, username, private_key_path, remote_dir):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    private_key = paramiko.Ed25519Key(filename=private_key_path)
    ssh.connect(hostname=host, username=username, pkey=private_key, port=port)

    sftp = ssh.open_sftp()
    no_files_message_logged = False  # Flag to track if the message has been logged

    while True:
        files = sftp.listdir(remote_dir)

        if not files:
            if not no_files_message_logged:
                print("No files left in the remote directory. Waiting for new files...")
                no_files_message_logged = True
            time.sleep(10)
            continue

        file_path = files[0]
        local_directory = "lftp_files"
        local_file_path = os.path.join(local_directory, file_path)

        # Create the local directory if it doesn't exist
        if not os.path.exists(local_directory):
            os.makedirs(local_directory)

        sftp.get(os.path.join(remote_dir, file_path), local_file_path)
        print(f"Get: {file_path}")

        process_lftp_file(local_file_path)

        delete_remote_file(sftp, os.path.join(remote_dir, file_path))
        no_files_message_logged = False

    sftp.close()
    ssh.close()

download_and_process_files(host, username, private_key_path, remote_dir)
