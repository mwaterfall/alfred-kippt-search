# -*- coding: utf-8 -*-

import time
import alfred
import kippt.kippt as kippt

def process(query_str):
    """ Entry point """
    if query_str and len(query_str) > 2:
        results = get_results(query_str)
        if results is not None:
            response = alfred_items_for_results(results)
            xml = alfred.xml(response) # compiles the XML answer
            alfred.write(xml) # writes the XML back to Alfred

def get_results(query_str):
    """ Return value for the query string """
    results = client.search(query_str)
    return results

def alfred_items_for_results(value):
    """ Create alfred items for each result """
    index = 0
    results = []
    meta, items = value
    if not meta:
        display_message('Invalid username or API key')
    if not items:
        display_message(None, 'No results found')
    for item in items:
        results.append(alfred.Item(
            title=item.get('title'),
            subtitle=item.get('url_domain'),
            attributes={
                'uid': alfred.uid(index), 
                'arg': item.get('url'),
            },
            icon='icon.png',
        ))
        index += 1
    return results

def display_message(message, subtitle=None):
    """ Inform them that something's wrong """
    if message is None:
        # Display same message as the placeholder
        message = 'Search your Kippt bookmarks'
    xml = alfred.xml([
        alfred.Item(
            title=message,
            subtitle=subtitle,
            attributes={
                'uid': alfred.uid(0),
            },
            icon='icon.png',
        )
    ]) # compiles the XML answer
    alfred.write(xml) # writes the XML back to Alfred
    exit()

if __name__ == "__main__":
    try:
        username = alfred.args()[0]
        api_key = alfred.args()[1]
        if not username or not api_key:
            raise ValueError()
        query_str = alfred.args()[2]
        client = kippt.user(username, api_key)
    except (IndexError, ValueError):
        display_message('Please add your Kippt username & API key to '
                        'the workflow script filter')
    process(query_str)
