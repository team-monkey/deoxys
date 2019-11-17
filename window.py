from tkinter import *
import deoxys

class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Pokévolution")

        self.label = Label(master, text="Pokévolution Clusterfuck")#heehee bad word XD
        vcmd = master.register(self.validate)

        self.teamNum = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.teamNumLabel = Label(master, text=" # of teams each evolution ")

        self.iterations = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.iterationsLabel = Label(master, text=" # of generations simulated ")

        self.mutRate = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.mutRateLabel = Label(master, text=" Rate of mutation ")

        self.quitButton = Button(master, text="Cancel", command=self.quit)
        self.clearButton = Button(master, text="Clear")#FIXME: add command
        self.startButton = Button(master, text="Start", command=lambda: self.startSim())

        #L A Y OU   T
        self.label.grid(row=0, column=0, columnspan=3, sticky=N)

        self.teamNumLabel.grid(row=1, column=0, sticky=E)
        self.teamNum.grid(row=1, column=1, columnspan=2, sticky=E)
        
        self.iterationsLabel.grid(row=2, column=0, sticky=E)
        self.iterations.grid(row=2, column=1, columnspan=2, sticky=E)

        self.mutRateLabel.grid(row=3, column=0, sticky=E)
        self.mutRate.grid(row=3, column=1, columnspan=2, sticky=E)

        self.quitButton.grid(row=4, column=0, sticky=W+E)
        self.clearButton.grid(row=4, column=1, sticky=S+W+E)
        self.startButton.grid(row=4, column=2, sticky=W+E)

    def validate(self, new_text):
        if not new_text:
            self.entered_number = 0
            return True
        try:
            self.entered_number = float(new_text)
            return True
        except ValueError:
            return False

    def startSim(self):
        tn = int(self.teamNum.get())
        i = int(self.iterations.get())
        mr = float(self.mutRate.get())
        x = deoxys.Simulation(tn, i, mr)
        x.start()

root = Tk()
my_gui = Window(root)
root.mainloop()
