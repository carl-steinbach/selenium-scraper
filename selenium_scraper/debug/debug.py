from bs4 import BeautifulSoup
from pprint import pprint


def print_local_html(html, tag_name, class_name):
    soup = BeautifulSoup(html, "html.parser")
    result = soup.find(tag_name, {"class": class_name})
    print(f"-------------------------------------[ result for <{tag_name} class='{class_name}'> ]-------------------------------------")
    pprint(result)