import imaplib
import email
from email.header import decode_header

# Get user input for email credentials
email_user = input("Enter your email address: ")
email_password = input("Enter your email password: ")

# Connect to Gmail's IMAP server
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(email_user, email_password)
mail.select("inbox")

# Search for emails with specific keywords and date range
status, msg_ids = mail.search(None, "ALL")
msg_ids = msg_ids[0].split()
msg_ids.reverse()  # Reverse the list of message IDs

for msg_id in msg_ids:
    try:
        # Fetch email details
        status, msg_data = mail.fetch(msg_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        # Decode email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        # Create a folder based on the decoded subject
        target_folder = subject.strip().replace(" ", "_")  # Modify this as needed
        target_folder = target_folder[:30]  # Limit folder name length if necessary

        print(f"Subject: {subject}, Target Folder: {target_folder}")

        # Check if the target folder exists, and create it if not
        folders = [folder.decode().split('"')[-2] for folder in mail.list()[1]]
        if target_folder not in folders:
            mail.create(target_folder)
            print(f"Created folder: {target_folder}")

        # Move email to the target folder
        mail.copy(msg_id, target_folder)
        mail.store(msg_id, "+FLAGS", "\\Deleted")
        mail.expunge()

        print(f"Email '{subject}' moved to '{target_folder}'")
    except Exception as e:
        print(f"Error processing email {msg_id}: {e}")

# Disconnect from the server
mail.logout()
