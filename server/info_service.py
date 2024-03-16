import shutil
import socket
from collections import OrderedDict

import requests
import psutil

from configs.constants import DISK_ROOT_PATH, BYTES_IN_GB, ROUTER_ADDR
from logs.logger import server_logger


class ServerAddress:

    def __init__(self):
        self.__api_ip = "https://httpbin.org/ip"
        self.__api_data = "https://ipinfo.io/%s/json"
        self.__public_dns = "8.8.8.8"

    def get(self) -> OrderedDict:
        public_ip = self._get_public_ip()
        local_ip = self._get_local_ip()
        local_vpn_ip = self._get_local_vpn_ip()
        info = self._get_info(public_ip=public_ip, local_ip=local_ip, local_vpn_ip=local_vpn_ip)
        return info

    def _get_public_ip(self) -> str:
        public_ip = ""
        warn_msg = "Failed to retrieve public IP"
        try:
            response = requests.get(self.__api_ip)
            if response.status_code == 200:
                data = response.json()
                public_ip = data.get("origin")
                return public_ip
            else:
                server_logger.warning(warn_msg)
                raise Exception(warn_msg)
        except Exception:
            server_logger.warning(warn_msg)
            raise Exception(warn_msg)
        finally:
            return public_ip

    def _get_local_ip_data(self, dns: str) -> str:
        local_addr = ""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((dns, 80))
            local_addr = s.getsockname()[0]
            s.close()
            return local_addr
        except Exception:
            msg = "Failed to retrieve local IP"
            server_logger.warning(msg)
            raise Exception(msg)
        finally:
            return local_addr

    def _get_local_vpn_ip(self):
        return self._get_local_ip_data(dns=self.__public_dns)

    def _get_local_ip(self):
        return self._get_local_ip_data(dns=ROUTER_ADDR)

    def _get_info(self, public_ip, local_ip, local_vpn_ip) -> OrderedDict:
        structured_data = OrderedDict([("*Public IP*", public_ip), ("Country Code", ""), ("City", ""),
                                       ("Region", ""), ("Timezone", ""), ("Provider", ""),
                                       ("*Local IP*", f"`{local_ip}`"), ("*Local VPN IP*", f"`{local_vpn_ip}`")])
        try:
            response = requests.get(self.__api_data % (public_ip,))
            if response.status_code == 200:
                data = response.json()
                structured_data["*Public IP*"] = f"`{data.get('ip')}`"
                structured_data["Country Code"] = data.get("country")
                structured_data["City"] = data.get("city")
                structured_data["Region"] = data.get("region")
                structured_data["Timezone"] = data.get("timezone")
                structured_data["Provider"] = data.get("org")
                return structured_data
        except Exception:
            msg = "Failed to retrieve IP information"
            server_logger.warning(msg)
            raise Exception(msg)
        finally:
            return structured_data


class HardwareStat:

    def get(self) -> OrderedDict:
        structured_data = OrderedDict([("CPU load", ""), ("CPU temp", ""), ("RAM free", ""),
                                       ("RAM total", ""), ("Disk free space", "")])
        try:
            structured_data["CPU load"] = self._get_cpu_load()
            structured_data["CPU temp"] = self._get_cpu_temp()
            ram_free, ram_total = self._get_ram_data()
            structured_data["RAM free"] = ram_free
            structured_data["RAM total"] = ram_total
            structured_data["Disk free space"] = self._get_free_disk_space_for_downloads()
            return structured_data
        except Exception:
            msg = "Failed to retrieve hardware information"
            server_logger.warning(msg)
            raise Exception(msg)
        finally:
            return structured_data

    @classmethod
    def _get_cpu_load(cls):
        return f"{'%.1f' % (psutil.cpu_percent(),)}%"

    @classmethod
    def _get_cpu_temp(cls) -> str:
        return f"{psutil.sensors_temperatures()['coretemp'][0].current}°C"

    @classmethod
    def _get_ram_data(cls) -> tuple:
        ram_info = psutil.virtual_memory()
        total = f"{'%.3f' % ((ram_info.total / 1073741824),)} GB"
        free = f"{'%.3f' % ((ram_info.available / 1073741824),)} GB"
        return free, total

    @classmethod
    def _get_free_disk_space_for_downloads(cls) -> str:
        return f"{'%.3f' % ((shutil.disk_usage(DISK_ROOT_PATH).free / BYTES_IN_GB),)} GB"
