PageSpeed Insight (PSI) reports the user experience of a page on mobile devices
and desktop and provides suggestions on how to improve it.

The UX data in PSI are based on the Chrome User Experience Report (CrUX) dataset.
PSI uses Lighthouse to analyze the URL in a simulated environment for the categories
Performance, Accessibility, Best Practice and SEO (here is used mainly for performance).

[Score docs](https://developers.google.com/speed/docs/insights/v5/about?hl=it) <br />

[API docs](https://developers.google.com/speed/docs/insights/rest/v5/pagespeedapi/runpagespeed)

This module takes as a input the URI of the page, which you want to test the performace, and
returns a JSON file with all the data.

### DOCS:
```
pagespeed.**test**(*URI*)
    Runs a performance test, using the PageSpeed Insight's API, on the given URI and returns a JSON with all the data.

```
