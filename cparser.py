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
        
        
class CppParser(object):
    def __init__(self):
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
        self.__parse(str, lambda x: x)
        
    def __parse(self, str, f):
        index = 0
        while index < len(str):
            if (str[index] in string.whitespace):
                f(self.OnWhitespace(str[index]))
                index = index + 1
            else:     
                i, s = self.__sub_parse(str, index, f)
                if (i == -1): index = index + 1
                else: index = i
                
    def __sub_parse(self, str, index, f):
        for parser, callback in self.parsers:
            i, s = parser.parse(str, index)
            if (i != -1):
                f(callback(s))
                return (i, s)
        self.OnError(str[index])
        return (-1, str)

    def transform(self, str):
        out = []
        self.__parse(str, lambda x: out.append(x))
        return ''.join(out)
        
    def OnCppComment(self, s):
        return s
    def OnCComment(self, s):
        return s
    def OnCloseBlock(self, s):
        return s
    def OnOpenBlock(self, s):
        return s
    def OnStatement(self, s):
        return s
    def OnDirective(self, s):
        return s
    def OnWhitespace(self, s):
        return s
    def OnError(self, s):
        return s
