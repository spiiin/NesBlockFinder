from itertools import izip_longest
from find_blocks import *

def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return list(izip_longest(*[iter(iterable)]*n, fillvalue=padvalue))
    
def readLinear(romdata, addr, blockCount, blockSize):
    return grouper(blockSize, romdata[addr:addr+blockCount*blockSize])
    
def readFromAlignedArrays(romdata, addrs, blocksCount):
    return grouper(4, [romdata[addr+x] for x in xrange(blocksCount) for addr in addrs])
    
def remap(screenBlocks, blocks):
    ans = []
    for sb in screenBlocks:
        try:    
            ans.append(chr(blocks.index(sb)))
        except:
            ans.append(chr(255))
    return ans
   
def checkInOut(screenBlocks, blocks):
    inCount, outCount = 0,0
    for sb in screenBlocks:
        if sb in blocks:
            inCount +=1
            #print [hex(ord(b)) for b in sb], "In"
        else:
            outCount +=1
            #print [hex(ord(b)) for b in sb], "Out"
    print "In", inCount
    print "Out", outCount
    return inCount, outCount

#---------------------------------------------------------------------------------
def readBlocks16x1(d, addr, blocksCount):
    return readLinear(d, addr, blocksCount, 16)
    
def readScreenBlocks16x1(l, offset):
    tiles = l[NAME_TABLE_ADDR_1 + offset : NAME_TABLE_ADDR_1+NAME_TABLE_SIZE]
    return getAllScreenBlocks(start4x4h, tiles, BLOCK_SIZE_ENUM_4x4, 64)
    
#----------------------------------------------------------------------------
def findScreens(romName, dataName, blocksAddr, blocksCount):
    with open(romName, "rb") as f:
        d = f.read()
    with open(dataName, "rb") as f:
        l = f.read()
    blocks = readBlocks16x1(d, blocksAddr, blocksCount)
    #check if blocks start from not first line!
    maxInBlocks = 0
    for offset in [0,32,64,96]:
        possibleScreenBlocks = readScreenBlocks16x1(l, offset)
        inCount, _ = checkInOut(possibleScreenBlocks, blocks)
        if inCount > maxInBlocks:
            screenBlocks = possibleScreenBlocks
    
    macroTiles = remap(screenBlocks, blocks)
    #print [hex(ord(mt)) for mt in macroTiles]
    found = findBlocksInRom(grouper(4, macroTiles), d, escapeRe, blockBeginStride = 4, maxDistance = 32)
    return found[:10]
#-----------------------------------------------------------------------------------
#findScreens("Teenage Mutant Ninja Turtles III - The Manhattan Project (U) [!].nes", "Teenage Mutant Ninja Turtles III - The Manhattan Project (U) [!]_ppu1.bin", 0x30471, 220)