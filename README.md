# Local Service Connect App

A comprehensive Flask-based web application that connects local service users with qualified service providers in their area. The platform enables seamless booking, communication, and job management between customers and service professionals.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Database](#database)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## 🎯 Overview

**Local Service Connect** is a two-sided marketplace platform that bridges the gap between service seekers and service providers. Users can request services or browse available providers, while service professionals can accept jobs, communicate with customers, and build their reputation through ratings and reviews.

### Key Objectives:
- Enable users to discover and book local services
- Allow service providers to manage bookings and customer interactions
- Implement real-time notifications and messaging system
- Provide admin panel for platform management
- Ensure secure authentication and data protection

---

## ✨ Features

### **For Users (Service Seekers)**
- ✅ User registration and authentication
- ✅ Browse service providers by profession (Plumber, Electrician, Cleaner, Handyman, Carpenter, General Worker)
- ✅ Book specific providers or request general services
- ✅ Real-time messaging with service providers
- ✅ View booking history and status
- ✅ Rate and review completed services
- ✅ Job completion verification
- ✅ Profile management
- ✅ Real-time notifications

### **For Service Providers**
- ✅ Provider registration with profession selection
- ✅ View available job requests from users
- ✅ Accept or reject booking requests
- ✅ Real-time chat with customers
- ✅ Mark jobs as complete
- ✅ View completion rate and performance metrics
- ✅ Manage active and pending jobs
- ✅ Build professional profile and reputation

### **General Features**
- ✅ Secure user authentication with bcrypt password hashing
- ✅ CSRF protection on all forms
- ✅ Email notifications for booking requests
- ✅ Session management (24-hour session duration)
- ✅ Responsive design
- ✅ Admin dashboard for platform management
- ✅ RESTful API for testing

---

## 🛠️ Technology Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Flask 3.1.2 |
| **Database** | MySQL 8.0+ |
| **Authentication** | Flask-Bcrypt, PyJWT |
| **Forms & Validation** | Flask-WTF, WTForms |
| **Email** | Flask-Mail |
| **Frontend** | HTML, CSS, JavaScript (Jinja2 Templates) |
| **Server** | Gunicorn |
| **Containerization** | Docker |
| **Environment** | Python 3.10 |

### Dependencies:
```
Flask==3.1.2
Flask-Bcrypt==1.0.1
Flask-MySQLdb==2.0.0
Flask-WTF==1.2.2
Flask-Mail==0.10.0
mysql-connector-python==8.1.0
python-dotenv==1.1.1
gunicorn==21.2.0
PyJWT==2.10.1
```

---

## 📁 Project Structure

```
Local_service_connect_app/
├── app/
│   ├── __init__.py                 # Flask app initialization and configuration
│   ├── database/
│   │   └── migrate.py             # Database migration script
│   ├── forms/
│   │   └── forms.py               # WTForms form classes
│   ├── routess/
│   │   ├── auths.py               # Authentication routes (login, register)
│   │   ├── dashboards.py          # Main application routes
│   │   ├── admins_panel.py        # Admin dashboard routes
│   │   └── api/
│   │       └── api_routes.py      # REST API endpoints
│   ├── static/                     # CSS, JavaScript, images
│   ├── templates/                  # HTML Jinja2 templates
│   └── utils/
│       └── mail.py                # Email and notification utilities
├── database/
│   └── migrations/                 # SQL migration files
├── main.py                         # Application entry point
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker configuration
├── railway.json                    # Railway deployment config
└── .gitignore                      # Git ignore rules
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- Git
- Docker (optional, for containerization)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/muhammads-git/Local_service_connect_app.git
   cd Local_service_connect_app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv lsc_env
   source lsc_env/bin/activate  # On Windows: lsc_env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   ```bash
   cp .env.example .env  # if available, or create manually
   ```

5. **Configure environment variables** (see Configuration section)

6. **Run database migrations:**
   ```bash
   python -m app.database.migrate
   ```

7. **Start the application:**
   ```bash
   python main.py
   ```
   
   The application will run at `http://localhost:5000`

---

## ⚙️ Configuration

Create a `.env` file in the root directory with the following variables:

### **Database Configuration**
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=serviconnect
```

### **Flask Configuration**
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

### **Email Configuration** (for booking notifications)
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=Ibuild@serviconnect.com
```

### **Railway Deployment** (optional)
```env
DB_HOST=switchyard.proxy.rlwy.net
DB_PORT=port_number
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=railway
```

---

## 🗄️ Database

### Database Schema Overview

**Key Tables:**
- `users` - User accounts and profiles
- `service_providers` - Service provider profiles
- `bookings` - Service booking records
- `messages` - User-provider messaging
- `notifications` - Real-time notifications
- `reviews` - Service ratings and reviews
- `admins` - Admin user accounts
- `migrations_history` - Migration tracking

### Migration
The app uses an automated migration system. SQL migration files are stored in `database/migrations/` and are applied sequentially on startup.

---

## 📖 Usage

### **User Flow**

1. **Register as User:**
   - Visit `/auth/register` 
   - Fill registration form with name, email, phone, and password
   - Complete profile with address

2. **Browse Providers:**
   - View available service providers on dashboard
   - Filter by profession (Plumber, Electrician, etc.)
   - Check provider ratings and reviews

3. **Book a Service:**
   - Click "Book Now" on provider profile
   - Fill booking form with date, time, address, service type, and description
   - Provider receives email notification

4. **Communicate:**
   - Access chat with assigned provider
   - View message history for each job
   - Receive real-time notifications

5. **Complete Job:**
   - Verify job completion
   - Rate and review provider
   - View completed service in profile

### **Provider Flow**

1. **Register as Provider:**
   - Visit `/auth/provider-register`
   - Select profession and provide description
   - Profile created and verified

2. **Manage Bookings:**
   - View available jobs in "Available Jobs" section
   - Accept jobs matching your expertise
   - Chat with customers before starting

3. **Track Performance:**
   - Dashboard shows:
     - Total bookings
     - Completed jobs
     - Pending jobs
     - Average rating
     - Completion rate percentage

4. **Mark Completion:**
   - Mark job as complete
   - Customer receives verification notification
   - Customer confirms and provides rating

### **Admin Functions**
- Monitor platform activity
- Manage users and providers
- View booking statistics
- Handle disputes

---

## 🔌 API Endpoints

The application includes a testing API blueprint at `/api/`

### **Authentication Routes**
- `POST /auth/user-register` - Register new user
- `POST /auth/user-login` - User login
- `POST /auth/provider-register` - Register service provider
- `POST /auth/provider-login` - Provider login
- `GET /auth/logout` - Logout (clears session)
- `POST /auth/complete-profile` - Complete user profile

### **Dashboard Routes**
- `GET /dashboard/user` - User dashboard
- `GET /dashboard/provider` - Provider dashboard
- `POST /dashboard/book_service/<provider_id>` - Book service
- `POST /dashboard/accept_booking/<booking_id>` - Accept booking
- `POST /dashboard/reject_booking/<booking_id>` - Reject booking
- `GET /dashboard/available_jobs` - View available jobs
- `GET /dashboard/active_jobs` - View active jobs
- `GET /dashboard/myChats` - View all conversations
- `POST /dashboard/send_message` - Send message to provider
- `POST /dashboard/complete_job/<job_id>` - Mark job complete
- `POST /dashboard/acceptJobDone/<job_id>` - Verify completion
- `GET /dashboard/user_profile` - View user profile
- `POST /dashboard/UpdateProfile` - Update profile

### **Notification Routes**
- `POST /dashboard/mark_as_read_single/<job_id>` - Mark single notification
- `POST /dashboard/mark_all_asread` - Mark all notifications

---

## 🐳 Deployment

### **Docker Deployment**

1. **Build Docker image:**
   ```bash
   docker build -t local-service-connect .
   ```

2. **Run container:**
   ```bash
   docker run -p 5000:5000 --env-file .env local-service-connect
   ```

### **Railway Deployment**

The app includes `railway.json` configuration for Railway deployment:

```bash
railway up
```

**Note:** Uncomment Railway database configuration in `app/__init__.py` for cloud deployment.

---

## 📝 Form Classes

All forms are validated using Flask-WTF and WTForms:

- `User_RegisterForms` - User registration
- `Provider_RegisterForm` - Provider registration
- `User_LoginForm` - User login
- `Provider_LoginForm` - Provider login
- `BookingForm` - Service booking
- `BookServiceForm` - General service request
- `UserEditProfile` - Profile editing
- `Admin_LoginForm` - Admin authentication

---

## 🔐 Security Features

- ✅ **Password Hashing:** Bcrypt encryption for all passwords
- ✅ **CSRF Protection:** Enabled on all forms using Flask-WTF
- ✅ **Session Management:** Secure 24-hour sessions with permanent tracking
- ✅ **JWT Support:** JWT tokens for API authentication
- ✅ **Input Validation:** WTForms validation on all user inputs
- ✅ **SQL Injection Prevention:** Parameterized queries throughout

---

## 🐛 Troubleshooting

### Database Connection Issues
- Verify MySQL is running: `mysql -u root -p`
- Check `.env` database credentials
- Ensure database `serviconnect` exists
- Run migrations: `python -m app.database.migrate`

### Email Sending Issues
- Enable "Less secure app access" for Gmail
- Use app-specific passwords
- Check MAIL_* environment variables

### Port Already in Use
```bash
# Kill process using port 5000
lsof -ti :5000 | xargs kill -9
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Muhammad S** - [GitHub Profile](https://github.com/muhammads-git)

---

## 📞 Support

For issues, questions, or suggestions, please open an issue on the [GitHub repository](https://github.com/muhammads-git/Local_service_connect_app/issues).

---

**Last Updated:** April 14, 2026
