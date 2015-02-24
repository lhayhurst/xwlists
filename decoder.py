#!/usr/bin/python -u
# -*- coding: utf-8 -*-

##
## cp1252 to UTF-8 decoder
##
## An expansion of the code found at http://effbot.org/zone/unicode-gremlins.htm
##

import re
import unicodedata


cp1252 = {

    u"\x80": u"\u20AC",    #            e282ac
    u"\x81": u"\uFFFD",    #    `   ?    efbfbd
    u"\x82": u"\u201A",    #            e2809a
    u"\x83": u"\u0192",    #    à   à   c692
    u"\x84": u"\u201E",    #    Ġ   Ġ   e2809e
    u"\x85": u"\u2026",    #    Š   Š   e280a6
    u"\x86": u"\u2020",    #    Ơ   Ơ   e280a0
    u"\x87": u"\u2021",    #    Ǡ   Ǡ   e280a1
    u"\x88": u"\u02C6",    #    Ƞ   Ƞ   cb86
    u"\x89": u"\u2030",    #    ɠ   ɠ   e280b0
    u"\x8a": u"\u0160",    #    ʠ   ʠ   c5a0
    u"\x8b": u"\u2039",    #    ˠ   ˠ   e280b9
    u"\x8c": u"\u0152",    #    ̠   ̠   c592
    u"\x8d": u"\uFFFD",    #    ͠   ?    efbfbd
    u"\x8e": u"\u017D",    #    Π   Π   c5bd
    u"\x8f": u"\uFFFD",    #    Ϡ   ?    efbfbd
    u"\x90": u"\uFFFD",    #    Р   ?    efbfbd
    u"\x91": u"\u2018",    #    Ѡ   Ѡ   e28098
    u"\x92": u"\u2019",    #    Ҡ   Ҡ   e28099
    u"\x93": u"\u201C",    #    Ӡ   Ӡ   e2809c
    u"\x94": u"\u201D",    #    Ԡ   Ԡ   e2809d
    u"\x95": u"\u2022",    #    ՠ   ՠ   e280a2
    u"\x96": u"\u2013",    #    ֠   ֠   e28093
    u"\x97": u"\u2014",    #    נ   נ   e28094
    u"\x98": u"\u02DC",    #    ؠ   ؠ   cb9c
    u"\x99": u"\u2122",    #    ٠   ٠   e284a2
    u"\x9a": u"\u0161",    #    ڠ   ڠ   c5a1
    u"\x9b": u"\u203A",    #    ۠   ۠   e280ba
    u"\x9c": u"\u0153",    #    ܠ   ܠ   c593
    u"\x9d": u"\uFFFD",    #    ݠ   ?    efbfbd
    u"\x9e": u"\u017E",    #    ޠ   ޠ   c5be
    u"\x9f": u"\u0178",    #    ߠ   ߠ   c5b8
    u"\xa0": u"\u00A0",    #             c2a0
    u"\xa1": u"\u00A1",    #    `   `   c2a1
    u"\xa2": u"\u00A2",    #            c2a2
    u"\xa3": u"\u00A3",    #    à   à   c2a3
    u"\xa4": u"\u00A4",    #    Ġ   Ġ   c2a4
    u"\xa5": u"\u00A5",    #    Š   Š   c2a5
    u"\xa6": u"\u00A6",    #    Ơ   Ơ   c2a6
    u"\xa7": u"\u00A7",    #    Ǡ   Ǡ   c2a7
    u"\xa8": u"\u00A8",    #    Ƞ   Ƞ   c2a8
    u"\xa9": u"\u00A9",    #    ɠ   ɠ   c2a9
    u"\xaa": u"\u00AA",    #    ʠ   ʠ   c2aa
    u"\xab": u"\u00AB",    #    ˠ   ˠ   c2ab
    u"\xac": u"\u00AC",    #    ̠   ̠   c2ac
    u"\xad": u"\u00AD",    #    ͠   ͠   c2ad
    u"\xae": u"\u00AE",    #    Π   Π   c2ae
    u"\xaf": u"\u00AF",    #    Ϡ   Ϡ   c2af
    u"\xb0": u"\u00B0",    #    Р   Р   c2b0
    u"\xb1": u"\u00B1",    #    Ѡ   Ѡ   c2b1
    u"\xb2": u"\u00B2",    #    Ҡ   Ҡ   c2b2
    u"\xb3": u"\u00B3",    #    Ӡ   Ӡ   c2b3
    u"\xb4": u"\u00B4",    #    Ԡ   Ԡ   c2b4
    u"\xb5": u"\u00B5",    #    ՠ   ՠ   c2b5
    u"\xb6": u"\u00B6",    #    ֠   ֠   c2b6
    u"\xb7": u"\u00B7",    #    נ   נ   c2b7
    u"\xb8": u"\u00B8",    #    ؠ   ؠ   c2b8
    u"\xb9": u"\u00B9",    #    ٠   ٠   c2b9
    u"\xba": u"\u00BA",    #    ڠ   ڠ   c2ba
    u"\xbb": u"\u00BB",    #    ۠   ۠   c2bb
    u"\xbc": u"\u00BC",    #    ܠ   ܠ   c2bc
    u"\xbd": u"\u00BD",    #    ݠ   ݠ   c2bd
    u"\xbe": u"\u00BE",    #    ޠ   ޠ   c2be
    u"\xbf": u"\u00BF",    #    ߠ   ߠ   c2bf
    u"\xc0": u"\u00C0",    #            c380
    u"\xc1": u"\u00C1",    #    `   `   c381
    u"\xc2": u"\u00C2",    #            c382
    u"\xc3": u"\u00C3",    #    à   à   c383
    u"\xc4": u"\u00C4",    #    Ġ   Ġ   c384
    u"\xc5": u"\u00C5",    #    Š   Š   c385
    u"\xc6": u"\u00C6",    #    Ơ   Ơ   c386
    u"\xc7": u"\u00C7",    #    Ǡ   Ǡ   c387
    u"\xc8": u"\u00C8",    #    Ƞ   Ƞ   c388
    u"\xc9": u"\u00C9",    #    ɠ   ɠ   c389
    u"\xca": u"\u00CA",    #    ʠ   ʠ   c38a
    u"\xcb": u"\u00CB",    #    ˠ   ˠ   c38b
    u"\xcc": u"\u00CC",    #    ̠   ̠   c38c
    u"\xcd": u"\u00CD",    #    ͠   ͠   c38d
    u"\xce": u"\u00CE",    #    Π   Π   c38e
    u"\xcf": u"\u00CF",    #    Ϡ   Ϡ   c38f
    u"\xd0": u"\u00D0",    #    Р   Р   c390
    u"\xd1": u"\u00D1",    #    Ѡ   Ѡ   c391
    u"\xd2": u"\u00D2",    #    Ҡ   Ҡ   c392
    u"\xd3": u"\u00D3",    #    Ӡ   Ӡ   c393
    u"\xd4": u"\u00D4",    #    Ԡ   Ԡ   c394
    u"\xd5": u"\u00D5",    #    ՠ   ՠ   c395
    u"\xd6": u"\u00D6",    #    ֠   ֠   c396
    u"\xd7": u"\u00D7",    #    נ   נ   c397
    u"\xd8": u"\u00D8",    #    ؠ   ؠ   c398
    u"\xd9": u"\u00D9",    #    ٠   ٠   c399
    u"\xda": u"\u00DA",    #    ڠ   ڠ   c39a
    u"\xdb": u"\u00DB",    #    ۠   ۠   c39b
    u"\xdc": u"\u00DC",    #    ܠ   ܠ   c39c
    u"\xdd": u"\u00DD",    #    ݠ   ݠ   c39d
    u"\xde": u"\u00DE",    #    ޠ   ޠ   c39e
    u"\xdf": u"\u00DF",    #    ߠ   ߠ   c39f
    u"\xe0": u"\u00E0",    #    ࠠ  ࠠ  c3a0
    u"\xe1": u"\u00E1",    #    ᠠ  ᠠ  c3a1
    u"\xe2": u"\u00E2",    #    ⠠  ⠠  c3a2
    u"\xe3": u"\u00E3",    #    㠠  㠠  c3a3
    u"\xe4": u"\u00E4",    #    䠠  䠠  c3a4
    u"\xe5": u"\u00E5",    #    堠  堠  c3a5
    u"\xe6": u"\u00E6",    #    栠  栠  c3a6
    u"\xe7": u"\u00E7",    #    砠  砠  c3a7
    u"\xe8": u"\u00E8",    #    蠠  蠠  c3a8
    u"\xe9": u"\u00E9",    #    頠  頠  c3a9
    u"\xea": u"\u00EA",    #    ꠠ  ꠠ  c3aa
    u"\xeb": u"\u00EB",    #    렠  렠  c3ab
    u"\xec": u"\u00EC",    #    젠  젠  c3ac
    u"\xed": u"\u00ED",    #    ��  ��  c3ad
    u"\xee": u"\u00EE",    #        c3ae
    u"\xef": u"\u00EF",    #        c3af
    u"\xf0": u"\u00F0",    #    𠠠 𠠠 c3b0
    u"\xf1": u"\u00F1",    #    񠠠 񠠠 c3b1
    u"\xf2": u"\u00F2",    #    򠠠 򠠠 c3b2
    u"\xf3": u"\u00F3",    #    󠠠 󠠠 c3b3
    u"\xf4": u"\u00F4",    #    ���� ���� c3b4
    u"\xf5": u"\u00F5",    #    ���� ���� c3b5
    u"\xf6": u"\u00F6",    #    ���� ���� c3b6
    u"\xf7": u"\u00F7",    #    ���� ���� c3b7
    u"\xf8": u"\u00F8",    #    𠠠 𠠠 c3b8
    u"\xf9": u"\u00F9",    #    񠠠 񠠠 c3b9
    u"\xfa": u"\u00FA",    #    򠠠 򠠠 c3ba
    u"\xfb": u"\u00FB",    #    󠠠 󠠠 c3bb
    u"\xfc": u"\u00FC",    #    ���� ���� c3bc
    u"\xfd": u"\u00FD",    #    ���� ���� c3bd
    u"\xfe": u"\u00FE",    #    ���� ���� c3be
    u"\xff": u"\u00FF",    #    ���� ���� c3bf

}
cp1252 = {

    u"\x80": u"\u20AC",    #            e282ac
    u"\x81": u"\uFFFD",    #    `   ?    efbfbd
    u"\x82": u"\u201A",    #            e2809a
    u"\x83": u"\u0192",    #    à   à   c692
    u"\x84": u"\u201E",    #    Ġ   Ġ   e2809e
    u"\x85": u"\u2026",    #    Š   Š   e280a6
    u"\x86": u"\u2020",    #    Ơ   Ơ   e280a0
    u"\x87": u"\u2021",    #    Ǡ   Ǡ   e280a1
    u"\x88": u"\u02C6",    #    Ƞ   Ƞ   cb86
    u"\x89": u"\u2030",    #    ɠ   ɠ   e280b0
    u"\x8a": u"\u0160",    #    ʠ   ʠ   c5a0
    u"\x8b": u"\u2039",    #    ˠ   ˠ   e280b9
    u"\x8c": u"\u0152",    #    ̠   ̠   c592
    u"\x8d": u"\uFFFD",    #    ͠   ?    efbfbd
    u"\x8e": u"\u017D",    #    Π   Π   c5bd
    u"\x8f": u"\uFFFD",    #    Ϡ   ?    efbfbd
    u"\x90": u"\uFFFD",    #    Р   ?    efbfbd
    u"\x91": u"\u2018",    #    Ѡ   Ѡ   e28098
    u"\x92": u"\u2019",    #    Ҡ   Ҡ   e28099
    u"\x93": u"\u201C",    #    Ӡ   Ӡ   e2809c
    u"\x94": u"\u201D",    #    Ԡ   Ԡ   e2809d
    u"\x95": u"\u2022",    #    ՠ   ՠ   e280a2
    u"\x96": u"\u2013",    #    ֠   ֠   e28093
    u"\x97": u"\u2014",    #    נ   נ   e28094
    u"\x98": u"\u02DC",    #    ؠ   ؠ   cb9c
    u"\x99": u"\u2122",    #    ٠   ٠   e284a2
    u"\x9a": u"\u0161",    #    ڠ   ڠ   c5a1
    u"\x9b": u"\u203A",    #    ۠   ۠   e280ba
    u"\x9c": u"\u0153",    #    ܠ   ܠ   c593
    u"\x9d": u"\uFFFD",    #    ݠ   ?    efbfbd
    u"\x9e": u"\u017E",    #    ޠ   ޠ   c5be
    u"\x9f": u"\u0178",    #    ߠ   ߠ   c5b8
    u"\xa0": u"\u00A0",    #             c2a0
    u"\xa1": u"\u00A1",    #    `   `   c2a1
    u"\xa2": u"\u00A2",    #            c2a2
    u"\xa3": u"\u00A3",    #    à   à   c2a3
    u"\xa4": u"\u00A4",    #    Ġ   Ġ   c2a4
    u"\xa5": u"\u00A5",    #    Š   Š   c2a5
    u"\xa6": u"\u00A6",    #    Ơ   Ơ   c2a6
    u"\xa7": u"\u00A7",    #    Ǡ   Ǡ   c2a7
    u"\xa8": u"\u00A8",    #    Ƞ   Ƞ   c2a8
    u"\xa9": u"\u00A9",    #    ɠ   ɠ   c2a9
    u"\xaa": u"\u00AA",    #    ʠ   ʠ   c2aa
    u"\xab": u"\u00AB",    #    ˠ   ˠ   c2ab
    u"\xac": u"\u00AC",    #    ̠   ̠   c2ac
    u"\xad": u"\u00AD",    #    ͠   ͠   c2ad
    u"\xae": u"\u00AE",    #    Π   Π   c2ae
    u"\xaf": u"\u00AF",    #    Ϡ   Ϡ   c2af
    u"\xb0": u"\u00B0",    #    Р   Р   c2b0
    u"\xb1": u"\u00B1",    #    Ѡ   Ѡ   c2b1
    u"\xb2": u"\u00B2",    #    Ҡ   Ҡ   c2b2
    u"\xb3": u"\u00B3",    #    Ӡ   Ӡ   c2b3
    u"\xb4": u"\u00B4",    #    Ԡ   Ԡ   c2b4
    u"\xb5": u"\u00B5",    #    ՠ   ՠ   c2b5
    u"\xb6": u"\u00B6",    #    ֠   ֠   c2b6
    u"\xb7": u"\u00B7",    #    נ   נ   c2b7
    u"\xb8": u"\u00B8",    #    ؠ   ؠ   c2b8
    u"\xb9": u"\u00B9",    #    ٠   ٠   c2b9
    u"\xba": u"\u00BA",    #    ڠ   ڠ   c2ba
    u"\xbb": u"\u00BB",    #    ۠   ۠   c2bb
    u"\xbc": u"\u00BC",    #    ܠ   ܠ   c2bc
    u"\xbd": u"\u00BD",    #    ݠ   ݠ   c2bd
    u"\xbe": u"\u00BE",    #    ޠ   ޠ   c2be
    u"\xbf": u"\u00BF",    #    ߠ   ߠ   c2bf
    u"\xc0": u"\u00C0",    #            c380
    u"\xc1": u"\u00C1",    #    `   `   c381
    u"\xc2": u"\u00C2",    #            c382
    u"\xc3": u"\u00C3",    #    à   à   c383
    u"\xc4": u"\u00C4",    #    Ġ   Ġ   c384
    u"\xc5": u"\u00C5",    #    Š   Š   c385
    u"\xc6": u"\u00C6",    #    Ơ   Ơ   c386
    u"\xc7": u"\u00C7",    #    Ǡ   Ǡ   c387
    u"\xc8": u"\u00C8",    #    Ƞ   Ƞ   c388
    u"\xc9": u"\u00C9",    #    ɠ   ɠ   c389
    u"\xca": u"\u00CA",    #    ʠ   ʠ   c38a
    u"\xcb": u"\u00CB",    #    ˠ   ˠ   c38b
    u"\xcc": u"\u00CC",    #    ̠   ̠   c38c
    u"\xcd": u"\u00CD",    #    ͠   ͠   c38d
    u"\xce": u"\u00CE",    #    Π   Π   c38e
    u"\xcf": u"\u00CF",    #    Ϡ   Ϡ   c38f
    u"\xd0": u"\u00D0",    #    Р   Р   c390
    u"\xd1": u"\u00D1",    #    Ѡ   Ѡ   c391
    u"\xd2": u"\u00D2",    #    Ҡ   Ҡ   c392
    u"\xd3": u"\u00D3",    #    Ӡ   Ӡ   c393
    u"\xd4": u"\u00D4",    #    Ԡ   Ԡ   c394
    u"\xd5": u"\u00D5",    #    ՠ   ՠ   c395
    u"\xd6": u"\u00D6",    #    ֠   ֠   c396
    u"\xd7": u"\u00D7",    #    נ   נ   c397
    u"\xd8": u"\u00D8",    #    ؠ   ؠ   c398
    u"\xd9": u"\u00D9",    #    ٠   ٠   c399
    u"\xda": u"\u00DA",    #    ڠ   ڠ   c39a
    u"\xdb": u"\u00DB",    #    ۠   ۠   c39b
    u"\xdc": u"\u00DC",    #    ܠ   ܠ   c39c
    u"\xdd": u"\u00DD",    #    ݠ   ݠ   c39d
    u"\xde": u"\u00DE",    #    ޠ   ޠ   c39e
    u"\xdf": u"\u00DF",    #    ߠ   ߠ   c39f
    u"\xe0": u"\u00E0",    #    ࠠ  ࠠ  c3a0
    u"\xe1": u"\u00E1",    #    ᠠ  ᠠ  c3a1
    u"\xe2": u"\u00E2",    #    ⠠  ⠠  c3a2
    u"\xe3": u"\u00E3",    #    㠠  㠠  c3a3
    u"\xe4": u"\u00E4",    #    䠠  䠠  c3a4
    u"\xe5": u"\u00E5",    #    堠  堠  c3a5
    u"\xe6": u"\u00E6",    #    栠  栠  c3a6
    u"\xe7": u"\u00E7",    #    砠  砠  c3a7
    u"\xe8": u"\u00E8",    #    蠠  蠠  c3a8
    u"\xe9": u"\u00E9",    #    頠  頠  c3a9
    u"\xea": u"\u00EA",    #    ꠠ  ꠠ  c3aa
    u"\xeb": u"\u00EB",    #    렠  렠  c3ab
    u"\xec": u"\u00EC",    #    젠  젠  c3ac
    u"\xed": u"\u00ED",    #    ��  ��  c3ad
    u"\xee": u"\u00EE",    #        c3ae
    u"\xef": u"\u00EF",    #        c3af
    u"\xf0": u"\u00F0",    #    𠠠 𠠠 c3b0
    u"\xf1": u"\u00F1",    #    񠠠 񠠠 c3b1
    u"\xf2": u"\u00F2",    #    򠠠 򠠠 c3b2
    u"\xf3": u"\u00F3",    #    󠠠 󠠠 c3b3
    u"\xf4": u"\u00F4",    #    ���� ���� c3b4
    u"\xf5": u"\u00F5",    #    ���� ���� c3b5
    u"\xf6": u"\u00F6",    #    ���� ���� c3b6
    u"\xf7": u"\u00F7",    #    ���� ���� c3b7
    u"\xf8": u"\u00F8",    #    𠠠 𠠠 c3b8
    u"\xf9": u"\u00F9",    #    񠠠 񠠠 c3b9
    u"\xfa": u"\u00FA",    #    򠠠 򠠠 c3ba
    u"\xfb": u"\u00FB",    #    󠠠 󠠠 c3bb
    u"\xfc": u"\u00FC",    #    ���� ���� c3bc
    u"\xfd": u"\u00FD",    #    ���� ���� c3bd
    u"\xfe": u"\u00FE",    #    ���� ���� c3be
    u"\xff": u"\u00FF",    #    ���� ���� c3bf

}


def decode2(input_str):
     input_str = input_str.decode('latin-1')
     nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
     return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def decode(text):
    # map cp1252 gremlins to real unicode characters
    if re.search(u"[\x80-\xff]", text):
        def fixup(m):
            s = m.group(0)
            return cp1252.get(s, s)
        if isinstance(text, type("")):
            # make sure we have a unicode string
            text = unicode(text, "iso-8859-1")
        text = re.sub(u"[\x80-\xff]", fixup, text)
    return text
