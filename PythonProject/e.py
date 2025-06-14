import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from playsound import playsound
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
df = pd.read_csv("ufo_sightings_scrubbed.csv", dtype={0: str}, low_memory=False)

if "comments" in df.columns:
    df = df.drop('duration (hours/min)', axis=1)
    df = df.drop('comments', axis=1)
    df = df.drop('date posted', axis=1)
    df = df.drop('latitude', axis=1)
    df = df.drop('longitude ', axis=1)


def add():
    global df
    datetime_val = input('input date time in this format YYYY-MM-DD HOUR:MINUTE:SECOND : ')
    city = input('give city of sighting: ')
    state = input('give state of sighting: ')
    country = input('give country of sighting: ')
    shape = input('give shape of sighting: ')
    duratz = float(input('give duration in seconds of sighting: '))

    df.loc[len(df)] = {
        'datetime': datetime_val,
        'city': city,
        'state': state,
        'country': country,
        'shape': shape,
        'duration (seconds)': duratz
    }

    print(df)

    df.to_csv('ufos.csv', index=False)
def delete():
    global df
    datetime_val = input('input date time in this format YYYY-MM-DD HOUR:MINUTE:SECOND : ')
    city = input('give city of sighting: ')
    row_ = df[(df['datetime'] == datetime_val) & (df['city'] == city)]
    if not row_.empty:
        df.drop(row_.index[0], inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_csv('ufo_sightings_scrubbed.csv', index=False)
        print("deleted.")
    else:
        print("No matching row.")

while True:
    inputs = input('add or delete or save? ')
    if inputs == 'add':
        add()
    elif inputs == 'delete':
        delete()
    elif inputs == 'save':
        df.to_csv('ufos.csv', index=False)
        break



df = pd.read_csv("ufos.csv", dtype={0: str}, low_memory=False)
df = df.loc[df['state'] == "ny"]

yeardf = df['datetime'].astype(str).str[:4]
month = df['datetime'].astype(str).str[5:7]
day = df['datetime'].astype(str).str[8:10]
timehour = df['datetime'].astype(str).str[11:13]
timehour = timehour.astype(int)
timemin = df['datetime'].astype(str).str[14:16]
timemin = timehour.astype(int)
timeseconds = df['duration (seconds)'].astype(str)
timeseconds = df['duration (seconds)'].astype(float)
df["year"] = yeardf
df["month"] = month
df["day"] = day
df["hour"] = timehour
df["min"] = timemin
df["sec"] = timeseconds

df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

df = df[(df['datetime'].dt.year >= 2010)]

df = df.sort_values(by='datetime')

df.to_csv("ufos.csv", index=False)

df.to_csv('ufo_sightings_scrubbed.csv', index=False)

listofdurationx = df["duration (seconds)"].tolist()
listofduration = [float(x) for x in listofdurationx]
for i in range(len(listofduration)):
    min = i
    for j in range(i + 1, len(listofduration)):
        if listofduration[j] < listofduration[min]:
            min = j
    listofduration[i], listofduration[min] = listofduration[min], listofduration[i]
print(listofduration[:-1])

def bargraphoftheyearandtimeview():
    for widget in window.winfo_children():
        widget.destroy()
    show_menu()
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    years = df['year'].unique()
    sightings = []
    for year in years:
        avgduration = df['year'].value_counts().get(year, 0)
        sightings.append(avgduration)
    ax.bar(years, sightings)
    ax.set_title('UFO Sightings by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Sightings')
    canvas.draw()


def bargraphoftheyearandaveragesightingstimes():
    for widget in window.winfo_children():
        widget.destroy()
    show_menu()
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    years = df['year'].unique()
    duration = []
    for year in years:
        durations = df[df["year"] == str(year)]["duration (seconds)"].astype(float)
        avgduration = durations.mean()
        duration.append(avgduration)
    ax.bar(years, duration)
    ax.set_title('average duration of UFO sightings and years')
    ax.set_xlabel('years')
    ax.set_ylabel('average duration of UFO sightings(seconds)')
    canvas.draw()



def launch_data_viewer():
    viewer = Toplevel()
    viewer.title("UFO Sightings Viewer")

    def update_display(val):
        try:
            index = int(val)
            if 0 <= index < len(df):
                row = df.iloc[index]
                display_text = (
                    f"Date: {row.get('datetime', 'N/A')}\n"
                    f"City: {row.get('city', 'N/A')}\n"
                    f"State: {row.get('state', 'N/A')}\n"
                    f"Country: {row.get('country', 'N/A')}\n"
                    f"Shape: {row.get('shape', 'N/A')}\n"
                    f"Duration: {row.get('duration (seconds)', 'N/A')} seconds"
                )
                data_label.config(text=display_text)
        except Exception as e:
            data_label.config(text=f"Error: {e}")

    slider = Scale(viewer, from_=0, to=len(df) - 1, orient='horizontal', command=update_display)
    slider.pack(fill='x', padx=20, pady=10)

    data_label = Label(viewer, text="", font=("Arial", 14), justify='left')
    data_label.pack(padx=20, pady=20)
    update_display(0)

    search_frame = Frame(viewer)
    search_frame.pack(pady=10)
    Label(search_frame, text="Enter date (YYYY-MM-DD):").pack(side='left')
    date_entry = Entry(search_frame)
    date_entry.pack(side='left', padx=5)

    def search_date():
        try:
            input_date = pd.to_datetime(date_entry.get(), errors='coerce').date()
            match = df[df['datetime'].dt.date == input_date]
            if not match.empty:
                slider.set(match.index[0])
            else:
                data_label.config(text=f"No sightings found on {input_date}")
        except Exception:
            data_label.config(text="Invalid date. Use YYYY-MM-DD.")

    Button(search_frame, text="Search", command=search_date).pack(side='left', padx=5)



import pygame

def goofy():
    for widget in window.winfo_children():
        widget.destroy()
    window.photos = PhotoImage(file="pp.png")
    photozz = Label(window, image=window.photos)
    photozz.pack()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    sound_path = os.path.join(script_dir, "tuah.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

def show_menu():
    for widget in window.winfo_children():
        widget.destroy()
    btn1 = Button(window, text="Bar Graph of Sightings", font=("Arial", 14), command=bargraphoftheyearandtimeview)
    btn2 = Button(window, text="Avg Duration Bar Graph", font=("Arial", 14),
                  command=bargraphoftheyearandaveragesightingstimes)
    btn3 = Button(window, text="View Data", font=("Arial", 14), command=launch_data_viewer)
    btn4 = Button(window, text="goofy button", font=("Arial", 14), command=goofy)
    btn5 = Button(window, text="Exit", font=("Arial", 14), command=exit)

    btn1.pack(pady=30)
    btn2.pack(pady=30)
    btn3.pack(pady=30)
    btn4.pack(pady=30)
    btn5.pack(pady=30)


window = Tk()
window.geometry("1920x1080")
window.title("UFO sightings")
img = PhotoImage(file="photo.png")
photo = Label(window, image=img)
photo.place(relx=0.5, rely=0.6, anchor='center')


label = Label(window, text="UFO sightings", font=("arial", 24))

start_button = Button(window, text="Start", font=("Arial", 16), command=show_menu)
start_button.place(relx=0.5, rely=0.4, anchor='center')
label.place(relx=0.5, rely=0.2, anchor='center')
window.mainloop()

def binarysearch(target, listofduration):
    low = 0
    high = len(listofduration)-1
    while low <= high:
        mid = (high+low)//2
        if listofduration[mid] == target:
            return mid
        elif listofduration[mid] > target:
            high = mid -1
        elif listofduration[mid] < target:
            low = mid + 1
        if low == high:
            print(-1)
    if low == high:
        print(-1)
target = int(input("What number do you want? "))
print(binarysearch(target, listofduration))

