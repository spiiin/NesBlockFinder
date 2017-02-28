import re
from operator import itemgetter
#--------------------------------------------------------------------------------
NAME_TABLE_ADDR_1 = 0x2000
NAME_TABLE_SIZE   = 960
NAME_TABLE_ROW    = 32

#ATTR_TABLE_ADDR_1 = 0x23C0
#ATTR_TABLE_SIZE   = 64

BLOCK_SIZE_ENUM_2x2 = 0
BLOCK_SIZE_ENUM_4x4 = 1
BLOCK_SIZE_ENUM_4x2 = 2
BLOCK_SIZE_ENUM_2x4 = 3

start2x2h = (0,1,32,33)
start2x2v = (0,32,1,33)
start4x2h = (0,1,2,3, 32,33,34,35)
start4x2v = (0,32, 1,33, 2,34, 3,35)
start2x4h = (0,1,32,33, 64,65,96,97)
start2x4v = (0,32,64,96, 1,33,65,97)
start4x4h = (0,1,2,3, 32,33,34,35, 64,65,66,67, 96,97,98,99)
start4x4v = (0,32,64,96, 1,33,65,97, 2,34,66,98, 3,35,67,99)
#--------------------------------------------------------------------------------
def getBlocks(startIndexes, tiles, blockSizeType, rowLenInBytes = 64, nameTableSize = NAME_TABLE_SIZE):
    blocks = getAllScreenBlocks(startIndexes, tiles, blockSizeType, rowLenInBytes, nameTableSize)
    blocks = list(set(blocks))
    zeroBlock, ffBlock = ('\x00',) * len(blocks[0]), ('\xFF',)*len(blocks[0])
    if zeroBlock in blocks : blocks.remove(zeroBlock)
    if ffBlock in blocks : blocks.remove(ffBlock)
    return blocks
    
def getAllScreenBlocks(startIndexes, tiles, blockSizeType, rowLenInBytes = 64, nameTableSize = NAME_TABLE_SIZE):
    rowCount = rowLenInBytes/2
    def getNextItem2x2(firstIndex, maxIndex):
        i = firstIndex
        while i < maxIndex:
            for x in xrange(rowCount/2):
                yield i
                i += 2
            i += rowCount
    def getNextItem4x4(firstIndex, maxIndex):
        i = firstIndex
        while i < maxIndex:
            for x in xrange(rowCount/4):
                yield i
                i += 4
            i += rowCount*2
    def getNextItem4x2(firstIndex, maxIndex):
        i = firstIndex
        while i < maxIndex:
            for x in xrange(rowCount/4):
                yield i
                i += 4
            i += rowCount
    def getNextItem2x4(firstIndex, maxIndex):
        i = firstIndex
        while i < maxIndex:
            for x in xrange(rowCount/2):
                yield i
                i += 2
            i += rowCount*2
            
    getNextFromPage2x2 = lambda fi : getNextItem2x2(fi, nameTableSize)
    getNextFromPage4x4 = lambda fi : getNextItem4x4(fi, nameTableSize)
    getNextFromPage4x2 = lambda fi : getNextItem4x2(fi, nameTableSize)
    getNextFromPage2x4 = lambda fi : getNextItem2x4(fi, nameTableSize)
    getNextFromPage = getNextFromPage2x2
    if blockSizeType == BLOCK_SIZE_ENUM_4x4:
        getNextFromPage = getNextFromPage4x4
    elif blockSizeType == BLOCK_SIZE_ENUM_4x2:
        getNextFromPage = getNextFromPage4x2
    elif blockSizeType == BLOCK_SIZE_ENUM_2x4:
        getNextFromPage = getNextFromPage2x4
    
    blockIndexesIters = [getNextFromPage(x) for x in startIndexes]
    blocksIndexes = zip(*blockIndexesIters)
    blocks = [itemgetter(*b)(tiles) for b in blocksIndexes]
    return blocks
    
#--------------------------------------------------------------------------------
def findBlocksInRom(blocks, romData, convertBlockToReFunc, blockBeginStride):
    blockFound = [-1,]*len(romData)

    for blockIndex, block in enumerate(blocks):
        blockStr = convertBlockToReFunc(block)
        #print blockStr
        #print [hex(ord(b)) for b in block]
        try:
            for m in re.finditer(blockStr, romData, re.DOTALL):
                #print hex(m.start())
                blockFound[m.start()] = blockIndex
        except:
            print blockStr

    def calcLongestStrip(blockFound, blockBeginStride):
        longestStrip = []
        blockFoundLen = len(blockFound)
        for x in xrange(blockFoundLen):
            curIndexes = set()
            if blockFound[x] == -1:
                continue
            for lenIndex in xrange(256):
                ind = x + lenIndex * blockBeginStride
                if ind >= blockFoundLen:
                    break
                if blockFound[ind] != -1:
                    curIndexes.add(blockFound[ind])
            if len(curIndexes) > 3:
                longestStrip.append((x, len(curIndexes), curIndexes))
        return sorted(longestStrip, key = lambda v:v[1], reverse = True)
    
    return calcLongestStrip(blockFound, blockBeginStride)
#--------------------------------------------------------------------------------
def escapeRe(blockStr):
    return re.escape(''.join(blockStr))
    
def buildReWithStride(blockStr, stride):
    strideStr = r".{%d}"%stride
    e = re.escape
    return e(blockStr[0]) + strideStr + e(blockStr[1]) + strideStr + e(blockStr[2]) + strideStr + e(blockStr[3])
    
def checkRom(romName, dataName, blockOrder, convertBlockToReFunc = escapeRe, blockBeginStride = 4, blockSizeType = BLOCK_SIZE_ENUM_2x2, rowLen = 32, maxResults = 10):
    with open(dataName, "rb") as f:
        l = f.read()
    tiles = l[NAME_TABLE_ADDR_1 : NAME_TABLE_ADDR_1+NAME_TABLE_SIZE]
    blocks = getBlocks(blockOrder, tiles, blockSizeType, rowLen)
    
    with open(romName, "rb") as f:
        d = f.read()
    found = findBlocksInRom(blocks, d, convertBlockToReFunc, blockBeginStride)
    print romName
    for addr, val, curIndexes in found[:maxResults]:
        print "   ", hex(addr), " ", val, "(", curIndexes, ")"
        
def checkRomGui(romName, dataName, blockOrder, convertBlockToReFunc = escapeRe, blockBeginStride = 4, blockSizeType = BLOCK_SIZE_ENUM_2x2, rowLen = 32, maxResults = 10):
    with open(dataName, "rb") as f:
        l = f.read()
    tiles = l[NAME_TABLE_ADDR_1 : NAME_TABLE_ADDR_1+NAME_TABLE_SIZE]
    blocks = getBlocks(blockOrder, tiles, blockSizeType, rowLen)
    
    with open(romName, "rb") as f:
        d = f.read()
    found = findBlocksInRom(blocks, d, convertBlockToReFunc, blockBeginStride)
    return found[:maxResults]