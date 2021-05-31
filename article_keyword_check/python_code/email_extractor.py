import re
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup


def web_email_crawler(url_input):

    craws_time = 0
    # starting url. replace google with your own url.
    starting_url = url_input


    # a queue of urls to be crawled
    unprocessed_urls = deque([starting_url])

    # set of already crawled urls for email
    processed_urls = set()

    # a set of fetched emails
    emails = set()

    # process urls one by one from unprocessed_url queue until queue is empty
    while len(unprocessed_urls):

        # move next url from the queue to the set of processed urls
        url = unprocessed_urls.popleft()
        # processed_urls.add(url)

        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        # get url's content
        # print("Crawling URL %s" % url)
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # ignore pages with errors and continue with next url
            continue

        # extract all email addresses and add them into the resulting set
        # You may edit the regular expression as per your requirement
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)
        print(emails)
        # create a beutiful soup for the html document
        soup = BeautifulSoup(response.text, 'lxml')

        # Once this document is parsed and processed, now find and process all the anchors i.e. linked urls in this document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            # resolve relative links (starting with /)
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            # add the new url to the queue if it was not in unprocessed list nor in processed list yet
            if not link in unprocessed_urls and not link in processed_urls:
                unprocessed_urls.append(link)
        if craws_time <= 25:
            craws_time += 1
        else:
            break

    for mail in emails:
        print(mail)

    return emails






from requests_html import HTMLSession

def my_email():
    # page url
    url = r"https://www.prothomalo.com/"

    # regex pattern
    pattern = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"

    # initialize the session
    session = HTMLSession()

    # send the get request
    response = session.get(url)

    # simulate JS running code
    response.html.render()

    # get body element
    body = response.html.find("body")[0]

    # extract emails
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", body.text)

    for index, email in enumerate(emails):
        print(index + 1, "---->", email)
