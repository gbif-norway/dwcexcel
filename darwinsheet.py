#!/usr/bin/python

import sys
import uuid
import rdflib
import xlsxwriter

# grab descriptions/examples from the dwc rdf
comments = {}
descriptions = {}
g = rdflib.Graph()
g.load("https://raw.githubusercontent.com/tdwg/dwc/master/rdf/dwcterms.rdf")
for s, p, o in g:
    term = s.replace("http://rs.tdwg.org/dwc/terms/", "")
    if unicode(p) == "http://www.w3.org/2000/01/rdf-schema#comment":
        comments[term] = unicode(o)
    elif unicode(p) == "http://purl.org/dc/terms/description":
        descriptions[term] = unicode(o)

terms = [
    'occurrenceID',
    'basisOfRecord',
    'eventDate',
    'kingdom',
    'scientificName',
    'taxonRank',
    'decimalLatitude',
    'decimalLongitude',
    'geodeticDatum',
    'coordinateUncertaintyInMeters',
    'countryCode',
    'individualCount',
    'organismQuantity',
    'organismQuantityType'
]
required = [
    'occurrenceID',
    'basisOfRecord',
    'eventDate',
    'scientificName'
]

workbook = xlsxwriter.Workbook("occurrences.xlsx")
worksheet = workbook.add_worksheet()

overflow = workbook.add_format({ 'align': 'vjustify' })
reqformat = workbook.add_format({ 'bold': True, 'bg_color': '#aaffaa' })
recformat = workbook.add_format({ 'bold': True, 'bg_color': '#ffffaa' })

reqformat.set_shrink()

for n, term in enumerate(terms):
    worksheet.write(0, n, term, reqformat if term in required else recformat)
    worksheet.write_comment(0, n,
            ("REQUIRED" if term in required else "RECOMMENDED") + "\n\n" + 
            comments[term] + "\n\n" + descriptions[term])
    width = len(term) + 4
    worksheet.set_column(0, n, width)
    if(term == 'occurrenceID'):
        for row in range(1, 10000):
            worksheet.write(row, n, "urn:uuid:" + str(uuid.uuid4()), overflow)

workbook.close()

