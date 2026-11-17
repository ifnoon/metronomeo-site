# Metronomeo website

Production: https://metronomeo.com

Static HTML and CSS. No application framework or build step. `nginx:alpine` serves the site on Railway's injected PORT.

## Local preview

`python3 -m http.server 8766`

## Deployment

Railway project **Websites**, service **metronomeo**, production environment. The main branch of `ifnoon/metronomeo-site` is the deployment source. Custom domains are `metronomeo.com` and `www.metronomeo.com`; www redirects permanently to the root domain.

## Search structure

Homepage → footer Practice guides → /guides/ → individual articles. Related guides link articles together. Every public page is listed in sitemap.xml. robots.txt points to the sitemap. Articles include Article and BreadcrumbList JSON-LD, titles, descriptions and canonical URLs.

Article source text is in content/. Published HTML is in guides/. To update articles, install scripts/requirements.txt in a Python virtual environment and run `python scripts/build_site.py`. ffmpeg is needed when creating the original audio examples. The builder writes guide pages, related links, structured data, responsive WebP images and sitemap.xml. It does not run in production. Review the output before committing. Use real modification dates only when content changes. No rankings or indexing timelines are guaranteed.

Seven guides cover subdivisions, displaced clicks, silent bars, tempo ladders, polyrhythms, polymetric groupings and Ableton Link/MIDI. Diagrams and click examples are original educational illustrations, not app recordings. Audio never autoplays and is not preloaded. The app manual is the reference for product behavior; the connectivity guide also links to Ableton's official documentation.

Homepage metadata uses WebSite, WebPage and Organization structured data. Software app rich results require genuine eligible review/rating data which we do not currently publish. Do not fabricate ratings or add incomplete app rich-result markup simply to satisfy a checker. This does not prevent ordinary search indexing.

Nginx uses relative redirects behind Railway's HTTPS proxy so internal port 8080 is never exposed in directory redirects. `/guides` redirects to `/guides/`. Index file aliases retain canonical tags; they must not have unconditional redirect locations, because Nginx internally resolves directory indexes through those locations. Responsive image filenames include a source hash and can be cached for 30 days.

Google Search Console domain property: metronomeo.com. Keep the google-site-verification DNS TXT record. Sitemap submitted and homepage indexing requested on 17 November 2026.

## Analytics

GA4 account 54653930, property 564772486 (Metronomeo), web stream 16357081669, measurement ID G-DNJX7KFH00. Website analytics is distinct from app analytics. Analytics loads only after consent. Google signals and ad personalization are disabled. Footer Cookie settings can change the choice.

`app_store_click` measures website clicks to Apple's listing, not actual installs. App Store Connect is the source for downloads and subscription revenue.

## Verification

Check local links, headings, anchors, JSON-LD and sitemap XML; inspect desktop and 320px mobile layouts; verify production URLs return 200 and www returns 301; check consent accept/decline and the App Store click event in GA4 Realtime.
