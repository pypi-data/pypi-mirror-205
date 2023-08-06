import os
from importlib import import_module


def import_from_dir(ctx, class_suffix, module_path, path=None, case_insensitive=False):
    """
    Loads EME handlers
    :param ctx: parent app class instance
    :param class_suffix: handler class as suffix. loaded classes must have this suffix
    :param module_path: module_path from app/module handler root
    :param path: sys.path for the app/module. must be included in sys.app
    """

    # replace / to . in module_path:
    if os.sep in module_path:
        module_path = module_path.replace(os.sep, '.')
    if '/' in module_path:
        module_path = module_path.replace('/', '.')
    module_path = module_path.lstrip('.').rstrip('.')

    # list handler names:
    handler_names = [os.path.splitext(f)[0] for f in sorted(os.listdir(path)) if
                     f.endswith(class_suffix + '.py')]
    handlers = {}

    # load the modules:
    CL = -len(class_suffix) if class_suffix else None
    for module_name in handler_names:
        module = import_module(module_path + "." + module_name)

        # instantiate class
        handler_class = getattr(module, module_name)
        handler = handler_class(*ctx) if isinstance(ctx, tuple) else handler_class(ctx)

        handler_name = module_name[:CL]
        if case_insensitive:
            handler_name = handler_name.lower()

        handlers[handler_name] = handler

    return handlers


def get_dict_hierarchy(conf: dict, opts, default=None, cast=None):
    parts = opts.split('.')
    cont = conf

    try:
        for part in parts[:-1]:
            cont = cont[part]
    except Exception as e:
        return default

    last_opt = parts[-1]
    return cont.get(last_opt, default)

    # if '.' not in opts:
    #
    #     if cast is not None:
    #         return {k: cast(val) for k, val in conf[opts].items()}
    #     else:
    #
    # if main not in conf:
    #     return default
    #
    # val = conf[main].get(opt)
    #
    # if opt is None:
    #     if cast is bool:
    #         return False
    #     elif cast is float or cast is int:
    #         return 0
    #
    #     return default
    #
    # if val is None:
    #     return default
    #
    # if cast is not None:
    #     return cast(val)
    # return val
