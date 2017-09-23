from bs4 import BeautifulSoup as bs
from bs4 import Comment
import html


# This function adds label '&trade; ' (TM) to all words with 'size'
def add_labels(string, size=6, label='&trade;'):
    string = string + ' '  # add additional space to the end
    counter = 0
    changes = []  # {'index': 1, 'size': 6} - index of start and length of the word
    for i in range(len(string)):
        if string[i] != ' ':
            counter += 1
        else:
            if counter == size:
                changes.append({'index': i - counter, 'size': counter})
                counter = 0
            else:
                counter = 0

    res = string
    inserted = 0
    for ch in changes:
        i = ch['index'] + ch['size'] + len(label) * inserted  # insert index
        res = res[:i] + label + res[i:]  # insert label
        inserted += 1
    return res[:-1]  # remove additional space


# It takes [requests] content and transform html tags
def transform_request(content, port=8080):
    soup = bs(content, 'lxml')
    exclude_tags = ['script', 'style', 'noscript', 'meta', 'link', 'code']  # skip changing certain tags

    # Remove comment tags <-- -->
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    # Add TM tag to all long words
    for element in soup.find_all(text=True):
        text = element.string
        if text and False not in [element.find_parent(x) is None for x in exclude_tags] and text != 'html':
            element.replace_with(add_labels(text))

    # Change urls
    local_url = "http://localhost:{port}".format(port=port)
    for a in soup.findAll('a', href=True):
        a['href'] = a['href'].replace("https://habrahabr.ru", local_url)
        a['href'] = a['href'].replace("http://habrahabr.ru", local_url)

    return html.unescape(soup.prettify(formatter="html"))
