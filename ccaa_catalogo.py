import json
import requests
from bs4 import BeautifulSoup
# import lxml

print("Inicio App. ======")
print("DECATHLON - FILTRO-PRODUCTOS-POR-COMUNIDAD - MANU GALLEGO - MATTERKIND ES.")

generalFeed = 'https://feeds.lengow.io/3/ye4jv'
comunidadesListado = [
    {'nombre': 'Asturias', 'pagina_id': 1},
    {'nombre': 'Galicia', 'pagina_id': 2},
    {'nombre': 'Cantabria', 'pagina_id': 3},
    {'nombre': 'Pais_vasco', 'pagina_id': 4},
    {'nombre': 'Navarra', 'pagina_id': 5},
    {'nombre': 'Aragon', 'pagina_id': 6},
    {'nombre': 'La_rioja', 'pagina_id': 7},
    {'nombre': 'Catalunya', 'pagina_id': 8},
    {'nombre': 'Castilla_y_leon', 'pagina_id': 9},
    {'nombre': 'Extremadura', 'pagina_id': 10},
    {'nombre': 'Madrid', 'pagina_id': 11},
    {'nombre': 'Castilla_la_mancha', 'pagina_id': 12},
    {'nombre': 'Comunidad_valenciana', 'pagina_id': 13},
    {'nombre': 'Murcia', 'pagina_id': 14},
    {'nombre': 'Andalucia', 'pagina_id': 15},
    {'nombre': 'Baleares', 'pagina_id': 16},
    {'nombre': 'Canarias', 'pagina_id': 17},
    {'nombre': 'Ceuta', 'pagina_id': 18},
    {'nombre': 'Melilla', 'pagina_id': 19}
    ]
productosActualesComunidades = []

def get_ld_json(url: str) -> dict:
    parser = "html.parser"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, parser)
    return soup


for comunidad in comunidadesListado:
    try:
        url = 'https://spreadsheets.google.com/feeds/cells/1Yw0xLEMyDudD-qI4oJKThF4CLL1UrigiMon6IFUphes/' + str(comunidad["pagina_id"]) + '/public/full?alt=json'
        data = get_ld_json(url)
        datastr = data.text
        datajson = json.loads(datastr)
        itemsComunidad = []
        for item in datajson['feed']['entry']:
            # Para omitir el titulo del spreadsheet:
            if item['content']['$t'] == 'id_producto':
                continue
            # print(item['gs$cell']['inputValue'])
            itemsComunidad.append(str(item['gs$cell']['inputValue']))
        # Agregar la lista de ids a la data de cada comunidad.
        comunidad['data'] = itemsComunidad
    except:
        print("Error al intentar traer datos de id por comunidad de los spreadsheets.")
    

#FEED GENERAL petición de datos con requests:
req = requests.get(generalFeed)

soupGeneralFeed = BeautifulSoup(req.text, "xml")

# tag comunidad que se agrega a cada Product
comunidad = soupGeneralFeed.new_tag("Comunidad")
peso = soupGeneralFeed.new_tag("Peso_prod")
# comunidad.string = "Madrid"

tagProductos = soupGeneralFeed.find_all('Product')

productosFiltrados = []


print("===================================")
# Abrir un nuevo documento XML para guardar todos los productos
file = open("prods.xml", 'wb')
file.write('<?xml version="1.0" encoding="UTF-8"?><Products>'.encode())

def filtrador(comunidadData, comunidadNombre):
    try:
        for producto in tagProductos:
            # print(producto.Brand) # imprime <Brand>QUECHUA</Brand>
            # pid = str(producto.Product_ID.get_text())
            modelid = str(producto.Modelid.get_text())

            if modelid in comunidadData:
                comunidad.string = comunidadNombre
                peso.string = '15'
                producto.append(comunidad)
                producto.append(peso)
                
                productosFiltrados.append(producto)
                file.write(str(producto).encode())
    except:
        print("Error al filtrar los model ids por cada comunidad.")


for c in comunidadesListado:
    # print(c['nombre'])
    # print(c['data'])
    # print(len(c['data']))
    # print('---------')
    try:
        # Ejecutar la funcion que filtra los productos con cada lista de productos comunitaria:
        filtrador(c['data'], c['nombre'])
    except:
        print("Error en el loop de ejecución de filtrado por CCAA.")


file.write('</Products>'.encode())
file.close()
if file.closed:
    print("Archivo guardado.")