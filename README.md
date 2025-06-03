# 📝 Personal Notebook - Django Web Application

---

## 🌟 Features

### 📚 **Note Management**
- ✅ **Rich Text Editor** - Create and edit notes with formatting
- ✅ **Categories & Tags** - Organize notes efficiently
- ✅ **Search & Filter** - Find notes quickly
- ✅ **Pin & Favorite** - Mark important notes
- ✅ **Version History** - Track note changes
- ✅ **Note Templates** - Use predefined structures

### 👤 **User Experience**
- ✅ **User Authentication** - Secure login/registration
- ✅ **Profile Management** - Upload profile pictures
- ✅ **Dark/Light Mode** - Toggle themes
- ✅ **Responsive Design** - Works on all devices
- ✅ **Real-time Search** - Instant search results

### 🔧 **Advanced Features**
- ✅ **Note Sharing** - Collaborate with others
- ✅ **File Attachments** - Add files to notes
- ✅ **Reminders** - Set note reminders
- ✅ **Export Options** - Export to various formats
- ✅ **Voice Notes** - Audio note support

</div>

---

## 🚀 Quick Start

### 📋 Prerequisites

- 🐍 **Python 3.8+**
- 📦 **pip** (Python package manager)
- 🗄️ **PostgreSQL** (for production)
- 

## 📁 Project Structure

\`\`\`
django-notebook-app/
├── 📁 accounts/              # User authentication & profiles
│   ├── 📄 models.py         # User & UserProfile models
│   ├── 📄 views.py          # Authentication views
│   ├── 📄 forms.py          # User forms
│   └── 📄 signals.py        # Profile creation signals
├── 📁 notes/                # Note management
│   ├── 📄 models.py         # Note, Category, Tag models
│   ├── 📄 views.py          # Note CRUD operations
│   ├── 📄 forms.py          # Note forms
│   └── 📄 admin.py          # Admin configuration
├── 📁 core/                 # Shared utilities
│   ├── 📄 mixins.py         # Custom mixins
│   └── 📄 utils.py          # Utility functions
├── 📁 templates/            # HTML templates
│   ├── 📄 base.html         # Base template
│   ├── 📁 accounts/         # User templates
│   └── 📁 notes/            # Note templates
├── 📁 static/               # Static files (CSS, JS)
├── 📁 media/                # User uploads
├── 📁 scripts/              # Database scripts
├── 📄 manage.py             # Django management
├── 📄 requirements.txt      # Python dependencies
└── 📄 README.md             # This file
\`\`\`

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 **Reporting Bugs**

1. **🔍 Check** existing issues
2. **📝 Create** detailed bug report
3. **🏷️ Add** appropriate labels

### ✨ **Suggesting Features**

1. **💡 Open** feature request issue
2. **📋 Describe** the feature clearly
3. **🎯 Explain** the use case

---

## 📊 Development Status

<div align="center">

| Feature | Status | Priority |
|---------|--------|----------|
| 📝 Basic Notes | ✅ Complete | High |
| 👤 User Auth | ✅ Complete | High |
| 🎨 UI/UX | ✅ Complete | High |
| 🔍 Search | ✅ Complete | Medium |
| 📱 Mobile | ✅ Complete | Medium |
| 🔊 Voice Notes | 🚧 In Progress | Low |
| 🎨 Drawing | 🚧 In Progress | Low |
| 📧 Email Alerts | ⏳ Planned | Low |

</div>

---

## 🐛 Troubleshooting

### ❗ **Common Issues**

<details>
<summary><strong>🔧 Pillow Installation Error</strong></summary>

\`\`\`bash
# Install Pillow
pip install Pillow==10.1.0

# Or run setup script
python setup_complete.py
\`\`\`
</details>

<details>
<summary><strong>🗄️ Database Migration Error</strong></summary>

\`\`\`bash
# Reset database
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
\`\`\`
</details>

<details>
<summary><strong>👤 Profile Error</strong></summary>

\`\`\`bash
# Fix user profiles
python fix_profiles.py
\`\`\`
</details>

## 🙏 Acknowledgments

- 🎨 **Bootstrap** for the beautiful UI components
- 📝 **Quill.js** for the rich text editor
- 🚀 **Railway** for easy deployment
- 🐍 **Django** community for the amazing framework

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

 | 📧 [Contact](mailto:sajibuddin729@gmail.com) |

---

*Made with ❤️ by [Md. Sajib Uddin](https://github.com/sajibuddin729)*

</div>
