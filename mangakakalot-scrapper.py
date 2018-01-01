import os
import cfscrape
from BeautifulSoup import *

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    print ("######################################################")
    print ("Welcome, introduce the url, take care of all the parts (include the http or https)")
    print ("url example: http://manganelo.com/chapter/yakusoku_no_neverland/chapter_2")
    print ("Leave blank for exit")
    print ("######################################################")

    while True:
        url = raw_input('-------------------\nEnter chapter url: ')
        if len(url) < 1: break
        http, empty, page, string, serie, chapter = url.split("/")

        scrape = cfscrape.create_scraper()
        html = scrape.get(url).content
        soup = BeautifulSoup(html)

        image_list = [tag.findAll('img') for tag in soup.findAll('div', id="vungdoc")]

        def download_image(image_response, image_number):
            path_directory = "{}/Downloads/{}/{}/".format(SCRIPT_DIR, serie, chapter)
            file_name = "{}.png".format("img-" + "%03d" % (image_number,))
            if image_response.status_code == 200:
                if not os.path.exists(path_directory):
                    os.makedirs(path_directory)
                with open(path_directory + file_name, 'wb') as out_file:
                    for data in image_response:
                        out_file.write(data)
                    print path_directory
                    print file_name
            else:
                print image_response.status_code

        counter = 0;
        for img in image_list[0]:
            download_image(scrape.get(img['src']), counter)
            counter += 1


if __name__ == "__main__":
    main()
