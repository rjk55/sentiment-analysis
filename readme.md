<!-- Project Title -->

# Product Sentiment Analysis

<!-- Short Description -->

This project is a sentiment analysis of product reviews. The goal is to predict the sentiment of a review based on the review text. The data set used is the Amazon Reviews dataset. The analysis is done using the pandas library in Python. The app can accept a product url(Amazon, Flipkart) and return the sentiment of the reviews.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Scalability](#scalability)
- [Future Work](#future-work)

## Installation

install requirements.txt

```bash
pip install -r requirements.txt
```

### Run the scrapper

```bash
python3 main.py <url>

# Example
python3 main.py "https://www.amazon.co.uk/Apple-iPhone-13-128GB-Starlight/dp/B09G9FB7LV/ref=cm_cr_arp_d_product_top?ie=UTF8"
```

### Run unit tests

```bash
python -m unittest
```

## Extras

- [Scalability](#scalability)
- [Future Scope](#future-scope)

## Modules

- [Web Server](#web-server)
- [Product URL Input](#product-url-input)
- [Product Review Scraper](#product-review-scraper)
- [Sentiment Analysis](#sentiment-analysis)
- [Data Visualization](#data-visualization)
- [Deployment](#deployment)
