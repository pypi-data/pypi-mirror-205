# dm_ret = dm.BindWindowEx(hwnd,"dx.graphic.opengl","dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor","windows","dx.public.active.api|dx.public.active.message|dx.public.hide.dll|dx.public.active.api2|dx.public.anti.api|dx.public.km.protect|dx.public.inject.super|dx.public.memory|dx.public.inject.c",11)

import win32com.client
from win32com.client import Dispatch
import ctypes

dm = win32com.client.Dispatch('dm.dmsoft')  # 必须是32位python解释器才能调用
print(dm.ver())

#免注册调用方法
# import ctypes
# import os
# from comtypes.client import CreateObject
# import win32com.client
#
# try:
#     dm = win32com.client.Dispatch('dm.dmsoft')
#     print('本机系统中已经安装大漠插件，版本为:', dm.ver())
# except:
#     print('本机并未安装大漠，正在免注册调用')
#     dms = ctypes.windll.LoadLibrary('C://Users/DmReg.dll')
#     location_dmreg = 'C://Users/dm.dll'
#     dms.SetDllPathW(location_dmreg, 0)
#     dm = CreateObject('dm.dmsoft')
#     print('免注册调用成功 版本号为:',dm.Ver())
