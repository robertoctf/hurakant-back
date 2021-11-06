from pprint import pp, pprint
import xmltodict
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO


link = "http://www.nhc.noaa.gov/gis/kml/nhc_active.kml"



def main():
    #Abrir link
    data = urlopen(link)

    dicto = xmltodict.parse(data)
    newDict = dicto["kml"]["Document"]["Folder"]


    wspTemp = ""
    wsp = {}
    cyclones = []
    #crear diccionario
    for x in newDict:
        #agregar los datos de wsp
        if x["@id"] == "wsp":
            wspTemp = x["Folder"]["NetworkLink"]
            for y in wspTemp:

                wsp[y["@id"]] = {
                    "name": y["name"],
                    "visibility": y["visibility"],
                    "open": y["open"],
                    "link": y["Link"]["href"],
                    "kml": kmzToKml(y["Link"]["href"])
                }
            continue
        #extraer los datos cientificos de cada ciclon
        tempMetadata = {}
        for y in x["ExtendedData"][0]["Data"]:
            tempMetadata[y["@name"]] = y["value"]

        #extraer el link y datos generales
        tempDatos = {}
        for y in x["NetworkLink"]:
            tempDatos[y["@id"]] = {
                "name": y["name"],
                "visibility": y["visibility"],
                "link": y["Link"]["href"],
                "kml": kmzToKml(y["Link"]["href"])
            }
        #agregarlo a lista
        cyclones.append({
            "id": x["@id"],
            "name": x["name"],
            "visibility": x["visibility"],
            "metaData": tempMetadata,
            "id": x["@id"],
            "datos": tempDatos

        })

    pprint(wsp)
            
def kmzToKml(link):
    resp = urlopen(link)
    
    name = ""
    zipfile = ZipFile(BytesIO(resp.read()))
    for x in zipfile.namelist():
        if "kml" in x:
            name = x
        
    kml = zipfile.open(name, 'r')
    return kml



main()