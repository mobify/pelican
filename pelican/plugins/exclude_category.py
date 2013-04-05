# -*- coding: utf-8 -*-
"""
    Exclude the given category from article lists, author pages and tag pages
"""

from pelican import signals
from pelican.contents import Article

def exclude_category(sender):

    import pdb;
    category_slug = sender.settings['EXCLUDED_CATEGORIES']

    print '*** EXAMINING ARTICLES LIST ***'

    # Remove all articles with provided category from the articles list
    for article in sender.articles:
        for category in article.category:
            if category_slug.encode('utf8') == category.feed_slug.encode('utf8'):
                print 'Article found with category ', category_slug
                sender.articles.remove(article)

    print '*** EXAMINING TAGS LIST ***'

    # Remove all articles with provided category from the tags list
    for tag in sender.tags:
        # The tags are a dict of type tag: article
        for article in sender.tags[tag]:            
            for category in article.category:
                if category_slug.encode('utf8') == category.feed_slug.encode('utf8'):
                    print 'Article with tag', tag.slug, ' found with category ', category_slug
                    sender.tags[tag].pop()

    print '*** EXAMINING AUTHORS LIST ***'

    # Remove all articles with provided category from the authors list
    for author in sender.authors:
        # sender.authors is a type tuple with [0]: author and [1]: list of articles
        for article in author[1]:
            for category in article.category:
                if category_slug.encode('utf8') == category.feed_slug.encode('utf8'):
                    print 'Author', author[0].slug, ' found with category ', category_slug
                    author[1].remove(article)

def register():
    signals.article_generator_finalized.connect(exclude_category)