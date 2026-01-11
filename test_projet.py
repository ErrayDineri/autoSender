"""
TEST - Projet Welcome Emails
Sends Projet welcome emails to test.csv recipients
"""
import os
from main import EmailSender, load_config

def main():
    print("=== 🧪 TEST - Projet Welcome Emails ===\n")
    
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
    if not os.path.exists("templateProjet.txt"):
        print("❌ templateProjet.txt not found!")
        return
    
    # Ask for confirmation
    response = input("\n🧪 Send TEST Projet emails? (y/n): ").lower().strip()
    if response != 'y':
        print("❌ Test cancelled.")
        return
    
    print("\n🚀 Starting test email sending...\n")
    
    # Initialize email sender
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)
    
    # Read test recipients
    test_emails = email_sender.read_csv_emails("test.csv")
    
    if not test_emails:
        print("❌ No emails found in test.csv")
        return
    
    print(f"📧 Found {len(test_emails)} test recipients\n")
    
    # Read template
    template = email_sender.read_template("templateProjet.txt")
    if not template:
        print("❌ Template is empty")
        return
    
    # Send test emails
    for name, mail_sesame, mail_autre in test_emails:
        personalized_message = email_sender.personalize_message(template, name)
        
        recipients = [mail_sesame]
        if mail_autre:
            recipients.append(mail_autre)
        
        subject = "🧪 TEST - 🎉 Bienvenue à Sesame Junior Entreprise - Pole Projet"
        
        print(f"📤 Sending Projet test email to {name}...")
        email_sender.send_email(recipients, subject, personalized_message, "Pole Projet", name)
    
    print(f"\n✅ Test completed! Sent {len(test_emails)} test emails.")

if __name__ == "__main__":
    main()
