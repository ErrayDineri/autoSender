import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
import os
from typing import List, Tuple, Optional
from dotenv import load_dotenv

class EmailSender:
    def __init__(self, smtp_server: str, smtp_port: int, email: str, password: str):
        """
        Initialize the email sender with SMTP configuration
        
        Args:
            smtp_server: SMTP server address (e.g., 'smtp.gmail.com')
            smtp_port: SMTP port (e.g., 587 for TLS)
            email: Sender email address
            password: Sender email password or app password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
        self.cc_list = self.load_cc_list()
    
    def load_cc_list(self) -> List[str]:
        """
        Load carbon copy email list from cc.csv
        
        Returns:
            List of CC email addresses
        """
        cc_emails = []
        cc_file = "cc.csv"
        
        if not os.path.exists(cc_file):
            print(f"ℹ️  CC file {cc_file} not found, no carbon copies will be sent")
            return cc_emails
        
        try:
            with open(cc_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Handle None values safely
                    email = (row.get('email') or '').strip()
                    if email:
                        cc_emails.append(email)
            
            if cc_emails:
                print(f"📋 Loaded {len(cc_emails)} CC addresses from {cc_file}")
            
        except Exception as e:
            print(f"⚠️  Error reading {cc_file}: {str(e)}")
        
        return cc_emails
    
    def read_csv_emails(self, csv_file: str) -> List[Tuple[str, str, Optional[str]]]:
        """
        Read emails from CSV file
        
        Args:
            csv_file: Path to CSV file
            
        Returns:
            List of tuples (name, mailSesame, mailAutre)
        """
        emails = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Handle None values safely
                    name = (row.get('name') or '').strip()
                    mail_sesame = (row.get('mailSesame') or '').strip()
                    mail_autre = (row.get('mailAutre') or '').strip()
                    
                    if name and mail_sesame:  # Only add if both name and mailSesame exist
                        emails.append((name, mail_sesame, mail_autre if mail_autre else None))
        except FileNotFoundError:
            print(f"Error: File {csv_file} not found")
        except Exception as e:
            print(f"Error reading {csv_file}: {str(e)}")
        
        return emails
    
    def read_template(self, template_file: str) -> str:
        """
        Read email template from file
        
        Args:
            template_file: Path to template file
            
        Returns:
            Template content as string
        """
        try:
            with open(template_file, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: Template file {template_file} not found")
            return ""
        except Exception as e:
            print(f"Error reading template {template_file}: {str(e)}")
            return ""
    
    def personalize_message(self, template: str, name: str) -> str:
        """
        Replace [X] placeholder with the actual name
        
        Args:
            template: Email template
            name: Name to replace [X] with
            
        Returns:
            Personalized message
        """
        return template.replace('[X]', name)
    
    def convert_to_html(self, text: str, pole: str) -> str:
        """
        Convert plain text template to HTML with styling
        
        Args:
            text: Plain text template
            pole: Pole name for color theming
            
        Returns:
            HTML formatted message
        """
        # Use the requested colors for both poles
        primary_color = "#007cc1"  # Blue
        secondary_color = "#12c2d2"  # Light blue/cyan
        
        # Determine if this is a convocation/meeting email
        is_convocation = "Convocation" in pole or "AG" in pole
        is_meeting = "Réunion" in pole or "Meeting" in pole
        
        # Convert to HTML with styling
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                .email-container {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f9f9f9;
                }}
                .email-content {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .company-name {{
                    color: {primary_color};
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .pole-name {{
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    background: linear-gradient(135deg, {primary_color}, {secondary_color});
                    padding: 8px 16px;
                    border-radius: 20px;
                    display: inline-block;
                }}
                .greeting {{
                    font-size: 18px;
                    color: #333;
                    margin-bottom: 20px;
                }}
                .content {{
                    line-height: 1.6;
                    color: #555;
                    font-size: 16px;
                    margin-bottom: 15px;
                }}
                .highlight {{
                    color: {primary_color};
                    font-weight: bold;
                }}
                .important {{
                    background-color: #fff3cd;
                    border-left: 4px solid {secondary_color};
                    padding: 10px 15px;
                    margin: 15px 0;
                    border-radius: 5px;
                }}
                .congratulations {{
                    background: linear-gradient(135deg, {primary_color}, {secondary_color});
                    color: white;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .program {{
                    background: linear-gradient(to right, #f0f8ff, #e6f7ff);
                    border-left: 5px solid {primary_color};
                    border-right: 5px solid {secondary_color};
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    box-shadow: 0 3px 8px rgba(0, 124, 193, 0.15);
                }}
                .agenda-item {{
                    background-color: white;
                    padding: 12px 15px;
                    margin: 10px 0;
                    border-radius: 6px;
                    border-left: 3px solid {secondary_color};
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                }}
                .event-header {{
                    background: linear-gradient(135deg, {primary_color}, {secondary_color});
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                    margin: 20px 0;
                    box-shadow: 0 4px 10px rgba(0, 124, 193, 0.3);
                }}
                .meeting-info {{
                    background: linear-gradient(to bottom right, #f0f8ff, #ffffff);
                    border: 3px solid {secondary_color};
                    padding: 25px;
                    border-radius: 15px;
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(18, 194, 210, 0.2);
                }}
                .meeting-link {{
                    background: linear-gradient(135deg, {primary_color}, {secondary_color});
                    color: white;
                    padding: 15px 25px;
                    border-radius: 8px;
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                    margin: 15px 0;
                    box-shadow: 0 4px 10px rgba(0, 124, 193, 0.3);
                    text-decoration: none;
                    display: block;
                }}
                .meeting-link a {{
                    color: white;
                    text-decoration: none;
                }}
                .meeting-link:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 15px rgba(0, 124, 193, 0.4);
                }}
                .signature {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 2px solid {primary_color};
                }}
                .emoji {{
                    font-size: 1.2em;
                    margin-right: 5px;
                }}
                .date-info {{
                    background-color: #f0f8ff;
                    border-left: 4px solid {secondary_color};
                    padding: 15px;
                    border-radius: 8px;
                    margin: 15px 0;
                    font-size: 16px;
                    line-height: 1.8;
                }}
                .closing-message {{
                    background: linear-gradient(to bottom, #ffffff, #f0f8ff);
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    font-style: italic;
                    color: #333;
                    margin: 20px 0;
                    border: 2px solid {secondary_color};
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-content">
                    <div class="header">
                        <div class="company-name">Sesame Junior Entreprise</div>
                        <div class="pole-name">{pole}</div>
                    </div>
        """
        
        # Split text into paragraphs and format them
        paragraphs = text.strip().split('\n\n')
        
        for i, paragraph in enumerate(paragraphs):
            # Skip empty paragraphs
            if not paragraph.strip():
                continue
                
            # Check for greeting
            if i == 0 and ("Chers" in paragraph or "Bonsoir" in paragraph):
                html += f'<div class="greeting">{paragraph}</div>\n'
            # Meeting info detection (check for Date/Heure/Lien keywords or meeting links)
            elif is_meeting and (any(keyword in paragraph for keyword in ["Date :", "Heure :", "Lien de la réunion"]) or "https://" in paragraph or "meet.google.com" in paragraph):
                # Check if paragraph contains meeting link
                if "https://" in paragraph or "meet.google.com" in paragraph:
                    # Split into lines and format each
                    lines = paragraph.split('\n')
                    html += '<div class="meeting-info">\n'
                    for line in lines:
                        if "https://" in line or "meet.google.com" in line:
                            # Extract the link
                            import re
                            link_match = re.search(r'https://[^\s]+', line)
                            if link_match:
                                link = link_match.group(0)
                                html += f'<div class="meeting-link"><a href="{link}" target="_blank">Rejoindre la réunion</a></div>\n'
                            else:
                                html += f'<div style="margin: 8px 0; font-size: 17px;">{line}</div>\n'
                        else:
                            html += f'<div style="margin: 8px 0; font-size: 17px;">{line}</div>\n'
                    html += '</div>\n'
                else:
                    html += f'<div class="meeting-info">{paragraph.replace(chr(10), "<br>")}</div>\n'
            # Check for special event header (AG invitation)
            elif "cordialement conviés" in paragraph.lower():
                html += f'<div class="event-header">{paragraph}</div>\n'
            # Check for congratulations/important announcements
            elif "félicitons" in paragraph.lower() or "accueillons" in paragraph.lower():
                html += f'<div class="congratulations">{paragraph}</div>\n'
            # Check for program/schedule sections with enhanced formatting
            elif any(keyword in paragraph for keyword in ["Programme de la journée", "Ordre du jour"]):
                # Split into lines and format as agenda items
                lines = paragraph.split('\n')
                html += f'<div class="program"><strong style="color: {primary_color}; font-size: 18px;">{lines[0]}</strong><br><br>\n'
                for line in lines[1:]:
                    if line.strip() and not line.startswith(('Programme', 'Ordre')):
                        html += f'<div class="agenda-item">{line}</div>\n'
                html += '</div>\n'
            # Check for important information sections
            elif any(keyword in paragraph for keyword in ["Informations importantes", "IMPORTANT", "obligatoire", "strictement"]):
                html += f'<div class="important">{paragraph.replace(chr(10), "<br>")}</div>\n'
            # Check for closing/motivational message
            elif any(keyword in paragraph.lower() for keyword in ["journée inaugurale marque", "au plaisir de", "À tout à l'heure", "exceptionnelle"]) and len(paragraph) > 50:
                html += f'<div class="closing-message">{paragraph}</div>\n'
            else:
                # Add highlights to important words
                styled_paragraph = paragraph
                
                if is_convocation or is_meeting:
                    important_words = ['Sésame Junior Entreprise', 'Sesame Junior Entreprise', 
                                     'Assemblée Générale', 'CTJE', 'Confédération Tunisienne des Junior Entreprises',
                                     'obligatoire', 'strictement', 'tenue formelle', 'Pôle Projet']
                else:
                    important_words = ['Junior Entreprise', 'Sésame Junior Entreprise', 'Sesame Junior Entreprise', 
                                     'motivation', 'créativité', 'dynamique', 'ambitieux', 'professionnel', 'professionnellement']
                
                # Sort by length (longest first) to avoid partial replacements
                important_words.sort(key=len, reverse=True)
                
                for word in important_words:
                    if word.lower() in styled_paragraph.lower():
                        # Use case-insensitive replacement
                        import re
                        pattern = re.compile(re.escape(word), re.IGNORECASE)
                        styled_paragraph = pattern.sub(f'<span class="highlight">{word}</span>', styled_paragraph)
                
                # Replace line breaks within paragraphs with <br>
                styled_paragraph = styled_paragraph.replace('\n', '<br>')
                
                html += f'<div class="content">{styled_paragraph}</div>\n'
        
        html += """
                    <div class="signature">
                        <img src="cid:signature" alt="Signature" style="max-width: 100%; height: auto;">
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_email(self, recipients: List[str], subject: str, message: str, pole: str = "", recipient_name: str = "") -> bool:
        """
        Send HTML email to recipients with signature and CC
        
        Args:
            recipients: List of email addresses
            subject: Email subject
            message: Email body (plain text)
            pole: Pole name for styling
            recipient_name: Name of the recipient for unique message ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('related')
            msg['From'] = self.email
            msg['To'] = ', '.join(recipients)
            
            # Add CC if available
            if self.cc_list:
                msg['Cc'] = ', '.join(self.cc_list)
                # Add CC addresses to the actual recipient list for sending
                all_recipients = recipients + self.cc_list
            else:
                all_recipients = recipients
            
            msg['Subject'] = Header(subject, 'utf-8')
            
            # Add unique headers to prevent threading
            import time
            import uuid
            unique_id = f"{int(time.time())}.{uuid.uuid4().hex[:8]}"
            msg['Message-ID'] = f"<welcome.{recipient_name.replace(' ', '.')}.{unique_id}@sesame.com.tn>"
            msg['Date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
            
            # Prevent threading by ensuring no References or In-Reply-To headers
            if 'References' in msg:
                del msg['References']
            if 'In-Reply-To' in msg:
                del msg['In-Reply-To']
            
            # Create multipart alternative for both HTML and plain text
            msg_alternative = MIMEMultipart('alternative')
            msg.attach(msg_alternative)
            
            # Add plain text version
            text_part = MIMEText(message, 'plain', 'utf-8')
            msg_alternative.attach(text_part)
            
            # Convert to HTML and add HTML version
            html_message = self.convert_to_html(message, pole)
            html_part = MIMEText(html_message, 'html', 'utf-8')
            msg_alternative.attach(html_part)
            
            # Add signature image
            signature_path = "signature.png"
            if os.path.exists(signature_path):
                with open(signature_path, 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data)
                    image.add_header('Content-ID', '<signature>')
                    image.add_header('Content-Disposition', 'inline', filename='signature.png')
                    msg.attach(image)
            else:
                print(f"Warning: Signature file {signature_path} not found")
            
            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable security
                server.login(self.email, self.password)
                
                # Send email to all recipients (including CC)
                server.send_message(msg, to_addrs=all_recipients)
                
            cc_info = f" (CC: {', '.join(self.cc_list)})" if self.cc_list else ""
            print(f"Email sent successfully to: {', '.join(recipients)}{cc_info}")
            return True
            
        except Exception as e:
            print(f"Error sending email to {', '.join(recipients)}: {str(e)}")
            return False
    
    def send_bulk_email(self, csv_file: str, template_file: str, subject_suffix: str):
        """
        Send one email to all recipients from CSV (for announcements like AG convocations)
        
        Args:
            csv_file: Path to CSV file
            template_file: Path to template file
            subject_suffix: Suffix for email subject
        """
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
        generic_message = template.replace('[X]', 'Chers membres de Sesame Junior Entreprise')
        
        # Create subject without emojis
        subject = f"Sesame Junior Entreprise - {subject_suffix}"
        
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
        
        print(f"\nSending bulk email from {csv_file} to {len(unique_recipients)} recipients...")
        print(f"Recipients: {', '.join(unique_recipients[:5])}{'...' if len(unique_recipients) > 5 else ''}")
        
        # Send one email to all recipients
        self.send_email(unique_recipients, subject, generic_message, subject_suffix, "all_members")

    def process_csv_and_send(self, csv_file: str, template_file: str, subject_suffix: str):
        """
        Process a CSV file and send emails according to template
        
        Args:
            csv_file: Path to CSV file
            template_file: Path to template file
            subject_suffix: Suffix for email subject (e.g., "Pole Projet")
        """
        # Read emails and template
        emails = self.read_csv_emails(csv_file)
        template = self.read_template(template_file)
        
        if not template:
            print(f"Cannot send emails: template from {template_file} is empty")
            return
        
        if not emails:
            print(f"No emails found in {csv_file}")
            return
        
        # Create subject without emojis
        if "Pole" in subject_suffix:
            subject = f"Bienvenue à Sesame Junior Entreprise - {subject_suffix}"
        else:
            subject = f"Sesame Junior Entreprise - {subject_suffix}"
        
        print(f"\nProcessing {csv_file} with {len(emails)} email(s)...")
        
        for name, mail_sesame, mail_autre in emails:
            # Personalize message with the name from CSV
            personalized_message = self.personalize_message(template, name)
            
            # Prepare recipients list
            recipients = [mail_sesame]
            if mail_autre:
                recipients.append(mail_autre)
            
            # Send email
            print(f"Sending email to {name} ({', '.join(recipients)})...")
            self.send_email(recipients, subject, personalized_message, subject_suffix, name)

def load_config():
    """
    Load configuration from .env file
    """
    load_dotenv()
    
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')  # Default to Gmail
    smtp_port = int(os.getenv('SMTP_PORT', '587'))  # Default to 587
    
    return smtp_server, smtp_port, sender_email, sender_password

def main():
    """
    Main function to configure and run the email sender
    """
    print("=== Sesame Junior Entreprise - Welcome Email Sender ===\n")
    
    # Try to load configuration from .env file
    smtp_server, smtp_port, sender_email, sender_password = load_config()
    
    if not sender_email or not sender_password:
        print("⚠️  CONFIGURATION NEEDED:")
        print("Please ensure your .env file contains:")
        print("SENDER_EMAIL=your_email@domain.com")
        print("SENDER_PASSWORD=your_password")
        print("SMTP_SERVER=smtp.gmail.com (optional, defaults to Gmail)")
        print("SMTP_PORT=587 (optional, defaults to 587)")
        return
    
    print(f"Using email: {sender_email}")
    print(f"🌐 SMTP server: {smtp_server}:{smtp_port}")
    
    # Ask for confirmation before sending
    response = input("\n🚀 Ready to send welcome emails? (y/n): ").lower().strip()
    if response != 'y':
        print("Operation cancelled.")
        return
    
    # Initialize email sender
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)
    
    # Process Marketing Commercial emails
    if os.path.exists("MC.csv"):
        email_sender.process_csv_and_send(
            csv_file="MC.csv",
            template_file="templateMC.txt", 
            subject_suffix="Pole Marketing Commercial"
        )
    else:
        print("⚠️  MC.csv not found, skipping Marketing Commercial emails")
    
    # Process Projet emails
    if os.path.exists("Projet.csv"):
        email_sender.process_csv_and_send(
            csv_file="Projet.csv",
            template_file="templateProjet.txt",
            subject_suffix="Pole Projet"
        )
    else:
        print("⚠️  Projet.csv not found, skipping Projet emails")
    
    # Process Convocation emails for all members
    if os.path.exists("all.csv"):
        email_sender.process_csv_and_send(
            csv_file="all.csv",
            template_file="ConvocationAGetVisite.txt",
            subject_suffix="Convocation - AG et Visite CTJE"
        )
    else:
        print("⚠️  all.csv not found, skipping Convocation emails")
    
    print("\n✅ All emails processed!")

if __name__ == "__main__":
    main()
