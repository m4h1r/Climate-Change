# importing libraries
import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
from matplotlib import pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

# Data Collecting
for yil in range(2015,2019):
  for ay in range(1,13):
    if ay==4 or ay==6 or ay==9 or ay==11:
      songun=31
    elif ay==2:
      songun=29
    else:
      songun=32
    for gun in range(1,songun):
      #print(str(yil)+"-"+str(ay)+"-"+str(gun))
      html = urlopen("https://tr.freemeteo.com/havadurumu/istanbul/history/monthly-history/?gid=745044&station=5328&month="+str(ay)+"&year="+str(yil)+"&language=turkish&country=turkey")
      bsObj = BeautifulSoup(html.read());
      GunB = bsObj.find('tr', {"data-day":gun})
      #Eğer tarih listede yoksa if komutu ile sorgulanıp pas geçme kodu.
      if GunB==None:
        print(str(gun)+"."+str(ay)+"."+str(yil)+" Tarihi pas geçildi.")
        continue
      #print(GunB)
      Tarih = ((GunB.find_all("td"))[0]).text
      Sicaklik = ((GunB.find_all("td"))[1]).text
      row = [Tarih, Sicaklik]
      with open('Istanbul.csv', 'a') as csvFile:
          writer = csv.writer(csvFile)
          writer.writerow(row)
      csvFile.close()
      print(str(gun)+"."+str(ay)+"."+str(yil))
print("İstenilen yıl sorunsuz indirildi.")

# importing data
df = pd.read_csv("Istanbul.csv", header=None, usecols=[0,1])

# cleaning data
df[1] = df[1].str.replace("°C", "")
df[1] = df[1].fillna(0)
df[1] = df[1].astype(np.int32)
df[0] = range(1, len(df[0])+1)
# df[0] = pd.to_datetime(df[0], format='%d.%m.%Y')

sns.set_style("whitegrid")

# Visualise the data
sns.lmplot(x="0", y="1", height=10, scatter_kws={"s": 5}, markers=["x"], data=df.rename(columns=lambda x: str(x)))
