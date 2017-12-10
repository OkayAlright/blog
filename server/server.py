from flask import Flask
from flask import url_for
from jinja2 import Template
import json
import markdown
import os
import random

class server(object):
    def __init__(self, conf_file):
        self.config = json.loads(open(conf_file,'r').read())

class common_templates():
    template = {item.split('.')[0]: open('./common/templates/'+item).read()
                for item in os.listdir('./common/templates')}


app = Flask(__name__)


def get_random_quote():
    quotes = open('./common/phrases.txt', 'r').read().split('\n')
    return quotes[random.randint(0,len(quotes))-1]

def format_post(post_markdown):
    return markdown.markdown(post_markdown)+'\n'


@app.route('/')
def main_page():
    name = 'Home'
    phrase = "Don't mistake the description of the city for the city itself. -Calvino"
    outer = Template(common_templates.template["header_and_title"])

    single_page_black_list = ['resume', 'contact']
    all_pages = [(item, item) for item in os.listdir('./pages')]
    post_pages = [item for item in all_pages if item[0] not in single_page_black_list]
    single_pages = [item for item in all_pages if item[0] in single_page_black_list]

    content = Template(common_templates.template["side_bar"])

    return outer.render(page_name=name,
                        phrase=get_random_quote(),
                        middle_content=content.render(post_page_names=post_pages,
                                                      single_pages=single_pages),
                        url_for=url_for)


@app.route('/pages/<name>')
def render_subpage(name):
    phrase = 'Goes to show that you can make something without the faintest clue of how it fucking works... -Es Devlin'

    outer = Template(common_templates.template["header_and_title"])
    nav = Template(common_templates.template["side_bar"])

    formatted = None

    if 'posts' in os.listdir('./pages/{}'.format(name)):
        posts = os.listdir('./pages/{}/posts'.format(name))
        unformatted_posts = [open('./pages/{}/posts/{}/post.md'.format(name, item)).read() for item in posts]
        formatted = [markdown.markdown(item) for item in unformatted_posts]

    single_page_black_list = ['Resume', 'Contact']
    all_pages = [(item, '../'+item) for item in os.listdir('./pages')]
    post_pages = [item for item in all_pages if item[0] not in single_page_black_list]
    single_pages = [item for item in all_pages if item[0] in single_page_black_list]

    content = None

    if 'landing.template' not in os.listdir('./pages/{}/'.format(name)):
        content = Template(open('./common/templates/landing.template'.format(name), 'r').read())
    else:
        content = Template(open('./pages/{}/landing.template'.format(name), 'r').read())

    return outer.render(page_name=name,
                        phrase=get_random_quote(),
                        middle_content=(nav.render(post_page_names=post_pages,
                                                   single_pages=single_pages)+
                                        content.render(posts=formatted)),
                        url_for=url_for)










