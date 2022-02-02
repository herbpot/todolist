import asyncio
import os
from time import *
import datetime
from tkinter import *
from tkinter.messagebox import *
from turtle import width

todolist = {} # [[아이디,할일,끝 여부,걸린시간],[번호,할일,끝 여부,걸린시간]]

root = Tk()
root.geometry("200x400")
root.title("ToDoList")
btnFrame = Frame(root, height=400)
entryFrame = Frame(btnFrame).grid(row=0, columnspan=3)

label_ = Label(root, text='[아이디 | 할 일 | 끝 | 걸린시간')
listbox = Listbox(root, exportselection=False, width=200, height=18)

label = Label(entryFrame, text='새 할일')
entry = Entry(entryFrame)

b1 = Button(btnFrame, text='생성')
b2 = Button(btnFrame, text='끝')
b3 = Button(btnFrame, text='삭제')

label_.pack(side='top')
listbox.pack(side='top')

label.pack(side='top')
entry.pack(side='top')
b1.grid(row=2,column=1)
b2.grid(row=2,column=2)
b3.grid(row=2,column=3)

btnFrame.pack(side='top')

keys = []

def printtodo():
    keys.clear()
    entry.delete(0, END)
    listbox.delete(0, END)
    listbox.insert(END,'\n')
    with open(os.path.dirname(os.path.abspath(__file__))+'/todolist.txt','w') as f:    
        for i in todolist.keys():
            printer = str(i) + '| '
            for j in todolist[i]:
                printer += str(j) + ' | '
            listbox.insert(END,printer)
            keys.append(i)
            f.write(printer.replace(' ',''))

def addnewtodo(todo):
    newtodo = [todo,"no",time()]
    todolist[len(todolist)] = newtodo
    listbox.insert(END,newtodo)
    printtodo()

def donetodo(num : int):
    i = todolist[keys[num-1]]
    i[1] = 'yes'
    res = datetime.timedelta(seconds=(time() - float(i[2])))
    i[2] = str(res).split('.')[0]
    printtodo()

def load():
    with open(os.path.dirname(os.path.abspath(__file__))+'/todolist.txt','r') as f :
        for i in f.readlines() :
            i = i.split("|")
            onetodo = []
            for j in i :
                if j == '':continue
                onetodo.append(j)
            todolist[onetodo[0]] = onetodo[1:]
            if onetodo != []:
                listbox.insert(END,onetodo)
    printtodo()

def btn_add(event):
    subject = entry.get().strip()
    if not subject:
        showerror("오류", "내용을 입력해 주세요")
        return
    addnewtodo(subject)

def btn_remove(event):
    sel = listbox.curselection()
    if not sel:
        showerror("오류", "리스트를 먼저 선택해 주세요")
        return
    
    if askyesno("확인", "정말로 삭제하시겠습니까?"):
        id = sel[0]
        todolist.pop(id)
    printtodo()
    

def btn_done(event):
    sel = listbox.curselection()
    if not sel :
        showerror("오류","리스트를 먼저 선텍해 주세요")
    
    if askyesno("확인","정말로 다하셨습니까?"):
        donetodo(sel[0])

def main():
    load()
    b1.bind('<Button-1>', btn_add)
    b2.bind('<Button-1>',btn_done)
    b3.bind('<Button-1>', btn_remove)
    root.mainloop()
    root.attributes("-topmost", True)
            
main()