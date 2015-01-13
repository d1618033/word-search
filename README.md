Word Search
============

Usage
------
    $ python word_search.py [board_size]
    
Prints a word search table in html
containing the words from the stdin.
If `board_size` is not supplied, 
uses the max word length instead.

Example
--------

    $ cat examples/word_list.txt | python word_search.py > examples/word_search.html
    
Opening examples/word_search.html in your browser should show something like this:

    W   V   F   D   O
    K   O   Y   C   D
    I   G   R   I   T
    H   E   L   L   O
    T   U   K   I   D 

