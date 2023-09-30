import string, secrets, re
from imapclient import IMAPClient

def passgen() -> str:
    letters = string.ascii_letters
    digits = string.digits
    alphabet = digits + letters
    password = ''
    for i in range(0, 16):
        password += ''.join(secrets.choice(alphabet))
    return password

def parse(filename) -> list:
    result = []
    with open(filename, 'r') as f:
        for line in f:
            result.append(line.strip())
    return result

def email_link(login, password) -> str:
    client = IMAPClient('imap.mail.ru', use_uid=True) 
    client.login(login, password)
    client.select_folder('INBOX')
    message = str(client.fetch(client.search(['FROM', 'forwarding-noreply@google.com']), 'RFC822'))
    print(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)[0].split('\\')[0])