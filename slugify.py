#!/usr/bin/env python3
"""slugify - Convert text to URL-safe slugs and identifiers.

One file. Zero deps. Cleans text.

Usage:
  slugify.py "Hello, World!"             → hello-world
  slugify.py "Hello, World!" --snake     → hello_world
  slugify.py "Hello, World!" --camel     → helloWorld
  slugify.py "Hello, World!" --pascal    → HelloWorld
  slugify.py "Hello, World!" --const     → HELLO_WORLD
  slugify.py "My Document.pdf" --file    → my-document.pdf
  echo -e "line one\\nline two" | slugify.py --batch
"""

import argparse
import re
import sys
import unicodedata


TRANSLITERATIONS = {
    'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
    'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'å': 'a',
    'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
    'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
    'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o',
    'ù': 'u', 'ú': 'u', 'û': 'u',
    'ñ': 'n', 'ç': 'c', 'ð': 'd', 'ø': 'o', 'þ': 'th',
    'æ': 'ae', 'œ': 'oe', 'ł': 'l', 'đ': 'd',
}


def transliterate(text: str) -> str:
    result = []
    for ch in text:
        if ch.lower() in TRANSLITERATIONS:
            repl = TRANSLITERATIONS[ch.lower()]
            result.append(repl.upper() if ch.isupper() else repl)
        else:
            # NFD decomposition strips accents
            decomposed = unicodedata.normalize('NFD', ch)
            result.append(''.join(c for c in decomposed if unicodedata.category(c) != 'Mn'))
    return ''.join(result)


def to_slug(text: str, separator: str = '-', max_len: int = 0) -> str:
    text = transliterate(text)
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', separator, text)
    text = text.strip(separator)
    if max_len and len(text) > max_len:
        text = text[:max_len].rstrip(separator)
    return text


def to_snake(text: str) -> str:
    return to_slug(text, separator='_')


def to_camel(text: str) -> str:
    slug = to_slug(text)
    parts = slug.split('-')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])


def to_pascal(text: str) -> str:
    slug = to_slug(text)
    return ''.join(p.capitalize() for p in slug.split('-'))


def to_const(text: str) -> str:
    return to_snake(text).upper()


def to_filename(text: str) -> str:
    # Preserve extension
    parts = text.rsplit('.', 1)
    if len(parts) == 2 and len(parts[1]) <= 5:
        return to_slug(parts[0]) + '.' + parts[1].lower()
    return to_slug(text)


def main():
    parser = argparse.ArgumentParser(description="Convert text to URL-safe slugs")
    parser.add_argument("text", nargs="?", help="Text to slugify")
    parser.add_argument("--snake", action="store_true", help="snake_case")
    parser.add_argument("--camel", action="store_true", help="camelCase")
    parser.add_argument("--pascal", action="store_true", help="PascalCase")
    parser.add_argument("--const", action="store_true", help="CONSTANT_CASE")
    parser.add_argument("--file", action="store_true", help="Filename-safe (preserves extension)")
    parser.add_argument("--max", type=int, default=0, help="Max length")
    parser.add_argument("--sep", default="-", help="Separator (default: -)")
    parser.add_argument("--batch", action="store_true", help="Process stdin line by line")
    parser.add_argument("--all", action="store_true", help="Show all formats")

    args = parser.parse_args()

    def convert(text: str) -> str:
        if args.all:
            return (f"  slug:     {to_slug(text, args.sep, args.max)}\n"
                    f"  snake:    {to_snake(text)}\n"
                    f"  camel:    {to_camel(text)}\n"
                    f"  pascal:   {to_pascal(text)}\n"
                    f"  const:    {to_const(text)}\n"
                    f"  filename: {to_filename(text)}")
        if args.snake: return to_snake(text)
        if args.camel: return to_camel(text)
        if args.pascal: return to_pascal(text)
        if args.const: return to_const(text)
        if args.file: return to_filename(text)
        return to_slug(text, args.sep, args.max)

    if args.batch or (not args.text and not sys.stdin.isatty()):
        for line in sys.stdin:
            line = line.strip()
            if line:
                print(convert(line))
        return 0

    if not args.text:
        parser.print_help()
        return 1

    print(convert(args.text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
