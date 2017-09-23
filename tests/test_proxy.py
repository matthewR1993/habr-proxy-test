# -*- coding: utf-8 -*-

import unittest
import proxy.converter as conv


class TestTransformRequestFunc(unittest.TestCase):
    def test_common(self):
        input = b'''<html><body><div>looooong mini 
        \xd0\xbf\xd0\xbe\xd0\xb3\xd0\xbe\xd0\xb4\xd0\xb0</div></body></html>'''
        output = '<html>\n <body>\n  <div>\n   looooong mini \n        погода&trade;\n  </div>\n </body>\n</html>'
        self.assertEqual(conv.transform_request(input), output)

    def test_modify_http_urls(self):
        input = b'''<html><body><a href="http://habrahabr.ru/post/338068/"></a></body></html>'''
        output = '<html>\n <body>\n  <a href="http://localhost:8080/post/338068/">\n  </a>\n </body>\n</html>'
        self.assertEqual(conv.transform_request(input), output)

    def test_modify_https_urls(self):
        input = b'''<html><body><a href="https://habrahabr.ru/post/338068/"></a></body></html>'''
        output = '<html>\n <body>\n  <a href="http://localhost:8080/post/338068/">\n  </a>\n </body>\n</html>'
        self.assertEqual(conv.transform_request(input), output)

    def test_skipping_tags(self):
        input = b'''<html><body><script>var longname = 5;</script><style>longword</style>
        <code>longword</code></body></html>'''
        output = '<html>\n <body>\n  <script>\n   var longname = 5;\n  </script>\n  <style>\n   longword\n' \
                 '  </style>\n  <code>\n   longword\n  </code>\n </body>\n</html>'
        self.assertEqual(conv.transform_request(input), output)

    def test_nested_tags(self):
        input = b'''<html><body><p>conten word<p>nested</p></p></body></html>'''
        output = '<html>\n <body>\n  <p>\n   conten&trade; word\n  </p>\n  <p>\n   ' \
                 'nested&trade;\n  </p>\n </body>\n</html>'
        self.assertEqual(conv.transform_request(input), output)


class TestAddLabelsFunc(unittest.TestCase):
    def test_empty(self):
        input = u''
        output = u''
        self.assertEqual(conv.add_labels(input), output)

    def test_only_space(self):
        input = u' '
        output = u' '
        self.assertEqual(conv.add_labels(input), output)

    def test_one_suitable_word(self):
        input = u'погода'
        output = u'погода&trade;'
        self.assertEqual(conv.add_labels(input), output)

    def test_one_little_word(self):
        input = u'дом'
        output = u'дом'
        self.assertEqual(conv.add_labels(input), output)

    def test_one_big_word(self):
        input = u'сатисфакция'
        output = u'сатисфакция'
        self.assertEqual(conv.add_labels(input), output)

    def test_basic(self):
        input = u'тут текстт here is a target toolong'
        output = u'тут текстт&trade; here is a target&trade; toolong'
        self.assertEqual(conv.add_labels(input), output)

    def test_corner_spaces(self):
        input = u' Starting and ending with long words with spaces '
        output = u' Starting and ending&trade; with long words with spaces&trade; '
        self.assertEqual(conv.add_labels(input), output)

    def test_last_word(self):
        input = u'В конце длинно сслово'
        output = u'В конце длинно&trade; сслово&trade;'
        self.assertEqual(conv.add_labels(input), output)

    def test_first_word(self):
        input = u'начало с длиным&trade; словом и все'
        output = u'начало&trade; с длиным&trade; словом&trade; и все'
        self.assertEqual(conv.add_labels(input), output)

    def test_avoiding_punctuation(self):
        input = u'''знаки препя,&trade; как и другая орфоргафия 
        не учитываются! nobody gives a shit!'''
        output = u'''знаки препя,&trade; как и другая&trade; орфоргафия 
        не учитываются! nobody&trade; gives a shit!'''
        self.assertEqual(conv.add_labels(input), output)


if __name__ == '__main__':
    unittest.main()
