"""Pygments lexer for XMPP over SIP

With inspiration from HttpLexer and OpenSSLConfLexer.
"""

import re

from pygments.lexer import RegexLexer, bygroups, using
from pygments.token import *

__all__ = ['SdpLexer', 'SipLexer', 'SoxLexer']

class SdpLexer(RegexLexer):
    """
    Lexer for Session Description Protocol (SDP) `RFC 4566
    <http://tools.ietf.org/html/rfc4566>`
    """

    name = 'SDP'
    aliases = ['sdp']
    filenames = ['*.sdp']
    mimetypes = ['application/sdp']

    tokens = {
      'root': [
        (r'^\s+$', Whitespace),
        (r'^(.)(\=)', bygroups(Name.Class, Operator), 'value')
      ],
      'value': [
        ('\n', Whitespace, '#pop'),
        (r'sip:[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+', String),
        (r'[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+', String),
        #(r'\b[\d\.]+\b', Number),
        (r'.', Literal)
      ]
    }

class HeaderValueLexer(RegexLexer):
  name = 'MIME Header Value'
  tokens = {
    'root': [
      (r'&\S*?;', Name.Entity),
      (r'(?:sip:)?[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+', Name.Namespace),
      (r'.', Literal)
    ]
  }

class SipLexer(RegexLexer):
    """
    Session Initiation Protocol (SIP) `RFC 3261
    <http://tools.ietf.org/html/rfc3261>`
    """

    name = 'SIP'
    aliases = ['sip']

    flags = re.DOTALL

    def header_callback(self, match):
        if match.group(1).lower() == 'content-type':
            content_type = match.group(5).strip()
            if ';' in content_type:
                content_type = content_type[:content_type.find(';')].strip()
            self.content_type = content_type
        yield match.start(1), Name.Attribute, match.group(1)
        yield match.start(2), Text, match.group(2)
        yield match.start(3), Operator, match.group(3)
        yield match.start(4), Text, match.group(4)

        hv = HeaderValueLexer()
        for start, tok, s in hv.get_tokens_unprocessed(match.group(5)):
          yield match.start(5)+start, tok, s

        #yield match.start(5), using(HeaderValueLexer), match.group(5)
        yield match.start(6), Text, match.group(6)

    def continuous_header_callback(self, match):
        yield match.start(1), Text, match.group(1)

        hv = HeaderValueLexer()
        for start, tok, s in hv.get_tokens_unprocessed(match.group(2)):
          yield match.start(2)+start, tok, s

        #yield match.start(2), Literal, match.group(2)
        yield match.start(3), Text, match.group(3)

    def content_callback(self, match):
        content_type = getattr(self, 'content_type', None)
        content = match.group()
        offset = match.start()
        if content_type:
            from pygments.lexers import get_lexer_for_mimetype
            try:
                lexer = get_lexer_for_mimetype(content_type)
            except ClassNotFound:
                pass
            else:
                for idx, token, value in lexer.get_tokens_unprocessed(content):
                    yield offset + idx, token, value
                return
        yield offset, Text, content

    tokens = {
        'root': [
            # request
            (r'([A-Z]+)( +)([^ ]+)( +)'
             r'(SIP)(/)(\d+\.\d+)(\r?\n|$)',
             bygroups(Name.Function, Text, Name.Namespace, Text,
                      Keyword.Reserved, Operator, Number, Text),
             'headers'),
            #response
            (r'(SIP)(/)(\d+\.\d+)( +)(\d{3})( +)([^\r\n]+)(\r?\n|$)',
             bygroups(Keyword.Reserved, Operator, Number, Text, Number,
                      Text, Name.Exception, Text),
             'headers'),
        ],
        'headers': [
            (r'([^\s:]+)( *)(:)( *)([^\r\n]+)(\r?\n|$)', header_callback),
            (r'([\t ]+)([^\r\n]+)(\r?\n|$)', continuous_header_callback),
            (r'\r?\n', Text, 'content')
        ],
        'content': [
            (r'.+', content_callback)
        ]
    }

class SoxLexer(RegexLexer):
    """
    Lexer for SIP over XMPP (SoX)
    """

    name = 'SoX'
    aliases = ['sox']
    filenames = ['*.sox']
    flags = re.MULTILINE | re.DOTALL | re.UNICODE

    tokens = {
      'root': [
          ('[^<&]+', Text),
          (r'&\S*?;', Name.Entity),
          (r'\<\!\[CDATA\[.*?\]\]\>', Comment.Preproc),
          ('<!--', Comment, 'comment'),
          (r'<\?.*?\?>', Comment.Preproc),
          ('<![^>]*>', Comment.Preproc),
          (r'<\s*sox', Name.Tag, 'sox'),
          (r'<\s*[\w:.-]+', Name.Tag, 'tag'),
          (r'<\s*/\s*[\w:.-]+\s*>', Name.Tag),
      ],
      'comment': [
          ('[^-]+', Comment),
          ('-->', Comment, '#pop'),
          ('-', Comment),
      ],
      'sox': [
          (r'\s+', Text),
          (r'[\w.:-]+\s*=', Name.Attribute, 'attr'),
          (r'(\s*>)(\s*)([^<]+)', bygroups(Name.Tag, Whitespace, using(SipLexer)), '#pop'),
      ],
      'tag': [
          (r'\s+', Text),
          (r'[\w.:-]+\s*=', Name.Attribute, 'attr'),
          (r'/?\s*>', Name.Tag, '#pop'),
      ],
      'attr': [
          ('\s+', Text),
          ('".*?"', String, '#pop'),
          ("'.*?'", String, '#pop'),
          (r'[^\s>]+', String, '#pop'),
      ],
    }

