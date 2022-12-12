# FGT-New-password-api-create
Using pexpect to add default password and create api-user and generate api token

This script uses pexpect against a FortiGate firewall after being factory reset.

Step 1: It creates an ssh tunnel, accepts the new SSH key into the key repository
Step 2: It sets the new password to your desired admin passowrd
Step 3: Creates api user profile with desired read-write privileges and your desired name.
Step 4: Crerate api user with desired name.
Step 5: Set new profile to the new uses
Step 6: Generates the API key and prints it out.

This was created on MACOS using python3

Created by Andy Faulkner AKA "The EvilBastard"
