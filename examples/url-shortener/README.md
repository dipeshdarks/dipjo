# Dipjo Short - URL Shortener

A fully working URL shortener built entirely with Dipjo. Demonstrates HTTP server, SQLite database, JSON APIs, and web frontend — all powered by Dipjo.

## Run

```bash
dipjo examples/url-shortener/app.dipjo
```

Optional: specify a port:

```bash
dipjo examples/url-shortener/app.dipjo 8080
```

Default port: `3000`

## Open

```
http://localhost:3000
```

## Features

- Shorten any valid URL (http:// or https://)
- Generate random 6-character short codes
- Track click counts
- View all URLs in a dashboard
- Delete URLs
- SQLite database persistence
- REST API
- Web interface

## API

### Shorten a URL

```
POST /api/shorten
Content-Type: application/json

{
  "url": "https://github.com/dipeshdarks/dipjo"
}
```

Response:

```json
{
  "success": true,
  "code": "a8Kx2Q",
  "short_url": "http://localhost:3000/a8Kx2Q",
  "original_url": "https://github.com/dipeshdarks/dipjo"
}
```

### Redirect

```
GET /:code
```

Returns HTTP 302 redirect to the original URL.

### List all URLs

```
GET /api/urls
```

### Get URL info

```
GET /api/urls/:code
```

### Delete a URL

```
DELETE /api/urls/:code
```

## Dipjo Features Used

| Feature | API |
|---------|-----|
| HTTP Server | `http_server(port)`, `server.get()`, `server.post()`, `server.delete()`, `server.start()` |
| Database | `database("urls")`, `.create()`, `.find()`, `.update()`, `.delete()` |
| JSON | `json_parse()`, `json_stringify()` |
| File I/O | `file_read()` |
| Random | `random_code()` |
| String | `string_split()`, `string_starts_with()`, `string_contains()` |
| Environment | `env("DIPJO_CWD")` |
| CLI Args | `args_get(0)` |
| HTTP Request | `request("body")`, `request("params")`, `request("method")` |

## Project Structure

```
examples/url-shortener/
├── app.dipjo          # Main application
├── public/
│   ├── index.html     # Homepage
│   ├── dashboard.html # Dashboard
│   ├── style.css      # Styles
│   └── app.js         # Frontend JavaScript
└── README.md
```

## Persistence

Data is stored in `.dipjo/data/dipjo.db` relative to the application directory. The database persists between application restarts.
