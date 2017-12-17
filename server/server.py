"""
server.py

A simple little blog server in Flask.

For usage and organization, refer to the README (Logan, write the README)

Usage:
    flask server.py
"""
import json
import markdown
import os
import random
from flask import Flask
from flask import url_for
from jinja2 import Template

version = '0.1'
app = Flask(__name__)
app.base_url = os.path.dirname(os.path.realpath(__file__))


class Config(object):
    config_file = open('./config.json')
    server_config = json.load(config_file)
    config_file.close()


class CommonTemplates():
    template = {item.split('.')[0]: open('./common/templates/'+item).read()
                for item in os.listdir('./common/templates')}


def get_random_quote():
    with open('./common/phrases.txt', 'r') as file:
        quotes = file.read().split('\n')
        return quotes[random.randint(0,len(quotes))-1]


def get_ignores():
    with open('./common/ignores.txt', 'r') as file:
        folders_to_ignore = file.read().split('\n')
        return folders_to_ignore


def format_post(post_markdown):
    return markdown.markdown(post_markdown)+'\n'


def separate_pages(all_pages_tuple):
    single_page_black_list = Config.server_config["Single Post Pages"]
    post_pages = [item for item in all_pages_tuple if item[0] not in single_page_black_list]
    single_pages = [item for item in all_pages_tuple if item[0] in single_page_black_list]
    return {
        "multi post": post_pages,
        "single post": single_pages
    }


def get_categorized_pages():
    all_pages = [(item, '/pages/'+item) for item in os.listdir(app.base_url+'/pages')
                 if item not in get_ignores()]
    return separate_pages(all_pages)


@app.route('/')
def main_page():
    outer = Template(CommonTemplates.template["header_and_title"])
    page_groups = get_categorized_pages()
    content = Template(CommonTemplates.template["side_bar"])

    return outer.render(page_name=Config.server_config["Index Name"],
                        display_name=Config.server_config["Display Name"],
                        phrase=get_random_quote(),
                        middle_content=content.render(post_page_names=page_groups["multi post"],
                                                      single_pages=page_groups["single post"]),
                        url_for=url_for)

@app.route('/pages/<name>')
def render_subpage(name):
    outer = Template(CommonTemplates.template["header_and_title"])
    nav = Template(CommonTemplates.template["side_bar"])

    page_groups = get_categorized_pages()

    if 'posts' in os.listdir('./pages/{}'.format(name)):
        posts = os.listdir('./pages/{}/posts'.format(name))
        unformatted_posts = [open('./pages/{}/posts/{}/post.md'.format(name, item)).read() for item in posts]
        formatted = [markdown.markdown(item) for item in unformatted_posts]
    else:
        formatted = []

    if 'landing.template' not in os.listdir('./pages/{}/'.format(name)):
        content = Template(open('./common/templates/landing.template'.format(name), 'r').read())
    else:
        content = Template(open('./pages/{}/landing.template'.format(name), 'r').read())

    return outer.render(page_name=name,
                        display_name=Config.server_config["Display Name"],
                        phrase=get_random_quote(),
                        middle_content=(nav.render(post_page_names=page_groups["multi post"],
                                                   single_pages=page_groups["single post"])+
                                        content.render(posts=formatted)),
                        url_for=url_for)
