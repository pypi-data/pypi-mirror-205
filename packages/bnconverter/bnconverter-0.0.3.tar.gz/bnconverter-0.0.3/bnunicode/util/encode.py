from . import common

def uniEncode(line):

    conversion_map = common.encode_string_conversion_map 
    line = common.preg_replace('ো', 'ো', line)
    line = common.preg_replace('ৌ', 'ৌ', line)

    line = common.ReArrangeUniEncodeText(line)

    for  unic in conversion_map:
        line = common.preg_replace(unic, conversion_map[unic], line)
    return line

# print(uniEncode("রাশিয়ায় পড়াশোনা, দেশে ফিরে বিয়ে, আজ লাশ উদ্ধার"))
# print(uniEncode("বিএনপি কোনো কৌশলেই সিটি নির্বাচনে অংশ নেবে না: ফখরুল"))
# print(uniEncode("রাজধানী উন্নয়ন কর্তৃপক্ষের (রাজউক) সার্ভার থেকে প্রায় ৩০ হাজার গ্রাহকের নথি গায়েব হয়ে যাওয়ার ঘটনা অনুসন্ধানে ৩ সদস্যের কমিটি গঠন করেছে দুর্নীতি দমন কমিশন (দুদক)।"))