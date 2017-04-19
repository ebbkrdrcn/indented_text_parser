import re
from math import ceil

class IndentedTextParser(object):

    class Node(object):
        def __init__(self, text=None):
            self.__children = []
            self.__text = text or ''

        def text(self, text=None):
            if not text:
                return self.__text

            self.__text = text

        def children(self):
            return self.__children

        def append_child(self, child):
            self.__children.append(child)

    def __init__(self):
        self.__indent = 2

    def parse(self, input):
        if not isinstance(input, str):
            raise ValueError('input')

        root = self.__class__.Node()
        input = self.__fix_missing_indents(input)
        self.__parse(input.splitlines(), parent=root, depth=1)
        return root

    def __parse(self, lines, parent=None, depth=0):
        while len(lines) > 0:
            l = lines[0]
            d = self.__get_depth(l)
            if d == depth:
                lines.pop(0)
                if not l:
                    continue

                child = self.__class__.Node(l.strip())
                parent.append_child(child)
                if len(lines) > 0:
                    while 1:
                        if not len(lines):
                            return
                        elif lines[0]:
                            break

                        lines.pop(0)

                    d1 = self.__get_depth(lines[0])
                    if d1 > d:
                        self.__parse(lines, parent=child, depth=d1)
                continue
            return

    def __detect_indent(self, input):
        i = 0
        indent = 0
        for it in re.finditer('^((\s+)?)', input, re.MULTILINE | re.DOTALL):
            l = len(it.group(1).split(' ')) - 1
            if indent == 0:
                indent = l
            else:
                if l > indent:
                    if (l % indent) > 0:
                        indent = l
                        continue
                    ni = l - indent
                    if indent == ni:
                        if i >= 3:
                            break
                        i += 1
                    else:
                        indent = ni
                elif indent > l:
                    indent = l
        return indent

    def __fix_missing_indents(self, input):
        fixes = []
        self.__indent = self.__detect_indent(input)
        for line in input.splitlines():
            l = self.__get_indent(line)
            if l > 0 and self.__indent > 0:
                if l % self.__indent > 0:
                    c = (self.__indent * ceil(l / self.__indent)) or self.__indent
                    spaces = ''
                    for i in range(0, int(c)):
                        spaces += ' '
                    fixes.append((line, re.sub(r'^\s+', spaces, line),))

        for x in fixes:
            input = input.replace(x[0], x[1])

        return input

    def __get_indent(self, line):
        m = re.search(r'^(\s+).+', line)
        if m:
            spaces = m.groups()[0].split(' ')
            l = len(spaces) - 1
            return l
        return 0

    def __get_depth(self, line):
        sc = self.__get_indent(line)
        return (sc / self.__indent) + 1
