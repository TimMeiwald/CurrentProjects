#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 09:12:37 2021

@author: tim
"""


class Scanner():
    
    def __init__(self,Path,File,List):
        self.String_New, self.String_Old = b"", b""
        self.WHITESPACE = -1
        self.NEWLINE = -2
        self.String_MAXLENGTH = 255
        self.Flag_Comment = False
        self.Flag_Comment_Multiline = False
        self.Flag_String1 = False
        self.Flag_String2 = False
        self.Flag_WhitespaceCounter = 0
        self.GetTokenBuffer = b""
        self.StringStreamBuffer = b""
        self.Dict_KeyToValue, self.Dict_ValueToKey = self.CreateDict(Path,List)
        self.fileHandler = self.OpenFile(Path,File)

        
    def CreateDict(self,Path,List):
        with open(Path + List,"rb") as fileHandler:
            tokens = fileHandler.read().split()
        tokens.sort(key = len)
        Dict_KeyToValue = {}
        Dict_ValueToKey = {}

        Dict_KeyToValue[b"\r"] = self.NEWLINE
        Dict_KeyToValue[b"\n"] = self.NEWLINE
        Dict_KeyToValue[b" "] = self.WHITESPACE
        Dict_ValueToKey[self.WHITESPACE] = b" "
        Dict_ValueToKey[self.NEWLINE] = b"\r"
        Dict_ValueToKey[self.NEWLINE] = b"\n"
        Count = 0
        for i in tokens:
            Dict_KeyToValue[i] = Count
            Dict_ValueToKey[Count] = i
            Count += 1
        #print(Dict_KeyToValue, Dict_ValueToKey)
        return Dict_KeyToValue, Dict_ValueToKey
    
    def OpenFile(self,Path,File):
        try:
            fileHandler = open(Path + File, "rb")
            return fileHandler
        except:
            raise Exception("Failed to open file, check path and file")
    
    def CloseFile(self):
        try:
            self.fileHandler.close()
            return 0
        except:
            raise Exception("Could not successfully close file")


    def GetToken(self):
        if(self.GetTokenBuffer != b"EOF"):
            y2 = self.SplitByToken()
            self.GetTokenBuffer = y2
            y3 = self.CommentStream(y2)
            y4 = self.MultiLineCommentStream(y3)
            y5 = self.StringStream1(y4)
            y6 = self.StringStream2(y5)
            y7 = self.StripNewLinesStream(y6)
            y8 = self.StripWhiteSpaceStream(y7)
            y9 = self.TokenConversionStream(y8)
            if(y9 == None):
                y9 = self.GetToken()
            if(type(y9) == bytes and y9 != b"EOF"):
                y9 = y9.decode("ASCII")
            return y9
        else:
            return b"EOF"

    
    def SplitByToken(self):
        Input = self.fileHandler.read(1)
        if(Input != b""):
            self.String_Old = self.String_New
            self.String_New += Input
            if(self.String_Old in self.Dict_KeyToValue and self.String_New not in self.Dict_KeyToValue):
                self.String_New = Input
                return self.String_Old
            if(self.String_New not in  self.Dict_KeyToValue and Input in self.Dict_KeyToValue):
                self.String_New = Input
                return self.String_Old
            return self.SplitByToken()
        else:
            return b"EOF"
        
    def CommentStream(self,InputStream):
        if(InputStream == b"//"):
            self.Flag_Comment = True
            return None
        elif(InputStream == b"\n" and self.Flag_Comment == True):
            self.Flag_Comment = False
            return None
        else:
            if(self.Flag_Comment == False):
                return InputStream
            else:
                return None
        
    def MultiLineCommentStream(self,InputStream):
        if(InputStream == None):
            return None
        if(InputStream == b"/*"):
            self.Flag_Comment_Multiline = True
            return None
        elif(InputStream == b"*/" and self.Flag_Comment_Multiline  == True):
            self.Flag_Comment_Multiline  = False
            return None
        else:
            if(self.Flag_Comment_Multiline  == False):
                return InputStream
            else:
                return None

    
    def StringStream1(self,InputStream):
        Char = b'"'
        #Char since " and ' need to be handled seperately in e.g Python 
        if(self.Flag_String2 == True):
            return InputStream
        if(InputStream == None):
            return None
        if(InputStream == Char and self.Flag_String1 == True):
            self.Flag_String1 = False
            self.StringStreamBuffer += InputStream
            Temp = self.StringStreamBuffer
            self.StringStreamBuffer = b""
            if(len(Temp) >= self.String_MAXLENGTH):
                raise Exception("String is larger than {} characters".format(self.String_MAXLENGTH))
            else: 
                return Temp.decode("ASCII")
        elif(InputStream == Char):
            self.Flag_String1 = True
            self.StringStreamBuffer += InputStream
            return None
        else:
            if(self.Flag_String1 == False):
                return InputStream
            else:
                self.StringStreamBuffer += InputStream
    
    def StringStream2(self,InputStream):
        #Char since " and ' need to be handled seperately in e.g Python 
        if(self.Flag_String1 == True):
            return InputStream
        Char = b"'"
        if(InputStream == None):
            return None
        if(InputStream == Char and self.Flag_String2 == True):
            self.Flag_String2 = False
            self.StringStreamBuffer += InputStream
            Temp = self.StringStreamBuffer
            self.StringStreamBuffer = b""
            if(len(Temp) >= self.String_MAXLENGTH):
                raise Exception("String is larger than {} characters".format(self.String_MAXLENGTH))
            else: 
                return Temp.decode("ASCII")
        elif(InputStream == Char):
            self.Flag_String2 = True
            self.StringStreamBuffer += InputStream
            return None
        else:
            if(self.Flag_String2 == False):
                return InputStream
            else:
                self.StringStreamBuffer += InputStream
                
    def StripNewLinesStream(self,InputStream):
        if(InputStream == b"\n" or InputStream == b"\r"):
            return b" "
        else:
            return InputStream
    
    def StripWhiteSpaceStream(self,InputStream):
        #Strips ALL whitespace, keeps one since most languages use it
        # as a statement seperator 
        if(InputStream == None): 
            return None
        if(InputStream == b" "):
            self.Flag_WhitespaceCounter += 1
            if(self.Flag_WhitespaceCounter <= 0):
                return InputStream
            else:
                return None
        else:
            self.Flag_WhitespaceCounter = 0
            return InputStream
            

    
    def TokenConversionStream(self, InputStream):
        if(InputStream in self.Dict_KeyToValue):
            return self.Dict_KeyToValue[InputStream]
        else:
            return InputStream
                

    def Descanner(self,TokenList):
        ResultString = b""
        for i in TokenList:
            if(type(i) == int):
                i = self.Dict_ValueToKey[i]
                ResultString += i
            elif(type(i) == str):
                ResultString += i.encode(encoding = "ASCII")
            else:
                if(i == b"EOF"):
                    continue
                else: 
                    ResultString += i
        ResultString = ResultString.decode("ASCII")
        return ResultString

