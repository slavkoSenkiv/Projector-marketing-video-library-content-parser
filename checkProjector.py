import requests, bs4, openpyxl

def skipBlank(text):
    return ' '.join(text.split())

lectureNum = 1
wb = openpyxl.Workbook()
sheet = wb.active
mainUrl = 'https://prjctr.online'
libUrl = 'https://prjctr.online/library'

for pageNum in range(2, 17): #290 lectures = 17 pages
    print(libUrl)
    res = requests.get(libUrl)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    lectureUrl = soup.select('.card__link')

    for i in range(len(lectureUrl)):
        lectureRes = requests.get(mainUrl + lectureUrl[i].get('href'))
        print(f'page # {pageNum-1}, lecture # {lectureNum}: ' + mainUrl + lectureUrl[i].get('href'))
        lectureRes.raise_for_status()
        lectureSoup = bs4.BeautifulSoup(lectureRes.text, 'html.parser')

        lectureTitle = lectureSoup.select('.video-content__title')
        lectureSpeaker = lectureSoup.select('#content > section.video-content > p')
        lectureDescription = lectureSoup.select('#content > section.video-content > div.video-content__inner > div > div.video-content__info-block > article')
        lectureTags = lectureSoup.select('#content > section.video-content > div.video-content__inner > div > div.video-content__tags.tags > ul')

        sheet.cell(row=lectureNum+1, column=1).value = skipBlank(lectureTitle[0].getText())
        sheet.cell(row=lectureNum+1, column=2).value = mainUrl + lectureUrl[i].get('href')
        sheet.cell(row=lectureNum+1, column=3).value = skipBlank(lectureTags[0].getText())
        sheet.cell(row=lectureNum+1, column=4).value = skipBlank(lectureSpeaker[0].getText())
        sheet.cell(row=lectureNum+1, column=5).value = skipBlank(lectureDescription[0].getText())

        lectureNum += 1
    libUrl = mainUrl + f'/library?page={str(pageNum)}'

wb.save('projector.xlsx')
print('Done')