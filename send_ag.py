"""
Convocation Email Sender for AG (Assemblée Générale)
Sends convocation emails to all members from all.csv
"""
import os
from main import EmailSender, load_config

def main():
    print("=== 📧 AG Convocation - Email Sender ===\n")
    
    # Load configuration
    smtp_server, smtp_port, sender_email, sender_password = load_config()
    
    if not sender_email or not sender_password:
        print("⚠️  CONFIGURATION NEEDED:")
        print("Please ensure your .env file contains email credentials")
        return
    
    print(f"📧 Using email: {sender_email}")
    print(f"🌐 SMTP server: {smtp_server}:{smtp_port}")
    
    # Check if all.csv exists
    if not os.path.exists("all.csv"):
        print("❌ all.csv not found!")
        return
    
    # Check if template exists
    if not os.path.exists("ConvocationAGetVisite.txt"):
        print("❌ ConvocationAGetVisite.txt not found!")
        return
    
    # Ask for confirmation
    response = input("\n🚀 Ready to send AG convocation emails to all members? (y/n): ").lower().strip()
    if response != 'y':
        print("Operation cancelled.")
        return
    
    # Initialize email sender and send bulk email to all members
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)
    email_sender.send_bulk_email(
        csv_file="all.csv",
        template_file="ConvocationAGetVisite.txt",
        subject_suffix="Convocation - AG et Visite CTJE"
    )
    
    print("\n✅ AG Convocation emails processed!")

if __name__ == "__main__":
    main()
