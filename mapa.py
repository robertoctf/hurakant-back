import folium

def main():
    mymap= folium.Map(
    location=[19, -89],
    zoom_start=6,
    tiles='OpenStreetMap')
    mymap.save('Cono.html')



main()