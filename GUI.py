import sys
from tkinter import *
from tkinter import filedialog, messagebox

from PIL import ImageTk, Image

from matplotlib import pyplot as plt

from Clustering import Clustering
from Bayes import Bayes

root = Tk()
root.title("DaZZ Solver")
root.geometry("500x550")

print_geometry = "400x500"
# logo_image = ImageTk.PhotoImage(Image.open("logo.jpg"))  # 400x200
# logo_image_label = Label(root, image=logo_image)

logo_label = Label(root, text='************************** \n NEPODLIEHAJTE \n PANIKE! \n **************************',
                   font=('helvetica', 28, 'bold'))

version_label = Label(root, text='Verzia 0.0.3',
                   font=('helvetica', 8, 'bold'))
# all
csv_file_path: StringVar = StringVar()
# k-means
centroids: StringVar = StringVar()
# bayes
non_linguistic_variable: BooleanVar = BooleanVar()
# pre hierarchical clustering
hierarchical_clustering_list: list = ["Single linkage", "Complete linkage"]
used_method_h: StringVar = StringVar()
used_method_h.set(hierarchical_clustering_list[0])

# pre hlavné menu
method_type_list: list = ["Hierarchické zhlukovanie", "K-means", "Bayes", "K-cestný rozhodovací strom"]
used_method: StringVar = StringVar()
used_method.set(method_type_list[0])
method_label: Label = Label(root, text='Výber metódy', font=('helvetica', 11, 'bold'))


# vypnutie GUI
def on_exit() -> None:
    """
    vypnutie GUI
    """
    root.destroy()
    sys.exit()


# vypnutie GUI
root.protocol('WM_DELETE_WINDOW', on_exit)


def start_clustering() -> None:
    if used_method.get() == method_type_list[0]:
        hierarchical_clustering_window()
    elif used_method.get() == method_type_list[1]:
        k_means_method_window()
    elif used_method.get() == method_type_list[2]:
        bayes_method_window()
    elif used_method.get() == method_type_list[3]:
        messagebox.showinfo('TO DO', ' ¯\_(o_o)_/¯  \n TO DO')


def k_means_method_window() -> None:
    """
    GUI okno pre k-means
    """
    k_means = Toplevel()
    k_means.title('K-Means')
    k_means.geometry("400x400")

    csv_file_label: Label = Label(k_means, text='.csv alebo .txt súbor \n (variables x points) \n vzor v test.csv',
                                  font=('helvetica', 14, 'bold'))
    centroids_label: Label = Label(k_means, text='Zadaj body na inicializáciu centroidov \n napr: 1,2,3 (bez medzier)',
                                   font=('helvetica', 14, 'bold'))
    centroids_entry: Entry = Entry(k_means, borderwidth=5, font=('helvetica', 14, 'bold'),
                                   textvariable=centroids)
    csv_file_button = Button(k_means, text=".csv súbor", command=get_csv_file,
                             bg='green', fg='white', font=('helvetica', 14, 'bold'),
                             padx=20, pady=10, borderwidth=5)
    csv_file_start = Button(k_means, text="start", command=k_means_method,
                            bg='green', fg='white', font=('helvetica', 14, 'bold'),
                            padx=20, pady=10, borderwidth=5)
    csv_file_label.pack(anchor="center", pady=5)
    csv_file_button.pack(anchor="center", pady=5)
    centroids_label.pack(anchor="center", pady=5)
    centroids_entry.pack(anchor="center", pady=5)
    csv_file_start.pack(anchor="center", pady=5)


def k_means_method() -> None:
    """
    zavolá fuknciu na zhlukovanie a zobrazí výsledky
    :rtype: None
    """
    try:
        clu = Clustering()
        labels, centers = clu.k_means_clustering(csv_file_path.get(), centroids.get())

        top_200 = Toplevel()
        top_200.title('Clusters and centers')
        top_200.geometry(print_geometry)
        t = Text(top_200)
        s = Scrollbar(top_200)

        t.insert(END, "Priradenie bodov do zhlukov" + '\n')
        t.insert(END, str(labels) + '\n')
        t.insert(END, "--------------------------------------" + '\n')
        t.insert(END, "Súradnice stredov" + '\n')
        for c in centers:
            t.insert(END, str(c) + '\n')

        s.pack(side=RIGHT, fill=Y)
        t.pack(side=LEFT, fill=Y)

        s.config(command=t.yview)
        t.config(yscrollcommand=s.set)

    except ValueError as err:
        messagebox.showinfo('Error',
                            'Zadaj súradnice stredov alebo Súbor nie je v spravnom formáte - pozri test.csv \n' + str(
                                err))
    except FileNotFoundError as err:
        messagebox.showinfo('Error', 'Súbor sa nenašiel \n' + str(err))
    except IndexError as err:
        messagebox.showinfo('Error', 'Stredov je viac ako bodov alebo index bodu > počet bodov \n' + str(err))
    except Exception as err:
        messagebox.showinfo('Error', ' ¯\_(o_o)_/¯  \n' + str(err))


def bayes_method_window() -> None:
    """
    GUI pre bayes method
    :rtype: None
    """
    bayes = Toplevel()
    bayes.title('Bayes Method')
    bayes.geometry("400x400")
    xlsx_file_label: Label = Label(bayes,
                                   text='excel súbor (meno.xlsx) \n '
                                        'musí byť rovnaký ako vzor - bayes.xlsx \n '
                                        'na počte nezávislých atríbútov nezáleží \n '
                                        'na počte hodnôt nezáleží \n '
                                        'všetko musí byť na hárku 1',
                                   font=('helvetica', 14, 'bold'))
    min_priority_check_button = Checkbutton(bayes, text='Nelingvistické premenné (čísla)',
                                            font=('helvetica', 11, 'bold'), variable=non_linguistic_variable)
    csv_file_button = Button(bayes, text=".xlsx súbor", command=get_xlsx_file,
                             bg='green', fg='white', font=('helvetica', 14, 'bold'),
                             padx=20, pady=10, borderwidth=5)
    csv_file_start = Button(bayes, text="start", command=bayes_method,
                            bg='green', fg='white', font=('helvetica', 14, 'bold'),
                            padx=20, pady=10, borderwidth=5)
    xlsx_file_label.pack(anchor="center", pady=5)
    csv_file_button.pack(anchor="center", pady=5)
    min_priority_check_button.pack(anchor="center", pady=5)
    csv_file_start.pack(anchor="center", pady=5)


def bayes_method() -> None:
    try:
        bayes = Bayes()

        if non_linguistic_variable.get():
            # počítanie z nelingvistickými hodnotami
            messagebox.showinfo('TO DO', ' ¯\_(o_o)_/¯  \n TO DO')
        else:
            variable_list, citatel, norm, counts, counts_norm = bayes.count_bayes(csv_file_path.get())

            bayes_top = Toplevel()
            bayes_top.title('Čitateľ a Normalizácia')
            bayes_top.geometry(print_geometry)
            t = Text(bayes_top)
            s = Scrollbar(bayes_top)

            t.insert(END, "Ling   |   Čitateľ   |   Normalizácia" + '\n')
            t.insert(END, "-----------------------------------------" + '\n')
            for v, c, n in zip(variable_list, citatel, norm):
                t.insert(END, str(v) + ' | ' + str(c) + ' | ' + str(n) + '\n')
            t.insert(END, '\n')
            t.insert(END, "Keď násobým výsledok aj početnosťou výskitu" + '\n')
            t.insert(END, "Napr. koľko krát je low, hight z 10" + '\n')
            t.insert(END, '\n')
            t.insert(END, "Ling   |   Čitateľ   |   Normalizácia" + '\n')
            t.insert(END, "-----------------------------------------" + '\n')
            for v, c, n in zip(variable_list, counts, counts_norm):
                t.insert(END, str(v) + ' | ' + str(c) + ' | ' + str(n) + '\n')

            s.pack(side=RIGHT, fill=Y)
            t.pack(side=LEFT, fill=Y)

            s.config(command=t.yview)
            t.config(yscrollcommand=s.set)

    except FileNotFoundError as err:
        messagebox.showinfo('Error', 'Súbor sa nenašiel \n' + str(err))
    except IndexError as err:
        messagebox.showinfo('Error', 'Tabuľka je zle \n' + str(err))
    except Exception as err:
        messagebox.showinfo('Error', ' ¯\_(o_o)_/¯  \n' + str(err))


def hierarchical_clustering_window() -> None:
    """
    GUI okno pre hierarchical clustering
    """
    hierarchical = Toplevel()
    hierarchical.title('Hierarchical clustering')
    hierarchical.geometry("400x400")

    csv_file_label: Label = Label(hierarchical, text='.csv alebo .txt súbor \n (variables x points) \n vzor v test.csv',
                                  font=('helvetica', 14, 'bold'))
    csv_file_button = Button(hierarchical, text=".csv/txt súbor", command=get_csv_file,
                             bg='green', fg='white', font=('helvetica', 14, 'bold'),
                             padx=20, pady=10, borderwidth=5)

    method_label_h: Label = Label(hierarchical, text='Výber metódy',
                                  font=('helvetica', 14, 'bold'))

    method_drop_down_menu_h = OptionMenu(hierarchical, used_method_h, *hierarchical_clustering_list)

    start_button = Button(hierarchical, text="start", command=hierarchical_clustering,
                          bg='green', fg='white', font=('helvetica', 14, 'bold'),
                          padx=20, pady=10, borderwidth=5)

    csv_file_label.pack(anchor="center", pady=5)
    csv_file_button.pack(anchor="center", pady=5)
    method_label_h.pack(anchor="center", pady=5)
    method_drop_down_menu_h.pack(anchor="center", pady=5)
    method_drop_down_menu_h.config(font=('helvetica', 12, 'bold'), bg='green', fg='white',
                                   activebackground='green', activeforeground='black', width=27)
    start_button.pack(anchor="center", pady=5)


def hierarchical_clustering() -> None:
    """
    zavolá fuknciu na zhlukovanie a zobrazí výsledky/dendogram
    :rtype: None
    """
    try:
        c = Clustering()
        if used_method_h.get() == hierarchical_clustering_list[0]:
            hierarchical, dn, points_1, points_2 = c.hierarchical_clustering(csv_file_path.get(), True)
        else:
            hierarchical, dn, points_1, points_2 = c.hierarchical_clustering(csv_file_path.get(), False)

        top_h = Toplevel()
        top_h.title('Hierarchical clustering')
        top_h.geometry(print_geometry)
        t = Text(top_h)
        s = Scrollbar(top_h)

        #t.insert(END, "Priradenie 0 - A, 1 - B..." + '\n')
        t.insert(END, "--------------------------------------" + '\n')
        t.insert(END, "Spojené body  |  Vzdialenosť " + '\n')
        for h, p1, p2 in zip(hierarchical, points_1, points_2):
            t.insert(END, str(p1) + '-' + str(p2) + ' | ' + str(h) + '\n')
        t.insert(END, "--------------------------------------" + '\n')

        s.pack(side=RIGHT, fill=Y)
        t.pack(side=LEFT, fill=Y)

        s.config(command=t.yview)
        t.config(yscrollcommand=s.set)
        plt.show()

    except FileNotFoundError as err:
        messagebox.showinfo('Error', 'Súbor sa nenašiel \n' + str(err))
    except IndexError as err:
        messagebox.showinfo('Error', 'Tabuľka je zle \n' + str(err))
    except Exception as err:
        messagebox.showinfo('Error', ' ¯\_(o_o)_/¯  \n' + str(err))


# prerobiť aby to bola jedna funkcia
def get_csv_file() -> None:
    """
    otvorí prehladávanie preičinkov na nájdene csv súboru
    :rtype: None
    """
    root.filename = filedialog.askopenfilename(
        initialdir="",
        title="Select a file",
        filetypes=(("csv files", "*.csv"),
                   ("all files", "*.*")))
    csv_file_path.set(root.filename)
    t = Label(root, text=root.filename).pack(anchor="center")


def get_xlsx_file() -> None:
    """
    otvorí prehladávanie preičinkov na nájdene xlsx súboru
    :rtype: None
    """
    root.filename = filedialog.askopenfilename(
        initialdir="",
        title="Select a file",
        filetypes=(("xlsx files", "*.xlsx"),
                   ("all files", "*.*")))
    csv_file_path.set(root.filename)
    t = Label(root, text=root.filename).pack(anchor="center")


# #########################################################################
select_button = Button(root, text="Start", command=start_clustering,
                       bg='green', fg='white', font=('helvetica', 14, 'bold'),
                       padx=20, pady=10, borderwidth=5)

# logo_image_label.pack(anchor="center", pady=5)
logo_label.pack(anchor="center", pady=30)

method_label.pack(anchor="center", pady=5)
method_drop_down_menu = OptionMenu(root, used_method, *method_type_list)
method_drop_down_menu.pack(anchor="center", pady=5)
method_drop_down_menu.config(font=('helvetica', 12, 'bold'), bg='green', fg='white',
                             activebackground='green', activeforeground='black', width=27)

select_button.pack(anchor="center", pady=30, padx=5)
version_label.pack(anchor="se", pady=15, padx=30)

root.mainloop()
