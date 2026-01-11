"""
Welcome Email Sender for Projet Pole
Sends welcome emails to new Projet members from Projet.csv
"""
import os
from main import EmailSender, load_config

def main():
    print("=== 📧 Projet - Welcome Email Sender ===\n")
    
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
    if not os.path.exists("templateProjet.txt"):
        print("❌ templateProjet.txt not found!")
        return
    
    # Ask for confirmation
    response = input("\n🚀 Ready to send Projet welcome emails? (y/n): ").lower().strip()
    if response != 'y':
        print("Operation cancelled.")
        return
    
    # Initialize email sender and send
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)
    email_sender.process_csv_and_send(
        csv_file="Projet.csv",
        template_file="templateProjet.txt",
        subject_suffix="Pole Projet"
    )
    
    print("\n✅ Projet emails processed!")

if __name__ == "__main__":
    main()
