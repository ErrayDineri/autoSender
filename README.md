# Sesame Junior Entreprise - Welcome Email Sender

This script automatically sends welcome emails to new members based on CSV files and email templates.

## Files Structure

### Core Files
- `main.py` - Main email sender class and utilities (imported by other scripts)
- `.env` - Environment file with email configuration (not included in repo)
- `signature.png` - Email signature image

### Production Scripts
- `send_mc.py` - Send welcome emails to Marketing Commercial (MC.csv)
- `send_projet.py` - Send welcome emails to Projet (Projet.csv)
- `send_ag.py` - Send AG convocation to all members (all.csv)
- `send_meeting.py` - Send meeting announcements to Projet members (Projet.csv)

### Test Scripts
- `test_mc.py` - Test MC welcome emails (test.csv)
- `test_projet.py` - Test Projet welcome emails (test.csv)
- `test_ag.py` - Test AG convocation emails (test.csv)
- `test_meeting.py` - Test meeting announcements (test.csv)
- `test_sender.py` - Test with random template selection (test.csv)

### Data Files
- `cc.csv` - Carbon copy email addresses (optional)
- `test.csv` - Test recipients for test scripts
- `MC.csv` - Email addresses for Marketing Commercial pole
- `Projet.csv` - Email addresses for Projet pole
- `all.csv` - Email addresses for all members (used for convocations)

### Templates
- `templateMC.txt` - Email template for Marketing Commercial
- `templateProjet.txt` - Email template for Projet
- `ConvocationAGetVisite.txt` - Email template for convocations/announcements
- `MeetingAnnouncement.txt` - Email template for meeting reminders

## Setup Instructions

### 1. Install Dependencies

```powershell
pip install python-dotenv
```

### 2. Configure Email Credentials

Create or edit the `.env` file in the project root with your email credentials:

```env
SENDER_EMAIL=your_email@domain.com
SENDER_PASSWORD=your_password_or_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Note**: `SMTP_SERVER` and `SMTP_PORT` are optional and will default to Gmail settings if not specified.

### 3. Gmail Setup (Recommended)

For Gmail users:
1. Enable 2-factor authentication
2. Generate an App Password: https://support.google.com/accounts/answer/185833
3. Use the App Password as `SENDER_PASSWORD` in `.env`

### 4. Prepare CSV Files

Each CSV file should have three columns:
- `name`: Person's name (used in email personalization)
- `mailSesame`: Primary email (always sent to)
- `mailAutre`: Secondary email (optional, sent to if provided)

Example:
```csv
name,mailSesame,mailAutre
John Doe,john.doe@sesame.fr,john.doe@gmail.com
Marie Martin,marie.martin@sesame.fr,
Pierre Durand,pierre.durand@sesame.fr,pierre.d@outlook.com
```

### 5. Add Signature Image

Place a `signature.png` file in the project root. This image will be automatically attached to all emails.

### 6. Configure Carbon Copy (Optional)

Create a `cc.csv` file to add carbon copy recipients to all emails:

```csv
email
admin@sesame.com.tn
hr@sesame.com.tn
```

### 7. Set Up Test Environment (Optional)

Create a `test.csv` file for testing with sample recipients:

```csv
name,mailSesame,mailAutre
Test User,test@example.com,test2@example.com
```

## Usage

### Production Mode

Send specific email campaigns:

```powershell
# Send Marketing Commercial welcome emails
python send_mc.py

# Send Projet welcome emails
python send_projet.py

# Send AG convocation to all members
python send_ag.py

# Send meeting announcement to Projet members
python send_meeting.py
```

### Test Mode

Test specific templates before production:

```powershell
# Test MC welcome email
python test_mc.py

# Test Projet welcome email
python test_projet.py

# Test AG convocation email
python test_ag.py

# Test meeting announcement
python test_meeting.py

# Test with random template selection
python test_sender.py
```

### Benefits of Separate Scripts

✅ **Focused**: Each script does one thing well  
✅ **Safe**: Can't accidentally send wrong emails to wrong people  
✅ **Clear**: Script name tells you exactly what it does  
✅ **Testable**: Each template has its own test script  
✅ **Simple**: No complex menu or options, just run and confirm  
✅ **Maintainable**: All scripts share the same core code from main.py  

### How It Works

**Production Scripts:**
- Each script is focused on one specific task
- Reads from specific CSV file (MC.csv, Projet.csv, or all.csv)
- Uses specific template (templateMC.txt, templateProjet.txt, or ConvocationAGetVisite.txt)
- Includes CC recipients automatically
- Asks for confirmation before sending

**Test Scripts:**
- All test scripts read from test.csv
- Send emails with "🧪 TEST" prefix
- Use the same styling and formatting as production
- Include CC recipients
- Safe to run without affecting production recipients

## Email Features

- **HTML Formatting**: Emails are sent in both plain text and HTML formats
- **Color Coding**: Professional blue color scheme (#007cc1 and #12c2d2)
- **Styling**: Bold text, colored highlights, and professional layout
- **Signature**: Automatic signature image attachment
- **Carbon Copy**: Optional CC functionality for administrative oversight
- **Test Mode**: Safe testing with random template selection
- **Multiple Templates**: Welcome emails (MC/Projet) and Convocation emails
- **Special Sections**: Highlighted program sections, important notices, and formatted schedules
- **Responsive**: Emails look good on both desktop and mobile devices
- **Unique Message IDs**: Prevents email threading issues

## Email Subjects

- Marketing Commercial: "🎉 Bienvenue à Sesame Junior Entreprise - Pole Marketing Commercial"
- Projet: "🎉 Bienvenue à Sesame Junior Entreprise - Pole Projet"
- Convocation: "📧 Sesame Junior Entreprise - Convocation - AG et Visite CTJE"

## Template Variables

Templates use `[X]` as placeholder for the person's name, which is taken from the `name` column in the CSV files.

The script automatically converts plain text templates to beautiful HTML emails with:
- Color-coded headers based on the pole
- Bold and highlighted important text
- Professional styling and layout
- Embedded signature image

## Common SMTP Servers

- Gmail: `smtp.gmail.com` (port 587)
- Outlook/Hotmail: `smtp-mail.outlook.com` (port 587)  
- Yahoo: `smtp.mail.yahoo.com` (port 587)

## Security Notes

- Never commit `.env` to version control (add it to `.gitignore`)
- Use App Passwords instead of regular passwords when possible
- Keep your email credentials secure