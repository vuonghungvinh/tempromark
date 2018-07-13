
import collections
import logging
import re

from django.db.models import Q


log = logging.getLogger(__name__)


# A hand-picked list of just the functional words from the 100 most-common
# english words list.
# http://oxforddictionaries.com/words/the-oec-facts-about-the-language
STOP_WORDS = set((
    'about', 'after', 'all', 'also', 'an', 'and', 'any', 'as', 'at',
    'back', 'be', 'because', 'but', 'by',
    'can', 'come', 'could',
    'day', 'do',
    'even',
    'for', 'from',
    'get', 'go',
    'have', 'he', 'her', 'him', 'his', 'how',
    'if', 'in', 'into', 'it', 'its',
    'just',
    'know',
    'like', 'look',
    'make', 'me', 'most', 'my',
    'new', 'no', 'not', 'now',
    'of', 'on', 'one', 'only', 'or', 'other', 'our', 'out', 'over',
    'say', 'see', 'she', 'so', 'some',
    'take', 'than', 'that', 'the', 'their', 'them', 'then',
    'there', 'these', 'they', 'think', 'this', 'to', 'two',
    'up', 'us', 'use',
    'way', 'we', 'well', 'what', 'when', 'which',
    'who', 'will', 'with', 'work', 'would',
    'you', 'your',
))


class TinySearch(object):
    """
    Simple searcher that will work with any database, including SQLite.

    Suitiable only for small data sets -- tens, or hundreds of objects only
    as a brute-force approach is used (see notes below for details).

    queryset
        Django database queryset to search on, eg.
            `Blog.objects.all`
            `Blog.objects.select_related('images')`

    fields
        Mapping of fields to search on to their weightings, eg.:
        dict(title=5, body=1)

    Notes:

    * Uses database LIKE search to fetch possible results from database, then
      regular expressions on all results to perform scoring and to eliminate
      bad matches.
    * Returns good results, but requires lots of CPU to do so.
    * DO NOT USE if your dataset is larger than about 1,000 items, or a
      couple of Megabytes in size.

    """
    def __init__(self, queryset, fields):
        self.fields = fields
        self.queryset = queryset

    def search(self, query):
        """
        Perform search against database.

        query
            String containing query, eg. 'Carrot and apple juice'

        Returns a standard library `collections.Counter` object containing
        matching objects and their scores.  Use its `most_common` method to
        get list of matches sorted by score.

        http://docs.python.org/2/library/collections.html#collections.Counter

        Results against multiple tables can be easily combined together using
        standard `collections.Counter` objects, eg:

            >>> r1 = searcher1.search('Banana Sundae')
            >>> r2 = searcher2.search('Desert wine')
            >>> results = r1 + r2
            >>> results = results.most_common()

        """
        tokens = self._tokenise(query)
        log.debug("Search for '%s' tokenised to '%s'", query, tokens)
        items = self._fetch(tokens)
        log.debug(
            "Search for '%s' fetched %s records from database",
            query, len(items))
        results = self._score(items, tokens)
        log.info("Search for '%s' found %s results", query, len(results))
        return results

    def _fetch(self, tokens):
        """
        Find and fetch all potential matches from the database.

        A brute-force, lowest common denominator, approach.
        """
        if not tokens:
            return []
        query = []
        for token in tokens:
            for field in self.fields:
                key = '{}__icontains'.format(field)
                q = Q(**{key: token})
                query.append(q)
        query = reduce(lambda x, y: x | y, query)
        items = self.queryset.filter(query)
        return items

    def _score(self, items, tokens):
        """
        Score objects found by database against a regular expression.

        Eliminates bad matches in the form of not-prefix sub-strings.  For
        example, the fetch method will return 'against' as a possible
        match for 'gain'.
        """
        results = collections.Counter()
        pattern = re.compile(
            r'\b{}'.format('|'.join(tokens)),
            re.IGNORECASE | re.MULTILINE)
        for item in items:
            score = 0
            for field, weight in self.fields.items():
                matches = pattern.findall(getattr(item, field))
                score += len(matches) * weight
            results[item] += score

        # Remove zero or negative scores
        results += collections.Counter()
        return results

    def _tokenise(self, query, max_tokens=4, min_length=3):
        """
        Break query in tokens.

        Avoid abuse by setting restrictions on the minimum length of the
        tokens, and the maximum number to search for.
        """
        tokens = query.split()
        # Remove stop words
        tokens = [x for x in tokens if x not in STOP_WORDS]
        # Remove too-short tokens
        tokens = [x for x in tokens if len(x) >= min_length]
        # Remove duplicates (while retaining order)
        unique = []
        for t in tokens:
            if t not in unique:
                unique.append(t)
        tokens = unique
        # Limit to reasonable number
        tokens = tokens[:max_tokens]
        return tokens
