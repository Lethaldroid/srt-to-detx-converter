''' srt format is:
1
00:01:18,287 --> 00:01:22,212
<i>Get ready for the feel,
the feel of real. X1 .</i>

2
00:01:22,374 --> 00:01:24,126
<i>No pain, no gain.</i>

'''
#opening the subtitles file and reading it into a variable
sub_file = open('sub.srt', mode = 'r', errors="ignore")
Lines = sub_file.readlines()

#removing all empty lines from the file
try:
    while True:
        Lines.remove("\n")
except ValueError:
    pass

#removing block numbers
for i in range(len(Lines)):
    try:
        tmp = int(Lines[i])
        Lines.remove(Lines[i])
    except:
        pass

#concatenating a dialouge on multiple lines into a single index        
temp = []

for i in range(len(Lines)):
    if(Lines[i][0] == '0'):
        if(len(temp)>0):
            Lines[i-1] = " ".join(temp)
            temp=[]
        continue
    else:
        temp.append(Lines[i].strip())       
        Lines[i] = " "
Lines[len(Lines)-1]=temp[0]

#removing indices with blank spaces        
try:
    while True:
        Lines.remove(" ")
except ValueError:
    pass


#dividing the time of subtitles and dialogues into different lists
time=[]
dialogue=[]

for i in range(len(Lines)):
    if(i%2==0):
        time.append(Lines[i])
        time[i//2] = time[i//2].strip()
    else:
        dialogue.append(Lines[i])
del Lines


dialogue = [s.replace("<i>", "") for s in dialogue]
dialogue = [s.replace("</i>", "") for s in dialogue]

#splitting the time into start and ending time and formatting it
for i in range(len(time)):
    start_time_millis = 0
    end_time_millis = 0
    start_timestamp = ""
    end_timestamp = ""
    
    time[i] = time[i].replace("-->","")
    time[i] = time[i].replace(",",":")
    time[i] = time[i].split("  ")
    
    start_timestamp = time[i][0]
    end_timestamp = time[i][1]
    start_time_millis = int(time[i][0][-3:]) // 10
    end_time_millis = int(time[i][1][-3:]) // 10
    time[i][0] = start_timestamp[0:-3] + str(start_time_millis)
    time[i][1] = end_timestamp[0:-3] + str(end_time_millis)

#variables and custom strings for .detx
last_position = time[len(time)-1][1]    
char_name = "Lucas"
lines=[]

meta_start = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<detx copyright="Chinkel S.A., 2007-2022">'''

meta_end = '''
  </body>

</detx>'''

header = f'''
   <header>
        <cappella version="3.7.0"/>
        <last_position timecode=\"{last_position}\" track="0"/>
    </header>'''
    
roles = f'''
    <roles>
    <role color="#000000" description="" id=\"{char_name}\" name=\"{char_name}\"/>
  </roles>

  <body>'''
  
track=0
for i in range(len(time)):
    if(track%3==0):
        track=0
    lines.append(f'''
    <line role="{char_name}" track="{track}">
      <lipsync timecode="{time[i][0]}" type="in_open"/>
      <text>{dialogue[i]}</text>
      <lipsync timecode="{time[i][1]}" type="out_open"/>
    </line>
    ''')
    track+=1

detx_file = open('sub.detx', 'w')
detx_file.writelines(meta_start)
detx_file.writelines(header)
detx_file.writelines(roles)
for i in range(len(lines)):
    detx_file.writelines(lines[i])
detx_file.writelines(meta_end)
detx_file.close()

