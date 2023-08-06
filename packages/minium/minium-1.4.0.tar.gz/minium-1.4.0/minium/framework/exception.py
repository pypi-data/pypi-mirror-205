#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Author:         lockerzhang
Filename:       exception.py
Create time:    2020/4/22 22:13
Description:

"""
import minium.miniprogram.base_driver.minium_log as minum_log
import time


class MiniError(Exception):
    def __init__(self, msg):  # real signature unknown
        ep_data = {}
        ep_data["TimeStamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ep_data["Type"] = str(self.__class__.__name__)
        ep_data["Args"] = msg
        ep_data["Trace"] = ""
        minum_log.report_exception(ep_data)
        Exception.__init__(self, msg)


class MiniConnectError(MiniError):
    ...


class MiniConnectSvrError(MiniConnectError):
    ...


class MiniReConnectSvrError(MiniConnectSvrError):
    ...


class MiniTimeoutError(MiniConnectError):
    ...


# 链接断了
class MiniConnectionClosedError(MiniConnectError):
    ...


# 小程序下线了
class MiniClientOfflineError(MiniConnectError):
    ...


# 调试通道错误
class MiniDebugConnectionError(MiniConnectError):
    ...

# 因断连造成的未收到指令回复
class MiniTimeoutCauseByConnectionBreakError(
    MiniTimeoutError, MiniConnectionClosedError
):
    ...


# 因小程序下线造成的未收到指令回复
class MiniTimeoutCauseByClientOffline(MiniTimeoutError, MiniClientOfflineError):
    ...


class MiniRefuseError(MiniConnectError):
    ...


class MiniNotAttributeError(AttributeError):
    ...


class MiniLaunchError(MiniError):
    ...


class MiniShutdownError(MiniError):
    ...


class MiniConfigError(MiniError):
    ...


class MiniAppError(MiniError):
    ...


class MiniLowVersionSdkError(MiniAppError):
    ...


class MiniObserverError(MiniError):
    ...


class MiniNoncallableError(MiniObserverError):
    ...


class MiniParamsError(Exception):
    ...


class MiniElementNotFoundError(Exception):
    ...


class LoadCaseError(ModuleNotFoundError):
    def __init__(self, *args: object, name: str = ..., path: str = ...) -> None:
        if len(args) > 0 and isinstance(args[0], ModuleNotFoundError):
            err = args[0]
            super().__init__(err.msg, *args[1:], name=err.name, path=err.path)
            self.with_traceback(err.__traceback__)
        else:
            super().__init__(*args, name=name, path=path)

class RemoteDebugConnectionLost(MiniAppError):  # 远程调试服务掉线
    ...
