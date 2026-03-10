# 🛡️ RoadRakshaka 

**RoadRakshaka** (meaning *Road Protector*) is a modern, responsive web application designed as a citizen civic-issue reporting platform. It empowers citizens to report everyday municipal issues—like potholes, broken streetlights, or garbage accumulation—directly to local authorities, fostering transparency and faster issue resolution.

![RoadRakshaka Interface](https://via.placeholder.com/800x400.png?text=RoadRakshaka+Dashboard)

## ✨ Features

* **User Authentication**: Secure signup and login for both regular citizens and administrative personnel.
* **Civic Issue Reporting**: Easily report problems with photos, descriptions, automatically tracking severity, category, and geolocation coordinates.
* **Public Map & List Views**: Explore reports submitted by peers on an interactive map (Leaflet.js) or in a detailed list view. Everything is completely transparent.
* **Reviewer Dashboard**: A dedicated, protected frontend dashboard for municipal staff to review, update statuses, and add administrative notes to active reports.
* **Rewards System**: Gamified civic engagement! Earn points for reporting issues effectively, which can be tracked on the dedicated Rewards page.
* **Modern UI & Aesthetics**: Built with a sleek, responsive design featuring glassmorphism, dynamic animations, and a cohesive design language.

## 🛠️ Technology Stack

* **Backend Framework**: Django (Python)
* **Database**: SQLite (Default development database)
* **Frontend Basics**: HTML5, CSS3 (Vanilla & Custom Animations)
* **Interactive Elements**: JavaScript (Vanilla)
* **Mapping Library**: Leaflet.js (for OpenStreetMap integration)

## 🚀 Local Development Setup

Follow these steps to get the project running locally on your machine.

### Prerequisites

* Python 3.8+ installed
* Open to running a fast, lightweight virtual environment

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/avin243/rrakshaka.git
   cd rrakshaka
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install django pillow
   ```
   *(Note: `pillow` is required for image uploading capability)*

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (admin account) for reviewer access:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set a username, email, and password.

6. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## 📸 Media & Static Files

The local server automatically serves uploaded images (e.g., issue report photos) in the `media/` directory during development.

## 🤝 Contributing

This project is open-source. Feel free to submit issues, fork the repository, and create pull requests to enhance RoadRakshaka's capabilities!

---
> Empowering citizens for a better tomorrow.
