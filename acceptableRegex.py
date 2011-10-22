#coding: utf-8
import random
import sre_parse

limit = 10
word = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
wordSet = set(word)
printableASCII = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,!@#$%^&*()-_=+\|`~[]{};:'",.<>/?1234567890 """
printableASCIISet = set(printableASCII)

def getAcceptableRegex(text, isDebug = False):
    def printTree(item, isAll = False):
        outString = ""

        for node in item:
            status = node[0]
            right = node[1]

            if status == sre_parse.NOT_LITERAL:
                while True:
                    t = random.choice(printableASCII)
                    if t != chr(right):
                        break
                outString += t

            if status == sre_parse.LITERAL: #文字列リテラル
                outString += chr(right)

            if status == 'subpattern':      #() の処理
                patternNum = right[0]
                next = right[1]
                outString += printTree(next)

            if status == sre_parse.BRANCH:  # | の分岐
                #print right
                next = random.choice(right[1])
                outString += printTree(next)


            if status == sre_parse.IN:  # []
                if right[0][0] == sre_parse.NEGATE: #[^hoge]
                    disallowedSet = set(printTree(right, True))
                    allowedList = list(printableASCIISet - disallowedSet)
                    outString += random.choice(allowedList)

                else:   #[hoge]
                    next = right
                    if isAll:
                        outString += printTree(next)
                    else:
                        outString += printTree([random.choice(next)])

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
                    outString += printTree(next)

            if status == sre_parse.CATEGORY:    # \dとか
                categorySet = set()
                if right == sre_parse.CATEGORY_DIGIT:
                    categorySet = sre_parse.DIGITS
                elif right == sre_parse.CATEGORY_NOT_DIGIT:
                    categorySet = printableASCIISet - sre_parse.DIGITS
                elif right == sre_parse.CATEGORY_SPACE:
                    categorySet = sre_parse.WHITESPACE
                elif right == sre_parse.CATEGORY_NOT_SPACE:
                    categorySet = printableASCIISet - sre_parse.WHITESPACE
                elif right == sre_parse.CATEGORY_WORD:
                    categorySet = wordSet
                elif right == sre_parse.CATEGORY_NOT_WORD:
                    categorySet = printableASCIISet - wordSet

                if isAll:
                    outString += "".join(categorySet)
                else:
                    outString += random.choice(list(categorySet))

        return outString

    regexTree = sre_parse.parse(text)
    if isDebug:
        print regexTree

    return printTree(regexTree)

if __name__ == "__main__":
    print getAcceptableRegex("(hoge|fooo|fuga|buzz)")
    print getAcceptableRegex("(fug+a{4,10})")
    print getAcceptableRegex("\d+")
    print getAcceptableRegex("[abc]+ , [\d]+ , [\w]+ , [\W]+ , [^abcdefg]+ , [a-z]+")

    # mobile phone(japan)
    print getAcceptableRegex("^0(80-(7([0-3]\d|4[0-8])|9(1[0-4]|0[0-6])|[1-68]\d\d)|90-[1-9]\d\d)\d{5}$")

    # email (short)
    print getAcceptableRegex("[\d\w.]+@(([-a-z0-9]+\.)*[a-z]+|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])")

    # url http://www.din.or.jp/~ohzaki/perl.htm#httpURL
    url = getAcceptableRegex("""https//(([-_.!~*'()a-zA-Z0-9;:&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*@)?(([a-zA-Z0-9]([-a-zA-Z0-9]*[a-zA-Z0-9])?\.)*[a-zA-Z]([-a-zA-Z0-9]*[a-zA-Z0-9])?\.?|[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)(:[0-9]*)?(/([-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*(;([-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*(/([-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*(;([-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*)*)?(\?([-_.!~*'()a-zA-Z0-9;/@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)?(#([-_.!~*'()a-zA-Z0-9;/@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)?""")
    print url

    #try to parse
    import urlparse
    print urlparse.urlparse(url)



