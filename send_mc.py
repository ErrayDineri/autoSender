"""
Welcome Email Sender for Marketing Commercial Pole
Sends welcome emails to new MC members from MC.csv
"""
import os
from main import EmailSender, load_config

def main():
    print("=== 📧 Marketing Commercial - Welcome Email Sender ===\n")
    
    # Load configuration
    smtp_server, smtp_port, sender_email, sender_password = load_config()
    
    if not sender_email or not sender_password:
        print("⚠️  CONFIGURATION NEEDED:")
        print("Please ensure your .env file contains email credentials")
        return
    
    print(f"📧 Using email: {sender_email}")
    print(f"🌐 SMTP server: {smtp_server}:{smtp_port}")
    
    # Check if MC.csv exists
    if not os.path.exists("MC.csv"):
        print("❌ MC.csv not found!")
        return
    
    # Check if template exists
    if not os.path.exists("templateMC.txt"):
        print("❌ templateMC.txt not found!")
        return
    
    # Ask for confirmation
    response = input("\n🚀 Ready to send Marketing Commercial welcome emails? (y/n): ").lower().strip()
    if response != 'y':
        print("Operation cancelled.")
        return
    
    # Initialize email sender and send
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)
    email_sender.process_csv_and_send(
        csv_file="MC.csv",
        template_file="templateMC.txt",
        subject_suffix="Pole Marketing Commercial"
    )
    
    print("\n✅ Marketing Commercial emails processed!")

if __name__ == "__main__":
    main()
