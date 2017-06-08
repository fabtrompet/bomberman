from Tkinter import *

root = Tk()

def find_in_grid(frame, row, column):
    for children in frame.children.values():
        info = children.grid_info()
        #note that rows and column numbers are stored as string                                                                         
        if info['row'] == str(row) and info['column'] == str(column):
            return children
    return None

#create an array of button                                                                                                              
width = 10
for i in range(width):
    for j in range(width):
        b = Button(root, text=str(i*width+j))
        b.grid(row=i, column=j)

#Create two entries to set row and column to find. Changing entries print the                                                           
#text of the button (and flash it on compatible platforms)                                                                              
def update(var, value, op):
    r = row.get()
    c = col.get()
    b = find_in_grid(root, r, c)
    if b:
        print "button ({0},{1}) : {2}".format(r, c, b["text"])
        b.flash()

Label(root,text="row:").grid(row=width,column=0)
row = StringVar()
row.trace('w',update)
Entry(root,textvar=row, width=3).grid(row=width,column=1)

Label(root,text="col:").grid(row=width,column=2)
col = StringVar()
col.trace('w',update)
Entry(root,textvar=col, width=3).grid(row=width,column=3)

row.set('3')
col.set('2')

mainloop()