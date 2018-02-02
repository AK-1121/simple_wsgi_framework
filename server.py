import http.client
import json
import re


class App:
    def __init__(self):
        self.handlers = {
            # '/': self.index_url_handler,
            # '/info/': self.index_url_handler,
        }

    def get_handler(self, environ):
        # query_string = environ.get('QUERY_STRING')  # Example: 'a=1&b=128'
        path_info = environ.get('PATH_INFO')
        if not path_info.endswith('/'):
            return self.redirect_without_slash_handler, dict()

        current_method = environ.get('REQUEST_METHOD')  # GET or POST
        current_url_handler, url_params = None, None
        allowed_methods = ["GET"]
        for url_regexp, (handler, methods) in self.handlers.items():
            url_match = re.match(url_regexp, path_info)
            if not url_match:
                continue
            current_url_handler = handler
            allowed_methods = methods
            url_params = url_match.groupdict()
            break

        if not current_url_handler:
            current_url_handler = self.not_found_handler
        if current_method not in allowed_methods:
            current_url_handler = self.not_allowed_handler

        return current_url_handler, url_params

    def __call__(self, environ, start_response):
        current_url_handler, url_params = self.get_handler(environ)
        response_text, status_code, extra_headers = current_url_handler(
            environ, url_params
        )

        status_code_message = '%s %s ' % (
            status_code, http.client.responses[status_code]
        )
        headers = {
            'Content-Type': 'text/plain'
        }
        headers.update(extra_headers)

        if isinstance(response_text, (list, dict)):
            response_text = json.dumps(response_text)
            headers['Content-Type'] = 'text/json'

        start_response(status_code_message, list(headers.items()))
        return [response_text.encode('utf-8')]

    @staticmethod
    def not_found_handler(environ, url_params):
        return "Check your request please", 404, {'X_not_found_header': ":("}

    @staticmethod
    def not_allowed_handler(environ, url_params):
        return "Method not allowed ", 405, {'X_not_allowed_header': ":("}

    @staticmethod
    def redirect_without_slash_handler(environ, url_params):
        url = environ.get('PATH_INFO', '/')
        url_with_slash = url + '/'
        return "You are redirecting to correct page", 301, {"Location": url_with_slash}

    def register_handler(self, url, methods=None):
        methods = methods or ['GET']

        def inner_f(handler):
            self.handlers[url] = (handler, methods)
        return inner_f


application = App()


@application.register_handler('^\/$', methods=['GET', 'POST'])
def index_url_handler(environ, url_params):
    return "Index page", 200, {'X_index-test-header': '5512'}


@application.register_handler('^\/products\/$')
def info_url_handler(environ, url_params):
    data = [
        {"title": 'IphoneX', "price": 50000},
        {"title": 'IphoneX+', "price": 60000},
    ]
    return data, 200, {'X12-test-header': '5577'}


@application.register_handler('^\/products\/(?P<product_id>\d+)\/$')
def product_info_url_handler(environ, url_params):
    data = [
        {"title": 'IphoneX', "price": 50000, "params": url_params},
    ]
    return data, 200, {'X12-test-header': '5227'}


@application.register_handler('^\/cart\/$')
def cart_url_handler(environ, url_params):
    return 'Cart page', 200, {}


# application.register_handler('/', index_url_handler)
# application.register_handler('/info/', info_url_handler)
# application.register_handler('/cart/', cart_url_handler)

