from tkinter import *
import math
import random

class ruta:
    grannar=0
    bomb=False
    tom=False

def skapaspelplan(längd, höjd, antalbomber, klickx, klicky):
    spelplan=[[(ruta()) for l in range (längd+1)]for h in range (höjd+1)]
    spelplan[klickx][klicky].tom = True
    tommarutor=1

    while tommarutor < 10:
        "denna loop skapar det tomma området runt där man klickar första gången"
        tommarutor +=1
        UtgångspunktFörTomtOmrådeX = klickx
        UtgångspunktFörTomtOmrådeY = klicky
        while True:
            if spelplan[UtgångspunktFörTomtOmrådeX][UtgångspunktFörTomtOmrådeY].tom==False:
                spelplan[UtgångspunktFörTomtOmrådeX][UtgångspunktFörTomtOmrådeY].tom=True
                break
            steg=random.randint(1,4)
            if steg == 1 and UtgångspunktFörTomtOmrådeX != längd:
                UtgångspunktFörTomtOmrådeX += 1
            elif steg == 2 and UtgångspunktFörTomtOmrådeX != 0:
                UtgångspunktFörTomtOmrådeX -= 1
            elif steg == 3 and UtgångspunktFörTomtOmrådeY != höjd:
                UtgångspunktFörTomtOmrådeY += 1
            elif steg == 4 and UtgångspunktFörTomtOmrådeY != 0:
                UtgångspunktFörTomtOmrådeY -= 1


    for i in range (antalbomber):
        "denna loop placerar ut alla bomber på tiles och säger till dess grannar att " \
        "det är en bomb i dess närhet"

        def LäggTillGrannar(sidledvänster, sidledhöger, höjdledned, höjdledupp):
            "denna funktion lägger till +1 till alla grannar till bomben"
            for sidled in range(sidledvänster, sidledhöger):
                for höjdled in range(höjdledned, höjdledupp):
                    spelplan[x + sidled][y + höjdled].grannar += 1
        while True:
            x = random.randint(0,längd)
            y = random.randint(0,höjd)

            if spelplan[x][y].tom==False and spelplan[x][y].bomb==False:
                "om det inte är en bomb eller uttryckligen tom ruta så placerar den ut en bomb och " \
                "informerar grannar om att det är en bomb i närhetetn"
                spelplan[x][y].bomb=True

                if x != längd and x != 0 and y != höjd and y != 0:
                    "om det är en bomb mitt i brädet så placerar den ut grannar +1 på alla runtikring"
                    LäggTillGrannar(-1, 2, -1, 2)
                else:
                    "om det är så att en bomb placeras på kanten av brädet måste det undersökas ytterligare och göras specialfall"
                    if x==0:
                        if y!=0 and y != höjd:
                            LäggTillGrannar(0, 2, -1, 2)
                        elif y==0:
                            LäggTillGrannar(0, 2, 0 , 2)
                        else:
                            LäggTillGrannar(0,2,-1,1)
                    elif x==längd:
                        if y!=0 and y != höjd:
                            LäggTillGrannar(-1, 1, -1, 2)
                        elif y==0:
                            LäggTillGrannar(-1, 1, 0, 2)
                        else:
                            LäggTillGrannar(-1,1,-1,1)
                    elif y==0:
                        LäggTillGrannar(-1, 2, 0 ,2)
                    else:
                        LäggTillGrannar(-1, 2, -1, 1)
                break


    for sidled in range (längd):
        for höjdled in range(höjd):
            "om en ruta är helt tom och inte har några grannar tilldelas den attributet TOM"
            if spelplan[sidled][höjdled].grannar == 0:
                spelplan[sidled][höjdled].tom=True
    return spelplan

def main():
    SizeX=700
    SizeY=500
    bredd = 25
    höjd = 15




    window = Tk()
    canvas = Canvas(window, width=SizeX, height=SizeY, bg="#000000")
    canvas.pack()

    class knapp:
        k=Label(window, width=(700/bredd), höjd)



    for b in range (bredd):
        for h in range (höjd):
            img= PhotoImage(width=SizeX, height=SizeY)
            canvas.create_image((SizeX / 2, SizeY / 2), image=img, state="normal")


    mainloop()

