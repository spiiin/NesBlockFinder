from Tkinter import *
from tkFileDialog import *
import ttk
from find_screens import *

root = Tk()
root.title("NES Screen Finder 1.0")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#-----------------------------------------------------------------------------------------------------------------

def strToInt(s):
    if s[:2].lower() == "0x":
        return int(s[2:], 16)
    else:
        return int(s)
        
def run():
    result1.delete("1.0", END)
    mainframe.update()
    
    blocksAddr = strToInt(blocksAddrVar.get())
    blocksCount = strToInt(blocksCountVar.get())
    niceSearch("Search screens result:", fname.get(), dump.get(), blocksAddr, blocksCount)
    mainframe.update()
    result1.insert(END, "Search complete!" + "\n", "method")
    
def niceSearch(text, *args, **kwargs):
    def niceHex(addr):
        return hex(addr)[2:].upper()
    found = findScreens(*args, **kwargs)
    result1.insert(END, text + "\n", "method")
    if len(found) == 0:
         result1.insert(END, "Nothing found\n", "addr")
    for addr, val, curIndexes in found:
        result1.insert(END, niceHex(addr)+" ("+str(val)+" blocks around)\n", "addr")
        #result1.insert(END, str(sorted(list(curIndexes))) +"\n", "color")
    result1.focus_set()
#-----------------------------------------------------------------------------------------------------------------
def fnameClick(event):
    fname = askopenfilename(filetypes=(("All files", "*.*"),))
    event.widget.delete(0,END)
    event.widget.insert(0,fname)
    
def rangeValidate(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if text in '0123456789':
        try:
            i = int(value_if_allowed)
            if i > 0 and i < 255:
                return True
            else:
                return False
        except ValueError:
            return False
    else:
        return False
    

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(1, weight=1)
mainframe.rowconfigure(13, weight=1)

fname = StringVar()
dump  = StringVar()

filenameEntry = ttk.Entry(mainframe, width=64, textvariable=fname)
filenameEntry.grid(column=1, row=1, sticky=(W, E))
filenameEntry.bind("<Button-1>", fnameClick)

dumpEntry = ttk.Entry(mainframe, width=64, textvariable=dump)
dumpEntry.grid(column=1, row=2, sticky=(W, E), pady = 5)
dumpEntry.bind("<Button-1>", fnameClick)

ttk.Label(mainframe, text="ROM file:").grid(column=0, row=1, sticky=W)
ttk.Label(mainframe, text="PPU dump:").grid(column=0, row=2, sticky=W, pady = 5)

#--------------------------------------------------------------------------------------------------
vcmd = (mainframe.register(rangeValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

blocksAddrVar  = StringVar()
ttk.Label(mainframe, text="Blocks address:").grid(column=0, row=3, sticky=W)
blocksAddrEntry = ttk.Entry(mainframe, width=12, textvariable=blocksAddrVar, validate = 'key')
blocksAddrEntry.grid(column=1, row=3, sticky=(W,))
blocksAddrVar.set("0x10")

blocksCountVar = StringVar()
ttk.Label(mainframe, text="Blocks count:").grid(column=0, row=4, sticky=W)
blocksCountEntry = ttk.Entry(mainframe, width=12, textvariable=blocksCountVar, validate = 'key', validatecommand = vcmd)
blocksCountEntry.grid(column=1, row=4, sticky=(W,))
blocksCountVar.set("255")

#--------------------------------------------------------------------------------------------------
ttk.Button(mainframe, text="Run", command=run).grid(column=0, row=5, sticky=(W,E), columnspan=2)
#--------------------------------------------------------------------------------------------------
result1 = Text(mainframe, width=32, height=12)
result1.grid(column=0, row=6, sticky=(W,E,S,N), columnspan=2)
result1.tag_configure('method', font=('Verdana', 12, 'bold'))
result1.tag_configure('method_error', font=('Verdana', 12, 'bold'), foreground='#FF0000')
result1.tag_configure('addr', font=('Courier New', 10, 'bold'))
result1.tag_configure('color', foreground='#476042', font=('Courier New', 10))
s = ttk.Scrollbar(mainframe, orient=VERTICAL, command=result1.yview)
s.grid(column=2, row=6, sticky=(N,S))
result1['yscrollcommand'] = s.set
#--------------------------------------------------------------------------------------------------
root.mainloop()
