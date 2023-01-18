<!-- Project Title -->

# Product Sentiment Analysis

<!-- Short Description -->

This project is a sentiment analysis of product reviews. The goal is to predict the sentiment of a review based on the review text. The app can accept a product url(Amazon, Flipkart, Currys) and return the sentiment of the reviews and a recommendation based on the sentiment. The reviews are scraped from the product page using `Beautiful Soup` in the real-time and the sentiment analysis is done using `NLTK` and `Pandas`.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Scalability](#scalability)
- [Future Work](#future-work)

## Features

- Real-time sentiment analysis of product reviews
- Fake review detection
- Recommendation based on the sentiment

## Installation

install required libraries using `pip`

```bash
pip install -r requirements.txt
```

### Run the project

```bash
python manage.py runserver

```

### Usage

Head to the url `http://localhost:8000/` and enter the product url.

Example url:
https://www.amazon.co.uk/Apple-iPhone-13-128GB-Starlight/dp/B09G9FB7LV/ref=cm_cr_arp_d_product_top?ie=UTF8

### Run unit tests

```bash
python manage.py test
```

## Libraries and Frameworks Used

- [Django](https://www.djangoproject.com/) - The web framework used
- [Pandas](https://pandas.pydata.org/) - Data analysis
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web scraping
- [NLTK](https://www.nltk.org/) - Natural Language Processing
- [Requests](https://requests.readthedocs.io/en/master/) - HTTP requests
- [TextBlob](https://textblob.readthedocs.io/en/dev/) - Text processing
- [Chart.js](https://www.chartjs.org/) - Data visualization
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework

## Deployment

The project can be deployed as normal Django project. Use `AWS Elastic Cloud` or `Heroku` for deployment.

- https://docs.djangoproject.com/en/4.1/howto/deployment/

## Extras

- [Scalability](#scalability)
- [Future Scope](#future-scope)
