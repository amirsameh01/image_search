# Django Selenium Image Search API

A Django API that accepts POST requests to the `/search/` endpoint. The API searches for the specified text (`stext`) in Google Images and findes the specified number of images (`scount`) & resizes them according to the defined scales(scales are defined in settings.py ln134). finally the service will save the resized images in a folder named `media` in the project directory (`MEDIA_ROOT, defined in settings.py ln130).

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)

## Getting Started

## Prerequisites

- Python 3.x
- WebDriver

### Installation
1) Create a virtual environment:
```bash
python -m venv venv
```
2) Activate the virtual environment:
```bash
venv\Scripts\activate
```
3) Install project dependencies:
```bash
pip install -r requirements.txt
```
### Configuration

1) Download ChromeDriver and replace the existing chromedriver.exe in the project directory from the link below.
   https://chromedriver.chromium.org/downloads

2) Create a .env file in the project directory with the following content:
```bash
DB_NAME=images
DB_USER=postgres
DB_PASSWORD=44414101
DB_HOST=127.0.0.1
DB_PORT=5432
```
Update the values accordingly.

### Usage

1) Apply database migrations:
```bash
python manage.py migrate
```
2) Run the development server:

```bash
python manage.py runserver
```
3) Send a POST request to the /search/ endpoint with the following JSON payload:

```bash
{
  "stext": "your search text",
  "scount": 5
}
```

Adjust the values of "stext" and "scount" as needed.
4) The API will search for the specified text in Google Images and save the specified number of images in the media folder.


