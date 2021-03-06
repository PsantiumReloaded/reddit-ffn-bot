from urllib.parse import urlencode
from lxml.html import fromstring

from ffn_bot.searchengines.base import register, SearchEngine
from ffn_bot.searchengines.helpers import Throttled, Randomizing
from ffn_bot.searchengines.helpers import TagUsing

@register
class DuckDuckGoScraper(TagUsing, Throttled, Randomizing, SearchEngine):

    def __init__(self):
        super(DuckDuckGoScraper, self).__init__(
            requests=6,
            timeframe=Throttled.MINUTE
        )

    def _get_page(self, request):
        from ffn_bot import cache
        return fromstring(cache.default_cache.get_page(request))

    def _search(self, query, site=None, limit=1):
        # Retrieve the page.
        page = self._get_page(
            "https://duckduckgo.com/html/?" + urlencode({
                "q": query
            })
        )

        # Return our wanted results:
        return list(
            item.get("href")
            for item in page.cssselect(".links_main a")
        )[:limit]
