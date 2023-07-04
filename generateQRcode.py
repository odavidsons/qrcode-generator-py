import qrcode
import customtkinter as ctk
from PIL import ImageTk

class generateQRcode(ctk.CTk):

    imagePath = ""
    fontLarge = ("default",18)
    fontMedium = ("default",16)

    def __init__(self):
        super().__init__()
        self.renderUI()

    def renderUI(self):
        frameLeft = ctk.CTkFrame(self)
        frameLeft.grid(row=0,column=0,sticky="nsew",padx=5,pady=10)
        self.tabView = ctk.CTkTabview(frameLeft)
        self.tabView.grid(row=0,column=0,sticky="nsew")
        self.tabView.add("From Text")
        self.tabView.add("From Image")
        self.tabView.set("From Text")
        label1 = ctk.CTkLabel(self.tabView.tab("From Text"),text="Enter text:",font=self.fontMedium)
        label1.grid(row=0,column=0,padx=20)
        self.inputText = ctk.CTkTextbox(self.tabView.tab("From Text"))
        self.inputText.grid(row=1,column=0,padx=20,pady=10)
        label2 = ctk.CTkLabel(self.tabView.tab("From Image"),text="Select image:",font=self.fontMedium)
        label2.grid(row=0,column=0,padx=20)
        btnSelectImg = ctk.CTkButton(self.tabView.tab("From Image"),text="Select",font=self.fontMedium,command=self.selectImage)
        btnSelectImg.grid(row=1,column=0,padx=20,pady=10)
        self.labelImgPath = ctk.CTkLabel(self.tabView.tab("From Image"),text="Path:")
        self.labelImgPath.grid(row=2,column=0,padx=20,pady=5)

        frameCenter = ctk.CTkFrame(self)
        frameCenter.grid(row=0,column=1,padx=5,pady=10)
        btnGenerate = ctk.CTkButton(frameCenter,text=">> Generate >>",font=self.fontMedium,command=self.setType)
        btnGenerate.grid(row=0,column=0,padx=20,pady=20,sticky="ns")
        btnClear = ctk.CTkButton(frameCenter,text="Clear QR Code",font=self.fontMedium,command=self.clearCode)
        btnClear.grid(row=1,column=0,padx=20,pady=20,sticky="ns")

        frameRight = ctk.CTkFrame(self)
        frameRight.grid(row=0,column=2,sticky="nsew",padx=5,pady=10)
        self.labelQRCode = ctk.CTkLabel(frameRight,text="")
        self.labelQRCode.grid(row=0,column=0)

    def selectImage(self):
        filetypes = (('Image Files', '.png .jpeg .jpg'),('All files', '*.*'))
        self.imagePath = ctk.filedialog.askopenfilename(filetypes=filetypes,title="Select an image")
        self.labelImgPath.configure(text=f"Path: {self.imagePath}")

    def setType(self):
        text = self.inputText.get("1.0", "end-1c")
        image = self.imagePath
        selectedTab = self.tabView.get()
        if selectedTab == "From Text":
            self.generateCode(text)
        elif selectedTab == "From Image":
            self.generateCode(image)

    def generateCode(self,data):
        if len(data) != 0:
            try:
                generated = qrcode.make(data)
                img = ImageTk.PhotoImage(generated)
                #PIL = Image.open("qrcode.png")
                #img = ctk.CTkImage(dark_image=generated,size=(self.winfo_height(),self.winfo_height()))
                self.labelQRCode.configure(image=img)
            except: pass
        else: print("Data is empty")

    def clearCode(self):
        self.labelQRCode.configure(image=None)

windowApp = generateQRcode()
windowApp.title("QR Code Generator")
windowApp.resizable(True,True)
windowApp.grid_rowconfigure(0,weight=1)
windowApp.grid_columnconfigure(0,weight=1)
ctk.set_appearance_mode("dark")
windowApp.mainloop()