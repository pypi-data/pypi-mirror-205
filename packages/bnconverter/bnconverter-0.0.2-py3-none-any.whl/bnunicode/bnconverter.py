from . import util

class UnicodeStreaming:

    # main conversion def
    def convertBnUniCodeToDecode(self, srcString):
        if not srcString:
            return srcString

        srcString = util.doCharMapDecode(srcString)
        return srcString

    def convertBnUniCodeToEncode(self, srcString):
        if not srcString:
            return srcString
        srcString = util.doCharMapEncode(srcString)
        
        return srcString
    
    def bnReplaceUniCodeFont(self,srcString):
        convertEncodeText= self.convertBnUniCodeToEncode(srcString)
        convertDecodeTxt = self.convertBnUniCodeToDecode(convertEncodeText)
        return convertDecodeTxt
    def __init__(self):
        pass