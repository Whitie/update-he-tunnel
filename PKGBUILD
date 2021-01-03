# Maintainer: Thorsten Weimann <weimann.th@yahoo.com>

pkgname=update-he-tunnel-git
pkgver=0.1
pkgrel=1
pkgdesc='Update HE tunnelbroker.net if external IP changes'
arch=('any')
url='https://github.com/whitie/update-he-tunnel'
license=('MIT')
depends=('python' 'python-requests')
source=('update-he-tunnel.timer' 'update-he-tunnel.service' 'update-he-tunnel.conf'
        'update-he-tunnel.py' 'LICENSE' 'README.md')

md5sums=('a9207c3ceb0939c440c45e14390bcf7e'
         '22a1d17890d6165e8b0e373d47370ce8'
         '99ca43f0a6758b573c57ac7b9a0771bf'
         '5a02ef3792700edd8886478ef25ba23f'
         '683a216c6bcd595b7b4bbc281d5d37b1'
         '6bed779dcb2ca1ef40cea7eb849479b9')

package() {
  install -Dm 755 update-he-tunnel.py "$pkgdir"/usr/bin/update-he-tunnel.py
  install -Dm 644 update-he-tunnel.timer "$pkgdir"/usr/lib/systemd/system/update-he-tunnel.timer
  install -Dm 644 update-he-tunnel.service "$pkgdir"/usr/lib/systemd/system/update-he-tunnel.service
  install -Dm 600 update-he-tunnel.conf "$pkgdir"/etc/update-he-tunnel.conf
}

