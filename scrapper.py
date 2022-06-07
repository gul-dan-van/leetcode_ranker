contest = '-'.join('Weekly Contest 295'.lower().split())
users = users=['wif', 'wifiii','hongrock']
total_participants = 10
sleep_time_bw_users = 0


class Participant:
    def __init__(self,name,participated=False, rank=None,x=total_participants):
        self.name = name
        self.participated = participated
        self.rank=rank
        self.score=None
        if self.rank!=None:
            self.calcScore(total_participants)

############################################################################## CALCULATE SCORE
    def calcScore(self, x):
        self.score = 80*(x-self.rank)/x
############################################################################## CALCULATE SCORE

    def __str__(self):
        s=f'Name: {self.name}\n'
        if self.participated:
            s+=f'Rank: {self.rank}\n'
        else:
            s+='Participant did not participated in the contest\n'

        return s

participants = []        

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os

CWD = os.getcwd()
DRIVER_PATH = "C:\\Program Files (x86)\\chromedriver.exe"
URL = r"https://fatminmin.com/leetcode-ranking-search/contest/"+contest

# Creating an instance of chromedriver
options = Options()
options.add_argument("--diable-extensions")
options.add_argument("--headless")
driver = webdriver.Chrome(DRIVER_PATH, options=options)
driver.get(URL) # Getting the website at the formated url
time.sleep(5)

for user in users:

    searchBox = driver.find_element_by_id('__BVID__11')
    searchBox.clear()
    searchBox.send_keys(user)
    searchBox.send_keys(Keys.ENTER)
    time.sleep(sleep_time_bw_users)

    table=driver.find_element_by_tag_name('tbody')
    rows=table.find_elements_by_tag_name('tr')
    if len(rows)==0:
        participants+=[Participant(user)]
        continue

    cols = rows[0].find_elements_by_xpath('./*')
    text = [col.text for col in cols]
    participants += [Participant(user, True, int(text[0]))]


print()
print(*participants, sep='\n')

import pandas as pd

data = {
    'Name':[],
    'Participated':[],
    'Rank':[],
    'Score':[]
}
for p in participants:
    data['Name']+=[p.name]
    data['Participated']+=[['NO','YES'][p.participated]]
    data['Rank']+=[p.rank]
    data['Score']+=[p.score]

df = pd.DataFrame(data)
df.to_csv('Results.csv')

driver.quit()