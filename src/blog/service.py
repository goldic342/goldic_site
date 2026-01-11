import os
import yaml
from datetime import datetime


class BlogService:

    def __parse_meta(self, text: list[str]) -> tuple[dict[str, str | int | float], int]:
        meta = {}
        raw_meta = ""
        found = False
        meta_end = 0

        for i, line in enumerate(text):
            line = line.strip()

            if line == "---":
                if found:
                    try:
                        meta_end = i
                    except ValueError:
                        meta_end = 0
                    break
                found = True
                continue

            if found:
                raw_meta += line + "\n"

        if raw_meta:
            meta = yaml.safe_load(raw_meta)

        return meta, meta_end

    def __get_meta(
        self,
        path: str,
    ) -> tuple[dict[str, str | int | float], list[str]]:
        with open(path, "r") as f:
            text = f.readlines()

        meta, meta_end = self.__parse_meta(text)

        return meta, text[meta_end + 1 :]

    def get_posts(self) -> list[dict]:
        posts_names = os.listdir("data/md")
        posts = []

        for p in posts_names:
            post_path = os.path.join("data/md", p)

            meta, _ = self.__get_meta(post_path)

            name = meta.get("name")
            generic_name = meta.get("generic_name")
            dt = meta.get("datetime", 0)

            if not name or not generic_name:
                continue

            if not isinstance(dt, int):
                continue

            posts.append(
                {
                    "datetime": datetime.fromtimestamp(dt).strftime("%B %d, %Y"),
                    "url": f"/b/{generic_name}",
                    "name": name,
                }
            )

        return posts

    def get_post(self, name: str) -> tuple[dict, list[str]] | tuple[None, None]:
        name = os.path.basename(name)

        posts = os.listdir("data/md")

        for p in posts:
            p = os.path.join("data/md", p)
            meta, text = self.__get_meta(p)

            if meta.get("generic_name") == name:
                return meta, text

        return None, None
