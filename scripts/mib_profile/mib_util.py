import functools
import json
import pathlib

from scripts.mib_profile import config, entity


@functools.cache
def _load_mib_cache_abs(path: pathlib.Path) -> dict:
    """キャッシュしたファイルローダ

    Parameters
    ----------
    path : pathlib.Path
        _description_

    Returns
    -------
    dict
    """
    return json.load(path.open())


def load_mib_cache(path: pathlib.Path) -> dict:
    """キャッシュしたファイルローダ絶対パスにして

    Parameters
    ----------
    path : pathlib.Path
        _description_

    Returns
    -------
    dict
    """
    return _load_mib_cache_abs(path.absolute())


def load_mib(mib_name: str) -> dict:
    """src dirにある{mib_name}.jsonの中身を取り出す

    Parameters
    ----------
    mib_name : str
        mib name
    field : str | None, optional
        mib の

    Returns
    -------
    dict
    """
    return load_mib_cache((config.SRC_DIR / f"{mib_name}.json"))


def find_mib_symbol(mib_object_identifier: str, **kwargs) -> entity.Symbol:
    """yamahaのobjectを探してくる

    Parameters
    ----------
    mib_object_identifier : str
        mib object識別子
    kwargs
        entity.Symbolに渡される

    Returns
    -------
    entity.Symbol
        識別子

    Raises
    ------
    KeyError
        見つからない場合
    """
    for f in config.SRC_DIR.glob("*.json"):
        mib = load_mib_cache(f)
        if mib_object_identifier in mib:
            kwargs["OID"] = mib[mib_object_identifier]["oid"]
            kwargs["name"] = kwargs.get("name", mib_object_identifier)
            return entity.Symbol(**kwargs)

    raise KeyError(mib_object_identifier)
