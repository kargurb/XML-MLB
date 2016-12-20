from tkinter import *
import xml.etree.ElementTree as etree

class pitch:

    def __init__(self,w):
        self.w=w
        Button(self.w,text="Choose a file",command=self.clicked).pack()

    def clicked(self):
        try:
            self.fileName=filedialog.askopenfilename()
            self.tree = etree.parse(self.fileName)
            self.root=self.tree.getroot()
            self.peopleDict={}
            for game in self.root:
                for inning in game:
                    for tb in inning:
                        for atbat in tb:
                            if atbat.tag=="atbat":
                                for data in atbat:
                                    batDict=atbat.attrib
                                    pitcher=batDict["pitcher"]
                                    dataDict=data.attrib
                                    try:
                                        speed=float(dataDict["start_speed"])
                                        Type=dataDict["type"]
                                        if Type != "B":
                                            Type="S"
                                        pType=dataDict["pitch_type"]
                                        keys=self.peopleDict.keys()
                                        if pitcher not in keys:
                                            self.peopleDict[pitcher]=[]
                                            self.peopleDict[pitcher].append([pType,speed,Type])
                                        else:
                                            self.peopleDict[pitcher].append([pType,speed,Type])
                                    except:
                                        pass
            
            messagebox.showinfo("Parse successful!", "Press OK to save your output file.")
        except:
            messagebox.showerror("Error", "Invalid xml File")
            return None
        
        self.dict={}
        for key in self.peopleDict.keys():
            name=key
            pitches=self.peopleDict[name]
            typeDict={}
            for pitch in pitches:
                keys=typeDict.keys()
                Type=pitch[0]
                if Type not in keys:
                    typeDict[Type]=[]
                    typeDict[Type].append([pitch[1],pitch[2]])
                else:
                    typeDict[Type].append([pitch[1],pitch[2]])

            Dict={}
            for Type in typeDict.keys():
                pitchList=typeDict[Type]
                speedSum=0
                Bcount=0
                for pitch in pitchList:
                    speedSum=speedSum+pitch[0]
                    if pitch[1]=="B":
                        Bcount=Bcount+1
                speedAvg=speedSum/len(pitchList)
                if Bcount != 0:
                    ratio=float((len(pitchList)-Bcount)/Bcount)
                else:
                    ratio=float(len(pitchList)-Bcount)
                Dict[Type]=[len(pitchList),speedAvg,ratio]
                
            self.dict[key]=[Dict]
        self.writeXML()
        self.result = messagebox.askyesno("Save File", "Do you want to save as XML?")
        if self.result==True:
            self.saveName=filedialog.asksaveasfilename()
            self.tree.write(self.saveName,"UTF-8")
            Label(self.w,text="File successfully Saved!").pack()
        else:
            return None

    def writeXML(self):
        root=etree.Element("Pitchers")
        self.nameList=[]
        for key in self.dict.keys():
            self.nameList.append(key)
        self.nameList.sort()

        for person in self.nameList:
            pitcher=etree.SubElement(root,"Pitcher",name=person) 
            Dict=self.dict[person][0]
            for Type in Dict.keys():
                pitchType=etree.Element("PitchData",pitchType=Type)
                pitcher.append(pitchType)
                PTList=Dict[Type]
                
                NumPitched=etree.Element("NumPitched")
                NumPitched.text=str(PTList[0])
                pitchType.append(NumPitched)

                AvgSpeed=etree.Element("AvgSpeed")
                AvgSpeed.text=str(PTList[1])
                pitchType.append(AvgSpeed)

                StrikeToBallRatio=etree.Element("StrikeToBallRatio")
                StrikeToBallRatio.text=str(PTList[2])
                pitchType.append(StrikeToBallRatio)

        self.tree=etree.ElementTree(root)


w=Tk()
app=pitch(w)
w.mainloop()
