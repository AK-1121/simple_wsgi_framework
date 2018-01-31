import http.client


def application(environ, start_response):
    request_uri = environ.get('REQUEST_URI')  # GET or POST
    path_info = environ.get('PATH_INFO')
    request_method = environ.get('REQUEST_METHOD')  # GET or POST
    query_string = environ.get('QUERY_STRING')  # Example: 'a=1&b=128'
    # print(environ)
    handlers = {
        '/': index_url_handler,
        '/info/': index_url_handler,
    }
    current_url_handler = handlers.get(path_info, not_found_handler)
    # if path_info == '/info/': 
    #     # response_text = b"Our contacts: ..."
    #     response_text, status_code, extra_headers = info_url_handler(environ)
    # elif path_info == '/':
    #     response_text, status_code, extra_headers = index_url_handler(environ)
    # # elif path_info == '/debug/':
    # #     response_text = str(environ).encode()
    # else:
    #     response_text, status_code, extra_headers = not_found_handler(environ)
    response_text, status_code, extra_headers = current_url_handler(environ)


    status_code_message = '%s %s ' % (
        status_code, http.client.responses[status_code]
    )
    headers = {
        'Content-Type': 'text/plain'
    }
    headers.update(extra_headers)
    # start_response('200 OK', [('Content-Type', 'text/plain')])
    start_response(status_code_message, list(headers.items()))
    return [response_text]


def index_url_handler(environ):
    return b"Index page", 200, {'X_index-test-header': '5512'}


def info_url_handler(environ):
    return b"Contacts page", 201, {'X12-test-header': '5577'}


def not_found_handler(environ):
    return b"Check your request please", 404, {'X_not_found_header': ":("}

