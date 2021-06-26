import requests, bs4, openpyxl, re

libUrl = 'https://prjctr.online/library'
mainUrl = 'https://prjctr.online'
pageNum = 1
doc = open('test.txt', 'w')

def skipBlank(text):
    regex = re.compile(r'''\S.+''')
    matchObject = regex.search(text)
    if matchObject != None:
        newText = matchObject.group()
    else:
        newText = 'None'
    return newText

print(f'reading page # {pageNum}')
res = requests.get(libUrl)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
lectureUrl = soup.select('.card__link')
for i in range(len(lectureUrl)):
    lectureRes = requests.get(mainUrl + lectureUrl[i].get('href'))
    lectureRes.raise_for_status()
    lectureSoup = bs4.BeautifulSoup(lectureRes.text, 'html.parser')

    lectureTitle = lectureSoup.select('.video-content__title')
    lectureSpeaker = lectureSoup.select('p > a.link')
    lectureSpeakerCompany = lectureSoup.select('p > a:nth-child(2)')
    # lectureSpeakerCompanyLink get href instead of text
    lectureSpeakerWhoIs = lectureSoup.select('#content > section.video-content > p')

    doc.write('\n Title: ' + skipBlank(lectureTitle[0].getText()) +
              '\n Speaker: ' + skipBlank(lectureSpeaker[0].getText()) +
              '\n Speaker Company: ' + skipBlank(lectureSpeakerCompany[0].getText()) +
              '\n Speaker Company Link: ' + skipBlank(lectureSpeakerCompany[0].get('href')) +
              '\n Who is Speaker: ' + skipBlank(lectureSpeakerWhoIs[0].getText()) + '\n'
              )

doc.close()