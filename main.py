import requests
import hashlib

def check_password_leak(password):
    sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    
    if response.status_code == 200:
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return count
    return 0

def main():
    with open("user_passwords.txt", "r") as file:
        for line in file:
            username, password = line.strip().split(',')
            leak_count = check_password_leak(password)
            if leak_count:
                print(f"Password for user {username} has been leaked {leak_count} times!")
            else:
                print(f"Password for user {username} is secure.")

if __name__ == "__main__":
    main()
