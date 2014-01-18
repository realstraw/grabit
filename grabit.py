import urllib2
from bs4 import BeautifulSoup
import re
import argparse


def get_all_pdfs(html_content):
    """
    return the urls of all pdf files in an html document
    """
    soup = BeautifulSoup(html_content)
    pdf_a = soup.findAll('a', attrs={
        'href': re.compile(r'^http[s]?://.*?\.pdf$')})
    return [l.get('href') for l in pdf_a]


def get_internet_files(urls, target_location):
    successful_downloads = []
    failed_downloads = []
    for url in urls:
        print "getting file from url: {}".format(url)
        try:
            pdf_file = urllib2.urlopen(url)
            successful_downloads.append(url)
            fname = url.split('/')[-1]
            fname = "{}/{}".format(target_location, fname)
            with open(fname, 'w') as f:
                f.write(pdf_file.read())
        except urllib2.HTTPError:
            failed_downloads.append(url)

    # print out a summary
    print "Successfully downloaded:"
    print '\n'.join(successful_downloads)
    print "Failed downloaded:"
    print '\n'.join(failed_downloads)

    print "Summary: successful count is {}\nfailed count is "\
        "{}".format(len(successful_downloads), len(failed_downloads))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download all linked pdf files in the given document")
    parser.add_argument(
        'source', help="the source html document containing all the links")
    parser.add_argument(
        'destination',
        help="the destination folder that pdf should be downloaded to")
    args = parser.parse_args()
    html_file = args.source
    target_location = args.destination

    with open(html_file, 'r') as html_content:
        pdf_links = get_all_pdfs(html_content)
        get_internet_files(pdf_links, target_location)
