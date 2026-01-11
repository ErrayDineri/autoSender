"""
TEST - Meeting Announcement
Sends meeting announcement to test.csv recipients
"""
import os
from main import EmailSender, load_config

def main():
    print("=== TEST - Meeting Announcement ===\n")
    
    # Load configuration
    smtp_server, smtp_port, sender_email, sender_password = load_config()
    
    if not sender_email or not sender_password:
        print("⚠️  CONFIGURATION NEEDED:")
        print("Please ensure your .env file contains email credentials")
        return
    
    print(f"📧 Using email: {sender_email}")
    print(f"🌐 SMTP server: {smtp_server}:{smtp_port}")
    
    # Check if test.csv exists
    if not os.path.exists("test.csv"):
        print("❌ test.csv not found!")
        return
    
    # Check if template exists
    if not os.path.exists("MeetingAnnouncement.txt"):
        print("❌ MeetingAnnouncement.txt not found!")
        return
    
    # Ask for confirmation
    response = input("\nSend TEST meeting announcement? (y/n): ").lower().strip()
    if response != 'y':
        print("Test cancelled.")
        return
    
    print("\nStarting test bulk email sending...\n")
    
    # Initialize email sender
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)
    
    # Read test recipients to show count
    test_emails = email_sender.read_csv_emails("test.csv")
    if not test_emails:
        print("No emails found in test.csv")
        return
    
    print(f"Sending ONE test email to ALL {len(test_emails)} test recipients\n")
    
    # Create a modified version that adds TEST prefix to subject
    class TestEmailSender(EmailSender):
        def send_bulk_email(self, csv_file: str, template_file: str, subject_suffix: str):
            # Read emails and template
            emails = self.read_csv_emails(csv_file)
            template = self.read_template(template_file)
            
            if not template:
                print(f"Cannot send emails: template from {template_file} is empty")
                return
            
            if not emails:
                print(f"No emails found in {csv_file}")
                return
            
            # For bulk emails, use generic greeting without personalization
            generic_message = template.replace('[X]', 'Chers membres du Pôle Projet')
            
            # Create subject with TEST prefix
            subject = f"TEST - Sesame Junior Entreprise - {subject_suffix}"
            
            # Collect all email addresses
            all_recipients = []
            for name, mail_sesame, mail_autre in emails:
                all_recipients.append(mail_sesame)
                if mail_autre:
                    all_recipients.append(mail_autre)
            
            # Remove duplicates while preserving order
            unique_recipients = []
            seen = set()
            for email in all_recipients:
                if email not in seen:
                    unique_recipients.append(email)
                    seen.add(email)
            
            print(f"Sending bulk TEST email from {csv_file} to {len(unique_recipients)} recipients...")
            print(f"Recipients: {', '.join(unique_recipients)}")
            
            # Send one email to all recipients
            self.send_email(unique_recipients, subject, generic_message, subject_suffix, "all_test_members")
    
    # Use the test version
    test_email_sender = TestEmailSender(smtp_server, smtp_port, sender_email, sender_password)
    test_email_sender.send_bulk_email(
        csv_file="test.csv",
        template_file="MeetingAnnouncement.txt",
        subject_suffix="Réunion Pôle Projet - Ce soir 20h00"
    )
    
    print(f"\nTest completed! Sent one bulk email to all {len(test_emails)} test recipients.")

if __name__ == "__main__":
    main()
