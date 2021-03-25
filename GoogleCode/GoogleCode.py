import os


class WriteOutputFile():

    def __init__(self,Path,FileName,A):
        #Initizializatio
        self.A_NumberOfIntersections = A
        #self.IntersectionID = 0
        #self.E_NumberOfStreets = 0
        #self.Ei_ListOfOrderAndDuration = []
        self.Path = Path
        self.FileName = FileName
        self.OutputFirstLine()

    def OutputFirstLine(self):
        with open(self.Path+"/"+self.FileName,"w") as openfile:
            openfile.write("{}\n".format(self.A_NumberOfIntersections))
        openfile.close()

    def WriteSingleIntersectionOutput(self,i_ID,E_i_IncomingStreets,E_i_OrderDuration):
        with open(self.Path+"/"+self.FileName,"a") as openfile:
            openfile.write("{}\n{}\n".format(i_ID,E_i_IncomingStreets))
            #Loop over Order duration Ei_ListOfOrderAndDuration
            #List of A intersections with format [[String,Duration],[String,Duration]...]
            for i in E_i_OrderDuration:
                openfile.write("{} {}\n".format(i[0],i[1]))
        openfile.close()

ID = 0
IncomingStreets = 3
OrderDuration = [["street 1", 5],["street 2", 10],["street 3", 15]]
ExampleIntersection = [ID,IncomingStreets,OrderDuration]

TimPath = "/home/tim/Documents/Python Scripts/GoogleCode/"
TimFile = "TestOutput"

Output = WriteOutputFile(TimPath,TimFile,5)
Output.WriteSingleIntersectionOutput(*ExampleIntersection)
Output.WriteSingleIntersectionOutput(*ExampleIntersection)
