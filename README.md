# Event Booking Web Application

This project is a *Web Event Booking System* built using *Django*, *HTML*, *CSS*, and *JavaScript*. The application allows users to browse events, register, and book tickets online.

---

## Features
- *User Authentication:* Register, login, and manage user profiles.
- *Event:* View events.
- *Booking System:* Book tickets for available events.
- *Responsive Design:* Mobile-friendly layout using CSS.
- *Interactive UI:* Dynamic elements with JavaScript.

---

## Technologies Used
- *Backend:* Django (Python Framework)
- *Frontend:* HTML, CSS, JavaScript
- *Database:* SQLite (default)

---

## Installation

### Setup Steps
1. *Clone the repository:*
   bash
   git clone https://github.com/your-repository/event-booking.git
   cd event-booking
   

2. *Create and activate a virtual environment:*
   bash
   python3 -m venv venv
   source venv/bin/activate
   

3. *Install dependencies:*
   bash
   pip install -r requirements.txt
   

4. *Run migrations:*
   bash
   python manage.py makemigrations
   python manage.py migrate
   

5. *Create a superuser (admin):*
   bash
   python manage.py createsuperuser
   

6. *Run the development server:*
   bash
   python manage.py runserver
   

7. Open `http://127.0.0.1:8000/` in your browser.

---

## Usage
- Visit the homepage to view available events.
- Sign up or log in to make bookings.
- Use the admin panel at `/admin/` to manage events and users.

---

## File Structure

├── eventbooking/
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, images
│   ├── events/            # Event management app
│   ├── users/             # User authentication app
│   ├── db.sqlite3         # SQLite database
│   ├── manage.py          # Django management script
│   ├── requirements.txt   # Python dependencies
