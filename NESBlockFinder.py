from Tkinter import *
from tkFileDialog import *
import ttk
from find_blocks import *

root = Tk()
root.title("NES Block Finder 1.1")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#-----------------------------------------------------------------------------------------------------------------
def run():
    result1.delete("1.0", END)
    advancedSearcihDisabled = blockStride.get() == False and blockStride255.get() == False and attrSearch.get() == False
    if blockLeftRight.get() == False and blockUpDown.get() == False and advancedSearcihDisabled:
        result1.insert(END, "Select at least one of 'Left-right block search' or 'Top-down block search' or select one of advance search methods" + "\n", "method_error")
    if block2x2.get()==False and block4x4.get()==False and block2x4.get()==False and advancedSearcihDisabled:
        result1.insert(END, "Select at least one of 'Search 2x2 blocks' or 'Search 4x4 blocks' or 'Search 4x2 blocks' or select one of advance search methods" + "\n", "method_error")
    mainframe.update()
    if blockLeftRight.get() == True and block2x2.get() == True:
        niceSearch("Search 2x2 blocks, left-right", fname.get(), dump.get(), start2x2h)
        mainframe.update()
    if blockUpDown.get() == True and block2x2.get() == True:
        niceSearch("Search 2x2 blocks, top-down"  , fname.get(), dump.get(), start2x2v)
        mainframe.update()
    if blockLeftRight.get() == True and block4x4.get() == True:
        niceSearch("Search 4x4 blocks, left-right", fname.get(), dump.get(), start4x4h, blockSizeType = BLOCK_SIZE_ENUM_4x4)
        mainframe.update()
    if blockUpDown.get() == True and block4x4.get() == True:
        niceSearch("Search 4x4 blocks, top-down"  , fname.get(), dump.get(), start4x4v, blockSizeType = BLOCK_SIZE_ENUM_4x4)
        mainframe.update()
    if blockLeftRight.get() == True and block2x4.get() == True:
        niceSearch("Search 4x2 blocks, left-right", fname.get(), dump.get(), start4x2h, blockSizeType = BLOCK_SIZE_ENUM_4x2)
        mainframe.update()
    if blockUpDown.get() == True and block2x4.get() == True:
        niceSearch("Search 2x4 blocks, top-down"  , fname.get(), dump.get(), start2x4v, blockSizeType = BLOCK_SIZE_ENUM_2x4)
        mainframe.update()
    if blockLeftRight.get() == True and block4x1.get() == True:
        niceSearch("Search 4x1 blocks, left-right", fname.get(), dump.get(), start4x1h, blockSizeType = BLOCK_SIZE_ENUM_4x1)
        mainframe.update()
    if block1x1.get() == True:
        niceSearch("Search 1x1 blocks (tiles indexes)"  , fname.get(), dump.get(), start1x1, blockBeginStride = 1, blockSizeType = BLOCK_SIZE_ENUM_1x1)
        mainframe.update()
    if attrSearch.get() == True:
        niceSearch("Attributes bytes search", fname.get(), dump.get(), start1x1, blockBeginStride = 1, blockSizeType = BLOCK_SIZE_ENUM_1x1, maxDistance = 64, findInAttr = True)
        mainframe.update()
    if blockStride255.get() == True:
        niceSearch("Search with stride 255, block 2x2, left-right", fname.get(), dump.get(), start2x2h, lambda(block) : buildReWithStride (block, 255), 1)
        mainframe.update()
        niceSearch("Search with stride 255, block 2x2, top-down"  , fname.get(), dump.get(), start2x2v, lambda(block) : buildReWithStride (block, 255), 1)
        mainframe.update()
    if blockStride.get() == True:
        minStride, maxStride = int(minRange.get()), int(maxRange.get())
        for curStride in xrange(minStride, maxStride+1):
            niceSearch("Search with stride %d, block 2x2, left-right"%curStride, fname.get(), dump.get(), start2x2h, lambda(block) : buildReWithStride (block, curStride), 1)
            mainframe.update()
            niceSearch("Search with stride %d, block 2x2, top-down"%curStride , fname.get(), dump.get(), start2x2v, lambda(block) : buildReWithStride (block, curStride), 1)
            mainframe.update()
    result1.insert(END, "Search complete!" + "\n", "method")
    
def niceSearch(text, *args, **kwargs):
    def niceHex(addr):
        return hex(addr)[2:].upper()
    found = checkRomGui(*args, **kwargs)
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
#mainframe.columnconfigure(2, weight=1)
mainframe.rowconfigure(14, weight=1)

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
ttk.Label(mainframe, text="Simple search methods (linear):").grid(column=0, row=3, sticky=W, pady = 5)

blockLeftRight = BooleanVar()
cbLeftRight = ttk.Checkbutton(mainframe, text='Left-right block search', variable = blockLeftRight)
cbLeftRight.grid(column=1, row=4, sticky=(W, E))
blockLeftRight.set(True)

blockUpDown = BooleanVar()
cbUpDown = ttk.Checkbutton(mainframe, text='Top-down block search', variable = blockUpDown)
cbUpDown.grid(column=1, row=5, sticky=(W, E))
blockUpDown.set(True)

block2x2 = BooleanVar()
cb2x2 = ttk.Checkbutton(mainframe, text='Search 2x2 blocks', variable = block2x2)
cb2x2.grid(column=0, row=4, sticky=(W, E))
block2x2.set(True)

block4x4 = BooleanVar()
cb4x4 = ttk.Checkbutton(mainframe, text='Search 4x4 blocks', variable = block4x4)
cb4x4.grid(column=0, row=5, sticky=(W, E))
block4x4.set(True)

block2x4 = BooleanVar()
cb2x4 = ttk.Checkbutton(mainframe, text='Search 2x4/4x2 blocks', variable = block2x4)
cb2x4.grid(column=0, row=6, sticky=(W, E))
block2x4.set(False)

block4x1 = BooleanVar()
cb4x1 = ttk.Checkbutton(mainframe, text='Search 4x1 blocks', variable = block4x1)
cb4x1.grid(column=0, row=7, sticky=(W, E))
block4x1.set(False)

block1x1 = BooleanVar()
cb1x1 = ttk.Checkbutton(mainframe, text='Search 1x1 blocks (use with cut-scenes)', variable = block1x1)
cb1x1.grid(column=0, row=8, sticky=(W, E))
block1x1.set(False)
#--------------------------------------------------------------------------------------------------
ttk.Label(mainframe, text="Advance search:").grid(column=0, row=9, sticky=W, pady = 5)

attrSearch = BooleanVar()
cbAttrSearch = ttk.Checkbutton(mainframe, text='Attributes search (use with 4x4 standart blocks)', variable = attrSearch)
cbAttrSearch.grid(column=0, row=10, sticky=(W, E))
attrSearch.set(True)

blockStride255 = BooleanVar()
cbStride255 = ttk.Checkbutton(mainframe, text='Search block parts with stride 255', variable = blockStride255)
cbStride255.grid(column=0, row=11, sticky=(W, E))
blockStride255.set(True)

blockStride = BooleanVar()
cbStride = ttk.Checkbutton(mainframe, text='Search block parts with stride range:', variable = blockStride)
cbStride.grid(column=0, row=12, sticky=(W, E))
blockStride.set(False)

minRange  = StringVar()
maxRange  = StringVar()

vcmd = (mainframe.register(rangeValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

ttk.Label(mainframe, text="Min range:").grid(column=0, row=12, sticky=W)
minEntry = ttk.Entry(mainframe, width=4, textvariable=minRange, validate = 'key', validatecommand = vcmd)
minEntry.grid(column=1, row=13, sticky=(W,))
minRange.set("64")

ttk.Label(mainframe, text="Max range:").grid(column=0, row=13, sticky=W)
maxEntry = ttk.Entry(mainframe, width=4, textvariable=maxRange, validate = 'key', validatecommand = vcmd)
maxEntry.grid(column=1, row=14, sticky=(W,))
maxRange.set("255")
#--------------------------------------------------------------------------------------------------
ttk.Button(mainframe, text="Run", command=run).grid(column=0, row=15, sticky=(W,E), columnspan=2)
#--------------------------------------------------------------------------------------------------
result1 = Text(mainframe, width=32, height=12)
result1.grid(column=0, row=16, sticky=(W,E,S,N), columnspan=2)
result1.tag_configure('method', font=('Verdana', 12, 'bold'))
result1.tag_configure('method_error', font=('Verdana', 12, 'bold'), foreground='#FF0000')
result1.tag_configure('addr', font=('Courier New', 10, 'bold'))
result1.tag_configure('color', foreground='#476042', font=('Courier New', 10))
s = ttk.Scrollbar(mainframe, orient=VERTICAL, command=result1.yview)
s.grid(column=2, row=16, sticky=(N,S))
result1['yscrollcommand'] = s.set
#--------------------------------------------------------------------------------------------------
root.mainloop()
