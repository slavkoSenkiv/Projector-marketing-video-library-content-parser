import requests, bs4, openpyxl, re

libUrl = 'https://prjctr.online/library'
mainUrl = 'https://prjctr.online'
pageNum = 1
doc = open('test.txt', 'w')

def skipBlank(text):
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text.strip()

print(f'reading page # {pageNum}')
res = requests.get(libUrl)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
lectureUrl = soup.select('.card__link')
for i in range(len(lectureUrl)):
    lectureRes = requests.get(mainUrl + lectureUrl[i].get('href'))
    print('handling with ' + mainUrl + lectureUrl[i].get('href'))
    lectureRes.raise_for_status()
    lectureSoup = bs4.BeautifulSoup(lectureRes.text, 'html.parser')

    lectureTitle = lectureSoup.select('.video-content__title')
    lectureSpeaker = lectureSoup.select('#content > section.video-content > p')

    doc.write('\n Title: ' + skipBlank(lectureTitle[0].getText()) +
              '\n Speaker: ' + skipBlank(lectureSpeaker[0].getText() + '\n')
              )

doc.close()