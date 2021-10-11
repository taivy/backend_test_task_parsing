# Usage

Start app:

```
docker-compose up -d
```

Go to localhost:5000, there will be a form with inputs



# Architecture

The app has microservice architecture. There are 2 services: client service for interface (web form and showing result) and API service for parsing the site, * and * in docker-compose respectively. Interface service makes requests to API service to get results.
API service potentially could be scaled for higher loads.



# Settings


settings.ini in client folder - for client settings


If RETURN_ONLY_GENERAL_RESULTS_PAGE env var (in api service in docker-compose) is True, the returned url is like https://www.peoplesearchexpert.com/search?q%5Bfull_name%5D=Bob++Smith&q%5Blocation%5D=Fort+Worth%2C+TX otherwise https://www.peoplesearchexpert.com/people/bob-smith?state=Texas#fort-worth
