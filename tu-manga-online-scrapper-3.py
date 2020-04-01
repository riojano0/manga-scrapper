import os
import cfscrape
import requests
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    print ("######################################################")
    print ("Welcome, introduce the url, take care of all the parts (include the http or https)")
    print ("url example: https://www.tumangaonline.com/lector/Akatsuki-no-Yona/8720/1.00/108")
    print ("Leave blank for exit")
    print ("######################################################")

    while True:
        url = input('-------------------\nEnter chapter url: ')
        if len(url) < 1: break

        http, empty, page, string, serie, id_manga, id_chapter, id_scanlation = url.split("/")
        api = "https://www.tumangaonline.com/api/v1/imagenes?idManga={}&idScanlation={}&numeroCapitulo={}".format(
            id_manga,
            id_scanlation,
            id_chapter)
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.tumangaonline.com/",
            "X-Requested-With": "XMLHttpRequest",
            "Cache-mode": "no-cache"
        }
        json_response = json.loads(requests.get(api, headers=headers).content)
        images = json.loads(json_response['imagenes'])

        def download_image(image_response, image_number):
            path_directory = "{}/Downloads/{}/{}/".format(SCRIPT_DIR, serie, "%03d" % (float(id_chapter),))
            file_name = "{}.png".format("img-" + "%03d" % (image_number,))
            if image_response.status_code == 200:
                if not os.path.exists(path_directory):
                    os.makedirs(path_directory)
                with open(path_directory + file_name, 'wb') as out_file:
                    for data in image_response:
                        out_file.write(data)
                    print (path_directory)
                    print (file_name)
            else:
                print (image_response.status_code)

        counter = 0
        scrape = cfscrape.create_scraper()
        for image in images:
            image_target = "https://img1.tumangaonline.com/subidas/{}/{}/{}/{}".format(id_manga, id_chapter,
                                                                                       id_scanlation,
                                                                                       image)
            download_image(scrape.get(image_target), counter)
            counter += 1


if __name__ == "__main__":
    main()
