# from jsonTolink import productId_extract
# import pymongo
# from decouple import config
# import time

# urls = []


# cliente = pymongo.MongoClient(config("MONGODB"))
# base_de_datos = cliente["shopstar"]
# coleccion = base_de_datos["links"]



# def web_to_jsonUrl(urls):

#     cliente = pymongo.MongoClient(config("MONGODB"))
#     base_de_datos = cliente["shopstar"]
#     coleccion = base_de_datos["json_link"]
#     for i in range (50):

#         for e in urls:
#             link1 = e+"&page="+str(i+1)
#             web = productId_extract(link1)

#             if web == "https://shopstar.pe/api/catalog_system/pub/products/search?":
#                  continue
           


#             # page = int(page)
#             lista = 1


#             # Crear un documento para MongoDB
#             documento = {
#                 "_id": link1,
#                 "category": link1,
#                 "lista": lista,
#                 "url": web,

#             }
      


#             # Utilizar update_one con upsert=True para evitar duplicados
#             coleccion.update_one(
#                 {"_id": link1},
#                 {"$set": documento},
#                 upsert=True
#             )





# webs = []
# documentos = coleccion.find()
# for documento in documentos:

#         # lista = documento["lista"]
#         url = documento["url"]

#         webs.append(url)

# web_to_jsonUrl(webs)






from jsonTolink import productId_extract
import pymongo
from decouple import config
from multiprocessing import Pool
import time

# Your existing code...

def process_url(url):

    cliente = pymongo.MongoClient(config("MONGODB"))
    base_de_datos = cliente["shopstar"]
    coleccion = base_de_datos["json_link"]

    for i in range(50):
        link1 = url + str(i + 1)

        print(link1)
  
        web = productId_extract(link1)

        if web == False:
            continue

        

        if web == "https://shopstar.pe/api/catalog_system/pub/products/search?":
            continue

        lista = 1
        documento = {
            "_id": link1,
            "category": link1,
            "lista": lista,
            "url": web,
        }

        coleccion.update_one(
            {"_id": link1},
            {"$set": documento},
            upsert=True
        )

def web_to_jsonUrl_parallel(urls):

   
    with Pool(processes=8) as pool:  # Adjust the number of processes as needed
        pool.map(process_url, urls)



# Rest of your code...
cliente = pymongo.MongoClient(config("MONGODB"))
base_de_datos = cliente["shopstar"]
coleccion = base_de_datos["links"]



if __name__ == '__main__':
    webs = []
    documentos = coleccion.find()
    for documento in documentos:
        url = documento["url"]
        webs.append(url)

    web_to_jsonUrl_parallel(webs)