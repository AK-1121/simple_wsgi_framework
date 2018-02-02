Simple wsgi framework. Evolved from start_example.py.
Get requests, and chose suitable handlers. Register allowed HTTP methods for each handler.

In case when handler was not found call not_found_handler.
If suitable handler was found but its method is not allowed will be called not_allowed_handler.

New handlers can be added after instantiation of framework class as functions that get 2 arguments: environ object and params dict.
This function-handler must be decorated with @application.register_handler and regular expression in Python (re library) style should be passed to it as an argument.  



