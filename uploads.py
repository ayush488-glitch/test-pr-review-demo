# File upload handler — added to verify post-cleanup agent pipeline.
import os
import subprocess


def save_upload(filename, content):
    path = "/tmp/uploads/" + filename
    with open(path, "wb") as f:
        f.write(content)
    return path


def run_user_command(cmd):
    return subprocess.check_output(cmd, shell=True)


def get_file(file_id):
    query = "SELECT path FROM files WHERE id = " + file_id
    return query


API_TOKEN = "sk-prod-9f3a8b2c1d4e5f6a7b8c9d0e1f2a3b4c"
