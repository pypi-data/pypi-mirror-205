import functools
import json
import sys
from itertools import product

import tabulate

from flask import Flask

from .flask_jerry import flask_apps, FlaskAppJerrySetup


def flask_jerry_setup(app: Flask, cfg: str | dict | None = None, path: str = None):
    # load toml config
    # setup (or leave alone -- keep default)
    # debug, host, port

    if isinstance(cfg, str):
        with open(cfg) as fh:
            cfg = json.load(fh)
    elif cfg is None:
        # use defaults?
        cfg = {}

    if path:
        sys.path.append(path)

    flask_apps[app.name] = FlaskAppJerrySetup(app, cfg, path)


def flask_jerry(cfg_file: str | dict = None):
    def actual_decorator(flask_app_cls: Flask):
        @functools.wraps(flask_app_cls)
        def wrapper(*args, **kwargs):
            app = flask_app_cls(*args, **kwargs)
            flask_jerry_setup(app, cfg_file)
            return app

        return wrapper
    return actual_decorator


def print_endpoints(app: Flask):
    setup = flask_apps[app.name]
    table = []
    reverse_endpoints = {}

    # set tomcru-jerry set custom endpoints
    for _endpoint, _urls in setup.custom_routes.items():
        for _url in _urls:
            sp = _url.split(' ')
            if len(sp) == 2:
                _url = _url.removeprefix(sp[0]+' ')
            reverse_endpoints.setdefault(_url, []).append(_endpoint)

    for rule in app.url_map.iter_rules():
        methods = rule.methods.copy()
        methods.discard('OPTIONS')
        methods.discard('HEAD')

        url = f'{setup.module_route}{rule.rule}'
        endpoints = reverse_endpoints.get(url)

        if not endpoints:
            # (flask) list endpoints as function names
            endpoints = [rule.endpoint]

        for endpoint, method in product(endpoints, methods):
            table.append([method, url, endpoint])

    print(tabulate.tabulate(table, headers=('OPT', 'URL', 'ENDPOINT_ID')))


__all__ = ['flask_jerry', 'flask_jerry_setup']
