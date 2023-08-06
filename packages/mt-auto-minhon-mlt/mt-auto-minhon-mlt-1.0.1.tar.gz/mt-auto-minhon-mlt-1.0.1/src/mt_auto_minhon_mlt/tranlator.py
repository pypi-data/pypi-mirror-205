from __future__ import annotations

import json
import urllib
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request


def load_support_translate() -> list[tuple[str, str, str]]:
    path = Path(__file__).parent / "assets/support_translate.json"
    with open(path, encoding="utf-8") as f:
        support_languages = json.load(f)
    return [tuple(support_language) for support_language in support_languages]


def request(url: str, data: dict[str, str]) -> dict:
    request_object = Request(url, urlencode(data).encode("ascii"), method="POST")

    with urllib.request.urlopen(request_object) as response:
        response_body = response.read().decode("utf-8")
        return json.loads(response_body)


class Translator:
    __DOMAIN = "https://mt-auto-minhon-mlt.ucri.jgn-x.jp"
    __SUPPORT_TRANSLATE = load_support_translate()

    def __init__(self, client_id: str, client_secret: str, user_name: str):
        self.__client_id = client_id
        self.__user_name = user_name
        self.__access_token = self.__get_access_token(
            client_id=client_id,
            client_secret=client_secret,
        )

    def translate_text(self, text: str, source_lang: str, target_lang: str, translate_type: str = "generalNT") -> str:
        self.__check(text, translate_type, source_lang, target_lang)

        request_data = dict(
            key=self.__client_id,
            name=self.__user_name,
            type="json",
            access_token=self.__access_token,
            text=text,
        )
        url = f"{self.__DOMAIN}/api/mt/{translate_type}_{source_lang}_{target_lang}/"
        response = request(url, data=request_data)
        return response["resultset"]["result"]["text"]

    def __check(self, text: str, translate_type: str, source_lang: str, target_lang: str):
        if not self.__is_support_translate(translate_type, source_lang, target_lang):
            raise ValueError(
                f"doesn't support. translate_type: {translate_type}, source_lang: {source_lang}"
                f", target_lang: {target_lang}"
            )
        if text is None or text == "":
            raise ValueError("doesn't exist text")

    @classmethod
    def __is_support_translate(cls, translate_type: str, src_lang: str, target_lang: str):
        return (translate_type, src_lang, target_lang) in cls.__SUPPORT_TRANSLATE

    @classmethod
    def __get_access_token(cls, client_id: str, client_secret: str) -> str:
        url = f"{cls.__DOMAIN}/oauth2/token.php"
        client_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        response = request(url, data=client_data)
        return response["access_token"]
