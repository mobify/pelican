# -*- coding: utf-8 -*-
'''
Absolutize relative URLs in Articles.

Useful to ensure RSS feeds include absolute URLs.

'''
from pelican import signals
from pelican.contents import Article

from lxml.html import fromstring, tostring


def _update_content(self, content, siteurl):
    '''
    Monkey-patch `article.content` to absolutize links relative to `siteurl`.

    '''
    content = super(Article, self)._update_content(content, siteurl)
    document = fromstring(content)
    document.make_links_absolute(siteurl)
    content = tostring(document)
    return content


def absolutize(sender):
    Article._update_content = _update_content


def register():
    signals.initialized.connect(absolutize)