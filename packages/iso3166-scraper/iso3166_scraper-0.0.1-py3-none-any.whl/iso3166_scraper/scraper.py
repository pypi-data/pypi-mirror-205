import argparse
import json
import os

import ruamel.yaml

from iso3166_scraper.extractor import Extractor
from iso3166_scraper.flag_mapper import map_flags
from iso3166_scraper.retriever import Retriever


PROG = "iso3166-scraper"
DEFAULT_URL = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"

BASE_FILENAME = "iso3166"
DEFAULT_JSON_FILENAME = f"{BASE_FILENAME}.json"
DEFAULT_YAML_FILENAME = f"{BASE_FILENAME}.yml"


class OutputAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs, **kwargs):
        super().__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, f"{self.dest}_enabled", True)
        if values:
            setattr(namespace, self.dest, values)


def parse_args():
    parser = argparse.ArgumentParser(prog=PROG,
                                     description="a utility for scraping ISO 3166 country codes from Wikipedia")
    parser.set_defaults(json_enabled=False, json=DEFAULT_JSON_FILENAME,
                        yaml_enabled=False, yaml=DEFAULT_YAML_FILENAME,
                        dir=".", url=DEFAULT_URL)
    parser.add_argument("--url", "-u", help="specify the URL for the page to scrape")
    parser.add_argument("--dir", "-d", help="specify a directory path for output files")
    parser.add_argument("--json", "-j", nargs="?", action=OutputAction,
                        help="enable JSON and optionally specify output filename")
    parser.add_argument("--yaml", "-y", nargs="?", action=OutputAction,
                        help="enable YAML and optionally specify output filename")
    return parser.parse_args()


def generate_json(records, output_dir, filename):
    output_filename = os.path.join(output_dir, filename) if output_dir else filename
    print(f"writing JSON file: {output_filename}")
    with open(output_filename, "w+") as output_file:
        json.dump(records, output_file, indent=2)


def generate_yaml(records, output_dir, filename):
    output_filename = os.path.join(output_dir, filename) if output_dir else filename
    print(f"writing YAML file: {output_filename}")
    with open(output_filename, "w+") as output_file:
        yaml = ruamel.yaml.YAML()
        yaml.dump(records, output_file)


def main():
    args = parse_args()
    extractor = Extractor()
    retriever = Retriever(args.url)

    text = retriever.retrieve()
    records = map_flags(extractor.extract_data(text))

    if not args.json_enabled and not args.yaml_enabled:
        generate_json(records, args.dir, args.json)
        generate_yaml(records, args.dir, args.yaml)
    if args.json_enabled:
        generate_json(records, args.dir, args.json)
    if args.yaml_enabled:
        generate_yaml(records, args.dir, args.yaml)


if __name__ == "__main__":
    main()
