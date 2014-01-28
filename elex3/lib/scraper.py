#!/usr/bin/env python
from urllib import urlretrieve


def download_results(path):
    """Download CSV of fake Virginia election results from GDocs

    Downloads the file to the root of the repo (/path/to/refactoring101/).

    NOTE: This will only download the file if it doesn't already exist
    This approach is simplified for demo purposes. In a real-life application,
    you'd likely have a considerable amount of additional code
    to appropriately handle HTTP timeouts, 404s, and other real-world scenarios.
    For example, you might retry a request several times after a timeout, and then
    send an email alert that the site is non-responsive.

    """
    url = "https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=csv"
    urlretrieve(url, path)
