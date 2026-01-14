import os
from pathlib import Path
import yaml
from datetime import datetime
from config import settings


class BlogService:
    posts_path = Path(settings.DATA_DIR) / "md"

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

    def get_meta(
        self,
        text: list[str],
    ) -> tuple[dict[str, str | int | float], list[str]] | tuple[None, None]:
        meta, meta_end = self.__parse_meta(text)

        if not self.__validate_meta(meta):
            return None, None

        return meta, text[meta_end + 1 :]

    def __validate_meta(self, meta: dict) -> bool:
        required = {
            "name": str,
            "generic_name": str,
            "publish_date": (int, float),
            "description": str,
        }

        for key, expected_type in required.items():
            if key not in meta:
                return False
            if not isinstance(meta[key], expected_type):
                return False

        return True

    def get_posts(self, time_format: str = "%B %d, %Y") -> list[dict]:
        posts = []

        for p in os.listdir(self.posts_path):
            post_path = self.posts_path / p

            with open(post_path, "r") as f:
                meta, _ = self.get_meta(f.readlines())

            if not meta:
                continue

            dt = meta.get("publish_date", 0)

            posts.append(
                {
                    "_ts": dt,
                    "publish_date": datetime.fromtimestamp(dt).strftime(time_format),  # type: ignore
                    "url": f"/b/{meta.get('generic_name')}",
                    "name": meta.get("name"),
                    "description": meta.get("description"),
                }
            )

        posts.sort(key=lambda p: p["_ts"], reverse=True)

        for p in posts:
            p.pop("_ts")

        return posts

    def get_post(self, name: str) -> tuple[dict, list[str]] | tuple[None, None]:
        name = os.path.basename(name)

        for p in os.listdir(self.posts_path):
            p = self.posts_path / p
            with open(p, "r") as f:
                meta, text = self.get_meta(f.readlines())

            if not meta or not text:
                continue

            if meta.get("generic_name") == name:
                return meta, text

        return None, None
