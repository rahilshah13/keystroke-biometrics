from pynput import keyboard
import time, sys, pickle

buff = ''
downbuff, upbuff, deltadown, deltaup = [],[], [], []
start = time.time()
timedownbuff, timeupbuff, point_temp, index = [], [], [], []
first, k, h, count, trial = 0, 2, .02, 0, 0

#change value of password depending on password used in data collection
password = '4wordsalllowercase'

#change value of user depending on whose models are being tested
user = 'rahil'

#loads relevant classification models
def load_models():
    global clf_svm, clf_knn, clf_nt
    with open('svm2_rahil.pkl', 'rb') as input:
        clf_svm = pickle.load(input)
    with open('knn_rahil.pkl', 'rb') as input:
        clf_knn = pickle.load(input)
    with open('nt_rahil.pkl', 'rb') as input:
        clf_nt = pickle.load(input)

#calculates typing data from test attempt
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
    global clf_svm, clf_knn, clf_nt

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
        calculate_delta()
        load_models()
        for i in range(len(deltaup)):
            point_temp.append([deltaup[i], deltadown[i], index[i]])
        h1 = clf_svm.predict(point_temp)
        h2 = clf_nt.predict(point_temp)
        h3 = clf_knn.predict(point_temp)

        positive1, positive2, positive3 = 0, 0, 0
        for x in h1: positive1 += x
        for x in h2: positive2 += x
        for x in h3: positive3 += x

        percent_user1 = float(positive1) / float(len(h1))
        percent_user2 = float(positive2) / float(len(h2))
        percent_user3 = float(positive3) / float(len(h3))


        if percent_user1 > .50 or percent_user2 > .5 or percent_user3 > .5:
            print("Welcome User")
            print("You are " + str(percent_user1*100) + "% the user with SVM")
            print("You are " + str(percent_user2*100) + "% the user with NN")
            print("You are " + str(percent_user3*100) + "% the user with KNN")

        else:
            print("You're not the user")
            print("You are " + str(percent_user1*100) + "% the user with SVM")
            print("You are " + str(percent_user2*100) + "% the user with NN")
            print("You are " + str(percent_user3*100) + "% the user with KNN")

        sys.exit(0)


def on_key_press(key):
    global buff, upbuff, start_time, downbuff, deltadown, deltaup, start, first, timedownbuff, count

    key = str(key).replace('u\'', '', 1).replace('\'', '')
    print(key)

    if (key == "Key.esc"):
        calculate_delta()
        #		save_output()
        print(''.join(str(deltadown)))
        print(''.join(str(deltaup)))
        print(buff)
        sys.exit(0)

    if (first == 0):
        first = 1
        start = time.time()
        timedownbuff.append(0)
    else:
        timedownbuff.append(time.time() - start)
    downbuff.append(time.time())
    index.append(count)
    count += 1


with keyboard.Listener(on_release=on_key_release, on_press=on_key_press) as listener:
    listener.join()