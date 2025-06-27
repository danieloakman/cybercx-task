# Cyber CX Take Home Task

## Setup & Install

- Requires Python v3.12
- Create a venv with whatever method you want
  - If using nix, there is a nix shell file provided, run `nix-shell` and this will install the required python version and and put you in a venv.
- Run `make install-dev`
- Run `make dev` for the server to reload on code changes. Or run `make start`

## Example requests

### POST /submit - Submit new entries

Submit an IP address:

```bash
curl -X POST "http://localhost:8000/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "value": "192.168.1.1",
    "tags": ["internal", "router"]
  }'
```

Submit a domain:

```bash
curl -X POST "http://localhost:8000/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "value": "example.com",
    "tags": ["malicious", "phishing"]
  }'
```

Submit a hash (MD5/SHA1/SHA256):

```bash
curl -X POST "http://localhost:8000/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "value": "d41d8cd98f00b204e9800998ecf8427e",
    "tags": ["malware", "trojan"]
  }'
```

Submit without tags:

```bash
curl -X POST "http://localhost:8000/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "value": "10.0.0.1"
  }'
```

### GET /data - Search entries

Search for an IP address:

```bash
curl -X GET "http://localhost:8000/data?q=192.168.1.1&limit=10"
```

Search for a domain with tags filter:

```bash
curl -X GET "http://localhost:8000/data?q=example.com&tags=malicious&tags=phishing&limit=5"
```

Search for a hash:

```bash
curl -X GET "http://localhost:8000/data?q=d41d8cd98f00b204e9800998ecf8427e&limit=20"
```

Check if the server is running:

```bash
curl -X GET "http://localhost:8000/health"
```

### Docs page

See [Docs page](http://localhost:8000/docs)

## Notes on my design

- [storage.py](./storage.py) - exposes functions to read and write to the in memory storage, which is just a dict. The keys for the dict are hashes of `StorageEntry`, see validation.py.

- [validatio.py](./validation.py) - I've put the route validation and `StorageEntry` class in here. I tossed up whether to use fastAPI's `Depend` to make use of the Value and Tags Validation which is shared but ultimtely just went with refactoring the validation functions out and using them in each pydantic model.

- [main.py](./main.py) - I added a validation handler so there's neat error messages when you get a 422 response.
 