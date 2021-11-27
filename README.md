# Transactional Email Service API

This is a submission for the Senior Software Engineer position at Rupa Health utilizing the Django REST Framework to create an API for a transactional email service in accordance with the specifications given for the technical interview.

## Installation

It is recommended that you use conda or another virtual environment when installing this application. Instructions for Conda installation here: https://docs.conda.io/en/latest/miniconda.html#installing

Create a new environment and activate whichever virtual environment system you use.

From the root project directory (/emailservice) install all necessary python packages by running:

```
make install
```

Then, run database migrations by running:

```
make build
```

Before running the application, you will need to add a handful of OS Environment variables for Mailgun and Sendgrid:

```
export MAILGUN_API_URL=...
export MAILGUN_API_KEY=...
export SENDGRID_API_URL=...
export SENDGRID_API_KEY=...
```

Finally, ensure that you have no other applications running on port 8000 and run

```
make serve
```

As an additional note, if you want to change default email providers from Mailgun to Sendgrid, simply change the default value in `/emailservice/emailservice/settings.py` under `USE_MAILGUN_SERVICE_AS_DEFAULT`

## Technologies Used

- Python 3.8
- Django REST Framework
- Django
- Vanilla Python for the rest

I decided to use Django for this application as I was informed that Django was used at Rupa Health. I also happen to have several years of experience with Django, so together the use of the framework seemed ideal.

I added on the Django REST Framework as it is an excellent addition to the Django ecosystem for RESTful APIs. I especially found the serializers to be useful for this application when validating and cleaning the JSON submissions.

## Tradeoffs

If I were to spend additional time on this project I would add in support for the templating that comes default with both the mailgun and sendgrid services. These seem extremely powerful and could potentially alleviate any issues that would arise when using plaintext/html in the email body.

I ran into a bit of a roadblock with the sendgrid api for about 30 minutes, which left me short on time over the weekend to write unit tests that covered validation and cleaning of the JSON fields submitted over the POST request. If I had more time I would have liked to implement those tests to provide a broader coverage of edge cases and functionality.

## Time Spent on Exercise

I spent about 3 hours on this exercise, ~30 minutes of that was spent debugging a few typos I had when writing the POST body for the Sendgrid request.

## Additional Comments

This wasn't necessarily a tradeoff, but when deciding on what framework/package to use for the API I was considering using FastAPI instead of Django. I did not because Rupa Health uses Django, but if I were to have more time I would love to implement this API in FastAPI. I find it to be a much more robust way to write RESTful APIs in Python, and it is what I use daily at my current position at Novozymes.
