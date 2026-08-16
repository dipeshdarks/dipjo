"""
Dipjo HTTP Server - Provides HTTP server capabilities for Dipjo programs.
Uses Python's built-in http.server with threading for request handling.
"""

import os
import json
import threading
import re
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class DipjoHTTPServer:
    """HTTP server that routes requests to Dipjo callback functions."""

    def __init__(self, port=3000):
        self.port = port
        self.routes = []  # list of (method, pattern, callback_name)
        self._interpreter = None
        self._server = None
        self._lock = threading.Lock()
        self.static_dir = None

    def set_interpreter(self, interpreter):
        self._interpreter = interpreter

    def get(self, path, callback_name):
        self.routes.append(("GET", path, callback_name))

    def post(self, path, callback_name):
        self.routes.append(("POST", path, callback_name))

    def delete(self, path, callback_name):
        self.routes.append(("DELETE", path, callback_name))

    def set_static(self, directory):
        self.static_dir = directory

    def _match_route(self, method, path):
        for route_method, pattern, callback in self.routes:
            if route_method != method:
                continue
            param_names = []
            regex_parts = []
            for part in pattern.split("/"):
                if part.startswith(":"):
                    param_names.append(part[1:])
                    regex_parts.append(r"([^/]+)")
                elif part:
                    regex_parts.append(re.escape(part))
            regex = "^/" + "/".join(regex_parts) + "$"
            match = re.match(regex, path)
            if match:
                params = dict(zip(param_names, match.groups()))
                return callback, params
        return None, {}

    def start(self):
        server_ref = self

        class RequestHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass  # suppress default logging

            def do_GET(self):
                server_ref._handle_request("GET", self)

            def do_POST(self):
                server_ref._handle_request("POST", self)

            def do_DELETE(self):
                server_ref._handle_request("DELETE", self)

        self._server = HTTPServer(("0.0.0.0", self.port), RequestHandler)
        print(f"Dipjo Short - Server running at http://localhost:{self.port}")
        self._server.serve_forever()

    def _handle_request(self, method, handler):
        parsed = urlparse(handler.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # Read body for POST/DELETE
        content_length = int(handler.headers.get("Content-Length", 0))
        body = handler.requestline
        raw_body = ""
        if content_length > 0:
            raw_body = handler.rfile.read(content_length).decode("utf-8")

        callback_name, params = self._match_route(method, path)

        if callback_name is None:
            search_match = re.match(r"^/search/([a-zA-Z0-9_-]+)$", path)
            if search_match and method == "GET":
                self._handle_search(search_match.group(1), query, handler)
                return
            if self.static_dir and method == "GET":
                if self._serve_static(handler, path):
                    return
            self._send_json(handler, 404, {"error": "Not found"})
            return

        # Build request object for Dipjo
        request = {
            "method": method,
            "path": path,
            "query": query,
            "params": params,
            "headers": dict(handler.headers),
            "body": raw_body,
        }

        try:
            with self._lock:
                self._interpreter.set_http_request(request)
                result = self._interpreter.call_function(callback_name, [])

            if result is None:
                self._send_json(handler, 500, {"error": "Handler returned None"})
                return

            if isinstance(result, dict):
                status = result.get("status", 200)
                body_data = result.get("body", result)
                headers = result.get("headers", {})
                content_type = result.get("content_type", "application/json")

                if isinstance(body_data, str) and content_type == "text/html":
                    self._send_html(handler, status, body_data, headers)
                elif isinstance(body_data, str):
                    self._send_text(handler, status, body_data, headers)
                else:
                    self._send_json(handler, status, body_data, headers)
            else:
                self._send_json(handler, 200, result)

        except Exception as e:
            self._send_json(handler, 500, {"error": str(e)})

    def _handle_search(self, index_name, query_params, handler):
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        try:
            from search import SearchIndex
            q = query_params.get("q", [""])[0]
            limit = int(query_params.get("limit", ["20"])[0])
            offset = int(query_params.get("offset", ["0"])[0])
            if not q:
                self._send_json(handler, 400, {"error": "Missing 'q' parameter"})
                return
            start = time.time()
            index = SearchIndex(index_name)
            results = index.search(q, {"limit": limit, "offset": offset})
            index.close()
            elapsed_ms = round((time.time() - start) * 1000, 2)
            results["time_ms"] = elapsed_ms
            self._send_json(handler, 200, results)
        except Exception as e:
            self._send_json(handler, 500, {"error": str(e)})

    def _serve_static(self, handler, path):
        if path == "/":
            path = "/index.html"
        filepath = os.path.join(self.static_dir, path.lstrip("/"))
        if not os.path.isfile(filepath):
            return False
        ext = os.path.splitext(filepath)[1].lower()
        content_types = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".json": "application/json",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".ico": "image/x-icon",
        }
        content_type = content_types.get(ext, "text/plain")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            handler.send_response(200)
            handler.send_header("Content-Type", content_type)
            handler.send_header("Content-Length", str(len(content.encode())))
            handler.end_headers()
            handler.wfile.write(content.encode())
            return True
        except Exception:
            return False

    def _send_json(self, handler, status, data, extra_headers=None):
        body = json.dumps(data, default=str)
        handler.send_response(status)
        handler.send_header("Content-Type", "application/json")
        handler.send_header("Content-Length", str(len(body.encode())))
        if extra_headers:
            for k, v in extra_headers.items():
                handler.send_header(k, v)
        handler.end_headers()
        handler.wfile.write(body.encode())

    def _send_html(self, handler, status, data, extra_headers=None):
        handler.send_response(status)
        handler.send_header("Content-Type", "text/html")
        handler.send_header("Content-Length", str(len(data.encode())))
        if extra_headers:
            for k, v in extra_headers.items():
                handler.send_header(k, v)
        handler.end_headers()
        handler.wfile.write(data.encode())

    def _send_text(self, handler, status, data, extra_headers=None):
        handler.send_response(status)
        handler.send_header("Content-Type", "text/plain")
        handler.send_header("Content-Length", str(len(data.encode())))
        if extra_headers:
            for k, v in extra_headers.items():
                handler.send_header(k, v)
        handler.end_headers()
        handler.wfile.write(data.encode())

    def redirect(self, handler, url, status=302):
        handler.send_response(status)
        handler.send_header("Location", url)
        handler.send_header("Content-Length", "0")
        handler.end_headers()
