# RedditProject
 
# RedditProject - Discussion Platform for News

**RedditProject** is a discussion platform for sharing and commenting on news, inspired by Reddit. Users can create news posts, comment on posts, and engage in discussions across various categories like Technology, Education, and more.

## Overview

RedditProject provides an easy-to-navigate interface for users to discuss trending topics and news. It includes voting features, profile management, and category-based navigation to ensure an engaging user experience.


## Features
1. **Login to your profile account**: on the site, the user can log in to an account or register for further use, if the user has forgotten his password, he can click on the forgot password button, after which the user will receive an email notification to change the password.
![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-5.png)
![alt text](image-6.png)
1. **Post Creation and Interaction**: Users can create posts about news and current events. Each post supports likes and dislikes to show community engagement.
2. **Commenting System**: Users can leave comments on posts to join discussions.
3. **Category-based Navigation**: News posts are organized by categories, making it easier for users to find topics of interest.
4. **Search Functionality**: Search through posts to quickly find relevant discussions.
5. **User Profiles**: Users have profile pictures (avatars) and can view their activity history.



## Technologies Used

- **Backend**: Django, with SQLite for local development and PostgreSQL for production.
- **Frontend**: HTML, CSS, and JavaScript.
- **Hosting**: Heroku for easy deployment and scaling.
- **Authentication**: Django’s built-in authentication system.

---

## Project Structure

```plaintext
RedditProject/
├── media/                  # User media files (avatars)
│   └── avatars/            # Folder with user avatars
├── news/                   # News application
│   ├── management/         # Custom management commands
│   ├── migrations/         # Database migrations
│   ├── static/             # Static files (CSS, images) for the news app
│   ├── templates/          # HTML templates for rendering news pages
│   ├── models.py           # Database models for the news app
│   ├── views.py            # Views for handling news-related requests
│   └── urls.py             # URL routes for the news app
├── news_site/              # Main site configuration
│   ├── static/             # Global static files for the site
│   ├── settings.py         # Django settings for the project
│   ├── urls.py             # Main URL routes for the site
│   └── wsgi.py             # WSGI entry point for deployment
├── venv/                   # Python virtual environment
├── db.sqlite3              # SQLite database (for local development)
├── manage.py               # Django’s command-line utility
├── Procfile                # Heroku deployment instructions
└── requirements.txt        # List of Python dependencies
```

---

## Installation and Setup

To run RedditProject locally, follow these steps:

### Prerequisites

- Python 3.8+
- Django
- SQLite (for local development)
- PostgreSQL (for production)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/RedditProject.git
   cd RedditProject
   ```

2. **Set Up Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate   # Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the project root and add the following variables:

   ```plaintext
   DATABASE_URL=postgres://username:password@localhost:5432/redditproject_db
   SECRET_KEY=your_secret_key
   DEBUG=True  # Set to False in production
   ```

5. **Initialize the Database**

   Run migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (for admin access)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

8. Open `http://127.0.0.1:8000` in your browser to access the application.

---

## Deployment to Heroku

1. **Log in to Heroku**

   ```bash
   heroku login
   ```

2. **Create a Heroku App**

   ```bash
   heroku create your-app-name
   ```

3. **Add PostgreSQL Database**

   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set Environment Variables**

   ```bash
   heroku config:set SECRET_KEY=your_secret_key DEBUG=False
   ```

5. **Deploy the App**

   ```bash
   git push heroku main
   ```

6. **Run Database Migrations on Heroku**

   ```bash
   heroku run python manage.py migrate
   ```

7. Your app is now live at `https://your-app-name.herokuapp.com`.

---

## Contributing

We welcome contributions from the community! Please fork the repository, create a new branch, commit your changes, and open a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using **RedditProject**! We hope you find it engaging and useful.


 
