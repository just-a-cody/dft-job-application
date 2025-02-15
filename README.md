# Job Application of DfT Software Developer

This is a full-stack web application built with Django framework. In order to fullfil the user requirement, which is to use API to serve the data, this project uses Django REST framework to create API endpoints rather than directly querying Django models in the views, providing a clean separation between the backend API and frontend interface.

## Project Overview

Develop a simple Contacts web application that stores information such as name, address, and telephone numbers for contacts. Users should be able to see a list of contacts, as well as be able to perform CRUD activity for contacts. This application should:

- Demonstrate your ability to build a basic web application.
- Showcase your proficiency with web development frameworks and tools.

## User Requirements

- Use any web framework (Django recommended) to build a styled web front-end interface
- Store data in a database (SQLite recommended)
- Create a basic API endpoint to serve the application's data
- Add dynamic UI interactions (Good to have, DOM updates)
- Only need to run locally
- Use version control like Git and publish to GitHub
- Include README with:
  - Clone instructions
  - Dependency setup
  - How to run locally guide
  - Production deployment notes to cloud service

## Tech Stack

Here are the tech stack used in this project:

### Programming Language

- Python 3.10+

### Frameworks

- Django 5.0+
- Tailwind CSS 4.0
- DaisyUI 5.0

## Get Started

To install dependencies:

```bash
pip install -r requirements.txt
```

### Backend

To run the backend server:

```bash
cd api
fastapi run main.py
```

### Frontend

To run the frontend Django server:

```bash
cd frontend
python manage.py runserver
```

This project was created using `django-admin startproject` in Django 5.0.
