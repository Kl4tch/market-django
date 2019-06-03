import requests

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from bs4 import BeautifulSoup

from market.models import Brand
from scraper.models import *
from market.models import *
requests.packages.urllib3.disable_warnings()


def scrapeR():
    # сразу единственными запросоми создаем массив строк из существующих загововков, групп и тд
    # так как у нас 1 поток всего скрипта - самое оптимальное решение
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
        titleSource = soup.find_all('h2', 'h1 ng-star-inserted')
        titleSource = str(titleSource[0])
        i1 = titleSource.find('>')+1
        i2 = titleSource.find('</h2>')

        # в розетке плюшки при покупки к некоторым товарам
        # указываются в названии через "+ ...", отсекаем это
        plusInd = titleSource.find(' + ')

        if plusInd != -1:
            return titleSource[i1: plusInd-1]
        else:
            return titleSource[i1:i2]

    def getBrand(title):
        stringBrand = title.split()[0]
        if stringBrand not in stringsBrands:
            brand = Brand(name=stringBrand)
            brand.save()
            stringsBrands.append(stringBrand)
        else:
            brand = Brand.objects.get(name=stringBrand)

        return brand

    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)"}

    # url = "https://rozetka.com.ua/mobile-phones/c80003/"
    url = "https://rozetka.com.ua/headphones/c80027/page=2/"
    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, "html.parser")

    titles = soup.find_all('div', {'class':'g-i-tile-i-title clearfix'})
    titlesS = []

    for i in titles:
        titlesS.append(str(i))

    itemsMainUrls = []

    for i1 in titlesS:
        a = i1.find("href")
        a1 = i1.find('"', a)+1
        a2 = i1.find('"', a1+1)
        link = i1[a1:a2]
        print(f"{link}")
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

            # в душе не ебу откуда тут так много комментов ПУСТЫХ, пока убираю
            buf = buf.replace('<!-- -->', '')
            tableRawsString.append(buf)

        def getItem():
            if title not in stringsItems:
                newItem = Item(title=title, category=Category.objects.get(name='Наушники'),
                       brand=getBrand(title), text='fd')
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

                print('TEST228  = ' + imageUrl)

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
                else:
                    bigGroup = GroupTitle.objects.get(title="(пустышка)")   # костыль, продумать надо
            else:
                bigGroup = GroupTitle.objects.get(title="(пустышка)")  # костыль, продумать надо


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
                        print(value + " (" + attributeTitle.attr + ')')
                    else:
                        a3 = i.find('>', a + 1) + 1
                        a4 = i.find('<', a3)

                        value = i[a3:a4]

                        obsh = a4

                        k = i.find("feature-value features-full-view ng-star-inserted", obsh)


                    print("TEST ERROR:" + "value = " + value + ", titile = " +  attributeTitle.attr)
                    if [value, attributeTitle.attr, attributeTitle.bigTitle.title] not in stringsAttributeValue:
                        print('new AtributeValue: ' + value)
                        attributeTitleObject = AttributeValue(value=value, attributeTitle=attributeTitle)
                        attributeTitleObject.save()
                        stringsAttributeValue.append([value, attributeTitle.attr, attributeTitle.bigTitle.title])
                        stringsAttributeValue.append([value, attributeTitle.attr, attributeTitle.bigTitle.title])
                    else:
                        print('old AtributeValue' + value + " - " + attributeTitle.attr)
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


scrapeR()
