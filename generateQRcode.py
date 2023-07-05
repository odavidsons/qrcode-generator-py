import qrcode
import customtkinter as ctk
from PIL import ImageTk,Image

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
        self.tabView.add("Input data")
        self.tabView.add("Configurations")
        self.tabView.set("Input data")
        label1 = ctk.CTkLabel(self.tabView.tab("Input data"),text="Enter text:",font=self.fontMedium)
        label1.grid(row=0,column=0,padx=20)
        self.inputText = ctk.CTkTextbox(self.tabView.tab("Input data"))
        self.inputText.grid(row=1,column=0,padx=20,pady=10)
        label2 = ctk.CTkLabel(self.tabView.tab("Configurations"),text="Foreground color:")
        label2.grid(row=0,column=0,padx=10)
        colors = ["darkred","red","orange","yellow","green","lime","cyan","blue","purple","violet","pink","white","black","brown"]
        self.foregroundColor = ctk.StringVar()
        self.foregroundColor.set("black")
        select1 = ctk.CTkOptionMenu(self.tabView.tab("Configurations"),variable=self.foregroundColor,values=colors)
        select1.grid(row=0,column=1,padx=10,pady=10)
        label3 = ctk.CTkLabel(self.tabView.tab("Configurations"),text="Background color:")
        label3.grid(row=1,column=0,padx=10)
        self.backgroundColor = ctk.StringVar()
        self.backgroundColor.set("white")
        select2 = ctk.CTkOptionMenu(self.tabView.tab("Configurations"),variable=self.backgroundColor,values=colors)
        select2.grid(row=1,column=1,padx=10,pady=10)
        sizes = ["1","2","3","4","5","6","7","8","9","10"]
        self.qrcodeSize = ctk.StringVar()
        self.qrcodeSize.set("1")
        label4 = ctk.CTkLabel(self.tabView.tab("Configurations"),text="Size:")
        label4.grid(row=2,column=0,padx=10)
        select3 = ctk.CTkOptionMenu(self.tabView.tab("Configurations"),variable=self.qrcodeSize,values=sizes)
        select3.grid(row=2,column=1,padx=10,pady=10)
        label4 = ctk.CTkLabel(self.tabView.tab("Configurations"),text="Logo image:")
        label4.grid(row=3,column=0,padx=10)
        btnSelectImg = ctk.CTkButton(self.tabView.tab("Configurations"),text="Select",command=self.selectImage)
        btnSelectImg.grid(row=3,column=1,padx=10,pady=10)
        self.labelImgPath = ctk.CTkLabel(self.tabView.tab("Configurations"),text="Path:")
        self.labelImgPath.grid(row=4,column=0,padx=20,pady=5)
        frameLeft.grid_rowconfigure(0,weight=1)
        frameLeft.grid_columnconfigure(0,weight=1)

        frameCenter = ctk.CTkFrame(self)
        frameCenter.grid(row=0,column=1,padx=5,pady=10)
        btnGenerate = ctk.CTkButton(frameCenter,text=">> Generate >>",font=self.fontMedium,command=self.generateCode)
        btnGenerate.grid(row=0,column=0,padx=20,pady=20,sticky="ns")
        btnClear = ctk.CTkButton(frameCenter,text="Clear QR Code",font=self.fontMedium,command=self.clearCode)
        btnClear.grid(row=1,column=0,padx=20,pady=20,sticky="ns")
        btnSave = ctk.CTkButton(frameCenter,text="Save as",font=self.fontMedium,command=self.saveCode)
        btnSave.grid(row=2,column=0,padx=20,pady=20,sticky="ns")
        self.labelMessage = ctk.CTkLabel(frameCenter,text="")
        self.labelMessage.grid(row=3,column=0,padx=10,pady=5)
        frameCenter.grid_rowconfigure(0,weight=1)
        frameCenter.grid_columnconfigure(0,weight=1)

        frameRight = ctk.CTkFrame(self)
        frameRight.grid(row=0,column=2,sticky="nsew",padx=5,pady=10)
        self.labelQRCode = ctk.CTkLabel(frameRight,text="")
        self.labelQRCode.grid(row=0,column=0)
        frameRight.grid_rowconfigure(0,weight=1)
        frameRight.grid_columnconfigure(0,weight=1)

    def selectImage(self):
        filetypes = (('Image Files', '.png .jpeg .jpg'),('All files', '*.*'))
        self.imagePath = ctk.filedialog.askopenfilename(filetypes=filetypes,title="Select an image")
        self.labelImgPath.configure(text=f"Path: {self.imagePath}")

    def generateCode(self):
            try:
                self.labelMessage.configure(text="")
                text = self.inputText.get("1.0", "end-1c")
                if self.imagePath != "":
                    logo = Image.open(self.imagePath)
                if len(text)>0:
                    qr = qrcode.QRCode(version=self.qrcodeSize.get(),error_correction=qrcode.ERROR_CORRECT_L,box_size=10,border=4)
                    qr.add_data(text)
                    qr.make(fit=True)
                    generated = qr.make_image(fill_color=self.foregroundColor.get(), back_color=self.backgroundColor.get())
                    qrcode_img = ImageTk.PhotoImage(generated)
                    self.labelQRCode.configure(image=qrcode_img)
                    self.labelMessage.configure(text="Code generated!")
                else: self.labelMessage.configure(text="You can't create an empty QR code.")
            except: self.labelMessage.configure(text="There was an error generating your QR code.")

    def clearCode(self):
        self.labelQRCode.configure(image=None)
        self.labelMessage.configure(text="")

    def saveCode(self):
        if self.labelQRCode.cget("image") != None:
            filetypes = (('Image Files', '.png .jpeg .jpg'),('All files', '*.*'))
            filename = ctk.filedialog.asksaveasfilename(filetypes=filetypes,title="Save image as")
            img = ImageTk.getimage(self.labelQRCode.cget("image"))
            img.save(filename)
            self.labelMessage.configure(text="Image saved!")

windowApp = generateQRcode()
windowApp.title("QR Code Generator")
windowApp.resizable(True,True)
windowApp.grid_rowconfigure(0,weight=1)
windowApp.grid_columnconfigure(0,weight=1)
ctk.set_appearance_mode("dark")
windowApp.mainloop()