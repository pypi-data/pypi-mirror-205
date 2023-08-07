import re

decode_string_conversion_map = {
    'i¨': 'র‌্য',
    'ª¨': '্র্য',
    '°': 'ক্ক',
    '±': 'ক্ট',
    '³': 'ক্ত',
    'K¡': 'ক্ব',
    '¯Œ': 'স্ক্র',
    'µ': 'ক্র',
    'K¬': 'ক্ল',
    '¶': 'ক্ষ',
    'ÿ': 'ক্ষ',
    '·': 'ক্স',
    '¸': 'গু',
    '»': 'গ্ধ',
    'Mœ': 'গ্ন',
    'M¥': 'গ্ম',
    'M­': 'গ্ল',
    '¼': 'ঙ্ক',
    '•¶': 'ঙ্ক্ষ',
    '•L': 'ঙ্খ',
    '½': 'ঙ্গ',
    '•N': 'ঙ্ঘ',
    '•': 'ক্স',
    '”P': 'চ্চ',
    '”Q': 'চ্ছ',
    '”Q¡': 'চ্ছ্ব',
    '”T': 'চ্ঞ',
    '¾¡': 'জ্জ্ব',
    '¾': 'জ্জ',
    'À': 'জ্ঝ',
    'Á': 'জ্ঞ',
    'R¡': 'জ্ব',
    'Â': 'ঞ্চ',
    'Ã': 'ঞ্ছ',
    'Ä': 'ঞ্জ',
    'Å': 'ঞ্ঝ',
    'Æ': 'ট্ট',
    'U¡': 'ট্ব',
    'U¥': 'ট্ম',
    'Ç': 'ড্ড',
    'È': 'ণ্ট',
    'É': 'ণ্ঠ',
    'Ý': 'ন্স',
    'Ê': 'ণ্ড',
    'š‘': 'ন্তু',
    'Y\\^': 'ণ্ব',
    'Ë': 'ত্ত',
    'Ë¡': 'ত্ত্ব',
    'Ì': 'ত্থ',
    'Z¥': 'ত্ম',
    'š—¡': 'ন্ত্ব',
    'Z¡': 'ত্ব',
    'Î': 'ত্র',
    '_¡': 'থ্ব',
    '˜M': 'দ্গ',
    '˜N': 'দ্ঘ',
    'Ï': 'দ্দ',
    '×': 'দ্ধ',
    '˜¡': 'দ্ব',
    'Ø': 'দ্ব',
    '™¢': 'দ্ভ',
    'Ù': 'দ্ম',
    '`ª“': 'দ্রু',
    'aŸ': 'ধ্ব',
    'a¥': 'ধ্ম',
    '›U': 'ন্ট',
    'Ú': 'ন্ঠ',
    'Û': 'ন্ড',
    'šÍ': 'ন্ত',
    'š—': 'ন্ত',
    'š¿': 'ন্ত্র',
    'š’': 'ন্থ',
    '›`': 'ন্দ',
    '›Ø': 'ন্দ্ব',
    'Ü': 'ন্ধ',
    'bœ': 'ন্ন',
    'š\\^': 'ন্ব',
    'b¥': 'ন্ম',
    'Þ': 'প্ট',
    'ß': 'প্ত',
    'cœ': 'প্ন',
    'à': 'প্প',
    'cø': 'প্ল',
    'c­': 'প্ল',
    'á': 'প্স',
    'd¬': 'ফ্ল',
    'â': 'ব্জ',
    'ã': 'ব্দ',
    'ä': 'ব্ধ',
    'eŸ': 'ব্ব',
    'e­': 'ব্ল',
    'å': 'ভ্র',
    'gœ': 'ম্ন',
    '¤ú': 'ম্প',
    'ç': 'ম্ফ',
    '¤\\^': 'ম্ব',
    '¤¢': 'ম্ভ',
    '¤£': 'ম্ভ্র',
    '¤§': 'ম্ম',
    '¤­': 'ম্ল',
    'i“': 'রু',
    'iæ': 'রু',
    'iƒ': 'রূ',
    'é': 'ল্ক',
    'ê': 'ল্গ',
    'ë': 'ল্ট',
    'ì': 'ল্ড',
    'í': 'ল্প',
    'î': 'ল্ফ',
    'j¦': 'ল্ব',
    'j¥': 'ল্ম',
    'jø': 'ল্ল',
    'ï': 'শু',
    'ð': 'শ্চ',
    'kœ': 'শ্ন',
    'kø': 'শ্ল',
    'k¦': 'শ্ব',
    'k¥': 'শ্ম',
    'k­': 'শ্ল',
    '®‹': 'ষ্ক',
    '®Œ': 'ষ্ক্র',
    'ó': 'ষ্ট',
    'ô': 'ষ্ঠ',
    'ò': 'ষ্ণ',
    '®ú': 'ষ্প',
    'õ': 'ষ্ফ',
    '®§': 'ষ্ম',
    '¯‹': 'স্ক',
    '÷': 'স্ট',
    'ö': 'স্খ',
    '¯—': 'স্ত',
    '¯Í': 'স্ত',
    '¯‘': 'স্তু',
    '¯¿': 'স্ত্র',
    '¯’': 'স্থ',
    'mœ': 'স্ন',
    '¯ú': 'স্প',
    'ù': 'স্ফ',
    '¯\\^': 'স্ব',
    '¯§': 'স্ম',
    '¯­': 'স্ল',
    'û': 'হু',
    'nè': 'হ্ণ',
    'ý': 'হ্ন',
    'þ': 'হ্ম',
    'n¬': 'হ্ল',
    'ü': 'হৃ',
    '©': 'র্',
    'Av': 'আ',
    'A': 'অ',
    'B': 'ই',
    'C': 'ঈ',
    'D': 'উ',
    'E': 'ঊ',
    'F': 'ঋ',
    'G': 'এ',
    'H': 'ঐ',
    'I': 'ও',
    'J': 'ঔ',
    'K': 'ক',
    'L': 'খ',
    'M': 'গ',
    'N': 'ঘ',
    'O': 'ঙ',
    'P': 'চ',
    'Q': 'ছ',
    'R': 'জ',
    'S': 'ঝ',
    'T': 'ঞ',
    'U': 'ট',
    'V': 'ঠ',
    'W': 'ড',
    'X': 'ঢ',
    'Y': 'ণ',
    'Z': 'ত',
    '_': 'থ',
    '`': 'দ',
    'a': 'ধ',
    'b': 'ন',
    'c': 'প',
    'd': 'ফ',
    'e': 'ব',
    'f': 'ভ',
    'g': 'ম',
    'h': 'য',
    'i': 'র',
    'j': 'ল',
    'k': 'শ',
    'l': 'ষ',
    'm': 'স',
    'n': 'হ',
    'o': 'ড়',
    'p': 'ঢ়',
    'q': 'য়',
    'r': 'ৎ',
    '0': '০',
    '1': '১',
    '2': '২',
    '3': '৩',
    '4': '৪',
    '5': '৫',
    '6': '৬',
    '7': '৭',
    '8': '৮',
    '9': '৯',
    'v': 'া',
    'w': 'ি',
    'x': 'ী',
    'y': 'ু',
    'z': 'ু',
    '~': 'ূ',
    '„': 'ৃ',
    '‡': 'ে',
    '†': 'ে',
    '‰': 'ৈ',
    '\\ˆ': 'ৈ',
    'Š': 'ৗ',
    'Ô': '‘',
    'Õ': '’',
    '\\|': '।',
    'Ò': '“',
    'Ó': '”',
    's': 'ং',
    't': 'ঃ',
    'u': 'ঁ',
    'ª': '্র',
    'Ö': '্র',
    '«': '্র',
    '¨': '্য',
    '\\&': '্',
    '…': 'ৃ',
}


encode_string_conversion_map = {
    '।'  : '|',
    '‘'  : 'Ô',
    '’'  : 'Õ',
    '“'  : 'Ò',
    '”'  : 'Ó',
    '্র্য'  : 'ª¨',
    'র‌্য': 'i¨',
    'ক্ক': '°',
    'ক্ট': '±',
    'ক্ত': '³',
    'ক্ব': 'K¡',
    'স্ক্র': '¯Œ',
    'ক্র': 'µ',
    'ক্ল': 'K¬',
    'ক্ষ': '¶',
    'ক্স': '·',
    'গু': '¸',
    'গ্ধ': '»',
    'গ্ন': 'Mœ',
    'গ্ম': 'M¥',
    'গ্ল': 'M­',
    'গ্রু': 'Mªy',
    'ঙ্ক': '¼',
    'ঙ্ক্ষ': '•¶',
    'ঙ্খ': '•L',
    'ঙ্গ': '½',
    'ঙ্ঘ': '•N',
    'চ্চ': '”P',
    'চ্ছ': '”Q',
    'চ্ছ্ব': '”Q¡',
    'চ্ঞ': '”T',
    'জ্জ্ব': '¾¡',
    'জ্জ': '¾',
    'জ্ঝ': 'À',
    'জ্ঞ': 'Á',
    'জ্ব': 'R¡',
    'ঞ্চ': 'Â',
    'ঞ্ছ': 'Ã',
    'ঞ্জ': 'Ä',
    'ঞ্ঝ': 'Å',
    'ট্ট': 'Æ',
    'ট্ব': 'U¡',
    'ট্ম': 'U¥',
    'ড্ড': 'Ç',
    'ণ্ট': 'È',
    'ণ্ঠ': 'É',
    'ন্স': 'Ý',
    'ণ্ড': 'Ê',
    'ন্তু': 'š‘',
    'ণ্ব': 'Y^',
    'ত্ত': 'Ë',
    'ত্ত্ব': 'Ë¡',
    'ত্থ': 'Ì',
    'ত্ন': 'Zœ',
    'ত্ম': 'Z¥',
    'ন্ত্ব': 'š—¡',
    'ত্ব': 'Z¡',
    'থ্ব': '_¡',
    'দ্গ': '˜M',
    'দ্ঘ': '˜N',
    'দ্দ': 'Ï',
    'দ্ধ': '×',
    'দ্ব': '˜¡',
    'দ্ব': 'Ø',
    'দ্ভ': '™¢',
    'দ্ম': 'Ù',
    'দ্রু': '`ª“',
    'ধ্ব': 'aŸ',
    'ধ্ম': 'a¥',
    'ন্ট': '›U',
    'ন্ঠ': 'Ú',
    'ন্ড': 'Û',
    'ন্ত্র': 'š¿',
    'ন্ত': 'š—',
    'স্ত্র': '¯¿',
    'ত্র': 'Î',
    'ন্থ': 'š’',
    'ন্দ': '›`',
    'ন্দ্ব': '›Ø',
    'ন্ধ': 'Ü',
    'ন্ন': 'bœ',
    'ন্ব': 'š^',
    'ন্ম': 'b¥',
    'প্ট': 'Þ',
    'প্ত': 'ß',
    'প্ন': 'cœ',
    'প্প': 'à',
    'প্ল': 'c­',
    'প্স': 'á',
    'ফ্ল': 'd¬',
    'ব্জ': 'â',
    'ব্দ': 'ã',
    'ব্ধ': 'ä',
    'ব্ব': 'eŸ',
    'ব্ল': 'e­',
    'ভ্র': 'å',
    'ম্ন': 'gœ',
    'ম্প': '¤ú',
    'ম্ফ': 'ç',
    'ম্ব': '¤^',
    'ম্ভ': '¤¢',
    'ম্ভ্র': '¤£',
    'ম্ম': '¤§',
    'ম্ল': '¤­',
    'রু': 'i“',
    'রূ': 'iƒ',
    'ল্ক': 'é',
    'ল্গ': 'ê',
    'ল্প': 'í',
    'ল্ট': 'ë',
    'ল্ড': 'ì',
    'ল্ফ': 'î',
    'ল্ব': 'j¦',
    'ল্ম': 'j¥',
    'ল্ল': 'jø',
    'শু': 'ï',
    'শ্চ': 'ð',
    'শ্ন': 'kœ',
    'শ্ব': 'k¦',
    'শ্ম': 'k¥',
    'শ্ল': 'kø',
    'ষ্ক': '®‹',
    'ষ্ক্র': '®Œ',
    'ষ্ট': 'ó',
    'ষ্ঠ': 'ô',
    'ষ্ণ': 'ò',
    'ষ্প': '®ú',
    'ষ্ফ': 'õ',
    'ষ্ম': '®§',
    'স্ক': '¯‹',
    'স্ট': '÷',
    'স্খ': 'ö',
    'স্ত': '¯—',
    'স্তু': '¯‘',
    'স্থ': '¯’',
    'স্ন': 'mœ',
    'স্প': '¯ú',
    'স্ফ': 'ù',
    'স্ব': '¯^',
    'স্ম': '¯§',
    'স্ল': '¯­',
    'হু': 'û',
    'হ্ণ': 'nè',
    'হ্ন': 'ý',
    'হ্ম': 'þ',
    'হ্ল': 'n¬',
    'হৃ': 'ü',
    'র্': '©',
    '্র': '«',
    '্য': '¨',
    '্': '&',
    'আ': 'Av',
    'অ': 'A',
    'ই': 'B',
    'ঈ': 'C',
    'উ': 'D',
    'ঊ': 'E',
    'ঋ': 'F',
    'এ': 'G',
    'ঐ': 'H',
    'ও': 'I',
    'ঔ': 'J',
    'ক': 'K',
    'খ': 'L',
    'গ': 'M',
    'ঘ': 'N',
    'ঙ': 'O',
    'চ': 'P',
    'ছ': 'Q',
    'জ': 'R',
    'ঝ': 'S',
    'ঞ': 'T',
    'ট': 'U',
    'ঠ': 'V',
    'ড': 'W',
    'ঢ': 'X',
    'ণ': 'Y',
    'ত': 'Z',
    'থ': '_',
    'দ': '`',
    'ধ': 'a',
    'ন': 'b',
    'প': 'c',
    'ফ': 'd',
    'ব': 'e',
    'ভ': 'f',
    'ম': 'g',
    'য': 'h',
    'র': 'i',
    'ল': 'j',
    'শ': 'k',
    'ষ': 'l',
    'স': 'm',
    'হ': 'n',
    'ড়': 'o',
    'ঢ়': 'p',
    'য়': 'q',
    'ৎ': 'r',
    '০': '0',
    '১': '1',
    '২': '2',
    '৩': '3',
    '৪': '4',
    '৫': '5',
    '৬': '6',
    '৭': '7',
    '৮': '8',
    '৯': '9',
    'া': 'v',
    'ি': 'w',
    'ী': 'x',
    'ু': 'y',
    'ূ': '~',
    'ৃ': '…',
    'ে': '‡',
    'ৈ': '‰',
    'ৗ': 'Š',
    'ং': 's',
    'ঃ': 't',
    'ঁ': 'u',
}


def IsBanglaPreKar(CUni):
    if (CUni == 'ি' or CUni == 'ৈ' or CUni == 'ে'):
        return True; 
    return False

def IsBanglaKar(CUni):
    if (IsBanglaPreKar(CUni) or IsBanglaPostKar(CUni)):
        return True
    return False

def IsBanglaPostKar(CUni):
    if (CUni == 'া' or CUni == 'ো' or CUni == 'ৌ' or CUni == 'ৗ' or CUni == 'ু' or CUni == 'ূ' or CUni == 'ী' or CUni == 'ৃ'):
        return True; 
    return False

def IsBanglaBanjonborno(CUni):
    if (CUni == 'ক' or CUni == 'খ' or CUni == 'গ' or CUni == 'ঘ' or CUni == 'ঙ' or CUni == 'চ' or CUni == 'ছ' or CUni == 'জ' or CUni == 'ঝ' or CUni == 'ঞ' or CUni == 'ট' or CUni == 'ঠ' or CUni == 'ড' or CUni == 'ঢ' or CUni == 'ণ' or CUni == 'ত' or CUni == 'থ' or CUni == 'দ' or CUni == 'ধ' or CUni == 'ন' or CUni == 'প' or CUni == 'ফ' or CUni == 'ব' or CUni == 'ভ' or CUni == 'ম' or CUni == 'শ' or CUni == 'ষ' or CUni == 'স' or CUni == 'হ' or CUni == 'য' or CUni == 'র' or CUni == 'ল' or CUni == 'য়' or CUni == 'ং' or CUni == 'ঃ' or CUni == 'ঁ' or CUni == 'ৎ'):
        return True
    return False

def IsBanglaHalant(CUni):
    if (CUni == '্'):
        return True 
    return False

def IsBanglaNukta(CUni):
    if (CUni == 'ং' or CUni == 'ঃ' or CUni == 'ঁ'):
        return True
    return False

def IsSpace(C):
    if (C == ' ' or C == '\t' or C == '\n' or C == '\r'):
        return True; 
    return False

def preg_replace(srcKey, keyVal, text):
    return re.sub(srcKey, keyVal, text)

def mb_strlen(str):
    return len(str)

def mbCharAt(str, i):
    return str[i]

# returns the javascript 'substring' method equivalent
def subString(string, frm, to):
    return string[frm:to]


def ReArrangeUniDecodeText(str):
    i = 0
    while i<mb_strlen(str):
            
            if ( i > 0 and mbCharAt(str,i) == '\u09CD' and (IsBanglaKar(mbCharAt(str,i - 1)) or IsBanglaNukta(mbCharAt(str,i - 1))) and  i < mb_strlen(str) - 1 ):
                temp = subString(str,0, i - 1)
                temp += mbCharAt(str,i)
                temp += mbCharAt(str,i + 1)
                temp += mbCharAt(str,i - 1)
                temp += subString(str,i + 2, mb_strlen(str))
                str = temp
            
            if (  i > 0 and i < mb_strlen(str) - 1 and mbCharAt(str,i) == '\u09CD' and mbCharAt(str,i - 1) == '\u09B0' and mbCharAt(str,i - 2) != '\u09CD' and  IsBanglaKar(mbCharAt(str,i + 1)) ):
                temp = subString(str,0, i - 1)
                temp += mbCharAt(str,i + 1)
                temp += mbCharAt(str,i - 1)
                temp += mbCharAt(str,i)
                temp += subString(str,i + 2, mb_strlen(str))
                str = temp
            
            if ( i < mb_strlen(str) - 1 and mbCharAt(str,i) == 'র' and IsBanglaHalant(mbCharAt(str,i + 1)) and  not IsBanglaHalant(mbCharAt(str,i - 1)) ):
                j = 1
                while (True) :
                    if (i - j < 0): break
                    if (  IsBanglaBanjonborno(mbCharAt(str,i - j)) and  IsBanglaHalant(mbCharAt(str,i - j - 1)) ):
                        j += 2
                    elif (j == 1 and IsBanglaKar(mbCharAt(str,i - j))): j+=1
                    else: break
                
                temp = subString(str,0, i - j)
                temp += mbCharAt(str,i)
                temp += mbCharAt(str,i + 1)
                temp += subString(str,i - j, i)
                temp += subString(str,i + 2, mb_strlen(str))
                str = temp
                i += 1
                continue
            
            if ( i < mb_strlen(str) - 1 and  IsBanglaPreKar(mbCharAt(str,i)) and IsSpace(mbCharAt(str,i + 1)) == False ) :
                temp = subString(str,0, i)
                j = 1
                while (IsBanglaBanjonborno(mbCharAt(str,i + j))) :
                    if (IsBanglaHalant(mbCharAt(str,i + j + 1))): j += 2
                    else: break
                
                temp += subString(str,i + 1, i + j + 1)
                l = 0
                if (mbCharAt(str,i) == 'ে' and mbCharAt(str,i + j + 1) == 'া') :
                    temp += 'ো'
                    l = 1
                
                elif (mbCharAt(str,i) == 'ে' and mbCharAt(str,i + j + 1) == 'ৗ') :
                    temp += 'ৌ'
                    l = 1
                
                else :
                    temp += mbCharAt(str,i)
                
                temp += subString(str,i + j + l + 1, mb_strlen(str))
                str = temp
                i += j
            
            if ( i < mb_strlen(str) - 1 and mbCharAt(str,i) == 'ঁ' and IsBanglaPostKar(mbCharAt(str,i + 1)) ) :
                temp = subString(str,0, i)
                temp += mbCharAt(str,i + 1)
                temp += mbCharAt(str,i)
                temp += subString(str,i + 2, mb_strlen(str))
                str = temp
            i+=1
    
    return str


def ReArrangeUniEncodeText(str):
    barrier = 0
    i = 0
    while i<mb_strlen(str):
        i+=1
        if (i < mb_strlen(str) and IsBanglaPreKar(mbCharAt(str,i))):
            j = 1
            while (IsBanglaBanjonborno(mbCharAt(str,i - j))):
                if (i - j < 0): break
                if (i - j <= barrier): break
                if (IsBanglaHalant(mbCharAt(str,i - j - 1))): j += 2
                else: break
            
            temp = subString(str,0, i - j)
            temp += mbCharAt(str,i)
            temp += subString(str,i - j, i)
            temp += subString(str,i + 1, mb_strlen(str))
            str = temp
            barrier = i + 1
            continue
        
        if ( i < mb_strlen(str) - 1 and IsBanglaHalant(mbCharAt(str,i)) and  mbCharAt(str,i - 1) == 'র' and not IsBanglaHalant(mbCharAt(str,i - 2)) ):
            j = 1
            found_pre_kar = 0
            while (True):
                if (IsBanglaBanjonborno(mbCharAt(str,i + j)) and  IsBanglaHalant(mbCharAt(str,i + j + 1)) ):
                    j += 2
                elif ( IsBanglaBanjonborno(mbCharAt(str,i + j)) and  IsBanglaPreKar(mbCharAt(str,i + j + 1)) ):
                    found_pre_kar = 1
                    break
                else: break
            
            temp = subString(str,0, i - 1)
            temp += subString(str,i + j + 1, i + j + found_pre_kar + 1)
            temp += subString(str,i + 1, i + j + 1)
            temp += mbCharAt(str,i - 1)
            temp += mbCharAt(str,i)
            temp += subString(str,i + j + found_pre_kar + 1, mb_strlen(str))
            str = temp
            i += j + found_pre_kar
            barrier = i + 1
            continue
        
    
    return str

