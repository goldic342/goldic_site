import os
import yaml
from datetime import datetime


class BlogService:

    def __parse_meta(self, text: list[str]) -> dict[str, str | int | float]:
        meta = {}
        raw_meta = ""
        found = False

        for line in text:
            line = line.strip()

            if line == "---":
                if found:
                    break
                found = True
                continue

            if found:
                raw_meta += line + "\n"

        if raw_meta:
            meta = yaml.safe_load(raw_meta)

        return meta

    def get_posts(self) -> list[dict]:
        posts_names = os.listdir("data/md")
        posts = []

        for p in posts_names:
            post_path = os.path.join("data/md", p)

            with open(post_path, "r") as f:
                text = f.readlines()

            meta = self.__parse_meta(text)

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
