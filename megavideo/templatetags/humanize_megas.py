from django.template import Library
from django.template import Context, Template
from django.template.defaultfilters import safe

register = Library()

@register.filter
def humanize_bytes(bytes, fontsize = 0):
    precision = 1
    """Return a humanized string representation of a number of bytes.

    Assumes `from __future__ import division`.

    >>> humanize_bytes(1)
    '1 byte'
    >>> humanize_bytes(1024)
    '1.0 kB'
    >>> humanize_bytes(1024*123)
    '123.0 kB'
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    >>> humanize_bytes(1024*12342,2)
    '12.05 MB'
    >>> humanize_bytes(1024*1234,2)
    '1.21 MB'
    >>> humanize_bytes(1024*1234*1111,2)
    '1.31 GB'
    >>> humanize_bytes(1024*1234*1111,1)
    '1.3 GB'
    """

    if fontsize:
        style = ' style="font-size:%s"' % fontsize
    else:
        style = ''

    abbrevs = (
        (1 << 50L, '<span%s>PB</span>' % style),
        (1 << 40L, '<span%s>TB</span>' % style),
        (1 << 30L, '<span%s>GB</span>' % style),
        (1 << 20L, '<span%s>MB</span>' % style),
        (1 << 10L, '<span%s>kB</span>' % style),
        (1, '<span%s>bytes</span>' % style)
    )

    if bytes:
        if bytes == 1:
            return '1 <span%s>byte</span>' % style
        for factor, suffix in abbrevs:
            if bytes >= factor:
                break
        return safe('%.*f %s' % (precision, bytes / factor, suffix))

    return safe('0 <span%s>bytes</span>' % style)
