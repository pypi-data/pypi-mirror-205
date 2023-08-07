from time import sleep
import asyncio, os, sys, time, logging,json
from datetime import datetime

b = "\033[1;34m"
c = "\033[1;36m"
d = "\033[0m"
h = "\033[1;32m"
k = "\033[1;33m"
m = "\033[1;31m"
p = "\033[1;37m"
u = "\033[1;35m"
mm = "\033[101m\033[1;31m"
mp = "\033[101m\033[1;37m"
hp = "\033[1;7m"
n = "\n"

def Ascii_calvin(strings,versi):
    acssi = {"a" : ["┌─┐","├─┤","┴ ┴"],"b":["┌┐ ","├┴┐","└─┘"],"c":["┌─┐","│  ","└─┘"],"d":["┌┬┐"," ││","─┴┘"],"e":["┌─┐","├┤ ","└─┘"],"f" : ["┌─┐","├┤ ","└  "],"g":["┌─┐","│ ┬","└─┘"],"h":["┬ ┬","├─┤","┴ ┴"],"i":["┬","│","┴"],"j":[" ┬"," │","└┘"],"k":["┬┌─","├┴┐","┴ ┴"],"l" : ["┬  ","│  ","┴─┘"],"m":["┌┬┐","│││","┴ ┴"],"n":["┌┐┌","│││","┘└┘"],"o":["┌─┐","│ │","└─┘"],"p":["┌─┐","├─┘","┴  "],"q" : ["┌─┐ ","│─┼┐","└─┘└"],"r":["┬─┐","├┬┘","┴└─"],"s":["┌─┐","└─┐","└─┘"],"t":["┌┬┐"," │ "," ┴ "],"u":["┬ ┬","│ │","└─┘"],"v" : ["┬  ┬","└┐┌┘"," └┘ "],"w":["┬ ┬","│││","└┴┘"],"x":["─┐ ┬","┌┴┬┘","┴ └─"],"y":["┬ ┬","└┬┘"," ┴ "],"z":["┌─┐","┌─┘","└─┘"]}
    string = list(strings)
    for i in string:
        print(b+acssi[i][0],flush=True,end="")
    print(k+" versi "+m+": "+h+versi)
    for i in string:
        print(c+acssi[i][1],flush=True,end="")
    print(k+" status"+m+": "+h+"on")
    for i in string:
        print(p+acssi[i][2],flush=True,end="")
    print(n,flush=True,end="")

def Banner(title,versi):
    os.system('cls' if os.name=='nt' else 'clear')
    print(p+"─"*16+m+"> "+h+"Scrypt by "+p+"iewil"+m+" <"+p+"─"*15)
    Ascii_calvin(title,versi)
    Line()
    print(mm+"["+mp+"▶"+mm+"]"+d,flush=True,end="")
    print(p+" https://www.youtube.com/c/iewil")
    print(hp+" >_"+d,flush=True,end="")
    print(b+" Team-Function-INDO")
    Line()
    print(mm+"["+mp+"!"+mm+"]"+d,flush=True,end="")
    print(m+" SCRIPT GRATIS TIDAK UNTUK DI OBRAL!"+b)
    Line()

def Line():
    print(b+"─"*50)

def Echo(message,eror = False):
    print(m+"["+p+f'{datetime.now().strftime("%H:%M:%S")}'+m+"] ",flush=True,end="")
    if eror:
        print(m+message)
    else:
        print(h+message)

def Simpan(filename):
    if os.path.exists(filename):
        data = open(filename).read()
    else:
        print(m+"Input "+filename+p+" : ")
        data = input()
        file = open(filename,"w")
        file.write(data)
        file.close()
    return data

def Timer(seconds):
    warna = 0
    while seconds:
        for x in [' \ ',' | ',' / ',' - ']:
            mins, secs = divmod(seconds, 60)
            hour, mins = divmod(mins, 60)
            timer = f' ({x}) {hour}:{mins}:{secs} '
            print(timer,end='\r')
            sleep(0.25)
        seconds -= 1
