import requests

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from bs4 import BeautifulSoup

from scraper.models import *
from market.models import *
from django.core.management.base import BaseCommand

requests.packages.urllib3.disable_warnings()


class Command(BaseCommand):

    URL = ""
    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='Начальная страница')
        parser.add_argument('category', type=str, help='В какую категорию добавлять товары')
        parser.add_argument('startPage', type=int, help='Страница, с которой начинаем')
        parser.add_argument('endPage', type=int, help='Страница, на которой заканиваем')

    def handle(self, *args, **kwargs):
        URL = kwargs['url']
        CATEGORY_NAME = kwargs['category']
        startPage = kwargs['startPage']
        endPage = kwargs['endPage']

        pages = []

        for i in range(startPage, endPage+1):
            pages.append(URL + "page=" + str(i) + "/")

        # сразу единственными запросоми создаем массив строк из существующих товаров, загововков, групп и тд
        # так как у нас 1 поток всего скрипта - самое оптимальное решение, чтобы каждый раз не делать перезапрос в бд
        def getAll():
            bigGroups = GroupTitle.objects.all()
            attributeTitle = AttributeTitle.objects.all()
            attributeValue = AttributeValue.objects.all()
            items = Item.objects.all()
            brands = Brand.objects.all()

            for i in items:
                stringsItems.append(i.title)

            for i in brands:
                stringsBrands.append(i.name)

            for i in bigGroups:
                stringsBigGroups.append(i.title)

            for i in attributeTitle:
                stringsAttributeTitle.append([i.attr, i.bigTitle.title])

            for i in attributeValue:
                stringsAttributeValue.append([i.value, i.attributeTitle.attr, i.attributeTitle.bigTitle.title])

        stringsBigGroups = []
        stringsAttributeTitle = []
        stringsAttributeValue = []
        stringsItems = []
        stringsBrands = []
        getAll()

        def getTitle():
            f = open('FINAL', 'w')
            f.write(str(soup))
            f.close()
            titleSource = soup.find_all('h2', 'detail-title h1')
            if len(titleSource) == 0:
                titleSource = soup.find_all('h2', 'h1 ng-star-inserted')
            titleSource = str(titleSource[0])
            i1 = titleSource.find('>')+1
            i2 = titleSource.find('</h2>')

            titleSource.replace('\n', '')
            titleSource.replace(' ', '')
            titleSource.replace('\n', '')

            # в розетке плюшки при покупки к некоторым товарам
            # указываются в названии через "+ ...", отсекаем это
            plusInd = titleSource.find(' + ')


            if plusInd == -1:
                t = titleSource[i1:i2]
            else:
                plus2Ind = titleSource.find(')', plusInd)
                if plus2Ind != -1:
                    t = titleSource[i1: plus2Ind+1]
                else:
                    t = titleSource[i1:plusInd]
            print("Title = " + t)
            return t

        # почти идеально работает, brand я вытаскиваю из script, в 1-5% почему-то его
        # там нет, вместо этого в название бренда будет часть кода html :(
        def getBrand():
            a = str(soup)

            ind = a.find("productVendorName")
            ind1 = a.find(':', ind) + 2
            ind2 = a.find('"', ind1)

            stringBrand = a[ind1:ind2]
            print("BRAND = " + stringBrand)

            if stringBrand not in stringsBrands:
                brand = Brand(name=stringBrand)
                brand.save()
                stringsBrands.append(stringBrand)
            else:
                brand = Brand.objects.get(name=stringBrand)

            return brand

        session = requests.Session()
        session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)"}

        for page in pages:

            content = session.get(page, verify=False).content

            soup = BeautifulSoup(content, "html.parser")

            titles = soup.find_all('div', {'class':'g-i-tile-i-title clearfix'})
            titlesS = []

            for i in titles:
                f = open('newTest.html', 'w')
                f.write(str(i))
                f.close()
                titlesS.append(str(i))

            itemsMainUrls = []

            for i1 in titlesS:
                a = i1.find("href")
                a1 = i1.find('"', a)+1
                a2 = i1.find('"', a1+1)
                link = i1[a1:a2]
                print(f"itemsMainUrl = {link}")
                itemsMainUrls.append(link)

            for itemMainUrl in itemsMainUrls:
                itemDetailsUrl = itemMainUrl + "characteristics/"
                content = session.get(itemDetailsUrl, verify=False).content

                soup = BeautifulSoup(content, "html.parser")

                title1 = soup.find_all('table')

                groups = soup.find_all('span', {'class':'feature-glossary-term ng-star-inserted'})
                # print(groups)
                # print("\nKol-vo атрибутов: " + str(len(groups)))

                attr = soup.find_all('tr', 'ng-star-inserted')

                tableRawsString = []

                title = getTitle()

                for i in attr:
                    buf = str(i)
                    # в розетке если в 1 группе несколько атрибутов - то они разделяются <br>
                    # это мешает для скрейпа + удобней мне если через ',' будет
                    buf = buf.replace('<br/>\n', ', ')

                    # в душе не ебу откуда тут так много комментов ПУСТЫХ, пока убираю - могут помешать при скрейпе
                    buf = buf.replace('<!-- -->', '')
                    tableRawsString.append(buf)

                def getItem():
                    if title not in stringsItems:
                        category, _ = Category.objects.get_or_create(name=CATEGORY_NAME)
                        newItem = Item(title=title, category=category, brand=getBrand(), text='fd', rozetkaUrl=itemMainUrl)
                        newItem.save()
                        stringsItems.append(title)
                        return newItem
                    else:
                        return Item.objects.get(title=title)

                newItem = getItem()

                def getImages(href):
                    content = session.get(href, verify=False).content
                    soup = BeautifulSoup(content, "html.parser")

                    pageString = str(soup)

                    # imagesHrefs = []
                    #
                    # ind = pageString.find('<script id="serverApp-state" type="application/json">')
                    #
                    # ind1 = pageString.find('https://i1.rozetka.ua/goods/', ind)
                    # ind2 = pageString.find('&q', ind1)

                    ind = pageString.find('https://i1.rozetka.ua/goods')

                    if ind!=-1:
                        ind2 = pageString.find('"', ind+1)

                        imageUrl = pageString[ind:ind2]

                        # print('TEST228  = ' + imageUrl)

                        r = requests.get(imageUrl)

                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(r.content)
                        img_temp.flush()

                        a = Image(item=newItem, position=0)
                        a.file.save(newItem.slug + ".jpg", File(img_temp), save=True)
                        a.save()

                    # imagesHrefs.append(a)

                    # print("TEST228: " + a + ", ind1 = " + str(ind) + ", ind2 = " + str(ind2) + ' (' + str(len(a)) + ')\n')

                    # while ind != -1:
                    #     ind = pageString.find('https://i1.rozetka.ua/goods/', ind)
                    #     ind2 = pageString.find('&q')
                    #
                    #     imagesHrefs.append(pageString[ind:ind2-1])
                    #
                    #     print("TEST228: " + pageString[ind:ind2-1] + ", ind1 = " + str(ind) + ", ind2 = " + str(ind2) + '\n')
                    #
                    #     ind = pageString.find('https://i1.rozetka.ua/goods/', ind2)
                    #
                    # for i in imagesHrefs:
                    #     print("TEST228: " + i)

                getImages(itemMainUrl)

                # print("NEW ITEM = " + newItem.title)

                for i in tableRawsString:
                    #GroupTitles
                    bigGroup = GroupTitle.objects.get(title="(пустышка)")  # костыль, продумать надо
                    isBigTitle = i.find("feature-group-title")
                    if isBigTitle != -1:
                        a = i.find('>', isBigTitle) + 1
                        a2 = i.find('<', a)
                        bigTitle = i[a:a2]
                        if (not bigTitle.isspace()) and (bigTitle != ''):
                            if bigTitle not in stringsBigGroups:
                                test = GroupTitle(title=bigTitle)
                                test.save()
                                stringsBigGroups.append(bigTitle)
                                bigGroup = GroupTitle.objects.get(title=bigTitle)
                            else:
                                bigGroup = GroupTitle.objects.get(title=bigTitle)


                    # atributesTitles
                    isTitle = i.find("pp-characteristics-title")
                    if isTitle != -1:
                        a = i.find("span")
                        a2 = i.find(">", a)+1
                        a3 = i.find("<", a2)
                        title = i[a2:a3]

                        if [title, bigGroup.title] not in stringsAttributeTitle:
                            # print('new: ' + title)
                            attributeTitle = AttributeTitle(attr=title, bigTitle=bigGroup)
                            attributeTitle.save()
                            stringsAttributeTitle.append([title, bigGroup.title])
                        else:
                            # print('old' + title)
                            attributeTitle = AttributeTitle.objects.get(attr=title, bigTitle=bigGroup)


                        # print("AtrTitleId = " + str(len(attributeTitle)))
                        # atributesValues
                        isAtributeValue = i.find("feature-value features-full-view ng-star-inserted")
                        if isAtributeValue != -1:
                            k = 0
                            obsh = 0
                            len1 = len("feature-value features-full-view ng-star-inserted")
                            while k != -1:
                                a = i.find("feature-value features-full-view ng-star-inserted", obsh)
                                a2 = i.find('ng-star-inserted', a+len1)

                                if (a2 != -1):
                                    a3 = i.find('>', a2+1) + 1
                                    a4 = i.find('<', a3)

                                    value = i[a3:a4]

                                    obsh = a4

                                    k = i.find("feature-value features-full-view ng-star-inserted", obsh)
                                    # print(value + " (" + attributeTitle.attr + ')')
                                else:
                                    a3 = i.find('>', a + 1) + 1
                                    a4 = i.find('<', a3)

                                    value = i[a3:a4]

                                    obsh = a4

                                    k = i.find("feature-value features-full-view ng-star-inserted", obsh)


                                # print("TEST ERROR:" + "value = " + value + ", titile = " +  attributeTitle.attr)
                                if [value, attributeTitle.attr, attributeTitle.bigTitle.title] not in stringsAttributeValue:
                                    # print('new AtributeValue: ' + value)
                                    attributeTitleObject = AttributeValue(value=value, attributeTitle=attributeTitle)
                                    attributeTitleObject.save()
                                    stringsAttributeValue.append([value, attributeTitle.attr, attributeTitle.bigTitle.title])
                                    stringsAttributeValue.append([value, attributeTitle.attr, attributeTitle.bigTitle.title])
                                else:
                                    # print('old AtributeValue' + value + " - " + attributeTitle.attr)
                                    attributeTitleObject = AttributeValue.objects.get(value=value, attributeTitle=attributeTitle)

                                a = ItemDetail(item=newItem, attr=attributeTitleObject)
                                a.save()



# def scrapeY():
#     session = requests.Session()
#     session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)"}
#
#     url = "https://market.yandex.ru/catalog--mobilnye-telefony/54726/list?hid=91491&onstock=1&local-offers-first=0"
#
#     proxy = {'http': 'http://84.51.77.30:4145'}
#
#     content = session.get(url, verify=False, proxies=proxy).content
#
#     items = soup.find_all('div', {'class':'n-snippet-cell2 i-bem b-zone b-spy-visible'})
#     print(soup)


