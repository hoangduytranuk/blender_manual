#!/usr/bin/env python3
# same as the closing pattern, so quoted strings can
# be included.  However quotes are not ignored inside
# quotes.  More logic is needed for that....
import re

pat = re.compile("""
    ( .*? )
    ( \( | \) | \[ | \] | \{ | \} | \< | \> |
                           \' | \" | BEGIN | END | $ )
    ( .* )
    """, re.X)

# The keys to the dictionary below are the opening strings,
# and the values are the corresponding closing strings.
# For example "(" is an opening string and ")" is its
# closing string.

matching = { "(" : ")",
             "[" : "]",
             "{" : "}",
             "<" : ">",
             '"' : '"',
             "'" : "'",
             "BEGIN" : "END" }

# The procedure below matches string s and returns a
# recursive list matching the nesting of the open/close
# patterns in s.

def matchnested(s, term=""):
    lst = []
    while True:
        m = pat.match(s)

        if m.group(1) != "":
            lst.append(m.group(1))

        if m.group(2) == term:
            return lst, m.group(3)

        if m.group(2) in matching:
            item, s = matchnested(m.group(3), matching[m.group(2)])
            lst.append(m.group(2))
            lst.append(item)
            lst.append(matching[m.group(2)])
        else:
            raise ValueError("After <<%s %s>> expected %s not %s" %
                             (lst, s, term, m.group(2)))

# Unit test.

if __name__ == "__main__":

    t = "(Current POV syntax is closer to C than Python, so anything that follows two slash character (``//``) is a comment.)"
    try:
        lst, s = matchnested(t)
        print("output", lst)
    except ValueError as e:
        print(str(e))

    #for s in ("simple string",
              #""" "double quote" """,
              #""" 'single quote' """,
              #"one'two'three'four'five'six'seven",
              #"one(two(three(four)five)six)seven",
              #"one(two(three)four)five(six(seven)eight)nine",
              #"one(two)three[four]five{six}seven<eight>nine",
              #"one(two[three{four<five>six}seven]eight)nine",
              #"oneBEGINtwo(threeBEGINfourENDfive)sixENDseven",
              #"ERROR testing ((( mismatched ))] parens"):
        #print("\ninput", s)

        #try:

            #lst, s = matchnested(s)
            #print("output", lst)
        #except ValueError as e:
            #print(str(e))
    print("done")
