import json
import hashlib
import os
import requests
from typing import Any, Dict

ENCODING = 'utf-8'

class APIReqestCache:
    def __init__(self, cache_dir : str) -> None:
        self.cache_dir = cache_dir

    def load_from_cache(self, url : str):
        # create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)

        # generate a hash from the url
        hash : str = hashlib.sha256(url.encode(encoding=ENCODING)).hexdigest()

        abs_file_path = os.path.abspath(os.path.join(self.cache_dir, hash))

        data = None
        if os.path.exists(abs_file_path):
            with open(abs_file_path, 'r') as file:
                data = json.load(file)

        return data
    

    def save_to_cache(self, data : dict, url : str):
        # create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)

        # generate hash from url
        hash : str = hashlib.sha256(url.encode(encoding=ENCODING)).hexdigest()

        abs_file_path = os.path.abspath(os.path.join(self.cache_dir, hash))
        
        with open(abs_file_path, 'w') as file:
            json.dump(data, file, indent=4)
    

    def make_query(self, url : str) -> Dict[Any, Any]:
        """Check cache first, make API request if necessary"""
        cached_response = self.load_from_cache(url)

        if cached_response:
            print("Cache hit! - returning cached response...")
            return cached_response, None

        try: 
            print("Cache miss! - querying API...")
            res = requests.get(url)
            res.raise_for_status()

        except Exception as exc:
            err = f"{__name__}() - {exc}"
            return None, err
        
        res_json = res.json()
        self.save_to_cache(res_json, url)

        return res_json, None

