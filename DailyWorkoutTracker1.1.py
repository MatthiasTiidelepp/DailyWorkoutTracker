#Projekti autor: Matthias Tiidelepp
#
#Loon programmi, mille abil on võimalik igapäevaselt tehtavate treeningharjutuste
#(näiteks kätekõverdused, kõhulihased jne) koguseid salvestada.
#
#Baaskujul näeb see välja järgmine: kasutades tkinterit loon akna, kus on listbox,
#millesse on entry välja ja nupu abil võimalik sisestada uut tüüpi treeningharjutus.
#Selle kõrval on teine listbox, mis sisaldab harjutuste kogust sellel päeval.
#Teise listboxi all on entry väli ja nupp, millega saab lisada soovitud arvu
#harjutuste tänasele kogusele. Programm salvestab harjutused .txt faili ja
#uuel käivitamisel loeb tänase päeva andmed (kui need juba eksisteerivad) ning täidab
#listboxid vastavalt.

#impordi tkinteri graafilise kasutajaliidese, kuupäeva ning kellaaja ja os.path moodulid
from tkinter import *
from datetime import *
from os import path

#loo põhiaken
window = Tk()
window.title("Daily Workout Tracker 1.1")
window.geometry("400x260")

#tänane kuupäev formaadis "päev.kuu(sõnana).aasta"
dateVar = datetime.today().strftime("%d.%b.%Y")
#lisa praegune kuupäev sildina aknale
dateLabel = Label(window, text=dateVar)
dateLabel.grid(row=0, column=1, padx=5, pady=5)

#lisa harjutuste listbox
exList = Listbox(window, width=50)
exList.grid(row=1, column=0, padx=5, pady=5, columnspan=3)

#lisa harjutuste koguse listbox
exCntList = Listbox(window, width=5)
exCntList.grid(row=1, column=3, padx=5, pady=5)

#kontrolli, kas tänase kuupäevaga fail eksisteerib
if path.exists(dateVar + ".txt"):
    #kui tänase kuupäevaga fail eksisteerib, ava see read mode'is
    exReadFile = open(dateVar + ".txt", "r", encoding="UTF-8")
    #loo järjend ning sisesta sinna andmed failist rea kaupa
    fileData = []
    for rida in exReadFile:
        fileData.append(rida)
    #loo teine järjend ning sisesta sinna liikmed eelmisest järjendist ilma kellaaja ning newline sümbolita
    #lõika eelmise järjendi liikmed kolmeks jupiks, eraldades harjutuse nime " - " ja harjutuse koguse
    exercises = []
    for item in fileData:
        exercises.append(item[6:-1].partition(" - "))
    #kui harjutuste listboxis  pole harjutust, siis lisa see sinna ning lisa harjutuste koguse listboxi selle harjutuse kogus
    for exercise in exercises:
        if exercise[0] not in exList.get(0, "end"):
            exList.insert(END, exercise[0])
            exCntList.insert(END, int(exercise[2]))
        #kui harjutuste listboxis harjutus juba on, võta harjutuse parajasti käsitletava harjutuse kogus ja lisa see
        #harjutuste koguse listboxi selle harjutuse indexiga kohale
        else:
            exIndex = exList.get(0, "end").index(exercise[0])
            exCntList.delete(exIndex)
            exCntList.insert(exIndex, exercise[2])
    #sulge fail
    exReadFile.close()

#lisa entry väli harjutuse tüübi sisestamiseks, mida soovitakse lisada
exEntry = Entry(window, width=40)
exEntry.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

#lisa entry väli harjutuste kogusele lisamiseks
exCntEntry = Entry(window, width=5)
exCntEntry.grid(row=2, column=3, padx=5, pady=5)

#funktsioon, mis käivitub nupu Add vajutamisel
def addEx():
    #lisa nimekirja tekst entry väljalt
    exList.insert(END, exEntry.get())
    #lisa harjutuste koguse nimekirja sissekanne
    exCntList.insert(END, 0)
    #ava või loo fail nimega tänane kuupäev ja kirjuta sinna praegune kellaaeg, tabelisse sisestatud harjutuse nimi ja praegune kogus
    exFile = open(dateVar + ".txt", "a", encoding="UTF-8")
    exFile.write(datetime.today().strftime("%H:%M") + " " + exEntry.get() + " - 0\n")
    exFile.close()
    #tühjenda entry väli
    exEntry.delete(0, "end")

#funktsioon, mis käivitab enteri vajutamisel funktsiooni addEx
def enter(event):
    addEx()

#kui entry väli on selekteeritud, käivitab enter klahv funktsiooni enter
exEntry.bind('<Return>', enter)

#lisa nupp, mille vajutamisel lisatakse harjutuse entry väljal olev tekst listboxi
addExBtn = Button(window, text="Add", padx=5, pady=5, command=addEx)
addExBtn.grid(row=2, column=2)

#funktsioon, mis lisab harjutuste koguse listboxi vanale numbrile uue ja sisestab selle vana kohale
def changeCnt(index):
    #salvesta lisatav kogus ja muuda see integeriks
    addCnt = int(exCntEntry.get())
    #salvesta vana number harjutuste koguse listboxist selekteeritud indeksi kohal ja muuda see integeriks
    oldCnt = int(exCntList.get(index))
    #kustuta vana number
    exCntList.delete(index)
    #sisesta harjutuste koguse listboxi vana numbri kohale 5 võrra suurem number
    exCntList.insert(index, oldCnt + addCnt)
    exFile = open(dateVar + ".txt", "a", encoding="UTF-8")
    exFile.write(datetime.today().strftime("%H:%M") + " " + exList.get(index) + " - " + str(oldCnt + addCnt) + "\n")
    exFile.close()
    #tühjenda lisatava koguse väli
    exCntEntry.delete(0, "end")

#funtksioon, mis lisab harjutuste koguse entry väljal oleva arvu selekteeritud harjutusele
def addExCnt():
    #leia selekteeritud asja index listboxis ja salvesta see muutujasse
    exIndex = exList.curselection()
    exCntIndex = exCntList.curselection()
    #kui harjutuste koguse listboxis pole ükski asi selekteeritud, käivita funktsioon changeCnt
    if exCntIndex == ():
        changeCnt(exIndex)
    else:
        changeCnt(exCntIndex)        
    
#lisa nupp, mille vajutamisel lisatakse harjutuse koguse entry väljal olev arv selekteeritud harjutusele
addCntBtn = Button(window, text="+", padx=5, pady=5, command=addExCnt)
addCntBtn.grid(row=2, column=4)


window.mainloop()