# RSS Scraper

A modern, elegant web application for checking and validating RSS/Atom feeds. Built with Python (Flask) and featuring a glassmorphism-inspired UI.

![License](https://img.shields.io/github/license/pedrobritx/rss_scraper)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)

## ✨ Features

- **🔍 Feed Discovery**: Automatically finds RSS and Atom feeds from any URL.
- **✅ Validation**: Validates feed availability and structure.
- **🎨 Modern UI**: Beautiful glassmorphism design with responsive layout.
- **⚡ Real-time Feedback**: Interactive progress indicators and error handling.
- **📋 Easy Copying**: One-click copy for discovered feed URLs.
- **📱 Responsive**: Fully optimized for desktop and mobile devices.

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Beautiful Soup 4, Requests
- **Frontend**: HTML5, CSS3 (Custom Glassmorphism), JavaScript (Vanilla)
- **Tools**: Ruff (Linting), Pytest (Testing)

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/pedrobritx/rss_scraper.git
   cd rss_scraper
   ```

2. **Create a virtual environment (Optional but Recommended)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the server**

   ```bash
   python run.py
   ```

   _Optionally, specify a custom port:_

   ```bash
   PORT=8000 python run.py
   ```

2. **Access the app**
   Open your browser and navigate to: `http://localhost:5001` (or your custom port)

## 📂 Project Structure

```
rss_scraper/
├── rss_scraper/
│   ├── scraper/          # Scraping logic and validation
│   ├── static/           # CSS, JS, and assets
│   ├── templates/        # HTML templates
│   ├── routes.py         # Flask routes
│   └── text_utils.py     # Utilities
├── tests/                # Unit and integration tests
├── pyproject.toml        # Project configuration
├── requirements.txt      # Dependencies
└── run.py               # Application entry point
```

## 🧪 Running Tests

To run the test suite, ensure you have the dev dependencies installed:

```bash
pip install .[dev]
pytest
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
