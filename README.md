<h1 align="center" >Gigsgo.at</h1>

<p align="center">
  <a href="https://github.com/essteer/gigsgo-api/actions/workflows/test.yaml"><img src="https://github.com/essteer/gigsgo-api/actions/workflows/test.yaml/badge.svg"></a>
  <a href="https://github.com/essteer/gigsgo-api"><img src="https://img.shields.io/badge/Python-3.10_~_3.12-3776AB.svg?style=flat&logo=Python&logoColor=white"></a>
  <a href="https://github.com/tiangolo/fastapi"><img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=FastAPI&labelColor=555&logoColor=white"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json"></a>
  <a href="https://github.com/tailwindlabs/tailwindcss"><img src="https://img.shields.io/badge/Tailwind-06B6D4.svg?style=flat&labelColor=555&logo=Tailwind-CSS&logoColor=white"></a>
</p>

<p align="center">
An API and web app for live music listings.
</p>

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
