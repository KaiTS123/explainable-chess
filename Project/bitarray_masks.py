from bitarray import bitarray

def posToIndex(position: str) -> int:
    if len(position) != 2:
        return -1
    fileTranslation = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    return 8*(int(position[1])-1)+fileTranslation[position[0]]

def indexToPos(index: int) -> str:
    if index < 0 or index >= 64:
        return "-"
    fileTranslation = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    return fileTranslation[index % 8] + str(1 + index // 8 )

def northMask(position: int):
    result = bitarray('0000000010000000100000001000000010000000100000001000000010000000') >> position
    return result

def southMask(position: int):
    result = result = bitarray('0000000100000001000000010000000100000001000000010000000100000000') << (63-position)
    return result

def fileMask(position: int):
    result = bitarray('1000000010000000100000001000000010000000100000001000000010000000') >> (position&7)
    result[position] = 0
    return result

def rankMask(position: int):
    result = bitarray('1111111100000000000000000000000000000000000000000000000000000000') >> (position&56)
    result[position] = 0
    return result

def antiDiagonalMask(position: int):
    result = bitarray('0000000100000010000001000000100000010000001000000100000010000000')
    diag = 56-8*(position&7) - (position & 56)
    nort = -diag & ( diag >> 31)
    sout =  diag & (-diag >> 31)
    result = (result << sout) >> nort
    result[position] = 0
    return result

def diagonalMask(position: int):
    result = bitarray('1000000001000000001000000001000000001000000001000000001000000001')
    diag = 8*(position&7) - (position & 56)
    nort = -diag & ( diag >> 31)
    sout =  diag & (-diag >> 31)
    result = (result << sout) >> nort
    result[position] = 0
    return result

def rankMask(position: int):
    result = bitarray('1111111100000000000000000000000000000000000000000000000000000000') >> (position&56)
    result[position] = 0
    return result

def queenAttackMask(position: int):
    return rankMask(position) | fileMask(position) | diagonalMask(position) | antiDiagonalMask(position)

def rookAttackMask(position: int):
    return rankMask(position) | fileMask(position)

def bishopAttackMask(position: int):
    return diagonalMask(position) | antiDiagonalMask(position)

def bitMaskString(bits):
    result = ''
    for i in range(7,-1,-1):
        for j in range(8):
            if bits[i*8+j]:
                result += 'x'
            else:
                result += '.'
        result += '\n'
    return result

