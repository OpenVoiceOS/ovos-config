# START_VERSION_BLOCK
VERSION_MAJOR = 2
VERSION_MINOR = 3
VERSION_BUILD = 11
VERSION_ALPHA = 2
# END_VERSION_BLOCK

__version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_BUILD}" + (f"a{VERSION_ALPHA}" if VERSION_ALPHA else "")

# Deprecations are removed at the next major bump. Derive the version from
# the block above so deprecation warnings can never drift out of date.
NEXT_MAJOR_VERSION = f"{VERSION_MAJOR + 1}.0.0"
