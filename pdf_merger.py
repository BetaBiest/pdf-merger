#!\\bin\env\python3
import os.path
import tkinter
from tkinter import Tk, Menu, Label, LabelFrame, Button, LEFT, Toplevel, Checkbutton
from tkinter.filedialog import askopenfilenames, asksaveasfile
from tkinter.messagebox import showwarning, showinfo
from PyPDF2 import PdfFileMerger


class Program():
  """Main Functionallity of the PDF File Merger"""

  def __init__(self):
    self.__files = []
    self.__fileMerger = PdfFileMerger()

  def addPdfs(self, files=()):
    for file in files:
      self.__files.append(file)
    return self

  def removeAllPdfs(self):
    self.__files = []
    return self

  def removePdf(self, file):
    self.__files.remove(file)
    return self

  def mergePdfs(self, destination):
    for file in self.__files:
      if (os.path.isfile(file)):
        self.__fileMerger.append(file)
      else:
        raise ValueError("File not found")
    self.__fileMerger.write(destination)
    return

  def getFiles(self):
    return self.__files

  def test(self):
    print("Button works")
    return

  # files = property(getFiles) #syntaxsugar if needed


class UI(Program):
  """Graphical UI for the PDF File Merger Program"""

  def __init__(self):
    super().__init__()
    self.root = Tk()

    self.menu = Menu(self.root)
    self.root.config(menu=self.menu)

    self.fileMenu = Menu(self.menu)
    self.menu.add_cascade(label="File", menu=self.fileMenu)
    self.fileMenu.add_command(label="Add PDF", command=self.addPdfs)
    self.fileMenu.add_command(label="Remove file", command=self.removePdf)
    self.fileMenu.add_command(label="Clear files", command=self.removeAllPdfs)
    self.fileMenu.add_command(label="Merge PDFs", command=self.mergePdfs)
    self.fileMenu.add_separator()
    self.fileMenu.add_command(label="Exit", command=self.exit)

    self.helpMenu = Menu(self.menu)
    self.menu.add_cascade(label="Help", menu=self.helpMenu)
    self.helpMenu.add_command(label="?", command=self.q)
    self.helpMenu.add_command(label="About", command=self.about)

    self.frame = LabelFrame(self.root, text="PDF Merger")
    self.frame.pack(fill="both")
    self.labels = []

    self.button_addPdf = Button(
        self.frame, text="Add PDF", command=self.addPdfs)
    self.button_addPdf.pack(side=LEFT)
    self.button_mergePdf = Button(
        self.frame, text="Merge PDFs", command=self.mergePdfs)
    self.button_mergePdf.pack(side=LEFT)

    self.root.mainloop()

  def exit(self):
    self.root.destroy()

  def test(self):
    print("sub")
    super().test()
    return

  def clearLabels(self):
    for label in self.labels:
      label.pack_forget()
    return

  def delLabels(self):
    del self.labels
    self.labels = []
    return

  def addPdfs(self):
    names = askopenfilenames()  # tuple
    super().addPdfs(names)
    self.clearLabels()
    for file in super().getFiles():
      self.labels.append(Label(self.frame, text=file))
      self.labels[- 1].pack()
    return

  def removeAllPdfs(self):
    super().removeAllPdfs()
    self.clearLabels()
    self.delLabels()
    return

  def removePdf(self):
    """Deletes latest file"""
    labelToDelete = self.labels[-1]
    super().removePdf(labelToDelete["text"])
    labelToDelete.pack_forget()
    self.labels.remove(labelToDelete)
    return

  def mergePdfs(self):
    if not self.labels:
      showwarning("Warning", "No files to merge are selected")
    else:
      destination = asksaveasfile(mode="w",
                                  defaultextension=".pdf",
                                  filetypes=[("PDF file", "*.pdf")],
                                  initialdir=os.getcwd(),
                                  initialfile="output.pdf")
      if destination is None:
        showwarning(
            "Warning", "Output process was canceld.\nNo output file selected")
      else:
        super().mergePdfs(destination.name)
    return

  def q(self):
    showinfo("?", "This programm allows you to merge multiple PDF files\nIt concatenates the files in the order they get displayed.")
    return

  def about(self):
    showinfo(
        "About", "Version: 0.01\nAuthor: Leo Schurrer \u00AE\nEmail: l.schurrer@oth-aw.de")
    return


if (__name__ == "__main__"):
  App = UI()
