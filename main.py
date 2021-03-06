from tkinter import *
from tkinter import font
from PIL import ImageTk, Image
import os
import threading

root = Tk()
root.title("Where's Wally?")
root.configure(background="white")
image_arr = []
myFont = font.Font(family="Helvatica")

for i in range(1, 37):
    image_arr.append(ImageTk.PhotoImage(Image.open("images/{}.jpg".format(i)).resize((1500, 1000), Image.ANTIALIAS)))

my_img1 = image_arr[0]
my_label = Label(image=my_img1)
my_label.grid(row=0, column=0, columnspan=3)

def updateStyle():
    find_wally['font'] = myFont
    find_wally_pretty['font'] = myFont
    button_back['font'] = myFont
    button_exit['font'] = myFont
    button_forward['font'] = myFont
    my_label.grid(row=0, column=0, columnspan=3)
    find_wally.grid(row=1, column=1)
    find_wally_pretty.grid(row=2, column=1)
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2 ,pady="10")
    button_exit.grid(row=3, column=1,pady="10")


def forward(image_number):
    global my_label
    global button_forward
    global button_back
    global find_wally
    global find_wally_pretty
    my_label.grid_forget()
    my_label = Label(image=image_arr[image_number - 1])
    button_forward = Button(root, text=">>",bg="#b2b2ff", command=lambda: forward(image_number + 1))
    button_back = Button(root, text="<<",bg="#b2b2ff", command=lambda: back(image_number - 1))
    find_wally = Button(root, text="Find Wally",bg="#90EE90", command=lambda: find(image_number,"regular"))
    find_wally_pretty = Button(root, text="Find Wally Pretty",bg="#90EE90", command=lambda: find(image_number,"pretty"))
    if image_number == 36:
        button_forward = Button(root, text=">>", state=DISABLED)
    updateStyle()


def back(image_number):
    global my_label
    global button_forward
    global button_back
    global find_wally
    global find_wally_pretty

    my_label.grid_forget()
    my_label = Label(image=image_arr[image_number - 1])
    button_forward = Button(root, text=">>",bg="#b2b2ff", command=lambda: forward(image_number + 1))
    button_back = Button(root, text="<<",bg="#b2b2ff", command=lambda: back(image_number - 1))
    find_wally = Button(root, text="Find Wally", bg="#90EE90" ,command=lambda: find(image_number))
    find_wally_pretty = Button(root, text="Find Wally Pretty", bg="#90EE90" ,command=lambda: find(image_number))

    if image_number == 1:
        button_back = Button(root, text="<<", state=DISABLED)
    updateStyle()


def find(imgName,mode="regular"):
    imgName = str(imgName)
    file = "find_wally_pretty.py" if mode == "pretty" else "find_wally.py"
    cmd = "python "+file+" images/"+imgName+".jpg"
    ThreadA = threading.Thread(target=os.system(cmd))
    ThreadA.start()


find_wally = Button(root, text="Find Wally",bg="#90EE90", command=lambda: find(1,"regular"))
find_wally_pretty = Button(root, text="Find Wally Pretty",bg="#90EE90", command=lambda: find(1,"pretty"))
button_back = Button(root, text="<<", bg="#b2b2ff" , command=back, state=DISABLED)
button_exit = Button(root, bg="#FA8072",text="Exit Program", command=root.quit)
button_forward = Button(root, text=">>",bg="#b2b2ff", command=lambda: forward(2))
updateStyle()


root.mainloop()
