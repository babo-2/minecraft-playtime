from datetime import datetime
import os, gzip, re, json

if False:#read data
    with open("data.json", "r") as f:
        data=json.load(f)
    total = 0
    for datum in data:
        total+=sum(data[datum])
    print("Playtime total:", str(round(total/3600, 0)) + "h")
    quit(1)

ALL_DATA={}

#default path    (all paths need an / at the end)
paths = ["C:/Users/" + os.getlogin() + "/AppData/Roaming/.minecraft/logs/"]

logs = [path + file_name for path in paths for file_name in os.listdir(path)]#convert relative paths to absolute paths
i=0
total_logs_amount=len(logs)
for log in logs:
    i+=1
    try:
        re_date=re.search(r'\d{4}-\d{2}-\d{2}', log)
        if not re_date:
            continue
        date:str=re_date.group(0)

        if log.endswith(".gz"):
            with gzip.open(log, 'rt') as gz_file:
                gz_file.seek(1)
                start_time = gz_file.read(8)
                if not re.search(r'\d{2}:\d{2}:\d{2}', start_time):
                    continue
                gz_file.seek(0, 2)
                block_size = 256
                blocks = []
                last_newline_pos = gz_file.tell()
                while last_newline_pos > 0:
                    read_size = min(block_size, last_newline_pos)
                    gz_file.seek(last_newline_pos - read_size)
                    data = gz_file.read(read_size)
                    last_newline_pos -= read_size
                    blocks += data
                    if '\n[' in data:
                        break
                matches = re.findall(r'\d{2}:\d{2}:\d{2}', ''.join(blocks))
                if not matches:
                    continue
                end_time:str=matches[-1]
        elif log.endswith(".log"):
            with open(log, 'rb') as f:
                f.seek(1)
                start_time = f.read(8).decode("latin-1")
                if not re.search(r'\d{2}:\d{2}:\d{2}', start_time):
                    continue
                f.seek(0, 2)
                block_size = 256
                blocks = []
                last_newline_pos = f.tell()
                while last_newline_pos > 0:
                    read_size = min(block_size, last_newline_pos)
                    f.seek(last_newline_pos - read_size)
                    data = f.read(read_size)
                    last_newline_pos -= read_size
                    blocks.insert(0, data)
                    if b'\n[' in data:
                        break
                matches = re.findall(r'\d{2}:\d{2}:\d{2}', b''.join(blocks).decode("latin-1"))
                if not matches:
                    continue
                end_time:str=matches[-1]
        else:
            continue

        year, month, day = int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2])
        start = datetime(year, month, day, int(start_time.split(":")[0]), int(start_time.split(":")[1]), int(start_time.split(":")[2])).timestamp()
        end = datetime(year, month, day, int(end_time.split(":")[0]), int(end_time.split(":")[1]), int(end_time.split(":")[2])).timestamp()
        if end-start<0:#this will not work if minecraft is open for 2 days or longer
            end += 3600*24

        lenght=end-start
        if date in ALL_DATA:
            ALL_DATA[date].append(lenght)
        else:
            ALL_DATA[date]=[lenght]
        print(str(round((i/total_logs_amount)*100, 2)) + "%")
    except Exception as e:
        print("[ERROR]:", e)
with open("data.json", "w") as f:
    json.dump(ALL_DATA, f)