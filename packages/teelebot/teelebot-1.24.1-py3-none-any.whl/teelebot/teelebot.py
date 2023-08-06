# -*- coding:utf-8 -*-
"""
@description:基于Telegram Bot Api 的机器人框架
@creation date: 2019-08-13
@last modification: 2023-04-28
@author: Pluto (github:plutobell)
@version: 1.24.1
"""
import inspect
import time
import sys
import os
import json
import string
import random
import shutil
import importlib
import threading

from pathlib import Path
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor

from .handler import _config, _bridge, _plugin_info
from .logger import _logger
from .schedule import _Schedule
from .buffer import _Buffer
from .request import _Request


class Bot(object):
    """机器人的基类"""

    def __init__(self, key=""):
        config = _config()

        if key != "":
            self._key = key
        elif key == "":
            self._key = config["key"]
        
        self.__proxies = config["proxies"]

        self._cloud_api_server = config["cloud_api_server"]
        self._local_api_server = config["local_api_server"]
        if self._local_api_server != "False":
            self._basic_url = config["local_api_server"]
        else:
            self._basic_url = self._cloud_api_server
        self._url = self._basic_url + r"bot" + self._key + r"/"

        self._webhook = config["webhook"]
        if self._webhook:
            self._self_signed = config["self_signed"]
            self._cert_key = config["cert_key"]
            self._cert_pub = config["cert_pub"]
            self._server_address = config["server_address"]
            self._server_port = config["server_port"]
            self._local_address = config["local_address"]
            self._local_port = config["local_port"]
            self._secret_token = self.__make_token()
        self._offset = 0
        self._timeout = 60
        self._debug = config["debug"]
        self._pool_size = config["pool_size"]
        self._buffer_size = config["buffer_size"]
        self._drop_pending_updates = config["drop_pending_updates"]
        self._updates_chat_member = config["updates_chat_member"]
        self._allowed_updates = []
        if self._updates_chat_member:
            self._allowed_updates = [
                "update_id",
                "message",
                "edited_message",
                "channel_post",
                "edited_channel_post",
                "inline_query",
                "chosen_inline_result",
                "callback_query",
                "shipping_query",
                "pre_checkout_query",
                "poll",
                "poll_answer",
                "my_chat_member",
                "chat_member",
                "chat_join_request"
            ]

        self.__root_id = config["root_id"]
        self.__bot_id = self._key.split(":")[0]
        self.__common_pkg_prefix = config["common_pkg_prefix"]
        self.__inline_mode_prefix = config["inline_mode_prefix"]
        self.__AUTHOR = config["author"]
        self.__VERSION = config["version"]
        self.__plugin_dir = config["plugin_dir"]
        self.__plugin_bridge = config["plugin_bridge"]
        self.__non_plugin_list = config["non_plugin_list"]
        self.__start_time = int(time.time())
        self.__response_times = 0
        self.__response_chats = []
        self.__response_users = []

        thread_pool_size = round(int(self._pool_size) * 2 / 3)
        schedule_queue_size = int(self._pool_size) - thread_pool_size
        self.request = _Request(thread_pool_size, self._url, self._debug, self.__proxies)
        self.schedule = _Schedule(schedule_queue_size)
        self.buffer = _Buffer(int(self._buffer_size) * 1024 * 1024,
            self.__plugin_bridge.keys(), self.__plugin_dir)

        self.__thread_pool = ThreadPoolExecutor(
            max_workers=thread_pool_size)
        self.__timer_thread_pool = ThreadPoolExecutor(
            max_workers=int(self._pool_size) * 5)

        self.__plugin_info = config["plugin_info"]
        self.__non_plugin_info = config["non_plugin_info"]

        del config
        del thread_pool_size
        del schedule_queue_size

    def __del__(self):
        self.__thread_pool.shutdown(wait=True)
        self.__timer_thread_pool.shutdown(wait=True)
        del self.request
        del self.schedule

    # teelebot method
    def __threadpool_exception(self, fur):
        """
        线程池异常回调
        """
        if fur.exception() is not None:
            os.system("")
            _logger.debug("EXCEPTION" + " - " + str(fur.result()))

    def __import_module(self, plugin_name):
        """
        动态导入模块
        """
        sys.path.append(self.path_converter(self.__plugin_dir + plugin_name + os.sep))
        Module = importlib.import_module(plugin_name)  # 模块检测

        return Module

    def __update_plugin(self, plugin_name, as_plugin=True):
        """
        热更新插件
        """

        if as_plugin:
            plugin_info = self.__plugin_info
        else:
            plugin_info = self.__non_plugin_info

        plugin_uri = self.path_converter(
            self.__plugin_dir + plugin_name + os.sep + plugin_name + ".py")
        now_mtime = os.stat(plugin_uri).st_mtime
        # print(now_mtime, self.__plugin_info[plugin_name])
        if now_mtime != plugin_info[plugin_name]:  # 插件热更新
            if os.path.exists(self.path_converter(self.__plugin_dir + plugin_name + r"/__pycache__")):
                shutil.rmtree(self.path_converter(self.__plugin_dir + plugin_name + r"/__pycache__"))
            plugin_info[plugin_name] = now_mtime
            Module = self.__import_module(plugin_name)
            importlib.reload(Module)
            os.system("")
            _logger.info("The plugin " + plugin_name + " has been updated")

    def __load_plugin(self, now_plugin_info, as_plugin=True,
        now_plugin_bridge={}, now_non_plugin_list=[]):
        """
        动态装载插件
        """
        if as_plugin:
            for plugin in list(now_plugin_bridge.keys()): # 动态装载插件
                if plugin not in list(self.__plugin_bridge.keys()):
                    os.system("")
                    _logger.info("The plugin " + plugin + " has been installed")
                    self.__plugin_info[plugin] = now_plugin_info[plugin]
            for plugin in list(self.__plugin_bridge.keys()):
                if plugin not in list(now_plugin_bridge.keys()):
                    os.system("")
                    _logger.info("The plugin " + plugin + " has been uninstalled")
                    self.__plugin_info.pop(plugin)

                    if (self.__plugin_dir + plugin) in sys.path:
                        sys.modules.pop(self.__plugin_dir + plugin)
                        sys.path.remove(self.__plugin_dir + plugin)

            self.__plugin_bridge = now_plugin_bridge

            self.buffer._update(now_plugin_bridge.keys()) # Buffer动态更新

        else:
            for plugin in list(now_non_plugin_list): # 动态装载非插件包
                if plugin not in list(self.__non_plugin_list):
                    os.system("")
                    _logger.info("The plugin " + plugin + " has been installed")
                    self.__non_plugin_info[plugin] = now_plugin_info[plugin]

                    if (self.__plugin_dir + plugin) not in sys.path:
                        sys.path.append(self.__plugin_dir + plugin)

            for plugin in list(self.__non_plugin_list):
                if plugin not in list(now_non_plugin_list):
                    os.system("")
                    _logger.info("The plugin " + plugin + " has been uninstalled")
                    self.__non_plugin_info.pop(plugin)

                    if (self.__plugin_dir + plugin) in sys.path:
                        sys.modules.pop(self.__plugin_dir + plugin)
                        sys.path.remove(self.__plugin_dir + plugin)

            self.__non_plugin_list = now_non_plugin_list

    def __control_plugin(self, plugin_bridge, chat_type, chat_id):
        if chat_type != "private" and "PluginCTL" in plugin_bridge.keys() \
                and plugin_bridge["PluginCTL"] == "/pluginctl":
            if os.path.exists(self.path_converter(self.__plugin_dir + "PluginCTL/db/" + str(chat_id) + ".db")):
                with open(self.path_converter(self.__plugin_dir + "PluginCTL/db/" + str(chat_id) + ".db"), "r") as f:
                    plugin_setting = f.read().strip()
                plugin_list_off = plugin_setting.split(',')
                plugin_bridge_temp = {}
                for plugin in list(plugin_bridge.keys()):
                    if plugin not in plugin_list_off:
                        plugin_bridge_temp[plugin] = plugin_bridge[plugin]
                plugin_bridge = plugin_bridge_temp

        return plugin_bridge

    def __mark_message_for_pluginRun(self, message):
        if "callback_query_id" in message.keys():  # callback query
            message["message_type"] = "callback_query_data"
            message_type = "callback_query_data"
        elif "query" in message.keys():
            message["message_type"] = "inline_query"
            message_type = "query"
        elif "voice_chat_started" in message.keys():
            message["message_type"] = "voice_started"
            message_type = "voice_started"
            message["voice_started"] = ""
        elif "voice_chat_ended" in message.keys():
            message["message_type"] = "voice_ended"
            message_type = "voice_ended"
            message["voice_ended"] = ""
        elif "voice_chat_participants_invited" in message.keys():
            message["message_type"] = "voice_invited"
            message_type = "voice_invited"
            message["voice_invited"] = ""
        elif "message_auto_delete_timer_changed" in message.keys():
            message["message_type"] = "message__timer_changed"
            message_type = "message__timer_changed"
            message["message__timer_changed"] = ""
        elif "my_chat_member_id" in message.keys():
            message["message_type"] = "my_chat_member_data"
            message_type = "my_chat_member_data"
            message["my_chat_member_data"] = ""
        elif "chat_member_id" in message.keys():
            message["message_type"] = "chat_member_data"
            message_type = "chat_member_data"
            message["chat_member_data"] = ""
        elif "chat_join_request_id" in message.keys():
            message["message_type"] = "chat_join_request_data"
            message_type = "chat_join_request_data"
            message["chat_join_request_data"] = ""
        elif "new_chat_members" in message.keys():
            message["message_type"] = "chat_members"
            message_type = "chat_members"
            message["chat_members"] = ""  # default prefix of command
        elif "left_chat_member" in message.keys():
            message["message_type"] = "left_member"
            message_type = "left_member"
            message["left_member"] = ""
        elif "photo" in message.keys():
            message["message_type"] = "photo"
            message_type = "message_type"
        elif "sticker" in message.keys():
            message["message_type"] = "sticker"
            message_type = "message_type"
        elif "video" in message.keys():
            message["message_type"] = "video"
            message_type = "message_type"
        elif "audio" in message.keys():
            message["message_type"] = "audio"
            message_type = "message_type"
        elif "document" in message.keys():
            message["message_type"] = "document"
            message_type = "message_type"
        elif "text" in message.keys():
            message["message_type"] = "text"
            message_type = "text"
        elif "caption" in message.keys():
            message["message_type"] = "caption"
            message_type = "caption"
        else:
            message["message_type"] = "unknown"
            message_type = "unknown"

        return message_type, message

    def __logging_for_pluginRun(self, message, plugin):
        title = ""  # INFO日志
        user_name = ""

        if message["chat"]["type"] == "private":
            if "first_name" in message["chat"].keys():
                title += message["chat"]["first_name"]
            if "last_name" in message["chat"].keys():
                if "first_name" in message["chat"].keys():
                    title += " " + message["chat"]["last_name"]
                else:
                    title += message["chat"]["last_name"]
        elif "title" in message["chat"].keys():
            title = message["chat"]["title"]
        if "reply_markup" in message.keys() and \
                message["message_type"] == "callback_query_data":
            from_id = message["click_user"]["id"]
            if "first_name" in message["click_user"].keys():
                user_name += message["click_user"]["first_name"]
            if "last_name" in message["click_user"].keys():
                if "first_name" in message["click_user"].keys():
                    user_name += " " + message["click_user"]["last_name"]
                else:
                    user_name += message["chat"]["last_name"]
        else:
            from_id = message["from"]["id"]
            if "first_name" in message["from"].keys():
                user_name += message["from"]["first_name"]
            if "last_name" in message["from"].keys():
                if "first_name" in message["from"].keys():
                    user_name += " " + message["from"]["last_name"]
                else:
                    user_name += message["from"]["last_name"]

        if message["message_type"] == "unknown":
            os.system("")
            _logger.info(
            "From:" + title + "(" + str(message["chat"]["id"]) + ") - " + \
            "User:" + user_name + "(" + str(from_id) + ") - " + \
            "Plugin: " + "" + " - " + \
            "Type:" + message["message_type"])
        else:
            os.system("")
            _logger.info(
                "From:" + title + "(" + str(message["chat"]["id"]) + ") - " + \
                "User:" + user_name + "(" + str(from_id) + ") - " + \
                "Plugin: " + str(plugin) + " - " + \
                "Type:" + message["message_type"])

    def __make_token(self, len=64):
        """
        生成指定长度的token
        """
        if len > 64:
            return "Specified length is too long."
        else:
            token = ''.join(random.sample(string.ascii_letters + string.digits + "-_", 64))
            return token

    def _pluginRun(self, bot, message):
        """
        运行插件
        """
        if message is None:
            return

        now_plugin_bridge, now_non_plugin_list = _bridge(self.__plugin_dir)
        now_plugin_info = _plugin_info(now_plugin_bridge.keys(), self.__plugin_dir)
        now_non_plugin_info = _plugin_info(now_non_plugin_list, self.__plugin_dir)

        if now_plugin_bridge != self.__plugin_bridge: # 动态装载插件
            self.__load_plugin(now_plugin_info=now_plugin_info, now_plugin_bridge=now_plugin_bridge)
        if len(now_plugin_info) != len(self.__plugin_info) or \
            now_plugin_info != self.__plugin_info: # 动态更新插件信息
            for plugin_name in list(self.__plugin_bridge.keys()):
                self.__update_plugin(plugin_name) # 热更新插件

        if now_non_plugin_list != self.__non_plugin_list: # 动态装载非插件包
            self.__load_plugin(now_plugin_info=now_non_plugin_info, as_plugin=False,
                now_non_plugin_list=now_non_plugin_list)
        if len(now_non_plugin_info) != len(self.__non_plugin_info) or \
            now_non_plugin_info != self.__non_plugin_info: # 动态更新非插件包信息
            for plugin_name in list(self.__non_plugin_list):
                self.__update_plugin(plugin_name, as_plugin=False) # 热更新非插件包

        if len(self.__plugin_bridge) == 0:
            os.system("")
            _logger.warn("\033[1;31mNo plugins installed\033[0m")

        ok, buffer_status = self.buffer.status() # 数据暂存区容量监测
        if ok and buffer_status["used"] >= buffer_status["size"]:
            os.system("")
            _logger.warn("\033[1;31m The data buffer area is full \033[0m")

        plugin_bridge = self.__control_plugin( # pluginctl控制
            self.__plugin_bridge, message["chat"]["type"], message["chat"]["id"])

        message_type = ""
        message_type, message = self.__mark_message_for_pluginRun(message) # 分类标记消息

        if message_type == "unknown":
            self.__logging_for_pluginRun(message, "unknown")
            return

        for plugin, command in plugin_bridge.items():
            if message_type == "query":
                if command in ["", " ", None]:
                    continue

            if message.get(message_type)[:len(command)] == command:
                module = self.__import_module(plugin)
                pluginFunc = getattr(module, plugin)
                fur = self.__thread_pool.submit(pluginFunc, bot, message)
                fur.add_done_callback(self.__threadpool_exception)

                self.__response_times += 1

                if message["chat"]["type"] != "private" and \
                message["chat"]["id"] not in self.__response_chats:
                    self.__response_chats.append(message["chat"]["id"])
                if message["from"]["id"] not in self.__response_users:
                    self.__response_users.append(message["from"]["id"])

                self.__logging_for_pluginRun(message, plugin)

    def _washUpdates(self, results):
        """
        清洗消息队列
        results应当是一个列表
        """
        if not results:
            return False
        elif len(results) < 1:
            return None
        update_ids = []
        messages = []
        for result in results:
            if "update_id" not in result.keys():
                return None
            update_ids.append(result["update_id"])
            query_or_message = ""
            if result.get("inline_query"):
                query_or_message = "inline_query"
            elif result.get("callback_query"):
                query_or_message = "callback_query"
            elif result.get("my_chat_member"):
                query_or_message = "my_chat_member"
            elif result.get("chat_member"):
                query_or_message = "chat_member"
            elif result.get("chat_join_request"):
                query_or_message = "chat_join_request"
            elif result.get("edited_message"):
                query_or_message = "edited_message"
            elif result.get("message"):
                query_or_message = "message"
            update_ids.append(result.get("update_id"))

            if query_or_message == "inline_query":
                inline_query = result.get(query_or_message)
                inline_query["message_id"] = result["update_id"]
                inline_query["chat"] = inline_query.get("from")
                inline_query["chat"].pop("language_code")
                inline_query["chat"].pop("is_bot")
                inline_query["chat"]["type"] = "private"
                inline_query["text"] = ""
                inline_query["query"] = self.__inline_mode_prefix + inline_query["query"] # Inline Mode Plugin Prefix
                messages.append(inline_query)
            elif query_or_message == "callback_query":
                callback_query = result.get(query_or_message).get("message")
                callback_query["click_user"] = result.get(query_or_message)[
                    "from"]
                callback_query["callback_query_id"] = result.get(
                    query_or_message).get("id")
                callback_query["callback_query_data"] = result.get(
                    query_or_message).get("data")
                messages.append(callback_query)
            elif query_or_message == "my_chat_member":
                my_chat_member = result.get(query_or_message)
                my_chat_member["message_id"] = result.get("update_id")
                my_chat_member["my_chat_member_id"] = result.get("update_id")
                messages.append(my_chat_member)
            elif query_or_message == "chat_member":
                chat_member = result.get(query_or_message)
                chat_member["message_id"] = result.get("update_id")
                chat_member["chat_member_id"] = result.get("update_id")
                messages.append(chat_member)
            elif query_or_message == "chat_join_request":
                chat_join_request = result.get(query_or_message)
                chat_join_request["message_id"] = result.get("update_id")
                chat_join_request["chat_join_request_id"] = result.get("update_id")
                messages.append(chat_join_request)
            else:
                messages.append(result.get(query_or_message))

        if len(update_ids) >= 1:
            self._offset = max(update_ids) + 1
            return messages
        else:
            return None

    def message_deletor(self, time_gap, chat_id, message_id):
        """
        定时删除一条消息，时间范围：[0, 900],单位秒
        """
        if time_gap < 0 or time_gap > 900:
            return "time_gap_error"
        else:
            def message_deletor_func(time_gap, chat_id, message_id):
                time.sleep(int(time_gap))
                self.deleteMessage(chat_id=chat_id, message_id=message_id)

            if time_gap == 0:
                message_deletor_func(chat_id, message_id)
            else:
                fur = self.__timer_thread_pool.submit(
                    message_deletor_func, time_gap, chat_id, message_id)
                fur.add_done_callback(self.__threadpool_exception)

            return "ok"

    def timer(self, time_gap, func, args):
        """
        单次定时器，时间范围：[0, 900],单位秒
        """
        if time_gap < 0 or time_gap > 900:
            return "time_gap_error"
        elif type(args) is not tuple:
            return "args_must_be_tuple"
        else:
            def timer_func(time_gap, func, args):
                time.sleep(int(time_gap))
                func(*args)

            if time_gap == 0:
                func(args)
            else:
                fur = self.__timer_thread_pool.submit(
                    timer_func, time_gap, func, args)
                fur.add_done_callback(self.__threadpool_exception)

            return "ok"

    def path_converter(self, path):
        """
        根据操作系统转换URI
        """

        path = str(Path(path))

        return path

    @property
    def plugin_bridge(self):
        """
        获取插件桥
        """

        return self.__plugin_bridge

    @property
    def plugin_dir(self):
        """
        获取插件路径
        """

        return self.__plugin_dir

    @property
    def version(self):
        """
        获取框架版本号
        """

        return self.__VERSION

    @property
    def author(self):
        """
        作者信息
        """

        return self.__AUTHOR

    @property
    def root_id(self):
        """
        获取root用户ID
        """

        return self.__root_id

    @property
    def bot_id(self):
        """
        获取Bot的ID
        """

        return self.__bot_id

    @property
    def uptime(self):
        """
        获取框架的持续运行时间(单位为秒)
        """
        second = int(time.time()) - self.__start_time

        return second

    @property
    def response_times(self):
        """
        获取框架启动后响应指令的统计次数
        """
        return self.__response_times

    @property
    def response_chats(self):
        """
        获取框架启动后响应的所有群组ID
        """
        return self.__response_chats

    @property
    def response_users(self):
        """
        获取框架启动后响应的所有用户ID
        """
        return self.__response_users
    
    @property
    def proxies(self):
        """
        获取代理信息
        """
        return self.__proxies

    def getChatCreator(self, chat_id):
        """
        获取群组创建者信息
        """
        if str(chat_id)[0] == "-":
            req = self.getChatAdministrators(str(chat_id))
            if req:
                creator = []
                for i, user in enumerate(req):
                    if user["status"] == "creator":
                        creator.append(req[i])
                if len(creator) == 1:
                    return creator[0]
                else:
                    return False
        else:
            return False

    def getChatMemberStatus(self, chat_id, user_id):
        """
        获取群组用户状态
        "creator",
        "administrator",
        "member",
        "restricted",
        "left",
        "kicked"
        """
        if str(chat_id)[0] == "-":
            req = self.getChatMember(chat_id=chat_id, user_id=user_id)

            if req != False:
                return req["status"]
        else:
            return False

    def getFileDownloadPath(self, file_id):
        """
        生成文件下载链接
        注意：下载链接包含Bot Key
        """
        req = self.getFile(file_id=file_id)
        if req:
            file_path = req["file_path"]
            if (self._local_api_server != "False" and
                "telegram.org" not in self._basic_url):
                return file_path
            else:
                file_download_path = self._basic_url + "file/bot" + self._key + r"/" + file_path
                return file_download_path
        else:
            return False

    # Getting updates
    def getUpdates(self, limit=100, allowed_updates=None):
        """
        获取消息队列
        """
        command = inspect.stack()[0].function
        addr = command + "?offset=" + str(self._offset) + \
            "&limit=" + str(limit) + "&timeout=" + str(self._timeout)

        if allowed_updates is not None:
            addr += "&allowed_updates=" + json.dumps(allowed_updates)

        return self.request.get(addr)

    def setWebhook(self, url, certificate=None, ip_address=None, max_connections=None,
        allowed_updates=None, drop_pending_updates=None, secret_token=None):
        """
        设置Webhook
        Ports currently supported for Webhooks: 443, 80, 88, 8443.
        """
        command = inspect.stack()[0].function
        addr = command + "?url=" + str(url)
        if ip_address is not None:
            addr += "&ip_address=" + str(ip_address)
        if max_connections is not None:
            addr += "&max_connections=" + str(max_connections)
        if allowed_updates is not None:
            addr += "&allowed_updates=" + json.dumps(allowed_updates)
        if drop_pending_updates is not None:
            addr += "&drop_pending_updates=" + str(drop_pending_updates)
        if secret_token is not None:
            addr += "&secret_token=" + str(secret_token)

        file_data = None
        if certificate is not None:
            if type(certificate) == bytes:
                file_data = {"certificate": certificate}
            else:
                file_data = {"certificate": open(certificate, 'rb')}

        if file_data is None:
            return self.request.post(addr)
        else:
            return self.request.postFile(addr, file_data)

    def deleteWebhook(self, drop_pending_updates=None):
        """
        删除设置的Webhook
        """
        command = inspect.stack()[0].function
        addr = command
        if drop_pending_updates is not None:
            addr += "?drop_pending_updates=" + str(drop_pending_updates)
        return self.request.post(addr)

    def getWebhookInfo(self):
        """
        获取当前的Webhook状态
        """
        command = inspect.stack()[0].function
        addr = command

        return self.request.post(addr)

    # Available methods

    def getMe(self):
        """
        获取机器人基本信息
        """
        command = inspect.stack()[0].function
        addr = command + "?" + "offset=" + \
            str(self._offset) + "&timeout=" + str(self._timeout)
        return self.request.post(addr)

    def getFile(self, file_id):
        """
        获取文件信息
        """
        command = inspect.stack()[0].function
        addr = command + "?file_id=" + file_id
        return self.request.post(addr)

    def logOut(self):
        """
        在本地启动机器人之前，使用此方法从云Bot API服务器注销。
        """
        command = inspect.stack()[0].function
        addr = command

        return self.request.post(addr)

    def close(self):
        """
        在将bot实例从一个本地服务器移动到另一个本地服务器之前
        使用此方法关闭它
        """
        command = inspect.stack()[0].function
        addr = command

        return self.request.post(addr)

    def sendMessage(self, chat_id, text, parse_mode="Text", reply_to_message_id=None,
        reply_markup=None, disable_web_page_preview=None, entities=None,
        allow_sending_without_reply=None, protect_content=None, message_thread_id=None):
        """
        发送文本消息
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&text=" + quote(text)
        if parse_mode in ("Markdown", "MarkdownV2", "HTML"):
            addr += "&parse_mode=" + parse_mode
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if disable_web_page_preview is not None:
            addr += "&disable_web_page_preview=" + str(disable_web_page_preview)
        if entities is not None:
            addr += "&entities=" + json.dumps(entities)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        return self.request.post(addr)

    def sendVoice(self, chat_id, voice, caption=None, parse_mode="Text", reply_to_message_id=None,
        reply_markup=None, allow_sending_without_reply=None, caption_entities=None,
        protect_content=None, message_thread_id=None):
        """
        发送音频消息 .ogg
        """
        command = inspect.stack()[0].function
        if voice[:7] == "http://" or voice[:7] == "https:/":
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&voice=" + voice
        elif type(voice) == bytes:
            file_data = {"voice": voice}
            addr = command + "?chat_id=" + str(chat_id)
        elif type(voice) == str and '.' not in voice:
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&voice=" + voice
        else:
            file_data = {"voice": open(voice, 'rb')}
            addr = command + "?chat_id=" + str(chat_id)

        if caption is not None:
            addr += "&caption=" + quote(caption)
        if parse_mode in ("Markdown", "MarkdownV2", "HTML"):
            addr += "&parse_mode" + parse_mode
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if caption_entities is not None:
            addr += "&caption_entities=" + json.dumps(caption_entities)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        if file_data is None:
            return self.request.post(addr)
        else:
            return self.request.postFile(addr, file_data)


    def sendAnimation(self, chat_id, animation, message_thread_id=None, duration=None,
        width=None, height=None, thumbnail=None, caption=None, parse_mode=None,
        caption_entities=None, has_spoiler=None, disable_notification=None,
        protect_content=None, reply_to_message_id=None, allow_sending_without_reply=None,
        reply_markup=None):
        """
        使用此方法发送动画文件（GIF或H.264/MPEG-4 AVC视频，无声音）
        目前，机器人可以发送大小为50MB的动画文件，这个限制在未来可能会被改变
        """
        command = inspect.stack()[0].function
        file_data = {}
        if animation[:7] == "http://" or animation[:7] == "https:/":
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&animation=" + animation
        elif type(animation) == bytes:
            file_data = {"animation": animation}
            addr = command + "?chat_id=" + str(chat_id)
        elif type(animation) == str and '.' not in animation:
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&animation=" + animation
        else:
            file_data = {"animation": open(animation, 'rb')}
            addr = command + "?chat_id=" + str(chat_id)

        if thumbnail is not None:
            if thumbnail[:7] == "http://" or thumbnail[:7] == "https:/":
                addr += "&thumbnail=" + thumbnail
            elif type(thumbnail) == bytes:
                if file_data is None:
                    file_data = {"thumbnail": thumbnail}
                else:
                    file_data["thumbnail"] = thumbnail
            elif type(thumbnail) == str and '.' not in thumbnail:
                addr += "&thumbnail=" + thumbnail
            else:
                if file_data is None:
                    file_data = {"thumbnail": open(thumbnail, 'rb')}
                else:
                    file_data["thumbnail"] = open(thumbnail, 'rb')

        if duration is not None:
            addr += "&duration=" + quote(duration)
        if width is not None:
            addr += "&width=" + quote(width)
        if height is not None:
            addr += "&height=" + quote(height)
        if disable_notification is not None:
            addr += "&disable_notification=" + quote(disable_notification)
        if caption is not None:
            addr += "&caption=" + quote(caption)
        if parse_mode in ("Markdown", "MarkdownV2", "HTML"):
            addr += "&parse_mode" + parse_mode
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if caption_entities is not None:
            addr += "&caption_entities=" + json.dumps(caption_entities)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)
        if has_spoiler is not None:
            addr += "&has_spoiler=" + str(has_spoiler)

        if file_data is None:
            return self.request.post(addr)
        else:
            self.request.postFile(addr, file_data)

    def sendAudio(self, chat_id, audio, message_thread_id=None, caption=None,
        parse_mode=None, caption_entities=None, duration=None, performer=None, title=None,
        thumbnail=None, disable_notification=None, protect_content=None,
        reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        使用此方法发送音频文件
        """
        command = inspect.stack()[0].function
        file_data = {}
        if audio[:7] == "http://" or audio[:7] == "https:/":
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&audio=" + audio
        elif type(audio) == bytes:
            file_data = {"audio": audio}
            addr = command + "?chat_id=" + str(chat_id)
        elif type(audio) == str and '.' not in audio:
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&audio=" + audio
        else:
            file_data = {"audio": open(audio, 'rb')}
            addr = command + "?chat_id=" + str(chat_id)

        if thumbnail is not None:
            if thumbnail[:7] == "http://" or thumbnail[:7] == "https:/":
                addr += "&thumbnail=" + thumbnail
            elif type(thumbnail) == bytes:
                if file_data is None:
                    file_data = {"thumbnail": thumbnail}
                else:
                    file_data["thumbnail"] = thumbnail
            elif type(thumbnail) == str and '.' not in thumbnail:
                addr += "&thumbnail=" + thumbnail
            else:
                if file_data is None:
                    file_data = {"thumbnail": open(thumbnail, 'rb')}
                else:
                    file_data["thumbnail"] = open(thumbnail, 'rb')

        if duration is not None:
            addr += "&duration=" + quote(duration)
        if performer is not None:
            addr += "&performer=" + quote(performer)
        if disable_notification is not None:
            addr += "&disable_notification=" + quote(disable_notification)
        if caption is not None:
            addr += "&caption=" + quote(caption)
        if parse_mode in ("Markdown", "MarkdownV2", "HTML"):
            addr += "&parse_mode" + parse_mode
        if title is not None:
            addr += "&title=" + title
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if caption_entities is not None:
            addr += "&caption_entities=" + json.dumps(caption_entities)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        if file_data is None:
            return self.request.post(addr)
        else:
            return self.request.postFile(addr, file_data)

    def sendPhoto(self, chat_id, photo, caption=None, parse_mode="Text", reply_to_message_id=None,
        reply_markup=None, allow_sending_without_reply=None, caption_entities=None,
        protect_content=None, message_thread_id=None, has_spoiler=None):  # 发送图片
        """
        发送图片
        """
        command = inspect.stack()[0].function
        if photo[:7] == "http://" or photo[:7] == "https:/":
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&photo=" + photo
        elif type(photo) == bytes:
            file_data = {"photo": photo}
            addr = command + "?chat_id=" + str(chat_id)
        elif type(photo) == str and '.' not in photo:
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&photo=" + photo
        else:
            file_data = {"photo": open(photo, 'rb')}
            addr = command + "?chat_id=" + str(chat_id)

        if caption is not None:
            addr += "&caption=" + quote(caption)
        if parse_mode in ("Markdown", "MarkdownV2", "HTML"):
            addr += "&parse_mode=" + parse_mode
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if caption_entities is not None:
            addr += "&caption_entities=" + json.dumps(caption_entities)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)
        if has_spoiler is not None:
            addr += "&has_spoiler=" + str(has_spoiler)

        if file_data is None:
            return self.request.post(addr)
        else:
            return self.request.postFile(addr, file_data)

    def sendVideo(self, chat_id, video, message_thread_id=None, duration=None, width=None,
        height=None, thumbnail=None, caption=None, parse_mode=None, caption_entities=None,
        has_spoiler=None, supports_streaming=None, disable_notification=None,
        protect_content=None, reply_to_message_id=None, allow_sending_without_reply=None,
        reply_markup=None):
        """
        发送视频
        """
        command = inspect.stack()[0].function
        file_data = {}
        if video[:7] == "http://" or video[:7] == "https:/":
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&video=" + video
        elif type(video) == bytes:
            file_data = {"video": video}
            addr = command + "?chat_id=" + str(chat_id)
        elif type(video) == str and '.' not in video:
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&video=" + video
        else:
            file_data = {"video": open(video, 'rb')}
            addr = command + "?chat_id=" + str(chat_id)

        if thumbnail is not None:
            if thumbnail[:7] == "http://" or thumbnail[:7] == "https:/":
                addr += "&thumbnail=" + thumbnail
            elif type(thumbnail) == bytes:
                if file_data is None:
                    file_data = {"thumbnail": thumbnail}
                else:
                    file_data["thumbnail"] = thumbnail
            elif type(thumbnail) == str and '.' not in thumbnail:
                addr += "&thumbnail=" + thumbnail
            else:
                if file_data is None:
                    file_data = {"thumbnail": open(thumbnail, 'rb')}
                else:
                    file_data["thumbnail"] = open(thumbnail, 'rb')

        if duration is not None:
            addr += "&duration=" + quote(duration)
        if width is not None:
            addr += "&width=" + quote(width)
        if height is not None:
            addr += "&height=" + quote(height)
        if disable_notification is not None:
            addr += "&disable_notification=" + quote(disable_notification)
        if supports_streaming is not None:
            addr += "&supports_streaming=" + quote(supports_streaming)
        if caption is not None:
            addr += "&caption=" + quote(caption)
        if parse_mode in ("Markdown", "MarkdownV2", "HTML"):
            addr += "&parse_mode=" + parse_mode
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if caption_entities is not None:
            addr += "&caption_entities=" + json.dumps(caption_entities)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)
        if has_spoiler is not None:
            addr += "&has_spoiler=" + str(has_spoiler)

        if file_data is None:
            return self.request.post(addr)
        else:
            return self.request.postFile(addr, file_data)

    def sendVideoNote(self, chat_id, video_note, message_thread_id=None, duration=None,
        length=None, thumbnail=None, disable_notification=None, protect_content=None,
        reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        发送圆形或方形视频？
        """
        command = inspect.stack()[0].function
        file_data = {}
        char_id_str = str(chat_id)
        if video_note[:7] == "http://" or video_note[:7] == "https:/":
            file_data = None
            addr = command + "?chat_id=" + char_id_str + "&video_note=" + video_note
        elif type(video_note) == bytes:
            file_data = {"video_note": video_note}
            addr = command + "?chat_id=" + char_id_str
        elif type(video_note) == str and '.' not in video_note:
            file_data = None
            addr = command + "?chat_id=" + char_id_str + "&video_note=" + video_note
        else:
            file_data = {"video_note": open(video_note, 'rb')}
            addr = command + "?chat_id=" + char_id_str

        if thumbnail is not None:
            if thumbnail[:7] == "http://" or thumbnail[:7] == "https:/":
                addr += "&thumbnail=" + thumbnail
            elif type(thumbnail) == bytes:
                if file_data is None:
                    file_data = {"thumbnail": thumbnail}
                else:
                    file_data["thumbnail"] = thumbnail
            elif type(thumbnail) == str and '.' not in thumbnail:
                addr += "&thumbnail=" + thumbnail
            else:
                if file_data is None:
                    file_data = {"thumbnail": open(thumbnail, 'rb')}
                else:
                    file_data["thumbnail"] = open(thumbnail, 'rb')

        if duration is not None:
            addr += "&duration=" + quote(duration)
        if length is not None:
            addr += "&length=" + quote(length)
        if disable_notification is not None:
            addr += "&disable_notification=" + quote(disable_notification)
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        if file_data is None:
            return self.request.post(addr)
        else:
            return self.request.postFile(addr, file_data)

    def sendMediaGroup(self, chat_id, medias, disable_notification=None,
        reply_to_message_id=None, reply_markup=None, allow_sending_without_reply=None,
        protect_content=None, message_thread_id=None):  # 暂未弄懂格式。
        """
        使用此方法可以将一组照片，视频，文档或音频作为相册发送。
        文档和音频文件只能在具有相同类型消息的相册中分组。
        (目前只支持http链接和文件id，暂不支持上传文件)
        media的格式：（同时请求需要加入header头，指定传送参数为json类型，
        并且将data由字典转为json字符串传送）
        medias ={
            'caption': 'test',
            'media': [
            {
            'type': 'photo',
            'media': 'https://xxxx.com/sample/7kwx_2.jpg'
            },
            {
            'type': 'photo',
            'media': 'AgACAgQAAx0ETbyLwwADeF5s6QosSI_IW3rKir3PrMUX'
            }
            ]
        }
        InputMediaPhoto:
        type
        media
        caption
        parse_mode

        InputMediaVideo:
        type
        media
        thumb
        caption
        parse_mode
        width
        height
        duration
        supports_streaming
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)
        if disable_notification is not None:
            addr += "&disable_notification=" + str(disable_notification)
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        return self.request.postJson(addr, medias)

    def sendDocument(self, chat_id, document, message_thread_id=None, thumbnail=None,
        caption=None, parse_mode=None, caption_entities=None,
        disable_content_type_detection=None, disable_notification=None,
        protect_content=None, reply_to_message_id=None, allow_sending_without_reply=None,
        reply_markup=None):
        """
        发送文件
        """
        command = inspect.stack()[0].function
        file_data = {}
        if document[:7] == "http://" or document[:7] == "https:/":
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&document=" + document
        elif type(document) == bytes:
            file_data = {"document": document}
            addr = command + "?chat_id=" + str(chat_id)
        elif type(document) == str and '.' not in document:
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&document=" + document
        else:
            file_data = {"document": open(document, 'rb')}
            addr = command + "?chat_id=" + str(chat_id)

        if thumbnail is not None:
            if thumbnail[:7] == "http://" or thumbnail[:7] == "https:/":
                addr += "&thumbnail=" + thumbnail
            elif type(thumbnail) == bytes:
                if file_data is None:
                    file_data = {"thumbnail": thumbnail}
                else:
                    file_data["thumbnail"] = thumbnail
            elif type(thumbnail) == str and '.' not in thumbnail:
                addr += "&thumbnail=" + thumbnail
            else:
                if file_data is None:
                    file_data = {"thumbnail": open(thumbnail, 'rb')}
                else:
                    file_data["thumbnail"] = open(thumbnail, 'rb')

        if disable_notification is not None:
            addr += "&disable_notification=" + quote(disable_notification)
        if caption is not None:
            addr += "&caption=" + quote(caption)
        if parse_mode in ("Markdown", "MarkdownV2", "HTML"):
            addr += "&parse_mode=" + parse_mode
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if disable_content_type_detection is not None:
            addr += "&disable_content_type_detection=" + str(disable_content_type_detection)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if caption_entities is not None:
            addr += "&caption_entities=" + json.dumps(caption_entities)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        if file_data is None:
            return self.request.post(addr)
        else:
            return self.request.postFile(addr, file_data)

    def leaveChat(self, chat_id):
        """
        退出群组
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)
        return self.request.post(addr)

    def getChat(self, chat_id):
        """
        使用此方法可获取有关聊天的最新信息（一对一对话的用户的当前名称，
        用户的当前用户名，组或频道等）。
        成功返回一个Chat对象。
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)
        return self.request.post(addr)

    def getChatAdministrators(self, chat_id):
        """
        获取群组所有管理员信息
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)
        return self.request.post(addr)

    def getChatMemberCount(self, chat_id):
        """
        获取群组成员总数
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)

        return self.request.post(addr)

    def getUserProfilePhotos(self, user_id, offset=None, limit=None):
        """
        获取用户头像
        """
        command = inspect.stack()[0].function
        addr = command + "?user_id=" + str(user_id)

        if offset is not None:
            addr += "&offset=" + str(offset)
        if limit is not None and limit in list(range(1, 101)):
            addr += "&limit=" + str(limit)

        return self.request.post(addr)

    def getChatMember(self, chat_id, user_id):
        """
        获取群组特定用户信息
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&user_id=" + str(user_id)

        return self.request.post(addr)

    def setChatTitle(self, chat_id, title):
        """
        设置群组标题
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&title=" + quote(str(title))

        return self.request.post(addr)

    def setChatDescription(self, chat_id, description):
        """
        设置群组简介（测试好像无效。。）
        //FIXME
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&description=" + quote(str(description))
        return self.request.post(addr)

    def setChatPhoto(self, chat_id, photo):
        """
        设置群组头像
        """
        command = inspect.stack()[0].function
        file_data = {"photo": open(photo, 'rb')}
        addr = command + "?chat_id=" + str(chat_id)

        return self.request.postFile(addr, file_data)

    def deleteChatPhoto(self, chat_id):
        """
        删除群组头像
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)
        return self.request.post(addr)

    def setChatPermissions(self, chat_id, permissions,
    use_independent_chat_permissions=None):
        """
        设置群组默认聊天权限
        permissions = {
            'can_send_messages':False,
            'can_send_audios':False,
            'can_send_documents':False,
            'can_send_photos':False,
            'can_send_videos':False,
            'can_send_video_notes':False,
            'can_send_voice_notes':False,
            'can_send_polls':False,
            'can_send_other_messages':False,
            'can_add_web_page_previews':False,
            'can_change_info':False,
            'can_invite_users':False,
            'can_pin_messages':False,
            'can_manage_topics':False
        }
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)
        if use_independent_chat_permissions is not None:
            addr += "&use_independent_chat_permissions=" + str(use_independent_chat_permissions)
        permissions = {"permissions": permissions}

        return self.request.postJson(addr, permissions)

    def restrictChatMember(self, chat_id, user_id, permissions,
    until_date=None, use_independent_chat_permissions=None):
        """
        限制群组用户权限
        permissions = {
            'can_send_messages':False,
            'can_send_audios':False,
            'can_send_documents':False,
            'can_send_photos':False,
            'can_send_videos':False,
            'can_send_video_notes':False,
            'can_send_voice_notes':False,
            'can_send_polls':False,
            'can_send_other_messages':False,
            'can_add_web_page_previews':False,
            'can_change_info':False,
            'can_invite_users':False,
            'can_pin_messages':False,
            'can_manage_topics':False
        }
        until_date format:
        timestamp + offset
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + \
            str(chat_id) + "&user_id=" + str(user_id)
        if len(permissions) != 8:
            return False
        if until_date is not None:
            until_date = int(time.time()) + int(until_date)
            addr += "&until_date=" + str(until_date)
        if use_independent_chat_permissions is not None:
            addr += "&until_date=" + str(use_independent_chat_permissions)

        return self.request.postJson(addr, permissions)

    def promoteChatMember(self, chat_id, user_id, is_anonymous=None,
        can_manage_chat=None, can_change_info=None, can_post_messages=None,
        can_edit_messages=None, can_delete_messages=None, can_manage_video_chats=None,
        can_invite_users=None, can_restrict_members=None, can_pin_messages=None,
        can_promote_members=None, can_manage_topics=None):
        """
        修改管理员权限(只能修改由机器人任命的管理员的权限,
        范围为机器人权限的子集)
        {
        'is_anonymous':False,
        'can_manage_chat':False,
        'can_change_info':False,
        'can_post_messages':False,
        'can_edit_messages':False,
        'can_delete_messages':False,
        'can_manage_video_chats':False,
        'can_invite_users':False,
        'can_restrict_members':False,
        'can_pin_messages':False,
        'can_promote_members':False,
        'can_manage_topics':False
        }
        """
        command = inspect.stack()[0].function

        addr = command + "?chat_id=" + str(chat_id) + "&user_id=" + str(user_id)

        if is_anonymous is not None:
            addr += "&is_anonymous=" + str(is_anonymous)
        if can_manage_chat is not None:
            addr += "&can_manage_chat=" + str(can_manage_chat)
        if can_change_info is not None:
            addr += "&can_change_info=" + str(can_change_info)
        if can_post_messages is not None:
            addr += "&can_post_messages=" + str(can_post_messages)
        if can_edit_messages is not None:
            addr += "&can_edit_messages=" + str(can_edit_messages)
        if can_delete_messages is not None:
            addr += "&can_delete_messages=" + str(can_delete_messages)
        if can_manage_video_chats is not None:
            addr += "&can_manage_video_chats=" + str(can_manage_video_chats)
        if can_invite_users is not None:
            addr += "&can_invite_users=" + str(can_invite_users)
        if can_restrict_members is not None:
            addr += "&can_restrict_members=" + str(can_restrict_members)
        if can_pin_messages is not None:
            addr += "&can_pin_messages=" + str(can_pin_messages)
        if can_promote_members is not None:
            addr += "&can_promote_members=" + str(can_promote_members)
        if can_manage_topics is not None:
            addr += "&can_manage_topics=" + str(can_manage_topics)

        return self.request.post(addr)

    def pinChatMessage(self, chat_id, message_id, disable_notification=None):
        """
        置顶消息
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&message_id=" + str(message_id)
        if disable_notification is not None:
            addr += "&disable_notification=" + str(disable_notification)

        return self.request.post(addr)

    def unpinChatMessage(self, chat_id, message_id=None):
        """
        使用此方法可以从聊天中的置顶消息列表中删除消息
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)

        if message_id is not None:
            addr += "&message_id=" + str(message_id)

        return self.request.post(addr)

    def unpinAllChatMessages(self, chat_id):
        """
        使用此方法可以清除聊天中的置顶消息列表中的所有置顶消息
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)

        return self.request.post(addr)

    def sendLocation(self, chat_id, latitude, longitude,
        horizontal_accuracy=None, live_period=None,
        heading=None, disable_notification=None,
        reply_to_message_id=None, reply_markup=None,
        allow_sending_without_reply=None, protect_content=None,
        message_thread_id=None):
        """
        发送地图定位，经纬度
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&latitude=" + str(
            float(latitude)) + "&longitude=" + str(float(longitude))
        if live_period is not None:
            addr += "&live_period=" + str(live_period)
        if horizontal_accuracy is not None:
            addr += "&horizontal_accuracy=" + str(horizontal_accuracy)
        if heading is not None:
            addr += "&heading=" + str(heading)
        if disable_notification is not None:
            addr += "&disable_notification=" + str(disable_notification)
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        return self.request.post(addr)

    def sendContact(self, chat_id, phone_number, first_name, last_name=None,
        reply_to_message_id=None, reply_markup=None, allow_sending_without_reply=None,
        protect_content=None, message_thread_id=None):
        """
        发送联系人信息
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&phone_number=" + str(phone_number) + "&first_name=" + str(
            first_name)
        if last_name is not None:
            addr += "&last_name=" + str(last_name)
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        return self.request.post(addr)

    def sendPoll(self, chat_id, question, options, is_anonymous=None,
        type_=None, allows_multiple_answers=None, correct_option_id=None,
        explanation=None, explanation_parse_mode=None, explanation_entities=None,
        open_period=None, close_date=None, is_closed=None, disable_notification=None,
        reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None,
        protect_content=None, message_thread_id=None):
        """
        使用此方法发起投票(quiz or regular, defaults to regular)
        options格式:
        options = [
            "option 1",
            "option 2"
        ]
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&question=" + str(question)
        addr += "&options=" + json.dumps(options)

        if is_anonymous is not None:
            addr += "&is_anonymous=" + str(is_anonymous)
        if type_ is not None:
            addr += "&type=" + str(type_)

        if type_ == "quiz":
            if allows_multiple_answers is not None:
                addr += "&allows_multiple_answers=" + str(allows_multiple_answers)
            if correct_option_id is not None:
                addr += "&correct_option_id=" + str(correct_option_id)
            if explanation is not None:
                addr += "&explanation=" + str(explanation)
            if explanation_parse_mode is not None:
                addr += "&explanation_parse_mode=" + str(explanation_parse_mode)
            if explanation_entities is not None:
                addr += "&explanation_entities=" + json.dumps(explanation_entities)

        if open_period is not None:
            addr += "&open_period=" + str(open_period)
        if close_date is not None:
            addr += "&close_date=" + str(close_date)
        if is_closed is not None:
            addr += "&is_closed=" + str(is_closed)
        if disable_notification is not None:
            addr += "&disable_notification=" + str(disable_notification)
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        return self.request.post(addr)

    def sendDice(self, chat_id, emoji=None, disable_notification=None,
        reply_to_message_id=None, allow_sending_without_reply=None,
        reply_markup=None, protect_content=None, message_thread_id=None):
        """
        使用此方法发送一个动画表情
        emoji参数必须是以下几种：
            1.🎲dice(骰子) values 1-6
            2.🎯darts(飞镖) values 1-6
            3.🎳bowling(保龄球) values 1-6
            4.🏀basketball(篮球) values 1-5
            5.⚽football(足球) values 1-5
            6.🎰slot machine(老虎机) values 1-64
            默认为骰子
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)

        if emoji is not None:
            addr += "&emoji=" + str(emoji)
        if disable_notification is not None:
            addr += "&disable_notification=" + str(disable_notification)
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        return self.request.post(addr)

    def sendVenue(self, chat_id, latitude, longitude, title, address, 
        allow_sending_without_reply=None,
        foursquare_id=None, foursquare_type=None,
        google_place_id=None, google_place_type=None,
        disable_notification=None, reply_to_message_id=None,
        reply_markup=None, protect_content=None, message_thread_id=None):
        """
        使用此方法发送关于地点的信息。
        (发送地点，显示在地图上)
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&latitude=" + str(float(latitude)) + "&longitude=" + str(
            float(longitude)) + "&title=" + str(title) + "&address=" + str(address)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if foursquare_id is not None:
            addr += "&foursquare_id=" + str(foursquare_id)
        if foursquare_type is not None:
            addr += "&foursquare_type=" + str(foursquare_type)
        if google_place_id is not None:
            addr += "&google_place_id=" + str(google_place_id)
        if google_place_type is not None:
            addr += "&google_place_type=" + str(google_place_type)
        if disable_notification is not None:
            addr += "&disable_notification=" + str(disable_notification)
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        return self.request.post(addr)

    def sendChatAction(self, chat_id, action, message_thread_id=None):
        """
        发送聊天状态，类似： 正在输入...
            typing :for text messages,
            upload_photo :for photos,
            record_video/upload_video :for videos,
            record_voice/upload_voice: for voice notes,
            upload_document :for general files,
            choose_sticker: for stickers,
            find_location :for location data,
            record_video_note/upload_video_note :for video notes.
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&action=" + str(action)

        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        return self.request.post(addr)

    def forwardMessage(self, chat_id, from_chat_id, message_id,
        disable_notification=None, protect_content=None, message_thread_id=None):
        """
        转发消息
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&from_chat_id=" + str(from_chat_id) \
            + "&message_id=" + str(message_id)

        if disable_notification is not None:
            addr += "&disable_notification=" + str(disable_notification)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        return self.request.post(addr)

    def copyMessage(self, chat_id, from_chat_id, message_id,
        caption=None, parse_mode="Text", caption_entities=None,
        disable_notification=None, reply_to_message_id=None,
        allow_sending_without_reply=None, reply_markup=None,
        protect_content=None, message_thread_id=None):
        """
        使用此方法可以复制任何类型的消息。
        该方法类似于forwardMessages方法,
        但是复制的消息没有指向原始消息的链接。
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&from_chat_id=" + str(from_chat_id) \
            + "&message_id=" + str(message_id)

        if caption is not None:
            addr += "&caption=" + quote(caption)
        if parse_mode in ("Markdown", "MarkdownV2", "HTML"):
            addr += "&parse_mode" + parse_mode
        if disable_notification is not None:
            addr += "&disable_notification=" + str(disable_notification)
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        if caption_entities is not None:
            return self.request.postJson(addr, caption_entities)
        else:
            return self.request.post(addr)


    def banChatMember(self, chat_id, user_id, until_date=None,
        revoke_messages=None):
        """
        从Group、Supergroup或者Channel中踢人，
        被踢者在until_date期限内不可再次加入
        可通过revoke_messages参数删除被踢者发送的所有消息
        until_date format:
        timestamp + offset
        """

        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&user_id=" + str(user_id)
        if until_date is not None:
            until_date = int(time.time()) + int(until_date)
            addr += "&until_date=" + str(until_date)
        if revoke_messages is not None:
            addr += "&revoke_messages=" + str(revoke_messages) #似乎无效

        return self.request.post(addr)

    def unbanChatMember(self, chat_id, user_id, only_if_banned=None):
        """
        使用此方法可以取消超级组或频道中以前被踢过的用户的权限。
        (解除user被设置的until_date)
        ChatPermissions:
        can_send_messages
        can_send_media_messages
        can_send_polls
        can_send_other_messages
        can_add_web_page_previews
        can_change_info
        can_invite_users
        can_pin_messages
        """

        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + \
            str(chat_id) + "&user_id=" + str(user_id)

        if only_if_banned is not None:
            addr += "&only_if_banned=" + str(only_if_banned)

        return self.request.post(addr)

    def banChatSenderChat(self, chat_id, sender_chat_id):
        """
        使用此方法禁止超级组或频道中的频道聊天
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&sender_chat_id=" + str(sender_chat_id)

        return self.request.post(addr)

    def unbanChatSenderChat(self, chat_id, sender_chat_id):
        """
        使用此方法在超级组或频道中解禁频道聊天
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&sender_chat_id=" + str(sender_chat_id)

        return self.request.post(addr)

    def setChatAdministratorCustomTitle(self, chat_id, user_id, custom_title):
        """
        为群组的管理员设置自定义头衔
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&user_id=" + str(user_id) + "&custom_title=" + quote(str(custom_title))

        return self.request.post(addr)

    def exportChatInviteLink(self, chat_id):
        """
        使用此方法生成新的群组分享链接，
        旧有分享链接全部失效,成功返回分享链接
        聊天中的每个管理员都会生成自己的邀请链接
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)

        return self.request.post(addr)

    def createChatInviteLink(self, chat_id, name=None,
        expire_date=None, member_limit=None, creates_join_request=None):
        """
        使用此方法为聊天创建一个额外的邀请链接，
        可以使用方法 revokeChatInviteLink 撤销该链接
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)

        if name is not None:
            addr += "&name=" + str(name)
        if expire_date is not None:
            expire_date = int(time.time()) + int(expire_date)
            addr += "&expire_date=" + str(expire_date)
        if member_limit is not None:
            addr += "&member_limit=" + str(member_limit)
        if creates_join_request is not None:
            bool_val = ""
            if  creates_join_request == True:
                bool_val = "true"
            elif creates_join_request == False:
                bool_val = "false"
            addr += "&creates_join_request=" + bool_val

        return self.request.post(addr)

    def editChatInviteLink(self, chat_id, invite_link,
        name=None, expire_date=None, member_limit=None, creates_join_request=None):
        """
        使用此方法编辑机器人创建的非主要邀请链接。
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + \
            "&invite_link=" + str(invite_link)

        if name is not None:
            addr += "&name=" + str(name)
        if expire_date is not None:
            expire_date = int(time.time()) + int(expire_date)
            addr += "&expire_date=" + str(expire_date)
        if member_limit is not None:
            addr += "&member_limit=" + str(member_limit)
        if creates_join_request is not None:
            bool_val = ""
            if  creates_join_request == True:
                bool_val = "true"
            elif creates_join_request == False:
                bool_val = "false"
            addr += "&creates_join_request=" + bool_val

        return self.request.post(addr)

    def revokeChatInviteLink(self, chat_id, invite_link):
        """
        使用此方法撤销机器人创建的邀请链接,
        如果主要链接被撤销，则会自动生成一个新的链接。
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + \
            "&invite_link=" + str(invite_link)

        return self.request.post(addr)

    def approveChatJoinRequest(self, chat_id, user_id):
        """
        使用此方法批准聊天加入请求
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + \
            "&user_id=" + str(user_id)

        return self.request.post(addr)

    def declineChatJoinRequest(self, chat_id, user_id):
        """
        使用此方法拒绝聊天加入请求
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + \
            "&user_id=" + str(user_id)

        return self.request.post(addr)

    def setChatStickerSet(self, chat_id, sticker_set_name):
        """
        为一个超级群组设置贴纸集
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&sticker_set_name=" + str(sticker_set_name)

        return self.request.post(addr)

    def deleteChatStickerSet(self, chat_id):
        """
        删除超级群组的贴纸集
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)

        return self.request.post(addr)

    def editMessageLiveLocation(self, latitude, longitude,
        horizontal_accuracy=None, chat_id=None, message_id=None,
        heading=None, inline_message_id=None, reply_markup=None):
        """
        使用此方法编辑实时位置消息
        在未指定inline_message_id的时候chat_id和message_id为必须存在的参数
        """
        command = inspect.stack()[0].function

        if inline_message_id is None:
            if message_id is None or chat_id is None:
                return False

        if inline_message_id is not None:
            addr = command + "?inline_message_id=" + str(inline_message_id)
        else:
            addr = command + "?chat_id=" + str(chat_id)
            addr += "&message_id=" + str(message_id)

        addr += "&latitude=" + str(latitude)
        addr += "&longitude=" + str(longitude)

        if horizontal_accuracy is not None:
            addr += "&horizontal_accuracy="  + str(horizontal_accuracy)
        if heading is not None:
            addr += "&heading=" + str(heading)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)

        return self.request.post(addr)

    def stopMessageLiveLocation(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        """
        使用此方法可在活动期间到期前停止更新活动位置消息
        在未指定inline_message_id的时候chat_id和message_id为必须存在的参数
        """
        command = inspect.stack()[0].function

        if inline_message_id is None:
            if message_id is None or chat_id is None:
                return False

        if inline_message_id is not None:
            addr = command + "?inline_message_id=" + str(inline_message_id)
        else:
            addr = command + "?chat_id=" + str(chat_id)
            addr += "&message_id=" + str(message_id)

        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)

        return self.request.post(addr)

    def setMyName(self, name="", language_code=None):
        """
        使用此方法来改变机器人的名字
        """
        command = inspect.stack()[0].function
        addr = command + "?name=" + str(name)

        if language_code is not None:
            addr += "&language_code=" + str(language_code)

        return self.request.post(addr)
    
    def getMyName(self, language_code=None):
        """
        使用此方法来获取给定用户语言的当前机器人名称
        """
        command = inspect.stack()[0].function
        addr = command

        if language_code is not None:
            addr += "?language_code=" + str(language_code)

        return self.request.post(addr)

    def setMyCommands(self, commands, scope=None, language_code=None):
        """
        使用此方法更改机器人的命令列表

        commands传入格式示例：
            commands = [
                {"command": "start", "description": "插件列表"},
                {"command": "bing", "description": "获取每日Bing壁纸"}
            ]
        scope传入格式示例：
            scope = {
                "type": "all_private_chats"
            }
        language_code:
            A two-letter ISO 639-1 language code.(e.g. zh en)
        """
        command = inspect.stack()[0].function
        addr = command
        data = {"commands": commands}
        if scope is not None:
            data["scope"] = scope
        if language_code is not None:
            data["language_code"] = str(language_code)

        return self.request.postJson(addr, data)

    def getMyCommands(self, scope=None, language_code=None):
        """
        使用此方法获取给定范围和用户语言的机器人命令的当前列表

        scope传入格式示例：
            scope = {
                "type": "all_private_chats"
            }
        language_code:
            A two-letter ISO 639-1 language code.(e.g. zh en)
        """
        command = inspect.stack()[0].function
        addr = command

        data = {}
        if scope is not None:
            data["scope"] = scope
        if language_code is not None:
            data["language_code"] = str(language_code)

        if len(data) != 0:
            return self.request.postJson(addr, data)
        else:
            return self.request.post(addr)

    def deleteMyCommands(self, scope=None, language_code=None):
        """
        使用此方法删除给定范围和用户语言的机器人命令列表

        scope传入格式示例：
            scope = {
                "type": "all_private_chats"
            }
        language_code:
            A two-letter ISO 639-1 language code.(e.g. zh en)
        """
        command = inspect.stack()[0].function
        addr = command

        data = {}
        if scope is not None:
            data["scope"] = scope
        if language_code is not None:
            data["language_code"] = str(language_code)

        if len(data) != 0:
            return self.request.postJson(addr, data)
        else:
            return self.request.post(addr)

    def setMyDescription(self, description="", language_code=None):
        """
        使用此方法改变机器人的描述
        """
        command = inspect.stack()[0].function
        addr = command + "?description=" + str(description)
        
        if language_code is not None:
            addr += "&language_code=" + str(language_code)
        
        return self.request.post(addr)

    def getMyDescription(self, language_code=None):
        """
        使用此方法来获得当前的机器人描述
        """
        command = inspect.stack()[0].function
        addr = command

        if language_code is not None:
            addr += "?language_code=" + str(language_code)
        
        return self.request.post(addr)

    def setMyShortDescription(self, short_description="", language_code=None):
        """
        使用这种方法来改变机器人的简短描述
        """
        command = inspect.stack()[0].function
        addr = command + "?short_description=" + str(short_description)
        
        if language_code is not None:
            addr += "&language_code=" + str(language_code)
        
        return self.request.post(addr)

    def getMyShortDescription(self, language_code=None):
        """
        使用此方法获得当前的机器人简短描述
        """
        command = inspect.stack()[0].function
        addr = command

        if language_code is not None:
            addr += "?&language_code=" + str(language_code)
        
        return self.request.post(addr)

    def setChatMenuButton(self, chat_id=None, menu_button=None):
        """
        使用此方法在私人聊天中更改机器人的菜单按钮或默认菜单按钮

        menu_button传入格式示例：
            menu_button = {
                "type": "web_app",  # 类型只能是 default | command | web_app
                "text": "botton text",
                "web_app": {
                    "url": "https://google.com"
                }
            }
        """
        command = inspect.stack()[0].function
        addr = command

        data = {}
        if chat_id is not None:
            data["chat_id"] = str(chat_id)
        if menu_button is not None:
            data["menu_button"] = menu_button
        
        if len(data) != 0:
            return self.request.postJson(addr, data)
        else:
            return self.request.post(addr)
    
    def getChatMenuButton(self, chat_id=None):
        """
        使用此方法在私人聊天中获取机器人菜单按钮的当前值或默认值
        """
        command = inspect.stack()[0].function
        addr = command

        if chat_id is not None:
            addr += "?chat_id=" + str(chat_id)
        
        return self.request.post(addr)

    def setMyDefaultAdministratorRights(self, rights=None, for_channels=None):
        """
        使用此方法更改机器人作为管理员将其添加到组或渠道时所要求的默认管理员权利

        rights传入格式示例：
            rights = {
                "is_anonymous": False,
                "can_manage_chat": False,
                "can_delete_messages": False,
                "can_manage_video_chats": False,
                "can_restrict_members": False,
                "can_promote_members": False,
                "can_change_info": False,
                "can_invite_users": False,
                "can_post_messages": False,
                "can_edit_messages": False,
                "can_pin_messages": False
            }
        """
        command = inspect.stack()[0].function
        addr = command

        data = {}
        if rights is not None:
            data["rights"] = rights
        if for_channels is not None:
            data["for_channels"] = bool(for_channels)
        
        if len(data) != 0:
            return self.request.postJson(addr, data)
        else:
            return self.request.post(addr)
    
    def getMyDefaultAdministratorRights(self, for_channels=None):
        """
        使用此方法获取机器人的当前默认管理员权限
        """
        command = inspect.stack()[0].function
        addr = command

        data = {}
        if for_channels is not None:
            data["for_channels"] = bool(for_channels)
        
        if len(data) != 0:
            return self.request.postJson(addr, data)
        else:
            return self.request.post(addr)

    # Updating messages
    def editMessageText(self, text, chat_id=None, message_id=None, inline_message_id=None,
        parse_mode="Text", disable_web_page_preview=None,
        reply_markup=None, entities=None):
        """
        编辑一条文本消息.成功时，若消息为Bot发送则返回编辑后的消息，其他返回True
        在未指定inline_message_id的时候chat_id和message_id为必须存在的参数
        """
        command = inspect.stack()[0].function

        if inline_message_id is None:
            if message_id is None or chat_id is None:
                return False

        if inline_message_id is not None:
            addr = command + "?inline_message_id=" + str(inline_message_id)
        else:
            addr = command + "?chat_id=" + str(chat_id)
            addr += "&message_id=" + str(message_id)

        addr += "&text=" + quote(str(text))
        if parse_mode in ("Markdown", "MarkdownV2", "HTML"):
            addr += "&parse_mode=" + str(parse_mode)
        if disable_web_page_preview is not None:
            addr += "&disable_web_page_preview=" + \
                    str(disable_web_page_preview)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if entities is not None:
            addr += "&entities=" + json.dumps(entities)

        return self.request.post(addr)

    def editMessageCaption(self, chat_id=None, message_id=None,
        inline_message_id=None, caption=None, parse_mode="Text",
        reply_markup=None, caption_entities=None):
        """
        编辑消息的Caption。成功时，若消息为Bot发送则返回编辑后的消息，其他返回True
        在未指定inline_message_id的时候chat_id和message_id为必须存在的参数
        """
        command = inspect.stack()[0].function
        if inline_message_id is None:
            if message_id is None or chat_id is None:
                return False

        if inline_message_id is not None:
            addr = command + "?inline_message_id=" + str(inline_message_id)
        else:
            addr = command + "?chat_id=" + str(chat_id)
            addr += "&message_id=" + str(message_id)

        if caption is not None:
            addr += "&caption=" + quote(str(caption))
        if parse_mode in ("Markdown", "MarkdownV2", "HTML"):
            addr += "&parse_mode=" + str(parse_mode)
        if reply_markup is not None:
            addr += "&reply_markup=" + str(reply_markup)
        if caption_entities is not None:
            addr += "&caption_entities=" + json.dumps(caption_entities)

        return self.request.post(addr)

    def editMessageMedia(self, media, type_, chat_id=None, message_id=None,
        caption=None, parse_mode=None, inline_message_id=None, reply_markup=None):
        """
        编辑消息媒体
        在未指定inline_message_id的时候chat_id和message_id为必须存在的参数
        media_dict format(not bytes):
        media_dict = {
            'media':{
                    'type': 'photo',
                    'media': 'uri or file_id',
                    'caption': 'caption'
            }
        }

        refer https://stackoverflow.com/questions/63843589/telegram-editmessagemedia-alternative-for-telepot
        """
        command = inspect.stack()[0].function
        if inline_message_id is None:
            if message_id is None or chat_id is None:
                return False

        if inline_message_id is not None:
            addr = command + "?inline_message_id=" + str(inline_message_id)
        else:
            addr = command + "?chat_id=" + str(chat_id)
            addr += "&message_id=" + str(message_id)

        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)

        if media[:7] == "http://" or media[:7] == "https:/":
            file_data = None
            media_dict = {
                'media':{
                    'type': str(type_),
                    'media': str(media)
                }
            }
        elif type(media) == bytes:
            file_data = {
                'media': media,
            }
            media_dict = {
                'type': str(type_),
                'media': "attach://media",
            }
        elif type(media) == str and '.' not in media:
            file_data = None
            media_dict = {
                'media':{
                    'type': str(type_),
                    'media': str(media)
                }
            }
        else:
            file_data = {
                'media': open(str(media), "rb"),
            }
            media_dict = {
                'type': str(type_),
                'media': "attach://media",
            }

        if file_data is not None:
            if caption is not None:
                media_dict["caption"] = str(caption)
            if parse_mode is not None:
                if parse_mode in ("Markdown", "MarkdownV2", "HTML"):
                    media_dict["parse_mode"] = str(parse_mode)
        else:
            if caption is not None:
                media_dict["media"]["caption"] = str(caption)
            if parse_mode is not None:
                if parse_mode in ("Markdown", "MarkdownV2", "HTML"):
                    media_dict["media"]["parse_mode"] = str(parse_mode)

        if file_data is not None:
            media_json = json.dumps(media_dict)
            addr += f"&media={media_json}"
            return self.request.postFile(addr, file_data)
        else:
            return self.request.postJson(addr, media_dict)

    def editMessageReplyMarkup(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        """
        编辑MessageReplyMarkup
        在未指定inline_message_id的时候chat_id和message_id为必须存在的参数
        """
        command = inspect.stack()[0].function
        if inline_message_id is None:
            if message_id is None or chat_id is None:
                return False

        if inline_message_id is not None:
            addr = command + "?inline_message_id=" + str(inline_message_id)
        else:
            addr = command + "?chat_id=" + str(chat_id)
            addr += "&message_id=" + str(message_id)

        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)

        return self.request.post(addr)

    def stopPoll(self, chat_id, message_id, reply_markup=None):
        """
        停止投票？并返回最终结果
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&message_id=" + str(message_id)

        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)

        return self.request.post(addr)

    def deleteMessage(self, chat_id, message_id):
        """
        删除一条消息，机器人必须具备恰当的权限
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&message_id=" + str(message_id)
        
        return self.request.post(addr)

    def createForumTopic(self, chat_id, name, icon_color=None, icon_custom_emoji_id=None):
        """
        使用此方法在论坛超组聊天中创建主题
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&name=" + str(name)

        if icon_color is not None:
            addr += "&icon_color=" + str(icon_color)
        if icon_custom_emoji_id is not None:
            addr += "&icon_custom_emoji_id=" + str(icon_custom_emoji_id)

        return self.request.post(addr)

    def editForumTopic(self, chat_id, message_thread_id,
    name=None, icon_custom_emoji_id=None):
        """
        使用此方法在论坛超组聊天中编辑主题的名称和图标
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)
        addr += "&message_thread_id=" + str(message_thread_id)

        if name is not None:
            addr += "&name=" + str(name)
        if icon_custom_emoji_id is not None:
            addr += "&icon_custom_emoji_id=" + str(icon_custom_emoji_id)

        return self.request.post(addr)

    def closeForumTopic(self, chat_id, message_thread_id):
        """
        使用此方法在论坛超组聊天中关闭一个公开主题
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&message_thread_id=" + str(message_thread_id)
        
        return self.request.post(addr)

    def reopenForumTopic(self, chat_id, message_thread_id):
        """
        使用此方法在论坛超组聊天中重新打开一个封闭的主题
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&message_thread_id=" + str(message_thread_id)
        
        return self.request.post(addr)

    def deleteForumTopic(self, chat_id, message_thread_id):
        """
        使用此方法在论坛超组聊天中删除论坛主题以及其所有消息
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&message_thread_id=" + str(message_thread_id)
        
        return self.request.post(addr)

    def unpinAllForumTopicMessages(self, chat_id, message_thread_id):
        """
        使用此方法清除论坛主题中的固定消息列表
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id) + "&message_thread_id=" + str(message_thread_id)
        
        return self.request.post(addr)

    def getForumTopicIconStickers(self):
        """
        使用此方法获取自定义表情符号贴纸
        任何用户都可以用作论坛主题图标
        不需要参数。返回一系列贴纸对象
        """
        command = inspect.stack()[0].function
        addr = command

        return self.request.post(addr)

    def editGeneralForumTopic(self, chat_id, name):
        """
        使用此方法在论坛超组聊天中编辑"General"主题的名称。
        """
        command = inspect.stack()[0].function
        addr += command + "?chat_id=" + str(chat_id)
        addr += "&name=" + str(name)

        return self.request.post(addr)

    def closeGeneralForumTopic(self, chat_id):
        """
        使用此方法在论坛超级聊天中关闭一个开放的"General"主题。
        """
        command = inspect.stack()[0].function
        addr += command + "?chat_id=" + str(chat_id)

        return self.request.post(addr)

    def reopenGeneralForumTopic(self, chat_id):
        """
        使用此方法在论坛SuperGroup聊天中重新打开一个封闭的"General"主题。
        """
        command = inspect.stack()[0].function
        addr += command + "?chat_id=" + str(chat_id)

        return self.request.post(addr)

    def hideGeneralForumTopic(selfr, chat_id):
        """
        使用此方法在论坛超组聊天中隐藏"General"主题。
        """
        command = inspect.stack()[0].function
        addr += command + "?chat_id=" + str(chat_id)

        return self.request.post(addr)

    def unhideGeneralForumTopic(sel, chat_id):
        """
        使用此方法在论坛超级聊天中解开"General"主题。
        """
        command = inspect.stack()[0].function
        addr += command + "?chat_id=" + str(chat_id)

        return self.request.post(addr)


    # Inline mode
    def answerInlineQuery(self, inline_query_id, results, cache_time=None,
        is_personal=None, next_offset=None, button=None):
        """
        使用此方法发送Inline mode的应答
        results format:
            results = [
                {
                    "type": "article",
                    "id": "item_id_1",
                    "title": "Item 1",
                    "input_message_content": {
                        "message_text": "123",
                        "parse_mode": "HTML"
                    }
                },
                {
                    "type": "article",
                    "id": "item_id_2",
                    "title": "Item 2",
                    "input_message_content": {
                        "message_text": "456",
                        "parse_mode": "HTML"
                    }
                }
            ]
        """
        command = inspect.stack()[0].function
        addr = command + "?inline_query_id=" + str(inline_query_id)
        addr += "&results=" + json.dumps(results)

        if cache_time is not None:
            addr += "&cache_time=" + str(cache_time)
        if is_personal is not None:
            addr += "&is_personal=" + str(is_personal)
        if next_offset is not None:
            addr += "&next_offset=" + str(next_offset)
        if button is not None:
            addr += "&button=" + json.dumps(button)
        
        return self.request.post(addr)

    def answerCallbackQuery(self, callback_query_id, text=None, show_alert=False, url=None, cache_time=0):
        """
        使用此方法发送CallbackQuery的应答
        InlineKeyboardMarkup格式:
        replyKeyboard = [
        [
            {  "text": "命令菜单","callback_data":"/start"},
            {  "text": "一排之二","url":"https://google.com"}
        ],
        [
            { "text": "二排之一","url":"https://google.com"},
            { "text": "二排之二","url":"https://google.com"},
            { "text": "二排之三","url":"https://google.com"}
        ]
        ]
        reply_markup = {
            "inline_keyboard": replyKeyboard
        }
        ReplyKeyboardMarkup格式(似乎不能用于群组):
        replyKeyboard = [
        [
            {  "text": "命令菜单"},
            {  "text": "一排之二"}
        ],
        [
            { "text": "二排之一"},
            { "text": "二排之二"},
            { "text": "二排之三"}
        ]
        ]
        reply_markup = {
        "keyboard": replyKeyboard,
        "resize_keyboard": bool("false"),
        "one_time_keyboard": bool("false"),
        "selective": bool("true")
        }
        ReplyKeyboardRemove格式:
        reply_markup = {
        "remove_keyboard": bool("true"),
        "selective": bool("true")
        }
        """
        command = inspect.stack()[0].function
        addr = command + "?callback_query_id=" + str(callback_query_id)

        if text is not None:
            addr += "&text=" + quote(str(text))
        if show_alert == True:
            addr += "&show_alert=true"
        if url is not None:
            addr += "&url=" + str(url)
        if cache_time != 0:
            addr += "&cache_time=" + str(cache_time)

        return self.request.post(addr)

    def answerWebAppQuery(web_app_query_id, result):
        """
        使用此方法设置与Web App的互动结果
        并代表用户向查询来源的聊天室发送相应的消息
        """
        command = inspect.stack()[0].function
        addr = command

        data = {}
        data["web_app_query_id"] = str(web_app_query_id)
        data["result"] = result
        
        return self.request.postJson(addr, data)
    

    # Stickers
    def sendSticker(self, chat_id, sticker, emoji=None, disable_notification=None,
        reply_to_message_id=None, reply_markup=None, allow_sending_without_reply=None,
        protect_content=None, message_thread_id=None):
        """
        使用此方法发送静态、webp或动画、tgs贴纸
        """
        command = inspect.stack()[0].function

        if sticker[:7] == "http://" or sticker[:7] == "https:/":
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&sticker=" + sticker
        elif type(sticker) == bytes:
            file_data = {"sticker": sticker}
            addr = command + "?chat_id=" + str(chat_id)
        elif type(sticker) == str and '.' not in sticker:
            file_data = None
            addr = command + "?chat_id=" + str(chat_id) + "&sticker=" + sticker
        else:
            file_data = {"sticker": open(sticker, 'rb')}
            addr = command + "?chat_id=" + str(chat_id)

        if emoji is not None:
            addr += "&emoji=" + str(emoji)
        if disable_notification is not None:
            addr += "&disable_notification=" + str(disable_notification)
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        if file_data is None:
            return self.request.post(addr)
        else:
            return self.request.postFile(addr, file_data)

    def getStickerSet(self, name):
        """
        使用此方法获取贴纸集
        """
        command = inspect.stack()[0].function
        addr = command + "?name=" + str(name)

        return self.request.post(addr)
    
    def getCustomEmojiStickers(self, custom_emoji_ids):
        """
        使用此方法通过其标识符获取有关自定义表情符号贴纸的信息
        返回一系列贴纸对象
        """
        command = inspect.stack()[0].function
        addr = command
        data = {}
        data["custom_emoji_ids"] = custom_emoji_ids

        return self.request.postJson(addr, data)

    def uploadStickerFile(self, user_id, sticker, sticker_format):
        """
        使用此方法上传一个带有贴纸的文件
        以便以后在createNewStickerSet和addStickerToSet方法中使用（该文件可以多次使用）
        成功时返回上传的文件
        """
        command = inspect.stack()[0].function
        addr = command + "?user_id=" + str(user_id)
        addr += "&sticker_format=" + str(sticker_format)
        
        return self.request.postFile(addr, sticker)

    def createNewStickerSet(self, user_id, name, title, stickers, sticker_format,
            sticker_type=None, needs_repainting=None):
        """
        使用此方法可以创建用户拥有的新贴纸集
        机器人将能够编辑由此创建的贴纸集
        """
        command = inspect.stack()[0].function
        addr = command + "?user_id=" + str(user_id)
        addr += "&name=" + str(name)
        addr += "&title=" + str(title)
        addr += "&sticker_format=" + str(sticker_format)

        if sticker_type is not None:
            addr += "&sticker_type=" + str(sticker_type)
        if needs_repainting is not None:
            addr += "&needs_repainting=" + str(needs_repainting)

        return self.request.postJson(addr, stickers)

    def addStickerToSet(self, user_id, name, sticker):
        """
        使用此方法可以将新标签添加到由机器人创建的集合中
        可以将动画贴纸添加到动画贴纸集中，并且只能添加到它们
        动画贴纸集最多可以包含50个贴纸。 静态贴纸集最多可包含120个贴纸
        """
        command = inspect.stack()[0].function
        addr = command + "?user_id=" + str(user_id)
        addr += "&name=" + str(name)

        return self.request.postJson(addr, sticker)

    def setStickerPositionInSet(self, sticker, position):
        """
        使用此方法将机器人创建的一组贴纸移动到特定位置
        """
        command = inspect.stack()[0].function
        addr = command + "?sticker=" + str(sticker)
        addr += "&position=" + str(position)

        return self.request.post(addr)

    def deleteStickerFromSet(self, sticker):
        """
        使用此方法从机器人创建的集合中删除贴纸
        """
        command = inspect.stack()[0].function
        addr = command + "?sticker=" + str(sticker)

        return self.request.post(addr)

    def setStickerSetThumbnail(self, name, user_id, thumbnail=None):
        """
        使用此方法设置贴纸集的缩略图
        只能为动画贴纸集设置动画缩略图
        """
        command = inspect.stack()[0].function
        addr = command + "?name=" + str(name)
        addr += "&user_id=" + str(user_id)

        if thumbnail is not None:
            if thumbnail[:7] == "http://" or thumbnail[:7] == "https:/":
                file_data = None
                addr += "&thumbnail=" + thumbnail
            elif type(thumbnail) == bytes:
                file_data = {"thumbnail": thumbnail}
            elif type(thumbnail) == str and '.' not in thumbnail:
                file_data = None
                addr += "&thumbnail=" + thumbnail
            else:
                file_data = {"thumbnail": open(thumbnail, 'rb')}

        if file_data is None:
            return self.request.post(addr)
        else:
            return self.request.postFile(addr, file_data)
        
    def setCustomEmojiStickerSetThumbnail(self, name, custom_emoji_id=""):
        """
        使用此方法来设置自定义表情贴纸集的缩略图
        """
        command = inspect.stack()[0].function
        addr = command + "?name=" + str(name)
        addr += "&custom_emoji_id=" + str(custom_emoji_id)

        return self.request.post(addr)
    
    def setStickerSetTitle(self, name, title):
        """
        使用此方法来设置已创建的贴纸集的标题
        """
        command = inspect.stack()[0].function
        addr = command + "?name=" + str(name)
        addr += "&custom_emoji_id=" + str(title)

        return self.request.post(addr)
    
    def deleteStickerSet(self, name):
        """
        使用此方法删除一个由机器人创建的贴纸集
        """
        command = inspect.stack()[0].function
        addr = command + "?name=" + str(name)

        return self.request.post(addr)
    
    def setStickerEmojiList(self, sticker, emoji_list):
        """
        使用这个方法来改变分配给普通或自定义表情贴纸的表情符号列表
        该贴纸必须属于由机器人创建的贴纸集
        """
        command = inspect.stack()[0].function
        addr = command + "?sticker=" + str(sticker)

        return self.request.postJson(addr, emoji_list)
    
    def setStickerKeywords(self, sticker, keywords=None):
        """
        使用这种方法来改变分配给普通或自定义表情符号贴纸的搜索关键词
        该贴纸必须属于由机器人创建的贴纸集
        """
        command = inspect.stack()[0].function
        addr = command + "?sticker=" + str(sticker)

        if keywords is not None:
            return self.request.postJson(addr, keywords)
        else:
            return self.request.post(addr)
        
    def setStickerMaskPosition(self, sticker, mask_position=None):
        """
        使用这个方法来改变一个面具贴纸的面具位置
        该贴纸必须属于一个由机器人创建的贴纸集
        """
        command = inspect.stack()[0].function
        addr = command + "?sticker=" + str(sticker)

        if mask_position is not None:
            return self.request.postJson(addr, mask_position)
        else:
            return self.request.post(addr)

    # Payments
    def sendInvoice(self, chat_id, title, description, payload, provider_token,
                    currency, prices, start_parameter=None, provider_data=None, photo_url=None,
                    photo_size=None, photo_width=None, photo_height=None,
                    need_name=None, need_phone_number=None, need_email=None,
                    need_shipping_address=None, send_phone_number_to_provider=None,
                    send_email_to_provider=None, is_flexible=None, disable_notification=None,
                    reply_to_message_id=None, reply_markup=None, allow_sending_without_reply=None,
                    max_tip_amount=None, suggested_tip_amounts=None, protect_content=None,
                    message_thread_id=None):
        """
        使用此方法发送发票
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)
        addr += "&title=" + str(title)
        addr += "&description=" + str(description)
        addr += "&payload" + str(payload)
        addr += "&provider_token=" + str(provider_token)
        addr += "&currency=" + str(currency)
        addr += "&prices=" + json.dumps(prices)

        if start_parameter is not None:
            addr += "&start_parameter=" + str(start_parameter)
        if provider_data is not None:
            addr += "&provider_data=" + str(provider_data)
        if photo_url is not None:
            addr += "&photo_url=" + str(photo_url)
        if photo_size is not None:
            addr += "&photo_size=" + str(photo_size)
        if photo_width is not None:
            addr += "&photo_width=" + str(photo_width)
        if photo_height is not None:
            addr += "&photo_height=" + str(photo_height)
        if need_name is not None:
            addr += "&need_name=" + str(need_name)
        if need_phone_number is not None:
            addr += "&need_phone_number=" + str(need_phone_number)
        if need_email is not None:
            addr += "&need_email=" + str(need_email)
        if need_shipping_address is not None:
            addr += "&need_shipping_address=" + str(need_shipping_address)
        if send_phone_number_to_provider is not None:
            addr += "&send_phone_number_to_provider=" + \
                    str(send_phone_number_to_provider)
        if send_email_to_provider is not None:
            addr += "&send_email_to_provider=" + str(send_email_to_provider)
        if is_flexible is not None:
            addr += "&is_flexible=" + str(is_flexible)
        if disable_notification is not None:
            addr += "&disable_notification=" + str(disable_notification)
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if max_tip_amount is not None:
            addr += "&max_tip_amount=" + str(max_tip_amount)
        if suggested_tip_amounts is not None:
            addr += "&suggested_tip_amounts=" + str(suggested_tip_amounts)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        return self.request.post(addr)

    def createInvoiceLink(self, title, description, payload, provider_token, currency,
        prices, max_tip_amount=None, suggested_tip_amounts=None, provider_data=None,
        photo_url=None, photo_size=None, photo_width=None, photo_height=None,
        need_name=None, need_phone_number=None, need_email=None,
        need_shipping_address=None, send_phone_number_to_provider=None,
        send_email_to_provider=None, is_flexible=None
        ):
        """
        使用此方法为发票创建链接
        返回创建的发票链接作为成功的字符串
        """
        command = inspect.stack()[0].function
        addr = command + "?title=" + str(title)
        addr += "&description=" + str(description)
        addr += "&payload" + str(payload)
        addr += "&provider_token=" + str(provider_token)
        addr += "&currency=" + str(currency)
        addr += "&prices=" + json.dumps(prices)

        if max_tip_amount is not None:
            addr += "&max_tip_amount=" + str(max_tip_amount)
        if suggested_tip_amounts is not None:
            addr += "&suggested_tip_amounts=" + json.dumps(suggested_tip_amounts)
        if provider_data is not None:
            addr += "&provider_data=" + str(provider_data)
        if photo_url is not None:
            addr += "&photo_url=" + str(photo_url)
        if photo_size is not None:
            addr += "&photo_size=" + str(photo_size)
        if photo_width is not None:
            addr += "&photo_width=" + str(photo_width)
        if photo_height is not None:
            addr += "&photo_height=" + str(photo_height)
        if need_name is not None:
            addr += "&need_name=" + str(need_name)
        if need_phone_number is not None:
            addr += "&need_phone_number=" + str(need_phone_number)
        if need_email is not None:
            addr += "&need_email=" + str(need_email)
        if need_shipping_address is not None:
            addr += "&need_shipping_address=" + str(need_shipping_address)
        if send_phone_number_to_provider is not None:
            addr += "&send_phone_number_to_provider=" + \
                    str(send_phone_number_to_provider)
        if send_email_to_provider is not None:
            addr += "&send_email_to_provider=" + str(send_email_to_provider)
        if is_flexible is not None:
            addr += "&is_flexible=" + str(is_flexible)

        return self.request.post(addr)
        
    def answerShippingQuery(self, shipping_query_id, ok, shipping_options=None, error_message=None):
        """
        使用此方法可以答复运输查询
        """
        command = inspect.stack()[0].function
        addr = command + "?shipping_query_id=" + str(shipping_query_id)
        addr += "&ok=" + str(ok)

        if shipping_options is not None:
            addr += "&shipping_options=" + json.dumps(shipping_options)
        if error_message is not None:
            addr += "&error_message=" + str(error_message)

        return self.request.post(addr)

    def answerPreCheckoutQuery(self, pre_checkout_query_id, ok, error_message=None):
        """
        使用此方法来响应此类预结帐查询
        """
        command = inspect.stack()[0].function
        addr = command + "?pre_checkout_query_id=" + str(pre_checkout_query_id)
        addr += "&ok=" + str(ok)

        if error_message is not None:
            addr += "&error_message=" + str(error_message)

        return self.request.post(addr)

    # Telegram Passport

    def setPassportDataErrors(self, user_id, errors):
        """
        通知用户他们提供的某些Telegram Passport元素包含错误
        在错误纠正之前，用户将无法重新提交其护照
        （错误返回字段的内容必须更改）
        """
        command = inspect.stack()[0].function
        addr = command + "?user_id=" + str(user_id)
        addr += "&errors=" + json.dumps(errors)

        return self.request.post(addr)

    # Games

    def sendGame(self, chat_id, game_short_name, disable_notification=None,
        reply_to_message_id=None, reply_markup=None, allow_sending_without_reply=None,
        protect_content=None, message_thread_id=None):
        """
        使用此方法发送游戏
        """
        command = inspect.stack()[0].function
        addr = command + "?chat_id=" + str(chat_id)
        addr += "&game_short_name=" + str(game_short_name)

        if disable_notification is not None:
            addr += "&disable_notification=" + str(disable_notification)
        if reply_to_message_id is not None:
            addr += "&reply_to_message_id=" + str(reply_to_message_id)
        if reply_markup is not None:
            addr += "&reply_markup=" + json.dumps(reply_markup)
        if allow_sending_without_reply is not None:
            addr += "&allow_sending_without_reply=" + str(allow_sending_without_reply)
        if protect_content is not None:
            addr += "&protect_content=" + str(protect_content)
        if message_thread_id is not None:
            addr += "&message_thread_id=" + str(message_thread_id)

        return self.request.post(addr)

    def setGameScore(self, user_id, score, force=None, disable_edit_message=None,
                    chat_id=None, message_id=None, inline_message_id=None):
        """
        使用此方法设置游戏中指定用户的分数
        在未指定inline_message_id的时候chat_id和message_id为必须存在的参数
        """
        command = inspect.stack()[0].function

        if inline_message_id is None:
            if message_id is None or chat_id is None:
                return False

        if inline_message_id is not None:
            addr = command + "?inline_message_id=" + str(inline_message_id)
        else:
            addr = command + "?chat_id=" + str(chat_id)
            addr += "&message_id=" + str(message_id)

        addr += "&user_id=" + str(user_id)
        addr += "&score=" + str(score)

        if force is not None:
            addr += "&force=" + str(force)
        if disable_edit_message is not None:
            addr += "&disable_edit_message=" + str(disable_edit_message)

        return self.request.post(addr)

    def getGameHighScores(self, user_id, chat_id=None, message_id=None, inline_message_id=None):
        """
        使用此方法获取高分表的数据
        将返回指定用户及其在游戏中几个邻居的分数
        在未指定inline_message_id的时候chat_id和message_id为必须存在的参数
        """
        command = inspect.stack()[0].function

        if inline_message_id is None:
            if message_id is None or chat_id is None:
                return False

        if inline_message_id is not None:
            addr = command + "?inline_message_id=" + str(inline_message_id)
        else:
            addr = command + "?chat_id=" + str(chat_id)
            addr += "&message_id=" + str(message_id)

        addr += "&user_id=" + str(user_id)

        return self.request.post(addr)
