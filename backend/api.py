import requests
import collections
import hashlib
import string
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Comment
from w3lib.html import remove_tags_with_content

from flask import Flask, request, jsonify
from flask_cors import CORS

# Flask initialization
app = Flask(__name__)
CORS(app)

# Scraper variables
visited_urls = set()
visited_hashes = set()
queue = collections.deque()
index = collections.defaultdict(list)
depth_limit = 3



@app.route('/clear/', methods=['GET'])
def clear():
    global visited_urls
    global visited_hashes
    global queue
    global index

    visited_urls = set()
    visited_hashes = set()
    queue = collections.deque()
    index = collections.defaultdict(list)

    return jsonify({
        'message': 'Search Index Cleared',
    })


@app.route('/search/', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if keyword:
        kw = keyword.lower()
        if kw in index:
            results = [r for r in index[kw] if r['title'] is not None and r['title'] is not '']
            results = sorted(results, key=lambda x: x['word_count'], reverse=True)
            return jsonify({
                'search_results': results,
                'number_of_results': len(results)
            })

    return jsonify({
        'search_results': [],
        'number_of_results': 0
    })


@app.route('/index/', methods=['GET'])
def crawl():
    global visited_urls
    global visited_hashes
    global queue
    pages_crawled, words_found = 0, 0

    # Set depth limit - may want to crawl less than 3 levels
    global depth_limit
    depth = request.args.get('depth')
    if depth:
        depth_limit = int(depth)

    start_url = request.args.get('url')
    if start_url:
        queue.append((start_url, 1))

        while queue:
            url, depth = queue.popleft()
            if url not in visited_urls:
                visited_urls.add(url)

                try:
                    response = requests.get(url, timeout=5)
                except Exception:
                    print('Exception')
                    response = None

                if (response is not None and
                        response.status_code == requests.codes.ok and
                        'text/html' in response.headers['Content-Type']):
                    # Need to create and check hash since multiple urls could have identical content
                    page_content = BeautifulSoup(
                        remove_tags_with_content(response.content, ('script', 'style')), 'html.parser')
                    hash = hashlib.md5(page_content.get_text().encode()).hexdigest()
                    if hash not in visited_hashes:
                        visited_hashes.add(hash)
                        if page_content:
                            pages_crawled += 1
                            words_on_page = create_index(page_content, url)
                            words_found += words_on_page
                            add_pages_to_queue(page_content, url, depth)

    return jsonify({
        'pages_crawled': pages_crawled,
        'words_found': words_found,
    })


def create_index(page_content, url):
    '''Modifies dictionary structure that will be used for searching'''
    global index
    words = get_words(page_content)
    title = ''
    if page_content.title:
        title = page_content.title.string

    for word, count in words.items():
        entry = {
            'url': url,
            'title': title,
            'word_count': count
        }
        index[word].append(entry)

    return len(words)


def get_words(page_content):
    '''Returns Counter(dict) of words and their counts'''
    text = []
    table = str.maketrans('', '', string.punctuation)
    pieces = page_content.findAll(text=lambda text: not isinstance(text, Comment))
    pieces = [p.strip() for p in pieces]
    for piece in pieces:
        words = piece.split()
        words_no_punc = []
        for w in words:
            wnp = w.translate(table).lower()
            if wnp:
                words_no_punc.append(wnp)
        text.extend(words_no_punc)

    return collections.Counter(text)


def add_pages_to_queue(page_content, url, depth):
    if depth+1 <= depth_limit:
        for link in page_content.findAll('a'):
            abs_path_link = urljoin(url, link.get('href'))
            if abs_path_link.startswith('http'):
                queue.append((abs_path_link, depth+1))
