# 🎓 Mentorship Management System

[![Deploy to Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new)

A comprehensive web-based mentorship management system for educational institutions. **One-click deploy to GitHub Codespaces!**

## 🚀 Quick Deploy (GitHub Codespaces)

1. **Click the "Code" button** → **"Create codespace on main"**
2. **Wait for setup** (2-3 minutes)
3. **Run**: `python run_online.py`
4. **Click the popup** to open your live app!

Your app will be available at: `https://[codespace-name]-5000.app.github.dev`

## ✨ Features

- 👨‍🏫 **Mentor Management** - Add, view, and manage mentors with specialties
- 👨‍🎓 **Mentee Management** - Comprehensive student profile management
- 🔗 **Smart Assignment** - Automatic mentor-student matching
- 📅 **Session Scheduling** - Schedule and track mentoring sessions
- 📊 **Dashboard Analytics** - Real-time statistics and insights
- 📱 **Responsive Design** - Mobile-friendly interface that works on all devices
- 📈 **Progress Tracking** - Monitor student progress and lesson completion
- 📤 **Data Export** - Export mentor/mentee data to CSV files
- 🔄 **Bulk Operations** - Reassign students, bulk mentor assignment

## 📱 How to Use (For End Users)

### 🚀 Getting Started
1. **Access the app** via your Codespace URL
2. **View the Dashboard** to see system overview
3. **Add mentors** with their expertise areas
4. **Add students** with their learning needs
5. **Use smart assignment** to match mentors with students

### 👨‍🏫 Managing Mentors
- Click "Mentors" → "Add Mentor"
- Fill in mentor details and subjects they teach
- View all mentors and their assignments

### 👨‍🎓 Managing Students
- Go to "Mentees" → "Add Mentee"  
- Enter student information and subjects needed
- View student profiles and progress

### 🔗 Assigning Mentors
- Use "Assign Mentor" for individual assignments
- Use "Bulk Assign" for multiple students at once
- Smart matching suggests best mentor-student pairs

### 📅 Scheduling Sessions
- Select mentor and student
- Choose date, time, and session type
- Add notes and track session completion

## 🛠️ For Developers

### Local Development

```bash
# Clone your repository
git clone [your-repo-url]
cd mentorship-system

# Install dependencies
pip install -r requirements.txt

# Run the application
python run_online.py
```

### File Structure
```
mentorship-system/
├── app.py                    # Main Flask application  
├── run_online.py            # Codespace launcher
├── requirements.txt         # Dependencies
├── .devcontainer/          # Codespace configuration
├── templates/              # HTML templates
├── static/                # CSS, JS, assets
└── instance/              # Database (auto-created)
```

## 🌐 Alternative Hosting

- **Replit**: Import from GitHub, click Run
- **Railway**: Connect repository, auto-deploy
- **Heroku**: Deploy from GitHub integration

See `HOSTING_GUIDE.md` for detailed instructions.

## 🔒 Security Features

- ✅ Source code protected in private repository
- ✅ Secure HTTPS hosting via GitHub
- ✅ Isolated database per deployment  
- ✅ No sensitive data exposure to end users

## 📞 Need Help?

- Check `HOSTING_GUIDE.md` for deployment help
- Review `README_DEPLOY.md` for detailed setup
- Create an issue for bugs or questions

---

**🎉 Ready to deploy?** Click the Codespaces button above!
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Use the navigation menu to:
   - Add mentors and mentees
   - Assign mentors to mentees
   - Schedule mentorship sessions
   - View the dashboard for system overview

## Project Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Application styles
│   └── js/
│       └── main.js       # JavaScript functionality
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── dashboard.html    # Dashboard view
│   ├── add_mentor.html   # Add mentor form
│   ├── add_mentee.html   # Add mentee form
│   ├── mentors.html      # Mentors listing
│   ├── mentees.html      # Mentees listing
│   ├── assign_mentor.html # Mentor assignment
│   ├── schedule_session.html # Session scheduling
│   ├── calendar.html     # Calendar view
│   └── ...               # Other templates
├── instance/
│   └── mentorship.db     # SQLite database (auto-created)
└── .gitignore            # Git ignore file
```

## Database Schema

The system uses SQLite with three main models:

- **Mentor**: Stores mentor information, subjects, and availability
- **Mentee**: Stores mentee information and learning goals  
- **Session**: Stores scheduled mentorship sessions

## Configuration

The application uses SQLite database by default. The database file is created automatically in the `instance/` directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
