import streamlit as st
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Auth:
    users_file = 'users.json'

    def __init__(self):
        self.file_path = 'users.json'

    def load_users(self):
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}  # Return an empty dictionary if JSON is invalid

    def save_users(self, users):
        with open(self.users_file, 'w') as file:
            json.dump(users, file, indent=4)

    def create_account(self, email, password, password_confirm):
        users = self.load_users()

        if email in users:
            return "Email already registered."
        
        if password != password_confirm:
            return "Passwords do not match."

        users[email] = {'password': password}
        self.save_users(users)
        return "Account created successfully."

    def login(self, email, password):
        users = self.load_users()

        if email not in users:
            return "Email not registered."

        if users[email]['password'] != password:
            return "Incorrect password."

        return "Login successful."

    def reset_password(self, email):
        users = self.load_users()

        if email not in users:
            return "Email not registered."

        # Send reset email
        reset_link = f"http://example.com/reset_password?email={email}"  # Dummy link, implement actual reset link
        self.send_reset_email(email, reset_link)
        return "Password reset email sent."

    def send_reset_email(self, email, reset_link):
        sender_email = "your-email@example.com"
        receiver_email = email
        password = "your-email-password"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Password Reset"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = f"Please reset your password using the following link: {reset_link}"
        html = f"<html><body><p>Please reset your password using the following link: <a href='{reset_link}'>Reset Password</a></p></body></html>"

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        with smtplib.SMTP_SSL("smtp.example.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return "Email sent."

# Jalankan aplikasi dengan perintah:
# streamlit run App.py
