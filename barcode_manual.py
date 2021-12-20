import tkinter as tk
import tkinter.messagebox as tkmsg
from tkinter import *
import turtle


class barcode_window(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.structure_ean = [
            "LLLLLL",
            "LLGLGG",
            "LLGGLG",
            "LLGGGL",
            "LGLLGG",
            "LGGLLG",
            "LGGGLL",
            "LGLGLG",
            "LGLGGL",
            "LGGLGL"
        ]
        self.L_Code = ["0001101", "0011001", "0010011", "0111101",
                       "0100011", "0110001", "0101111", "0111011", "0110111", "0001011"]
        self.G_Code = ["0100111", "0110011", "0011011", "0100001",
                       "0011101", "0111001", "0000101", "0010001", "0001001", "0010111"]
        self.R_Code = ["1110010", "1100110", "1101100", "1000010",
                       "1011100", "1001110", "1010000", "1000100", "1001000", "1110100"]
        self.pack()
        self.createWidget()

    def createWidget(self):
        self.ps_file = tk.StringVar()
        self.inputCode = tk.StringVar()

        tk.Label(self, text='Save Barcode to PS file [eg: EAN13.eps]:', font=(
            'Arial', 15)).grid(row=0, column=0, columnspan=2)
        tk.Entry(self, width=30, textvariable=self.ps_file).grid(
            row=1, column=0, columnspan=2)
        tk.Label(self, text='Enter Code (first 12 decimal digits):',
                 font=('Arial', 15)).grid(row=2, column=0, columnspan=2)
        code_entry = tk.Entry(self, width=30, textvariable=self.inputCode)
        code_entry.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        code_entry.bind('<Return>',self.validate)
        # tk.Button(self, text="Generate!", background="light green",
        #           command=self.validate).grid(row=4, column=0, columnspan=2, pady=(0, 10))

        self.canvas = Canvas(self, width=300, height=280, bg="white")
        self.canvas.grid(row=5, column=0, rowspan=2, columnspan=3)

    def validateCode(self):
        self.listCode = list(self.inputCode.get())

        check = False
        if len(self.listCode) != 12:
            check = True
        else:
            for i in self.listCode:
                if i.isdigit() == False:
                    check = True
                    break

        if check:
            tkmsg.showwarning("error", "please enter correct input code")
        else:
            return True

    def validateName(self):
        if self.ps_file.get().endswith(".eps"):
            return True
        else:
            tkmsg.showwarning("error", "please enter correct name file")

    def validate(self,tes):
        self.validasi_code = self.validateCode()
        self.validasi_nama = self.validateName()

        if self.validasi_nama and self.validasi_code:
            self.calculateDigits()

    def calculateDigits(self):
        self.code = list(self.inputCode.get())
        self.code = [int(i) for i in self.code]
        even_pos, odd_pos = 0, 0
        for i in range(len(self.code)):
            if i % 2 == 0:
                even_pos += self.code[i]
            else:
                odd_pos += self.code[i]

        checksum = (odd_pos*3)+even_pos
        x = checksum % 10

        if x != 0:
            self.code.append(10-x)
        else:
            self.code.append(x)

        encoding_start = self.structure_ean[self.code[0]]
        self.binary_encoding_start = []
        for code, encoding in zip(self.code[1:7], encoding_start):
            if encoding == "L":
                self.binary_encoding_start.append(self.L_Code[code])
            else:
                self.binary_encoding_start.append(self.G_Code[code])

        self.binary_encoding_end = []
        for code in self.code[7:len(self.code)]:
            self.binary_encoding_end.append(self.R_Code[code])

        self.draw_Barcode()

    def draw_Barcode(self):
        self.canvas.delete("all")
        t = turtle.RawTurtle(self.canvas)
        t.speed(speed=0)
        x, y = -140, 100
        t.penup()
        t.goto(x, y)
        t.pendown()
        t.right(90)
        t.width(3)

        temp = x
        t.pencolor("blue")
        for i in range(2):
            t.pendown()
            t.forward(170)
            t.penup()
            if i-1 != 0:
                temp += 5
            t.setpos(temp, y)

        t.pencolor("green")
        for digit in self.binary_encoding_start:
            for i in digit:
                if i == "1":
                    temp += 3
                    t.setpos(temp, y)
                    t.pendown()
                    t.forward(150)
                    t.penup()
                else:
                    temp += 3

        t.pencolor("blue")
        for i in range(2):
            temp += 5
            t.setpos(temp, y)
            t.pendown()
            t.forward(170)
            t.penup()

        temp += 3
        t.pencolor("green")
        for digit in self.binary_encoding_end:
            for i in digit:
                if i == "1":
                    temp += 3
                    t.setpos(temp, y)
                    t.pendown()
                    t.forward(150)
                    t.penup()
                else:
                    temp += 3

        t.pencolor("blue")
        for i in range(2):
            t.setpos(temp, y)
            t.pendown()
            t.forward(170)
            t.penup()
            temp += 5

        t.pencolor("blue")
        t.setpos(-100, -100)
        code = ''.join([str(i) for i in self.code])
        t.write(f"Digits: {code}", font=("Verdana", 10, "normal"))
        t.setpos(-100, -115)
        t.pencolor("red")
        t.write(f"Check Digit: {self.code[-1]}",
                font=("Verdana", 10, "normal"))
        t.setpos(-1000, -1000)

        ts = t.getscreen()
        canvas = ts.getcanvas()
        canvas.postscript(file=self.ps_file.get())


if __name__ == "__main__":
    m = barcode_window()
    m.master.title("EAN-13")
    m.master.geometry("400x450")
    m.master.mainloop()
