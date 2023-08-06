# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-04-22 17:27:47
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Image methods.
"""


from typing import List, Union, Optional
from io import BytesIO
from os.path import abspath as os_path_abspath
from qrcode import make as qrcode_make
from PIL.Image import open as pil_image_open

try:
    from pyzbar.pyzbar import decode as pyzbar_decode
except FileNotFoundError:
    pyzbar_decode = FileNotFoundError(
        "Reasons"
        "-------"
        "Missing component 'Visual C++ Redistributable Packages for Visual Studio 2013'."
        ""
        "Solutions"
        "---------"
        "First uninstall 'pyzbar', then install 'Visual C++ Redistributable Packages for Visual Studio 2013', then install 'pyzbar'."
    )


def encode_qrcode(text: str, path: Optional[str] = None) -> Union[str, bytes]:
    """
    Encoding text to QR code image.

    Parameters
    ----------
    text : Text.
    path : File generation path.
        * None : Not generate file, return image bytes data.
        * str : Generate file, return file path.

    Returns
    -------
    File path or image bytes data.
    """

    # Encode.
    image = qrcode_make(text)

    # Returns.

    ## Generate file and return file path.
    if path != None:
        image.save(path)
        result = os_path_abspath(path)

    ## Return image bytes data.
    else:
        bytesio = BytesIO()
        image.save(bytesio)
        result = bytesio.getvalue()

    return result


def decode_qrcode(image: Union[str, bytes]) -> List[str]:
    """
    Decoding QR code or bar code image.

    Parameters
    ----------
    image : Image bytes data or image file path.

    Returns
    -------
    QR code or bar code text list.
    """

    # Check.
    if pyzbar_decode.__class__ == FileNotFoundError:
        raise pyzbar_decode

    # Handle parameters.
    if image.__class__ == bytes:
        image = BytesIO(image)

    # Decode.
    image = pil_image_open(image)
    qrcodes_data = pyzbar_decode(image)

    # Convert.
    texts = [
        data.data.decode()
        for data in qrcodes_data
    ]

    return texts