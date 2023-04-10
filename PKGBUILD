pkgbase='python-ovos-config'
pkgname=('python-ovos-config')
_module='ovos-config'
pkgver='0.0.7'
pkgrel=1
pkgdesc="OpenVoiceOS configuration tool"
url="https://github.com/OpenVoiceOS/ovos-config"
depends=('python')
makedepends=('python-setuptools')
license=('unknown')
arch=('any')
source=("https://files.pythonhosted.org/packages/8e/33/70f4c643b9e0970d18461c7534861453eb90578bd815864f9db54fbc2526/ovos_config-${pkgver}-py3-none-any.whl")
sha256sums=('098a37b7375d3ba4dceaa85b839e0d9aa03597ba5704f8c22879c730e16b80ef')

build() {
    cd "${srcdir}/${_module}-${pkgver}"
    python setup.py build
}

package() {
    depends+=()
    cd "${srcdir}/${_module}-${pkgver}"
    python setup.py install --root="${pkgdir}" --optimize=1 --skip-build
}
