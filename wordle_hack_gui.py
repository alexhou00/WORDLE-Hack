# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 19:09:39 2022

@author: alexhou00
"""

def App():
    global word, col_seq, n, english_words, recom_btns, cur, possible_words, black_letters
    global yellow_letters
    
    possible_words = [i for i in english_words if len(i)==n]
    possible_words = sorted(possible_words, key=lambda x : rank_words(x), reverse=True)
    
    scale.config(state='disabled')
    #haveToContinue = True
    word = word.lower()
    
    
    
    counts = [0 for i in range(26)]
    possible_words = sorted(possible_words, key=lambda x : rank_words(x), reverse=True)
    
    #get black letters
    tmp = []
    for I,J in enumerate(col_seq):
        if (J=='b'):
            tmp.append(word[I])
    black_letters = black_letters.union(set(tmp))
    for ch in black_letters: keys_[keys_single.index(ch)].config(bg=DARKGRAY)
        
    #get yellow letters and their position
    contains = []
    for I,J in enumerate(col_seq):
        if (J=='y'):
            contains.append(word[I]+str(I))
    contains = {(j[0],j[1:]) for j in contains}
    yellow_letters.extend(list(contains))
    for ch,_ in yellow_letters: keys_[keys_single.index(ch)].config(bg=YELLOW)
    for l in {i for i,j in contains}:
        counts[ord(l)-ord('a')]+=1
    
    #get green letters
    reg_input = ''
    for I,J in enumerate(col_seq):
        if (J=='g'):
            reg_input += word[I]
            keys_[keys_single.index(word[I])].config(bg=GREEN)
        else:
            reg_input+='.'
    reg = re.compile(reg_input) #example: "l..st" --> least
    for l in [m for m in reg_input if m!='.']:
        counts[ord(l)-ord('a')]+=1
    
    #find possible words
    possible_words_fixed = possible_words.copy() 
    toPrint = []
    for word in possible_words_fixed:
        match_green = bool(re.match(reg, word))
        if (match_green) and \
           (all(j in word and word[int(k)]!=j for j,k in yellow_letters)) and \
           (all(word.count(m)<=counts[ord(m)-ord('a')] for m in black_letters)):
            toPrint.append(word)
        else: possible_words.remove(word)
    
    #print results
    numPrint = 10
    #if numPrint=='all': numPrint = len(toPrint)
    #else: numPrint = int(numPrint)
    
    
    cnt = 0;string = ''
    for word in toPrint[:numPrint]:
        string+=(word+' '*3)
        cnt += 1
        if cnt>=(60-3*(n-1))/5: string+='\n';cnt=0
        
    showinfo("\nPossible words sorted by possibility:", string)
   
    if len(toPrint)<5:
        for i in range(len(toPrint)): recom_btns[i].config(text=toPrint[i])
    else:
        for i in range(5): recom_btns[i].config(text=toPrint[i])
        
def exit_():
    certainty = ask("Did you win? ")
    if certainty>1:
        showinfo("%s%s"%
              (choice(('Congratulations','Congrats', "Hooray", "Yay")),
               choice(('!','!!', '!!!', '.'))),"%s"%
               choice(("I bet you're satisfied with my job.","Did I do a great job?",
                       "Did you enjoy the WORDLE game with my help?","Come again next time!")))
    elif certainty<0:
        showinfo("%s%s"%(
            choice(('Oops','Uh oh', "Oh", "Nah nevermind")), 
            choice(('...',' sorry.', ' I\'m sorry...', '.'))),
                 "%s"%
                 choice(("Better luck next time.","You can help the author improve the code, though.",
                       "Any suggestions for me to improve?","Try again next time!")))
    root.destroy()    

import tkinter as tk
import re
from wordfreq import word_frequency
from random import choice, sample
from tkinter.messagebox import askyesno, showinfo
from webbrowser import open as bopen

keys = (
    ('q','w','e','r','t','y','u','i','o','p'),
    (' ','a','s','d','f','g','h','j','k','l',' '),
    (u'\u23ce','z','x','c','v','b','n','m',u'\u232b',' '))
keys_single = tuple('qwertyuiop@asdfghjkl@@zxcvbnm@@')
keys_ = []
BGCOLOR = '#121213'
GRAY = '#818384'
DARKGRAY = '#616262'
WHITE = "#d7dadc"
ORANGE = '#f5793a'
BLUE = '#85c0f9'
GREEN = '#538d4e'
YELLOW = '#ffc800'
LIGHTGREEN = '#639d5e'
LIGHTYELLOW = '#ffd810'
LIGHTORANGE = '#ff894a'
LIGHTBLUE = '#95d0ff'

class Keyboard(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs,bg=BGCOLOR)
        self.create_buttons()
       
    def create_buttons(self):
        store_layer = tk.Frame(self)
        store_layer.pack(side='top',expand='yes',fill='both',padx=5, pady=5)
        for key_bunch in keys:
            store_key_frame = tk.Frame(store_layer, bg=BGCOLOR)
            store_key_frame.pack(side='top',expand='yes',fill='both')
            for k in key_bunch:
                k=k.capitalize()
                if k==' ':
                    store_button = tk.Button(store_key_frame, text=k, width=1, height=2)
                    store_button['bd'] = 0
                    store_button['state'] = 'disabled'
                    store_button['bg'] = BGCOLOR
                elif k==u'\u232b':
                    store_button = tk.Button(store_key_frame, text=k, width=3, height=2)
                    store_button['bg']=GRAY
                else:
                    store_button = tk.Button(store_key_frame, text=k, width=2, height=2)
                    store_button['bg']=GRAY
                store_button['fg']=WHITE
                store_button['activebackground']=DARKGRAY
                store_button['activeforeground']=WHITE
                store_button['font']=("Arial",10,"bold")
                store_button['command']=lambda q=k: button_command(q)
                store_button.pack(side='left',fill='both',expand='yes')
                keys_.append(store_button)

                
def button_command(event):
    global word, n, col_seq
    if event==u'\u232b':
        backspace()
    elif event==u'\u23ce':
        enter()
    elif len(word)<n:
        word+=event
        refresh_screen()
    #print(word)

def key_pressed(event):
    if event.char.isalpha():
        button_command(event.char.upper())

def backspace(*event):
    global word
    word = word[:-1]
    refresh_screen()

def enter(*event):
    global n, word, col_seq, cur, col_code
    #col_code = ['g','y','b']
    if len(col_seq)==n:
        txt.config(state='normal')
        #txt.insert('end', col_seq.upper()+'\n'+word.upper()+'\n\n')
        txt.insert('end', word.upper()+'\n\n')
        for I_ in range(n):
            txt.tag_add(str(cur)+'.'+str(I_), str(cur)+'.'+str(I_),str(cur)+'.'+str(I_+1))
            txt.tag_configure(str(cur)+'.'+str(I_),background=colors[col_code.index(col_seq[I_])])
            if (col_seq[I_]=='b'): txt.tag_configure(str(cur)+'.'+str(I_),foreground=WHITE)
        cur += 2
        txt.config(state='disabled')
        App()
        word = ''
        col_seq=''
    else: showinfo("Info","Your must fill all colors")
    refresh_screen()

def refresh_screen():
    global colors, col_code
    #colors = [GREEN,YELLOW,'#3a3a3c']
    #col_code = ['g','y','b']
    global word, col_seq
    for k,frame in enumerate(screen_letters):
        if k<len(word):
            frame['text'] = word[k]
        else:
            frame['text'] = ' '
    for k,frame in enumerate(screen_letters):
        if k<len(col_seq):
            frame['bg'] = colors[col_code.index(col_seq[k])]
        else:
            frame['bg'] = GRAY
    

def add_color(col):
    global col_seq
    if len(col_seq)<n: col_seq+=col
    #print(col_seq)
    refresh_screen()

def add_color_bind(event):
    global col_code
    add_color(col_code[int(event.char)-1])

def del_col(*event):
    global col_seq
    col_seq = col_seq[:-1]
    #print(col_seq)
    refresh_screen()

def set_n(val):
    global n, english_words,possible_words,word
    n = int(val)
    txt.config(width=n)
    word = ''
    possible_words = [i for i in english_words if len(i)==n]
    possible_words = sorted(possible_words, key=lambda x : rank_words(x), reverse=True)
    possible_words = (sample(possible_words[:20], 20))
    for i in range(5): recom_btns[i].config(text=possible_words[i])
    
    create_sq()
    
def create_sq():
    global n, screen_frames, screen_letters
    for i in screen_frames: i.destroy()
    for i in screen_letters: i.destroy()
    screen_frames = []
    screen_letters = []
    for i in range(n):
        screen_frames.append(tk.Frame(mainFrame))
        screen_frames[i].pack(side='left',padx=5,expand='yes',fill='both')
        screen_letters.append(tk.Label(screen_frames[i], text=' ',fg=WHITE, height=1, width=3,bg=GRAY,font=('Consolas',24),pady=11))
        screen_letters[i].pack()
    refresh_screen()

def colorBlind(on):
    global colors,col_fg
    if on:
        colors[0],colors[1] = ORANGE, BLUE
        col_fg[0],col_fg[1] = LIGHTORANGE, LIGHTBLUE
    else:
        colors[0],colors[1] = GREEN, YELLOW
        col_fg[0],col_fg[1] = LIGHTGREEN, LIGHTYELLOW
    refresh_screen()
    for idkWhatToName in range(2): 
        colbtns[idkWhatToName].config(bg=colors[idkWhatToName],fg=col_fg[idkWhatToName])

def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

def rank_words(word):
    global letterfreq, english_words
    score = word_frequency(word,'en')
    for letter in set(word):
        score *= (letterfreq[ord(letter)-ord('a')])
    if (word[-1]=='s' or word[-2:]=='ed') and word[:-1] in english_words:
        score /= 10
    return score

def ask(question):
    answer = askyesno(title='Question',
                message=question)
    return answer*3-1

def enterText(num):
    global possible_words, word
    try:
        word = possible_words[num].upper()
    except IndexError:
        pass
    refresh_screen()
    

word = ''
col_seq = ''

letterfreq = [2.7414499308958415, 0.6824224148762407, 0.8963940193491644, 0.9182811911044102, 
              2.5480588013569543, 0.40442266616409095, 0.6438748586505842, 0.7461238849101646, 
              1.6552581982661139, 0.12282950119361731, 0.5693931398416886, 1.3870586757130294, 
              0.814725468023621, 1.320743812036688, 1.704912677472044, 0.7510239979896971, 
              0.045407714537002125, 1.6800854378690793, 2.135469280060309, 1.3684382460108053, 
              1.0979520040206057, 0.28681995225530843, 0.38253549440884543, 0.11792938811408468, 
              0.8235456715667797, 0.15484357331323031]  #percentage*26/100

n = 5
english_words = load_words()
possible_words = [i for i in english_words if len(i)==n]
possible_words = sorted(possible_words, key=lambda x : rank_words(x), reverse=True)

root = tk.Tk()
root.title("WORDLE Hack")
root.resizable(False, False)

root_ = tk.Frame(root,bg=BGCOLOR)
root_.pack()
title = tk.Label(root_, text="WORDLE Hack", bg=BGCOLOR, fg=WHITE, font=("Arial",20,'bold'))
title.pack()

scale = tk.Scale(root_, bg=BGCOLOR, troughcolor=BGCOLOR, from_=4, to=11, width=20, sliderlength = 15, length=120,
                         activebackground=BGCOLOR, highlightbackground=BGCOLOR, command=set_n,fg=WHITE)
scale.set(5)
possible_words = (sample(possible_words[:20], 20))
scale.pack(side='left',padx=5)

win = tk.Frame(root_, bg=BGCOLOR)
win.pack(side='left')



txtLbl = tk.Label(root_, bg=BGCOLOR, fg=WHITE, text='History')
txtLbl.pack()
txt = tk.Text(root_, bg=BGCOLOR, width=5, height=14, #text='', anchor='n', justify='left',
              font=("Consolas",9),relief='sunken',state='disabled',selectbackground=BGCOLOR)
txt.pack()


black_letters = set()
yellow_letters = []

mainFrame = tk.Frame(win,bg=BGCOLOR)
screen_letters = []
screen_frames = []
recom_btns = []
create_sq()
cur = 1

mainFrame.pack(pady=5)

    
colorBtnFrame = tk.Frame(win, bg=BGCOLOR)
colorBtnFrame.pack(side='top')
colors = [GREEN,YELLOW,'#3a3a3c']
col_code = ['g','y','b']
col_fg = [LIGHTGREEN,LIGHTYELLOW,'#4a4a4c']
cb1 = tk.Button(colorBtnFrame,text='',width=2,bg=GREEN,
                  activebackground=YELLOW,command=lambda:colorBlind(0))
cb1.pack(side='left',fill='both',padx=(5,0),pady=5)
cb2 = tk.Button(colorBtnFrame,text='',width=2,bg=ORANGE,
                  activebackground=BLUE,command=lambda:colorBlind(1))
cb2.pack(side='left',fill='both',padx=(0,5),pady=5)
colbtns = []
for i in range(3):
    x = col_code[i]
    f = tk.Button(colorBtnFrame,text=str(i+1),width=4,bg=colors[i], fg=col_fg[i], 
                  activeforeground='gray',command=lambda x=x: add_color(x))
    f.pack(side='left',fill='both',padx=5,pady=5)
    colbtns.append(f)
btnBSCol = tk.Button(colorBtnFrame,text=u'\u232b',width=4,bg=GRAY,command=del_col)
btnBSCol.pack(side='left',fill='both',padx=5,pady=5)

kbFrame = tk.Frame(win, bg=BGCOLOR)
kbFrame.pack()
frame1 = tk.Frame(kbFrame, bg=BGCOLOR)
frame1.pack()
for i in range(5):
    recom_btns.append(tk.Button(frame1, text=possible_words[i],bg=GRAY,fg=WHITE,font=("Consolas",9),
                                activebackground=DARKGRAY,activeforeground=WHITE,command=lambda i=i:enterText(i)))
    recom_btns[i].pack(side='left')
Keyboard(kbFrame).pack()
transbtn = tk.Button(root_, text='Transl.',fg=WHITE,bg=DARKGRAY, activebackground=DARKGRAY,
                     command=lambda:bopen('https://translate.google.com.tw/?hl=zh-TW&sl=en&tl=zh-TW&text='+word.lower()))
transbtn.pack()
exitbtn = tk.Button(root_, text='Exit App', command=exit_,fg=WHITE,bg=DARKGRAY,
                    activebackground=DARKGRAY)
exitbtn.pack()
'''
suggest = ask("Want me to suggest any word to start? ")
num_rand = randint(10, 20)
if suggest>1:
    top = tk.Toplevel()
    top.title("Recommended Words:")
    top.resizable(False,False)
    toplbl = tk.Label(top, text = ' '.join(sample(possible_words[:num_rand], num_rand)))
    toplbl['font'] = ("Arial",15)
    toplbl.pack(padx=5, pady=5)
'''

root.focus_force()
root.bind('<Key>', key_pressed)
root.bind('<BackSpace>',backspace)
root.bind('<Return>',enter)
for i in range(1,4):
    x = col_code[i-1]
    root.bind(str(i), lambda x=x: add_color_bind(x))
root.bind('0', del_col)
root.mainloop()