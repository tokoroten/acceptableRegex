#coding: utf-8
import random
import sre_parse

limit = 10
word = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
wordSet = set(word)
printableASCII = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,!@#$%^&*()-_=+\|`~[]{};:'",.<>/?1234567890 """
printableASCIISet = set(printableASCII)

def getAcceptableRegex(text, isDebug = False, ):
    subpattern = {}
    def walkTree(item, isAll = False):
        outString = ""

        for node in item:
            status = node[0]
            right = node[1]

            if status == sre_parse.NOT_LITERAL: # [^hoge]
                while True:
                    t = random.choice(printableASCII)
                    if t != chr(right):
                        break
                outString += t

            if status == sre_parse.ANY: # .
                if isAll:
                    outString += printableASCII
                else:
                    outString += random.choice(printableASCII)

            if status == sre_parse.LITERAL: #文字列リテラル
                outString += chr(right)

            if status == sre_parse.SUBPATTERN:      #() の処理
                patternNum = right[0]   #(:?hoge) はNone
                next = right[1]
                if patternNum and patternNum in subpattern:
                    text = subpattern[patternNum]
                else:
                    text = walkTree(next)
                    subpattern[patternNum] = text

                outString += text

            if status == sre_parse.GROUPREF:    #groupの参照
                if right in subpattern:
                    outString += subpattern[right]


            if status == sre_parse.BRANCH:  # | の分岐
                #print right
                next = random.choice(right[1])
                outString += walkTree(next)


            if status == sre_parse.IN:  # []
                if right[0][0] == sre_parse.NEGATE: #[^hoge]
                    disallowedSet = set(walkTree(right, True))
                    allowedList = list(printableASCIISet - disallowedSet)
                    outString += random.choice(allowedList)

                else:   #[hoge]
                    next = right
                    if isAll:
                        outString += walkTree(next)
                    else:
                        outString += walkTree([random.choice(next)])

            if status == sre_parse.RANGE:
                if isAll:
                    for i in xrange(right[0], right[1] + 1):
                        outString += chr(i)
                else:
                    outString += chr(random.randrange(right[0], right[1]))

            if status in [sre_parse.MAX_REPEAT, sre_parse.MIN_REPEAT]:  # +,+?,*,*?,?
                minimum = right[0]
                maximum = min(right[1] , limit)
                next = right[2]
                for i in xrange(random.randrange(minimum, maximum + 1)):
                    outString += walkTree(next)

            if status == sre_parse.CATEGORY:    # \dとか
                categorySet = set()
                if right == sre_parse.CATEGORY_DIGIT:   # \d
                    categorySet = sre_parse.DIGITS
                elif right == sre_parse.CATEGORY_NOT_DIGIT: # \D
                    categorySet = printableASCIISet - sre_parse.DIGITS
                elif right == sre_parse.CATEGORY_SPACE: # \s
                    categorySet = sre_parse.WHITESPACE
                elif right == sre_parse.CATEGORY_NOT_SPACE: # \S
                    categorySet = printableASCIISet - sre_parse.WHITESPACE
                elif right == sre_parse.CATEGORY_WORD: # \w
                    categorySet = wordSet
                elif right == sre_parse.CATEGORY_NOT_WORD: # \W
                    categorySet = printableASCIISet - wordSet

                if isAll:
                    outString += "".join(categorySet)
                else:
                    outString += random.choice(list(categorySet))

        return outString

    regexTree = sre_parse.parse(text)
    if isDebug:
        print regexTree

    return walkTree(regexTree)

if __name__ == "__main__":
    print getAcceptableRegex("(hoge|fooo|fuga|buzz)")
    print getAcceptableRegex("(fug+a{4,10})+")
    print getAcceptableRegex("\d+")
    print getAcceptableRegex("[abc]+ , [\d]+ , [\w]+ , [\W]+ , [^abcdefg]+ , [a-z]+")
    print getAcceptableRegex(r"(hoge(foo))(fuga) \1,\2,\3")
    print getAcceptableRegex(r"(\w+(\d+))(\W+) \1,\2,\3")
    print getAcceptableRegex(r"(.+), \1")

    # mobile phone(japan)
    print getAcceptableRegex(r"^0(80-(7([0-3]\d|4[0-8])|9(1[0-4]|0[0-6])|[1-68]\d\d)|90-[1-9]\d\d)\d{5}$")

    # email (short)
    print getAcceptableRegex(r"[\d\w.]+@(([-a-z0-9]+\.)*[a-z]+|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])")


    # url http://www.din.or.jp/~ohzaki/perl.htm#httpURL
    url = getAcceptableRegex("""
(?:https?|shttp)://(?:(?:[-_.!~*'()a-zA-Z0-9;:&=+$,]|%[0-9A-Fa-f
][0-9A-Fa-f])*@)?(?:(?:[a-zA-Z0-9](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.)
*[a-zA-Z](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.?|[0-9]+\.[0-9]+\.[0-9]+\.
[0-9]+)(?::[0-9]*)?(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f]
[0-9A-Fa-f])*(?:;(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-
Fa-f])*)*(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f
])*(?:;(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*)
*)?(?:\?(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])
*)?(?:#(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*
)?
""".replace("\n",""))
    print url

    #try to parse
    import urlparse
    print urlparse.urlparse(url)

