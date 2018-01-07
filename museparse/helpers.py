import os


def SplitString(value):
    """simple method that puts in spaces every 10 characters"""
    string_length = len(value)
    chunks = int(string_length / 10)
    string_list = list(value)
    lstring = ""

    if chunks > 1:
        lstring = "\\markup { \n\r \column { "
        for i in range(int(chunks)):
            lstring += "\n\r\r \\line { \""
            index = i * 10
            for i in range(index):
                lstring += string_list[i]
            lstring += "\" \r\r}"
        lstring += "\n\r } \n }"
    if lstring == "":
        indexes = [
            i for i in range(
                len(string_list)) if string_list[i] == "\r" or string_list[i] == "\n"]
        lstring = "\\markup { \n\r \column { "
        if len(indexes) == 0:
            lstring += "\n\r\r \\line { \"" + \
                "".join(string_list) + "\" \n\r\r } \n\r } \n }"
        else:
            rows = []
            row_1 = string_list[:indexes[0]]
            rows.append(row_1)
            for i in range(len(indexes)):
                start = indexes[i]
                if i != len(indexes) - 1:
                    end = indexes[i + 1]
                else:
                    end = len(string_list)
                row = string_list[start:end]
                rows.append(row)

            for row in rows:
                lstring += "\n\r\r \\line { \""
                lstring += "".join(row)
                lstring += "\" \r\r}"
            lstring += "\n\r } \n }"
    return lstring


def GetID(attrs, tag, val):
    """
    handy method which pulls out a nested id: attrs refers to a dictionary holding the id
    tag refers to the tag we're looking at (e.g measure, part etc)
    val refers to the exact index of the tag we're looking for (e.g number, id etc)
    example case: attrs = self.attribs, tag=measure and val=number would
    return current measure number
    """

    if tag in attrs:
        if val in attrs[tag]:
            return attrs[tag][val]


def NumbersToWords(number):
    """
    little function that converts numbers to words. This could be more efficient,
    and won't work if the number is bigger than 999 but it's for stave names,
    and I doubt any part would have more than 10 staves let alone 999.
    """

    units = [
        'one',
        'two',
        'three',
        'four',
        'five',
        'six',
        'seven',
        'eight',
        'nine']
    tens = [
        'ten',
        'twenty',
        'thirty',
        'forty',
        'fifty',
        'sixty',
        'seventy',
        'eighty',
        'ninety']
    output = ""
    if number != 0:
        str_val = str(number)
        if 4 > len(str_val) > 2:
            output += units[int(str_val[0]) - 1]
            output += "hundred"
            if str_val[1] != 0:
                output += "and" + tens[int(str_val[1]) - 1]
                if str_val[2] != 0:
                    output += units[int(str_val[2]) - 1]
        if 3 > len(str_val) > 1:
            output += tens[int(str_val[0]) - 1]
            if str_val[1] != 0:
                output += units[int(str_val[1]) - 1]
        if 2 > len(str_val) == 1:
            output += units[int(str_val[0]) - 1]
    else:
        output = "zero"
    return output
