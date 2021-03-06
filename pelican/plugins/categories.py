"""
Adds support for multiple categories in Pelican by treating the `category`
attribute like the `tag` attribute.

Requires a modification to `generators.ArticlesGenerator.generate_context` to
allow articles to have multiple categories.

"""
from collections import defaultdict
import os

from pelican import signals
from pelican.contents import Category as BaseCategory
from pelican.readers import _METADATA_PROCESSORS
from pelican.utils import slugify


_METADATA_PROCESSORS["category"] = lambda x, y: [
        Category(category.strip(), y)
        for category in unicode(x).split(",")
    ]


class Category(BaseCategory):
    """
    A Category whose attributes can be remapped using the setting `CATEGORY_MAP`.

    """
    def __init__(self, name, settings):
        super(BaseCategory, self).__init__(name, settings)
        attributes = settings["CATEGORY_MAP"].get(self.slug, {})

        if "slug" not in attributes:
            attributes["slug"] = "blog/category/%s" % self.slug

        for key, value in attributes.items():
            setattr(self, key, value)

        # Our feeds don't live in the same place as our categories, so create a
        # custom `feed_slug` to store where the feed should live.
        self.feed_slug = self.slug.rsplit("/")[-1]


def fix_article_metadata(generator, metadata, source_path):
    """
    Articles without slugs are permalinked at "/blog/:filename".

    """
    if "slug" not in metadata:
        basename = os.path.basename(source_path)
        name = os.path.splitext(basename)[0]
        slug = "blog/%s" % name
        metadata["slug"] = slug


def fix_categories(generator):
    generator.categories = defaultdict(list)
    for article in generator.articles:
        # @jb: If the article doesn't have a category, this won't work.
        if not isinstance(article.category, list):
            print 'NO CATEGORY:', article.title
            continue

        for category in article.category:
            generator.categories[category].append(article)

    generator.categories = list(generator.categories.items())
    generator._update_context(("categories",))


def register():
    signals.article_generator_finalized.connect(fix_categories)

    signals.article_generate_context.connect(fix_article_metadata)