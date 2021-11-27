"""Utils file for email api endpoint."""

import requests
from emailservice import settings
from html.parser import HTMLParser


def _handle_data(self, html):
    """Handle data helper for HTMLParser.

    Source: https://stackoverflow.com/a/63899308

    Parameters
    ----------
    html: str
        Split html value.
    """
    self.text += html + "\n\n"


HTMLParser.handle_data = _handle_data


def html_to_plain_text(html):
    """Converts html to plain text.

    Parameters
    ----------
    html: str
        Entire html string to convert to plain text

    Returns
    -------
    parsert.text.strip(): str
        Plain text.
    """
    parser = HTMLParser()
    parser.text = ""
    parser.feed(html)

    return parser.text.strip()


def send_email(email_data, override_default=False):
    """Send email to default API.

    Parameters
    ----------
    email_data: dict
        Email data from JSON body of POST.
    override_default: bool
        Determine whether to use default email service or not.

    Returns
    -------
    dict
        Dictionary containing message, service, and status code of email service request
    """
    use_mailgun_as_default = settings.USE_MAILGUN_SERVICE_AS_DEFAULT

    if override_default:
        use_mailgun_as_default = not use_mailgun_as_default

    if use_mailgun_as_default:
        return send_to_mailgun(email_data)
    else:
        return send_to_sendgrid(email_data)


def send_to_mailgun(email_data):
    """Sends email to mailgun API.


    Parameters
    ----------
    email_data: dict
        Email data from POST request.

    Returns
    -------
    dict
        Dictionary containing message, service, and status code of email service request
    """
    response = requests.post(
        f"{settings.MAILGUN_API_URL}/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={
            "from": f'{email_data["from_name"]} <{email_data["from_email"]}>',
            "to": [f'{email_data["to_name"]} <{email_data["to_email"]}>'],
            "subject": email_data["subject"],
            "text": html_to_plain_text(email_data["body"]),
            "html": email_data["body"],
        },
    )

    return {
        "status_code": response.status_code,
        "message": response.json()["message"],
        "type": "MAILGUN",
    }


def send_to_sendgrid(email_data):
    """Sends email to sendgrid API.

    Parameters
    ----------
    email_data: dict
        Email data from POST request.

    Returns
    -------
    dict
        Dictionary containing message, service, and status code of email service request
    """
    response = requests.post(
        f"{settings.SENDGRID_API_URL}/mail/send",
        headers={
            "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
            "content-type": "application/json",
        },
        json={
            "personalizations": [
                {
                    "to": [
                        {"email": email_data["to_email"], "name": email_data["to_name"]}
                    ]
                }
            ],
            "subject": email_data["subject"],
            "content": [
                {"type": "text/plain", "value": html_to_plain_text(email_data["body"])}
            ],
            "from": {
                "email": email_data["from_email"],
                "name": email_data["from_name"],
            },
            "reply_to": {
                "email": email_data["from_email"],
                "name": email_data["from_name"],
            },
        },
    )

    if response.status_code == 202:
        return {
            "status_code": response.status_code,
            "message": "Your message has been sent",
            "type": "SENDGRID",
        }

    return {
        "status_code": response.status_code,
        "message": response.json()["errors"],
        "type": "SENDGRID",
    }
