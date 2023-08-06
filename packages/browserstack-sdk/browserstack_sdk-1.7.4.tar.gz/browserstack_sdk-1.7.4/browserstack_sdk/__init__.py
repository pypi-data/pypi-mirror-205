# coding: UTF-8
import sys
bstack1l_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstack111_opy_ = 7
def bstackl_opy_ (bstack1ll1_opy_):
    global bstack11l_opy_
    stringNr = ord (bstack1ll1_opy_ [-1])
    bstack1lll_opy_ = bstack1ll1_opy_ [:-1]
    bstack1l1l_opy_ = stringNr % len (bstack1lll_opy_)
    bstack1_opy_ = bstack1lll_opy_ [:bstack1l1l_opy_] + bstack1lll_opy_ [bstack1l1l_opy_:]
    if bstack1l_opy_:
        bstack1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack1l1_opy_ + stringNr) % bstack111_opy_) for bstack1l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack1ll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack1l1_opy_ + stringNr) % bstack111_opy_) for bstack1l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack1ll_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack1l11ll1ll_opy_ = {
	bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧࠁ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪࠂ"),
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪࠃ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫࠄ"),
  bstackl_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࠅ"): bstackl_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࠆ"),
  bstackl_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫࠇ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬࠈ"),
  bstackl_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࠉ"): bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨࠊ"),
  bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࠋ"): bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨࠌ"),
  bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࠍ"): bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩࠎ"),
  bstackl_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࠏ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫࠐ"),
  bstackl_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬࠑ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨࠒ"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠓ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠔ"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠕ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠖ"),
  bstackl_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࠗ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࠘"),
  bstackl_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࠙"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠚ"),
  bstackl_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠛ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠜ"),
  bstackl_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠝ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠞ"),
  bstackl_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠟ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠠ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࠡ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࠢ"),
  bstackl_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠣ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠤ"),
  bstackl_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠥ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠦ"),
  bstackl_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠧ"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠨ"),
  bstackl_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬࠩ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬࠪ"),
  bstackl_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠫ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠬ"),
  bstackl_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࠭"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࠮"),
  bstackl_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࠯"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࠰"),
  bstackl_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠱"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠲"),
  bstackl_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠳"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠴"),
  bstackl_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࠵"): bstackl_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ࠶"),
  bstackl_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ࠷"): bstackl_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ࠸"),
  bstackl_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࠹"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࠺"),
  bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠻"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠼"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠽"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠾"),
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࠿"): bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ࡀ"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡁ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡂ"),
  bstackl_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࡃ"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨࡄ"),
  bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡅ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡆ"),
  bstackl_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡇ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡈ"),
}
bstack1ll1l111_opy_ = [
  bstackl_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstackl_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstackl_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstackl_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack1l1l11111_opy_ = {
  bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩࡐ"): [bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩࡑ"), bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫࡒ")],
  bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࡓ"): bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧࡔ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࡕ"): bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩࡖ"),
  bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࡗ"): bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ࡘ"),
  bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࡙ࠫ"): bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࡚ࠬ"),
  bstackl_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰ࡛ࠫ"): bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭࡜"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ࡝"): bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ࡞"),
  bstackl_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ࡟"): bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ࡠ"),
  bstackl_opy_ (u"ࠪࡥࡵࡶࠧࡡ"): bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack1lll1111l_opy_ = {
  bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstackl_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstackl_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstackl_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstackl_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack1l1l1111l_opy_ = {
  bstackl_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstackl_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstackl_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstackl_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstackl_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstackl_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstackl_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstackl_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack1111111l_opy_ = [
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstackl_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstackl_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstackl_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstackl_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstackl_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstackl_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstackl_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstackl_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstackl_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack1l11llll_opy_ = [
  bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstackl_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstackl_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstackl_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
]
bstack11lll11l_opy_ = [
  bstackl_opy_ (u"ࠧࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬࢫ"),
  bstackl_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ"),
  bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ"),
  bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࢮ"),
  bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡒࡵ࡭ࡴࡸࡩࡵࡻࠪࢯ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࢰ"),
  bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡧࡧࠨࢱ"),
  bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࢲ"),
  bstackl_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢳ"),
  bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧࢴ"),
  bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫࢵ"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪࢶ"),
  bstackl_opy_ (u"ࠬࡵࡳࠨࢷ"),
  bstackl_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢸ"),
  bstackl_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭ࢹ"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪࢺ"),
  bstackl_opy_ (u"ࠩࡵࡩ࡬࡯࡯࡯ࠩࢻ"),
  bstackl_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬࢼ"),
  bstackl_opy_ (u"ࠫࡲࡧࡣࡩ࡫ࡱࡩࠬࢽ"),
  bstackl_opy_ (u"ࠬࡸࡥࡴࡱ࡯ࡹࡹ࡯࡯࡯ࠩࢾ"),
  bstackl_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࢿ"),
  bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡏࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫࣀ"),
  bstackl_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧࣁ"),
  bstackl_opy_ (u"ࠩࡱࡳࡕࡧࡧࡦࡎࡲࡥࡩ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ࣂ"),
  bstackl_opy_ (u"ࠪࡦ࡫ࡩࡡࡤࡪࡨࠫࣃ"),
  bstackl_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪࣄ"),
  bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩࣅ"),
  bstackl_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧࣆ"),
  bstackl_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫࣇ"),
  bstackl_opy_ (u"ࠨࡰࡲࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠬࣈ"),
  bstackl_opy_ (u"ࠩࡦ࡬ࡪࡩ࡫ࡖࡔࡏࠫࣉ"),
  bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊"),
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡇࡴࡵ࡫ࡪࡧࡶࠫ࣋"),
  bstackl_opy_ (u"ࠬࡩࡡࡱࡶࡸࡶࡪࡉࡲࡢࡵ࡫ࠫ࣌"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ࣍"),
  bstackl_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ࣎"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡛࡫ࡲࡴ࡫ࡲࡲ࣏ࠬ"),
  bstackl_opy_ (u"ࠩࡱࡳࡇࡲࡡ࡯࡭ࡓࡳࡱࡲࡩ࡯ࡩ࣐ࠪ"),
  bstackl_opy_ (u"ࠪࡱࡦࡹ࡫ࡔࡧࡱࡨࡐ࡫ࡹࡴ࣑ࠩ"),
  bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡐࡴ࡭ࡳࠨ࣒"),
  bstackl_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡎࡪ࣓ࠧ"),
  bstackl_opy_ (u"࠭ࡤࡦࡦ࡬ࡧࡦࡺࡥࡥࡆࡨࡺ࡮ࡩࡥࠨࣔ"),
  bstackl_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡐࡢࡴࡤࡱࡸ࠭ࣕ"),
  bstackl_opy_ (u"ࠨࡲ࡫ࡳࡳ࡫ࡎࡶ࡯ࡥࡩࡷ࠭ࣖ"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࣗ"),
  bstackl_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡐࡲࡷ࡭ࡴࡴࡳࠨࣘ"),
  bstackl_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩࣙ"),
  bstackl_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬࣚ"),
  bstackl_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪࣛ"),
  bstackl_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡂࡪࡱࡰࡩࡹࡸࡩࡤࠩࣜ"),
  bstackl_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࡖ࠳ࠩࣝ"),
  bstackl_opy_ (u"ࠩࡰ࡭ࡩ࡙ࡥࡴࡵ࡬ࡳࡳࡏ࡮ࡴࡶࡤࡰࡱࡇࡰࡱࡵࠪࣞ"),
  bstackl_opy_ (u"ࠪࡩࡸࡶࡲࡦࡵࡶࡳࡘ࡫ࡲࡷࡧࡵࠫࣟ"),
  bstackl_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪ࣠"),
  bstackl_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡃࡥࡲࠪ࣡"),
  bstackl_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭࣢"),
  bstackl_opy_ (u"ࠧࡴࡻࡱࡧ࡙࡯࡭ࡦ࡙࡬ࡸ࡭ࡔࡔࡑࣣࠩ"),
  bstackl_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ࣤ"),
  bstackl_opy_ (u"ࠩࡪࡴࡸࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstackl_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡔࡷࡵࡦࡪ࡮ࡨࣦࠫ"),
  bstackl_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫࣧ"),
  bstackl_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡇ࡭ࡧ࡮ࡨࡧࡍࡥࡷ࠭ࣨ"),
  bstackl_opy_ (u"࠭ࡸ࡮ࡵࡍࡥࡷࣩ࠭"),
  bstackl_opy_ (u"ࠧࡹ࡯ࡻࡎࡦࡸࠧ࣪"),
  bstackl_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧ࣫"),
  bstackl_opy_ (u"ࠩࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩ࣬"),
  bstackl_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷ࣭ࠫ"),
  bstackl_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹ࣮ࠧ"),
  bstackl_opy_ (u"ࠬࡧࡰࡱࡘࡨࡶࡸ࡯࡯࡯࣯ࠩ"),
  bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࣰࠬ"),
  bstackl_opy_ (u"ࠧࡳࡧࡶ࡭࡬ࡴࡁࡱࡲࣱࠪ"),
  bstackl_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࡷࣲࠬ"),
  bstackl_opy_ (u"ࠩࡦࡥࡳࡧࡲࡺࠩࣳ"),
  bstackl_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫࣴ"),
  bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫࣵ"),
  bstackl_opy_ (u"ࠬ࡯ࡥࠨࣶ"),
  bstackl_opy_ (u"࠭ࡥࡥࡩࡨࠫࣷ"),
  bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧࣸ"),
  bstackl_opy_ (u"ࠨࡳࡸࡩࡺ࡫ࣹࠧ"),
  bstackl_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࣺࠫ"),
  bstackl_opy_ (u"ࠪࡥࡵࡶࡓࡵࡱࡵࡩࡈࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠫࣻ"),
  bstackl_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡇࡦࡳࡥࡳࡣࡌࡱࡦ࡭ࡥࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪࣼ"),
  bstackl_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡈࡼࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨࣽ"),
  bstackl_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡍࡳࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstackl_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࠫࣿ"),
  bstackl_opy_ (u"ࠨࡴࡨࡷࡪࡸࡶࡦࡆࡨࡺ࡮ࡩࡥࠨऀ"),
  bstackl_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩँ"),
  bstackl_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬं"),
  bstackl_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡦࡹࡳࡤࡱࡧࡩࠬः"),
  bstackl_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡎࡵࡳࡅࡧࡹ࡭ࡨ࡫ࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨऄ"),
  bstackl_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡵࡥ࡫ࡲࡍࡳࡰࡥࡤࡶ࡬ࡳࡳ࠭अ"),
  bstackl_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡱࡲ࡯ࡩࡕࡧࡹࠨआ"),
  bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩइ"),
  bstackl_opy_ (u"ࠩࡺࡨ࡮ࡵࡓࡦࡴࡹ࡭ࡨ࡫ࠧई"),
  bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬउ"),
  bstackl_opy_ (u"ࠫࡵࡸࡥࡷࡧࡱࡸࡈࡸ࡯ࡴࡵࡖ࡭ࡹ࡫ࡔࡳࡣࡦ࡯࡮ࡴࡧࠨऊ"),
  bstackl_opy_ (u"ࠬ࡮ࡩࡨࡪࡆࡳࡳࡺࡲࡢࡵࡷࠫऋ"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡖࡲࡦࡨࡨࡶࡪࡴࡣࡦࡵࠪऌ"),
  bstackl_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪऍ"),
  bstackl_opy_ (u"ࠨࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬऎ"),
  bstackl_opy_ (u"ࠩࡵࡩࡲࡵࡶࡦࡋࡒࡗࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࡎࡲࡧࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧए"),
  bstackl_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬऐ"),
  bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऑ"),
  bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧऒ"),
  bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬओ"),
  bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩऔ"),
  bstackl_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫक"),
  bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨख"),
  bstackl_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬग"),
  bstackl_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧघ")
]
bstack1ll1ll1ll_opy_ = {
  bstackl_opy_ (u"ࠬࡼࠧङ"): bstackl_opy_ (u"࠭ࡶࠨच"),
  bstackl_opy_ (u"ࠧࡧࠩछ"): bstackl_opy_ (u"ࠨࡨࠪज"),
  bstackl_opy_ (u"ࠩࡩࡳࡷࡩࡥࠨझ"): bstackl_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"),
  bstackl_opy_ (u"ࠫࡴࡴ࡬ࡺࡣࡸࡸࡴࡳࡡࡵࡧࠪट"): bstackl_opy_ (u"ࠬࡵ࡮࡭ࡻࡄࡹࡹࡵ࡭ࡢࡶࡨࠫठ"),
  bstackl_opy_ (u"࠭ࡦࡰࡴࡦࡩࡱࡵࡣࡢ࡮ࠪड"): bstackl_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"),
  bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫण"): bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬत"),
  bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭थ"): bstackl_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧद"),
  bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨध"): bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩन"),
  bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪऩ"): bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫप"),
  bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾ࡮࡯ࡴࡶࠪफ"): bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡈࡰࡵࡷࠫब"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡱࡵࡸࠬभ"): bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭म"),
  bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧय"): bstackl_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩर"),
  bstackl_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪऱ"): bstackl_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫल"),
  bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫळ"): bstackl_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ऴ"),
  bstackl_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧव"): bstackl_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨश"),
  bstackl_opy_ (u"ࠧࡣ࡫ࡱࡥࡷࡿࡰࡢࡶ࡫ࠫष"): bstackl_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"),
  bstackl_opy_ (u"ࠩࡳࡥࡨ࡬ࡩ࡭ࡧࠪह"): bstackl_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ऺ"),
  bstackl_opy_ (u"ࠫࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ऻ"): bstackl_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨ़"),
  bstackl_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"): bstackl_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"),
  bstackl_opy_ (u"ࠨ࡮ࡲ࡫࡫࡯࡬ࡦࠩि"): bstackl_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"),
  bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬु"): bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"),
}
bstack1l1l1llll_opy_ = bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ृ")
bstack111lllll_opy_ = bstackl_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠩॄ")
bstack1lll111l_opy_ = {
  bstackl_opy_ (u"ࠧࡤࡴ࡬ࡸ࡮ࡩࡡ࡭ࠩॅ"): 50,
  bstackl_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧॆ"): 40,
  bstackl_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪे"): 30,
  bstackl_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨै"): 20,
  bstackl_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪॉ"): 10
}
DEFAULT_LOG_LEVEL = bstack1lll111l_opy_[bstackl_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ")]
bstack11llll1_opy_ = bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬो")
bstack1111ll11_opy_ = bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬौ")
bstack11lll_opy_ = bstackl_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack1lll11111_opy_ = bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨॎ")
bstack1lll11l_opy_ = [bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫॏ"), bstackl_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫॐ")]
bstack1111l1l_opy_ = [bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ॑"), bstackl_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ॒")]
bstack1ll11111l_opy_ = [
  bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡒࡦࡳࡥࠨ॓"),
  bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ॔"),
  bstackl_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ॕ"),
  bstackl_opy_ (u"ࠪࡲࡪࡽࡃࡰ࡯ࡰࡥࡳࡪࡔࡪ࡯ࡨࡳࡺࡺࠧॖ"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࠨॗ"),
  bstackl_opy_ (u"ࠬࡻࡤࡪࡦࠪक़"),
  bstackl_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨख़"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࠧग़"),
  bstackl_opy_ (u"ࠨࡱࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ज़"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࠧड़"),
  bstackl_opy_ (u"ࠪࡲࡴࡘࡥࡴࡧࡷࠫढ़"), bstackl_opy_ (u"ࠫ࡫ࡻ࡬࡭ࡔࡨࡷࡪࡺࠧफ़"),
  bstackl_opy_ (u"ࠬࡩ࡬ࡦࡣࡵࡗࡾࡹࡴࡦ࡯ࡉ࡭ࡱ࡫ࡳࠨय़"),
  bstackl_opy_ (u"࠭ࡥࡷࡧࡱࡸ࡙࡯࡭ࡪࡰࡪࡷࠬॠ"),
  bstackl_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࡐࡴ࡭ࡧࡪࡰࡪࠫॡ"),
  bstackl_opy_ (u"ࠨࡱࡷ࡬ࡪࡸࡁࡱࡲࡶࠫॢ"),
  bstackl_opy_ (u"ࠩࡳࡶ࡮ࡴࡴࡑࡣࡪࡩࡘࡵࡵࡳࡥࡨࡓࡳࡌࡩ࡯ࡦࡉࡥ࡮ࡲࡵࡳࡧࠪॣ"),
  bstackl_opy_ (u"ࠪࡥࡵࡶࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨ।"), bstackl_opy_ (u"ࠫࡦࡶࡰࡑࡣࡦ࡯ࡦ࡭ࡥࠨ॥"), bstackl_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧ०"), bstackl_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡐࡢࡥ࡮ࡥ࡬࡫ࠧ१"), bstackl_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡅࡷࡵࡥࡹ࡯࡯࡯ࠩ२"),
  bstackl_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭३"),
  bstackl_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡧࡶࡸࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭४"),
  bstackl_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࠬ५"), bstackl_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪࡋ࡮ࡥࡋࡱࡸࡪࡴࡴࠨ६"),
  bstackl_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡊࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪ७"),
  bstackl_opy_ (u"࠭ࡡࡥࡤࡓࡳࡷࡺࠧ८"),
  bstackl_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡓࡰࡥ࡮ࡩࡹ࠭९"),
  bstackl_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡖ࡬ࡱࡪࡵࡵࡵࠩ॰"),
  bstackl_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡓࡥࡹ࡮ࠧॱ"),
  bstackl_opy_ (u"ࠪࡥࡻࡪࠧॲ"), bstackl_opy_ (u"ࠫࡦࡼࡤࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧॳ"), bstackl_opy_ (u"ࠬࡧࡶࡥࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧॴ"), bstackl_opy_ (u"࠭ࡡࡷࡦࡄࡶ࡬ࡹࠧॵ"),
  bstackl_opy_ (u"ࠧࡶࡵࡨࡏࡪࡿࡳࡵࡱࡵࡩࠬॶ"), bstackl_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡹ࡮ࠧॷ"), bstackl_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡹࡳࡸࡱࡵࡨࠬॸ"),
  bstackl_opy_ (u"ࠪ࡯ࡪࡿࡁ࡭࡫ࡤࡷࠬॹ"), bstackl_opy_ (u"ࠫࡰ࡫ࡹࡑࡣࡶࡷࡼࡵࡲࡥࠩॺ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧॻ"), bstackl_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡆࡸࡧࡴࠩॼ"), bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࡆ࡬ࡶࠬॽ"), bstackl_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡃࡩࡴࡲࡱࡪࡓࡡࡱࡲ࡬ࡲ࡬ࡌࡩ࡭ࡧࠪॾ"), bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡖࡵࡨࡗࡾࡹࡴࡦ࡯ࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭ॿ"),
  bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹ࠭ঀ"), bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࡳࠨঁ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡈ࡮ࡹࡡࡣ࡮ࡨࡆࡺ࡯࡬ࡥࡅ࡫ࡩࡨࡱࠧং"),
  bstackl_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࡘ࡮ࡳࡥࡰࡷࡷࠫঃ"),
  bstackl_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡁࡤࡶ࡬ࡳࡳ࠭঄"), bstackl_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡄࡣࡷࡩ࡬ࡵࡲࡺࠩঅ"), bstackl_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡈ࡯ࡥ࡬ࡹࠧআ"), bstackl_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡤࡰࡎࡴࡴࡦࡰࡷࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ই"),
  bstackl_opy_ (u"ࠫࡩࡵ࡮ࡵࡕࡷࡳࡵࡇࡰࡱࡑࡱࡖࡪࡹࡥࡵࠩঈ"),
  bstackl_opy_ (u"ࠬࡻ࡮ࡪࡥࡲࡨࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧউ"), bstackl_opy_ (u"࠭ࡲࡦࡵࡨࡸࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭ঊ"),
  bstackl_opy_ (u"ࠧ࡯ࡱࡖ࡭࡬ࡴࠧঋ"),
  bstackl_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡖࡰ࡬ࡱࡵࡵࡲࡵࡣࡱࡸ࡛࡯ࡥࡸࡵࠪঌ"),
  bstackl_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲࡩࡸ࡯ࡪࡦ࡚ࡥࡹࡩࡨࡦࡴࡶࠫ঍"),
  bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ঎"),
  bstackl_opy_ (u"ࠫࡷ࡫ࡣࡳࡧࡤࡸࡪࡉࡨࡳࡱࡰࡩࡉࡸࡩࡷࡧࡵࡗࡪࡹࡳࡪࡱࡱࡷࠬএ"),
  bstackl_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫঐ"),
  bstackl_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡓࡥࡹ࡮ࠧ঑"),
  bstackl_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡔࡲࡨࡩࡩ࠭঒"),
  bstackl_opy_ (u"ࠨࡩࡳࡷࡊࡴࡡࡣ࡮ࡨࡨࠬও"),
  bstackl_opy_ (u"ࠩ࡬ࡷࡍ࡫ࡡࡥ࡮ࡨࡷࡸ࠭ঔ"),
  bstackl_opy_ (u"ࠪࡥࡩࡨࡅࡹࡧࡦࡘ࡮ࡳࡥࡰࡷࡷࠫক"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࡗࡨࡸࡩࡱࡶࠪখ"),
  bstackl_opy_ (u"ࠬࡹ࡫ࡪࡲࡇࡩࡻ࡯ࡣࡦࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩগ"),
  bstackl_opy_ (u"࠭ࡡࡶࡶࡲࡋࡷࡧ࡮ࡵࡒࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠭ঘ"),
  bstackl_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡏࡣࡷࡹࡷࡧ࡬ࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬঙ"),
  bstackl_opy_ (u"ࠨࡵࡼࡷࡹ࡫࡭ࡑࡱࡵࡸࠬচ"),
  bstackl_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡧࡦࡍࡵࡳࡵࠩছ"),
  bstackl_opy_ (u"ࠪࡷࡰ࡯ࡰࡖࡰ࡯ࡳࡨࡱࠧজ"), bstackl_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡘࡾࡶࡥࠨঝ"), bstackl_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯ࡐ࡫ࡹࠨঞ"),
  bstackl_opy_ (u"࠭ࡡࡶࡶࡲࡐࡦࡻ࡮ࡤࡪࠪট"),
  bstackl_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡤࡣࡷࡇࡦࡶࡴࡶࡴࡨࠫঠ"),
  bstackl_opy_ (u"ࠨࡷࡱ࡭ࡳࡹࡴࡢ࡮࡯ࡓࡹ࡮ࡥࡳࡒࡤࡧࡰࡧࡧࡦࡵࠪড"),
  bstackl_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧ࡚࡭ࡳࡪ࡯ࡸࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࠫঢ"),
  bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡲࡳࡱࡹࡖࡦࡴࡶ࡭ࡴࡴࠧণ"),
  bstackl_opy_ (u"ࠫࡪࡴࡦࡰࡴࡦࡩࡆࡶࡰࡊࡰࡶࡸࡦࡲ࡬ࠨত"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡴࡷࡵࡩ࡜࡫ࡢࡷ࡫ࡨࡻࡸࡎࡡࡷࡧࡓࡥ࡬࡫ࡳࠨথ"), bstackl_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࡄࡦࡸࡷࡳࡴࡲࡳࡑࡱࡵࡸࠬদ"), bstackl_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡄࡦࡶࡤ࡭ࡱࡹࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠪধ"),
  bstackl_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡲࡳࡷࡈࡧࡣࡩࡧࡏ࡭ࡲ࡯ࡴࠨন"),
  bstackl_opy_ (u"ࠩࡦࡥࡱ࡫࡮ࡥࡣࡵࡊࡴࡸ࡭ࡢࡶࠪ঩"),
  bstackl_opy_ (u"ࠪࡦࡺࡴࡤ࡭ࡧࡌࡨࠬপ"),
  bstackl_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫফ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡆࡰࡤࡦࡱ࡫ࡤࠨব"), bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡃࡸࡸ࡭ࡵࡲࡪࡼࡨࡨࠬভ"),
  bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡆࡩࡣࡦࡲࡷࡅࡱ࡫ࡲࡵࡵࠪম"), bstackl_opy_ (u"ࠨࡣࡸࡸࡴࡊࡩࡴ࡯࡬ࡷࡸࡇ࡬ࡦࡴࡷࡷࠬয"),
  bstackl_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡸࡒࡩࡣࠩর"),
  bstackl_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧ࡚ࡩࡧ࡚ࡡࡱࠩ঱"),
  bstackl_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡍࡳ࡯ࡴࡪࡣ࡯࡙ࡷࡲࠧল"), bstackl_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡆࡲ࡬ࡰࡹࡓࡳࡵࡻࡰࡴࠩ঳"), bstackl_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏࡧ࡯ࡱࡵࡩࡋࡸࡡࡶࡦ࡚ࡥࡷࡴࡩ࡯ࡩࠪ঴"), bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡧࡱࡐ࡮ࡴ࡫ࡴࡋࡱࡆࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࠧ঵"),
  bstackl_opy_ (u"ࠨ࡭ࡨࡩࡵࡑࡥࡺࡅ࡫ࡥ࡮ࡴࡳࠨশ"),
  bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡼࡤࡦࡱ࡫ࡓࡵࡴ࡬ࡲ࡬ࡹࡄࡪࡴࠪষ"),
  bstackl_opy_ (u"ࠪࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭স"),
  bstackl_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡎࡩࡾࡊࡥ࡭ࡣࡼࠫহ"),
  bstackl_opy_ (u"ࠬࡹࡨࡰࡹࡌࡓࡘࡒ࡯ࡨࠩ঺"),
  bstackl_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡓࡵࡴࡤࡸࡪ࡭ࡹࠨ঻"),
  bstackl_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡒࡦࡵࡳࡳࡳࡹࡥࡕ࡫ࡰࡩࡴࡻࡴࠨ়"), bstackl_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸ࡜ࡧࡩࡵࡖ࡬ࡱࡪࡵࡵࡵࠩঽ"),
  bstackl_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࠬা"),
  bstackl_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡷࡾࡴࡣࡆࡺࡨࡧࡺࡺࡥࡇࡴࡲࡱࡍࡺࡴࡱࡵࠪি"),
  bstackl_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡈࡧࡰࡵࡷࡵࡩࠬী"),
  bstackl_opy_ (u"ࠬࡽࡥࡣ࡭࡬ࡸࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬু"),
  bstackl_opy_ (u"࠭ࡦࡶ࡮࡯ࡇࡴࡴࡴࡦࡺࡷࡐ࡮ࡹࡴࠨূ"),
  bstackl_opy_ (u"ࠧࡸࡣ࡬ࡸࡋࡵࡲࡂࡲࡳࡗࡨࡸࡩࡱࡶࠪৃ"),
  bstackl_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡅࡲࡲࡳ࡫ࡣࡵࡔࡨࡸࡷ࡯ࡥࡴࠩৄ"),
  bstackl_opy_ (u"ࠩࡤࡴࡵࡔࡡ࡮ࡧࠪ৅"),
  bstackl_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡗࡑࡉࡥࡳࡶࠪ৆"),
  bstackl_opy_ (u"ࠫࡹࡧࡰࡘ࡫ࡷ࡬ࡘ࡮࡯ࡳࡶࡓࡶࡪࡹࡳࡅࡷࡵࡥࡹ࡯࡯࡯ࠩে"),
  bstackl_opy_ (u"ࠬࡹࡣࡢ࡮ࡨࡊࡦࡩࡴࡰࡴࠪৈ"),
  bstackl_opy_ (u"࠭ࡷࡥࡣࡏࡳࡨࡧ࡬ࡑࡱࡵࡸࠬ৉"),
  bstackl_opy_ (u"ࠧࡴࡪࡲࡻ࡝ࡩ࡯ࡥࡧࡏࡳ࡬࠭৊"),
  bstackl_opy_ (u"ࠨ࡫ࡲࡷࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡵࡴࡧࠪো"),
  bstackl_opy_ (u"ࠩࡻࡧࡴࡪࡥࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠫৌ"),
  bstackl_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡳࡴࡹࡲࡶࡩ্࠭"),
  bstackl_opy_ (u"ࠫࡺࡹࡥࡑࡴࡨࡦࡺ࡯࡬ࡵ࡙ࡇࡅࠬৎ"),
  bstackl_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹ࡝ࡄࡂࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠭৏"),
  bstackl_opy_ (u"࠭ࡷࡦࡤࡇࡶ࡮ࡼࡥࡳࡃࡪࡩࡳࡺࡕࡳ࡮ࠪ৐"),
  bstackl_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡸ࡭࠭৑"),
  bstackl_opy_ (u"ࠨࡷࡶࡩࡓ࡫ࡷࡘࡆࡄࠫ৒"),
  bstackl_opy_ (u"ࠩࡺࡨࡦࡒࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬ৓"), bstackl_opy_ (u"ࠪࡻࡩࡧࡃࡰࡰࡱࡩࡨࡺࡩࡰࡰࡗ࡭ࡲ࡫࡯ࡶࡶࠪ৔"),
  bstackl_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡒࡶ࡬ࡏࡤࠨ৕"), bstackl_opy_ (u"ࠬࡾࡣࡰࡦࡨࡗ࡮࡭࡮ࡪࡰࡪࡍࡩ࠭৖"),
  bstackl_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪࡗࡅࡃࡅࡹࡳࡪ࡬ࡦࡋࡧࠫৗ"),
  bstackl_opy_ (u"ࠧࡳࡧࡶࡩࡹࡕ࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡶࡹࡕ࡮࡭ࡻࠪ৘"),
  bstackl_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࡵࠪ৙"),
  bstackl_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴ࡬ࡩࡸ࠭৚"), bstackl_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵࡽࡎࡴࡴࡦࡴࡹࡥࡱ࠭৛"),
  bstackl_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࡍࡧࡲࡥࡹࡤࡶࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧড়"),
  bstackl_opy_ (u"ࠬࡳࡡࡹࡖࡼࡴ࡮ࡴࡧࡇࡴࡨࡵࡺ࡫࡮ࡤࡻࠪঢ়"),
  bstackl_opy_ (u"࠭ࡳࡪ࡯ࡳࡰࡪࡏࡳࡗ࡫ࡶ࡭ࡧࡲࡥࡄࡪࡨࡧࡰ࠭৞"),
  bstackl_opy_ (u"ࠧࡶࡵࡨࡇࡦࡸࡴࡩࡣࡪࡩࡘࡹ࡬ࠨয়"),
  bstackl_opy_ (u"ࠨࡵ࡫ࡳࡺࡲࡤࡖࡵࡨࡗ࡮ࡴࡧ࡭ࡧࡷࡳࡳ࡚ࡥࡴࡶࡐࡥࡳࡧࡧࡦࡴࠪৠ"),
  bstackl_opy_ (u"ࠩࡶࡸࡦࡸࡴࡊ࡙ࡇࡔࠬৡ"),
  bstackl_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡲࡹࡨ࡮ࡉࡥࡇࡱࡶࡴࡲ࡬ࠨৢ"),
  bstackl_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࡌ࡮ࡪࡤࡦࡰࡄࡴ࡮ࡖ࡯࡭࡫ࡦࡽࡊࡸࡲࡰࡴࠪৣ"),
  bstackl_opy_ (u"ࠬࡳ࡯ࡤ࡭ࡏࡳࡨࡧࡴࡪࡱࡱࡅࡵࡶࠧ৤"),
  bstackl_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌ࡯ࡳ࡯ࡤࡸࠬ৥"), bstackl_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡪ࡮ࡷࡩࡷ࡙ࡰࡦࡥࡶࠫ০"),
  bstackl_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡄࡦ࡮ࡤࡽࡆࡪࡢࠨ১")
]
bstack1ll11111_opy_ = bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡷࡳࡰࡴࡧࡤࠨ২")
bstack1ll11ll1l_opy_ = [bstackl_opy_ (u"ࠪ࠲ࡦࡶ࡫ࠨ৩"), bstackl_opy_ (u"ࠫ࠳ࡧࡡࡣࠩ৪"), bstackl_opy_ (u"ࠬ࠴ࡩࡱࡣࠪ৫")]
bstack1lllll11l_opy_ = [bstackl_opy_ (u"࠭ࡩࡥࠩ৬"), bstackl_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ৭"), bstackl_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ৮"), bstackl_opy_ (u"ࠩࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤࠨ৯")]
bstack11l111l_opy_ = {
  bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪৰ"): bstackl_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩৱ"),
  bstackl_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৲"): bstackl_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstackl_opy_ (u"ࠧࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬ৴"): bstackl_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৵"),
  bstackl_opy_ (u"ࠩ࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ৶"): bstackl_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৷"),
  bstackl_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵࡺࡩࡰࡰࡶࠫ৸"): bstackl_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭৹")
}
bstack1lll1ll1l_opy_ = [
  bstackl_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৺"),
  bstackl_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ৻"),
  bstackl_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩৼ"),
  bstackl_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ৽"),
  bstackl_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫ৾"),
]
bstack1l1l1ll_opy_ = bstack1l11llll_opy_ + bstack11lll11l_opy_ + bstack1ll11111l_opy_
bstack111l11l_opy_ = [
  bstackl_opy_ (u"ࠫࡣࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴࠥࠩ৿"),
  bstackl_opy_ (u"ࠬࡤࡢࡴ࠯࡯ࡳࡨࡧ࡬࠯ࡥࡲࡱࠩ࠭਀"),
  bstackl_opy_ (u"࠭࡞࠲࠴࠺࠲ࠬਁ"),
  bstackl_opy_ (u"ࠧ࡟࠳࠳࠲ࠬਂ"),
  bstackl_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠱࡜࠸࠰࠽ࡢ࠴ࠧਃ"),
  bstackl_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠳࡝࠳࠱࠾ࡣ࠮ࠨ਄"),
  bstackl_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠵࡞࠴࠲࠷࡝࠯ࠩਅ"),
  bstackl_opy_ (u"ࠫࡣ࠷࠹࠳࠰࠴࠺࠽࠴ࠧਆ")
]
bstack1llllll1_opy_ = bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾࠩਇ")
bstack1l1l11_opy_ = bstackl_opy_ (u"࠭ࡳࡥ࡭࠲ࡺ࠶࠵ࡥࡷࡧࡱࡸࠬਈ")
bstack11l11ll_opy_ = [ bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩਉ") ]
bstack1ll1l11_opy_ = [ bstackl_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧਊ") ]
bstack1ll11ll1_opy_ = [ bstackl_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ਋") ]
bstack1l111l11_opy_ = bstackl_opy_ (u"ࠪࡗࡉࡑࡓࡦࡶࡸࡴࠬ਌")
bstack111l1l11_opy_ = bstackl_opy_ (u"ࠫࡘࡊࡋࡕࡧࡶࡸࡆࡺࡴࡦ࡯ࡳࡸࡪࡪࠧ਍")
bstack11111ll_opy_ = bstackl_opy_ (u"࡙ࠬࡄࡌࡖࡨࡷࡹ࡙ࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠩ਎")
bstack1l1lll11l_opy_ = bstackl_opy_ (u"࠭࠴࠯࠲࠱࠴ࠬਏ")
bstack1ll1l11l_opy_ = bstackl_opy_ (u"ࠧࡔࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠽ࠤࢀࢃࠧਐ")
bstack1l1llll1l_opy_ = bstackl_opy_ (u"ࠨࡅࡲࡱࡵࡲࡥࡵࡧࡧࠤࡸ࡫ࡴࡶࡲࠤࠫ਑")
bstack111ll1l_opy_ = bstackl_opy_ (u"ࠩࡓࡥࡷࡹࡥࡥࠢࡦࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫ਒")
bstack1lll11l1l_opy_ = bstackl_opy_ (u"ࠪࡗࡦࡴࡩࡵ࡫ࡽࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨਓ")
bstack11ll1l_opy_ = bstackl_opy_ (u"࡚ࠫࡹࡩ࡯ࡩࠣ࡬ࡺࡨࠠࡶࡴ࡯࠾ࠥࢁࡽࠨਔ")
bstack111l1ll1_opy_ = bstackl_opy_ (u"࡙ࠬࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࡾࢁࠬਕ")
bstack1l1ll1lll_opy_ = bstackl_opy_ (u"࠭ࡒࡦࡥࡨ࡭ࡻ࡫ࡤࠡ࡫ࡱࡸࡪࡸࡲࡶࡲࡷ࠰ࠥ࡫ࡸࡪࡶ࡬ࡲ࡬࠭ਖ")
bstack1l1lll111_opy_ = bstackl_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬਗ")
bstack1llll11_opy_ = bstackl_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡤࡲࡩࠦࡰࡺࡶࡨࡷࡹ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡲࡤࡧࡰࡧࡧࡦࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࡥ࠭ਘ")
bstack1l1ll1_opy_ = bstackl_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵ࠮ࠣࡴࡦࡨ࡯ࡵࠢࡤࡲࡩࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࡭࡫ࡥࡶࡦࡸࡹࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡸࡴࠦࡲࡶࡰࠣࡶࡴࡨ࡯ࡵࠢࡷࡩࡸࡺࡳࠡ࡫ࡱࠤࡵࡧࡲࡢ࡮࡯ࡩࡱ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡲࡤࡦࡴࡺࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡵࡨࡰࡪࡴࡩࡶ࡯࡯࡭ࡧࡸࡡࡳࡻࡣࠫਙ")
bstack1ll11l1l_opy_ = bstackl_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡧ࡫ࡨࡢࡸࡨࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡦࡪ࡮ࡡࡷࡧࡣࠫਚ")
bstack111llll_opy_ = bstackl_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡧࡰࡱ࡫ࡸࡱ࠲ࡩ࡬ࡪࡧࡱࡸࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡆࡶࡰࡪࡷࡰ࠱ࡕࡿࡴࡩࡱࡱ࠱ࡈࡲࡩࡦࡰࡷࡤࠬਛ")
bstack1ll111l1_opy_ = bstackl_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡦࠧਜ")
bstack1ll1l1ll1_opy_ = bstackl_opy_ (u"࠭ࡈࡢࡰࡧࡰ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡰࡴࡹࡥࠨਝ")
bstack1l1l11l1_opy_ = bstackl_opy_ (u"ࠧࡂ࡮࡯ࠤࡩࡵ࡮ࡦࠣࠪਞ")
bstack1lll11ll_opy_ = bstackl_opy_ (u"ࠨࡅࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࠠࡢࡶࠣࡥࡳࡿࠠࡱࡣࡵࡩࡳࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡳ࡫ࠦࠢࡼࡿࠥ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡤ࡮ࡸࡨࡪࠦࡡࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠡࡨ࡬ࡰࡪࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡵࡧࡶࡸࡸ࠴ࠧਟ")
bstack11111l1l_opy_ = bstackl_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡵࡩࡩ࡫࡮ࡵ࡫ࡤࡰࡸࠦ࡮ࡰࡶࠣࡴࡷࡵࡶࡪࡦࡨࡨ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡸ࡭࡫࡭ࠡ࡫ࡱࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩࠥࡧࡳࠡࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦࠥࡧ࡮ࡥࠢࠥࡥࡨࡩࡥࡴࡵࡎࡩࡾࠨࠠࡰࡴࠣࡷࡪࡺࠠࡵࡪࡨࡱࠥࡧࡳࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴ࠼ࠣࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧࠦࡡ࡯ࡦࠣࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠢࠨਠ")
bstack11ll1l11_opy_ = bstackl_opy_ (u"ࠪࡑࡦࡲࡦࡰࡴࡰࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠧࢁࡽࠣࠩਡ")
bstack11l1111_opy_ = bstackl_opy_ (u"ࠫࡊࡴࡣࡰࡷࡱࡸࡪࡸࡥࡥࠢࡨࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࠤ࠲ࠦࡻࡾࠩਢ")
bstack1lll1lll1_opy_ = bstackl_opy_ (u"࡙ࠬࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰࠬਣ")
bstack1l11ll1_opy_ = bstackl_opy_ (u"࠭ࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱ࠭ਤ")
bstack11l111_opy_ = bstackl_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰࠥ࡯ࡳࠡࡰࡲࡻࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠧࠧਥ")
bstack1ll1lllll_opy_ = bstackl_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡸࡺࡡࡳࡶࠣࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡏࡳࡨࡧ࡬࠻ࠢࡾࢁࠬਦ")
bstack11l11l1l_opy_ = bstackl_opy_ (u"ࠩࡖࡸࡦࡸࡴࡪࡰࡪࠤࡱࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡻ࡮ࡺࡨࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࡿࢂ࠭ਧ")
bstack11l111ll_opy_ = bstackl_opy_ (u"࡙ࠪࡵࡪࡡࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠫਨ")
bstack1ll1lll_opy_ = bstackl_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠪ਩")
bstack1l1ll1ll1_opy_ = bstackl_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࠦࡡ࡯ࠢࡤࡴࡵࡸ࡯ࡱࡴ࡬ࡥࡹ࡫ࠠࡇ࡙ࠣࠬࡷࡵࡢࡰࡶ࠲ࡴࡦࡨ࡯ࡵࠫࠣ࡭ࡳࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠰ࠥࡹ࡫ࡪࡲࠣࡸ࡭࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡯ࡪࡿࠠࡪࡰࠣࡧࡴࡴࡦࡪࡩࠣ࡭࡫ࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡴ࡫ࡰࡴࡱ࡫ࠠࡱࡻࡷ࡬ࡴࡴࠠࡴࡥࡵ࡭ࡵࡺࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡣࡱࡽࠥࡌࡗ࠯ࠩਪ")
bstack1lll11lll_opy_ = bstackl_opy_ (u"࠭ࡓࡦࡶࡷ࡭ࡳ࡭ࠠࡩࡶࡷࡴࡕࡸ࡯ࡹࡻ࠲࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠠࡪࡵࠣࡲࡴࡺࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡳࡳࠦࡣࡶࡴࡵࡩࡳࡺ࡬ࡺࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥࡼࡥࡳࡵ࡬ࡳࡳࠦ࡯ࡧࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࠤ࠭ࢁࡽࠪ࠮ࠣࡴࡱ࡫ࡡࡴࡧࠣࡹࡵ࡭ࡲࡢࡦࡨࠤࡹࡵࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࡀࡀ࠸࠳࠶࠮࠱ࠢࡲࡶࠥࡸࡥࡧࡧࡵࠤࡹࡵࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡲࡧࡸ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡰࡪࡴࡩࡶ࡯࠲ࡶࡺࡴ࠭ࡵࡧࡶࡸࡸ࠳ࡢࡦࡪ࡬ࡲࡩ࠳ࡰࡳࡱࡻࡽࠨࡶࡹࡵࡪࡲࡲࠥ࡬࡯ࡳࠢࡤࠤࡼࡵࡲ࡬ࡣࡵࡳࡺࡴࡤ࠯ࠩਫ")
bstack1llll11l_opy_ = bstackl_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡽࡲࡲࠠࡧ࡫࡯ࡩ࠳࠴ࠧਬ")
bstack111ll1ll_opy_ = bstackl_opy_ (u"ࠨࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡨࡧࡱࡩࡷࡧࡴࡦࡦࠣࡸ࡭࡫ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠦ࠭ਭ")
bstack1llll1l11_opy_ = bstackl_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥ࠯ࠢࡾࢁࠬਮ")
bstack1llll1111_opy_ = bstackl_opy_ (u"ࠪࡉࡽࡶࡥࡤࡶࡨࡨࠥࡧࡴࠡ࡮ࡨࡥࡸࡺࠠ࠲ࠢ࡬ࡲࡵࡻࡴ࠭ࠢࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࠵࠭ਯ")
bstack1ll111l_opy_ = bstackl_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡨࡺࡸࡩ࡯ࡩࠣࡅࡵࡶࠠࡶࡲ࡯ࡳࡦࡪ࠮ࠡࡽࢀࠫਰ")
bstack1lll1ll11_opy_ = bstackl_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡰࡴࡧࡤࠡࡃࡳࡴ࠳ࠦࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࢁࡽ࠯ࠩ਱")
bstack1l1l1111_opy_ = bstackl_opy_ (u"࠭ࡋࡦࡻࡶࠤࡨࡧ࡮࡯ࡱࡷࠤࡨࡵ࠭ࡦࡺ࡬ࡷࡹࠦࡡࡴࠢࡤࡴࡵࠦࡶࡢ࡮ࡸࡩࡸ࠲ࠠࡶࡵࡨࠤࡦࡴࡹࠡࡱࡱࡩࠥࡶࡲࡰࡲࡨࡶࡹࡿࠠࡧࡴࡲࡱࠥࢁࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡵࡧࡴࡩ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡨࡻࡳࡵࡱࡰࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿ࡿ࠯ࠤࡴࡴ࡬ࡺࠢࠥࡴࡦࡺࡨࠣࠢࡤࡲࡩࠦࠢࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠥࠤࡨࡧ࡮ࠡࡥࡲ࠱ࡪࡾࡩࡴࡶࠣࡸࡴ࡭ࡥࡵࡪࡨࡶ࠳࠭ਲ")
bstack11l1ll_opy_ = bstackl_opy_ (u"ࠧ࡜ࡋࡱࡺࡦࡲࡩࡥࠢࡤࡴࡵࠦࡰࡳࡱࡳࡩࡷࡺࡹ࡞ࠢࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠢࡤࡶࡪࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠲ࠥࡌ࡯ࡳࠢࡰࡳࡷ࡫ࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡲ࡯ࡩࡦࡹࡥࠡࡸ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡲࡧࡸ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡱ࡫ࡸࡱ࠴ࡹࡥࡵ࠯ࡸࡴ࠲ࡺࡥࡴࡶࡶ࠳ࡸࡶࡥࡤ࡫ࡩࡽ࠲ࡧࡰࡱࠩਲ਼")
bstack1lllll1ll_opy_ = bstackl_opy_ (u"ࠨ࡝ࡌࡲࡻࡧ࡬ࡪࡦࠣࡥࡵࡶࠠࡱࡴࡲࡴࡪࡸࡴࡺ࡟ࠣࡗࡺࡶࡰࡰࡴࡷࡩࡩࠦࡶࡢ࡮ࡸࡩࡸࠦ࡯ࡧࠢࡤࡴࡵࠦࡡࡳࡧࠣࡳ࡫ࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠲ࠥࡌ࡯ࡳࠢࡰࡳࡷ࡫ࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡲ࡯ࡩࡦࡹࡥࠡࡸ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡲࡧࡸ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡱ࡫ࡸࡱ࠴ࡹࡥࡵ࠯ࡸࡴ࠲ࡺࡥࡴࡶࡶ࠳ࡸࡶࡥࡤ࡫ࡩࡽ࠲ࡧࡰࡱࠩ਴")
bstack1l111ll_opy_ = bstackl_opy_ (u"ࠩࡘࡷ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡥࡵࡶࠠࡪࡦࠣࡿࢂࠦࡦࡰࡴࠣ࡬ࡦࡹࡨࠡ࠼ࠣࡿࢂ࠴ࠧਵ")
bstack1lllll1l_opy_ = bstackl_opy_ (u"ࠪࡅࡵࡶࠠࡖࡲ࡯ࡳࡦࡪࡥࡥࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠢࡌࡈࠥࡀࠠࡼࡿࠪਸ਼")
bstack1l11l1ll_opy_ = bstackl_opy_ (u"࡚ࠫࡹࡩ࡯ࡩࠣࡅࡵࡶࠠ࠻ࠢࡾࢁ࠳࠭਷")
bstack1l111111_opy_ = bstackl_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡲࡶࠥࡼࡡ࡯࡫࡯ࡰࡦࠦࡰࡺࡶ࡫ࡳࡳࠦࡴࡦࡵࡷࡷ࠱ࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡸ࡫ࡷ࡬ࠥࡶࡡࡳࡣ࡯ࡰࡪࡲࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠤࡂࠦ࠱ࠨਸ")
bstack111l1l1_opy_ = bstackl_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࠿ࠦࡻࡾࠩਹ")
bstack111l11ll_opy_ = bstackl_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡧࡱࡵࡳࡦࠢࡥࡶࡴࡽࡳࡦࡴ࠽ࠤࢀࢃࠧ਺")
bstack1ll1l1lll_opy_ = bstackl_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤ࡬࡫ࡴࠡࡴࡨࡥࡸࡵ࡮ࠡࡨࡲࡶࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫࠮ࠡࡽࢀࠫ਻")
bstack1ll1l1l1_opy_ = bstackl_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡࡣࡳ࡭ࠥࡩࡡ࡭࡮࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࢀࢃ਼ࠧ")
bstack1ll11l111_opy_ = bstackl_opy_ (u"࡙ࠪࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡩࡱࡺࠤࡧࡻࡩ࡭ࡦ࡙ࠣࡗࡒࠬࠡࡣࡶࠤࡧࡻࡩ࡭ࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠠࡪࡵࠣࡲࡴࡺࠠࡶࡵࡨࡨ࠳࠭਽")
bstack11ll111_opy_ = bstackl_opy_ (u"ࠫࡘ࡫ࡲࡷࡧࡵࠤࡸ࡯ࡤࡦࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ࠭ࢁࡽࠪࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡥࡲ࡫ࠠࡢࡵࠣࡧࡱ࡯ࡥ࡯ࡶࠣࡷ࡮ࡪࡥࠡࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠬࢀࢃࠩࠨਾ")
bstack1llll111l_opy_ = bstackl_opy_ (u"ࠬ࡜ࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡲࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡩࡧࡳࡩࡤࡲࡥࡷࡪ࠺ࠡࡽࢀࠫਿ")
bstack1llll1l1_opy_ = bstackl_opy_ (u"࠭ࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡤࡧࡨ࡫ࡳࡴࠢࡤࠤࡵࡸࡩࡷࡣࡷࡩࠥࡪ࡯࡮ࡣ࡬ࡲ࠿ࠦࡻࡾࠢ࠱ࠤࡘ࡫ࡴࠡࡶ࡫ࡩࠥ࡬࡯࡭࡮ࡲࡻ࡮ࡴࡧࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡱࠤࡾࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧ࠽ࠤࡡࡴ࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰ࠤࡡࡴࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯࠾ࠥࡺࡲࡶࡧࠣࡠࡳ࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯ࠪੀ")
bstack1ll11ll11_opy_ = bstackl_opy_ (u"ࠧࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡪࡩࡹࡥ࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࡣࡪࡸࡲࡰࡴࠣ࠾ࠥࢁࡽࠨੁ")
bstack11lll1_opy_ = bstackl_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠࡣࡰࡴࡱ࡯ࡴࡶࡦࡨࡣࡪࡼࡥ࡯ࡶࠣࡪࡴࡸࠠࡔࡆࡎࡗࡪࡺࡵࡱࠢࡾࢁࠧੂ")
bstack1l1l111_opy_ = bstackl_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡࡤࡱࡵࡲࡩࡵࡷࡧࡩࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡵࡲࠡࡕࡇࡏ࡙࡫ࡳࡵࡃࡷࡸࡪࡳࡰࡵࡧࡧࠤࢀࢃࠢ੃")
bstack1ll1l1l1l_opy_ = bstackl_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥ࡯ࡦࡢࡥࡲࡶ࡬ࡪࡶࡸࡨࡪࡥࡥࡷࡧࡱࡸࠥ࡬࡯ࡳࠢࡖࡈࡐ࡚ࡥࡴࡶࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠦࡻࡾࠤ੄")
bstack1l11lll_opy_ = bstackl_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡴࡨࡣࡷ࡫ࡱࡶࡧࡶࡸࠥࢁࡽࠣ੅")
bstack11l1llll_opy_ = bstackl_opy_ (u"ࠧࡖࡏࡔࡖࠣࡉࡻ࡫࡮ࡵࠢࡾࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠ࠻ࠢࡾࢁࠧ੆")
bstack1l1ll1l_opy_ = bstackl_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࠥࡶࡲࡰࡺࡼࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪੇ")
bstack1ll11l_opy_ = bstackl_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧੈ")
bstack1ll1l11ll_opy_ = bstackl_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠧ੉")
from ._version import __version__
bstack1l1l1ll1l_opy_ = None
CONFIG = {}
bstack1l1llll1_opy_ = {}
bstack111lll_opy_ = {}
bstack1l111ll1_opy_ = None
bstack111l111_opy_ = None
bstack1ll1111l1_opy_ = None
bstack1l1l111ll_opy_ = -1
bstack1lll1ll1_opy_ = DEFAULT_LOG_LEVEL
bstack1lll1llll_opy_ = 1
bstack11111lll_opy_ = False
bstack11ll11_opy_ = bstackl_opy_ (u"ࠩࠪ੊")
bstack11l1l1_opy_ = bstackl_opy_ (u"ࠪࠫੋ")
bstack1l1ll11l1_opy_ = False
bstack1111l111_opy_ = True
bstack11llll_opy_ = bstackl_opy_ (u"ࠫࠬੌ")
bstack111ll1l1_opy_ = None
bstack1llllll_opy_ = None
bstack1ll1ll11l_opy_ = None
bstack1llll11l1_opy_ = None
bstack1111111_opy_ = None
bstack1l1ll11_opy_ = None
bstack11l111l1_opy_ = None
bstack1l1lll_opy_ = None
bstack1ll1l1l_opy_ = None
bstack1l1ll11ll_opy_ = None
bstack1llll1l_opy_ = None
bstack11ll1l1l_opy_ = None
bstack1111lll1_opy_ = bstackl_opy_ (u"ࠧࠨ੍")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1lll1ll1_opy_,
                    format=bstackl_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫ੎"),
                    datefmt=bstackl_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ੏"))
def bstack1ll111_opy_():
  global CONFIG
  global bstack1lll1ll1_opy_
  if bstackl_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ੐") in CONFIG:
    bstack1lll1ll1_opy_ = bstack1lll111l_opy_[CONFIG[bstackl_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫੑ")]]
    logging.getLogger().setLevel(bstack1lll1ll1_opy_)
def bstack1ll111lll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11lllll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11l1l111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstackl_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡧࡴࡴࡦࡪࡩࡩ࡭ࡱ࡫ࠢ੒") == args[i].lower() or bstackl_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡯ࡨ࡬࡫ࠧ੓") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack11llll_opy_
      bstack11llll_opy_ += bstackl_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡉ࡯࡯ࡨ࡬࡫ࡋ࡯࡬ࡦࠢࠪ੔") + path
      return path
  return None
def bstack1l11lll11_opy_():
  bstack1l111l1_opy_ = bstack11l1l111_opy_()
  if bstack1l111l1_opy_ and os.path.exists(os.path.abspath(bstack1l111l1_opy_)):
    fileName = bstack1l111l1_opy_
  if bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪ੕") in os.environ and os.path.exists(os.path.abspath(os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ੖")])) and not bstackl_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪ੗") in locals():
    fileName = os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭੘")]
  if bstackl_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬਖ਼") in locals():
    bstack11l1_opy_ = os.path.abspath(fileName)
  else:
    bstack11l1_opy_ = bstackl_opy_ (u"ࠫࠬਗ਼")
  bstack1ll1ll111_opy_ = os.getcwd()
  bstack111ll111_opy_ = bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨਜ਼")
  bstack1ll1lll1l_opy_ = bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿࡡ࡮࡮ࠪੜ")
  while (not os.path.exists(bstack11l1_opy_)) and bstack1ll1ll111_opy_ != bstackl_opy_ (u"ࠢࠣ੝"):
    bstack11l1_opy_ = os.path.join(bstack1ll1ll111_opy_, bstack111ll111_opy_)
    if not os.path.exists(bstack11l1_opy_):
      bstack11l1_opy_ = os.path.join(bstack1ll1ll111_opy_, bstack1ll1lll1l_opy_)
    if bstack1ll1ll111_opy_ != os.path.dirname(bstack1ll1ll111_opy_):
      bstack1ll1ll111_opy_ = os.path.dirname(bstack1ll1ll111_opy_)
    else:
      bstack1ll1ll111_opy_ = bstackl_opy_ (u"ࠣࠤਫ਼")
  if not os.path.exists(bstack11l1_opy_):
    bstack1l1ll1ll_opy_(
      bstack1lll11ll_opy_.format(os.getcwd()))
  with open(bstack11l1_opy_, bstackl_opy_ (u"ࠩࡵࠫ੟")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1l1ll1ll_opy_(bstack11ll1l11_opy_.format(str(exc)))
def bstack1lll1111_opy_(config):
  bstack1ll1l1_opy_ = bstack111llll1_opy_(config)
  for option in list(bstack1ll1l1_opy_):
    if option.lower() in bstack1ll1ll1ll_opy_ and option != bstack1ll1ll1ll_opy_[option.lower()]:
      bstack1ll1l1_opy_[bstack1ll1ll1ll_opy_[option.lower()]] = bstack1ll1l1_opy_[option]
      del bstack1ll1l1_opy_[option]
  return config
def bstack1l1l1l111_opy_():
  global bstack111lll_opy_
  for key, bstack1111ll1l_opy_ in bstack1l1l11111_opy_.items():
    if isinstance(bstack1111ll1l_opy_, list):
      for var in bstack1111ll1l_opy_:
        if var in os.environ:
          bstack111lll_opy_[key] = os.environ[var]
          break
    elif bstack1111ll1l_opy_ in os.environ:
      bstack111lll_opy_[key] = os.environ[bstack1111ll1l_opy_]
  if bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ੠") in os.environ:
    bstack111lll_opy_[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ੡")] = {}
    bstack111lll_opy_[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ੢")][bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ੣")] = os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ੤")]
def bstack1ll111ll_opy_():
  global bstack1l1llll1_opy_
  global bstack11llll_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstackl_opy_ (u"ࠨ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੥").lower() == val.lower():
      bstack1l1llll1_opy_[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭੦")] = {}
      bstack1l1llll1_opy_[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ੧")][bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭੨")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack1llll11ll_opy_ in bstack1lll1111l_opy_.items():
    if isinstance(bstack1llll11ll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1llll11ll_opy_:
          if idx<len(sys.argv) and bstackl_opy_ (u"ࠬ࠳࠭ࠨ੩") + var.lower() == val.lower() and not key in bstack1l1llll1_opy_:
            bstack1l1llll1_opy_[key] = sys.argv[idx+1]
            bstack11llll_opy_ += bstackl_opy_ (u"࠭ࠠ࠮࠯ࠪ੪") + var + bstackl_opy_ (u"ࠧࠡࠩ੫") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstackl_opy_ (u"ࠨ࠯࠰ࠫ੬") + bstack1llll11ll_opy_.lower() == val.lower() and not key in bstack1l1llll1_opy_:
          bstack1l1llll1_opy_[key] = sys.argv[idx+1]
          bstack11llll_opy_ += bstackl_opy_ (u"ࠩࠣ࠱࠲࠭੭") + bstack1llll11ll_opy_ + bstackl_opy_ (u"ࠪࠤࠬ੮") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack11ll111l_opy_(config):
  bstack11l11l_opy_ = config.keys()
  for bstack1llllll1l_opy_, bstack1l1lll11_opy_ in bstack1l11ll1ll_opy_.items():
    if bstack1l1lll11_opy_ in bstack11l11l_opy_:
      config[bstack1llllll1l_opy_] = config[bstack1l1lll11_opy_]
      del config[bstack1l1lll11_opy_]
  for bstack1llllll1l_opy_, bstack1l1lll11_opy_ in bstack1l1l1111l_opy_.items():
    if isinstance(bstack1l1lll11_opy_, list):
      for bstack1111l11l_opy_ in bstack1l1lll11_opy_:
        if bstack1111l11l_opy_ in bstack11l11l_opy_:
          config[bstack1llllll1l_opy_] = config[bstack1111l11l_opy_]
          del config[bstack1111l11l_opy_]
          break
    elif bstack1l1lll11_opy_ in bstack11l11l_opy_:
        config[bstack1llllll1l_opy_] = config[bstack1l1lll11_opy_]
        del config[bstack1l1lll11_opy_]
  for bstack1111l11l_opy_ in list(config):
    for bstack11l11l11_opy_ in bstack1l1l1ll_opy_:
      if bstack1111l11l_opy_.lower() == bstack11l11l11_opy_.lower() and bstack1111l11l_opy_ != bstack11l11l11_opy_:
        config[bstack11l11l11_opy_] = config[bstack1111l11l_opy_]
        del config[bstack1111l11l_opy_]
  bstack11lll111_opy_ = []
  if bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੯") in config:
    bstack11lll111_opy_ = config[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨੰ")]
  for platform in bstack11lll111_opy_:
    for bstack1111l11l_opy_ in list(platform):
      for bstack11l11l11_opy_ in bstack1l1l1ll_opy_:
        if bstack1111l11l_opy_.lower() == bstack11l11l11_opy_.lower() and bstack1111l11l_opy_ != bstack11l11l11_opy_:
          platform[bstack11l11l11_opy_] = platform[bstack1111l11l_opy_]
          del platform[bstack1111l11l_opy_]
  for bstack1llllll1l_opy_, bstack1l1lll11_opy_ in bstack1l1l1111l_opy_.items():
    for platform in bstack11lll111_opy_:
      if isinstance(bstack1l1lll11_opy_, list):
        for bstack1111l11l_opy_ in bstack1l1lll11_opy_:
          if bstack1111l11l_opy_ in platform:
            platform[bstack1llllll1l_opy_] = platform[bstack1111l11l_opy_]
            del platform[bstack1111l11l_opy_]
            break
      elif bstack1l1lll11_opy_ in platform:
        platform[bstack1llllll1l_opy_] = platform[bstack1l1lll11_opy_]
        del platform[bstack1l1lll11_opy_]
  for bstack1l11lllll_opy_ in bstack11l111l_opy_:
    if bstack1l11lllll_opy_ in config:
      if not bstack11l111l_opy_[bstack1l11lllll_opy_] in config:
        config[bstack11l111l_opy_[bstack1l11lllll_opy_]] = {}
      config[bstack11l111l_opy_[bstack1l11lllll_opy_]].update(config[bstack1l11lllll_opy_])
      del config[bstack1l11lllll_opy_]
  for platform in bstack11lll111_opy_:
    for bstack1l11lllll_opy_ in bstack11l111l_opy_:
      if bstack1l11lllll_opy_ in list(platform):
        if not bstack11l111l_opy_[bstack1l11lllll_opy_] in platform:
          platform[bstack11l111l_opy_[bstack1l11lllll_opy_]] = {}
        platform[bstack11l111l_opy_[bstack1l11lllll_opy_]].update(platform[bstack1l11lllll_opy_])
        del platform[bstack1l11lllll_opy_]
  config = bstack1lll1111_opy_(config)
  return config
def bstack1ll1111l_opy_(config):
  global bstack11l1l1_opy_
  if bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪੱ") in config and str(config[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫੲ")]).lower() != bstackl_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧੳ"):
    if not bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ੴ") in config:
      config[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧੵ")] = {}
    if not bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭੶") in config[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ੷")]:
      current_time = datetime.datetime.now()
      bstack1l1ll1l1l_opy_ = current_time.strftime(bstackl_opy_ (u"࠭ࠥࡥࡡࠨࡦࡤࠫࡈࠦࡏࠪ੸"))
      hostname = socket.gethostname()
      bstack1l11lll1_opy_ = bstackl_opy_ (u"ࠧࠨ੹").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstackl_opy_ (u"ࠨࡽࢀࡣࢀࢃ࡟ࡼࡿࠪ੺").format(bstack1l1ll1l1l_opy_, hostname, bstack1l11lll1_opy_)
      config[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭੻")][bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ੼")] = identifier
    bstack11l1l1_opy_ = config[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ੽")][bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ੾")]
  return config
def bstack11111111_opy_():
  if (
    isinstance(os.getenv(bstackl_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠫ੿")), str) and len(os.getenv(bstackl_opy_ (u"ࠧࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠬ઀"))) > 0
  ) or (
    isinstance(os.getenv(bstackl_opy_ (u"ࠨࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠧઁ")), str) and len(os.getenv(bstackl_opy_ (u"ࠩࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠨં"))) > 0
  ):
    return os.getenv(bstackl_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩઃ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠫࡈࡏࠧ઄"))).lower() == bstackl_opy_ (u"ࠬࡺࡲࡶࡧࠪઅ") and str(os.getenv(bstackl_opy_ (u"࠭ࡃࡊࡔࡆࡐࡊࡉࡉࠨઆ"))).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬઇ"):
    return os.getenv(bstackl_opy_ (u"ࠨࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠫઈ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠩࡆࡍࠬઉ"))).lower() == bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨઊ") and str(os.getenv(bstackl_opy_ (u"࡙ࠫࡘࡁࡗࡋࡖࠫઋ"))).lower() == bstackl_opy_ (u"ࠬࡺࡲࡶࡧࠪઌ"):
    return os.getenv(bstackl_opy_ (u"࠭ࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬઍ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠧࡄࡋࠪ઎"))).lower() == bstackl_opy_ (u"ࠨࡶࡵࡹࡪ࠭એ") and str(os.getenv(bstackl_opy_ (u"ࠩࡆࡍࡤࡔࡁࡎࡇࠪઐ"))).lower() == bstackl_opy_ (u"ࠪࡧࡴࡪࡥࡴࡪ࡬ࡴࠬઑ"):
    return 0 # bstack1l11l1l_opy_ bstack111lll1_opy_ not set build number env
  if os.getenv(bstackl_opy_ (u"ࠫࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠧ઒")) and os.getenv(bstackl_opy_ (u"ࠬࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠨઓ")):
    return os.getenv(bstackl_opy_ (u"࠭ࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨઔ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠧࡄࡋࠪક"))).lower() == bstackl_opy_ (u"ࠨࡶࡵࡹࡪ࠭ખ") and str(os.getenv(bstackl_opy_ (u"ࠩࡇࡖࡔࡔࡅࠨગ"))).lower() == bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨઘ"):
    return os.getenv(bstackl_opy_ (u"ࠫࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩઙ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠬࡉࡉࠨચ"))).lower() == bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫછ") and str(os.getenv(bstackl_opy_ (u"ࠧࡔࡇࡐࡅࡕࡎࡏࡓࡇࠪજ"))).lower() == bstackl_opy_ (u"ࠨࡶࡵࡹࡪ࠭ઝ"):
    return os.getenv(bstackl_opy_ (u"ࠩࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠬઞ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠪࡇࡎ࠭ટ"))).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩઠ") and str(os.getenv(bstackl_opy_ (u"ࠬࡍࡉࡕࡎࡄࡆࡤࡉࡉࠨડ"))).lower() == bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫઢ"):
    return os.getenv(bstackl_opy_ (u"ࠧࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠪણ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠨࡅࡌࠫત"))).lower() == bstackl_opy_ (u"ࠩࡷࡶࡺ࡫ࠧથ") and str(os.getenv(bstackl_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡍࡌࡘࡊ࠭દ"))).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩધ"):
    return os.getenv(bstackl_opy_ (u"ࠬࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧન"), 0)
  if str(os.getenv(bstackl_opy_ (u"࠭ࡔࡇࡡࡅ࡙ࡎࡒࡄࠨ઩"))).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬપ"):
    return os.getenv(bstackl_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨફ"), 0)
  return -1
def bstack1l1ll1l11_opy_(bstack1l11l_opy_):
  global CONFIG
  if not bstackl_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫબ") in CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬભ")]:
    return
  CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭મ")] = CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧય")].replace(
    bstackl_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨર"),
    str(bstack1l11l_opy_)
  )
def bstack1ll1l111l_opy_():
  global CONFIG
  if not bstackl_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭઱") in CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪલ")]:
    return
  current_time = datetime.datetime.now()
  bstack1l1ll1l1l_opy_ = current_time.strftime(bstackl_opy_ (u"ࠩࠨࡨ࠲ࠫࡢ࠮ࠧࡋ࠾ࠪࡓࠧળ"))
  CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ઴")] = CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭વ")].replace(
    bstackl_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫશ"),
    bstack1l1ll1l1l_opy_
  )
def bstack1ll1l1l11_opy_():
  global CONFIG
  if bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨષ") in CONFIG and not bool(CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩસ")]):
    del CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪહ")]
    return
  if not bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ઺") in CONFIG:
    CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ઻")] = bstackl_opy_ (u"ࠫࠨࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃ઼ࠧ")
  if bstackl_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫઽ") in CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨા")]:
    bstack1ll1l111l_opy_()
    os.environ[bstackl_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫિ")] = CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪી")]
  if not bstackl_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫુ") in CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬૂ")]:
    return
  bstack1l11l_opy_ = bstackl_opy_ (u"ࠫࠬૃ")
  bstack1ll11l11_opy_ = bstack11111111_opy_()
  if bstack1ll11l11_opy_ != -1:
    bstack1l11l_opy_ = bstackl_opy_ (u"ࠬࡉࡉࠡࠩૄ") + str(bstack1ll11l11_opy_)
  if bstack1l11l_opy_ == bstackl_opy_ (u"࠭ࠧૅ"):
    bstack1111l1ll_opy_ = bstack1l1l1lll1_opy_(CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ૆")])
    if bstack1111l1ll_opy_ != -1:
      bstack1l11l_opy_ = str(bstack1111l1ll_opy_)
  if bstack1l11l_opy_:
    bstack1l1ll1l11_opy_(bstack1l11l_opy_)
    os.environ[bstackl_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬે")] = CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫૈ")]
def bstack1ll1ll1l_opy_(bstack1ll1lll11_opy_, bstack1l11111_opy_, path):
  bstack11l1l1l_opy_ = {
    bstackl_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧૉ"): bstack1l11111_opy_
  }
  if os.path.exists(path):
    bstack1lll11l1_opy_ = json.load(open(path, bstackl_opy_ (u"ࠫࡷࡨࠧ૊")))
  else:
    bstack1lll11l1_opy_ = {}
  bstack1lll11l1_opy_[bstack1ll1lll11_opy_] = bstack11l1l1l_opy_
  with open(path, bstackl_opy_ (u"ࠧࡽࠫࠣો")) as outfile:
    json.dump(bstack1lll11l1_opy_, outfile)
def bstack1l1l1lll1_opy_(bstack1ll1lll11_opy_):
  bstack1ll1lll11_opy_ = str(bstack1ll1lll11_opy_)
  bstack11l1ll1l_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"࠭ࡾࠨૌ")), bstackl_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ્ࠧ"))
  try:
    if not os.path.exists(bstack11l1ll1l_opy_):
      os.makedirs(bstack11l1ll1l_opy_)
    file_path = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠨࢀࠪ૎")), bstackl_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ૏"), bstackl_opy_ (u"ࠪ࠲ࡧࡻࡩ࡭ࡦ࠰ࡲࡦࡳࡥ࠮ࡥࡤࡧ࡭࡫࠮࡫ࡵࡲࡲࠬૐ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstackl_opy_ (u"ࠫࡼ࠭૑")):
        pass
      with open(file_path, bstackl_opy_ (u"ࠧࡽࠫࠣ૒")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstackl_opy_ (u"࠭ࡲࠨ૓")) as bstack1l11ll11l_opy_:
      bstack1ll1111_opy_ = json.load(bstack1l11ll11l_opy_)
    if bstack1ll1lll11_opy_ in bstack1ll1111_opy_:
      bstack11111l_opy_ = bstack1ll1111_opy_[bstack1ll1lll11_opy_][bstackl_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૔")]
      bstack1ll11l1ll_opy_ = int(bstack11111l_opy_) + 1
      bstack1ll1ll1l_opy_(bstack1ll1lll11_opy_, bstack1ll11l1ll_opy_, file_path)
      return bstack1ll11l1ll_opy_
    else:
      bstack1ll1ll1l_opy_(bstack1ll1lll11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack111l1l1_opy_.format(str(e)))
    return -1
def bstack1l1llll_opy_(config):
  if not config[bstackl_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ૕")] or not config[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ૖")]:
    return True
  else:
    return False
def bstack1l1l1l11l_opy_(config):
  if bstack11lllll1_opy_() < version.parse(bstackl_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩ૗")):
    return False
  if bstack11lllll1_opy_() >= version.parse(bstackl_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪ૘")):
    return True
  if bstackl_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ૙") in config and config[bstackl_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭૚")] == False:
    return False
  else:
    return True
def bstack111l1ll_opy_(config, index = 0):
  global bstack1l1ll11l1_opy_
  bstack111111l1_opy_ = {}
  caps = bstack1l11llll_opy_ + bstack1111111l_opy_
  if bstack1l1ll11l1_opy_:
    caps += bstack1ll11111l_opy_
  for key in config:
    if key in caps + [bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૛")]:
      continue
    bstack111111l1_opy_[key] = config[key]
  if bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૜") in config:
    for bstack11lll11_opy_ in config[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૝")][index]:
      if bstack11lll11_opy_ in caps + [bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ૞"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ૟")]:
        continue
      bstack111111l1_opy_[bstack11lll11_opy_] = config[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૠ")][index][bstack11lll11_opy_]
  bstack111111l1_opy_[bstackl_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨૡ")] = socket.gethostname()
  if bstackl_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨૢ") in bstack111111l1_opy_:
    del(bstack111111l1_opy_[bstackl_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩૣ")])
  return bstack111111l1_opy_
def bstack1l1l111l_opy_(config):
  global bstack1l1ll11l1_opy_
  bstack1lll11ll1_opy_ = {}
  caps = bstack1111111l_opy_
  if bstack1l1ll11l1_opy_:
    caps+= bstack1ll11111l_opy_
  for key in caps:
    if key in config:
      bstack1lll11ll1_opy_[key] = config[key]
  return bstack1lll11ll1_opy_
def bstack1l1lll1l_opy_(bstack111111l1_opy_, bstack1lll11ll1_opy_):
  bstack1l1l1l1l1_opy_ = {}
  for key in bstack111111l1_opy_.keys():
    if key in bstack1l11ll1ll_opy_:
      bstack1l1l1l1l1_opy_[bstack1l11ll1ll_opy_[key]] = bstack111111l1_opy_[key]
    else:
      bstack1l1l1l1l1_opy_[key] = bstack111111l1_opy_[key]
  for key in bstack1lll11ll1_opy_:
    if key in bstack1l11ll1ll_opy_:
      bstack1l1l1l1l1_opy_[bstack1l11ll1ll_opy_[key]] = bstack1lll11ll1_opy_[key]
    else:
      bstack1l1l1l1l1_opy_[key] = bstack1lll11ll1_opy_[key]
  return bstack1l1l1l1l1_opy_
def bstack1lllll1_opy_(config, index = 0):
  global bstack1l1ll11l1_opy_
  caps = {}
  bstack1lll11ll1_opy_ = bstack1l1l111l_opy_(config)
  bstack1l1l1l1_opy_ = bstack1111111l_opy_
  bstack1l1l1l1_opy_ += bstack1lll1ll1l_opy_
  if bstack1l1ll11l1_opy_:
    bstack1l1l1l1_opy_ += bstack1ll11111l_opy_
  if bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૤") in config:
    if bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ૥") in config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૦")][index]:
      caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ૧")] = config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૨")][index][bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ૩")]
    if bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ૪") in config[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૫")][index]:
      caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ૬")] = str(config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૭")][index][bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭૮")])
    bstack11l11111_opy_ = {}
    for bstack1l11ll111_opy_ in bstack1l1l1l1_opy_:
      if bstack1l11ll111_opy_ in config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૯")][index]:
        if bstack1l11ll111_opy_ == bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ૰"):
          bstack11l11111_opy_[bstack1l11ll111_opy_] = str(config[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૱")][index][bstack1l11ll111_opy_] * 1.0)
        else:
          bstack11l11111_opy_[bstack1l11ll111_opy_] = config[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૲")][index][bstack1l11ll111_opy_]
        del(config[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૳")][index][bstack1l11ll111_opy_])
    bstack1lll11ll1_opy_ = update(bstack1lll11ll1_opy_, bstack11l11111_opy_)
  bstack111111l1_opy_ = bstack111l1ll_opy_(config, index)
  for bstack1111l11l_opy_ in bstack1111111l_opy_ + [bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ૴"), bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭૵")]:
    if bstack1111l11l_opy_ in bstack111111l1_opy_:
      bstack1lll11ll1_opy_[bstack1111l11l_opy_] = bstack111111l1_opy_[bstack1111l11l_opy_]
      del(bstack111111l1_opy_[bstack1111l11l_opy_])
  if bstack1l1l1l11l_opy_(config):
    bstack111111l1_opy_[bstackl_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭૶")] = True
    caps.update(bstack1lll11ll1_opy_)
    caps[bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ૷")] = bstack111111l1_opy_
  else:
    bstack111111l1_opy_[bstackl_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ૸")] = False
    caps.update(bstack1l1lll1l_opy_(bstack111111l1_opy_, bstack1lll11ll1_opy_))
    if bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧૹ") in caps:
      caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫૺ")] = caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩૻ")]
      del(caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪૼ")])
    if bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ૽") in caps:
      caps[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ૾")] = caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ૿")]
      del(caps[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ଀")])
  return caps
def bstack1ll111l1l_opy_():
  if bstack11lllll1_opy_() <= version.parse(bstackl_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪଁ")):
    return bstack111lllll_opy_
  return bstack1l1l1llll_opy_
def bstack11ll1ll_opy_(options):
  return hasattr(options, bstackl_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬଂ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l111_opy_(options, bstack111lll1l_opy_):
  for bstack11l11l1_opy_ in bstack111lll1l_opy_:
    if bstack11l11l1_opy_ in [bstackl_opy_ (u"ࠬࡧࡲࡨࡵࠪଃ"), bstackl_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ଄")]:
      next
    if bstack11l11l1_opy_ in options._experimental_options:
      options._experimental_options[bstack11l11l1_opy_]= update(options._experimental_options[bstack11l11l1_opy_], bstack111lll1l_opy_[bstack11l11l1_opy_])
    else:
      options.add_experimental_option(bstack11l11l1_opy_, bstack111lll1l_opy_[bstack11l11l1_opy_])
  if bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬଅ") in bstack111lll1l_opy_:
    for arg in bstack111lll1l_opy_[bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ଆ")]:
      options.add_argument(arg)
    del(bstack111lll1l_opy_[bstackl_opy_ (u"ࠩࡤࡶ࡬ࡹࠧଇ")])
  if bstackl_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧଈ") in bstack111lll1l_opy_:
    for ext in bstack111lll1l_opy_[bstackl_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨଉ")]:
      options.add_extension(ext)
    del(bstack111lll1l_opy_[bstackl_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩଊ")])
def bstack11l1ll1_opy_(options, bstack1lll1l1l_opy_):
  if bstackl_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬଋ") in bstack1lll1l1l_opy_:
    for bstack11ll1ll1_opy_ in bstack1lll1l1l_opy_[bstackl_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ଌ")]:
      if bstack11ll1ll1_opy_ in options._preferences:
        options._preferences[bstack11ll1ll1_opy_] = update(options._preferences[bstack11ll1ll1_opy_], bstack1lll1l1l_opy_[bstackl_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ଍")][bstack11ll1ll1_opy_])
      else:
        options.set_preference(bstack11ll1ll1_opy_, bstack1lll1l1l_opy_[bstackl_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ଎")][bstack11ll1ll1_opy_])
  if bstackl_opy_ (u"ࠪࡥࡷ࡭ࡳࠨଏ") in bstack1lll1l1l_opy_:
    for arg in bstack1lll1l1l_opy_[bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩଐ")]:
      options.add_argument(arg)
def bstack1l1l11l11_opy_(options, bstack1l11l11_opy_):
  if bstackl_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭଑") in bstack1l11l11_opy_:
    options.use_webview(bool(bstack1l11l11_opy_[bstackl_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧ଒")]))
  bstack1l111_opy_(options, bstack1l11l11_opy_)
def bstack1l11l1l1_opy_(options, bstack1ll1ll1l1_opy_):
  for bstack1ll1llll_opy_ in bstack1ll1ll1l1_opy_:
    if bstack1ll1llll_opy_ in [bstackl_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫଓ"), bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ଔ")]:
      next
    options.set_capability(bstack1ll1llll_opy_, bstack1ll1ll1l1_opy_[bstack1ll1llll_opy_])
  if bstackl_opy_ (u"ࠩࡤࡶ࡬ࡹࠧକ") in bstack1ll1ll1l1_opy_:
    for arg in bstack1ll1ll1l1_opy_[bstackl_opy_ (u"ࠪࡥࡷ࡭ࡳࠨଖ")]:
      options.add_argument(arg)
  if bstackl_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨଗ") in bstack1ll1ll1l1_opy_:
    options.use_technology_preview(bool(bstack1ll1ll1l1_opy_[bstackl_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩଘ")]))
def bstack1ll11l1l1_opy_(options, bstack1111ll_opy_):
  for bstack1lll111ll_opy_ in bstack1111ll_opy_:
    if bstack1lll111ll_opy_ in [bstackl_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪଙ"), bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬଚ")]:
      next
    options._options[bstack1lll111ll_opy_] = bstack1111ll_opy_[bstack1lll111ll_opy_]
  if bstackl_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬଛ") in bstack1111ll_opy_:
    for bstack1l11ll_opy_ in bstack1111ll_opy_[bstackl_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ଜ")]:
      options.add_additional_option(
          bstack1l11ll_opy_, bstack1111ll_opy_[bstackl_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧଝ")][bstack1l11ll_opy_])
  if bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩଞ") in bstack1111ll_opy_:
    for arg in bstack1111ll_opy_[bstackl_opy_ (u"ࠬࡧࡲࡨࡵࠪଟ")]:
      options.add_argument(arg)
def bstack111ll11l_opy_(options, caps):
  if not hasattr(options, bstackl_opy_ (u"࠭ࡋࡆ࡛ࠪଠ")):
    return
  if options.KEY == bstackl_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬଡ") and options.KEY in caps:
    bstack1l111_opy_(options, caps[bstackl_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ଢ")])
  elif options.KEY == bstackl_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧଣ") and options.KEY in caps:
    bstack11l1ll1_opy_(options, caps[bstackl_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨତ")])
  elif options.KEY == bstackl_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬଥ") and options.KEY in caps:
    bstack1l11l1l1_opy_(options, caps[bstackl_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ଦ")])
  elif options.KEY == bstackl_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧଧ") and options.KEY in caps:
    bstack1l1l11l11_opy_(options, caps[bstackl_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨନ")])
  elif options.KEY == bstackl_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ଩") and options.KEY in caps:
    bstack1ll11l1l1_opy_(options, caps[bstackl_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨପ")])
def bstack1l1111l_opy_(caps):
  global bstack1l1ll11l1_opy_
  if bstack1l1ll11l1_opy_:
    if bstack1ll111lll_opy_() < version.parse(bstackl_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩଫ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫବ")
    if bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଭ") in caps:
      browser = caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫମ")]
    elif bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨଯ") in caps:
      browser = caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩର")]
    browser = str(browser).lower()
    if browser == bstackl_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩ଱") or browser == bstackl_opy_ (u"ࠪ࡭ࡵࡧࡤࠨଲ"):
      browser = bstackl_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫଳ")
    if browser == bstackl_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭଴"):
      browser = bstackl_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ଵ")
    if browser not in [bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧଶ"), bstackl_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ଷ"), bstackl_opy_ (u"ࠩ࡬ࡩࠬସ"), bstackl_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪହ"), bstackl_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬ଺")]:
      return None
    try:
      package = bstackl_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ଻").format(browser)
      name = bstackl_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹ଼ࠧ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11ll1ll_opy_(options):
        return None
      for bstack1111l11l_opy_ in caps.keys():
        options.set_capability(bstack1111l11l_opy_, caps[bstack1111l11l_opy_])
      bstack111ll11l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1llllllll_opy_(options, bstack1lll1l1_opy_):
  if not bstack11ll1ll_opy_(options):
    return
  for bstack1111l11l_opy_ in bstack1lll1l1_opy_.keys():
    if bstack1111l11l_opy_ in bstack1lll1ll1l_opy_:
      next
    if bstack1111l11l_opy_ in options._caps and type(options._caps[bstack1111l11l_opy_]) in [dict, list]:
      options._caps[bstack1111l11l_opy_] = update(options._caps[bstack1111l11l_opy_], bstack1lll1l1_opy_[bstack1111l11l_opy_])
    else:
      options.set_capability(bstack1111l11l_opy_, bstack1lll1l1_opy_[bstack1111l11l_opy_])
  bstack111ll11l_opy_(options, bstack1lll1l1_opy_)
  if bstackl_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ଽ") in options._caps:
    if options._caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ା")] and options._caps[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧି")].lower() != bstackl_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫୀ"):
      del options._caps[bstackl_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪୁ")]
def bstack1111l1l1_opy_(proxy_config):
  if bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩୂ") in proxy_config:
    proxy_config[bstackl_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨୃ")] = proxy_config[bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫୄ")]
    del(proxy_config[bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ୅")])
  if bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ୆") in proxy_config and proxy_config[bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭େ")].lower() != bstackl_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫୈ"):
    proxy_config[bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ୉")] = bstackl_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭୊")
  if bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬୋ") in proxy_config:
    proxy_config[bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫୌ")] = bstackl_opy_ (u"ࠩࡳࡥࡨ୍࠭")
  return proxy_config
def bstack1l1l11l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ୎") in config:
    return proxy
  config[bstackl_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ୏")] = bstack1111l1l1_opy_(config[bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ୐")])
  if proxy == None:
    proxy = Proxy(config[bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ୑")])
  return proxy
def bstack1111l11_opy_(self):
  global CONFIG
  global bstack1l1lll_opy_
  if bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ୒") in CONFIG:
    return CONFIG[bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ୓")]
  elif bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭୔") in CONFIG:
    return CONFIG[bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ୕")]
  else:
    return bstack1l1lll_opy_(self)
def bstack111l11l1_opy_():
  global CONFIG
  return bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧୖ") in CONFIG or bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩୗ") in CONFIG
def bstack11llllll_opy_(config):
  if not bstack111l11l1_opy_():
    return
  if config.get(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ୘")):
    return config.get(bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ୙"))
  if config.get(bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ୚")):
    return config.get(bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭୛"))
def bstack1ll1l_opy_():
  return bstack111l11l1_opy_() and bstack11lllll1_opy_() >= version.parse(bstack1l1lll11l_opy_)
def bstack111llll1_opy_(config):
  if bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧଡ଼") in config:
    return config[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨଢ଼")]
  if bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୞") in config:
    return config[bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬୟ")]
  return {}
def bstack1l1lllll1_opy_(caps):
  global bstack11l1l1_opy_
  if bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨୠ") in caps:
    caps[bstackl_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩୡ")][bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨୢ")] = True
    if bstack11l1l1_opy_:
      caps[bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫୣ")][bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭୤")] = bstack11l1l1_opy_
  else:
    caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ୥")] = True
    if bstack11l1l1_opy_:
      caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ୦")] = bstack11l1l1_opy_
def bstack1l1lll1_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ୧") in CONFIG and CONFIG[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ୨")]:
    bstack1ll1l1_opy_ = bstack111llll1_opy_(CONFIG)
    bstack1ll111l11_opy_(CONFIG[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ୩")], bstack1ll1l1_opy_)
def bstack1ll111l11_opy_(key, bstack1ll1l1_opy_):
  global bstack1l1l1ll1l_opy_
  logger.info(bstack1lll1lll1_opy_)
  try:
    bstack1l1l1ll1l_opy_ = Local()
    bstack1l11l11l_opy_ = {bstackl_opy_ (u"ࠪ࡯ࡪࡿࠧ୪"): key}
    bstack1l11l11l_opy_.update(bstack1ll1l1_opy_)
    logger.debug(bstack11l11l1l_opy_.format(str(bstack1l11l11l_opy_)))
    bstack1l1l1ll1l_opy_.start(**bstack1l11l11l_opy_)
    if bstack1l1l1ll1l_opy_.isRunning():
      logger.info(bstack11l111_opy_)
  except Exception as e:
    bstack1l1ll1ll_opy_(bstack1ll1lllll_opy_.format(str(e)))
def bstack1lll1ll_opy_():
  global bstack1l1l1ll1l_opy_
  if bstack1l1l1ll1l_opy_.isRunning():
    logger.info(bstack1l11ll1_opy_)
    bstack1l1l1ll1l_opy_.stop()
  bstack1l1l1ll1l_opy_ = None
def bstack1ll11l11l_opy_():
  global bstack1111lll1_opy_
  if bstack1111lll1_opy_:
    logger.warning(bstack1llll1l1_opy_.format(str(bstack1111lll1_opy_)))
  logger.info(bstack1ll1l1ll1_opy_)
  global bstack1l1l1ll1l_opy_
  if bstack1l1l1ll1l_opy_:
    bstack1lll1ll_opy_()
  logger.info(bstack1l1l11l1_opy_)
  bstack1l1ll111_opy_()
def bstack111l1lll_opy_(self, *args):
  logger.error(bstack1l1ll1lll_opy_)
  bstack1ll11l11l_opy_()
  sys.exit(1)
def bstack1l1ll1ll_opy_(err):
  logger.critical(bstack11l1111_opy_.format(str(err)))
  bstack1l1ll111_opy_(bstack11l1111_opy_.format(str(err)))
  atexit.unregister(bstack1ll11l11l_opy_)
  sys.exit(1)
def bstack1llll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1ll111_opy_(message)
  atexit.unregister(bstack1ll11l11l_opy_)
  sys.exit(1)
def bstack1lll11_opy_():
  global CONFIG
  global bstack1l1llll1_opy_
  global bstack111lll_opy_
  global bstack1111l111_opy_
  CONFIG = bstack1l11lll11_opy_()
  bstack1l1l1l111_opy_()
  bstack1ll111ll_opy_()
  CONFIG = bstack11ll111l_opy_(CONFIG)
  update(CONFIG, bstack111lll_opy_)
  update(CONFIG, bstack1l1llll1_opy_)
  CONFIG = bstack1ll1111l_opy_(CONFIG)
  if bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ୫") in CONFIG and str(CONFIG[bstackl_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ୬")]).lower() == bstackl_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ୭"):
    bstack1111l111_opy_ = False
  if (bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ୮") in CONFIG and bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ୯") in bstack1l1llll1_opy_) or (bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ୰") in CONFIG and bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ୱ") not in bstack111lll_opy_):
    if os.getenv(bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ୲")):
      CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ୳")] = os.getenv(bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ୴"))
    else:
      bstack1ll1l1l11_opy_()
  elif (bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ୵") not in CONFIG and bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ୶") in CONFIG) or (bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ୷") in bstack111lll_opy_ and bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭୸") not in bstack1l1llll1_opy_):
    del(CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭୹")])
  if bstack1l1llll_opy_(CONFIG):
    bstack1l1ll1ll_opy_(bstack11111l1l_opy_)
  bstack11llll11_opy_()
  bstack1l1111_opy_()
  if bstack1l1ll11l1_opy_:
    CONFIG[bstackl_opy_ (u"ࠬࡧࡰࡱࠩ୺")] = bstack1lllll11_opy_(CONFIG)
    logger.info(bstack1l11l1ll_opy_.format(CONFIG[bstackl_opy_ (u"࠭ࡡࡱࡲࠪ୻")]))
def bstack1l1111_opy_():
  global CONFIG
  global bstack1l1ll11l1_opy_
  if bstackl_opy_ (u"ࠧࡢࡲࡳࠫ୼") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1llll1_opy_(e, bstack111llll_opy_)
    bstack1l1ll11l1_opy_ = True
def bstack1lllll11_opy_(config):
  bstack1111l_opy_ = bstackl_opy_ (u"ࠨࠩ୽")
  app = config[bstackl_opy_ (u"ࠩࡤࡴࡵ࠭୾")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1ll11ll1l_opy_:
      if os.path.exists(app):
        bstack1111l_opy_ = bstack11l11ll1_opy_(config, app)
      elif bstack1ll11lll1_opy_(app):
        bstack1111l_opy_ = app
      else:
        bstack1l1ll1ll_opy_(bstack1lll1ll11_opy_.format(app))
    else:
      if bstack1ll11lll1_opy_(app):
        bstack1111l_opy_ = app
      elif os.path.exists(app):
        bstack1111l_opy_ = bstack11l11ll1_opy_(app)
      else:
        bstack1l1ll1ll_opy_(bstack1lllll1ll_opy_)
  else:
    if len(app) > 2:
      bstack1l1ll1ll_opy_(bstack1l1l1111_opy_)
    elif len(app) == 2:
      if bstackl_opy_ (u"ࠪࡴࡦࡺࡨࠨ୿") in app and bstackl_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ஀") in app:
        if os.path.exists(app[bstackl_opy_ (u"ࠬࡶࡡࡵࡪࠪ஁")]):
          bstack1111l_opy_ = bstack11l11ll1_opy_(config, app[bstackl_opy_ (u"࠭ࡰࡢࡶ࡫ࠫஂ")], app[bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪஃ")])
        else:
          bstack1l1ll1ll_opy_(bstack1lll1ll11_opy_.format(app))
      else:
        bstack1l1ll1ll_opy_(bstack1l1l1111_opy_)
    else:
      for key in app:
        if key in bstack1lllll11l_opy_:
          if key == bstackl_opy_ (u"ࠨࡲࡤࡸ࡭࠭஄"):
            if os.path.exists(app[key]):
              bstack1111l_opy_ = bstack11l11ll1_opy_(config, app[key])
            else:
              bstack1l1ll1ll_opy_(bstack1lll1ll11_opy_.format(app))
          else:
            bstack1111l_opy_ = app[key]
        else:
          bstack1l1ll1ll_opy_(bstack11l1ll_opy_)
  return bstack1111l_opy_
def bstack1ll11lll1_opy_(bstack1111l_opy_):
  import re
  bstack1lllll1l1_opy_ = re.compile(bstackl_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤஅ"))
  bstack1l1ll_opy_ = re.compile(bstackl_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫ࠱࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢஆ"))
  if bstackl_opy_ (u"ࠫࡧࡹ࠺࠰࠱ࠪஇ") in bstack1111l_opy_ or re.fullmatch(bstack1lllll1l1_opy_, bstack1111l_opy_) or re.fullmatch(bstack1l1ll_opy_, bstack1111l_opy_):
    return True
  else:
    return False
def bstack11l11ll1_opy_(config, path, bstack11l1l11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstackl_opy_ (u"ࠬࡸࡢࠨஈ")).read()).hexdigest()
  bstack1l1ll111l_opy_ = bstack1l1lllll_opy_(md5_hash)
  bstack1111l_opy_ = None
  if bstack1l1ll111l_opy_:
    logger.info(bstack1l111ll_opy_.format(bstack1l1ll111l_opy_, md5_hash))
    return bstack1l1ll111l_opy_
  bstack1l111l1l_opy_ = MultipartEncoder(
    fields={
        bstackl_opy_ (u"࠭ࡦࡪ࡮ࡨࠫஉ"): (os.path.basename(path), open(os.path.abspath(path), bstackl_opy_ (u"ࠧࡳࡤࠪஊ")), bstackl_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡰ࡭ࡣ࡬ࡲࠬ஋")),
        bstackl_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ஌"): bstack11l1l11_opy_
    }
  )
  response = requests.post(bstack1ll11111_opy_, data=bstack1l111l1l_opy_,
                         headers={bstackl_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ஍"): bstack1l111l1l_opy_.content_type}, auth=(config[bstackl_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭எ")], config[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨஏ")]))
  try:
    res = json.loads(response.text)
    bstack1111l_opy_ = res[bstackl_opy_ (u"࠭ࡡࡱࡲࡢࡹࡷࡲࠧஐ")]
    logger.info(bstack1lllll1l_opy_.format(bstack1111l_opy_))
    bstack11111_opy_(md5_hash, bstack1111l_opy_)
  except ValueError as err:
    bstack1l1ll1ll_opy_(bstack1ll111l_opy_.format(str(err)))
  return bstack1111l_opy_
def bstack11llll11_opy_():
  global CONFIG
  global bstack1lll1llll_opy_
  bstack11llll1l_opy_ = 0
  bstack1ll1ll1_opy_ = 1
  if bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ஑") in CONFIG:
    bstack1ll1ll1_opy_ = CONFIG[bstackl_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨஒ")]
  if bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬஓ") in CONFIG:
    bstack11llll1l_opy_ = len(CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ஔ")])
  bstack1lll1llll_opy_ = int(bstack1ll1ll1_opy_) * int(bstack11llll1l_opy_)
def bstack1l1lllll_opy_(md5_hash):
  bstack1lll1_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠫࢃ࠭க")), bstackl_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ஖"), bstackl_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ஗"))
  if os.path.exists(bstack1lll1_opy_):
    bstack1ll111111_opy_ = json.load(open(bstack1lll1_opy_,bstackl_opy_ (u"ࠧࡳࡤࠪ஘")))
    if md5_hash in bstack1ll111111_opy_:
      bstack1l1l11ll1_opy_ = bstack1ll111111_opy_[md5_hash]
      bstack1ll1l1ll_opy_ = datetime.datetime.now()
      bstack1111l1_opy_ = datetime.datetime.strptime(bstack1l1l11ll1_opy_[bstackl_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫங")], bstackl_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ச"))
      if (bstack1ll1l1ll_opy_ - bstack1111l1_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l1l11ll1_opy_[bstackl_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ஛")]):
        return None
      return bstack1l1l11ll1_opy_[bstackl_opy_ (u"ࠫ࡮ࡪࠧஜ")]
  else:
    return None
def bstack11111_opy_(md5_hash, bstack1111l_opy_):
  bstack11l1ll1l_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠬࢄࠧ஝")), bstackl_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ஞ"))
  if not os.path.exists(bstack11l1ll1l_opy_):
    os.makedirs(bstack11l1ll1l_opy_)
  bstack1lll1_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠧࡿࠩட")), bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ஠"), bstackl_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ஡"))
  bstack1ll111ll1_opy_ = {
    bstackl_opy_ (u"ࠪ࡭ࡩ࠭஢"): bstack1111l_opy_,
    bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧண"): datetime.datetime.strftime(datetime.datetime.now(), bstackl_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩத")),
    bstackl_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ஥"): str(__version__)
  }
  if os.path.exists(bstack1lll1_opy_):
    bstack1ll111111_opy_ = json.load(open(bstack1lll1_opy_,bstackl_opy_ (u"ࠧࡳࡤࠪ஦")))
  else:
    bstack1ll111111_opy_ = {}
  bstack1ll111111_opy_[md5_hash] = bstack1ll111ll1_opy_
  with open(bstack1lll1_opy_, bstackl_opy_ (u"ࠣࡹ࠮ࠦ஧")) as outfile:
    json.dump(bstack1ll111111_opy_, outfile)
def bstack11ll11ll_opy_(self):
  return
def bstack1lll1l1l1_opy_(self):
  return
def bstack1llll111_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1l1l11l1l_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l111ll1_opy_
  global bstack1l1l111ll_opy_
  global bstack1ll1111l1_opy_
  global bstack11111lll_opy_
  global bstack11ll11_opy_
  global bstack111ll1l1_opy_
  CONFIG[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫந")] = str(bstack11ll11_opy_) + str(__version__)
  command_executor = bstack1ll111l1l_opy_()
  logger.debug(bstack11ll1l_opy_.format(command_executor))
  proxy = bstack1l1l11l_opy_(CONFIG, proxy)
  bstack1l11lll1l_opy_ = 0 if bstack1l1l111ll_opy_ < 0 else bstack1l1l111ll_opy_
  if bstack11111lll_opy_ is True:
    bstack1l11lll1l_opy_ = int(threading.current_thread().getName())
  bstack1lll1l1_opy_ = bstack1lllll1_opy_(CONFIG, bstack1l11lll1l_opy_)
  logger.debug(bstack111ll1l_opy_.format(str(bstack1lll1l1_opy_)))
  if bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧன") in CONFIG and CONFIG[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨப")]:
    bstack1l1lllll1_opy_(bstack1lll1l1_opy_)
  if desired_capabilities:
    bstack11111ll1_opy_ = bstack11ll111l_opy_(desired_capabilities)
    bstack11111ll1_opy_[bstackl_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ஫")] = bstack1l1l1l11l_opy_(CONFIG)
    bstack1llllll11_opy_ = bstack1lllll1_opy_(bstack11111ll1_opy_)
    if bstack1llllll11_opy_:
      bstack1lll1l1_opy_ = update(bstack1llllll11_opy_, bstack1lll1l1_opy_)
    desired_capabilities = None
  if options:
    bstack1llllllll_opy_(options, bstack1lll1l1_opy_)
  if not options:
    options = bstack1l1111l_opy_(bstack1lll1l1_opy_)
  if options and bstack11lllll1_opy_() >= version.parse(bstackl_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ஬")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack11lllll1_opy_() < version.parse(bstackl_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭஭")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lll1l1_opy_)
  logger.info(bstack1l1llll1l_opy_)
  if bstack11lllll1_opy_() >= version.parse(bstackl_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧம")):
    bstack111ll1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11lllll1_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩய")):
    bstack111ll1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack111ll1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  bstack1l111ll1_opy_ = self.session_id
  if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ர") in CONFIG and bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩற") in CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨல")][bstack1l11lll1l_opy_]:
    bstack1ll1111l1_opy_ = CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩள")][bstack1l11lll1l_opy_][bstackl_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬழ")]
  logger.debug(bstack111l1ll1_opy_.format(bstack1l111ll1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1lll1l11l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      if(bstackl_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥவ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠩࢁࠫஶ")), bstackl_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪஷ"), bstackl_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ஸ")), bstackl_opy_ (u"ࠬࡽࠧஹ")) as fp:
          fp.write(bstackl_opy_ (u"ࠨࠢ஺"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ஻")))):
          with open(args[1], bstackl_opy_ (u"ࠨࡴࠪ஼")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstackl_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨ஽") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll11l_opy_)
            lines.insert(1, bstack1ll1l11ll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧா")), bstackl_opy_ (u"ࠫࡼ࠭ி")) as bstack111l1111_opy_:
              bstack111l1111_opy_.writelines(lines)
        CONFIG[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧீ")] = str(bstack11ll11_opy_) + str(__version__)
        bstack1l11lll1l_opy_ = 0 if bstack1l1l111ll_opy_ < 0 else bstack1l1l111ll_opy_
        if bstack11111lll_opy_ is True:
          bstack1l11lll1l_opy_ = int(threading.current_thread().getName())
        CONFIG[bstackl_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨு")] = False
        bstack1lll1l1_opy_ = bstack1lllll1_opy_(CONFIG, bstack1l11lll1l_opy_)
        logger.debug(bstack111ll1l_opy_.format(str(bstack1lll1l1_opy_)))
        if CONFIG[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫூ")]:
          bstack1l1lllll1_opy_(bstack1lll1l1_opy_)
        if bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௃") in CONFIG and bstackl_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ௄") in CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௅")][bstack1l11lll1l_opy_]:
          bstack1ll1111l1_opy_ = CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧெ")][bstack1l11lll1l_opy_][bstackl_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪே")]
        args.append(os.path.join(os.path.expanduser(bstackl_opy_ (u"࠭ࡾࠨை")), bstackl_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ௉"), bstackl_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪொ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1lll1l1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦோ"))
      return bstack1llll1l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    logger.debug(bstack1ll111l1_opy_ + str(e))
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack111l11_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l111ll1_opy_
    global bstack1l1l111ll_opy_
    global bstack1ll1111l1_opy_
    global bstack11111lll_opy_
    global bstack11ll11_opy_
    global bstack111ll1l1_opy_
    CONFIG[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬௌ")] = str(bstack11ll11_opy_) + str(__version__)
    bstack1l11lll1l_opy_ = 0 if bstack1l1l111ll_opy_ < 0 else bstack1l1l111ll_opy_
    if bstack11111lll_opy_ is True:
      bstack1l11lll1l_opy_ = int(threading.current_thread().getName())
    CONFIG[bstackl_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆ்ࠦ")] = False
    bstack1lll1l1_opy_ = bstack1lllll1_opy_(CONFIG, bstack1l11lll1l_opy_)
    logger.debug(bstack111ll1l_opy_.format(str(bstack1lll1l1_opy_)))
    if CONFIG[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ௎")]:
      bstack1l1lllll1_opy_(bstack1lll1l1_opy_)
    if bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௏") in CONFIG and bstackl_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬௐ") in CONFIG[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௑")][bstack1l11lll1l_opy_]:
      bstack1ll1111l1_opy_ = CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௒")][bstack1l11lll1l_opy_][bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ௓")]
    import urllib
    import json
    bstack111111ll_opy_ = bstackl_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭௔") + urllib.parse.quote(json.dumps(bstack1lll1l1_opy_))
    browser = self.connect(bstack111111ll_opy_)
    return browser
except Exception as e:
    logger.debug(bstack1ll111l1_opy_ + str(e))
def bstack1l11ll1l_opy_():
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack111l11_opy_
    except Exception as e:
        logger.debug(bstack1ll111l1_opy_ + str(e))
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1lll1l11l_opy_
    except Exception as e:
      logger.debug(bstack1ll111l1_opy_ + str(e))
def bstack1ll1ll_opy_(context, bstack111lll11_opy_):
  try:
    context.page.evaluate(bstackl_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ௕"), bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪ௖")+ json.dumps(bstack111lll11_opy_) + bstackl_opy_ (u"ࠢࡾࡿࠥௗ"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨ௘"), e)
def bstack11ll1111_opy_(context, message, level):
  try:
    context.page.evaluate(bstackl_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ௙"), bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ௚") + json.dumps(message) + bstackl_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧ௛") + json.dumps(level) + bstackl_opy_ (u"ࠬࢃࡽࠨ௜"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤ௝"), e)
def bstack1ll11_opy_(context, status, message = bstackl_opy_ (u"ࠢࠣ௞")):
  try:
    if(status == bstackl_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ௟")):
      context.page.evaluate(bstackl_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ௠"), bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠫ௡") + json.dumps(bstackl_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࠨ௢") + str(message)) + bstackl_opy_ (u"ࠬ࠲ࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩ௣") + json.dumps(status) + bstackl_opy_ (u"ࠨࡽࡾࠤ௤"))
    else:
      context.page.evaluate(bstackl_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ௥"), bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩ௦") + json.dumps(status) + bstackl_opy_ (u"ࠤࢀࢁࠧ௧"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢ௨"), e)
def bstack1l1l1ll11_opy_(self, url):
  global bstack1l1ll11ll_opy_
  try:
    bstack1l1ll1l1_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll11ll11_opy_.format(str(err)))
  try:
    bstack1l1ll11ll_opy_(self, url)
  except Exception as e:
    try:
      bstack1l111l_opy_ = str(e)
      if bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡎࡐࡖࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࠬ௩") in bstack1l111l_opy_ or bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡈࡘࡗࡊࡊࠧ௪") in bstack1l111l_opy_ or bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡘ࡚ࡔࡎࡆࡎࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧ௫") in bstack1l111l_opy_:
        bstack1l1ll1l1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1ll11ll11_opy_.format(str(err)))
    raise e
def bstack11l1l11l_opy_(self, test):
  global CONFIG
  global bstack1l111ll1_opy_
  global bstack111l111_opy_
  global bstack1ll1111l1_opy_
  global bstack1llllll_opy_
  try:
    if not bstack1l111ll1_opy_:
      with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠧࡿࠩ௬")), bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ௭"), bstackl_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ௮"))) as f:
        bstack1l1l1l_opy_ = json.loads(bstackl_opy_ (u"ࠥࡿࠧ௯") + f.read().strip() + bstackl_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭௰") + bstackl_opy_ (u"ࠧࢃࠢ௱"))
        bstack1l111ll1_opy_ = bstack1l1l1l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l111ll1_opy_:
    try:
      data = {}
      bstack1lllllll_opy_ = None
      if test:
        bstack1lllllll_opy_ = str(test.data)
      if bstack1lllllll_opy_ and not bstack1ll1111l1_opy_:
        data[bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ௲")] = bstack1lllllll_opy_
      if bstack111l111_opy_:
        if bstack111l111_opy_.status == bstackl_opy_ (u"ࠧࡑࡃࡖࡗࠬ௳"):
          data[bstackl_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ௴")] = bstackl_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ௵")
        elif bstack111l111_opy_.status == bstackl_opy_ (u"ࠪࡊࡆࡏࡌࠨ௶"):
          data[bstackl_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ௷")] = bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ௸")
          if bstack111l111_opy_.message:
            data[bstackl_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭௹")] = str(bstack111l111_opy_.message)
      user = CONFIG[bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ௺")]
      key = CONFIG[bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ௻")]
      url = bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧ௼").format(user, key, bstack1l111ll1_opy_)
      headers = {
        bstackl_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ௽"): bstackl_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ௾"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll1lll_opy_.format(str(e)))
  bstack1llllll_opy_(self, test)
def bstack1l1l1l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll1ll11l_opy_
  bstack1ll1ll11l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack111l111_opy_
  bstack111l111_opy_ = self._test
def bstack1111ll1_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstackl_opy_ (u"ࠧࡵࡵࡵࡲࡸࡸࠧ௿"), bstackl_opy_ (u"ࠨ࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠥఀ"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstackl_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࡤࡪࡴࠥఁ"), bstackl_opy_ (u"ࠣ࠰ࠥం")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstackl_opy_ (u"ࠤ࠭࠲ࡽࡳ࡬ࠣః"))))
  if not files:
    pabot._write(bstackl_opy_ (u"࡛ࠪࡆࡘࡎ࠻ࠢࡑࡳࠥࡵࡵࡵࡲࡸࡸࠥ࡬ࡩ࡭ࡧࡶࠤ࡮ࡴࠠࠣࠧࡶࠦࠬఄ") % outs_dir, pabot.Color.YELLOW)
    return bstackl_opy_ (u"ࠦࠧఅ")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack111ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstackl_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤఆ") in options:
    del options[bstackl_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥఇ")]
  if ROBOT_VERSION < bstackl_opy_ (u"ࠢ࠵࠰࠳ࠦఈ"):
    stats = {
      bstackl_opy_ (u"ࠣࡥࡵ࡭ࡹ࡯ࡣࡢ࡮ࠥఉ"): {bstackl_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࠣఊ"): 0, bstackl_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥఋ"): 0, bstackl_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦఌ"): 0},
      bstackl_opy_ (u"ࠧࡧ࡬࡭ࠤ఍"): {bstackl_opy_ (u"ࠨࡴࡰࡶࡤࡰࠧఎ"): 0, bstackl_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢఏ"): 0, bstackl_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣఐ"): 0},
    }
  else:
    stats = {
      bstackl_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࠣ఑"): 0,
      bstackl_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥఒ"): 0,
      bstackl_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦఓ"): 0,
      bstackl_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨఔ"): 0,
    }
  if pabot_args[bstackl_opy_ (u"ࠨࡂࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡠࡔࡘࡒࠧక")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstackl_opy_ (u"ࠢࡃࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡡࡕ࡙ࡓࠨఖ")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstackl_opy_ (u"ࠣࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠦగ")], pabot_args[bstackl_opy_ (u"ࠤࡤࡶࡹ࡯ࡦࡢࡥࡷࡷ࡮ࡴࡳࡶࡤࡩࡳࡱࡪࡥࡳࡵࠥఘ")]
      )
      outputs += [
        bstack1111ll1_opy_(
          os.path.join(outs_dir, str(index)+ bstackl_opy_ (u"ࠥ࠳ࠧఙ")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstackl_opy_ (u"ࠦࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠦచ"), bstackl_opy_ (u"ࠧࡵࡵࡵࡲࡸࡸࠪࡹ࠮ࡹ࡯࡯ࠦఛ") % index),
        )
      ]
    if bstackl_opy_ (u"ࠨ࡯ࡶࡶࡳࡹࡹࠨజ") not in options:
      options[bstackl_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠢఝ")] = bstackl_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠧఞ")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lll1lll_opy_(self, ff_profile_dir):
  global bstack1llll11l1_opy_
  if not ff_profile_dir:
    return None
  return bstack1llll11l1_opy_(self, ff_profile_dir)
def bstack1l1ll1111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11l1l1_opy_
  bstack1l11111l_opy_ = []
  if bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬట") in CONFIG:
    bstack1l11111l_opy_ = CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఠ")]
  bstack1l1l1_opy_ = len(suite_group) * len(pabot_args[bstackl_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦడ")] or [(bstackl_opy_ (u"ࠧࠨఢ"), None)]) * len(bstack1l11111l_opy_)
  pabot_args[bstackl_opy_ (u"ࠨࡂࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡠࡔࡘࡒࠧణ")] = []
  for q in range(bstack1l1l1_opy_):
    pabot_args[bstackl_opy_ (u"ࠢࡃࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡡࡕ࡙ࡓࠨత")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstackl_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤథ")],
      pabot_args[bstackl_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥద")],
      argfile,
      pabot_args.get(bstackl_opy_ (u"ࠥ࡬࡮ࡼࡥࠣధ")),
      pabot_args[bstackl_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢన")],
      platform[0],
      bstack11l1l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstackl_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧ఩")] or [(bstackl_opy_ (u"ࠨࠢప"), None)]
    for platform in enumerate(bstack1l11111l_opy_)
  ]
def bstack1l1llll11_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack1ll11ll_opy_=bstackl_opy_ (u"ࠧࠨఫ")):
  global bstack1l1ll11_opy_
  self.platform_index = platform_index
  self.bstack1lll1l_opy_ = bstack1ll11ll_opy_
  bstack1l1ll11_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1lll1l11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack11l111l1_opy_
  global bstack11llll_opy_
  if not bstackl_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪబ") in item.options:
    item.options[bstackl_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫభ")] = []
  for v in item.options[bstackl_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬమ")]:
    if bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪయ") in v:
      item.options[bstackl_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧర")].remove(v)
    if bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ఱ") in v:
      item.options[bstackl_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩల")].remove(v)
  item.options[bstackl_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪళ")].insert(0, bstackl_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫఴ").format(item.platform_index))
  item.options[bstackl_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬవ")].insert(0, bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫశ").format(item.bstack1lll1l_opy_))
  if bstack11llll_opy_:
    item.options[bstackl_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧష")].insert(0, bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩస").format(bstack11llll_opy_))
  return bstack11l111l1_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l1l111l1_opy_(command):
  global bstack11llll_opy_
  if bstack11llll_opy_:
    command[0] = command[0].replace(bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭హ"), bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠭఺") + bstack11llll_opy_, 1)
  else:
    command[0] = command[0].replace(bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ఻"), bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲ఼ࠧ"), 1)
def bstack11l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1111111_opy_
  bstack1l1l111l1_opy_(command)
  return bstack1111111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1lll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1111111_opy_
  bstack1l1l111l1_opy_(command)
  return bstack1111111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1111111_opy_
  bstack1l1l111l1_opy_(command)
  return bstack1111111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1l1111l1_opy_(self, runner, quiet=False, capture=True):
  global bstack11lll1l_opy_
  bstack111l1_opy_ = bstack11lll1l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstackl_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫఽ")):
      runner.exception_arr = []
    if not hasattr(runner, bstackl_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩా")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111l1_opy_
def bstack111l1l_opy_(self, name, context, *args):
  global bstack1111_opy_
  if name in [bstackl_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧి"), bstackl_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩీ")]:
    bstack1111_opy_(self, name, context, *args)
  if name == bstackl_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩు"):
    try:
      bstack111lll11_opy_ = str(self.feature.name)
      bstack1ll1ll_opy_(context, bstack111lll11_opy_)
      context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧూ") + json.dumps(bstack111lll11_opy_) + bstackl_opy_ (u"ࠪࢁࢂ࠭ృ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫౄ").format(str(e)))
  if name == bstackl_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ౅"):
    try:
      if not hasattr(self, bstackl_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨె")):
        self.driver_before_scenario = True
      bstack1llll1ll1_opy_ = args[0].name
      bstack1l11l111_opy_ = bstack111lll11_opy_ = str(self.feature.name)
      bstack111lll11_opy_ = bstack1l11l111_opy_ + bstackl_opy_ (u"ࠧࠡ࠯ࠣࠫే") + bstack1llll1ll1_opy_
      if self.driver_before_scenario:
        bstack1ll1ll_opy_(context, bstack111lll11_opy_)
        context.browser.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ై") + json.dumps(bstack111lll11_opy_) + bstackl_opy_ (u"ࠩࢀࢁࠬ౉"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫొ").format(str(e)))
  if name == bstackl_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬో"):
    try:
      bstack11111l11_opy_ = args[0].status.name
      if str(bstack11111l11_opy_).lower() == bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬౌ"):
        bstack11l1111l_opy_ = bstackl_opy_ (u"్࠭ࠧ")
        bstack1lllllll1_opy_ = bstackl_opy_ (u"ࠧࠨ౎")
        bstack1l1l11lll_opy_ = bstackl_opy_ (u"ࠨࠩ౏")
        try:
          import traceback
          bstack11l1111l_opy_ = self.exception.__class__.__name__
          bstack1ll1llll1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1lllllll1_opy_ = bstackl_opy_ (u"ࠩࠣࠫ౐").join(bstack1ll1llll1_opy_)
          bstack1l1l11lll_opy_ = bstack1ll1llll1_opy_[-1]
        except Exception as e:
          logger.debug(bstack1ll1l1lll_opy_.format(str(e)))
        bstack11l1111l_opy_ += bstack1l1l11lll_opy_
        bstack11ll1111_opy_(context, json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤ౑") + str(bstack1lllllll1_opy_)), bstackl_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ౒"))
        if self.driver_before_scenario:
          bstack1ll11_opy_(context, bstackl_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ౓"), bstack11l1111l_opy_)
        context.browser.execute_script(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ౔") + json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨౕ") + str(bstack1lllllll1_opy_)) + bstackl_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨౖ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ౗") + json.dumps(bstackl_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢౘ") + str(bstack11l1111l_opy_)) + bstackl_opy_ (u"ࠫࢂࢃࠧౙ"))
      else:
        bstack11ll1111_opy_(context, bstackl_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨౚ"), bstackl_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ౛"))
        if self.driver_before_scenario:
          bstack1ll11_opy_(context, bstackl_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ౜"))
        context.browser.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ౝ") + json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨ౞")) + bstackl_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩ౟"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧࡶࡡࡴࡵࡨࡨࠧࢃࡽࠨౠ"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧౡ").format(str(e)))
  if name == bstackl_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ౢ"):
    try:
      if context.failed is True:
        bstack1lllll111_opy_ = []
        bstack11l11_opy_ = []
        bstack1ll1111ll_opy_ = []
        bstack11l1ll11_opy_ = bstackl_opy_ (u"ࠧࠨౣ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1lllll111_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1ll1llll1_opy_ = traceback.format_tb(exc_tb)
            bstack1ll1l1111_opy_ = bstackl_opy_ (u"ࠨࠢࠪ౤").join(bstack1ll1llll1_opy_)
            bstack11l11_opy_.append(bstack1ll1l1111_opy_)
            bstack1ll1111ll_opy_.append(bstack1ll1llll1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll1l1lll_opy_.format(str(e)))
        bstack11l1111l_opy_ = bstackl_opy_ (u"ࠩࠪ౥")
        for i in range(len(bstack1lllll111_opy_)):
          bstack11l1111l_opy_ += bstack1lllll111_opy_[i] + bstack1ll1111ll_opy_[i] + bstackl_opy_ (u"ࠪࡠࡳ࠭౦")
        bstack11l1ll11_opy_ = bstackl_opy_ (u"ࠫࠥ࠭౧").join(bstack11l11_opy_)
        if not self.driver_before_scenario:
          bstack11ll1111_opy_(context, bstack11l1ll11_opy_, bstackl_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ౨"))
          bstack1ll11_opy_(context, bstackl_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ౩"), bstack11l1111l_opy_)
          context.browser.execute_script(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ౪") + json.dumps(bstack11l1ll11_opy_) + bstackl_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ౫"))
          context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ౬") + json.dumps(bstackl_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣ౭") + str(bstack11l1111l_opy_)) + bstackl_opy_ (u"ࠫࢂࢃࠧ౮"))
      else:
        if not self.driver_before_scenario:
          bstack11ll1111_opy_(context, bstackl_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ౯") + str(self.feature.name) + bstackl_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ౰"), bstackl_opy_ (u"ࠢࡪࡰࡩࡳࠧ౱"))
          bstack1ll11_opy_(context, bstackl_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ౲"))
          context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ౳") + json.dumps(bstackl_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨ౴") + str(self.feature.name) + bstackl_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨ౵")) + bstackl_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ౶"))
          context.browser.execute_script(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪ౷"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ౸").format(str(e)))
  if name in [bstackl_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ౹"), bstackl_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ౺")]:
    bstack1111_opy_(self, name, context, *args)
def bstack11ll1lll_opy_(config, startdir):
  return bstackl_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣ౻").format(bstackl_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥ౼"))
class Notset:
  def __repr__(self):
    return bstackl_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢ౽")
notset = Notset()
def bstack11111l1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11ll1l1l_opy_
  if str(name).lower() == bstackl_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭౾"):
    return bstackl_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ౿")
  else:
    return bstack11ll1l1l_opy_(self, name, default, skip)
def bstack1l1lll1ll_opy_(bstack11l11lll_opy_):
  global bstack11ll11_opy_
  bstack11ll11_opy_ = bstack11l11lll_opy_
  logger.info(bstack1ll1l11l_opy_.format(bstack11ll11_opy_.split(bstackl_opy_ (u"ࠨ࠯ࠪಀ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    logger.warn(bstack1l1lll111_opy_ + str(e))
  Service.start = bstack11ll11ll_opy_
  Service.stop = bstack1lll1l1l1_opy_
  webdriver.Remote.__init__ = bstack1l1l11l1l_opy_
  webdriver.Remote.get = bstack1l1l1ll11_opy_
  WebDriver.close = bstack1llll111_opy_
  bstack1l11ll1l_opy_()
  if bstack1ll1l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1111l11_opy_
    except Exception as e:
      logger.error(bstack1l1ll1l_opy_.format(str(e)))
  if (bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨಁ") in str(bstack11l11lll_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1lll1lll_opy_
      except Exception as e:
        logger.warn(bstack1l1ll1_opy_ + str(e))
    except Exception as e:
      bstack1llll1_opy_(e, bstack1l1ll1_opy_)
    Output.end_test = bstack11l1l11l_opy_
    TestStatus.__init__ = bstack1l1l1l11_opy_
    QueueItem.__init__ = bstack1l1llll11_opy_
    pabot._create_items = bstack1l1ll1111_opy_
    try:
      from pabot import __version__ as bstack1l1l11ll_opy_
      if version.parse(bstack1l1l11ll_opy_) >= version.parse(bstackl_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪಂ")):
        pabot._run = bstack11ll_opy_
      elif version.parse(bstack1l1l11ll_opy_) >= version.parse(bstackl_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫಃ")):
        pabot._run = bstack1l1lll1l1_opy_
      else:
        pabot._run = bstack11l1lll_opy_
    except Exception as e:
      pabot._run = bstack11l1lll_opy_
    pabot._create_command_for_execution = bstack1lll1l11_opy_
    pabot._report_results = bstack111ll_opy_
  if bstackl_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ಄") in str(bstack11l11lll_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1llll1_opy_(e, bstack1ll11l1l_opy_)
    Runner.run_hook = bstack111l1l_opy_
    Step.run = bstack1l1111l1_opy_
  if bstackl_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ಅ") in str(bstack11l11lll_opy_).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
    except Exception as e:
      bstack1llll1_opy_(e, bstack1llll11_opy_)
    pytest_selenium.pytest_report_header = bstack11ll1lll_opy_
    Config.getoption = bstack11111l1_opy_
def bstack1ll11lll_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧಆ") in CONFIG and int(CONFIG[bstackl_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨಇ")]) > 1:
    logger.warn(bstack1l111111_opy_)
def bstack1lllll_opy_(bstack11ll1_opy_, index):
  bstack1l1lll1ll_opy_(bstack11llll1_opy_)
  exec(open(bstack11ll1_opy_).read())
def bstack1lll1l1ll_opy_(arg):
  global CONFIG
  bstack1l1lll1ll_opy_(bstack1lll11111_opy_)
  os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪಈ")] = CONFIG[bstackl_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬಉ")]
  os.environ[bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧಊ")] = CONFIG[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨಋ")]
  from _pytest.config import main as bstack1l1ll11l_opy_
  bstack1l1ll11l_opy_(arg)
def bstack111ll1_opy_(arg):
  bstack1l1lll1ll_opy_(bstack11lll_opy_)
  from behave.__main__ import main as bstack1lll1l111_opy_
  bstack1lll1l111_opy_(arg)
def bstack111111_opy_():
  logger.info(bstack1llll11l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstackl_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬಌ"), help=bstackl_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࠨ಍"))
  parser.add_argument(bstackl_opy_ (u"ࠨ࠯ࡸࠫಎ"), bstackl_opy_ (u"ࠩ࠰࠱ࡺࡹࡥࡳࡰࡤࡱࡪ࠭ಏ"), help=bstackl_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡶࡵࡨࡶࡳࡧ࡭ࡦࠩಐ"))
  parser.add_argument(bstackl_opy_ (u"ࠫ࠲ࡱࠧ಑"), bstackl_opy_ (u"ࠬ࠳࠭࡬ࡧࡼࠫಒ"), help=bstackl_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠧಓ"))
  parser.add_argument(bstackl_opy_ (u"ࠧ࠮ࡨࠪಔ"), bstackl_opy_ (u"ࠨ࠯࠰ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ಕ"), help=bstackl_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨಖ"))
  bstack1ll1lll1_opy_ = parser.parse_args()
  try:
    bstack1ll11llll_opy_ = bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡳ࡫ࡲࡪࡥ࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧಗ")
    if bstack1ll1lll1_opy_.framework and bstack1ll1lll1_opy_.framework not in (bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫಘ"), bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ಙ")):
      bstack1ll11llll_opy_ = bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬಚ")
    bstack1lll11l11_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll11llll_opy_)
    bstack1llll1ll_opy_ = open(bstack1lll11l11_opy_, bstackl_opy_ (u"ࠧࡳࠩಛ"))
    bstack111111l_opy_ = bstack1llll1ll_opy_.read()
    bstack1llll1ll_opy_.close()
    if bstack1ll1lll1_opy_.username:
      bstack111111l_opy_ = bstack111111l_opy_.replace(bstackl_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨಜ"), bstack1ll1lll1_opy_.username)
    if bstack1ll1lll1_opy_.key:
      bstack111111l_opy_ = bstack111111l_opy_.replace(bstackl_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫಝ"), bstack1ll1lll1_opy_.key)
    if bstack1ll1lll1_opy_.framework:
      bstack111111l_opy_ = bstack111111l_opy_.replace(bstackl_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫಞ"), bstack1ll1lll1_opy_.framework)
    file_name = bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧಟ")
    file_path = os.path.abspath(file_name)
    bstack1111lll_opy_ = open(file_path, bstackl_opy_ (u"ࠬࡽࠧಠ"))
    bstack1111lll_opy_.write(bstack111111l_opy_)
    bstack1111lll_opy_.close()
    logger.info(bstack111ll1ll_opy_)
    try:
      os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨಡ")] = bstack1ll1lll1_opy_.framework if bstack1ll1lll1_opy_.framework != None else bstackl_opy_ (u"ࠢࠣಢ")
      config = yaml.safe_load(bstack111111l_opy_)
      config[bstackl_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨಣ")] = bstackl_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡶࡩࡹࡻࡰࠨತ")
      bstack1l1111ll_opy_(bstack1l111l11_opy_, config)
    except Exception as e:
      logger.debug(bstack11lll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1llll1l11_opy_.format(str(e)))
def bstack1l1111ll_opy_(bstack1l1l1l1ll_opy_, config, bstack1llll_opy_ = {}):
  global bstack1111l111_opy_
  if not config:
    return
  bstack1llll1l1l_opy_ = bstack1ll11ll1_opy_ if not bstack1111l111_opy_ else ( bstack1ll1l11_opy_ if bstackl_opy_ (u"ࠪࡥࡵࡶࠧಥ") in config else bstack11l11ll_opy_ )
  data = {
    bstackl_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ದ"): config[bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧಧ")],
    bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩನ"): config[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ಩")],
    bstackl_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬಪ"): bstack1l1l1l1ll_opy_,
    bstackl_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬಫ"): {
      bstackl_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨಬ"): str(config[bstackl_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫಭ")]) if bstackl_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬಮ") in config else bstackl_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢಯ"),
      bstackl_opy_ (u"ࠧࡳࡧࡩࡩࡷࡸࡥࡳࠩರ"): bstack11l1lll1_opy_(os.getenv(bstackl_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥಱ"), bstackl_opy_ (u"ࠤࠥಲ"))),
      bstackl_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬಳ"): bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ಴"),
      bstackl_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ವ"): bstack1llll1l1l_opy_,
      bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩಶ"): config[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪಷ")]if config[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫಸ")] else bstackl_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥಹ"),
      bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ಺"): str(config[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭಻")]) if bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ಼ࠧ") in config else bstackl_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢಽ"),
      bstackl_opy_ (u"ࠧࡰࡵࠪಾ"): sys.platform,
      bstackl_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪಿ"): socket.gethostname()
    }
  }
  update(data[bstackl_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬೀ")], bstack1llll_opy_)
  try:
    response = bstack1l1llllll_opy_(bstackl_opy_ (u"ࠪࡔࡔ࡙ࡔࠨು"), bstack1l1l11_opy_, data, config)
    if response:
      logger.debug(bstack11l1llll_opy_.format(bstack1l1l1l1ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l11lll_opy_.format(str(e)))
def bstack1l1llllll_opy_(type, url, data, config):
  bstack11ll11l_opy_ = bstack1llllll1_opy_.format(url)
  proxy = bstack11llllll_opy_(config)
  proxies = {}
  response = {}
  if config.get(bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧೂ")):
    proxies = {
      bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫೃ"): proxy
    }
  if config.get(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪೄ")):
    proxies = {
      bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭೅"): proxy
    }
  if type == bstackl_opy_ (u"ࠨࡒࡒࡗ࡙࠭ೆ"):
    response = requests.post(bstack11ll11l_opy_, json=data,
                    headers={bstackl_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨೇ"): bstackl_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ೈ")}, auth=(config[bstackl_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭೉")], config[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨೊ")]), proxies=proxies)
  return response
def bstack11l1lll1_opy_(framework):
  return bstackl_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥೋ").format(str(framework), __version__) if framework else bstackl_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣೌ").format(__version__)
def bstack11lll1l1_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  bstack1lll11_opy_()
  logger.debug(bstack1lll11l1l_opy_.format(str(CONFIG)))
  bstack1ll111_opy_()
  sys.excepthook = bstack111l1l1l_opy_
  atexit.register(bstack1ll11l11l_opy_)
  signal.signal(signal.SIGINT, bstack111l1lll_opy_)
  signal.signal(signal.SIGTERM, bstack111l1lll_opy_)
def bstack111l1l1l_opy_(exctype, value, traceback):
  bstack1l1ll111_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
def bstack1l1ll111_opy_(message = bstackl_opy_ (u"ࠨ್ࠩ")):
  global CONFIG
  try:
    if message:
      bstack1llll_opy_ = {
        bstackl_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ೎"): str(message)
      }
      bstack1l1111ll_opy_(bstack11111ll_opy_, CONFIG, bstack1llll_opy_)
    else:
      bstack1l1111ll_opy_(bstack11111ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll1l1l1l_opy_.format(str(e)))
def bstack11l1l_opy_(bstack1l1l1lll_opy_, size):
  bstack111ll11_opy_ = []
  while len(bstack1l1l1lll_opy_) > size:
    bstack111l_opy_ = bstack1l1l1lll_opy_[:size]
    bstack111ll11_opy_.append(bstack111l_opy_)
    bstack1l1l1lll_opy_   = bstack1l1l1lll_opy_[size:]
  bstack111ll11_opy_.append(bstack1l1l1lll_opy_)
  return bstack111ll11_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack1llll1111_opy_)
    return
  if sys.argv[1] == bstackl_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭೏")  or sys.argv[1] == bstackl_opy_ (u"ࠫ࠲ࡼࠧ೐"):
    logger.info(bstackl_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬ೑").format(__version__))
    return
  if sys.argv[1] == bstackl_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ೒"):
    bstack111111_opy_()
    return
  args = sys.argv
  bstack11lll1l1_opy_()
  global CONFIG
  global bstack1lll1llll_opy_
  global bstack11111lll_opy_
  global bstack1l1l111ll_opy_
  global bstack11l1l1_opy_
  global bstack11llll_opy_
  bstack1l1l1l1l_opy_ = bstackl_opy_ (u"ࠧࠨ೓")
  if args[1] == bstackl_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ೔") or args[1] == bstackl_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪೕ"):
    bstack1l1l1l1l_opy_ = bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪೖ")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ೗"):
    bstack1l1l1l1l_opy_ = bstackl_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ೘")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ೙"):
    bstack1l1l1l1l_opy_ = bstackl_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭೚")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ೛"):
    bstack1l1l1l1l_opy_ = bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ೜")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪೝ"):
    bstack1l1l1l1l_opy_ = bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫೞ")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ೟"):
    bstack1l1l1l1l_opy_ = bstackl_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ೠ")
    args = args[2:]
  else:
    if not bstackl_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪೡ") in CONFIG or str(CONFIG[bstackl_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫೢ")]).lower() in [bstackl_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩೣ"), bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ೤")]:
      bstack1l1l1l1l_opy_ = bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ೥")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ೦")]).lower() == bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ೧"):
      bstack1l1l1l1l_opy_ = bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭೨")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ೩")]).lower() == bstackl_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ೪"):
      bstack1l1l1l1l_opy_ = bstackl_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ೫")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ೬")]).lower() == bstackl_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ೭"):
      bstack1l1l1l1l_opy_ = bstackl_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭೮")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೯")]).lower() == bstackl_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ೰"):
      bstack1l1l1l1l_opy_ = bstackl_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩೱ")
      args = args[1:]
    else:
      os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬೲ")] = bstack1l1l1l1l_opy_
      bstack1l1ll1ll_opy_(bstack1l1ll1ll1_opy_)
  global bstack1llll1l_opy_
  try:
    os.environ[bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ೳ")] = bstack1l1l1l1l_opy_
    bstack1l1111ll_opy_(bstack111l1l11_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll1l1l1l_opy_.format(str(e)))
  global bstack111ll1l1_opy_
  global bstack1llllll_opy_
  global bstack1ll1ll11l_opy_
  global bstack1llll11l1_opy_
  global bstack1111111_opy_
  global bstack1l1ll11_opy_
  global bstack11l111l1_opy_
  global bstack1ll1l1l_opy_
  global bstack1111_opy_
  global bstack11lll1l_opy_
  global bstack1l1ll11ll_opy_
  global bstack1l1lll_opy_
  global bstack11ll1l1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    logger.warn(bstack1l1lll111_opy_ + str(e))
  bstack111ll1l1_opy_ = webdriver.Remote.__init__
  bstack1ll1l1l_opy_ = WebDriver.close
  try:
    import Browser
    from subprocess import Popen
    bstack1llll1l_opy_ = Popen.__init__
  except Exception as e:
    logger.debug(bstack1ll111l1_opy_ + str(e))
  bstack1l1ll11ll_opy_ = WebDriver.get
  if bstack111l11l1_opy_():
    if bstack11lllll1_opy_() < version.parse(bstack1l1lll11l_opy_):
      logger.error(bstack1lll11lll_opy_.format(bstack11lllll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1lll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l1ll1l_opy_.format(str(e)))
  if (bstack1l1l1l1l_opy_ in [bstackl_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ೴"), bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ೵"), bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ೶")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1lll1lll_opy_
      except Exception as e:
        logger.warn(bstack1l1ll1_opy_ + str(e))
    except Exception as e:
      bstack1llll1_opy_(e, bstack1l1ll1_opy_)
    bstack1llllll_opy_ = Output.end_test
    bstack1ll1ll11l_opy_ = TestStatus.__init__
    bstack1111111_opy_ = pabot._run
    bstack1l1ll11_opy_ = QueueItem.__init__
    bstack11l111l1_opy_ = pabot._create_command_for_execution
  if bstack1l1l1l1l_opy_ == bstackl_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ೷"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1llll1_opy_(e, bstack1ll11l1l_opy_)
    bstack1111_opy_ = Runner.run_hook
    bstack11lll1l_opy_ = Step.run
  if bstack1l1l1l1l_opy_ == bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ೸"):
    try:
      from _pytest.config import Config
    except Exception as e:
      bstack1llll1_opy_(e, bstack1llll11_opy_)
    bstack11ll1l1l_opy_ = Config.getoption
  if bstack1l1l1l1l_opy_ == bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ೹"):
    bstack1l1lll1_opy_()
    bstack1ll11lll_opy_()
    if bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ೺") in CONFIG:
      bstack11111lll_opy_ = True
      bstack11l1l1ll_opy_ = []
      for index, platform in enumerate(CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ೻")]):
        bstack11l1l1ll_opy_.append(threading.Thread(name=str(index),
                                      target=bstack1lllll_opy_, args=(args[0], index)))
      for t in bstack11l1l1ll_opy_:
        t.start()
      for t in bstack11l1l1ll_opy_:
        t.join()
    else:
      bstack1l1lll1ll_opy_(bstack11llll1_opy_)
      exec(open(args[0]).read())
  elif bstack1l1l1l1l_opy_ == bstackl_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ೼") or bstack1l1l1l1l_opy_ == bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭೽"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1llll1_opy_(e, bstack1l1ll1_opy_)
    bstack1l1lll1_opy_()
    bstack1l1lll1ll_opy_(bstack1111ll11_opy_)
    if bstackl_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭೾") in args:
      i = args.index(bstackl_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ೿"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1lll1llll_opy_))
    args.insert(0, str(bstackl_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨഀ")))
    pabot.main(args)
  elif bstack1l1l1l1l_opy_ == bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬഁ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1llll1_opy_(e, bstack1l1ll1_opy_)
    for a in args:
      if bstackl_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫം") in a:
        bstack1l1l111ll_opy_ = int(a.split(bstackl_opy_ (u"࠭࠺ࠨഃ"))[1])
      if bstackl_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫഄ") in a:
        bstack11l1l1_opy_ = str(a.split(bstackl_opy_ (u"ࠨ࠼ࠪഅ"))[1])
      if bstackl_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩആ") in a:
        bstack11llll_opy_ = str(a.split(bstackl_opy_ (u"ࠪ࠾ࠬഇ"))[1])
    bstack1l1lll1ll_opy_(bstack1111ll11_opy_)
    run_cli(args)
  elif bstack1l1l1l1l_opy_ == bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫഈ"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      import importlib
      bstack11lll1ll_opy_ = importlib.find_loader(bstackl_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧഉ"))
      if bstack11lll1ll_opy_ is None:
        bstack1llll1_opy_(e, bstack1llll11_opy_)
    except Exception as e:
      bstack1llll1_opy_(e, bstack1llll11_opy_)
    bstack1l1lll1_opy_()
    try:
      if bstackl_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨഊ") in args:
        i = args.index(bstackl_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩഋ"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫഌ") in args:
        i = args.index(bstackl_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬ഍"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠪ࠱ࡵ࠭എ") in args:
        i = args.index(bstackl_opy_ (u"ࠫ࠲ࡶࠧഏ"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ഐ") in args:
        i = args.index(bstackl_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ഑"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠧ࠮ࡰࠪഒ") in args:
        i = args.index(bstackl_opy_ (u"ࠨ࠯ࡱࠫഓ"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1l11ll11_opy_ = config.args
    bstack11ll11l1_opy_ = config.invocation_params.args
    bstack11ll11l1_opy_ = list(bstack11ll11l1_opy_)
    bstack1ll1ll11_opy_ = []
    for arg in bstack11ll11l1_opy_:
      for spec in bstack1l11ll11_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack1ll1ll11_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstackl_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪഔ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l11ll11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l111lll_opy_)))
                    for bstack1l111lll_opy_ in bstack1l11ll11_opy_]
    bstack1ll1ll11_opy_.append(bstackl_opy_ (u"ࠪ࠱ࡵ࠭ക"))
    bstack1ll1ll11_opy_.append(bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩഖ"))
    bstack1ll1ll11_opy_.append(bstackl_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧഗ"))
    bstack1ll1ll11_opy_.append(bstackl_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ഘ"))
    bstack11lllll_opy_ = []
    for spec in bstack1l11ll11_opy_:
      bstack11ll1l1_opy_ = []
      bstack11ll1l1_opy_.append(spec)
      bstack11ll1l1_opy_ += bstack1ll1ll11_opy_
      bstack11lllll_opy_.append(bstack11ll1l1_opy_)
    bstack11111lll_opy_ = True
    bstack1l1l1ll1_opy_ = 1
    if bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧങ") in CONFIG:
      bstack1l1l1ll1_opy_ = CONFIG[bstackl_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨച")]
    bstack1l11l1_opy_ = int(bstack1l1l1ll1_opy_)*int(len(CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬഛ")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ജ")]):
      for bstack11ll1l1_opy_ in bstack11lllll_opy_:
        item = {}
        item[bstackl_opy_ (u"ࠫࡦࡸࡧࠨഝ")] = bstack11ll1l1_opy_
        item[bstackl_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫഞ")] = index
        execution_items.append(item)
    bstack111l111l_opy_ = bstack11l1l_opy_(execution_items, bstack1l11l1_opy_)
    for execution_item in bstack111l111l_opy_:
      bstack11l1l1ll_opy_ = []
      for item in execution_item:
        bstack11l1l1ll_opy_.append(threading.Thread(name=str(item[bstackl_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬട")]),
                                            target=bstack1lll1l1ll_opy_,
                                            args=(item[bstackl_opy_ (u"ࠧࡢࡴࡪࠫഠ")],)))
      for t in bstack11l1l1ll_opy_:
        t.start()
      for t in bstack11l1l1ll_opy_:
        t.join()
  elif bstack1l1l1l1l_opy_ == bstackl_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨഡ"):
    try:
      from behave.__main__ import main as bstack1lll1l111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1llll1_opy_(e, bstack1ll11l1l_opy_)
    bstack1l1lll1_opy_()
    bstack11111lll_opy_ = True
    bstack1l1l1ll1_opy_ = 1
    if bstackl_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩഢ") in CONFIG:
      bstack1l1l1ll1_opy_ = CONFIG[bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪണ")]
    bstack1l11l1_opy_ = int(bstack1l1l1ll1_opy_)*int(len(CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧത")]))
    config = Configuration(args)
    bstack1l11ll11_opy_ = config.paths
    bstack1lll111_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack1l11ll11_opy_:
        bstack1lll111_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstackl_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭ഥ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l11ll11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l111lll_opy_)))
                    for bstack1l111lll_opy_ in bstack1l11ll11_opy_]
    bstack11lllll_opy_ = []
    for spec in bstack1l11ll11_opy_:
      bstack11ll1l1_opy_ = []
      bstack11ll1l1_opy_ += bstack1lll111_opy_
      bstack11ll1l1_opy_.append(spec)
      bstack11lllll_opy_.append(bstack11ll1l1_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩദ")]):
      for bstack11ll1l1_opy_ in bstack11lllll_opy_:
        item = {}
        item[bstackl_opy_ (u"ࠧࡢࡴࡪࠫധ")] = bstackl_opy_ (u"ࠨࠢࠪന").join(bstack11ll1l1_opy_)
        item[bstackl_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨഩ")] = index
        execution_items.append(item)
    bstack111l111l_opy_ = bstack11l1l_opy_(execution_items, bstack1l11l1_opy_)
    for execution_item in bstack111l111l_opy_:
      bstack11l1l1ll_opy_ = []
      for item in execution_item:
        bstack11l1l1ll_opy_.append(threading.Thread(name=str(item[bstackl_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩപ")]),
                                            target=bstack111ll1_opy_,
                                            args=(item[bstackl_opy_ (u"ࠫࡦࡸࡧࠨഫ")],)))
      for t in bstack11l1l1ll_opy_:
        t.start()
      for t in bstack11l1l1ll_opy_:
        t.join()
  else:
    bstack1l1ll1ll_opy_(bstack1l1ll1ll1_opy_)
  bstack1l11llll1_opy_()
def bstack1l11llll1_opy_():
  global CONFIG
  try:
    if bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨബ") in CONFIG:
      host = bstackl_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩഭ") if bstackl_opy_ (u"ࠧࡢࡲࡳࠫമ") in CONFIG else bstackl_opy_ (u"ࠨࡣࡳ࡭ࠬയ")
      user = CONFIG[bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫര")]
      key = CONFIG[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭റ")]
      bstack1llll1lll_opy_ = bstackl_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪല") if bstackl_opy_ (u"ࠬࡧࡰࡱࠩള") in CONFIG else bstackl_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨഴ")
      url = bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠰࡭ࡷࡴࡴࠧവ").format(user, key, host, bstack1llll1lll_opy_)
      headers = {
        bstackl_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧശ"): bstackl_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬഷ"),
      }
      if bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬസ") in CONFIG:
        params = {bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩഹ"):CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨഺ")], bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ഻ࠩ"):CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ഼ࠩ")]}
      else:
        params = {bstackl_opy_ (u"ࠨࡰࡤࡱࡪ࠭ഽ"):CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬാ")]}
      response = requests.get(url, params=params, headers=headers)
      if response.json():
        bstack11l1l1l1_opy_ = response.json()[0][bstackl_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡣࡷ࡬ࡰࡩ࠭ി")]
        if bstack11l1l1l1_opy_:
          bstack1l11ll1l1_opy_ = bstack11l1l1l1_opy_[bstackl_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨീ")].split(bstackl_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧ࠲ࡨࡵࡪ࡮ࡧࠫു"))[0] + bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠵ࠧൂ") + bstack11l1l1l1_opy_[bstackl_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪൃ")]
          logger.info(bstack1llll111l_opy_.format(bstack1l11ll1l1_opy_))
          bstack1lll111l1_opy_ = CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫൄ")]
          if bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൅") in CONFIG:
            bstack1lll111l1_opy_ += bstackl_opy_ (u"ࠪࠤࠬെ") + CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭േ")]
          if bstack1lll111l1_opy_!= bstack11l1l1l1_opy_[bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪൈ")]:
            logger.debug(bstack11ll111_opy_.format(bstack11l1l1l1_opy_[bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ൉")], bstack1lll111l1_opy_))
    else:
      logger.warn(bstack1ll11l111_opy_)
  except Exception as e:
    logger.debug(bstack1ll1l1l1_opy_.format(str(e)))
def bstack1l1ll1l1_opy_(url, bstack1l11_opy_=False):
  global CONFIG
  global bstack1111lll1_opy_
  if not bstack1111lll1_opy_:
    hostname = bstack1111llll_opy_(url)
    is_private = bstack1ll11l1_opy_(hostname)
    if (bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫൊ") in CONFIG and not CONFIG[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬോ")]) and (is_private or bstack1l11_opy_):
      bstack1111lll1_opy_ = hostname
def bstack1111llll_opy_(url):
  return urlparse(url).hostname
def bstack1ll11l1_opy_(hostname):
  for bstack1ll1l11l1_opy_ in bstack111l11l_opy_:
    regex = re.compile(bstack1ll1l11l1_opy_)
    if regex.match(hostname):
      return True
  return False