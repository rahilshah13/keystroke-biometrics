from pynput import keyboard
import time, sys, csv, pickle

buff = ''

# downbuff contains timestamps of each time a key is pressed
# upbuff contains timestamps of each time a key is released
# deltadown contains the amount of time each key is pressed down
# deltaup contains the amount of time between key presses
# timedownbuff contains values for total time elapsed from when the first key was pressed down to when a key is pressed
# timeupbuff contains values for total time elapsed from the when the first key was pressed to when a key is released
downbuff, upbuff, deltadown, deltaup, timedownbuff, timeupbuff, = [],[], [], [], [], []


start = time.time()
point_temp, index = [], []
first, count, trial = 0, 0, 0

#change value to save data to different file
filename = 'training.csv'

#change value of password to desired value for data collection
password = '4wordsalllowercase'

#change value of user depending on who is providing data
user = 'rahil'



def save_output():
    i = 0;
    global deltaup, deltadown, upbuff, downbuff, buff, timedownbuff, timeupbuff
    text = ''
    try:
        with open(filename, 'r') as csvfile:
            mycsv = csv.reader(csvfile)
            for row in mycsv:
                text = row[0]
    except:
        print('creating file')
    #############################################
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['char', 'deltaup', 'deltadown', 'downtime', 'uptime', 'char_index', 'user']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print("successful attempt")
        #comment next 2 lines out if file exists
        if str(text.split(',')[0]) == '':
            writer.writeheader()

        for down, up in zip(deltadown, deltaup):
            writer.writerow({'char': ''.join(buff[i]), 'deltaup': ''.join(str(up)), 'deltadown': ''.join(str(down)),
                             'uptime': ''.join(str(timeupbuff[i])), 'downtime': ''.join(str(timedownbuff[i])),
                             'char_index': str(i%18), 'user': user})
            i += 1
        print('')


def calculate_delta():
    global deltaup, deltadown, upbuff, downbuff

    i = 0
    deltaup.append(0)
    while (i < len(downbuff)):
        deltadown.append(upbuff[i] - downbuff[i])
        i += 1
    i = 1
    while (i < len(downbuff)):
        deltaup.append(upbuff[i] - downbuff[i - 1])
        i += 1


def on_key_release(key):
    global password,upbuff,buff,downbuff,deltadown,deltaup,timeupbuff,timedownbuff,point_temp,index,clf,start,first,trial

    key = str(key).replace('u\'', '', 1).replace('\'', '')
    if str(key) != 'Key.enter':
        upbuff.append(time.time())
        buff += key
        timeupbuff.append(time.time() - start)

    if(buff not in password):
        print("Password Typed Incorrectly")
        buff = ""
        downbuff, upbuff, deltadown, deltaup = [], [], [], []
        first = 0
        timedownbuff, timeupbuff, point_temp, index = [], [], [], []

    if buff == password:
        print("")
        calculate_delta()
        save_output()
        buff=""
        downbuff, upbuff, deltadown, deltaup = [], [], [], []
        first = 0
        timedownbuff, timeupbuff, point_temp, index = [], [], [], []
        trial +=1

        if(trial==10):
            sys.exit(0)


def on_key_press(key):
    global buff, upbuff, start_time, downbuff, deltadown, deltaup, start, first, timedownbuff, count

    key = str(key).replace('u\'', '', 1).replace('\'', '')
    print(key)

    # if (key == "Key.esc"):
    #     calculate_delta()
    #     save_output()
    #     print(''.join(str(deltadown)))
    #     print(''.join(str(deltaup)))
    #     print(buff)
    #     sys.exit(0)

    if (first == 0):
        first = 1
        start = time.time()
        timedownbuff.append(0)

    else:
        timedownbuff.append(time.time() - start)

    downbuff.append(time.time())
    index.append(count)
    count += 1
# buff += key

with keyboard.Listener(on_release=on_key_release, on_press=on_key_press) as listener:
    listener.join()