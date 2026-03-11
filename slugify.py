#!/usr/bin/env python3
"""slugify - URL slug generator from text strings.

Single-file, zero-dependency CLI.
"""

import sys
import argparse
import re
import unicodedata


def slugify(text, separator="-", lowercase=True, max_length=0, transliterate=True):
    if transliterate:
        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    if lowercase:
        text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', separator, text).strip(separator)
    text = re.sub(f'{re.escape(separator)}+', separator, text)
    if max_length:
        text = text[:max_length].rstrip(separator)
    return text


def cmd_convert(args):
    text = " ".join(args.text)
    result = slugify(text, args.separator, not args.keep_case, args.max_length)
    print(result)


def cmd_batch(args):
    for line in sys.stdin:
        line = line.strip()
        if line:
            print(slugify(line, args.separator))


def cmd_filename(args):
    """Make safe filename."""
    text = " ".join(args.text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r'[^\w\s.\-]', '', text)
    text = re.sub(r'\s+', '_', text).strip('_')
    if args.ext:
        text = f"{text}.{args.ext.lstrip('.')}"
    print(text)


def main():
    p = argparse.ArgumentParser(prog="slugify", description="URL slug generator")
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("convert", aliases=["c"], help="Slugify text")
    s.add_argument("text", nargs="+")
    s.add_argument("-s", "--separator", default="-")
    s.add_argument("-k", "--keep-case", action="store_true")
    s.add_argument("-m", "--max-length", type=int, default=0)
    s = sub.add_parser("batch", aliases=["b"], help="Batch from stdin")
    s.add_argument("-s", "--separator", default="-")
    s = sub.add_parser("filename", aliases=["f"], help="Safe filename")
    s.add_argument("text", nargs="+")
    s.add_argument("-e", "--ext")
    args = p.parse_args()
    if not args.cmd: p.print_help(); return 1
    cmds = {"convert": cmd_convert, "c": cmd_convert, "batch": cmd_batch, "b": cmd_batch,
            "filename": cmd_filename, "f": cmd_filename}
    return cmds[args.cmd](args) or 0


if __name__ == "__main__":
    sys.exit(main())
