import requests
import logging
import configparser

token_url = "https://www.reddit.com/api/v1/access_token"
listings_url = "https://reddit.com/r/soccer/new.json"
listings_params = {"limit": "5"}
headers = {"User-Agent": "redditbot"}


class Post:
    def __init__(self, title, author, upvote_count):
        self.title = title
        self.author = author
        self.upvote_count = upvote_count

    def __repr__(self):
        return (
            f"Post(\n"
            f"    title={self.title},\n"
            f"    author={self.author},\n"
            f"    upvote_count={self.upvote_count}\n"
            f")"
        )


def load_config():
    config = configparser.ConfigParser()
    logger.info("Reading config file")
    config.read("config.ini")

    return {
        "client_id": config.get("credentials", "client_id"),
        "client_secret": config.get("credentials", "client_secret"),
        "username": config.get("credentials", "username"),
        "password": config.get("credentials", "password"),
    }


def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(levelname)s | %(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def get_access_token(credentials):
    request_body = {
        "grant_type": "password",
        "username": credentials["username"],
        "password": credentials["password"],
    }
    auth = (credentials["client_id"], credentials["client_secret"])

    try:
        logger.info("Requesting acesss token")
        response = requests.post(
            token_url,
            auth=auth,
            data=request_body,
            headers=headers,
        )

        response.raise_for_status()

    except requests.exceptions.HTTPError as err:
        logger.error("Failed to get access token %s", err)
        return None

    token = response.json().get("access_token")
    if not token:
        logger.error("Failed to get access token %s", response.text)
        return None

    headers["Authorization"] = f"bearer {token}"
    logger.info("Access token successfuly saved")


def get_listings(url=listings_url, params=listings_params):
    try:
        logger.info("Fetching listings at url=%s", listings_url)
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.error("Failed to get listings %s", err)
        return None

    return response.json()


def extract_posts(listings):
    if listings is None:
        logger.warning("No listings retrieved.")
        return
    else:
        logger.info("Successfully retrieved listings.")

    logger.info("Extracting posts from listings")
    posts = []
    for item in listings.get("data").get("children"):
        post_data = item.get("data")
        post_title = post_data.get("title")
        post_author = post_data.get("author")
        post_upvotes = post_data.get("ups")
        posts.append(Post(post_title, post_author, post_upvotes))

    return posts


if __name__ == "__main__":
    logger = init_logger()
    credentials = load_config()
    get_access_token(credentials)
    listings = get_listings()
    posts = extract_posts(listings)

    print(posts)
