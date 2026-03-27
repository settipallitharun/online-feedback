# Online Feedback Collector with Admin Dashboard

A complete full-stack web application that collects feedback from users and displays summarized results in an admin dashboard.

## 🚀 Features

### User Interface
- **Home Page**: Clean and modern landing page
- **Feedback Form**: User-friendly form with the following fields:
  - Name (required)
  - Email (required)
  - Rating (1-5 stars, required)
  - Comments (optional)
- **Real-time Validation**: Client-side form validation with visual feedback
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

### Backend (Flask)
- **RESTful API**: Clean and efficient backend routes
- **Database Integration**: SQLite database for data persistence
- **Data Validation**: Server-side validation for security
- **Error Handling**: Comprehensive error handling and user feedback

### Admin Dashboard
- **Statistics Overview**: 
  - Total feedback count
  - Average rating
  - Response rate
- **Interactive Charts**:
  - Rating distribution (pie chart)
  - Daily feedback trends (bar chart)
- **Data Management**:
  - View all feedback entries in a sortable table
  - Export data to CSV
  - Real-time data refresh

## 🛠️ Technology Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript**: Interactive functionality and AJAX requests
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icon library
- **Chart.js**: Data visualization

### Backend
- **Python 3**: Programming language
- **Flask**: Web framework
- **SQLite**: Database management
- **Jinja2**: Template engine

## 📁 Project Structure

```
OnlineFeedbackCollector/
│
├── app.py                 # Flask backend code
├── requirements.txt        # Required Python packages
├── database.db            # SQLite database (created automatically)
│
├── static/
│   ├── css/
│   │   └── style.css      # Custom styling
│   └── js/
│       └── script.js      # JavaScript functionality
│
├── templates/
│   ├── layout.html        # Base HTML template
│   ├── index.html         # Home page with feedback form
│   └── admin.html         # Admin dashboard page
│
└── README.md              # Project documentation
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or Download the Project**
   ```bash
   # If using git
   git clone <repository-url>
   cd OnlineFeedbackCollector
   
   # Or download and extract the ZIP file
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Application**
   - Open your web browser and go to: `http://127.0.0.1:5000`
   - Home page: `http://127.0.0.1:5000/`
   - Admin Dashboard: `http://127.0.0.1:5000/admin-dashboard`

## 📖 Usage Guide

### For Users
1. Visit the home page
2. Fill out the feedback form:
   - Enter your name and email
   - Select a rating (1-5 stars)
   - Optionally add comments
3. Click "Submit Feedback"
4. You'll see a success message confirming submission

### For Administrators
1. Navigate to the Admin Dashboard
2. View real-time statistics and charts
3. Browse all feedback entries in the table
4. Export data to CSV for further analysis
5. Use the refresh button to update data

## 🔧 Configuration

### Database
- The application uses SQLite (`database.db`) which is created automatically
- No additional database configuration required

### Customization
- Modify `static/css/style.css` for styling changes
- Update `templates/` for UI modifications
- Extend `app.py` for additional backend functionality

## 📊 Database Schema

```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    comments TEXT,
    date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🌟 Key Features Explained

### Form Validation
- **Client-side**: Real-time validation with visual feedback
- **Server-side**: Security validation before database insertion
- **Error Handling**: User-friendly error messages

### Data Visualization
- **Rating Distribution**: Pie chart showing feedback breakdown
- **Daily Trends**: Bar chart displaying last 7 days of activity
- **Responsive Charts**: Charts adapt to different screen sizes

### Export Functionality
- **CSV Export**: Download all feedback data in CSV format
- **Complete Data**: Includes all fields with proper formatting
- **Timestamp**: Automatically includes submission dates

## 🔒 Security Features

- Input validation and sanitization
- SQL injection prevention (parameterized queries)
- XSS protection (Jinja2 auto-escaping)
- CSRF protection (Flask built-in)

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill the process using port 5000 (Windows)
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   
   # Or use a different port
   python app.py --port 5001
   ```

2. **Module Not Found**
   ```bash
   # Ensure you're in the correct directory
   cd OnlineFeedbackCollector
   
   # install dependencies
   pip install -r requirements.txt
   ```

3. **Database Issues**
   - Delete `database.db` and restart the application
   - The database will be recreated automatically

## 🚀 Deployment

### Local Development
- Use the built-in Flask development server
- Suitable for testing and development

### Production Deployment
For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a reverse proxy (Nginx)
- Configuring a proper database (PostgreSQL, MySQL)
- Implementing SSL/TLS
- Setting up monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

If you encounter any issues or have questions:
- Check the troubleshooting section above
- Review the code comments for additional context
- Create an issue in the project repository

---

**Happy Feedback Collecting! 🎉**
