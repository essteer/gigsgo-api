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
$ uvicorn src.app:app --reload --reload-include *.html,*.css
```

## Tests

```console
$ source .venv/bin/activate
$ python3 -m unittest discover -s tests
```
