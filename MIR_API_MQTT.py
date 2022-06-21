

##MIR with MQTT test V1.0
##For Hai Robotic
##10_6_2022
##William Tiu


##----------
#sudo apt update
#sudo apt install python3-pip
#pip install paho-mqtt
#pip install  requests

##--REF--##
#How to use MQTT in Python (Paho)
#https://emqx.medium.com/how-to-use-mqtt-in-python-paho-4e622cb359f9





##------------------Program Start----------##

from tkinter import * ##UI
import tkinter as tk ##UI
from tkinter import messagebox
import requests, json
import threading
import time
import paho.mqtt.client as mqtt ##MQTT
import random
import json  
import datetime

##Setting

##-----------------MIR Setting ------------------##

##Robot ip and key setting
Mir_ip = '192.168.0.232'
Mir_host = 'http://'+ Mir_ip + '/api/v2.0.0/'
Check_status=0
Check_thread_start=0

##---Def -----##


#Hello World test
def test() :
    #myStatus = requests.get(Mir_host+'status', headers = headers)
    #statustext = myStatus.json()
    #End_Function(MQTT_Sub_Top[0])
    client.publish("Station_1/Task","come",0)
    End_Function('Hello World!')

#Get Missiion ID
def GetID() :
    mymission = requests.get(Mir_host + 'missions' , headers = headers)
    End_Function(mymission.text)

#Clear text
def Text_Clear() :
    mylistbox.delete(0,tk.END)
    mylistbox1.delete(0,tk.END)
    End_Function('Text Clear')

#End function
def End_Function(myfunction) :
    try:
        print(myfunction)
        mylistbox.insert(tk.END, str((time.strftime('%H:%M:%S: ')) + str(myfunction)))
        mylistbox.yview(tk.END)
    except:
        print("Error")
    return


##--MIR----##

##-----------------MIR Mission------------------------##
headers = {
    'Content-Type': "application/json",
    'Accept-Language': "en_US",
    'Authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
    'Host':Mir_ip + ":8080",
    'Connection': "keep-alive",
    'Cache-Control': "no-cache"
}

##Function
#Add Mission API 1
def post_mission_1 ():
   missions_id = {"mission_id": "5b2a609b-cb46-11ec-ae87-00012978ed77"}
   post_mission = requests.post(Mir_host+'mission_queue',json=missions_id, headers = headers)
   End_Function(post_mission)
   return

#Add Mission API 2
def post_mission_2 ():
   missions_id = {"mission_id": "e28731b1-cb58-11ec-ae87-00012978ed77"}
   post_mission = requests.post(Mir_host+'mission_queue',json=missions_id, headers = headers)
   End_Function(post_mission)
   return

#Mission Delete
def delete_quene ():
    delete =requests.delete(Mir_host+'mission_queue',headers = headers)
    End_Function(delete_quene)
    return

def mythread ():
    global Check_status
    while True:
        try:
        # print("Check_status")
        # if t.is_alive==False:
        #     t.run()
            myStatus = requests.get(Mir_host+'status', headers = headers)
            statustext = myStatus.json()
            mylistbox1.insert(tk.END, str((time.strftime('%H:%M:%S: '))+statustext["state_text"]))
            mylistbox1.yview(tk.END)
            client.publish("MIR_1/status",statustext["state_text"],0)
            time.sleep(0.5)
        except:
            print("Error")
        
        
t = threading.Thread(target = mythread)
t.start()


##-----------------------------MQTT-------------------------##

# 當地端程式連線伺服器得到回應時，要做的動作
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    if rc == 0:
            print("Connected to MQTT Broker!")
            global MQTT_Connected
            MQTT_Connected=True
            # 每次連線之後，重新設定訂閱主題
            client.subscribe(MQTT_Sub_Top)
            #client.subscribe("Try/MQTT")
    else:
            print("Failed to connect, return code %d\n", rc)
    return client
    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時 
    # 地端程式將會重新訂閱
#client.subscribe("Try/MQTT")

# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
    # 轉換編碼utf-8才看得懂中文
    data = msg.payload
    receive=data.decode("utf-8")
    print ("Message received: "  + str(receive))
    try:
        if msg.topic =='Station_1/Task':
            mylistbox_Station_1.insert(tk.END, str((time.strftime('%H:%M:%S: ')) + str(msg.payload.decode('utf-8'))))
            mylistbox.yview(tk.END)
        if msg.topic =='Station_2/Task':
            mylistbox_Station_2.insert(tk.END, str((time.strftime('%H:%M:%S: ')) + str(msg.payload.decode('utf-8'))))
            mylistbox.yview(tk.END)
        if msg.topic =='Station_3/Task':
            mylistbox_Station_3.insert(tk.END, str((time.strftime('%H:%M:%S: ')) + str(msg.payload.decode('utf-8'))))
            mylistbox.yview(tk.END)
        Mir_do(msg.topic,receive)
    except:
        print("Error")
    return

    End_Function("MQTT msg :" + msg.topic +":"+ msg.payload.decode('utf-8'))

## MIR to do##
def Mir_do(topic,recerive):
    if topic =='Station_1/Task':
        if recerive == 'come':
            post_mission_1 ()
            End_Function("Mir go to Station 1")
        elif recerive == 'back':
            post_mission_2 ()
            End_Function("Mir back to Station 1")
        else:
            End_Function("i donk not what to do")
    if topic =='Station_2/Task':
        if recerive == 'come':
            End_Function("Mir go to Station 2")
        elif recerive == 'back':
            End_Function("Mir back to Station 2")
        else:
            End_Function("i donk not what to do")
    if topic =='Station_3/Task':
        if recerive == 'come':
            End_Function("Mir go to Station 3")
        elif recerive == 'back':
            End_Function("Mir back to Station 3")
        else:
            End_Function("i donk not what to do")



def on_publish(client,userdata,result):             #create function for callback
    #client.publish("/Station_1/Task", "payload", 0)
    print("data published \n")
    pass

def MQTT_publish(client):
    print("HI")
    #  msg_count = 0
    #  while True:
    #      time.sleep(1)
    #      msg = f"messages: {msg_count}"
    #      result = client.publish(topic, msg)
    #      result: [0, 1]
    #      status = result[0]
    #      if status == 0:
    #          print(f"Send `{msg}` to topic `{topic}`")
    #      else:
    #          print(f"Failed to send message to topic {topic}")
    #      msg_count += 1


#MQTT multithreading subscribing
def MQTT_subscribing():
    client.on_message = on_message
    # 進入無窮處理迴圈
    client.loop_forever()


##MQTT---parameter##
client_id = f'python-mqtt-{random.randint(0, 1000)}'
MQTT_Connected=False
MQTT_ip ='192.168.0.188'
MQTT_timer=5
MQTT_User=""
MQTT_PW=""
MQTT_topic='Station_1/Task'
MQTT_Pub_msg='Test'
MQTT_Sub_Top=[("Station_1/Task",0),("Station_2/Task",0),("Station_3/Task",0)]


# 連線設定
# 初始化地端程式
client = mqtt.Client()

# 設定連線的動作
client.on_connect = on_connect

# 設定接收訊息的動作
client.on_message = on_message

client.on_publish = on_publish 


# 設定登入帳號密碼
client.username_pw_set(MQTT_User,MQTT_PW)



#設定連線資訊(IP, Port, 連線時間)
try:
    client.connect(MQTT_ip, 1883)
    print("OK")
except:
    print("NA")

#MQTT multithreading running
MQTT_sub=threading.Thread(target=MQTT_subscribing)
MQTT_sub.start()
     

##---------UI--------##
## Ref https://www.rs-online.com/designspark/python-tkinter-cn
##UI

def define_layout(obj, cols=1, rows=0):
    
    def method(trg, col, row):
        
        for c in range(cols):    
            trg.columnconfigure(c, weight=1)
        for r in range(rows):
            trg.rowconfigure(r, weight=1)

    if type(obj)==list:        
        [ method(trg, cols, rows) for trg in obj ]
    else:
        trg = obj
        method(trg, cols, rows)


win = tk.Tk()
#設定標題
win.title('MIR MQTT window')
#設定像素大小
win.geometry('1280x720')

#Grid編排
UI_div_size = 200
UI_align_mode = 'nswe'
pad = 5
#UI_div1 = tk.Frame(win,  width=UI_div_size , height=UI_div_size ,bg='blue')
UI_div2 = tk.Frame(win,  width=UI_div_size , height=UI_div_size,bg='yellow')
UI_div3 = tk.Frame(win,  width=UI_div_size, height=UI_div_size,bg='black')
UI_div4 = tk.Frame(win,  width=UI_div_size, height=UI_div_size ,bg='green')
UI_div5 = tk.Frame(win,  width=UI_div_size , height=UI_div_size,bg='orange' )

win.update()
win_size = min( win.winfo_width(), win.winfo_height())
print(win_size)

#UI_div1.grid(column=0, row=0, padx=pad, pady=pad, columnspan=3,sticky=UI_align_mode)
UI_div2.grid(column=0, row=0, padx=pad, pady=pad, sticky=UI_align_mode)
UI_div3.grid(column=1, row=0, padx=pad, pady=pad, sticky=UI_align_mode)
UI_div4.grid(column=2, row=0, padx=pad, pady=pad, sticky=UI_align_mode)
UI_div5.grid(column=0, row=1, padx=pad, pady=pad, sticky=UI_align_mode)
define_layout(win, cols=1, rows=1)
# define_layout(UI_div2, rows=10)
# define_layout(UI_div3, rows=1)
# define_layout(UI_div4, rows=1)
# define_layout(UI_div5, rows=5)
define_layout([UI_div2, UI_div3, UI_div4,UI_div5])



#button
#btn0 = tk.Label(UI_div1  , text="Test")
#btn0.grid(column=0, row=0, padx=pad, pady=pad, columnspan=3, sticky=UI_align_mode)

btn1 = tk.Button(UI_div2  , text="Mission 1" , command = post_mission_1)
btn1.grid(column=0, row=0, padx=pad, pady=pad, sticky=UI_align_mode)

btn2 = tk.Button(UI_div2  , text="Mission 2" , command = post_mission_2)
btn2.grid(column=0, row=1, padx=pad, pady=pad, sticky=UI_align_mode)

btn3 = tk.Button(UI_div2  , text="Delete" , command = delete_quene)
btn3.grid(column=0, row=2, padx=pad, pady=pad, sticky=UI_align_mode)

btn4 = tk.Button(UI_div2  , text="GetID" , command = GetID)
btn4.grid(column=0, row=3, padx=pad, pady=pad, sticky=UI_align_mode)

btn5 = tk.Button(UI_div2 , text="Test" , command = test)
btn5.grid(column=0, row=4, padx=pad, pady=pad, sticky=UI_align_mode)

btn6 = tk.Button(UI_div2, text="Clear" , command = Text_Clear)
btn6.grid(column=0, row=5, padx=pad, pady=pad, sticky=UI_align_mode)

btn7 = tk.Button(UI_div2, text="MQTT_PUB" , command = "MQTT_pub")
btn7.grid(column=0, row=6, padx=pad, pady=pad, sticky=UI_align_mode)

# btn8 = tk.Button(win , text="MQTT_Sub" , command = MQTT_Sub)
# btn8.place(x=10 ,y= 290)

##Textbox
Textbox_Label_1=tk.Label(UI_div5, text="Hello RUNOOB!")
Textbox_Label_1.grid(column=0, row=0, padx=pad, pady=pad,sticky=UI_align_mode)
TextBox_MIR_IP = tk.Entry (UI_div5)
TextBox_MIR_IP.grid(column=0, row=1, padx=pad, pady=pad,sticky=UI_align_mode)
Textbox_Label_2=tk.Label(UI_div5, text="Hello RUNOOB!")
Textbox_Label_2.grid(column=0, row=2, padx=pad, pady=pad,sticky=UI_align_mode)
TextBox_MQTT_IP = tk.Entry (UI_div5)
TextBox_MQTT_IP.grid(column=0, row=3, padx=pad, pady=pad,sticky=UI_align_mode)
Textbox_Label_3=tk.Label(UI_div5, text="Hello RUNOOB!")
Textbox_Label_3.grid(column=0, row=4, padx=pad, pady=pad,sticky=UI_align_mode)
TextBox_Data2 = tk.Entry (UI_div5)
TextBox_Data2.grid(column=0, row=5, padx=pad, pady=pad,sticky=UI_align_mode)


#listbox and scrollbar
scrollbar = tk.Scrollbar(UI_div3)
#scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
mylistbox = tk.Listbox(UI_div3,height = 20 ,width=45)
mylistbox.grid(column=0, row=0, padx=pad, pady=pad ,columnspan=3,sticky=UI_align_mode)
mylistbox_Station_1 = tk.Listbox(UI_div3,height = 10 ,width=15)
mylistbox_Station_1.grid(column=0, row=1,sticky=UI_align_mode)
mylistbox_Station_2 = tk.Listbox(UI_div3,height = 10 ,width=15)
mylistbox_Station_2.grid(column=1, row=1,sticky=UI_align_mode)
mylistbox_Station_3 = tk.Listbox(UI_div3,height = 10 ,width=15)
mylistbox_Station_3.grid(column=2, row=1,sticky=UI_align_mode)

mylistbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=mylistbox.yview)

mylistbox1 = tk.Listbox(UI_div4,height = 20 ,width=45)
mylistbox1.grid(column=0, row=0, padx=pad, pady=pad)
mylistbox1.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=mylistbox1.yview)


##----Bar---##

# def about():
#     messagebox.showinfo('MIR API MQTT Test ', 'This program is to test the MQTT and MIR')

# menubar = Menu(win)  
# file = Menu(menubar, tearoff=1, background='#ffcc99', foreground='black')  
# file.add_command(label="Set IP")  
# menubar.add_cascade(label="File", menu=file)  

# help = Menu(menubar, tearoff=0)  
# help.add_command(label="About", command=about)  
# menubar.add_cascade(label="Help", menu=help)  


# ##----UI Loop---#
# win.config(menu=menubar)
win.mainloop()




##--------------Dummy Code--------------##





##--------MQTT --- not in use
# client.loop_start()
# while MQTT_Connected!=True:
#     time.sleep(0.2)
# client.publish("Try/MQTT","Hello MQTT")
# client.loop_stop()
#client.loop_forever()
#client.on_disconnect = on_disconnect
#MQTT_pub=threading.Thread(target=MQTT_pub)
#MQTT_pub.start()

##------------------------------GUI-------------------##

# def mythread ():
#     global Check_status
#     while 1:
#         # print("Check_status")
#         # if t.is_alive==False:
#         #     t.run()
#         myStatus = requests.get(Mir_host+'status', headers = headers)
#         statustext = myStatus.json()
#         mylistbox1.insert(tk.END, str((time.strftime('%H:%M:%S: '))+statustext["state_text"]))
#         mylistbox1.yview(tk.END)
#         time.sleep(1)

# t = threading.Thread(target = mythread)
# t.start()




