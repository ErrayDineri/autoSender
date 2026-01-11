# Quick Reference - AutoSender Scripts

## 📧 Production Scripts (Send Real Emails)

| Script | Purpose | CSV Used | Template Used |
|--------|---------|----------|---------------|
| `send_mc.py` | Welcome new MC members | MC.csv | templateMC.txt |
| `send_projet.py` | Welcome new Projet members | Projet.csv | templateProjet.txt |
| `send_ag.py` | Send AG convocation to all | all.csv | ConvocationAGetVisite.txt |
| `send_meeting.py` | Send meeting announcement | Projet.csv | MeetingAnnouncement.txt |

## 🧪 Test Scripts (Send to test.csv)

| Script | Purpose | Template Used |
|--------|---------|---------------|
| `test_mc.py` | Test MC welcome email | templateMC.txt |
| `test_projet.py` | Test Projet welcome email | templateProjet.txt |
| `test_ag.py` | Test AG convocation | ConvocationAGetVisite.txt |
| `test_meeting.py` | Test meeting announcement | MeetingAnnouncement.txt |
| `test_sender.py` | Random template test | All templates randomly |

## 🚀 Quick Start

### Send Welcome Emails to New MC Members
```powershell
python send_mc.py
```

### Send Welcome Emails to New Projet Members
```powershell
python send_projet.py
```

### Send AG Convocation to All Members
```powershell
python send_ag.py
```

### Send Meeting Announcement to Projet Members
```powershell
python send_meeting.py
```

### Test Before Sending
```powershell
# Test the specific template first
python test_mc.py      # or test_projet.py or test_ag.py or test_meeting.py

# Check test.csv recipients receive the email correctly
# Then run the production version
python send_mc.py
```

## ⚙️ Architecture

```
main.py (Core Library)
├── EmailSender class
├── load_config()
└── Shared by all scripts

Production Scripts          Test Scripts
├── send_mc.py       →     ├── test_mc.py
├── send_projet.py   →     ├── test_projet.py
├── send_ag.py       →     ├── test_ag.py
└── send_meeting.py  →     └── test_meeting.py
```

## 📋 Features Included in All Scripts

✅ HTML formatted emails with styling  
✅ Signature image attachment  
✅ CC functionality (from cc.csv)  
✅ Personalized with recipient names  
✅ Unique message IDs (no threading)  
✅ Confirmation prompt before sending  
✅ Error handling and validation  

## 🎯 Best Practices

1. **Always test first**: Run test scripts before production
2. **Check test.csv**: Make sure it has valid test recipients
3. **Verify templates**: Ensure template files are up to date
4. **Review CC list**: Check cc.csv has correct addresses
5. **One task at a time**: Run scripts separately for clarity
