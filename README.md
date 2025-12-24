# ReseauSocial - Social Media Platform

A modern, responsive social media platform built with Django, featuring user authentication, posts, profiles, and real-time interactions.

## 🚀 Features

- **User Authentication** - Registration, login, logout
- **User Profiles** - Custom profiles with bio, location, and profile pictures
- **Post Creation** - Create text posts with image uploads
- **Social Interactions** - Like posts, follow users
- **Search Functionality** - Find users and content
- **Responsive Design** - Works on desktop and mobile
- **Modern UI** - Clean, intuitive interface with smooth animations

## 🛠️ Tech Stack

- **Backend:** Django 5.2
- **Database:** SQLite (development) / PostgreSQL (production)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Styling:** Custom CSS with Tailwind CSS integration
- **Icons:** Emoji and custom SVG icons

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/islvm7/ReseauSocial.git
cd ReseauSocial
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Database

```bash
# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser!

## 📁 Project Structure

```
ReseauSocial/
├── ReseauSocial/          # Django project settings
│   ├── settings.py       # Main configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI configuration
├── socialmedia/          # Main Django app
│   ├── migrations/      # Database migrations
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # App URL routing
│   ├── post.py          # App forms
│   ├── freind_recommendation.py          # App freinds suggestions Algorithm
│   ├── post_recommendation.py          # App posts suggestions Algorithm
│   ├── static/          # CSS, JS, images
│   │   ├── css/
│   │   └── js/
│   └── templates/       # HTML templates
│       └── main/
│       └── registration/
├── db.sqlite3           # Database (not in repo)
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root for sensitive settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### Static Files

For production deployment, configure static file serving:

```bash
python manage.py collectstatic
```

## 🎯 Usage

### Creating Posts

1. Log in to your account
2. Click the "Create Post" area
3. Write your message
4. Optionally add an image
5. Click "Publish"

### Managing Profile

1. Go to your profile (sidebar)
2. Click "Edit Profile"
3. Update your bio, location, or profile picture
4. Save changes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write descriptive commit messages
- Test your changes before submitting
- Update documentation as needed

## 📱 API Endpoints

### Authentication
- `POST /accounts/login/` - User login
- `POST /accounts/logout/` - User logout
- `POST /accounts/signup/` - User registration

### Social Features
- `GET /` - Feed/Home page
- `POST /upload/` - Create new post
- `GET /search/` - Search users
- `GET /dashboard/` - User dashboard

## 🐛 Troubleshooting

### Common Issues

**"TemplateDoesNotExist" Error:**
- Ensure all template files are in the correct directories
- Check template paths in views.py

**"Static files not loading":**
- Run `python manage.py collectstatic`
- Check STATIC_URL and STATICFILES_DIRS in settings.py

**"Database errors":**
- Run `python manage.py migrate`
- Check database file permissions

**"Port already in use":**
- Kill existing processes: `python manage.py runserver 8001`
- Or find and kill the process using port 8000

## 🚀 Deployment

### Heroku Deployment

1. Create a Heroku app
2. Set environment variables
3. Deploy using Heroku CLI or GitHub integration

### Docker Deployment

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```


## 👥 Authors


- Siakene Raihane
- Zerrouki Imane
- Yahiaoui Mohamed Islem
- Mellali Abderhmane Rayane
- Zitouni Lyna
- Yachir Meriem



## 🙏 Acknowledgments

- Django documentation
- Tailwind CSS for inspiration
- Open source community




