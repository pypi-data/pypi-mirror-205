
# bnunicode
Python converting Bangla &lt;=> Unicode (UTF-8) for Bengali to Bangla.


## License
MPL 2.0

## Installation

    pip install bnunicode

## Example
    from bnunicode import UnicodeStreaming
    
    data = UnicodeStreaming()
    unicode_bangla_text = 'Avgvi ‡mvbvi evsjv, Avwg ‡Zvgvh় fv‡jvevwm| wPiw`b ‡Zvgvi AvKvk, ‡Zvgvi evZvm, Avgvi c«v‡Y evRvh় evuwk॥'
    
    print(unicode_bangla_text)
    
    result=data.convertBnUniCodeToDecode(unicode_bangla_text)
    print(result)
    # আমার সোনার বাংলা, আমি তোমায় ভালোবাসি। চিরদিন তোমার আকাশ, তোমার বাতাস, আমার প্রাণে বাজায় বাঁশি॥
    toPrint=test.convertBnUniCodeToDecode(result)
    print(toPrint)

## References:
https://github.com/sh-sabbir/UnicodeToBijoy
