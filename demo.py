"""
demo.py — Quick command-line demo for the Ballon d'Or Scraper.

Runs all four modes (None, Player, Nation, Club) with a default
configuration and prints results to the console.

Usage
-----
    python demo.py
    python demo.py --player "Cristiano Ronaldo" --start 2000 --end 2023
    python demo.py --player "Ronaldo" --start 1995 --end 2005 --viz Club

Requirements
------------
    pip install -r requirements.txt
"""

import argparse
import sys

# ── Attempt import ────────────────────────────────────────────────────────────
try:
    from ballon_dor_scraper import ballon_dor_scraper
except ImportError:
    # Fallback: load the function directly from the notebook source
    import importlib.util, types, json, textwrap

    with open("ballon_dor_scraper.ipynb", "r", encoding="utf-8") as f:
        nb = json.load(f)

    source_cells = [
        "".join(cell["source"])
        for cell in nb["cells"]
        if cell["cell_type"] == "code"
    ]
    # Only the first code cell contains the function definitions
    module_source = source_cells[0] if source_cells else ""

    mod = types.ModuleType("ballon_dor_scraper")
    exec(compile(module_source, "ballon_dor_scraper.ipynb", "exec"), mod.__dict__)
    ballon_dor_scraper = mod.ballon_dor_scraper


# ── CLI argument parsing ──────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description="Ballon d'Or Scraper — command-line demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Examples:
              python demo.py
              python demo.py --player "Cristiano Ronaldo" --start 2010 --end 2023
              python demo.py --viz Nation
              python demo.py --viz Club --start 1990 --end 2010
        """)
    )
    parser.add_argument(
        "--url",
        default="https://en.wikipedia.org/wiki/Ballon_d%27Or",
        help="Wikipedia Ballon d'Or page URL (default: Wikipedia EN)"
    )
    parser.add_argument(
        "--start", type=int, default=2000,
        help="Start year, inclusive (default: 2000)"
    )
    parser.add_argument(
        "--end", type=int, default=2023,
        help="End year, inclusive (default: 2023)"
    )
    parser.add_argument(
        "--player", default="Lionel Messi",
        help="Player name to query (default: 'Lionel Messi')"
    )
    parser.add_argument(
        "--viz", default="None",
        choices=["None", "Player", "Nation", "Club"],
        help="Visualisation mode (default: None)"
    )
    return parser.parse_args()


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    args = parse_args()

    print("=" * 60)
    print("  Ballon d'Or Scraper & Analyser")
    print("=" * 60)
    print(f"  Year range : {args.start} – {args.end}")
    print(f"  Query      : {args.player}")
    print(f"  Viz mode   : {args.viz}")
    print("=" * 60)
    print()

    df = ballon_dor_scraper(
        url=args.url,
        start=args.start,
        end=args.end,
        PerfQuery=args.player,
        viz=args.viz
    )

    print(f"\nDataFrame shape : {df.shape[0]} rows × {df.shape[1]} columns")
    print("\nFirst 10 rows:")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
