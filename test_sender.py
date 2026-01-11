import random
import os
from dotenv import load_dotenv
from main import EmailSender, load_config

def main():
    """
    Test function - sends random templates to test.csv recipients
    """
    print("=== 🧪 Sesame Junior Entreprise - TEST Email Sender ===\n")
    
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
    
    # Define available templates
    templates = []
    if os.path.exists("templateMC.txt"):
        templates.append(("templateMC.txt", "Pole Marketing Commercial"))
    if os.path.exists("templateProjet.txt"):
        templates.append(("templateProjet.txt", "Pole Projet"))
    if os.path.exists("ConvocationAGetVisite.txt"):
        templates.append(("ConvocationAGetVisite.txt", "Convocation - AG et Visite CTJE"))
    
    if not templates:
        print("❌ No templates found!")
        return
    
    print(f"📋 Available templates: {[t[1] for t in templates]}")
    
    # Ask for confirmation
    response = input("\n🧪 Send test emails with random templates? (y/n): ").lower().strip()
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
    
    # Send emails with random templates
    for name, mail_sesame, mail_autre in test_emails:
        # Randomly select a template
        template_file, subject_suffix = random.choice(templates)
        
        # Read and personalize template
        template = email_sender.read_template(template_file)
        if not template:
            print(f"⚠️  Skipping {name} - template {template_file} is empty")
            continue
        
        personalized_message = email_sender.personalize_message(template, name)
        
        # Prepare recipients
        recipients = [mail_sesame]
        if mail_autre:
            recipients.append(mail_autre)
        
        # Create test subject with TEST prefix
        if "Pole" in subject_suffix:
            subject = f"🧪 TEST - 🎉 Bienvenue à Sesame Junior Entreprise - {subject_suffix}"
        else:
            subject = f"🧪 TEST - 📧 Sesame Junior Entreprise - {subject_suffix}"
        
        # Send email
        print(f"📤 Sending {template_file} to {name}...")
        email_sender.send_email(recipients, subject, personalized_message, subject_suffix, name)
    
    print(f"\n✅ Test completed! Sent {len(test_emails)} test emails with random templates.")

if __name__ == "__main__":
    main()