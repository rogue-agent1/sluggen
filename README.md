# slugify

Convert text to URL-safe slugs and identifiers.

One file. Zero deps. Cleans text.

## Usage

```bash
python3 slugify.py "Hello, World!"              # → hello-world
python3 slugify.py "Hello, World!" --snake       # → hello_world
python3 slugify.py "Hello, World!" --camel       # → helloWorld
python3 slugify.py "Hello, World!" --pascal      # → HelloWorld
python3 slugify.py "Hello, World!" --const       # → HELLO_WORLD
python3 slugify.py "Document.pdf" --file         # → document.pdf
python3 slugify.py "Héllo Wörld" --all           # → all formats

# Batch mode
cat titles.txt | python3 slugify.py --batch
```

## Features

- Unicode transliteration (ä→ae, ñ→n, é→e, etc.)
- 6 output formats: slug, snake, camel, pascal, const, filename
- Max length truncation
- Batch stdin processing

## Requirements

Python 3.8+. No dependencies.

## License

MIT
