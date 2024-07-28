# gigsgo-api

API for gigs data

## Operation

```console
$ source .venv/bin/activate
$ uvicorn src.main:app --reload --reload-include '*.html,*.css'
```

## Development

### Tailwind

Scan template files at input file (`-i`) and build them into output file (`-o`):

```console
$ tailwindcss -i ./src/static/src/tw.css -o ./src/static/css/main.css --watch
```

- Use the `--watch` argument for a watcher that compiles on save (similar to FastAPI's --reload)
- Use the `--minify` argument when compiling to production, as it minifies the output CSS

## Tests

```console
$ source .venv/bin/activate
$ python3 -m unittest discover -s tests
```
