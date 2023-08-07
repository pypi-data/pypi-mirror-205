from . import common


def uniDecode(line):
    conversion_map = common.decode_string_conversion_map
    
    for ascii in conversion_map:
        line = common.preg_replace(ascii, conversion_map[ascii], line)
    
    line = common.ReArrangeUniDecodeText(line)
    line = common.preg_replace('অা', 'আ', line)
    return line

# print(uniDecode("ivwkqvq cov‡kvbv, ‡`‡k wd‡i we‡q, AvR jvk D×vi"))
# print(uniDecode("weGbwc ‡Kv‡bv ‡KŠk‡jB wmwU wbe©vP‡b Ask ‡b‡e bv: dLi“j"))
# print(uniDecode("ivRavbx Dbœqb KZ©…c‡¶i (ivRDK) mvf©vi ‡_‡K c«vq 30 nvRvi M«vn‡Ki bw_ Mv‡qe n‡q hvIqvi NUbv AbymÜv‡b 3 m`‡m¨i KwgwU MVb K‡i‡Q `yb©xwZ `gb Kwgkb (`y`K)|"))