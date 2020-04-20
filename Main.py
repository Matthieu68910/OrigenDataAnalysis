# -*- coding: utf-8 -*-

'''Origen Data Analysis v1.0.0-beta
   author : Matthieu Duflot
   student at ISIB - BRUXELLES
   mail : duflotmatthieu1@gmail.com
   pre-release date : 20 april 2020'''

import tkinter as tk
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib import ticker
from win32api import GetSystemMetrics
from PIL import Image, ImageTk
import ctypes
import re
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter)

# variables
version = "OrigenDA v1.0.0-beta"
sys_width = GetSystemMetrics(0)
sys_height = GetSystemMetrics(1)
main_window_width = 0
main_window_height = 0
start_x_pos = 0
start_y_pos = 0
bg_color = '#cccccc'

data = []
charge_num = []
all_elements = []
all_isotopes = []

# set starting positions for high res screens
if sys_width > 1290 and sys_height > 730:
    start_x_pos = (sys_width / 2) - 640
    start_y_pos = (sys_height / 2) - 360

# main frame
main_window = tk.Tk()
main_window.title(version)
main_window.geometry("%dx%d+%d+%d" % (1240, 640, start_x_pos, start_y_pos))
main_window.configure(bg=bg_color)
main_window.resizable(width=False, height=False)


def openfile():
    global file_path
    file_path.set(askopenfilename(title="Open file", filetypes=[('u11 files', '.u11'), ('all files', '.*')]))
    return


def process_file():
    mylines = []  # lines of the file
    balise = [[], [], [], [], []]  # balise au format (1000 + line)
    global data, all_elements, all_isotopes, charge_num

    if file_path.get() == "":
        messagebox.showerror("Error", "Please select a file first")
        return
    try:
        with open(file_path.get(), "rt") as myfile:
            pass
    except FileNotFoundError:
        messagebox.showerror("Error", "Wrong file path, please select a .txt or .u11 file")
        return
    with open(file_path.get(), "rt") as myfile:  # file read
        for myline in myfile:
            mylines.append(myline)
        for x in range(len(mylines)):  # localisation of strips
            if mylines[x].find("ACTIVATION PRODUCT", 98, 120) != -1:
                balise[0].append(x)
            elif mylines[x].find("ACTINIDES+DAUGHTERS", 98, 120) != -1:
                balise[1].append(x)
            elif mylines[x].find("FISSION PRODUCTS", 98, 120) != -1:
                balise[2].append(x)
            elif mylines[x].find("(ALPHA,N)", 27, 40) != -1:
                balise[3].append(x)
            elif mylines[x].find("FISSION NEUTRON SOURCE", 40, 65) != -1:
                balise[4].append(x)
            else:
                pass
        for y in range(len(mylines)):  # recovery of CHARGE
            if mylines[y].find("CHARGE", 10, 20) != -1:
                line = mylines[y].replace("CHARGE", '')
                charge = line.split()
                for z in range(len(charge)):
                    if charge[z].find('D') != -1:
                        a = charge[z].replace("D", '')
                        charge_num.append(float(a))
                    elif charge[z].find('YR') != -1:
                        a = charge[z].replace("YR", '')
                        charge_num.append((float(a) * 365) + 600)
                break
        ctypes.windll.kernel32.SetFileAttributesW('data.txt', 0)
        f = open("data.txt", "w+")
        for z in range(len(mylines)):
            if balise[0][0] <= z <= balise[1][0]:
                if mylines[z][1:3] != "  " and mylines[z][0:6] != "ORIGEN" \
                        and mylines[z] != "\n" \
                        and mylines[z][0:3] != "---" \
                        and mylines[z][0:6] != "TOTALS" \
                        and mylines[z][0:6] != "OVERAL" \
                        and mylines[z][0:8] != "BASIS=ON" \
                        and mylines[z][0:5] != "TABLE" \
                        and mylines[z][0:6] != "ACTUAL" \
                        and mylines[z][0:1] != "":
                    isotope = mylines[z][0:10].replace(' ', '')
                    value = mylines[z][10:].split()
                    f.write(isotope + "\nActivation Products\n")
                    for x in value:
                        f.write(str(x) + ", ")
                    f.write("\n")
                    sep = re.match(r"(?P<element>[a-zA-Z]+)(?P<isotope>.+)$", isotope)
                    contains_digit = False
                    for character in isotope:
                        if character.isdigit():
                            contains_digit = True
                    if contains_digit:
                        elem = sep.group('element')
                        if len(elem) > 1:
                            elem1 = elem.lower()
                            elem2 = elem1[0].upper() + elem1[1:]
                        else:
                            elem2 = elem.upper()
                        iso = sep.group('isotope').lower()
                    else:
                        elem = isotope
                        if len(elem) > 1:
                            elem1 = elem.lower()
                            elem2 = elem1[0].upper() + elem1[1:]
                        else:
                            elem2 = elem.upper()
                        iso = ""
                    new = [1, elem2, iso, value]
                    data.append(new)
            if balise[1][0] <= z <= balise[2][0]:
                if mylines[z][1:3] != "  " and mylines[z][0:6] != "ORIGEN" \
                        and mylines[z] != "\n" \
                        and mylines[z][0:3] != "---" \
                        and mylines[z][0:6] != "TOTALS" \
                        and mylines[z][0:6] != "OVERAL" \
                        and mylines[z][0:8] != "BASIS=ON" \
                        and mylines[z][0:5] != "TABLE" \
                        and mylines[z][0:6] != "ACTUAL" \
                        and mylines[z][0:1] != "":
                    isotope = mylines[z][0:10].replace(' ', '')
                    value = mylines[z][10:].split()
                    f.write(isotope + "\nActinides + Daughters\n")
                    for x in value:
                        f.write(str(x) + ", ")
                    f.write("\n")
                    sep = re.match(r"(?P<element>[a-zA-Z]+)(?P<isotope>.+)$", isotope)
                    contains_digit = False
                    for character in isotope:
                        if character.isdigit():
                            contains_digit = True
                    if contains_digit:
                        elem = sep.group('element')
                        if len(elem) > 1:
                            elem1 = elem.lower()
                            elem2 = elem1[0].upper() + elem1[1:]
                        else:
                            elem2 = elem.upper()
                        iso = sep.group('isotope').lower()
                    else:
                        elem = isotope
                        if len(elem) > 1:
                            elem1 = elem.lower()
                            elem2 = elem1[0].upper() + elem1[1:]
                        else:
                            elem2 = elem.upper()
                        iso = ""
                    new = [2, elem2, iso, value]
                    data.append(new)
            if balise[2][0] <= z <= balise[3][0]:
                if mylines[z][1:3] != "  " and mylines[z][0:6] != "ORIGEN" \
                        and mylines[z] != "\n" \
                        and mylines[z][0:3] != "---" \
                        and mylines[z][0:6] != "TOTALS" \
                        and mylines[z][0:6] != "OVERAL" \
                        and mylines[z][0:8] != "BASIS=ON" \
                        and mylines[z][0:5] != "TABLE" \
                        and mylines[z][0:6] != "ACTUAL" \
                        and mylines[z][0:1] != "":
                    isotope = mylines[z][0:10].replace(' ', '')
                    value = mylines[z][10:].split()
                    f.write(isotope + "\nFission Products\n")
                    for x in value:
                        f.write(str(x) + ", ")
                    f.write("\n")
                    sep = re.match(r"(?P<element>[a-zA-Z]+)(?P<isotope>.+)$", isotope)
                    contains_digit = False
                    for character in isotope:
                        if character.isdigit():
                            contains_digit = True
                    if contains_digit:
                        elem = sep.group('element')
                        if len(elem) > 1:
                            elem1 = elem.lower()
                            elem2 = elem1[0].upper() + elem1[1:]
                        else:
                            elem2 = elem.upper()
                        iso = sep.group('isotope').lower()
                    else:
                        elem = isotope
                        if len(elem) > 1:
                            elem1 = elem.lower()
                            elem2 = elem1[0].upper() + elem1[1:]
                        else:
                            elem2 = elem.upper()
                        iso = ""
                    new = [3, elem2, iso, value]
                    data.append(new)
            if balise[3][0] <= z <= balise[4][0]:
                if mylines[z][1:3] != "  " and mylines[z][0:6] != "ORIGEN" \
                        and mylines[z] != "\n" \
                        and mylines[z][0:3] != "---" \
                        and mylines[z][0:6] != "TOTALS" \
                        and mylines[z][0:6] != "OVERAL" \
                        and mylines[z][0:5] != "BASIS" \
                        and mylines[z][0:5] != "TABLE" \
                        and mylines[z][0:6] != "ACTUAL" \
                        and mylines[z][0:1] != "":
                    isotope = mylines[z][0:10].replace(' ', '')
                    value = mylines[z][10:].split()
                    f.write(isotope + "\n(Alpha, N)\n")
                    for x in value:
                        f.write(str(x) + ", ")
                    f.write("\n")
                    sep = re.match(r"(?P<element>[a-zA-Z]+)(?P<isotope>.+)$", isotope)
                    contains_digit = False
                    for character in isotope:
                        if character.isdigit():
                            contains_digit = True
                    if contains_digit:
                        elem = sep.group('element')
                        if len(elem) > 1:
                            elem1 = elem.lower()
                            elem2 = elem1[0].upper() + elem1[1:]
                        else:
                            elem2 = elem.upper()
                        iso = sep.group('isotope').lower()
                    else:
                        elem = isotope
                        if len(elem) > 1:
                            elem1 = elem.lower()
                            elem2 = elem1[0].upper() + elem1[1:]
                        else:
                            elem2 = elem.upper()
                        iso = ""
                    new = [4, elem2, iso, value]
                    data.append(new)
            if balise[4][0] < z:
                if mylines[z][1:3] != "  " and mylines[z][0:6] != "ORIGEN" \
                        and mylines[z] != "\n" \
                        and mylines[z][0:3] != "---" \
                        and mylines[z][0:6] != "TOTALS" \
                        and mylines[z][0:6] != "OVERAL" \
                        and mylines[z][0:8] != "BASIS=ON" \
                        and mylines[z][0:5] != "TABLE" \
                        and mylines[z][0:6] != "ACTUAL" \
                        and mylines[z][0:1] != "":
                    isotope = mylines[z][0:10].replace(' ', '')
                    value = mylines[z][10:].split()
                    f.write(isotope + "\nSpontaneous Fiss. N. Source\n")
                    for x in value:
                        f.write(str(x) + ", ")
                    f.write("\n")
                    sep = re.match(r"(?P<element>[a-zA-Z]+)(?P<isotope>.+)$", isotope)
                    contains_digit = False
                    for character in isotope:
                        if character.isdigit():
                            contains_digit = True
                    if contains_digit:
                        elem = sep.group('element')
                        if len(elem) > 1:
                            elem1 = elem.lower()
                            elem2 = elem1[0].upper() + elem1[1:]
                        else:
                            elem2 = elem.upper()
                        iso = sep.group('isotope').lower()
                    else:
                        elem = isotope
                        if len(elem) > 1:
                            elem1 = elem.lower()
                            elem2 = elem1[0].upper() + elem1[1:]
                        else:
                            elem2 = elem.upper()
                        iso = ""
                    new = [5, elem2, iso, value]
                    data.append(new)
        f.close()
    ctypes.windll.kernel32.SetFileAttributesW('data.txt', 2)
    list_of_elements = []
    for vector in data:
        element = str(vector[1])
        element1 = element.lower()
        if len(element1) > 1:
            element2 = element1[0].upper() + element1[1:]
        else:
            element2 = element1.upper()
        list_of_elements.append(element2)
    list_of_elements = list(dict.fromkeys(list_of_elements))
    combobox_element["values"] = list_of_elements

    for vector in data:
        element = str(vector[1])
        element1 = element.lower()
        if len(element1) > 1:
            element2 = element1[0].upper() + element1[1:]
        else:
            element2 = element1.upper()
        all_elements.append(element2)
        isotope = element2 + str(vector[2])
        all_isotopes.append(isotope)
    all_elements = list(dict.fromkeys(all_elements))
    all_isotopes = list(dict.fromkeys(all_isotopes))
    text = "File successfully processed ! " + str(len(all_elements)) + " elements, and " + str(len(all_isotopes)) + " isotopes found."
    file_info.set(text)
    return


def process_plot():
    recherche = combobox_isotope.get()
    type_recherche = combobox_origin.get()
    values_for_graph = []
    if type_recherche == "Activation Products":
        pos = 1
    elif type_recherche == "Actinides + Daughters":
        pos = 2
    elif type_recherche == "Fission Products":
        pos = 3
    elif type_recherche == "(Alpha, N)":
        pos = 4
    elif type_recherche == "Spontaneous Fiss. N. Source":
        pos = 5
    else:
        return
    data_new = []
    for vector in data:
        if vector[0] == pos:
            data_new.append(vector)
    for vector in data_new:
        iso = str(vector[1]) + str(vector[2])
        if iso == recherche:
            values_for_graph = vector[3]
    values_num = []
    for x in values_for_graph:
        values_num.append(float(x))
    plot_fig(recherche, type_recherche, charge_num, values_num, 100, 9.4, 4.6, case_value_xlog.get(), case_value_ylog.get())
    img1 = ImageTk.PhotoImage(Image.open("graphnew.jpg"))
    canvas.configure(image=img1)
    canvas.image = img1
    return


def plot_fig(title, lab, x_data, y_data, res=100, width=9.4, height=4.6, x_log=False, y_log=False, save=True):
    title1 = title[0] + title[1:].lower()
    sep = re.match(r"(?P<element>[a-zA-Z]+)(?P<isotope>.+)$", title1)
    contains_digit = False
    for character in title1:
        if character.isdigit():
            contains_digit = True
    if contains_digit:
        elem = sep.group('element')
        iso = sep.group('isotope')
    else:
        elem = title1
        iso = ""
    title2 = r'${}^{%s}$%s' % (iso, elem)

    plt.close('all')
    alerte = False
    if len(x_data) != len(y_data):
        x_data.insert(0, 0)
    for x in range(len(y_data)):
        if y_data[x] < 1E-12:
            y_data[x] = 1E-12
            alerte = True

    plt.figure(figsize=(width, height), dpi=res)
    axes = plt.gca()
    plt.plot(x_data, y_data, label=title2)
    plt.axvline(600, 0, 1, label='Reactor stopped', color='g')
    if x_log:
        plt.xscale('log')
        axes.set_xlim([1E-03, (2 * max(x_data))])
    else:
        plt.xscale('linear')
        axes.set_xlim(0, max(x_data))
    if y_log:
        plt.yscale('log')
        if min(y_data) < 1E-09:
            axes.set_ylim([1E-09, (10 * max(y_data))])
        else:
            axes.set_ylim([min(y_data), (10 * max(y_data))])
    else:
        plt.yscale('linear')
        axes.set_ylim([min(y_data) - (0.1 * min(y_data)), (max(y_data) + (0.1 * max(y_data)))])
    plt.title("Evolution of " + title2 + " - " + lab)
    plt.xlabel("Duration (days)")
    if lab == "(Alpha, N)" or lab == "Spontaneous Fiss. N. Source":
        plt.ylabel("Neutrons / sec")
    else:
        plt.ylabel("Mass (g)")
    if not x_log:
        axes.xaxis.set_major_locator(MultipleLocator(365))
        axes.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        axes.xaxis.set_minor_locator(MultipleLocator(30.41666))
    else:
        axes.xaxis.set_major_formatter(FormatStrFormatter('%10.1e'))
    if not y_log:
        axes.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    else:
        axes.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, numticks=15))
    axes.tick_params(which='major', width=2)
    axes.tick_params(which='minor', width=1)
    axes.tick_params(which='major', length=7)
    axes.tick_params(which='minor', length=4, color='darkblue')
    plt.grid(b=True, which='major', color='black', linestyle='-')
    plt.grid(b=True, which='minor', color='darkblue', linestyle='-', alpha=0.2)
    plt.minorticks_on()
    plt.figtext(0.01, 0.01, 'Data from Origen22', size=6, horizontalalignment='left')
    plt.figtext(0.99, 0.01, 'Graph from OrigenDA v1.0.0', size=6, horizontalalignment='right')
    plt.legend()

    if save:
        plt.savefig("graphnew.jpg", quality=95)
    else:
        return plt
    plt.close('all')
    if alerte:
        graph_info.set("Infos:\t- Y-axis inferior limit set to 10E-12")
    return


def save_show_plot():
    title = entry_save_name.get()
    recherche = combobox_isotope.get()
    type_recherche = combobox_origin.get()
    values_for_graph = []
    if type_recherche == "Activation Products":
        pos = 1
    elif type_recherche == "Actinides + Daughters":
        pos = 2
    elif type_recherche == "Fission Products":
        pos = 3
    elif type_recherche == "(Alpha, N)":
        pos = 4
    elif type_recherche == "Spontaneous Fiss. N. Source":
        pos = 5
    else:
        return
    data_new = []
    for vector in data:
        if vector[0] == pos:
            data_new.append(vector)
    for vector in data_new:
        iso = str(vector[1]) + str(vector[2])
        if iso == recherche:
            values_for_graph = vector[3]
    values_num = []
    for x in values_for_graph:
        values_num.append(float(x))
    plot = plot_fig(recherche, type_recherche, charge_num, values_num, int(entry_save_resolution.get()), float(entry_save_width.get()), float(entry_save_height.get()), case_save_logx.get(), case_save_logy.get(), False)
    plot.show()
    return


def save_save_plot():
    title = entry_save_name.get()
    recherche = combobox_isotope.get()
    type_recherche = combobox_origin.get()
    values_for_graph = []
    if type_recherche == "Activation Products":
        pos = 1
    elif type_recherche == "Actinides + Daughters":
        pos = 2
    elif type_recherche == "Fission Products":
        pos = 3
    elif type_recherche == "(Alpha, N)":
        pos = 4
    elif type_recherche == "Spontaneous Fiss. N. Source":
        pos = 5
    else:
        return
    data_new = []
    for vector in data:
        if vector[0] == pos:
            data_new.append(vector)
    for vector in data_new:
        iso = str(vector[1]) + str(vector[2])
        if iso == recherche:
            values_for_graph = vector[3]
    values_num = []
    for x in values_for_graph:
        values_num.append(float(x))
    plot = plot_fig(recherche, type_recherche, charge_num, values_num, int(entry_save_resolution.get()), float(entry_save_width.get()), float(entry_save_height.get()), case_save_logx.get(), case_save_logy.get(), False)
    plot.savefig((str(title) + ".jpg"), quality=95)
    plt.close('all')
    messagebox.showinfo("Information", "Plot successfully saved")
    return


def combobox_element_function():
    combobox_isotope["state"] = ["readonly"]
    return


def combobox_isotope_function():
    if combobox_element.get() != "":
        element = combobox_element.get()
        new_values = []
        for vector in data:
            if vector[1] == element:
                x = str(vector[1]) + str(vector[2])
                new_values.append(x)
        new_values = list(dict.fromkeys(new_values))
        new_values.sort()
        combobox_isotope["values"] = new_values
        combobox_origin["state"] = ["readonly"]
    return


def combobox_origin_function():
    if combobox_isotope.get() != "":
        isotope = combobox_isotope.get()
        new_values = []
        for vector in data:
            x = str(vector[1]) + str(vector[2])
            if x == isotope:
                if vector[0] == 1:
                    typ = "Activation Products"
                elif vector[0] == 2:
                    typ = "Actinides + Daughters"
                elif vector[0] == 3:
                    typ = "Fission Products"
                elif vector[0] == 4:
                    typ = "(Alpha, N)"
                elif vector[0] == 5:
                    typ = "Spontaneous Fiss. N. Source"
                else:
                    typ = "Unknown"
                new_values.append(str(typ))
        new_values = list(dict.fromkeys(new_values))
        new_values.sort()
        combobox_origin["values"] = new_values
        button_graph_process["state"] = ["normal"]
        button_save_save["state"] = ["normal"]
        button_save_default["state"] = ["normal"]
        button_save_show["state"] = ["normal"]
    return


def check_graph_function1():
    check_graph_xlog.toggle()
    return


def check_graph_function2():
    check_graph_xlin.toggle()
    return


def check_graph_function3():
    check_graph_ylog.toggle()
    return


def check_graph_function4():
    check_graph_ylin.toggle()
    return


def save_default_settings():
    title = "graph_" + str(combobox_isotope.get())
    save_name.set(title)
    save_resolution.set("100")
    save_width.set("10.00")
    save_height.set("5.00")
    case_save_logx.set(False)
    case_save_logy.set(True)
    return


# create all containers
tips_frame = Frame(main_window, bg=bg_color, width=1234, height=23, borderwidth=2, relief="groove")
file_frame = Frame(main_window, bg=bg_color, width=1234, height=32, borderwidth=2, relief="groove")
graph_frame = Frame(main_window, bg=bg_color, width=1234, height=485)
save_frame = Frame(main_window, bg=bg_color, width=1234, height=65, borderwidth=2, relief="groove")

# layout all of the containers
main_window.grid_rowconfigure(1, weight=1)
main_window.grid_columnconfigure(0, weight=1)

# save frame widgets
save_name = StringVar()
save_resolution = StringVar()
save_resolution.set("100")
save_width = StringVar()
save_width.set("10.00")
save_height = StringVar()
save_height.set("5.00")

label_save_title = Label(save_frame, text="Save Plot", font=("Adobe Pi Std", 16, "bold"), width=25, height=2, relief="ridge", bg=bg_color)
label_save_name = Label(save_frame, text="Name:", font=("Adobe Pi Std", 12), width=15, height=1, relief="groove", bg=bg_color)
label_save_resolution = Label(save_frame, text="Res. (dpi):", font=("Adobe Pi Std", 12), width=15, height=1, relief="groove", bg=bg_color)
entry_save_name = Entry(save_frame, textvariable=str, text=save_name, font=("Adobe Pi Std", 12), width=15)
entry_save_resolution = Entry(save_frame, textvariable=str, text=save_resolution, font=("Adobe Pi Std", 12), width=15)
label_save_width = Label(save_frame, text="Width (inch):", font=("Adobe Pi Std", 12), width=15, height=1, relief="groove", bg=bg_color)
label_save_height = Label(save_frame, text="Height (inch):", font=("Adobe Pi Std", 12), width=15, height=1, relief="groove", bg=bg_color)
entry_save_width = Entry(save_frame, textvariable=str, text=save_width, font=("Adobe Pi Std", 12), width=10)
entry_save_height = Entry(save_frame, textvariable=str, text=save_height, font=("Adobe Pi Std", 12), width=10)
label_save_scale = Label(save_frame, text="X-Log Scale:", font=("Adobe Pi Std", 12), width=15, height=1, relief="groove", bg=bg_color)
label_save_show = Label(save_frame, text="Y-Log Scale:", font=("Adobe Pi Std", 12), width=15, height=1, relief="groove", bg=bg_color)
case_save_logx = tk.BooleanVar()
case_save_logx.set(False)
check_save_logx = Checkbutton(save_frame, text="", var=case_save_logx, width=3, relief="groove", bg=bg_color)
case_save_logy = tk.BooleanVar()
case_save_logy.set(True)
check_save_logy = Checkbutton(save_frame, text="", var=case_save_logy, width=3, relief="groove", bg=bg_color)
case_save_quick = tk.BooleanVar()
case_save_quick.set(False)
check_save_quick = Checkbutton(save_frame, text="Quick Save Plot", var=case_save_quick, width=20, relief="groove", bg=bg_color)
button_save_default = Button(save_frame, text="Set Default Settings", command=save_default_settings, state="disable", width=20, relief=RAISED, font=("Adobe Pi Std", 12, "bold"), bg='#c2c2d6')
button_save_show = Button(save_frame, text="Show Plot", command=save_show_plot, state="disable", width=20, relief=RAISED, font=("Adobe Pi Std", 12, "bold"), bg='#c2c2d6')
button_save_save = Button(save_frame, text="Save Plot", command=save_save_plot, state="disable", width=20, relief=RAISED, font=("Adobe Pi Std", 12, "bold"), bg='#c2c2d6')


label_save_title.grid(row=0, column=0, rowspan=2, sticky=W+E+N+S, padx=3, pady=3)
label_save_name.grid(row=0, column=1, sticky=W+E+N+S, padx=3, pady=3)
label_save_resolution.grid(row=1, column=1, sticky=W+E+N+S, padx=3, pady=3)
entry_save_name.grid(row=0, column=2, sticky=W+E+N+S, padx=3, pady=3)
entry_save_resolution.grid(row=1, column=2, sticky=W+E+N+S, padx=3, pady=3)
label_save_width.grid(row=0, column=3, sticky=W+E+N+S, padx=3, pady=3)
label_save_height.grid(row=1, column=3, sticky=W+E+N+S, padx=3, pady=3)
entry_save_width.grid(row=0, column=4, sticky=W+E+N+S, padx=3, pady=3)
entry_save_height.grid(row=1, column=4, sticky=W+E+N+S, padx=3, pady=3)
label_save_scale.grid(row=0, column=5, sticky=W+E+N+S, padx=3, pady=3)
label_save_show.grid(row=1, column=5, sticky=W+E+N+S, padx=3, pady=3)
check_save_logx.grid(row=0, column=6, sticky=W+E+N+S, padx=3, pady=3)
check_save_logy.grid(row=1, column=6, sticky=W+E+N+S, padx=3, pady=3)
check_save_quick.grid(row=0, column=7, sticky=W+E+N+S, padx=3, pady=3)
button_save_default.grid(row=1, column=7, sticky=W+E+N+S, padx=3, pady=3)
button_save_show.grid(row=0, column=8, sticky=W+E+N+S, padx=3, pady=3)
button_save_save.grid(row=1, column=8, sticky=W+E+N+S, padx=3, pady=3)

tips_frame.grid(row=0, sticky="nsew", padx=3, pady=3)
file_frame.grid(row=1, sticky="nsew", padx=3, pady=3)
graph_frame.grid(row=2, sticky="nwe", padx=3, pady=3)
save_frame.grid(row=3, sticky="nsew", padx=3, pady=3)

# create file frame widgets
file_path = StringVar()
file_info = StringVar()

label_file = Label(file_frame, text="File path:", font=("Adobe Pi Std", 12), width=15, height=1, relief="groove", bg=bg_color)
entry_file = Entry(file_frame, textvariable=str, text=file_path, font=("Adobe Pi Std", 12), width=61)
button_file = Button(file_frame, text="Open file", command=openfile, width=15, relief=RAISED, font=("Adobe Pi Std", 12, "bold"), bg='#c2c2d6')
button_file_process = Button(file_frame, text="Process file", command=process_file, width=15, relief=RAISED, font=("Adobe Pi Std", 12, "bold"), bg='#c2c2d6')
label_file_info = Label(file_frame, textvar=file_info, anchor="w", font=("Adobe Pi Std", 12), width=56, height=1, relief="groove", bg=bg_color)

label_file.grid(row=0, column=1, sticky=W+E+N+S, padx=3, pady=6)
entry_file.grid(row=0, column=2, sticky=W+E+N+S, padx=3, pady=6)
button_file.grid(row=0, column=0, sticky=W+E+N+S, padx=3, pady=6)
button_file_process.grid(row=0, column=3, sticky=W+E+N+S, padx=3, pady=6)
label_file_info.grid(row=0, column=4, sticky=W+E+N+S, padx=3, pady=6)

# create graph frames
graph_frame.grid_rowconfigure(0, weight=1)
graph_frame.grid_columnconfigure(1, weight=1)

graph_frame_control = Frame(graph_frame, bg=bg_color, width=228, height=478, padx=3, borderwidth=2, relief="groove")
graph_frame_plot = Frame(graph_frame, bg=bg_color, width=1000, height=478, padx=0, borderwidth=1, relief="sunken")

# create graph control widgets
combobox_element_values = []
combobox_isotope_values = []
combobox_origin_values = []
label_graph_element = Label(graph_frame_control, text="Element:", font=("Adobe Pi Std", 12), width=10, height=1, relief="groove", bg=bg_color)
label_graph_isotope = Label(graph_frame_control, text="Isotope:", font=("Adobe Pi Std", 12), width=10, height=1, relief="groove", bg=bg_color)
label_graph_origin = Label(graph_frame_control, text="Origin:", font=("Adobe Pi Std", 12), width=10, height=1, relief="groove", bg=bg_color)
combobox_element = ttk.Combobox(graph_frame_control, values=combobox_element_values, state="enable", postcommand=combobox_element_function)
combobox_isotope = ttk.Combobox(graph_frame_control, values=combobox_isotope_values, state="disable", postcommand=combobox_isotope_function)
combobox_origin = ttk.Combobox(graph_frame_control, values=combobox_origin_values, state="disable", postcommand=combobox_origin_function)
button_graph_process = Button(graph_frame_control, text="Process Plot", state="disable", command=process_plot, width=15, relief=RAISED, font=("Adobe Pi Std", 12, "bold"), bg='#c2c2d6')
label_graph_xaxis = Label(graph_frame_control, text="X-axis scale", font=("Adobe Pi Std", 12), width=10, height=1, relief="groove", bg=bg_color)
label_graph_yaxis = Label(graph_frame_control, text="Y-axis scale", font=("Adobe Pi Std", 12), width=10, height=1, relief="groove", bg=bg_color)
case_value_xlin = tk.BooleanVar()
case_value_xlin.set(True)
check_graph_xlin = Checkbutton(graph_frame_control, text="Linear", var=case_value_xlin, command=check_graph_function1, width=12, bg='#cccccc')
case_value_xlog = tk.BooleanVar()
case_value_xlog.set(False)
check_graph_xlog = Checkbutton(graph_frame_control, text="Log", var=case_value_xlog, command=check_graph_function2, width=12, bg='#cccccc')
case_value_ylin = tk.BooleanVar()
case_value_ylin.set(True)
check_graph_ylin = Checkbutton(graph_frame_control, text="Linear", var=case_value_ylin, command=check_graph_function3, width=12, bg='#cccccc')
case_value_ylog = tk.BooleanVar()
case_value_ylog.set(False)
check_graph_ylog = Checkbutton(graph_frame_control, text="Log", var=case_value_ylog, command=check_graph_function4, width=12, bg='#cccccc')
graph_info = StringVar()
graph_info.set("Info:")
label_graph_info = Label(graph_frame_control, textvar=graph_info, font=("Adobe Pi Std", 12), width=15, height=8, relief="groove", bg=bg_color, anchor="nw", justify=LEFT)
label_graph_title = Label(graph_frame_control, text="Plot Settings", font=("Adobe Pi Std", 16, "bold"), width=15, height=2, relief="ridge", bg=bg_color)

label_graph_title.grid(row=0, column=0, columnspan=2, sticky=W+E+N+S, padx=3, pady=10)
label_graph_element.grid(row=1, column=0, sticky=W+E+N+S, padx=3, pady=3)
label_graph_isotope.grid(row=2, column=0, sticky=W+E+N+S, padx=3, pady=3)
label_graph_origin.grid(row=3, column=0, sticky=W+E+N+S, padx=3, pady=3)
combobox_element.grid(row=1, column=1)
combobox_isotope.grid(row=2, column=1)
combobox_origin.grid(row=3, column=1)
label_graph_xaxis.grid(row=4, column=0, columnspan=2, sticky=W+E+N+S, padx=3, pady=4)
check_graph_xlin.grid(row=5, column=0, sticky=W+E+N+S, padx=3, pady=3)
check_graph_xlog.grid(row=5, column=1, sticky=W+E+N+S, padx=3, pady=3)
label_graph_yaxis.grid(row=6, column=0, columnspan=2, sticky=W+E+N+S, padx=3, pady=3)
check_graph_ylin.grid(row=7, column=0, sticky=W+E+N, padx=3, pady=3)
check_graph_ylog.grid(row=7, column=1, sticky=W+E+N, padx=3, pady=3)
label_graph_info.grid(row=8, column=0, columnspan=2, sticky=W+E+N+S, padx=3, pady=10)
button_graph_process.grid(row=9, column=0, columnspan=2, sticky=W+E+S, padx=3, pady=10)

# create canvas for plot
base = ImageTk.PhotoImage(Image.new('RGB', (940, 459), color='white'))
canvas = Label(graph_frame_plot, image=base, width=940, height=460, relief=RAISED)  # 947 x 465
canvas.grid(row=0, column=0, padx=6, sticky="nsew", pady=5)


graph_frame_control.grid(row=0, column=0, sticky="new")
graph_frame_plot.grid(row=0, column=1, sticky="e")

main_window.mainloop()
