# sitemap-generator

We will use this program to do the web crawling and link extraction from a website.

It addresses the following challenges the Applause team is facing:

 - number of links: The program is multithreaded and can handle as many links as the system memory allows.

- links that loop: Links are only checked once.

- deep links: The program only checks internal links and any other URL domain you specify in the configuration file.

- links that return a 404: It logs link errors but we can filter them out if we need to.

- links that are behind a login page and authentication (later), etc: The program supports username/password authorization for HTTP and FTP as well as proxy support. https://linkchecker.github.io/linkchecker/man/linkcheckerrc.html#authentication
  
# Pre-requisites
- [linkchecker](https://linkchecker.github.io/linkchecker/install.html) python library
- [graphviz dot utility](https://graphviz.org/download/)

# How to generate a sitemap

- Run the linkchecker with the following command:
  - > linkchecker --file-output=xml -v -r5 https://www.applause.com/ --ignore-url='.*(?:png|jpg|jpeg|gif|tiff|bmp|svg|js|webp|pdf|xml|css|woff)' --ignore-url='/*(?:fr|de|ja)/'
  - The linkchecker will output an xml map that needs to be filtered of various types of links.
- Run the `applause_links_tree.py` to filtered out links and generated the sitemap.
  - > python ./applause_links_tree.py linkchecker-out.xml filtered-links-out.xml links-tree-hierarchy.xml
    - `linkchecker-out.xml` is the file linkchecker generated.
    - `filtered-links-out.xml` is the file after all the link filters were applied.
    - `links-tree-hierarchy.xml` is the final output file. This file is neatly organized, so we can create a graph of the sitemap.
- To convert the final output file into a [DOT](https://graphviz.org/doc/info/lang.html) file, run the following command. We can use the DOT file to represent the xml tree into a graph.
  - > python xml2dot.py links-tree-hierarchy.xml
- To convert the DOT file into a graph, run the following command:
  - > dot website_links_graph.dot -Tsvg -Goverlap=false -Grankdir=LR > sitemap.svg
