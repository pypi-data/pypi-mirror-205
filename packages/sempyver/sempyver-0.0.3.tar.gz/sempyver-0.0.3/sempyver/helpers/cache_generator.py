"""
Generate cache for the sempyver module
"""
import json
from typing import Dict, List, Union, Any
from pathlib import Path


def create_cache(files: Union[List[str], None]) -> None:
    """Create the cache folder for the sempyver folder

    Args:
        files (List[str]): Files to be added in the cache folder.
    """
    # First, check if the cache folder exists
    cache_dir = Path(str(Path().absolute()) + "/.sempyver_cache")
    if cache_dir.exists():
        # Now, save once again the files in the cache
        _last_files = open_cache_file(cache_dir, open_mode="r")
        if _last_files is None:
            raise ValueError(
                "We're unable to create the last files for the cache file.")
        if files is None:
            # If there's no files to add, then empty the cache list
            _last_files["files"] = []
        else:
            # Check which files are not in the cache
            for file in files:
                if file not in _last_files["files"]:
                    _last_files["files"].append(file)
        # Now, save once again the files in the cache
        last_files = open_cache_file(cache_dir)
        if last_files is not None:
            with Path(str(cache_dir) +
                      "/v/cache/changesets.json").open("w", encoding="utf-8") as _cache:
                json.dump(_last_files, _cache)
        else:
            raise ValueError(
                "We're unable to create the last files for the cache file.")
        return

    # If not exists, then create it
    cache_dir.mkdir(parents=True, exist_ok=True)
    # Then, from there, create the .gitignore
    with open(Path(str(cache_dir) + "/.gitignore"), "w", encoding="utf-8") as gitignore:
        gitignore.write("# Created by sempyver automatically.\n*\n")
    # Create the CACHEDIR.TAG
    with open(cache_dir / "CACHEDIR.TAG",  "w", encoding="utf-8") as cache_tag:
        cache_tag.write("Signature: 8a477f597d28d172789f06886806bc55\n")
        cache_tag.write(
            "# This file is a cache directory tag created by sempyver.\n")
        cache_tag.write("# For information about cache directory tags, see:\n")
        cache_tag.write("#	https://bford.info/cachedir/spec.html)\n")
    # And, after that, create the v/cache file
    # Path(str(cache_dir) + "v").mkdir(parents=True, exist_ok=True)
    Path(str(cache_dir) + "/v/cache").mkdir(parents=True, exist_ok=True)
    with Path(str(cache_dir) + "/v/cache/changesets.json").open("w", encoding="utf-8") as _cache:
        json.dump({"files": files}, _cache)


def open_cache_file(cache_dir: Path, open_mode: str = "r") -> Union[Dict[str, Any], None]:
    """Open the cache file for the changesets

    Args:
        cache_dir (Path): Directory to search for the changesets
        open_mode (str, optional): How to open the file. Defaults to "r".

    Returns:
        TextIOWrapper: Cache file open
    """
    path_to_open: Path = Path(str(cache_dir) + "/v/cache/changesets.json")
    if path_to_open.exists() is True:
        return json.loads(path_to_open.open(open_mode, encoding="utf-8").read())
    return None
