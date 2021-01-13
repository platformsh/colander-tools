from colander_tools import bytes
import pytest
import sys

@pytest.mark.skipif(sys.version_info < (3, 0), reason="requires python 3")
def test_incompatible_types():
    """
    This test is only applicable to python3 code because strings and byte arrays are the
    same thing in python2.
    """
    with pytest.raises(TypeError):
        bytes.Base16Bytes.encoder(u"")
    with pytest.raises(TypeError):
        bytes.Base32Bytes.encoder(u"")
    with pytest.raises(TypeError):
        bytes.Base64Bytes.encoder(u"")
    with pytest.raises(TypeError):
        bytes.URLSafeBase64Bytes.encoder(u"")

def test_Base16Bytes():
    assert(bytes.Base16Bytes.encoder(b"") == u"")
    assert(bytes.Base16Bytes.encoder(b"iamsometext") == u"69616D736F6D6574657874")
    assert(bytes.Base16Bytes.decoder(u"69616D736F6D6574657874") == b"iamsometext")
    assert(bytes.Base16Bytes.decoder(b"69616D736F6D6574657874") == b"iamsometext")

def test_Base32Bytes():
    assert(bytes.Base32Bytes.encoder(b"") == u"")
    assert(bytes.Base32Bytes.encoder(b"iamsometext") == u"NFQW243PNVSXIZLYOQ======")
    assert(bytes.Base32Bytes.decoder(u"NFQW243PNVSXIZLYOQ======") == b"iamsometext")
    assert(bytes.Base32Bytes.decoder(b"NFQW243PNVSXIZLYOQ======") == b"iamsometext")

def test_Base64Bytes():
    assert(bytes.Base64Bytes.encoder(b"") == u"")
    assert(bytes.Base64Bytes.encoder(b"iamsometext") == u"aWFtc29tZXRleHQ=")
    assert(bytes.Base64Bytes.decoder(u"aWFtc29tZXRleHQ=") == b"iamsometext")
    assert(bytes.Base64Bytes.decoder(b"aWFtc29tZXRleHQ=") == b"iamsometext")

def test_URLSafeBase64Bytes():
    assert(bytes.URLSafeBase64Bytes.encoder(b"") == u"")
    assert(bytes.URLSafeBase64Bytes.encoder(b"url/?a=a&b=b") == u"dXJsLz9hPWEmYj1i")
    assert(bytes.Base64Bytes.decoder(u"dXJsLz9hPWEmYj1i") == b"url/?a=a&b=b")
    assert(bytes.Base64Bytes.decoder(b"dXJsLz9hPWEmYj1i") == b"url/?a=a&b=b")
    
