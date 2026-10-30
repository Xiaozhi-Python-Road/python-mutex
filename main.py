from Backstage_framework.Mutex import Mutex
from Backstage_framework.admin_pression import admin_uac
import sys

def main():
    input('已经运行')

if __name__ == '__main__':
    app = Mutex.Ultimate_mutex()
    check_admin = admin_uac.Check_the_administrator()

    mutex_handle,exits = app.check_the_ultimate_mutex_lock('我的互斥名字') # 如果是非管理员运行，需要加上Global\\
    if exits:
        sys.exit(1)

    if check_admin.process_admin():
        if app.ultimate_defense_against_process_hooks():
            try:
                main()
            finally:
                app.release_mutex()
                app.close_mutex()
    else:
        check_admin.relaunch_admin()




