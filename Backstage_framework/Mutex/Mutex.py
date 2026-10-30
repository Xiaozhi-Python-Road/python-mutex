import ctypes,sys
from ctypes import wintypes

class Ultimate_mutex:

    INFINITE = 0xFFFFFFFF
    ERROR_ALREADY_EXISTS = 183

    WAIT_OBJECT_0 = 0x00000000
    WAIT_ABANDONED = 0x00000080
    WAIT_TIMEOUT = 0x00000102
    WAIT_FAILED = 0xFFFFFFFF

    def __init__(self):
        self.kernel32 = ctypes.WinDLL('kernel32')
        self.ntdll = ctypes.WinDLL('ntdll')
        self.user32 = ctypes.WinDLL('user32')
        self._setup_struct()
        self.mutex_handle = None

    def _setup_struct(self):
        self.kernel32.CreateMutexW.argtypes = [wintypes.LPVOID,wintypes.BOOL,wintypes.LPCWSTR]
        self.kernel32.CreateMutexW.restype = wintypes.HANDLE

        #self.ntdll.NtWaitForSingleObject.argtypes = [wintypes.HANDLE,wintypes.BOOL,ctypes.POINTER(ctypes.c_longlong)]
        #self.ntdll.NtWaitForSingleObject.restype = ctypes.c_long 已被微软弃用

        self.kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE,wintypes.DWORD]
        self.kernel32.WaitForSingleObject.restype = wintypes.DWORD

        self.ntdll.NtClose.argtypes = [wintypes.HANDLE]
        self.ntdll.NtClose.restype = ctypes.c_long

        self.ntdll.RtlGetLastWin32Error.argtypes = []
        self.ntdll.RtlGetLastWin32Error.restype = wintypes.DWORD

        self.user32.MessageBoxW.argtypes = [wintypes.HWND,wintypes.LPCWSTR,wintypes.LPCWSTR,wintypes.UINT]
        self.user32.MessageBoxW.restype = wintypes.INT

    def check_the_ultimate_mutex_lock(self,mutex_name):

        handle = self.kernel32.CreateMutexW(None,False,mutex_name)
        last_error = self.ntdll.RtlGetLastWin32Error()

        if not handle:
            self.user32.MessageBoxW(0,"互斥体创建失败！程序无法启动，请确保你的系统文件正常，随后重启重试！","小智Python之路提醒您：",0x10 | 0x40000)
            sys.exit(1)

        if last_error == self.ERROR_ALREADY_EXISTS:
            self.ntdll.NtClose(handle)
            self.user32.MessageBoxW(0,"程序已经在运行中，不可多开！请勿重复运行，否则无法获得官方技术支持！","小智Python之路提醒您：",0x10 | 0x40000)
            return None,True

        self.mutex_handle = handle
        return handle,False

    def ultimate_defense_against_process_hooks(self,timeout=None):
        if not self.mutex_handle:
            return False

        if timeout is None or timeout == self.INFINITE:
            wait_ms = self.INFINITE
        else:
            wait_ms = int(timeout)

        status = self.kernel32.WaitForSingleObject(self.mutex_handle, wait_ms)
        return status in (self.WAIT_OBJECT_0,self.WAIT_ABANDONED)

        '''if not self.mutex_handle: 已被微软弃用
            return False

        if timeout is None or timeout == self.INFINITE:
            status = self.ntdll.NtWaitForSingleObject(self.mutex_handle,False,None)
        else:
            tv = ctypes.c_longlong(-int(timeout) * 10000)
            status = self.ntdll.NtWaitForSingleObject(self.mutex_handle,False,ctypes.byref(tv))
        return status in (self.STATUS_SUCCESS, self.STATUS_ABANDONED)'''

    def release_mutex(self):
        if self.mutex_handle:
            self.kernel32.ReleaseMutex(self.mutex_handle)

    def close_mutex(self):
        if self.mutex_handle:
            self.ntdll.NtClose(self.mutex_handle)
            self.mutex_handle = None