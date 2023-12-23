from dateutil.tz import gettz, tzlocal

import ovos_config

# lingua_franca is optional and might not be installed
# exceptions should only be raised in the parse and format utils


try:
    import lingua_franca as LF
except ImportError:
    LF = None

_lang = None
_default_tz = None


def get_full_lang_code(lang):
    """ given a 2-letter lang code, return the full default 4-letter code"""
    # first give preference to any configured dialects
    # eg, pt-br instead of pt-pt
    valid_langs = get_valid_languages()
    for l in valid_langs:
        if l.split("-")[0] == lang:
            return l

    # just go with the default full code
    langmap = {'az': 'az-az',
               'ca': 'ca-es',
               'cs': 'cs-cz',
               'da': 'da-dk',
               'de': 'de-de',
               'en': 'en-us',
               'es': 'es-es',
               'eu': 'eu-eu',
               'fa': 'fa-ir',
               'fr': 'fr-fr',
               'hu': 'hu-hu',
               'it': 'it-it',
               'nl': 'nl-nl',
               'pl': 'pl-pl',
               'pt': 'pt-pt',
               'ru': 'ru-ru',
               'sl': 'sl-si',
               'sv': 'sv-se',
               'tr': 'tr-tr',
               'uk': 'uk-ua'}
    return langmap.get(lang)


def get_primary_lang_code(config=None):
    global _lang
    if not _lang:
        config = config or ovos_config.Configuration()
        _lang = config.get("lang", "en-us")
    return _lang.split("-")[0]


def get_default_lang(config=None):
    """
    Get the default localized language code (i.e. `en-us`)
    @param config: Configuration (default is Configuration())
    @return: lowercase BCP-47 language code
    """
    global _lang
    if not _lang:
        config = config or ovos_config.Configuration()
        _lang = config.get("lang", "en-us")
    return _lang


def set_default_lang(lang):
    """ setup default language across OVOS packages
    
    currently only configures lingua-franca language, in the future 
    other hooks may be added if we need to perform this operation globally"""
    global _lang
    _lang = lang
    if LF:
        try:
            LF.set_default_lang(lang)
        except:
            pass

def get_config_tz():
    code = ovos_config.Configuration()["location"]["timezone"]["code"]
    return gettz(code)


def get_default_tz():
    # if default was set at runtime use it else use the timezone from .conf
    return _default_tz or get_config_tz()


def set_default_tz(tz=None):
    """ configure timezone across OVOS packages
    
    currently only configures lingua-franca, in the future 
    other hooks may be added if we need to perform this operation globally """
    global _default_tz
    tz = tz or get_config_tz() or tzlocal()
    _default_tz = tz
    if LF:
        # tz added in recently, depends on version
        try:
            LF.time.set_default_tz(tz)
        except:
            pass


def load_languages(langs):
    """ load and configure lang specific resources across OVOS packages
    
    currently only loads lingua-franca language data, in the future 
    other hooks may be added if we need to perform this operation globally"""
    if LF:
        try:
            LF.load_languages(langs)
        except:
            pass


def load_language(lang):
    """ load and configure lang specific resources across OVOS packages
    
    currently only loads lingua-franca language data, in the future 
    other hooks may be added if we need to perform this operation globally"""
    if LF:
        try:
            LF.load_language(lang)
        except:
            pass


def get_valid_languages():
    """ return all valid runtime languages according to mycroft.conf """
    lang_code = ovos_config.Configuration().get("lang", "en-us")
    extra_lang_codes = ovos_config.Configuration().get("secondary_langs", [])
    return set([lang_code] + extra_lang_codes)


def setup_locale(lang=None, tz=None):
    """ setup default language, timezone and other locale data across OVOS packages
    
    currently only configures lingua-franca, in the future 
    other hooks may be added if we need to perform this operation globally"""
    lang_code = lang or ovos_config.Configuration().get("lang", "en-us")
    valid_langs = get_valid_languages()
    # load any lang specific resources
    load_languages(valid_langs)
    # Set the active lang to match the configured one
    set_default_lang(lang_code)
    # Set the default timezone to match the configured one
    set_default_tz(tz)


# mycroft-core backwards compat LF only interface
def set_default_lf_lang(lang_code="en-us"):
    """Set the default language of Lingua Franca for parsing and formatting.

    Note: this is a temporary method until a global set_default_lang() method
    can be implemented that updates all Mycroft systems eg STT and TTS.
    It will be deprecated at the earliest possible point.

    Args:
        lang (str): BCP-47 language code, e.g. "en-us" or "es-mx"
    """
    return set_default_lang(lang_code)
