import urllib.request
import urllib.parse
import json
from SPARQLWrapper import SPARQLWrapper, JSON

# get property json
#------------------
url3 = 'https://tools.wmflabs.org/hay/propbrowse/props.json'
p = urllib.request.urlopen(url3)
propJson = json.loads(p.read().decode('utf-8'))
# print(json.dumps(propJson, indent=4))
# choose property
#----------------
# make the search better
def getPropId():
    searchProp = input("search property: ")
    prop = ''
    counter = 0
    propArray = []
    for property in enumerate(propJson):
        if searchProp in property[1]['label']:
            propArray.append(property)
            counter += 1
            # print(json.dumps(property, indent=4))
            print(str(counter)+'.', property[1]['label']+",", property[1]['description']+',', property[1]['id'])
    chooseProp = input('choose property: ')
    prop = propArray[int(chooseProp)-1][1]['id']
    propDesc = propArray[int(chooseProp)-1][1]['label']
    if prop == '':
        print('property query empty')
        getPropId()
    return(prop, propDesc)
prop, propDesc = getPropId();
# get entity id
#--------------
# query only wikipedia?
def getEntId():
    searchTerm = input("search entity: ").replace(' ', '_')
    url = 'https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=en&search=' + searchTerm
    s =  urllib.request.urlopen(url)
    jsonObj = json.loads(s.read().decode('utf-8'))
    print(json.dumps(jsonObj['search'], indent = 2))
    for i, searchResult in enumerate(jsonObj['search'],1):
        print(str(i)+".",searchResult['label'],end=", ")
        if 'description' in  searchResult: print (searchResult['description'], end=", ")
        print(searchResult['id'])
    return(jsonObj)
    if jsonObj['search'] == []:
        print("entity query empty")
        getEntId()
jsonObj = getEntId()
chooseEnt = input("choose entity: ")
searchEnt = jsonObj['search'][int(chooseEnt)-1]["id"]
# SPARQL query
searchEntLabel = jsonObj['search'][int(chooseEnt)-1]["label"]
from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""#Cats
SELECT ?item ?itemLabel
WHERE
{

  ?item wdt:"""+ prop +""" wd:"""+ searchEnt +""".
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
for result in results["results"]["bindings"]:
    print(json.dumps(result, indent=4))
print("property: "+propDesc,","+prop,"entity: "+searchEntLabel,","+searchEnt+",", str(len(results['results']['bindings']))+" results.")
