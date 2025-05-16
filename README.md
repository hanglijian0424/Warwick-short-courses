# Warwick Short Course Application System

This is a lightweight Flask-based web application for managing short course applications at the University of Warwick.

## 📁 Project Directory Structure

```
├── app.py                  # Main Flask application
├── internship.db           # SQLite database
├── requirements.txt        # Python dependencies
├── templates/              # All Jinja2 HTML templates
│   ├── index.html
│   ├── apply.html
│   ├── dashboard.html
│   └── ...
├── static/                 # Static assets (images, CSS)
│   ├── img/
│   │   ├── ai.jpg
│   │   ├── business.jpg
│   │   └── climate.jpg
│   └── style.css
├── test/                   # Unit tests
│   └── test_app.py
└── README.md               # Project description and structure
```

## 💡 Features

- Course listing homepage with images
- Application form with input validation
- Admin dashboard to review, accept, or delete applications
- Application status checking by email
- Bootstrap-based responsive design
- Python `unittest` support

## ✅ To Run the App

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` in your browser.

## 🔍 For Testing

```bash
cd test
python -m unittest test_app.py
```

## Author

Designed and implemented by **Lijian Hang**, University of Warwick.
