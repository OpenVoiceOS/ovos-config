import os
from os.path import basename, dirname, join
from unittest import TestCase

RECS = join(dirname(dirname(dirname(__file__))), "ovos_config", "recommends")


def resolve(lang, folder="base"):
    from ovos_config.utils import find_recommends_file
    path = find_recommends_file(join(RECS, folder), lang)
    return path and basename(path)


class TestRecommendsFileResolution(TestCase):

    def test_region_variant_beats_first_file_of_language(self):
        self.assertEqual(resolve("pt-pt"), "pt-PT.conf")
        self.assertEqual(resolve("pt-PT"), "pt-PT.conf")
        self.assertEqual(resolve("pt-BR"), "pt-BR.conf")

    def test_minority_language_files_are_bare_iso_639_3_codes(self):
        self.assertEqual(resolve("an-ES", "offline_female"), "arg.conf")
        self.assertEqual(resolve("arg", "offline_female"), "arg.conf")
        self.assertEqual(resolve("ast-ES", "offline_female"), "ast.conf")
        self.assertEqual(resolve("oc-FR", "offline_male"), "oci.conf")
        self.assertEqual(resolve("eu"), "eus.conf")
        self.assertEqual(resolve("eu-ES"), "eus.conf")
        self.assertEqual(resolve("kab-DZ", "offline_male"), "kab.conf")

    def test_exact_region_among_several(self):
        self.assertEqual(resolve("es-MX", "online_female"), "es-MX.conf")
        self.assertEqual(resolve("es-US", "online_female"), "es-US.conf")
        self.assertEqual(resolve("es-ES", "online_female"), "es-ES.conf")

    def test_language_without_file_has_no_match(self):
        self.assertIsNone(resolve("xx-XX"))
        self.assertIsNone(resolve("sw-TZ", "offline_female"))

    def test_every_recommends_file_resolves_to_itself(self):
        for folder in os.listdir(RECS):
            if folder == "platform":
                continue
            for f in os.listdir(join(RECS, folder)):
                self.assertEqual(resolve(f[:-5], folder), f, f"{folder}/{f}")

    def test_regional_fallback_is_kept(self):
        self.assertIn(resolve("en-NZ", "offline_female"), ("en-GB.conf", "en-US.conf"))
        self.assertEqual(resolve("pt-AO"), "pt-PT.conf")
        self.assertEqual(resolve("de-AT"), "de-DE.conf")
        self.assertEqual(resolve("pt"), "pt-PT.conf")
        self.assertEqual(resolve("en"), "en-US.conf")
        self.assertEqual(resolve("es-419", "online_female"), "es-MX.conf")
        self.assertEqual(resolve("es-419"), "es-ES.conf")

    def test_other_languages_are_rejected(self):
        self.assertIsNone(resolve("sr-Latn", "gpu"))
        self.assertIsNone(resolve("bs", "gpu"))
        self.assertIsNone(resolve("lb"))
        self.assertIsNone(resolve("zh-TW", "offline_stt"))

    def test_arabic_reaches_modern_standard_arabic(self):
        for lang in ("ar", "ar-SA", "ar-EG", "ar-MA", "arb"):
            for folder in ("offline_female", "offline_male", "offline_stt"):
                self.assertEqual(resolve(lang, folder), "arb.conf", f"{lang} {folder}")

    def test_arabic_in_a_folder_without_msa_file_has_no_match(self):
        self.assertIsNone(resolve("ar-SA"))
        self.assertIsNone(resolve("ar-MA", "gpu"))

    def test_other_macrolanguage_members_do_not_fall_back(self):
        self.assertIsNone(resolve("yue", "offline_stt"))
        self.assertIsNone(resolve("yue-HK", "offline_stt"))

    def test_distance_five_is_kept_in_single_file_folders(self):
        self.assertEqual(resolve("es-419", "base"), "es-ES.conf")
        self.assertEqual(resolve("en-NZ", "online_stt"), "en-US.conf")
