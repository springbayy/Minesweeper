
from tkinter import *
import time
import math
import random


def kontrollera_gränser(x, y, width, height):
    "denna funktion kallas på när en del av programmet ska kolla på rutorna runtikring sig"
    "den kollar att inget är utanför listan och returnerar objektet kontroll som har 4 värden som är giltiga gränser att kolla inom i listan"
    "input: storlek på spelplan och var man klickar" \
    "output: giltiga rutor runtikring att undersöka"

    class kontroll:
        def __init__(self, vänster, höger, upp, ned):
            "variablerna är representerar rutorna runtikring som måste vara innaför spelplanen"
            self.vänster = vänster
            self.höger = höger
            self.upp = upp
            self.ned = ned

    if x < width - 1 and x > 0 and y < height - 1 and y > 0:
        return kontroll(-1, 2, 2, -1)
    else:
        if x == 0:
            if y > 0 and y < height - 1:
                return kontroll(0, 2, 2, -1)
            elif y == 0:
                return kontroll(0, 2, 2, 0)
            elif y == height - 1:
                return kontroll(0, 2, 1, -1)
        elif x == width - 1:
            if y > 0 and y < height - 1:
                return kontroll(-1, 1, 2, -1)
            elif y == 0:
                return kontroll(-1, 1, 2, 0)
            elif y == height - 1:
                return kontroll(-1, 1, 1, -1)
        elif y == 0:
            return kontroll(-1, 2, 2, 0)
        elif y == height - 1:
            return kontroll(-1, 2, 1, -1)

def skapa_spelplan(klickx, klicky, width, height, antal_tomma, antal_bomber):
    "denna funtion skapar spelaplanen utifrån givna parametrar"
    "Iput: parametrar kring spelplanen"
    "lista med alla rutor och vad de har för attribut"

    class ruta:
        grannar = 0
        bomb = False
        tom = False
        ursprungsruta = False
        synlig = False
        flaggad = False

    spelplan = [[ruta() for l in range(height + 1)] for h in range(width + 1)]
    spelplan[klickx][klicky].ursprungsruta = True
    tomma_rutor = 1

    while tomma_rutor < antal_tomma:
        "denna loop skapar tomma rutorna vid första trycket genom att slumpmässsigt gå runtikring den punkten och tilldela attributet utsprungsruta och tom"
        tomma_rutor += 1
        tom_rutaX = klickx
        tom_rutaY = klicky
        while True:
            if spelplan[tom_rutaX][tom_rutaY].ursprungsruta == False:
                spelplan[tom_rutaX][tom_rutaY].ursprungsruta = True
                break
            steg = random.randint(1, 4)
            if steg == 1 and tom_rutaX != width:
                tom_rutaX += 1
            elif steg == 2 and tom_rutaX != 0:
                tom_rutaX -= 1
            elif steg == 3 and tom_rutaY != height:
                tom_rutaY += 1
            elif steg == 4 and tom_rutaY != 0:
                tom_rutaY -= 1

    bomber = 0
    while bomber < antal_bomber:
        "denna loop placerar ut bomber slumpmässigt"
        randomX = random.randint(0, width - 1)
        randomY = random.randint(0, height - 1)
        if spelplan[randomX][randomY].ursprungsruta == False and spelplan[randomX][randomY].bomb == False:
            spelplan[randomX][randomY].bomb = True
            tilldela_grannar = kontrollera_gränser(randomX, randomY, width, height)
            for sida in range(tilldela_grannar.vänster, tilldela_grannar.höger):
                for höjd in range(tilldela_grannar.ned, tilldela_grannar.upp):
                    spelplan[randomX + sida][randomY + höjd].grannar += 1
            bomber += 1

    return spelplan


def slut(tid_start, tid_slut, knapptryck, bombchans, minesweeper_fönster, width, height, antal_tomma):
    "denna funktion kallas på när spelet är slut. den skapar en ruta som visar ens poäng samt "
    "top 10. poängen baseras på passerad tid samt hur många rutor man röjt undan och om man klarar det eller inte"
    "input: information om spelet och fönstert"
    "output: fönster med resultat och skriver i topplistan"

    poäng = int((bombchans * knapptryck) / (tid_slut - tid_start + 10) * 1000)
    toppplista_skriv = open('topplista', 'a')
    toppplista_skriv.write(str(poäng) + '\n')
    toppplista_skriv.close()
    toppplista_läs = open('topplista')
    topplista = toppplista_läs.read()
    sorterad_topplista = topplista.split()
    for n in range(len(sorterad_topplista)):
        sorterad_topplista[n] = int(sorterad_topplista[n])
    sorterad_topplista.sort(reverse=True)

    slut_fönster = Tk()
    rubrik = Label(slut_fönster, text="Resultat", pady=8, padx=8).grid(row=1, column=1, columnspan=2)
    din_poäng_text = Label(slut_fönster, text="Din poäng", pady=8, padx=8).grid(row=2, column=1)
    din_poäng = Label(slut_fönster, text=str(poäng), pady=8, padx=8).grid(row=2, column=2)
    bästa_genom_tiderna = Label(slut_fönster, text="Bästa resultat genom tiderna", pady=8, padx=8).grid(row=3, column=1,
                                                                                                        columnspan=2)
    resultat_rutor = [[2] for i in range(min(10, len(sorterad_topplista)))]
    for rutor in range(min(10, len(sorterad_topplista))):
        resultat_rutor[0] = Label(slut_fönster, text=str(rutor + 1) + ".", pady=8, padx=8).grid(row=(4 + rutor), column=1)
        resultat_rutor[1] = Label(slut_fönster, text=str(sorterad_topplista[rutor]) + " poäng", pady=8, padx=8).grid(row=4 + rutor, column=2)

    def omstart(width, height, bombchans, antal_tomma):
        "input = spelparametrar"
        "output= nytt minesewper"
        minesweeper_fönster.destroy()
        slut_fönster.destroy()
        fönster = Tk()
        ny_tid_start = time.time()
        minesweeper(width, height, bombchans, antal_tomma, ny_tid_start, fönster)

    def nya_regler():
        "input = NIL"
        "output= stänger fönster och kör om main()"
        minesweeper_fönster.destroy()
        slut_fönster.destroy()
        main()

    spela_igen = Button(slut_fönster, text="Spela igen", command=lambda: omstart(width, height, bombchans, antal_tomma)).grid(row=15, column=1)
    nya_inställningar = Button(slut_fönster, text="Nya regler",command=lambda: nya_regler()).grid(row=15, column=2)


class minesweeper:
    "detta är klassen spelet som tar parametrarna för spelet och gör allt annat"

    def __init__(self, width, height, bombchans, antal_tomma, tid_start, fönster):
        "spelparametrar initieras oxh spelet körs"
        self.width =  width
        self.heigt = height
        self.bombchans = bombchans
        self.antal_tomma = antal_tomma
        self.tid_start = tid_start
        self.fönster = fönster
        minesweeper.grafik(self, width, height, bombchans, antal_tomma, tid_start, fönster)


    def grafik(self, width, height, bombchans, antal_tomma, tid_start, fönster):
        "detta är den stora funktionen som skapar grafiken"
        "input: spelparametrar"
        "output: stängs eller kan starta om main()"

        "bilder laddas in och konstanter defineras"
        minesweeper_fönster = fönster
        rutbild = PhotoImage(file=r"tile.png")
        oformaterad_flagga = PhotoImage(file=r"flag.png")
        mina = PhotoImage(file=r"mina.png").subsample(5, 5)
        flag = oformaterad_flagga.subsample(23, 23)
        gråruta = rutbild.subsample(5, 5)
        bilder = [0 for i in range(9)]
        rutnät = [[0 for h in range(height)] for b in range(width)]

        for i in range (9):
            filnamn= str(i)+".png"
            bilder[i] = PhotoImage(file=filnamn).subsample(5, 5)

        antal_bomber = math.ceil(((width * height) - antal_tomma) * bombchans)
        class spelinfo:
            "vitala variabler"
            information = 0
            antal_knapptryck = 0
            korrekta_flaggor = 0
            kvar_till_vinst = (width * height) - antal_bomber + 1


        def loser():
            "åtgärd om man förlorar BOOM, då stoppas spelet och man går till slut-panelen"
            "input= NIL"
            "output=slut() och visar hela spelplanen"
            tid_slut = time.time()
            for x in range (width):
                for y in range(height):
                    åtgärder_vid_synliggörande(x, y)

            slut(tid_start, tid_slut, spelinfo.antal_knapptryck-1, bombchans, minesweeper_fönster, width, height, antal_tomma)
            info_om_flaggor = Label(minesweeper_fönster, text="Antal korrekt markerade Minor: " + str(spelinfo.korrekta_flaggor)+ "/"+str(antal_bomber)).grid(row=1, column=1, columnspan=width)

        def winner():
            "åtgärd om man röjer alla rutor, då stoppas spelet och man går till slut-panelen"
            "input= NIL"
            "output=slut()"
            tid_slut = time.time()
            for x in range(width):
                for y in range(height):
                    åtgärder_vid_synliggörande(x, y)
            slut(tid_start, tid_slut, spelinfo.antal_knapptryck/0.9, bombchans, minesweeper_fönster, width, height, antal_tomma)


        def åtgärder_vid_synliggörande(x, y):
            "om en ruta synliggörs så visas olika bilder beroende på vad det är för någon ruta"
            "funktionen konfigurerar rutorna"
            "input: kordinater"
            "output=ändrar vad som visas på rutorna"
            spelinfo.information[x][y].synlig = True
            rutnät[x][y].unbind("<Button-1>")
            rutnät[x][y].unbind("<Button-3>")
            if spelinfo.information[x][y].flaggad==False:
                if spelinfo.information[x][y].bomb==True:
                    rutnät[x][y].config(image=mina)
                else:
                    rutnät[x][y].config(image=bilder[spelinfo.information[x][y].grannar])
                    spelinfo.kvar_till_vinst -= 1



        def gör_ruta_synlig(x, y):
            "denna funktion gör rutor synliga, den har även uppdraget att via rekursion synliggöra alla rutor i ett samanhängande"
            "område om dem har 0 bomber som grannar"
            "input: kordinater"
            "output=synliggör rutor enligt spelets regelr och tar en till slut-rutan vid vinst/förlust"
            if spelinfo.information[x][y].bomb == False:
                gräns = kontrollera_gränser(x, y, width, height)
                åtgärder_vid_synliggörande(x, y)
                if spelinfo.information[x][y].grannar == 0:
                    for sida in range(gräns.vänster, gräns.höger):
                        for höjden in range(gräns.ned, gräns.upp):
                            if spelinfo.information[x+sida][y+höjden].synlig==False and spelinfo.information[x+sida][y+höjden].bomb==False:
                                gör_ruta_synlig(x+sida, y+höjden)
                if spelinfo.kvar_till_vinst == 0:
                    winner()
            elif spelinfo.information[x][y].bomb == True:
                loser()

        def knapptryck(x, y):
            "denna funktion aktiveras vid varje vänsterklick och om det är första klicket skapar den hela spelplanen (dvs om antalknapptryck==0)"
            "input: kordinater"
            "output=skapar spelplanen vid första knapptrycket, alternativt, gör ruta synlig"
            if spelinfo.antal_knapptryck == 0:
                spelinfo.information = skapa_spelplan(x, y, width, height, antal_tomma, antal_bomber)
                gräns = kontrollera_gränser(x, y, width, height)
                for sida in range(gräns.vänster, gräns.höger):
                    for höjden in range(gräns.ned, gräns.upp):
                        if spelinfo.information[x + sida][y + höjden].synlig == False and spelinfo.information[x + sida][y + höjden].bomb == False:
                            gör_ruta_synlig(x + sida, y + höjden)
            gör_ruta_synlig(x, y)
            spelinfo.antal_knapptryck += 1

        def återgåfrånfalgga(x, y):
            "input: kordinater"
            "låter ruta gå från flagga till vanlig ruta"
            "input: kordinater"
            "output=ändrar bilden på rutan med den kordinaten och key-bindings"
            rutnät[x][y].config(image=gråruta)
            rutnät[x][y].bind("<Button-1>", lambda e, knapptryck=knapptryck: knapptryck(x, y))
            rutnät[x][y].bind("<Button-3>", lambda e, knapptryck=knapptryck: flagga(x, y))
            if spelinfo.information[x][y].bomb ==True:
                spelinfo.information[x][y].flaggad = False
                spelinfo.korrekta_flaggor -= 1

        def flagga(x, y):
            "låter en ruta bli o-klickbar och visar flagga"
            "input: kordinater"
            "output= ändrar bilden på rutan med den kordinaten och key-bindings"
            if spelinfo.antal_knapptryck != 0:
                rutnät[x][y].config(image=flag)
                rutnät[x][y].unbind("<Button-1>")
                rutnät[x][y].bind("<Button-3>", lambda e, återgåfrånfalgga=återgåfrånfalgga: återgåfrånfalgga(x, y))
                if spelinfo.information[x][y].bomb ==True:
                    spelinfo.information[x][y].flaggad = True
                    spelinfo.korrekta_flaggor += 1

        def skaparuta(x, y):
            "denna funktion skapar spelplanen med alla bilder det första som händer"
            "input: kordinater"
            "output=label med en korrespenderande handling vid klick"
            label = Label(minesweeper_fönster, image=gråruta, cursor="tcross")
            label.grid(column=x + 1, row=y + 2)
            label.bind("<Button-1>", lambda e, : knapptryck(x, y))
            label.bind("<Button-3>", lambda e, : flagga(x, y))
            return label

        "denna loop har i uppgift att skapa alla rutor och att tilldela alla Labels en position i en matris"
        for x in range(width):
            for y in range(height):
                rutnät[x][y] = skaparuta(x, y)





def main():

    "denna funktion sätter alla parametrar för spelet innan man börjar"
    window = Tk()

    välj_höjd = Label(window, text="välj höjd på spelplanen, minst 8 och maximalt 25 enheter: ")
    välj_höjd.grid(row=1, column=1, columnspan=2)
    höjd_input = Entry(window)
    höjd_input.grid(row=1, column=3)
    välj_bredd = Label(window, text="välj bredd på spelplanen, minst 8 och max 45 enheter enheter: ")
    välj_bredd.grid(row=2, column=1, columnspan=2)
    bredd_input = Entry(window)
    bredd_input.grid(row=2, column=3)

    def sätt_igång_spelet(svårighetsgrad):
        "denna funktion sätter igång spelet med de valda parametrar man valt"
        "input=spelparametrar"
        "output=minesweeper"
        try:
            spelbredd = int(bredd_input.get())
            spelhöjd = int(höjd_input.get())
        except ValueError:
            felmeddelande = Label(window, text="kontrollera inputs och försök igen")
            felmeddelande.grid(row=4, column=1, columnspan=3)

        else:
            if spelbredd < 8 or spelhöjd < 8 or spelbredd > 45 or spelhöjd > 25:
                felmeddelande = Label(window, text="kontrollera inputs och försök igen")
                felmeddelande.grid(row=4, column=1, columnspan=3)
            else:
                tid_start = time.time()
                antal_tomma = int(math.sqrt(spelhöjd * spelbredd))
                if antal_tomma > 20:
                    antal_tomma = 20
                bombchans = svårighetsgrad * 0.065
                window.destroy()
                fönster = Tk()
                minesweeper (spelbredd, spelhöjd, bombchans, antal_tomma, tid_start, fönster)


    spela_svår = Button(window, text="Expert", command=lambda: sätt_igång_spelet(4)).grid(row=3, column=3)
    spela_medel = Button(window, text="medel", command=lambda: sätt_igång_spelet(3)).grid(row=3, column=2)
    spela_lätt = Button(window, text="nybörjare", command=lambda: sätt_igång_spelet(2)).grid(row=3, column=1)
    tom_ruta = Label(window, text="")
    tom_ruta.grid(row=4, column=1)

    mainloop()


main()
