Sitemap Checker is a simple python script that checks if the given URL is crawlable (following the robots.txt rules) and if there is at least one sitemap file present, also searched from the given URL. <br />

If there's no sitemap parameter in robots.txt, it will searches using this sitemap files list:
    sitemap.xml,
    sitemap_index.xml,
    sitemap-index.xml,
    sitemap.php,
    sitemap.txt,
    sitemap.xml.gz,
    sitemap/,
    sitemap/sitemap.xml,
    sitemapindex.xml,
    sitemap/index.xml,
    sitemap1.xml,
    rss/,
    rss.xml,
    atom.xml
<br />

### DOCS:
```
sitemapchecker.**test**(*URI*)
    Returns a dict with info on url crawlability and presence of sitemap files.
    dict = {
        "is_crawlable": Boolean,
        "sitemap_present": {
            "present": Boolean,
            "notes": String
        }
    }
```