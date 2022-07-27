import datetime
import functools
from bs4 import BeautifulSoup
import requests
import time

# Based on https://github.com/goldsmith/Wikipedia

API_URL = 'https://nonciclopedia.org/w/api.php'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'


class WikipediaPage(object):
    def __init__(self, title=None, pageid=None, redirect=True, preload=False, original_title=''):
        if title is not None:
            self.title = title
            self.original_title = original_title or title
        elif pageid is not None:
            self.pageid = pageid
        else:
            raise ValueError("Either a title or a pageid must be specified")
        self.__load(redirect=redirect, preload=preload)
        if preload:
            for prop in ('content', 'summary', 'images', 'references', 'links', 'sections'):
                getattr(self, prop)

    def __load(self, redirect=True, preload=False):
        query_params = {
            'prop': 'info|pageprops',
            'inprop': 'url',
            'ppprop': 'disambiguation',
            'redirects': '',
        }
        if not getattr(self, 'pageid', None):
            query_params['titles'] = self.title
        else:
            query_params['pageids'] = self.pageid

        request = _wiki_request(query_params)
        query = request['query']
        pageid = list(query['pages'].keys())[0]
        page = query['pages'][pageid]

        if 'missing' in page:
            if hasattr(self, 'title'):
                raise Exception(self.title)
            else:
                raise Exception(pageid=self.pageid)
        elif 'redirects' in query:
            if redirect:
                redirects = query['redirects'][0]
                if 'normalized' in query:
                    normalized = query['normalized'][0]
                    assert normalized['from'] == self.title, "ERROR! REPORT!"
                    from_title = normalized['to']
                else:
                    from_title = self.title
                assert redirects['from'] == from_title, "ERROR! REPORT!"
                self.__init__(redirects['to'], redirect=redirect, preload=preload)
            else:
                raise Exception(getattr(self, 'title', page['title']))
        elif 'pageprops' in page:
            query_params = {
                'prop': 'revisions',
                'rvprop': 'content',
                'rvparse': '',
                'rvlimit': 1
            }
            if hasattr(self, 'pageid'):
                query_params['pageids'] = self.pageid
            else:
                query_params['titles'] = self.title
            request = _wiki_request(query_params)
            html = request['query']['pages'][pageid]['revisions'][0]['*']

            lis = BeautifulSoup(html, 'html.parser').find_all('li')
            filtered_lis = [li for li in lis if not 'tocsection' in ''.join(li.get('class', []))]
            may_refer_to = [li.a.get_text() for li in filtered_lis if li.a]

            raise Exception(getattr(self, 'title', page['title']), may_refer_to)
        else:
            self.pageid = pageid
            self.title = page['title']
            self.url = page['fullurl']

    @property
    def content(self):
        if not getattr(self, '_content', False):
            query_params = {
                'prop': 'extracts|revisions',
                'explaintext': '',
                'rvprop': 'ids'
            }
            if not getattr(self, 'title', None) is None:
                query_params['titles'] = self.title
            else:
                query_params['pageids'] = self.pageid
            request = _wiki_request(query_params)
            self._content = request['query']['pages'][self.pageid]['extract']
            self._revision_id = request['query']['pages'][self.pageid]['revisions'][0]['revid']
            self._parent_id = request['query']['pages'][self.pageid]['revisions'][0]['parentid']
        return self._content


def _wiki_request(params):
    global USER_AGENT
    params['format'] = 'json'
    params['action'] = 'query'
    return requests.get(API_URL, params=params, headers={'User-Agent': USER_AGENT}).json()


class cache(object):
    def __init__(self, fn):
        self.fn = fn
        self._cache = {}
        functools.update_wrapper(self, fn)

    def __call__(self, *args, **kwargs):
        key = str(args) + str(kwargs)
        if key in self._cache:
            ret = self._cache[key]
        else:
            ret = self._cache[key] = self.fn(*args, **kwargs)
        return ret

    def clear_cache(self):
        self._cache = {}


@cache
def search(query, results=10, suggestion=False):
    search_params = {
        'list': 'search',
        'srprop': '',
        'srlimit': results,
        'srsearch': query
    }
    if suggestion:
        search_params['srinfo'] = 'suggestion'
    raw_results = _wiki_request(search_params)
    if 'error' in raw_results:
        if raw_results['error']['info'] in ('HTTP request timed out.', 'Pool queue is full'):
            raise Exception(query)
        else:
            raise Exception(raw_results['error']['info'])
    search_results = (d['title'] for d in raw_results['query']['search'])
    if suggestion:
        if raw_results['query'].get('searchinfo'):
            return list(search_results), raw_results['query']['searchinfo']['suggestion']
        else:
            return list(search_results), None
    return list(search_results)


def page(title=None, pageid=None, auto_suggest=True, redirect=True, preload=False):
    if title is not None:
        if auto_suggest:
            results, suggestion = search(title, results=1, suggestion=True)
            try:
                title = suggestion or results[0]
            except IndexError:
                raise Exception(f"Page id \"{title}\" does not match any pages. Try another id!")
        return WikipediaPage(title, redirect=redirect, preload=preload)
    elif pageid is not None:
        return WikipediaPage(pageid=pageid, preload=preload)
    else:
        raise ValueError("Either a title or a pageid must be specified")
