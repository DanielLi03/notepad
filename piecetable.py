from enum import Enum
from dataclasses import dataclass

class Buffer(Enum):
    ORIGINAL = "original"
    ADD = "add"

@dataclass
class Piece:
    buffer: Buffer
    start: int
    length: int

class Piecetable():
    def __init__(self, text=""):
        # initialize original and add strings
        self.original = text
        self.add = ""
        # initialize piece table list
        if len(text) > 0:
            self.pieces = [Piece(Buffer.ORIGINAL, 0, len(self.original))]
        else:
            self.pieces = []
    
    def insert(self, position, text):
        addStart = len(self.add)
        self.add += text
        index, offset = self.findIndex(position)
        # two cases for if there offsetting or not
        if offset == 0:
            self.pieces.insert(index, Piece(Buffer.ADD, addStart, len(text)))
        else:
            split = self.pieces[index]
            split1 = Piece(split.buffer, split.start, offset)
            split2 = Piece(split.buffer, split.start + offset, split.length - offset)
            addPiece = Piece(Buffer.ADD, addStart, len(text))
            self.pieces[index:index+1] = [split1, addPiece, split2]

    def findIndex(self, position):
        # find index and offset position within piece if needed
        current = 0
        index = 0
        for piece in self.pieces:
            current += piece.length
            if current >= position:
                return (index, position - (current - piece.length))
            index += 1
        return (index, 0)
    
    def delete(self, position, length):
        startDelete, startOffset = self.findIndex(position)
        endDelete, endOffset = self.findIndex(position + length)
        startPiece = self.pieces[startDelete]
        endPiece = self.pieces[endDelete]
        # get the appropriate left/right pieces
        leftPiece = Piece(startPiece.buffer, startPiece.start, startOffset)
        rightPiece = Piece(endPiece.buffer, endPiece.start + endOffset, endPiece.length - endOffset)
        new_pieces = []
        # filter out zeros if needed
        if startOffset > 0:
            new_pieces.append(leftPiece)
        if endOffset < endPiece.length:
            new_pieces.append(rightPiece)
        # append to list
        self.pieces[startDelete:endDelete+1] = new_pieces
    
    def getText(self):
        text = []
        for piece in self.pieces:
            if piece.buffer == Buffer.ORIGINAL:
                text.append(self.original[piece.start:(piece.start + piece.length)])
            else:
                text.append(self.add[piece.start:(piece.start + piece.length)])
        return "".join(text)