import sys
from tkinter import *
from tkinter import filedialog, messagebox

from PIL import ImageTk, Image

from Clustering import Clustering

root = Tk()
root.title("DaZZ Solver App")
root.geometry("500x550")

print_geometry = "400x500"
logo_image = ImageTk.PhotoImage(Image.open("logo.jpg"))  # 400x200
logo_image_label = Label(root, image=logo_image)

csv_file_path: StringVar = StringVar()
centroids: StringVar = StringVar()


method_type_list: list = ["K-means", "Bayes"]
used_method: StringVar = StringVar()
used_method.set(method_type_list[0])
method_label = Label(root, text='Výber metódy', font=('helvetica', 11, 'bold'))


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
        k_means_method_window()
    elif used_method.get() == method_type_list[1]:
        bayes_method_window()


def k_means_method_window() -> None:
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
        messagebox.showinfo('Error', ' -\(o,o)/-  \n' + str(err))


def bayes_method_window() -> None:
    messagebox.showinfo('TO DO', ' -\(o,o)/-  \n TO DO')


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


select_button = Button(root, text="Start", command=start_clustering,
                       bg='green', fg='white', font=('helvetica', 14, 'bold'),
                       padx=20, pady=10, borderwidth=5)

logo_image_label.pack(anchor="center", pady=5)

method_label.pack(anchor="center", pady=5)
method_drop_down_menu = OptionMenu(root, used_method, *method_type_list)
method_drop_down_menu.pack(anchor="center", pady=5)
method_drop_down_menu.config(font=('helvetica', 12, 'bold'), bg='green', fg='white',
                             activebackground='green', activeforeground='black', width=13)

select_button.pack(anchor="center", pady=30, padx=5)

root.mainloop()
