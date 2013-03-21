#!/bin/python
import sys, os, re, string


class ParseDirective:
    def parse(self, str, i):
        #print "Parsing Directive"
        if (str[i] == '#'):
            start = i
            end = -1
            while i < len(str) and end == -1:
                if str[i] == '\n': end = i + 1
                i = i + 1
            if end != -1: return (end, str[start:end])
        return (-1, str)
    
class ParseCloseBlock:
    def parse(self, str, i):
        #print "Parsing CloseBlock"
        if (str[i] == '}'): return (i+1, str[i])
        else: return (-1, str)
        
class ParseOpenBlock:
    def parse(self, str, i):
        #print "Parsing OpenBlock"
        start = i;
        end = -1
        while i < len(str) and end == -1:
            if (str[i] == ';' or str[i] == '}'): break
            if (str[i] == '{'): end = i + 1
            i = i + 1
        if end == -1: return (end, str)
        else: return (end, str[start:end])
    
    
class ParseStatement:
    def parse(self, str, i):
        #print "Parsing Statement"
        start = i;
        end = -1
        while i < len(str) and end == -1:
            if (str[i] == '{' or str[i] == '}'): break
            if (str[i] == ';'): end = i + 1
            i = i + 1
        if end == -1: return (end, str)
        else: return (end, str[start:end])
        
class ParseCComment:
    def parse(self, str, i):
        #print "Parsing CComment"
        if ((len(str) - i) > 4 and str[i] == '/' and str[i+1] == '*'):
            start = i
            end = -1
            prevC = ' '
            while i < len(str) and end == -1:
                if (prevC == '*' and str[i] == '/'): end = i + 1
                prevC = str[i]
                i = i + 1
            if end != -1: return (end, str[start:end])
        return (-1, str)
        
class ParseCppComment:
    def parse(self, str, i):
        #print "Parsing CppComment"
        if ((len(str) - i) > 4 and str[i] == '/' and str[i+1] == '/'):
            start = i
            end = -1
            while i < len(str) and end == -1:
                if str[i] == '\n': end = i + 1
                i = i + 1
            if end != -1: return (end, str[start:end])
        return (-1, str)
        
        
class CppParser:
    def __init__(self):
        self.OnCppComment = lambda x: self.OnText(x)
        self.OnCComment = lambda x: self.OnText(x)
        self.OnCloseBlock = lambda x: self.OnText(x)
        self.OnOpenBlock = lambda x: self.OnText(x)
        self.OnStatement = lambda x: self.OnText(x)
        self.OnDirective = lambda x: self.OnText(x)
        self.OnWhitespace = lambda x: self.OnText(x)
        self.OnError = lambda x: self.OnText(x)
        self.parsers = \
        [
            (ParseCppComment(), lambda x: self.OnCppComment(x)),
            (ParseCComment(), lambda x: self.OnCComment(x)),
            (ParseDirective(), lambda x: self.OnDirective(x)),
            (ParseCloseBlock(), lambda x: self.OnCloseBlock(x)),
            (ParseOpenBlock(), lambda x: self.OnOpenBlock(x)),
            (ParseStatement(), lambda x: self.OnStatement(x))
        ]
        
        
    def parse(self, str):
        index = 0
        while index < len(str):
            if (str[index] in string.whitespace):
                self.OnWhitespace(str[index])
                index = index + 1
            else:     
                i, s = self.sub_parse(str, index)
                if (i == -1): index = index + 1
                else: index = i
                
    def sub_parse(self, str, index):
        for parser, callback in self.parsers:
            i, s = parser.parse(str, index)
            if (i != -1):
                callback(s)
                return (i, s)
        self.OnError(str[index])
        return (-1, str)
        
    def OnText(self, s):
        return s