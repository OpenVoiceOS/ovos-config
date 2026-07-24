import warnings

from dateutil.tz import gettz
from ovos_utils.log import deprecated

import ovos_config


def get_config_tz():
    code = ovos_config.Configuration()["location"]["timezone"]["code"]
    return gettz(code)


def get_valid_languages():
    """ return all valid runtime languages according to mycroft.conf """
    lang_code = ovos_config.Configuration().get("lang", "en-us")
    extra_lang_codes = ovos_config.Configuration().get("secondary_langs", [])
    return set([lang_code] + extra_lang_codes)


@deprecated("deprecated without replacement", "1.0.0")
def get_full_lang_code(lang):
    """ given a 2-letter lang code, return the full default 4-letter code"""
    warnings.warn(
        "deprecated without replacement",
        DeprecationWarning,
        stacklevel=2,
    )
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


@deprecated("deprecated without replacement", "1.0.0")
def get_primary_lang_code(config=None):
    """DEPRECATED"""
    warnings.warn(
        "deprecated without replacement",
        DeprecationWarning,
        stacklevel=2,
    )
    return get_default_lang(config).split("-")[0]


@deprecated("deprecated, use ovos_config.Configuration() object directly", "1.0.0")
def get_default_lang(config=None):
    """DEPRECATED"""
    warnings.warn(
        "deprecated, use ovos_config.Configuration() object directly",
        DeprecationWarning,
        stacklevel=2,
    )
    config = config or ovos_config.Configuration()
    return config.get("lang", "en-us")


@deprecated("deprecated without replacement", "1.0.0")
def set_default_lang(lang):
    """DEPRECATED"""
    warnings.warn(
        "deprecated without replacement",
        DeprecationWarning,
        stacklevel=2,
    )
    ovos_config.Configuration()["lang"] = lang


@deprecated("deprecated, use ovos_config.Configuration() object directly", "1.0.0")
def get_default_tz():
    # if default was set at runtime use it else use the timezone from .conf
    warnings.warn(
        "deprecated, use ovos_config.Configuration() object directly",
        DeprecationWarning,
        stacklevel=2,
    )
    return get_config_tz()


@deprecated("deprecated, use ovos_config.Configuration() object directly", "1.0.0")
def set_default_tz(tz=None):
    """ configure timezone across OVOS packages

    currently only configures lingua-franca, in the future
    other hooks may be added if we need to perform this operation globally """

    warnings.warn(
        "deprecated, use ovos_config.Configuration() object directly",
        DeprecationWarning,
        stacklevel=2,
    )
    return get_config_tz()


@deprecated("deprecated without replacement", "1.0.0")
def load_languages(langs):
    """DEPRECATED"""
    warnings.warn(
        "deprecated without replacement",
        DeprecationWarning,
        stacklevel=2,
    )


@deprecated("deprecated without replacement", "1.0.0")
def load_language(lang):
    """DEPRECATED"""
    warnings.warn(
        "deprecated without replacement",
        DeprecationWarning,
        stacklevel=2,
    )


@deprecated("deprecated without replacement", "1.0.0")
def setup_locale(lang=None, tz=None):
    """DEPRECATED"""
    warnings.warn(
        "deprecated without replacement",
        DeprecationWarning,
        stacklevel=2,
    )
    lang_code = lang or ovos_config.Configuration().get("lang", "en-us")
    # Set the active lang to match the configured one
    set_default_lang(lang_code)
    # Set the default timezone to match the configured one
    set_default_tz(tz)


# mycroft-core backwards compat LF only interface
@deprecated("deprecated without replacement", "1.0.0")
def set_default_lf_lang(lang_code="en-us"):
    """DEPRECATED"""
    warnings.warn(
        "deprecated without replacement",
        DeprecationWarning,
        stacklevel=2,
    )
