import os
import hashlib

# CWE-327: Use of broken cryptographic algorithm
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# CWE-259: Hardcoded password
ADMIN_PASSWORD = "changeme123"

# CWE-22: Path traversal
def get_user_file(username):
    filepath = os.path.join("/var/data", username)
    with open(filepath) as f:
        return f.read()

# CWE-676: Use of potentially dangerous function
def process_input(data):
    return eval(data)
# test 1784737491
