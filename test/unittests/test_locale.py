import os
from os.path import expanduser, dirname, join, isfile

from unittest import TestCase, mock


valid_config = {"lang": "es-mx"}
invalid_config = {"config": "val"}


class TestLocale(TestCase):
    def test_get_get_primary_lang_code(self):
        import ovos_config.locale
        ovos_config.locale.LF = None
        self.assertEqual(
            ovos_config.locale.get_primary_lang_code(valid_config), 'es')
        self.assertEqual(
            ovos_config.locale.get_primary_lang_code(invalid_config), 'en')

    def test_get_default_lang(self):
        import ovos_config.locale
        ovos_config.locale.LF = None
        self.assertEqual(
            ovos_config.locale.get_primary_lang_code(valid_config),
            valid_config['lang'])
        self.assertEqual(
            ovos_config.locale.get_primary_lang_code(invalid_config), 'en-us')

