

class GirdGui:
    
    def __init__(self,width_=20,height_=10,wid=5,hei=2,title="GirdGui"):
        import tkinter
        self.width_ = width_
        self.height_ = height_
        self.wid = wid
        self.hei = hei
        self.excl = {}
        self.tk = tkinter.Tk()
        self.tk.title(title)
        for w in range(self.width_):
            for h in range(self.height_):
                self.excl[f"ch{w}_{h}"] = tkinter.Label(self.tk,width=wid,height=hei,relief="raised",bg="white")
                self.excl[f"ch{w}_{h}"].grid(column=w,row=h)
    def delAll(self):
        for w in range(self.width_):
            for h in range(self.height_):
                self.excl[f"ch{w}_{h}"].config(background='white')
                self.excl[f"ch{w}_{h}"].grid(column=w,row=h)
    def light(self,x,y,color="blue"):
        if x > self.height_ or x < 0:
            raise ValueError("空间不足，请确保您X坐标未超出范围！")
        elif y > self.width_ or y < 0:
            raise ValueError("空间不足，请确保您Y坐标未超出范围！")
        else:
            self.excl[f"ch{x}_{y}"].config(bg=color)
    def drawNumber(self,pos=(0,0),word="2"):
        j = int(word[0])
        x = pos[0]
        y = pos[1]
        if j == 1:
            lists = [(x+1,y),(x+1,y+1),(x+1,y+2),(x+1,y+3),(x+1,y+4)]
        elif j == 2:
            lists = [(x,y),(x+1,y),(x+2,y),(x+2,y+1),
                (x+2,y+2),(x+1,y+2),(x,y+2),(x,y+3),(x,y+4),(x+1,y+4),(x+2,y+4)]
        elif j == 3:
            lists = [(x,y),(x+1,y),(x+2,y),(x+2,y+1),(x+2,y+2),(x+1,y+2),(x,y+2),
                (x+2,y+3),(x+2,y+4),(x+1,y+4),(x,y+4)]
        elif j == 4:
            lists = [(x,y),(x+2,y),(x,y+1),(x+2,y+1),(x,y+2),(x+1,y+2),(x+2,y+2),
                (x+2,y+3),(x+2,y+4)]
        elif j == 5:
            lists = [(x,y),(x+1,y),(x+2,y),(x,y+1),
                (x+2,y+2),(x+1,y+2),(x,y+2),(x+2,y+3),(x,y+4),(x+1,y+4),(x+2,y+4)]
        elif j == 6:
            lists = [(x,y),(x+1,y),(x+2,y),(x,y+1),
                (x+2,y+2),(x+1,y+2),(x,y+2),(x+2,y+3),(x,y+4),(x+1,y+4),(x+2,y+4),(x,y+3)]
        elif j == 7:
            lists = [(x,y),(x+1,y),(x+2,y),(x+2,y+1),(x+2,y+2),(x+2,y+3),(x+2,y+4)]
        elif j == 8:
            lists = [(x,y),(x+1,y),(x+2,y),(x,y+1),
                (x+2,y+2),(x+1,y+2),(x,y+2),(x+2,y+3),
                (x,y+4),(x+1,y+4),(x+2,y+4),(x,y+3),(x+2,y+1)]
        elif j == 9:
            lists = [(x,y),(x+1,y),(x+2,y),(x,y+1),
                (x+2,y+2),(x+1,y+2),(x,y+2),(x+2,y+3),
                (x,y+4),(x+1,y+4),(x+2,y+4),(x+2,y+1)]
        elif j == 0:
            lists = [(x,y),(x+1,y),(x+2,y),(x,y+1),
                (x+2,y+2),(x,y+2),(x+2,y+3),
                (x,y+4),(x+1,y+4),(x+2,y+4),(x,y+3),(x+2,y+1)]
        for spx,spy in lists:
            self.light(spx,spy)
    def display(self):
        self.tk.mainloop()

index = [9]
Ch = GirdGui(11,11,5,2)

def start_draw():
    Ch.delAll()
    Ch.drawNumber((4,3),str(index[0]))
    index[0] = index[0] - 1
    if index[0] < 0:
        Ch.tk.destroy()
        return
    Ch.tk.after(1000,start_draw)
if __name__ == '__main__':
    start_draw()
    
    Ch.display()