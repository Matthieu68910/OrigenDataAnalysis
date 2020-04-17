import tkinter as tk
from tkinter.filedialog import *
from tkinter import ttk
from origenpackage import fonctions
from tkinter import messagebox
import matplotlib.pyplot as plt
import os


# action button open file
def openfile():
    global filepath
    filepath.set(askopenfilename(title="Open file", filetypes=[('u11 files', '.u11'), ('all files', '.*')]))
    return


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        plt.close('all')
        fenetre.destroy()
        quit()


def process():
    mylines = []
    try:
        charge1 = fonctions.readfile(filepath.get())
    except:
        messagebox.showerror("Error", "Wrong path")
        return
    global charge
    charge = [0]
    for x in range(len(charge1)):
        charge.append(charge1[x])
    isotope = entree2.get().upper().replace(" ", '')
    if isotope == '':
        messagebox.showerror("Error", "Please specify an isotope")
        return
    typeIso = combo.get()
    # print(typeIso)
    # print(isotope)
    value = []
    with open("Data/data.txt", "rt") as myfile:
        for myline in myfile:
            mylines.append(myline)
        # print(mylines[141])
        for x in range(len(mylines)):
            if mylines[x] == (isotope + "\n"):
                # print("boucle1")
                if mylines[x + 1] == (typeIso + "\n"):
                    # print("boucle2")
                    dat = mylines[x + 2].split(", ")
                    # print(dat)
                    for y in range(len(dat) - 1):
                        value.append(float(dat[y]))
    # print(value)
    # print(charge)
    global Valeur
    Valeur = fonctions.Result(isotope, 0, typeIso, value)
    # Valeur.printResult()
    plt1 = fonctions.plotfig(charge, Valeur)
    plt1.savefig("Data/graphnew.png")
    graph1 = PhotoImage(file='Data/graphnew.png')
    img = canvas.create_image(0, 0, anchor=NW, image=graph1)
    canvas.itemconfigure(img, image=graph1)
    text.set(Valeur.returnResult())
    return


# main window
fenetre = tk.Tk()
fenetre.title("Origen Data Compiler v1.0")
fenetre.geometry("1003x820+400+100")
fenetre.configure(bg='#cccccc')
fenetre.resizable(width=False, height=False)


def new_window(Win_class):
    global win2
    try:
        if win2.state() == "normal": win2.focus()
    except NameError as e:
        print(e)
        win2 = tk.Toplevel(fenetre)
        win2.resizable(width=False, height=False)
        win2.configure(bg='#cccccc')
        Win_class(win2)


class Win2:
    def __init__(self, root):
        self.root = root
        self.root.title("Save Current Plot")
        self.root.geometry("400x333+1410+100")
        self.lb1 = tk.Label(win2, text="Name : ", relief="groove", height=2, width=20)
        self.lb1.grid(row=0, column=0, sticky=W+E+N+S, padx=5, pady=5)
        self.lb2 = tk.Label(win2, text="Resolution (dpi) : ", relief="groove", height=2, width=20)
        self.lb2.grid(row=1, column=0, sticky=W+E+N+S, padx=5, pady=5)
        self.lb3 = tk.Label(win2, text="Width (in) : ", relief="groove", height=2, width=20)
        self.lb3.grid(row=2, column=0, sticky=W+E+N+S, padx=5, pady=5)
        self.lb4 = tk.Label(win2, text="Height (in) : ", relief="groove", height=2, width=20)
        self.lb4.grid(row=3, column=0, sticky=W+E+N+S, padx=5, pady=5)
        self.en1 = tk.Entry(win2, textvariable=str, text="", width=20)
        self.en1.grid(row=0, column=1, sticky=W+E+N+S, padx=5, pady=5)
        self.en2 = tk.Entry(win2, textvariable=int, text="", width=20)
        self.en2.grid(row=1, column=1, sticky=W+E+N+S, padx=5, pady=5)
        self.en3 = tk.Entry(win2, textvariable=float, text="", width=20)
        self.en3.grid(row=2, column=1, sticky=W+E+N+S, padx=5, pady=5)
        self.en4 = tk.Entry(win2, textvariable=float, text="", width=20)
        self.en4.grid(row=3, column=1, sticky=W+E+N+S, padx=5, pady=5)
        global case1value
        case1value = tk.BooleanVar()
        case1value.set(False)
        self.case1 = Checkbutton(win2, text="Log scale", var=case1value, width=20, bg='#cccccc')
        self.case1.grid(row=4, column=0, sticky=W+E+N+S, padx=5, pady=5)
        global case2value
        case2value = tk.BooleanVar()
        case2value.set(False)
        self.case2 = Checkbutton(win2, text="Show plot", var=case2value, width=20, bg='#cccccc')
        self.case2.grid(row=4, column=1, sticky=W+E+N+S, padx=5, pady=5)
        self.bt1 = tk.Button(win2, text="Default\nSettings", command=self.default, width=20, relief=RAISED, font=("Adobe Pi Std", 14, "bold"), bg='#c2c2d6')
        self.bt1.grid(row=5, column=0, sticky=W + E + N + S, padx=5, pady=5)
        self.bt2 = tk.Button(win2, text="Save", command=self.saveplot, width=20, relief=RAISED, font=("Adobe Pi Std", 14, "bold"), bg='#c2c2d6')
        self.bt2.grid(row=5, column=1, sticky=W + E + N + S, padx=5, pady=5)
        self.lb5 = tk.Label(win2, text="Info : plot is saved to program main directory", relief="groove", height=2, width=20)
        self.lb5.grid(row=6, column=0, columnspan=2, sticky=W + E + N + S, padx=5, pady=5)
        # self.root["bg"] = "navy"

    def default(self):
        self.en1.delete(0, "end")
        try:
            self.en1.insert(0, "plot" + str(Valeur.getIsotope()))
        except:
            self.en1.insert(0, "plot")
        self.en2.delete(0, "end")
        self.en2.insert(0, "100")
        self.en3.delete(0, "end")
        self.en3.insert(0, "9.9")
        self.en4.delete(0, "end")
        self.en4.insert(0, "5")

    def saveplot(self):
        # print("Log, at start of saveplot : " + str(case1value.get()))
        # print("Show, at start of saveplot : " + str(case2value.get()))
        name = self.en1.get()
        resolution = int(self.en2.get())
        width = float(self.en3.get())
        height = float(self.en4.get())
        plt.close('all')
        plt2 = fonctions.plotfig(charge, Valeur, width, height, resolution, case1value.get())
        if case2value.get():
            if not os.path.exists("Plots"):
                os.mkdir("Plots")
            plt2.savefig("Plots/" + name + ".png")
            plt2.show()
        # self.root.destroy()
        else:
            if not os.path.exists("Plots"):
                os.mkdir("Plots")
            plt2.savefig("Plots/" + name + ".png")
            messagebox.showinfo("Information", "PLot successfully saved")



# string containing chosen file path
filepath = StringVar()

# label with useful tips
label = Label(fenetre, text="Usefull tips :\t 1. First, select the file path of your data"
                            "\n\t\t 2. Select an predefined isotope, or write one"
                            "\n\t\t 3. Chose the desired class of isotope"
                            "\n\t\t 4. Process the graph by clicking de 'Process' button"
                            "\n\t\t 5. Reach advanced options and plot save by selecting the 'Save' menu", font=("Adobe Pi Std", 14, "italic"), relief="groove", justify=LEFT)
label.grid(row=0, column=0, columnspan=5, sticky=W+E+N+S, padx=5, pady=5)

# menu bar
menubar = Menu(fenetre)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=on_closing)
menubar.add_cascade(label="File", menu=filemenu)
savemenu = Menu(menubar, tearoff=0)
savemenu.add_command(label="Save Plot", command=lambda: new_window(Win2))
menubar.add_cascade(label="Save", menu=savemenu)
fenetre.config(menu=menubar)

# label file path
label1 = Label(fenetre, text="File path ", font=("Adobe Pi Std", 12), width=20, height=2, relief="groove")
label1.grid(row=1, column=0, sticky=W+E+N+S, padx=5, pady=5)

# entry file path
entree = Entry(fenetre, textvariable=str, text=filepath, font=("Adobe Pi Std", 12))
entree.grid(row=1, column=1, columnspan=2, sticky=W+E+N+S, padx=5, pady=5)

# button open file
bouton = Button(fenetre, text="Open file", command=openfile, width=20, relief=RAISED, font=("Adobe Pi Std", 14, "bold"), bg='#c2c2d6')
bouton.grid(row=1, column=3, sticky=W+E+N+S, padx=5, pady=5)
bouton1 = Button(fenetre, text="PROCESS GRAPH", command=process, width=20, relief=RAISED, font=("Adobe Pi Std", 18, "bold"), bg='#c2c2d6')
bouton1.grid(row=1, column=4, rowspan=2, sticky=W+E+N+S, padx=5, pady=5)

# Isotope selection
label2 = Label(fenetre, text="Element (ex: CO60 or U238)", width=20, height=2, relief="groove", font=("Adobe Pi Std", 11))
label2.grid(row=2, column=0, sticky=W+E+N+S, padx=5, pady=5)
# entree2 = Entry(fenetre, textvariable=str, text="", width=20)
# entree2.grid(row=2, column=1, sticky=W+E+N+S, padx=5, pady=5)
entree2 = ttk.Combobox(fenetre,
                       values=["U238",
                                    "Am241",
                                    "I131",
                                    "Cs137",
                                    "Co60"], font=("Adobe Pi Std", 12))
entree2.current(4)
entree2.grid(row=2, column=1, sticky=W+E+N+S, padx=5, pady=5)
label21 = Label(fenetre, text="Type", width=20, relief="groove", font=("Adobe Pi Std", 12))
label21.grid(row=2, column=2, sticky=W+E+N+S, padx=5, pady=5)
combo = ttk.Combobox(fenetre,
                     values=[
                                    "Activation Products",
                                    "Actinides + Daughters",
                                    "Fission Products",
                                    "(Alpha, N)",
                                    "Spontaneous Fiss. N. Source"], font=("Adobe Pi Std", 12))
combo.current(0)
combo.grid(row=2, column=3, sticky=W+E+N+S, padx=5, pady=5)

# graph canvas
# graph = PhotoImage(file='graph1.png')
canvas = Canvas(fenetre, width=990, height=500, relief=RAISED)
# canvas.create_image(0, 0, anchor=NW, image=graph)
canvas.grid(row=3, column=0, columnspan=5, padx=5, pady=5)

# out
text = StringVar()
label3 = Label(fenetre, textvariable=text, width=141, height=5, relief="groove", justify=LEFT)
text.set("Value...")
label3.grid(row=4, column=0, columnspan=5, sticky=W+N+S, padx=5, pady=5)

fenetre.protocol("WM_DELETE_WINDOW", on_closing)
fenetre.mainloop()
