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
        self.history = [self.pieces]
        self.redoHistory = []
    
    def insert(self, position, text):
        self.redoHistory = []
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
        self.history.append(self.pieces.copy())


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
        if position == 0:
            return
        self.redoHistory = []
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
        self.history.append(self.pieces.copy())

    def getText(self):
        text = []
        for piece in self.pieces:
            if piece.buffer == Buffer.ORIGINAL:
                text.append(self.original[piece.start:(piece.start + piece.length)])
            else:
                text.append(self.add[piece.start:(piece.start + piece.length)])
        return "".join(text)
    
    def undo(self):
        if self.history:
            self.redoHistory.append(self.history.pop())
            self.pieces = self.history[-1] if self.history else []
    
    def redo(self):
        if self.redoHistory:
            self.history.append(self.redoHistory.pop())
            self.pieces = self.history[-1]

    
if __name__ == "__main__":
    pt = Piecetable("Hello World")
    assert pt.getText() == "Hello World"
    pt.insert(6, "Daniel's ")
    assert pt.getText() == "Hello Daniel's World"
    pt.delete(6, 9)
    assert pt.getText() == "Hello World"
    pt.undo()
    assert pt.getText() == "Hello Daniel's World"
    pt.redo()
    assert pt.getText() == "Hello World"
    print("Test 1 passed")