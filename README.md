# TFL status checker

## About

This project has been setup to develop a CLI tool & dash app to report on overground / tube statuses

To run the dash app locally:

1) Navigate to the parent folder of this project
2) Ensure _requirements_ are installed - `pip install -r requirements.txt`
3) Run `python front/app.py`
     - The default port is 8050

Built with Python <img src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" width="20" height="20" />

* API with requests
* Dashboard with dash
* CLI tool

Data sourced from the [TFL "Unified API"](https://tfl.gov.uk/info-for/open-data-users/unified-api) (_access token required_)
