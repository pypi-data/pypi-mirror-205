from icecream import colorizedStderrPrint, ic
from loguru import logger
from aioconsole import aprint
from pprint import pformat
from inspect import getmodule, stack
from pathlib import Path
from time import time


def get_mod():
    mod_logger = stack()[3][0]
    mod = getmodule(mod_logger)
    mod.name = Path(mod.__file__).stem
    return mod


def log_debug(s):
    mod = get_mod()
    if debug[mod.name]:
        if ac.deployed or debug.production:
            return logger.patch(lambda record: record.update(name=mod.__name__)).debug(
                s
            )
        return colorizedStderrPrint(s)


ic.configureOutput(prefix="    debug:  ", includeContext=True, outputFunction=log_debug)
if ac.deployed or debug.production:
    ic.configureOutput(prefix="", includeContext=False, outputFunction=log_debug)


async def apformat(obj, sort_dicts: bool = False) -> None:  # make purple
    mod = get_mod()
    if not ac.deployed and not debug.production and debug[mod.name]:
        await aprint(pformat(obj, sort_dicts=sort_dicts))


def timeit(func):
    def wrapped(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        logger.debug(f"Function '{func.__name__}' executed in {end - start} s")
        return result

    return wrapped


# from inspect import getargvalues
# from inspect import getmodule
# from inspect import getouterframes
# from inspect import stack
# from pathlib import AsyncPath
#
# from pydantic import BaseModel
#
#
# class InspectStack(BaseModel):
#     @staticmethod
#     def calling_function():
#         frm = stack()[2]
#         return AsyncPath(getmodule(frm[0]).__file__).stem
#
#     @staticmethod
#     def calling_page(calling_frame):
#         calling_stack = getouterframes(calling_frame)
#         page = ""
#         for f in calling_stack:
#             if f[3] == "render_template_string":
#                 page = getargvalues(f[0]).locals["context"]["page"]
#         return page
#
#
# inspect_ = InspectStack()
