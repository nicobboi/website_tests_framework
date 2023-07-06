import requests
import urllib.robotparser

# Checks if the given URI is crawlable (following the robots.txt rules) 
# and if there's at least one sitemap file at the given URI
def test(uri):
    output = ""
    '''
    output = {
        "is_crawlable": False,
        "sitemap_present": {
            "present": False,
            "notes": ""
        }
    }
    '''

    if uri[-1] != '/':
        uri += '/'

    # robot parser
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(uri + "robots.txt")
    rp.read()

    if rp.can_fetch("*", uri):
        output += "Url crawlable!\n\n"
    else:
        output += "Url not crawlable!\n\n"

    if rp.site_maps() != None:
        output += "Sitemap is present!\n"
        output += "Sitemap parameter is present in the robots.txt.\n\n"
    else:
        # list of commons sitemap files
        sitemap = [
            "sitemap.xml",
            "sitemap_index.xml",
            "sitemap-index.xml",
            "sitemap.php",
            "sitemap.txt",
            "sitemap.xml.gz",
            "sitemap/",
            "sitemap/sitemap.xml",
            "sitemapindex.xml",
            "sitemap/index.xml",
            "sitemap1.xml",
            "rss/,"
            "rss.xml",
            "atom.xml"
        ]

        for s in sitemap:
            res = requests.get(uri + s)
            if res.status_code == 200:
                output += "Sitemap is present!\n"
            
        output += "Sitemap parameter is not present in the robots.txt!\n\n"
        
    # TODO: controllare se i siti presenti nella sitemap non sono rotti

    return output    
    
