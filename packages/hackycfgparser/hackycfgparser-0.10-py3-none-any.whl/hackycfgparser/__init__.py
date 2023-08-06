import ast
import importlib
from collections import defaultdict
from functools import reduce
from configparser import ConfigParser
import re
from typing import Iterable
from flatten_any_dict_iterable_or_whatsoever import fla_tu, set_in_original_iter
from tolerant_isinstance import isinstance_tolerant
from deepcopyall import deepcopy
import os
import sys
from ast import literal_eval
from functools import wraps
from itertools import tee

nested_dict = lambda: defaultdict(nested_dict)
config = sys.modules[__name__]
config.parsedargs = {}
config.helptext = ""
config.stop_after_kill = True


def load_config_file_vars(cfgfile: str, onezeroasboolean: bool = False) -> None:
    """
    Loads the variables in the specified configuration file and sets them as global variables.

    Args:
    - cfgfile (str): The path of the configuration file to load.
    - onezeroasboolean (bool): Indicates whether the string "0" or "1" should be converted to boolean False or True,
        respectively (default False).

    Returns:
    - None
    """
    f = sys._getframe(1)
    dct = f.f_globals

    pars2 = ConfigParser()
    pars2.read(cfgfile)

    (
        cfgdictcopy,
        cfgdictcopyaslist,
    ) = copy_dict_and_convert_values(pars2, onezeroasboolean=onezeroasboolean)
    if "sys" not in dct:
        dct["sys"] = importlib.import_module("sys")
    for key, item in cfgdictcopyaslist:
        dct["sys"].argv.extend([f"--{item[-1]}", repr(key)])
    config.allsysargs = [
        ini for ini, x in enumerate(dct["sys"].argv) if x.startswith("-")
    ]

    parse_ar()


def convert_to_normal_dict(di: dict) -> dict:
    """
    Recursively converts the input dictionary to a normal dictionary (i.e., non-defaultdict) by copying its contents.

    Args:
    - di (dict): The input defaultdict or dictionary to convert.

    Returns:
    - A new dictionary that is a copy of the input dictionary, with all nested defaultdicts replaced with dictionaries.
    """
    if isinstance_tolerant(di, defaultdict):
        di = {k: convert_to_normal_dict(v) for k, v in di.items()}
    return di


def groupBy(
    key: Iterable,
    seq: Iterable,
    continue_on_exceptions: bool = True,
    withindex: bool = True,
    withvalue: bool = True,
) -> dict:
    """
    Groups the elements of the input iterable `seq` based on a grouping function `key`.

    Args:
    - key (Iterable): A function that takes a single argument and returns a hashable object that is used to group
        the elements of the input iterable.
    - seq (Iterable): The input iterable to group.
    - continue_on_exceptions (bool): Indicates whether to continue grouping even if a TypeError occurs when applying the
        grouping function to an element (default True).
    - withindex (bool): Indicates whether to include the index of each element in the groups (default True).
    - withvalue (bool): Indicates whether to include the value of each element in the groups (default True).

    Returns:
    - A dictionary where each key is a group, and the corresponding value is a list of the elements that belong to the group.
    """
    indexcounter = -1

    def execute_f(k, v):
        nonlocal indexcounter
        indexcounter += 1
        try:
            return k(v)
        except Exception as fa:
            if continue_on_exceptions:
                return "EXCEPTION: " + str(fa)
            else:
                raise fa

    # based on https://stackoverflow.com/a/60282640/15096247
    if withvalue:
        return convert_to_normal_dict(
            reduce(
                lambda grp, val: grp[execute_f(key, val)].append(
                    val if not withindex else (indexcounter, val)
                )
                or grp,
                seq,
                defaultdict(list),
            )
        )
    return convert_to_normal_dict(
        reduce(
            lambda grp, val: grp[execute_f(key, val)].append(indexcounter) or grp,
            seq,
            defaultdict(list),
        )
    )


def groupby_first_item(
    seq: Iterable,
    continue_on_exceptions: bool = True,
    withindex: bool = True,
    withvalue: bool = True,
) -> dict:
    """
    Groups the elements of the input iterable `seq` based on their first item.

    Args:
    - seq (Iterable): The input iterable to group.
    - continue_on_exceptions (bool): Indicates whether to continue grouping even if a TypeError occurs when applying the
        grouping function to an element (default True).
    - withindex (bool): Indicates whether to include the index of each element in the groups (default True).
    - withvalue (bool): Indicates whether to include the value of each element in the groups (default True).

    Returns:
    - A dictionary where each key is a group, and the corresponding value is a list of the elements that belong to the group.
    """
    return groupBy(
        key=lambda x: x[0],
        seq=seq,
        continue_on_exceptions=continue_on_exceptions,
        withindex=withindex,
        withvalue=withvalue,
    )


def copy_dict_and_convert_values(pars: ConfigParser, onezeroasboolean: bool = False):
    r"""
    Copy a ConfigParser object's sections and convert their values to the desired data types.
    Args:
    - pars: a ConfigParser object to be copied and whose values will be converted
    - onezeroasboolean: a boolean flag indicating whether to convert "0" and "1" to boolean values. (Default False)

    Returns:
    A tuple with the following elements:
    - copieddict: a dictionary containing the copied sections and their converted values
    - g: a flattened list of copieddict's keys and values

    """
    copieddict = deepcopy(pars.__dict__["_sections"])
    flattli = fla_tu(pars.__dict__["_sections"])
    for value, keys in flattli:
        if not re.search(r"^(?:[01])$", str(value)):
            try:
                valuewithdtype = pars.getboolean(*keys)
            except Exception:
                try:
                    valuewithdtype = ast.literal_eval(pars.get(*keys))
                except Exception:
                    valuewithdtype = pars.get(*keys)
        else:
            if onezeroasboolean:
                valuewithdtype = pars.getboolean(*keys)
            else:
                valuewithdtype = ast.literal_eval(pars.get(*keys))

        set_in_original_iter(iterable=copieddict, keys=keys, value=valuewithdtype)

    g = list(fla_tu(copieddict))
    return (copieddict, g)


def pairwise(iterable: Iterable) -> tuple:
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def iter_split_by_index(iterable, indexes):
    return (iterable[p[0] : p[1]] for p in pairwise([0] + indexes + [len(iterable)]))


def show_and_exit() -> None:
    print(config.helptext)
    if config.stop_after_kill:
        input()
    try:
        sys.exit(1)
    finally:
        os._exit(1)


def parse_ar() -> None:
    ges = list(iter_split_by_index(iterable=sys.argv, indexes=config.allsysargs))
    checkset = ("-?", "?", "-h", "--h", "help", "-help", "--help")
    for ini, g in enumerate(ges[1:]):
        try:
            there = g[0] in checkset
            if there:
                raise ValueError
            config.parsedargs[g[0].lstrip("- ")] = g[1]
        except Exception:
            show_and_exit()


def kill_when_not_there(necessary_keys: list | tuple) -> None:
    for key in necessary_keys:
        if key.strip("- ") not in config.parsedargs:
            show_and_exit()


def add_config(f_py=None):
    assert callable(f_py) or f_py is None
    f = sys._getframe(1)
    dct = f.f_globals

    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            varnames = dct[func.__name__].__dict__["__wrapped__"].__code__.co_varnames
            allanot = [
                x
                for x in dct[func.__name__]
                .__dict__["__wrapped__"]
                .__annotations__.items()
            ]
            newargs = []
            allanotdict = dict(allanot)
            for a, b in zip(
                varnames, dct[func.__name__].__dict__["__wrapped__"].__defaults__
            ):
                try:
                    dtypegood = False
                    conva = b

                    try:
                        conva = literal_eval(config.parsedargs[a])
                        if type(conva) in allanotdict[a].__args__:
                            dtypegood = True
                        else:
                            conva = literal_eval(conva)
                            if type(conva) in allanotdict[a].__args__:
                                dtypegood = True
                    except Exception:
                        pass

                    if not dtypegood:
                        try:
                            for dty in allanotdict[a].__args__:
                                try:
                                    conva = dty(config.parsedargs[a])
                                    break
                                except Exception as fe:
                                    continue
                        except Exception as fa:
                            conva = allanotdict[a](config.parsedargs[a])
                    newargs.append(conva)
                except Exception as adf:
                    newargs.append(b)
                    continue

            setattr(
                dct[func.__name__].__dict__["__wrapped__"],
                "__defaults__",
                tuple(newargs),
            )
            return func(*args, **kwargs)

        return wrapper

    return _decorator(f_py) if callable(f_py) else _decorator
