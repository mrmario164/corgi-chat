#hi
from tkinter import *
import mechanize
from threading import Thread
from tkinter import messagebox as box

tk = Tk()
tk.title("Corgi Chat")
tk.iconbitmap('icon.ico')
tk.resizable(0, 0)
canvas = Canvas(tk, width=400, height=500, bd=0, highlightthickness=0)
canvas.pack()
canvas.config(bg='gray')
tk.update()

class User:
    def __init__(self):
        self.username = ''

mainUser = User()

global oldText
oldText = ''''''
global br
br = mechanize.Browser()

userLabel = Label(canvas, text='Enter your username to\nbegin your session.', bg='gray', font='Arial 20')
userEntry = Entry(canvas, width=64)
receiveBox = Text(canvas, bg='white', width=49, height=20, font='Arial 11', state=DISABLED)
msgEntry = Entry(canvas, width=64)
titleLabel = Label(canvas, text='Corgi Chat', font='Arial 40', bg='gray')

def mainScreen():
    receiveBox.place(relx=0.007, rely=0.18)
    msgEntry.place(relx=0.015, rely=0.9)
    msgEntry.bind("<Return>", sendMessage)

def beginScreen():
    userLabel.place(relx=0.15, rely=0.2)
    titleLabel.place(relx=0.18, rely=0.02)
    userEntry.place(relx=0.015, rely=0.4)
    userEntry.bind("<Return>", setName)

def setName(*args):
    name = userEntry.get()
    if len(name) > 0 and len(name) < 12:
        mainUser.username = name
        userLabel.destroy()
        userEntry.destroy()
        main()
    elif len(name) > 12:
        box.showinfo('Username', 'Please make your username shorter than 12 characters.')

def internetError():
    try:
        receiveBox.config(state=NORMAL)
        receiveBox.delete('1.0', END)
        receiveBox.insert(INSERT, 'Could not connect to the server. Check your internet\nconnection, then restart the app.')
        receiveBox.see(END)
        receiveBox.config(state=DISABLED)
    except:
        pass

def sendMessage(*args):
    try:
        text = msgEntry.get()
        if len(text) < 200:
            msgEntry.delete(0, len(text))
            message = mainUser.username + ': ' + text
            response = br.open('http://freetexthost.com/qanua4zsmf')
            try:
                br.set_all_readonly(False)
            except:
                pass
            br.select_form("editform")
            control = br.form.find_control("adminpass")
            control.value = 'corgichat'
            response = br.submit()
            br.select_form("editform")
            control = br.form.find_control("text")
            control.value += '\n' + message
            response = br.submit()
        else:
            box.showinfo('Message', 'Please keep your message shorter than 200 characters!')
    except:
        internetError()

def readMessages(oldText):
    while True:
        try:
            response = br.open('http://freetexthost.com/qanua4zsmf')
            txt = response.read()
            t1 = re.findall(r'<div id="contentsinner">(.*?)<div style="clear: both;"><!-- --></div>', txt.decode(), re.DOTALL)
            t1 = t1[0]
            t1 = t1.strip()
            finalText = t1.replace('<br />', '')
            if finalText != oldText:
                receiveBox.config(state=NORMAL)
                receiveBox.delete('1.0', END)
                receiveBox.insert(INSERT, finalText)
                receiveBox.see(END)
                receiveBox.config(state=DISABLED)
                oldText = finalText
        except:
            internetError()

def main():
    readThread = Thread(target=readMessages, daemon=True, args=(oldText,))
    readThread.start()
    mainScreenThread = Thread(target=mainScreen, daemon=True)
    mainScreenThread.start()

def run():
    beginScreen()
    mainloop()
