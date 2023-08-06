iso3166-scraper
===============

A simple utility for scraping ISO-3166 country data from a [Wikipedia
article](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) that 
contains all current country codes, names, etc.

In a recent project, I had a need for the ISO 3166 country code data and was
disappointed to discover that there really wasn't a good free source for 
obtaining the data in structured form. I'm sure there's some place where I 
could spend money with ISO to get this data, but that's not a great option 
for an open source project with no revenue stream for such expenses.

However, the above referenced Wikipedia article was pretty cleanly structured 
and easy enough to scrape. The data changes infrequently, so occasionally 
running this utility to get the latest data seems like a decent compromise.
Maybe you'll find it useful too.

This utility scrapes the web page, and outputs the country code data in
JSON and YAML formats.

In addition to the basic country data, the script maps the country codes
to the corresponding Unicode code points for each country's flag and
includes the appropriate escape sequences in a string property of the
output data in every format.

This tool is built using some excellent open source components that make
creating tools like this really easy.

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) -- HTML
  page scraping
* [Requests](https://requests.readthedocs.io/en/latest/) -- HTTP for Humans
* [ruamel.yaml](https://pypi.org/project/ruamel.yaml/) -- YAML reader/writer


Installation
------------

This package is available for installation via PyPI and can therefore be 
installed using *pip* as follows.

```bash
python3 -m pip install iso3166-scraper
```

Usage
-----

After installation, you can simply run it.

```
$ iso3166-scraper
retrieving https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
writing JSON file: ./iso3166.json
writing YAML file: ./iso3166.yml
```

By default, it fetches the Wikipedia article, scrapes the ISO 3166 country
data from the page, and produces JSON and YAML output files in the current
directory. Using command line options, you can select which output format
you want and where to put it. To see all the options, use

```bash
iso3166-scraper --help
```

