# -*- coding: utf-8 -*-

import unittest
import proxy.converter as conv


class TestTransformRequestFunc(unittest.TestCase):
    def test_common(self):
        input = b'''<html><body><div>looooong 
        \xd1\x81\xd0\xb0\xd0\xbc\xd0\xbe\xd0\xb4\xd1\x83\xd1\x80</div></body></html>'''
        output = '<html>\n <body>\n  <div>\n   looooong&trade; \n        самодур&trade;\n  </div>\n </body>\n</html>'
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
        <code>longword</code><link>another</link></body></html>'''
        output = '<html>\n <body>\n  <script>\n   var longname = 5;\n  </script>\n  <style>\n   longword\n' \
                 '  </style>\n  <code>\n   longword\n  </code>\n  <link/>\n  another&trade;\n </body>\n</html>'
        self.assertEqual(conv.transform_request(input), output)

    def test_nested_tags(self):
        input = b'''<html><body><p>innercontent<p>nestedstuff</p></p></body></html>'''
        output = '<html>\n <body>\n  <p>\n   innercontent&trade;\n  </p>\n  <p>\n   ' \
                 'nestedstuff&trade;\n  </p>\n </body>\n</html>'
        self.assertEqual(conv.transform_request(input), output)


class TestAddLabelsFunc(unittest.TestCase):
    def test_basic(self):
        input = u'Тут находится текст для базового теста here is a text for basic test'
        output = u'Тут находится&trade; текст для базового&trade; теста here is a text for basic test'
        self.assertEqual(conv.add_labels(input), output)

    def test_corner_spaces(self):
        input = u' Starting and ending with long words with spaces '
        output = u' Starting&trade; and ending&trade; with long words with spaces&trade; '
        self.assertEqual(conv.add_labels(input), output)

    def test_last_long(self):
        input = u'В конце длинное словововоло'
        output = u'В конце длинное&trade; словововоло&trade;'
        self.assertEqual(conv.add_labels(input), output)

    def test_first_log(self):
        input = u'начинается длинным словом и все'
        output = u'начинается&trade; длинным&trade; словом&trade; и все'
        self.assertEqual(conv.add_labels(input), output)

    def test_avoiding_punctuation(self):
        input = u'''знаки препинания, как и другая орфоргафия 
        не учитываются! nobody gives a shit!'''
        output = u'''знаки препинания,&trade; как и другая&trade; орфоргафия&trade; 
        не учитываются!&trade; nobody&trade; gives a shit!'''
        self.assertEqual(conv.add_labels(input), output)


if __name__ == '__main__':
    unittest.main()
