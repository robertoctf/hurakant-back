from pprint import pp, pprint
import xmltodict
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import geopandas as gpd
import fiona
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point, MultiPolygon, shape


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



def main2():


    # Aqui va el archivo KML
    HURRICAN_KML = 'al212021_025adv_CONE.kml'
    # Aqui va el punto GPS
    GPS_POINT = (-30.0004, 43.63373)

    gdf_hurrican = read_kml(HURRICAN_KML)
    gdf_hurrican.geometry = convert_3D_2D(gdf_hurrican.geometry)
    poly_hurrican = gdf_hurrican.iloc[0]['geometry']

    point_gps = Point(GPS_POINT)

    # Interseccion entre el punto del gps y el
    # poligono del huracan
    print('Hay Interseccion? = ', point_gps.within(poly_hurrican))

    # Graficando el huracan y el punto GPS
    x,y = poly_hurrican.exterior.xy
    plt.plot(x,y)
    plt.plot(point_gps.x, point_gps.y, marker='o', markersize=3, color="red")
    plt.show()



# Convierte de kml a geopandas df
def read_kml(kml_file):
    gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
    df = gpd.read_file(kml_file, driver='KML')
    return df


# Convierte la informacion geometrica del shape de 3D a 2D
def convert_3D_2D(geometry):
    new_geo = []
    for p in geometry:
        if p.has_z:
            if p.geom_type == 'Polygon':
                lines = [xy[:2] for xy in list(p.exterior.coords)]
                new_p = Polygon(lines)
                new_geo.append(new_p)
            elif p.geom_type == 'MultiPolygon':
                new_multi_p = []
                for ap in p:
                    lines = [xy[:2] for xy in list(ap.exterior.coords)]
                    new_p = Polygon(lines)
                    new_multi_p.append(new_p)
                new_geo.append(MultiPolygon(new_multi_p))
    return new_geo



main()