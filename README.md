# Cropmaster

Cropmaster is an application designed to connect farmers, experts, and buyers in the agricultural industry. It provides features such as crop management, product listing, expert consultation, and community forums. This repository will serve as a backend for this platform.

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Contributing](#contributing)

## Project Description

Cropmaster aims to smoothen agricultural processes by facilitating communication and collaboration between different stakeholders in the industry. It provides farmers with communication tool to manage their crops, sell their products, seek advice from experts, and engage with the community.

## Features

- User registration and authentication
- Crop management for farmers
- Product listing and purchasing for buyers
- Expert consultation for farmers
- Community forums for discussions and knowledge sharing

## Technologies Used

- Django
- Django REST Framework
<!-- - PostgreSQL -->

## Installation

To run Cropmaster locally, follow these steps:

1. Clone the repository:


    `git clone https://github.com/CROPMASTER-FYP/cropmaster_backend.git`


2. Navigate to the project directory: 

    `cd cropmaster_backend`


3. Install dependencies: 

    `pip install -r requirements.txt`


4. Create migration files: 

    `python manage.py makemigrations accounts buyer crops extofficer farmer forum orders`


5. Set up the database: 

    `python manage.py migrate`


6. Start the development server: 


    `python manage.py runserver`


7. Open your web browser and go to 


    `http://localhost:8000`


## Contributing

To contribute, follow these steps:

1. Fork the repository
2. Create a new branch: 

    `git checkout -b feature-name`

3. Make your changes and commit them: 

    `git commit -m 'Add new feature'`


4. Push to the branch: 

    `git push origin feature-name`


5. Submit a pull request

