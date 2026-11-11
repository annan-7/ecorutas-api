"""Check actual image responses; run manually, never during application startup."""

import hashlib
import json
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    rows = json.loads((root / "src/data/routes.json").read_text())
    hashes: set[str] = set()
    for row in rows:
        request = Request(
            row["image_url"], headers={"User-Agent": "EcorutasImages/1.0"}
        )
        for attempt in range(3):
            try:
                with urlopen(request, timeout=45) as response:
                    if (
                        response.status != 200
                        or not response.headers.get_content_type().startswith("image/")
                    ):
                        raise ValueError(f"Not an image: {row['name']}")
                    content = response.read(10_000_001)
                break
            except HTTPError as exc:
                if exc.code != 429 or attempt == 2:
                    raise
                time.sleep(int(exc.headers.get("Retry-After", "30")) + 1)
        else:
            raise RuntimeError("Image request retries exhausted")
        if not 1000 < len(content) <= 10_000_000:
            raise ValueError(f"Unexpected image size: {row['name']}")
        if not content.startswith((b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n", b"RIFF")):
            raise ValueError(f"Unexpected image bytes: {row['name']}")
        digest = hashlib.sha256(content).hexdigest()
        if digest in hashes:
            raise ValueError(f"Duplicate image content: {row['name']}")
        hashes.add(digest)
        print(f"OK {row['name']}", flush=True)
    print(f"Verified {len(hashes)} distinct images")


if __name__ == "__main__":
    main()
