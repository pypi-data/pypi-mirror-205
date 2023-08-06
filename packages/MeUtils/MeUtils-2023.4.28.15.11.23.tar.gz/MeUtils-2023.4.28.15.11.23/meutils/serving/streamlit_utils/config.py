#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : config
# @Time         : 2023/4/26 10:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

import streamlit as st


def st_init_conf(conf):
    """
    class Conf(BaseConfig):
        embedding = 'shibing624/text2vec-base-chinese'
    conf = Conf()

    """

    for k, v in conf:  # 更新配置
        setattr(conf, k, st.sidebar.text_input(label=k, value=v))  # todo设置入参方式
    return conf
