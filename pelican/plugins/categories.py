"""
Adds support for multiple categories in Pelican by treating the `category`
attribute like the `tag` attribute.

Requires a modification to `generators.ArticlesGenerator.generate_context` to
allow articles to have multiple categories.

"""
from collections import defaultdict

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

        # Lowercase names.
        # self.name = self.name.lower()

        remap = settings.get("CATEGORY_MAP", {}).get(self.slug, {})
        for key, value in remap.items():
            print "REMAPPED", self, key, value
            setattr(self, key, value)


def fix_article_metadata(generator, metadata):
    """
    Generate slugs for Articles that are missing them.

    Normalize Author Names.

    """
    if "slug" not in metadata:
        category_slug = metadata["category"][0].slug
        article_slug = slugify(metadata["title"])
        slug = "%s/%s" % (category_slug, article_slug)
        metadata["slug"] = slug

    # author = metadata.get("author", None)
    # if author is not None:
    #     import pdb;pdb.set_trace()
    #     metadata["author"] = author.lower()

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