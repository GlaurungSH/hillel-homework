class Url:
    def __init__(self, scheme='', authority='', path='', query='', fragment=''):
        self.scheme = scheme
        self.authority = authority
        self.path = '/' + '/'.join(path) if isinstance(path, list) else path
        self.query = Url.f_query(query)
        self.fragment = fragment

    def __str__(self) -> str:
        return f'{self.scheme}://{self.authority}{self.path}{self.query}{self.fragment}'

    def __eq__(self, other) -> bool:
        if str(self) == str(other):
            return True
        else:
            return False

    @staticmethod
    def f_query(query):
        if isinstance(query, dict):
            result = ''
            for k, i in query.items():
                result += f'?{k}={i}' if k == 'q' else f'&{k}={i}'
            return result
        else:
            return query


class HttpsUrl(Url):

    def __init__(self, scheme='https', authority='', path='', query='', fragment=''):
        super().__init__(scheme, authority, path, query, fragment)


class HttpUrl(Url):

    def __init__(self, scheme='http', authority='', path='', query='', fragment=''):
        super().__init__(scheme, authority, path, query, fragment)


class GoogleUrl(HttpsUrl):

    def __init__(self, scheme='https', authority='google.com', path='', query='', fragment=''):
        super().__init__(scheme, authority, path, query, fragment)


class WikiUrl(HttpsUrl):

    def __init__(self, scheme='https', authority='wikipedia.org', path='', query='', fragment=''):
        super().__init__(scheme, authority, path, query, fragment)


class UrlCreator(Url):

    def __init__(self, scheme='', authority=''):
        super().__init__(scheme, authority)

    def __getattr__(self, item):
        self.path += f'/{item}'
        return self

    def __call__(self, *args, **kwargs):
        if len(args) > 0:
            self.path = ''
            self.path += f'/{"/".join(args)}'
        if len(kwargs) > 0:
            self.query = ''
            for k, i in kwargs.items():
                self.query += f'?{k}={i}' if k == 'q' else f'&{k}={i}'
        return self

    def _create(self):
        return self.__str__()


assert GoogleUrl() == HttpsUrl(authority='google.com')
assert GoogleUrl() == Url(scheme='https', authority='google.com')
assert GoogleUrl() == 'https://google.com'
assert WikiUrl() == str(Url(scheme='https', authority='wikipedia.org'))
assert WikiUrl(path=['wiki', 'python']) == 'https://wikipedia.org/wiki/python'
assert GoogleUrl(query={'q': 'python', 'result': 'json'}) == 'https://google.com?q=python&result=json'

url_creator = UrlCreator(scheme='https', authority='docs.python.org')
assert url_creator.docs.v1.api.list == 'https://docs.python.org/docs/v1/api/list'
assert url_creator('api', 'v1', 'list') == 'https://docs.python.org/api/v1/list'
assert url_creator('api', 'v1', 'list', q='my_list') == 'https://docs.python.org/api/v1/list?q=my_list'
assert url_creator('3').search(q='getattr', check_keywords='yes', area='default')._create() == \
       'https://docs.python.org/3/search?q=getattr&check_keywords=yes&area=default'
