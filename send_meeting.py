"""
Meeting Announcement Sender
Sends meeting announcements to Projet members from Projet.csv
"""
import os
from main import EmailSender, load_config

def main():
    print("=== Meeting Announcement - Email Sender ===\n")
    
    # Load configuration
    smtp_server, smtp_port, sender_email, sender_password = load_config()
    
    if not sender_email or not sender_password:
        print("⚠️  CONFIGURATION NEEDED:")
        print("Please ensure your .env file contains email credentials")
        return
    
    print(f"📧 Using email: {sender_email}")
    print(f"🌐 SMTP server: {smtp_server}:{smtp_port}")
    
    # Check if Projet.csv exists
    if not os.path.exists("Projet.csv"):
        print("❌ Projet.csv not found!")
        return
    
    # Check if template exists
    if not os.path.exists("MeetingAnnouncement.txt"):
        print("❌ MeetingAnnouncement.txt not found!")
        return
    
    # Ask for confirmation
    response = input("\nReady to send meeting announcement to Projet members? (y/n): ").lower().strip()
    if response != 'y':
        print("Operation cancelled.")
        return
    
    print("\nStarting bulk meeting announcement...\n")
    
    # Initialize email sender and send bulk email
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)
    email_sender.send_bulk_email(
        csv_file="Projet.csv",
        template_file="MeetingAnnouncement.txt",
        subject_suffix="Réunion Pôle Projet - Ce soir 20h00"
    )
    
    print("\nMeeting announcement sent!")

if __name__ == "__main__":
    main()
