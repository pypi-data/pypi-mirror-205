from django.apps import AppConfig
import os
import json
import copy

class MakasuipatchConfig(AppConfig):
    name = 'makasuipatch'
    def ready(self):
        try:
            print("+-" * 5 + "    Simple UI Pro Patch by Makabaka   " + "+-" * 5)
            print("文件: " + __file__)

            from simplepro import conf
            from simplepro import handlers
            from simplepro.utils import write_obj
            from simplepro.group import view
            
            lic_file = os.path.join(os.getcwd(), 'simplepro.lic')
            default_licinfo =  {
                    "end_date": "2099-12-25 19:52:34",
                    "device_id": conf.get_device_id(),
                    "code": "玛卡巴卡福利版 有条件请支持正版",
            }
            
            def offline_active(request):
                code = request.POST.get('code')
                r = online_active_code(code)
                if r:
                    return r
                data = {"state": True, "msg": "ok"}
                return write_obj(data)

            def online_active_code(code):
                d = copy.deepcopy(default_licinfo)
                d['code'] = f"{code}"
                json.dump(d, open(lic_file, "w+"))
                
                data = {"state": True, "msg": "ok", "license":f"{code}"}
                return write_obj(data)
            
            def get_licence_file_info(reload=False):
                d = default_licinfo
                if os.path.exists(lic_file):
                    d = json.load(open(lic_file, "r"))
                return d

            def is_active(request):
                return True

            def process_lic(request):
                # 调用服务器接口，获取激活信息，如果激活成功，就覆盖本地文件
                # 直接跳过服务器验证 直接返回信息
                data = {"state": True, "msg": "ok"}
                active_code = request.POST.get('active_code')
                r = online_active_code(active_code)
                if r:
                    return r
                return write_obj(data)
            # 离线激活
            view.offline_active = offline_active
            
            handlers.process_lic = process_lic
            handlers.OO0O0OO0OOO0OO0O0 = is_active
            handlers.O0O0OOO0OOO0OO0O0 = get_licence_file_info
            handlers.online_active_code = online_active_code
        except Exception as e:
            print(e)
