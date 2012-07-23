# -*- coding: utf-8 -*-

"""
Kate plugin to support zencoding expansions:
http://www.smashingmagazine.com/2009/11/21/zen-coding-a-new-way-to-write-html-code/
http://code.google.com/p/zen-coding/

@author: Massimiliano Torromeo <massimiliano.torromeo@gmail.com>
"""

import kate
import re

from PyKDE4.ktexteditor import KTextEditor
from zencoding import zen_core

find_spaces = re.compile("\s*")

@kate.action('Expand Zencoding Snippet', shortcut="Ctrl+,", menu="Edit")
def zenExpand():
    cursor = kate.activeView().cursorPosition()
    line = str(kate.activeDocument().line( cursor.line() ))
    abbr = zen_core.find_abbr_in_line( line, cursor.column() )
    code = zen_core.expand_abbreviation(abbr[0], 'html', 'xhtml')

    indentation = find_spaces.match(line).group(0)

    codelines = code.splitlines()
    cursor_column = -1
    for i, codeline in enumerate(codelines):
        if i > 0:
            codeline = indentation + codeline
            codelines[i] = codeline

        if cursor_column >= 0:
            continue

        cursor_column = codeline.find('|')
        if cursor_column >= 0:
            cursor_line = i
            codelines[cursor_line] = codeline[:cursor_column] + codeline[cursor_column+1:]
            cursor_column -= len(find_spaces.match(codeline).group(0))

    code = "\n".join(codelines)

    krange = KTextEditor.Range(cursor.line(), abbr[1], cursor.line(), abbr[1]+len(abbr[0]))
    kate.activeDocument().replaceText(krange, code)

    if cursor_column >= 0:
        cursor.setLine(cursor.line() + cursor_line)
        line = str(kate.activeDocument().line( cursor.line() ))
        if cursor_line == 0:
            cursor_column += abbr[1]
        else:
            cursor_column += len(find_spaces.match(line).group(0))
        cursor.setColumn(cursor_column)
        kate.activeView().setCursorPosition(cursor)
