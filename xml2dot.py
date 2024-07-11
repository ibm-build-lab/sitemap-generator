#!/usr/bin/env python

import sys
import os

"""
Example to convert XML to DOT file.
Call with XML filename as first argument.
Creates an DOT graph file.
Example command: python xml2dot.py links-tree-hierarchy.xml
To view the DOT graph, convert it to an SVG file using this command: dot website_links_graph.dot -Tsvg -Goverlap=false -Grankdir=LR > sitemap.svg
"""
from xml.sax import parse, ContentHandler

class Xml2DotHandler(ContentHandler):
	def __init__(self, html = False):
		self.parent = []
		self.id = 0
		self.html = html
		self.file = open("website_links_graph.dot", "w")
	def startDocument(self):
		
		
		self.file.write("digraph G {")
		self.file.write("""
			graph [
				rankdir = TD
			];
			node [
                fontname = "Bitstream Vera Sans"
                fontsize = 8
                shape = "Mrecord"
			];
		""")
	
	def endDocument(self):
		self.file.write("}")
	
	def startElement(self, name, attrs):
		print("name: ", name)
		print("attrs: ", attrs)
		node = {"name":"a%d" % (self.id,) ,"attributes":{n: attrs.getValue(n) for n in attrs.getNames()}, "content":""}
		self.parent.append(node)
		self.id += 1
	
	def characters(self, chars):
		self.parent[-1]["content"] += chars
	
	def endElement(self, name):
		node = self.parent.pop()
		node["content"] = node["content"].strip()
		label = ""
		if self.html:
			label += "<<TABLE><TR><TD>"+name+"</TD></TR>"
			if node["attributes"]:
				label += "<TR><TD>"
				label += "<BR/>".join(["%s = %s" % (item[0], item[1]) for item in node["attributes"].items()])
				label += "</TD></TR>"
			if node["content"]:
				label += "<TR><TD>" + node["content"] + "</TD></TR>"
			label += "</TABLE>>"
		else:
			label = "\"{" + name
			if node["attributes"]:
				print("attributes: ", node["attributes"])
				label += "|"
				label += "\l".join(["%s = %s" % (item[0], item[1]) for item in node["attributes"].items()])
			if node["content"]:
				#print("content: ", node["content"])
				label += "|" + node["content"]
			label += "}\""
		self.file.write("%s [label=%s];" % (node["name"], label))
		if self.parent:
			self.file.write("%s -> %s;" % (self.parent[-1]["name"], node["name"]))

doc = parse(sys.argv[1], Xml2DotHandler(html = False))

