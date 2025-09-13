import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np
import json

SCALE="linear"#log/symlog

with open("data.json", "r") as f:
    data :dict= json.load(f)

#kinda unnecessary (only for MONTHLY_INTERVAL)
start_date_str:str=list(data.keys())[0] 
start_date:int=int(datetime(int(start_date_str.split("-")[0]), int(start_date_str.split("-")[1]), int(start_date_str.split("-")[2])).timestamp())
end_date_str:str=list(data.keys())[-1] 
end_date:int=int(datetime(int(end_date_str.split("-")[0]), int(end_date_str.split("-")[1]), int(end_date_str.split("-")[2])).timestamp())
months = int((((end_date-start_date)/3600)/24)/30)
MONTHLY_INTERVAL=int(months/10)


dates = [int(datetime(int(datum_.split("-")[0]), int(datum_.split("-")[1]), int(datum_.split("-")[2])).timestamp())*1 for datum_ in list(data.keys())]

data2=[]
for datum in data:
    data2.append(int(sum(data[datum]))/60)#/60 for minutes

dates2 = np.array(dates, dtype='datetime64[s]')

plt.plot(dates2, data2, label='Playtime', linewidth=1)

plt.yscale(SCALE)

plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=MONTHLY_INTERVAL))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gcf().autofmt_xdate()

plt.xlabel('Time')
plt.ylabel('Playtime (minutes)')
plt.title('Playtime Over Time')
plt.legend()
plt.show()