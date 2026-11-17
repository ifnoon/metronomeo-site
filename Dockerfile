FROM nginx:alpine
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY *.html *.css *.js robots.txt sitemap.xml /usr/share/nginx/html/
COPY assets /usr/share/nginx/html/assets
COPY guides /usr/share/nginx/html/guides
ENV PORT=8080
EXPOSE 8080
