#!/usr/bin/python
"""
Example to filter XML output.
Call with XML output filename as first argument.
Prints filtered result on standard output.
Example command: python ./applause_links_tree.py linkchecker-out.xml filtered-links-out.xml links-tree-hierarchy.xml
"""
import sys
from xml.etree.ElementTree import parse
import xml.etree.cElementTree as ET
from xml.dom import minidom


def main(args):
    filename = args[0]
    filtered_file = args[1]
    final_output_file = args[2]

    with open(filename) as fd:
       
        tree = parse(fd)
        filter_tree(tree)

        # Save to XML file
        new_file = open(filtered_file, 'wb')
        tree.write(new_file, encoding="utf-8")

        # create a hierarchical tree of links
        root = tree.getroot()
        level = 0
        website_url = root.find(".//*[level='%s']" % level).find("realurl").text
        seed_root = ET.Element("seed_root", website_url=website_url)
        create_tree_hierarchy(root, seed_root)

        format_xml(seed_root, final_output_file)


"""
Use this function to remove all filtered links
"""
def filter_tree(tree):

    to_remove = []
    for elem in tree.findall("urldata"):
        valid = elem.find("valid")
        warnings = elem.find("warnings")

        parent = ''
        if (elem.find("parent") is not None):
            parent = elem.find("parent").text
        realurl = elem.find("realurl").text
        #TODO: Find a way to generalize this. Not all websites will have these paths.
        sister_links = False
        if ("/blog/" in parent and "/blog/" in realurl):
            sister_links = True
        if ("/newsroom/" in parent and "/newsroom/" in realurl):
            sister_links = True
        if ("/podcasts/" in parent and "/podcasts/" in realurl):
            sister_links = True
        if ("/resources/" in parent and "/resources/" in realurl):
            sister_links = True

        if (
            (valid is not None 
            and not valid.attrib.get("result").startswith("200 OK"))
            or (warnings is not None and warnings.find("warning").get("tag") == 'http-redirected') 
            or sister_links
        
        ):
            to_remove.append(elem)
    root = tree.getroot()
    for elem in to_remove:
        root.remove(elem)


"""
Create a tree hierarchy
"""
def create_tree_hierarchy(root, seed_root):

    get_children(root, (seed_root.attrib)["website_url"], seed_root)


"""
Recursively create child nodes in the tree
"""
def get_children(root, parent_url, seed_root):
    children = root.findall(".//*[parent='%s']" % parent_url)

    if(len(children) == 0):
        return

    for child in children:
        
        urldata = ET.SubElement(seed_root, "urldata",
                                 realurl=child.find("realurl").text,
                                 url=child.find("url").text,
                                 sourceurl=child.find("parent").text,
                                 depth=child.find("level").text
                                 )
        
        get_children(root, child.find("realurl").text, urldata)


"""
Use this function to test for any missimg URls
"""
def find_missing_child(root, url_tree, depth):
    root_children = root.findall(".//*[level='%s']" % depth)
    url_tree_children = url_tree.findall(".//*[depth='%s']" % depth)

    for child in root_children:
        match = False
        root_url = child.find("realurl").text
        for ch in url_tree_children:
            ch_url = ch.find("realurl").text
            if(root_url == ch_url):
                match = True
        if(not match): print("root_url: ", root_url)

"""
Use this function to format an xml file
"""
def format_xml(root, file_name):
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open(file_name, "w") as f:
        f.write(xmlstr) 
    

if __name__ == "__main__":
    main(sys.argv[1:])