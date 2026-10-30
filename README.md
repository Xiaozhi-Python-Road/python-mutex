# python-mutex

## Hi, everyone! I'm Xiaozhi. Welcome to the Python-Mutex project. This is a mutex lock implemented by calling the Windows api through the ctypes module based on the python language. It provides a single-process instance to prevent the trouble caused by starting a second process

### requirement：
### Only Windows platform is supported. Thank you. This project is not applicable to platforms other than Windows such as Linux and mac. If you want to download the source code quickly, you can download the project code(downloadable)-v1.0.zip in the repository!

### If you need local help documentation, you can:
| doc | url |
| ---- | ---- |
| chinese-help |[open/download](./resources_help/python-mutex-chinese.pdf)
| english-help |[open/download](./resources_help/python-mutex-english.pdf)

### Let'sget started with the introduction

The project structure is as follows (the Backstage_framework folder needsto be placed in the same directory as the script.
Among them, admin_pression.py is suitable for checkingadministrator/non-administrator permissions! Mutex.py is the core oftheMutex lock, and main.py is responsible for its invocation。

```
python-mutex
|--Backstage_framework
|   |--Mutex
|     |---Mutex.py
|   |--admin_pression
|     |--admin_uac.py
|--main.py
```

## The complete code can be found in the source code admin_uac.py. Theexplanation is as follows:
## In the function call, check_admin.process_admin() is used to checkwhether the current process has been elevated. If it is running, if not,relaunch_admin() is used to restart itself, then uac is initiated forelevation, and finally,...... is run as an administrator
### You can also use local_admin() to check. You can change process_admin()to the local_admin() function, but you need to know the risks:
### If the currently logged-in Windows account is not in the administratorgroup (SID), the uac may become invalid and a password needs to be enteredfor confirmation. This function is feasible, but the condition is thatthe currently logged-in account must be in the administrator group. Undernormal circumstances, it is recommended to use the process_admin()function to check whether the current process has been extracted!14
### By default, you need administrator privileges to run it because thedefault session is local\\. Non-administrators need to add Global\\
```python
# main.py
from Backstage_framework.admin_pression import admin_uac

check_admin = admin_uac.Check_the_administrator()
if check_admin.process_admin(): # local_admin()
  main()
else:
  check_admin.relaunch_admin()
```
### Mutex:
### When you call a check_the_ultimate_mutex_lock(), the namespace isalways ready. You need to pass a string in parentheses as your mutexname. If you need to run it under a non-administrator, you must addGlobal\.\ Because Windows defaults to the Loacl\\ session; otherwise, itwill fail silently
### At the same time, when you call a hook calledultimate_defense_against_process_hooks, this lock will be synchronized. As longasthe process exists, this lock exists, but the lock management handle needs to bereleased. Therefore, a finally function needs to be placed here to ensure thatregardless of success or failure, Then this lock can be cleared normally. Thank you!
```python
# main.py

from Backstage_framework.Mutex import Mutex
from Backstage_framework.admin_pression import admin_uac
import sys

def main():
    input('your running')

if __name__ == '__main__':
    app = Mutex.Ultimate_mutex()
    check_admin = admin_uac.Check_the_administrator()

    mutex_handle,exits = app.check_the_ultimate_mutex_lock('we name') # if it is not runby an administrator, Global\\ needs to be added
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
```
### This place must be placed before your main() function so as to blockmultiple instances before UAC is created!
```python
 app = Mutex.Ultimate_mutex()

 mutex_handle,exits = app.check_the_ultimate_mutex_lock('we name')
 if exits:
  sys.exit(1)
```

### In practical use, for example：
```python
from Backstage_framework.Mutex import Mutex
from Backstage_framework.admin_pression import admin_uac
import sys

import tkinter as tk

def main():
  root = tk.Tk()
  root.mainloop()


if __name__ == '__main__':
    app = Mutex.Ultimate_mutex()
    check_admin = admin_uac.Check_the_administrator()

    mutex_handle,exits = app.check_the_ultimate_mutex_lock('Global\\we name') # if it is not runby an administrator, Global\\ needs to be added
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
```
