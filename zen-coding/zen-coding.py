# -*- coding: utf-8 -*-

"""
Kate plugin to support zencoding expansions:
http://www.smashingmagazine.com/2009/11/21/zen-coding-a-new-way-to-write-html-code/
http://code.google.com/p/zen-coding/

@author: Massimiliano Torromeo <massimiliano.torromeo@gmail.com>
"""

import kate
from PyKDE4.ktexteditor import KTextEditor
from zencoding import zen_core

@kate.action('Expand Zencoding Snippet', shortcut="Ctrl+,", menu="Edit")
def zenExpand():
	cursor = kate.activeView().cursorPosition()
	line = str(kate.activeDocument().line( cursor.line() ))
	abbr = zen_core.find_abbr_in_line( line, cursor.column() )
	krange = KTextEditor.Range(cursor.line(), abbr[1], cursor.line(), abbr[1]+len(abbr[0]))
	code = zen_core.expand_abbr(abbr[0], 'html')
	kate.activeDocument().replaceText(krange, code)
