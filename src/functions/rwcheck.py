import os
from functions import script


def check_source_readable(SOURCE_DIR):
    script.info_msg("Testing source dir is readable...")

    # Check if source dir exists
    if not os.path.exists(SOURCE_DIR):
        script.err_msg("Source directory does not exist! Program will now exit...")
        return False

    # Check if path is dir or file
    if not os.path.isdir(SOURCE_DIR):
        script.err_msg("Source path is not a directory. Program will now exit...")
        return False

    unreadable_files = []
    for root, dirs, files in os.walk(os.path.abspath(SOURCE_DIR)):
        for file in files:
            if not os.access(os.path.join(root,file), os.R_OK):
                bad_file = os.path.join(root,file)
                unreadable_files.append(bad_file)
    if len(unreadable_files) == 0:
        script.ok_msg("Source directory is readable.")
        return True
    else:
        script.err_msg("The following file(s) are unreadable: \n")
        print(*unreadable_files, sep = "\n")
        print("\n\nProgram will now exit\n\n")
        exit()


def check_source_writable(SOURCE_DIR):
    print("\n\n")
    script.info_msg("Checking source directory is writable...")


    # Attempt to create the source dir if its missing
    # Write test file fails if dir doesn't exist
    try:
        os.system("mkdir -p " + SOURCE_DIR)
    except:
        script.err_msg("Cannot create source directory")


    # Attempt to write a test file
    try:
        test_content = "fghty7kfgh!RT*dfgju09"
        test_file_path = f"{SOURCE_DIR}/write_test.txt"
        
        with open(test_file_path, 'w') as test_file:
            test_file.write(test_content)
    except:        
        script.err_msg("The source directory is not writable.")
        print("\n\nProgram will now exit\n\n")
        exit()


    # Attempt to read the test file back
    with open(test_file_path, 'r') as test_file:
        read_content = test_file.read()


    # Check if the read content matches the written content
    if read_content == test_content:
        os.remove(test_file_path)
        print(script.ok_msg("The source is writable."))

        return True
    else:
        script.err_msg("The source directory is not writable.")
        print("\n\nProgram will now exit\n\n")
        exit()



def check_destination_readable(RECOVERY_ZIP):
    print("\n\n")
    script.info_msg("Checking recovery archive is readable...")

    
    if os.access(RECOVERY_ZIP, os.R_OK) is True:
        script.ok_msg("Recovery archive is readable.\n\n")
        return True
    else:
        script.err_msg("Recovery archive path is not readable. Program will now exit...")
        print("If applicable, check if you have a valid kerberos token or copy the ZIP to local disk and retry.\n")
        exit()



def check_destination_writable(DEST_DIR):
    print("\n\n")
    script.info_msg("Testing destination dir is writable...")

    try:
        # Attempt to write a test file
        test_content = "fghty7kfgh!RT*dfgju09"
        test_file_path = f"{DEST_DIR}/write_test.txt"
        
        with open(test_file_path, 'w') as test_file:
            test_file.write(test_content)
    except:        
        script.err_msg("The destination directory is not writable.")
        print("\n\nProgram will now exit\n\n")
        exit()

    # Attempt to read the test file back
    with open(test_file_path, 'r') as test_file:
        read_content = test_file.read()

    # Check if the read content matches the written content
    if read_content == test_content:
        os.remove(test_file_path)
        print(script.ok_msg("The destination is writable.\n\n"))

        return True
    else:
        script.err_msg("The destination directory is not writable.")
        print("\n\nProgram will now exit\n\n")
        exit()
                
