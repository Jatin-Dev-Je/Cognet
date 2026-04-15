"""Cognet CLI for power users and demos."""

from __future__ import annotations

import json
from urllib import request as urllib_request


BASE_URL = "http://localhost:8000"


def main() -> None:
    """Run an interactive Cognet CLI session."""

    print("Cognet CLI")
    while True:
        message = input(">> ").strip()
        if message.lower() in {"exit", "quit"}:
            break

        payload_bytes = json.dumps({"message": message, "user_id": "cli-user"}).encode("utf-8")
        api_request = urllib_request.Request(
            f"{BASE_URL}/api/v1/chat",
            data=payload_bytes,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib_request.urlopen(api_request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        print(payload.get("response", ""))


if __name__ == "__main__":
    main()
