import datetime

import pyparsing as pp


class ValueParser(object):

    def __init__(self):
        pass

    def __call__(self, value_str):
        parser = self.parser()
        return parser.parseString(value_str)

    def parser(self):
        # Define punctuation as suppressed literals.
        lparen, rparen, lbrack, rbrack, lbrace, rbrace, colon = \
            map(pp.Suppress, "()[]{}:")

        integer = pp.Combine(pp.Optional(pp.oneOf("+ -")) + pp.Word(pp.nums)) \
            .setName("integer") \
            .setParseAction(lambda toks: int(toks[0]))

        real = pp.Combine(pp.Optional(pp.oneOf("+ -")) + pp.Word(pp.nums) + "." +
                          pp.Optional(pp.Word(pp.nums)) +
                          pp.Optional(pp.oneOf("e E") + pp.Optional(pp.oneOf("+ -")) + pp.Word(pp.nums))) \
            .setName("real") \
            .setParseAction(lambda toks: float(toks[0]))

        tuple_str = pp.Forward()
        list_str = pp.Forward()
        dict_str = pp.Forward()

        list_item = real | integer | pp.quotedString.setParseAction(pp.removeQuotes) | \
                    pp.Group(list_str) | tuple_str | dict_str

        tuple_str << (pp.Suppress("(") + pp.Optional(pp.delimitedList(list_item)) +
                      pp.Optional(pp.Suppress(",")) + pp.Suppress(")"))
        tuple_str.setParseAction(lambda toks : tuple(toks.asList()))

        list_str << (lbrack + pp.Optional(pp.delimitedList(list_item) +
                                          pp.Optional(pp.Suppress(","))) + rbrack)

        dict_entry = pp.Group(list_item + colon + list_item)
        dict_str << (lbrace + pp.Optional(pp.delimitedList(dict_entry) +
                                          pp.Optional(pp.Suppress(","))) + rbrace)
        dict_str.setParseAction(lambda toks: dict(toks.asList()))
        return list_item


parse_value = ValueParser()

print parse_value("{ 'A':1, 'B':2, 'C': {'a': 1.2, 'b': 3.4} }")[0]