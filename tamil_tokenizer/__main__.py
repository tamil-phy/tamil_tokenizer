"""
Tamil Tokenizer CLI - Command-line interface for Tamil tokenization.

Usage:
    python -m tamil_tokenizer "அவன் வந்தான்."
    python -m tamil_tokenizer "அவன் வந்தான்." --level character
    python -m tamil_tokenizer "அவன் வந்தான். அவள் பார்த்தாள்." --level sentence
    python -m tamil_tokenizer "பள்ளிக்கு சென்றான்." --level morpheme
    python -m tamil_tokenizer --interactive
"""

import argparse
import sys
from typing import Optional

from .tokenizer import TamilTokenizer, Token


def print_tokens(tokens: list, level: str, text: str) -> None:
    """Print tokens in a formatted table."""
    print(f"\n{'='*60}")
    print(f"Tokenization Level: {level}")
    print(f"Input: {text}")
    print(f"{'='*60}")
    print(f"Tokens ({len(tokens)}):")

    for i, token in enumerate(tokens):
        meta_str = ""
        if token.metadata:
            meta_parts = [f"{k}={v}" for k, v in token.metadata.items()]
            meta_str = f"  ({', '.join(meta_parts)})"
        print(f"  {i+1}. [{token.token_type.value:>16}] '{token.text}'{meta_str}")


def interactive_mode(tokenizer: TamilTokenizer) -> None:
    """Run tokenizer in interactive mode."""
    print("Tamil Tokenizer - Interactive Mode")
    print("Type Tamil text to tokenize. Commands:")
    print("  :level <sentence|word|character|morpheme>  - Change level")
    print("  :quit                                      - Exit")
    print(f"{'='*60}")

    current_level = "word"

    while True:
        try:
            text = input(f"\n[{current_level}] >>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not text:
            continue

        if text == ":quit":
            print("Goodbye!")
            break

        if text.startswith(":level "):
            new_level = text.split(maxsplit=1)[1].strip()
            if new_level in ("sentence", "word", "character", "morpheme"):
                current_level = new_level
                print(f"Level set to: {current_level}")
            else:
                print(f"Unknown level: {new_level}. Use: sentence, word, character, morpheme")
            continue

        tokens = tokenizer.tokenize(text, level=current_level)
        print_tokens(tokens, current_level, text)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Tamil Tokenizer - Multi-level tokenization for Tamil text',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "அவன் வந்தான்."                           Word tokenization (default)
  %(prog)s "அவன் வந்தான்." --level character          Character tokenization
  %(prog)s "அவன் வந்தான். அவள் பார்த்தாள்." --level sentence  Sentence tokenization
  %(prog)s "பள்ளிக்கு சென்றான்." --level morpheme      Morpheme tokenization
  %(prog)s --interactive                              Interactive mode
        """
    )

    parser.add_argument('text', nargs='?', help='Tamil text to tokenize')
    parser.add_argument('-l', '--level', default='word',
                        choices=['sentence', 'word', 'character', 'morpheme'],
                        help='Tokenization level (default: word)')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Run in interactive mode')
    parser.add_argument('-d', '--data', metavar='PATH',
                        help='Path to data directory')
    parser.add_argument('-f', '--format', default='table',
                        choices=['table', 'text', 'json'],
                        help='Output format (default: table)')
    parser.add_argument('--version', action='version',
                        version='Tamil Tokenizer 1.0.0')

    args = parser.parse_args()

    tokenizer = TamilTokenizer(args.data)

    if args.interactive:
        interactive_mode(tokenizer)
    elif args.text:
        if args.format == 'json':
            import json
            result = tokenizer.tokenize_to_dicts(args.text, level=args.level)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.format == 'text':
            result = tokenizer.tokenize_to_strings(args.text, level=args.level)
            for t in result:
                print(t)
        else:
            tokens = tokenizer.tokenize(args.text, level=args.level)
            print_tokens(tokens, args.level, args.text)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
