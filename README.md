binasphere
==========

Short script to assist in Binasphere construction (or other text weaving needs).

    $ echo 'I see
    Do you see me?' > tmp
    $ python binasphere.py join 0,1,1 <tmp
    I Do you see see me?
    $ echo 'I Do you see see me?' | python binasphere.py split 0,1,1
    I see
    Do you see me?

You can also import and use the module.

    >>> import binasphere
    >>> binasphere.join([0, 1, 1], ['I see', 'Do you see me?'])
    'I Do you see see me?'
    >>> binasphere.split([0, 1, 1], 'I Do you see see me?')
    ['I see', 'Do you see me?']
