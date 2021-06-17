from flask import Flask
import re
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)


@app.route('/')
@app.route('/<number>')
def search(number=None):
    if number is None:
        return 'hello world'
    else:
        if '+82' in number:
            number = number.replace('+82', '0')
        number = re.sub(r"\D", "", number)
        if number[:2] == '00':
            number = number[1:]

        response = requests.get(f'http://whosnumber.com/kr/{number}')
        response.raise_for_status()

        parser = BeautifulSoup(re.sub(r'\r?\n', '', response.text), 'lxml')

        comments = []
        for idx, node in enumerate(parser.select('#comments .panel-body')):
            comment = node.text.split('                ')[0].strip()
            comments.append(comment)

            if idx > 3:
                break

        return os.linesep.join(comments)
