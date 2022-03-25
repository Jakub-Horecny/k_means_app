import sys
from tkinter import *
from tkinter import filedialog, messagebox

from Clustering import Clustering

root = Tk()
root.title("K-Means App")
root.geometry("500x450")

print_geometry = "400x500"

csv_file_path: StringVar = StringVar()
centroids: StringVar = StringVar()

csv_file_label: Label = Label(root, text='.csv súbor (variables x points) \n vzor v test.csv', font=('helvetica', 14, 'bold'))
centroids_label: Label = Label(root, text='Zadaj body na inicializáciu centroidov \n napr: 0,1,2 (bez medzier)',
                               font=('helvetica', 14, 'bold'))

centroids_entry: Entry = Entry(root, borderwidth=5, font=('helvetica', 14, 'bold'),
                               textvariable=centroids)


def start_clustering() -> None:
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
        messagebox.showinfo('Error', 'Zadaj súradnice stredov alebo Súbor nie je v spravnom formáte - pozri test.csv \n' + str(err))
    except FileNotFoundError as err:
        messagebox.showinfo('Error', 'Súbor sa nenašiel \n' + str(err))
    except IndexError as err:
        messagebox.showinfo('Error', 'Stredov je viac ako bodov alebo index bodu > počet bodov \n' + str(err))
    except Exception as err:
        messagebox.showinfo('Error', ' -\(o,o)/-  \n' + str(err))


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


csv_file_button = Button(root, text=".csv súbor", command=get_csv_file,
                      bg='green', fg='white', font=('helvetica', 14, 'bold'),
                      padx=20, pady=10, borderwidth=5)

start_button = Button(root, text="Start", command=start_clustering,
                      bg='green', fg='white', font=('helvetica', 14, 'bold'),
                      padx=20, pady=10, borderwidth=5)

csv_file_label.pack(anchor="center", pady=5)
csv_file_button.pack(anchor="center", pady=5)
centroids_label.pack(anchor="center", pady=5)
centroids_entry.pack(anchor="center", pady=5)
start_button.pack(anchor="center", pady=5)

root.mainloop()
