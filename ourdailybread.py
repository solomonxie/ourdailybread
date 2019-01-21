# Python3
# -*- coding: utf-8 -*-

"""
File: ourdailybread.py
Author: Solomon Xie
Email: solomonxiewise@gmail.com
Github: https://github.com/solomonxie
Description: 
    A simple script to scrap Our Daily Bread article of today,
    and would be used to send email to myself.
Workflow:
    - [x] Scrap odb.org and download today's content
    - [ ] Scrap the bible verses cited in the content from Biblegateway.com
    - [x] Organize contents to form a Markdown file
    - [ ] Save file and store at a folder for `crontab`
"""

import json
import requests
from bs4 import BeautifulSoup

from sendemail import Email
from biblegateway import BibleGateway

def main():
    odb = OurDailyBread()
    odb.save('./dataset/odb.md')
    odb.sendmail('/Volumes/SD/Workspace/etc/email.json', ['solomonxie@outlook.com'])
    

class OurDailyBread:
    """
    A class for an article from today's odb.org content.  
    """

    def __init__(self):
        self.url = 'https://odb.org'
        self.path = ''
        self.title = ''
        self.date = ''
        self.thumbnail = ''
        self.scripture = ''
        self.scripture_link = ''
        self.readbible = ''
        self.bible_link = ''
        self.verses = ''
        self.devotion = ''
        self.poem = ''
        self.thought = ''
        self.insight = ''
        self.markdown = ''
        self.html = ''

        self.fetch()

    def fetch(self):
        """TODO: fetch contents from odb.org
        :returns: Nothing. But composes markdown value of this instance.
        """
        print('Fetching Our daily bread...')
        #r = requests.get(self.url)
        #soup = BeautifulSoup(r.content, 'html5lib')
        print('OK.')

        with open('./dataset/odb.org.html', 'r') as f:
            soup = BeautifulSoup(f.read(), 'html5lib')

        # Parse contents
        self.title = soup.find('h2', attrs={'class': 'entry-title'}).get_text()
        self.date = soup.find('a', attrs={'class': 'calendar-toggle'}).get_text()
        self.thumbnail = soup.find('img', attrs={'class': 'post-thumbnail'})['src']
        self.verses = soup.find('div', attrs={'class': 'verse-box'}).get_text()
        self.devotion = soup.find('div', attrs={'class': 'post-content'}).get_text().strip()
        self.poem = soup.find('div', attrs={'class': 'poem-box'}).get_text().strip()
        self.thought = soup.find('div', attrs={'class': 'thought-box'}).get_text().strip()
        self.insight = soup.find('div', attrs={'class': 'insight-box'}).p.get_text().strip()
        self.scripture = self.fetch_bible(soup.find('div', attrs={'class': 'passage-box'}))

        body = '# %s (Our daily bread)\n**%s**\n> Verses: %s\n![thumbnail](%s)\n'\
                +'## Content\n%s\n%s\n%s\n## Scripture\n%s\n## INSIGHT\n> %s'
        self.markdown = body % (self.title, self.date,self.verses,self.thumbnail, \
            self.devotion, self.poem, self.thought, self.scripture, self.insight)
        
        # convert markdown to html format
        #self.html = ''
        with open('./dataset/out.html', 'r') as f:
            self.html = f.read()

        
    def fetch_bible(self, tag):
        """TODO: Fetch scriptures from Biblegateway.com
        :tag: ElementTag instance of BeautifulSoup, as the target tag includes scriptures
        :type: returns string
        :returns: Scripture content
        """

        links = tag.find_all('a')
        content = 'Read: [%s](%s) | Bible in a Year: [%s](%s)'\
                %(links[0].get_text(), links[0]['href'], links[1].get_text(), links[1]['href'])

        #bible = BibleGateway(links[0]['href'])

        return content


    def save(self, path):
        """TODO: Docstring for save.
        :returns: TODO
        """
        with open(path, 'w') as f:
            f.write(self.markdown)
        print('Saved markdown file.')

    
    def sendmail(self, path, recipients):
        """TODO: Docstring for sendmail.
        :path: String, A local JSON file including mail server info 
        :recipients: List, email recipients list
        :returns: None.
        """
        # create email instance
        mail = Email(path)
        # make Email body
        subject = self.title
        content = self.html
        # send mail
        mail.send(subject, content, recipients)



if __name__ == "__main__":
    main()
