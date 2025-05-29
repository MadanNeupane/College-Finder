# College Finder Appplication

![walkthrough](walkthrough.gif)
![Predicting Chances + Dark Mode](chance_prediction.gif)

### [https://collegefinderapp.herokuapp.com](https://collegefinderapp.herokuapp.com/)

A platform for graduate college aspirants.

## Current Features

- Beautiful interactive dashboard with vizualization
- More than 1500 universities
- Admission Chance Prediction using Machine Learning algorithm
- College Comparison
- Blogs
- Bookmarks feature
- Dark Mode
- All Device Responsive

## Getting started with development

Dependencies:

- Python 3.9.x
- pip 21.1.x
- Django 3.2.x

### 1. Clone this repository

```
git clone https://github.com/MadanNeupane/College-Finder.git
```

### 2. Install virtual environment

```bash
pip install virtualenv
```

Follow [instructions on official documentation page](https://virtualenv.pypa.io/en/latest/).

### 3. Create virtual environment in project and activate it

To create:

```bash
virtualenv env
```

To activate:

On windows `\env\Scripts\activate.bat`

Linux or, Using git CLI `source ./env/Scripts/activate`

### 4. Install python packages

```bash
pip install -r requirements.txt
```

### 5. Set up the environ variables

_Sample config instuctions can be found on `.env_sample_file` file_

### 6. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create superuser

```bash
python manage.py createsuperuser
```

### 8. Run development server

```bash
python manage.py runserver
```

## Hosted on:

- [GitHub](https://github.com/MadanNeupane/College-Finder)
- ~~Heroku: [Live](https://collegefinderapp.herokuapp.com/)~~
- Render: [Live](https://college-finder-m534.onrender.com/)

## License

Restricted to University of Wolverhampton for assessment.

© Madan Neupane, 2021
