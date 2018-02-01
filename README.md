# Test API
This is just a Test API. An API that help you to test your XPATH

## Installation
We assume that you already spin `extract.api`, so you just need to install this Test API
  1. `pip install -r requirements.txt`
  2. `gunicorn run:api -b 0.0.0.0:8001 --relaod`


## Configuration
The configuration of this Test API is located in `lib/config.py`. Please only and only modify configuration to avoid unwanted risk.