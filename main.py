import json
import logging
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


APP_NAME = os.getenv("APP_NAME", "sample-python-app")
APP_VERSION = os.getenv("APP_VERSION", "dev")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8080"))


def build_response() -> bytes:
    payload = {
        "app": APP_NAME,
        "version": APP_VERSION,
        "status": "ok",
    }
    return json.dumps(payload).encode("utf-8")


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path not in {"/", "/healthz", "/readyz"}:
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
            return

        body = build_response()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        logging.info("%s - %s", self.address_string(), format % args)


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(message)s",
    )
    server = ThreadingHTTPServer((HOST, PORT), AppHandler)
    logging.info("Starting %s version %s on %s:%s", APP_NAME, APP_VERSION, HOST, PORT)
    server.serve_forever()


if __name__ == "__main__":
    main()
