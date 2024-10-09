import os
import subprocess
import shutil
import getpass
import stat
from cryptography.fernet import Fernet

# Encryption key setup for sensitive files
key = Fernet.generate_key()
cipher_suite = Fernet(key)


def print_current_directory():
    current_path = os.getcwd()
    print(f"\nCurrent Directory: {current_path}")
    print("Directory Levels:")
    for root, dirs, files in os.walk(current_path):
        level = root.replace(current_path, "").count(os.sep)
        indent = " " * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")


def set_file_permissions(file_path):
    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)


def create_folder():
    folder_name = input("Enter folder name: ")
    os.makedirs(folder_name, exist_ok=True)
    print(f"Folder '{folder_name}' created.")
    print_current_directory()


def create_file():
    while True:
        file_name = input("Enter file name: ")
        if os.path.exists(file_name):
            print(f"File '{file_name}' already exists. Please enter a different name.")
        else:
            with open(file_name, "w") as file:
                file.write("")
            print(f"File '{file_name}' created.")
            break
    print_current_directory()


def delete_file_or_folder():
    path = input("Enter file/folder name to delete: ")
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f"Folder '{path}' deleted.")
    elif os.path.isfile(path):
        os.remove(path)
        print(f"File '{path}' deleted.")
    else:
        print(f"'{path}' does not exist.")
    print_current_directory()


def clone_git_repo():
    repo_url = input("Enter Git repository URL: ")
    subprocess.run(["git", "clone", repo_url])
    print(f"Repository '{repo_url}' cloned.")
    print_current_directory()


def har_edit():
    print("Available files:")
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            print(f"{root}>{file}")
    file_name = input("Enter file name to edit: ")
    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            file.write("")
    edit_file(file_name)


def edit_file(file_name):
    print(f"Editing file: {file_name}")
    print("Type your content below (type 'har_edit_exit()' to save and exit):")
    content = []
    while True:
        line = input()
        if line == "har_edit_exit()":
            break
        content.append(line)
    with open(file_name, "w") as file:
        file.write("\n".join(content))
    print(f"File '{file_name}' saved.")
    print_current_directory()


def har_list():
    print("\nAvailable Directories and Sizes:")
    for root, dirs, files in os.walk(os.getcwd()):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(dir_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            print(f"{dir_name}: {total_size / (1024 * 1024):.2f} MB")
    change_directory()


def change_directory():
    new_path = input("Enter the path of the directory to change to: ")
    if os.path.isdir(new_path):
        os.chdir(new_path)
        print(f"Changed directory to {new_path}")
    else:
        print(f"Directory '{new_path}' does not exist.")
    print_current_directory()


def run_python_files():
    print("Available Python files:")
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".py"):
                print(f"{root}>{file}")
    file_name = input("Enter the Python file to run: ")
    if os.path.exists(file_name):
        subprocess.run(["python", file_name])
    else:
        print(f"File '{file_name}' does not exist.")


def create_encrypted_file():
    file_name = input("Enter the file name to create: ")
    password = getpass.getpass("Set a password for this file: ")
    content = input("Enter the content for the file: ")
    encrypted_content = cipher_suite.encrypt(content.encode())
    hex_content = encrypted_content.hex()  # Convert to hexadecimal
    with open(file_name, "w") as file:
        file.write(hex_content)
    set_file_permissions(file_name)
    print(
        f"Encrypted file '{file_name}' created and stored securely in hexadecimal format."
    )
    print_current_directory()


def decrypt_file():
    file_name = input("Enter the file name to decrypt: ")
    if not os.path.exists(file_name):
        print("File does not exist.")
        return
    password = getpass.getpass("Enter password to decrypt the file: ")
    with open(file_name, "r") as file:
        hex_content = file.read()
        encrypted_content = bytes.fromhex(
            hex_content
        )  # Convert from hexadecimal back to bytes
        try:
            decrypted_content = cipher_suite.decrypt(encrypted_content).decode()
            print(f"Decrypted content:\n{decrypted_content}")
        except Exception as e:
            print("Failed to decrypt file. Incorrect password or corrupted file.")
            print(e)


def main():
    while True:
        print("\nFile Management System")
        print("1. Create Folder")
        print("2. Create File")
        print("3. Delete File/Folder")
        print("4. Clone Git Repository")
        print("5. Har Edit")
        print("6. List Directories and Sizes (har-list)")
        print("7. Change Directory")
        print("8. Run Python Files")
        print("9. Create Encrypted File")
        print("10. Decrypt File")
        print("11. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            create_folder()
        elif choice == "2":
            create_file()
        elif choice == "3":
            delete_file_or_folder()
        elif choice == "4":
            clone_git_repo()
        elif choice == "5":
            har_edit()
        elif choice == "6":
            har_list()
        elif choice == "7":
            change_directory()
        elif choice == "8":
            run_python_files()
        elif choice == "9":
            create_encrypted_file()
        elif choice == "10":
            decrypt_file()
        elif choice == "11" or choice.lower() == "exit":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
