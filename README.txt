================
pygments-sox
================
----------------------------------
A Pygments lexer for SIP over XMPP
----------------------------------

Overview
========

This package provides a SoX protocol lexer for Pygments_.
The lexer is published as an entry point and, once installed, Pygments will
pick it up automatically.

You can then use the ``sox``, ``sip``, and ``sdp`` language with Pygments::

    $ pygmentize -l sox my_protocol_dump.xml

.. _Pygments: http://pygments.org/

Installation
============

Use your favorite installer to install pygments-sox into the same
Python you have installed Pygments. For example::

    $ easy_install pygments-sox

To verify the installation run::

    $ pygmentize -L lexer | grep -i sox
    * sox:
        SoX (filenames *.sox)
