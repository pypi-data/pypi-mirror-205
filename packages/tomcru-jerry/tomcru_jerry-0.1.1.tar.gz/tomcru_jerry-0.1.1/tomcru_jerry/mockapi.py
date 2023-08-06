import re
import uuid

from flask import request, jsonify, Flask

from tomcru_jerry.controllers import preset_endpoint
from tomcru_jerry.utils import get_dict_hierarchy


class MockedController:
    def __init__(self, app: Flask, responses):
        self.app = app
        self.resp_tpls = {}
        flask_endpoint = 'Mocked:custom_endpoint'

        for url, response in responses.items():
            ep_id = response.get('endpoint_id', str(uuid.uuid4()))

            preset_endpoint(app, url, f'{app.name}.{flask_endpoint}' if app.name else flask_endpoint)
            self.resp_tpls[ep_id] = response

            # method, route = endpoint.split(' ') if ' ' in endpoint else ['GET', endpoint]
            # methods = method.split(',')
            #
            # setup.mockedapi.
            # app.add_url_rule(route, ep_id, setup.mockedapi.custom_endpoint, methods=methods)

    def custom_endpoint(self):
        ep_id = request.endpoint
        resp_tpl = self.resp_tpls[ep_id]

        req = {
            'headers': {k.lower():v for k,v in request.headers.items()},
            'params': dict(request.args),
        }

        if request.method != 'GET':
            req['body'] = request.get_json()

        resp2, status = transform_response(resp_tpl, req)

        r = jsonify(resp2['body'])
        if 'headers' in resp2:
            r.headers.update(resp2['headers'])
        r.status = status

        return r


def transform_response(resp_tpl: dict, req: dict):
    resp = resp_tpl.copy()
    status = 200

    if 'body' not in resp:
        resp = {
            'body': resp,
        }
    if 'headers' not in resp:
        resp['headers'] = {'Content-Type': 'application/json'}

    p = re.compile(r'\{([^}]*)}')

    for container in ['body', 'headers']:
        for key, transform in resp_tpl[container].items():
            if isinstance(transform, str):
                # subtitute request -> response transformations
                groups = p.findall(transform)

                if groups:
                    res = transform

                    for group in groups:
                        to_find = str(group)
                        if 'headers' == to_find.split('.')[0]:
                            to_find = to_find.lower()

                        if 'access_token' == to_find:
                            try:
                                _bearer, token = req['headers']['authorization'].split(' ')

                                assert _bearer.lower() == 'bearer'
                                if not token:
                                    raise Exception("")
                            except:
                                return {"body": {}}, 403

                            substitute = token
                        elif 'url' == to_find:
                            substitute = str(request.url_root)
                        else:
                            substitute = get_dict_hierarchy(req, to_find)
                            #substitute = req.get(to_find)

                        if f'{{{group}}}' == transform:
                            # replace as-is (keeps type)
                            if substitute is not None:
                                res = substitute
                                break
                        else:
                            # string template replace
                            if substitute is not None:
                                res = res.replace(f'{{{group}}}', str(substitute))

                    if res is not None:
                        resp[container][key] = res

    return resp, status
