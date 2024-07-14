# gigshk-pipeline

ETL pipeline for gigshk data

## Operation

### Scraper

```console
$ source .venv/bin/activate
$ python3 -m src.main -v 'https://www.example.com'
```

### App

```console
$ source .venv/bin/activate
$ uvicorn app.main:app --reload --reload-include '*.html,*.css'
```

## Development

### Tailwind

Scan template files at input file (`-i`) and build them into output file (`-o`):

```console
$ tailwindcss -i ./app/static/src/tw.css -o ./app/static/css/main.css --watch
```

- Use the `--watch` argument for a watcher that compiles on save (similar to FastAPI's --reload)
- Use the `--minify` argument when compiling to production, as it minifies the output CSS

## Tests

```console
$ source .venv/bin/activate
$ python3 -m unittest discover -s tests
```
