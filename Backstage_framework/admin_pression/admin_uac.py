import ctypes, sys
from ctypes import wintypes

class Check_the_administrator:

    TOKEN_QUERY = 0x0008
    TokenElevation = 20
    SECURITY_BUILTIN_DOMAIN_RID = 0x00000020
    DOMAIN_ALIAS_RID_ADMINS = 0x00000220
    NtCurrentProcess = wintypes.HANDLE(-1).value

    class SID_IDENTIFIER_AUTHORITY(ctypes.Structure):
        _fields_ = [("Value",ctypes.c_byte * 6)]

    class TOKEN_ELEVATION(ctypes.Structure):
        _fields_ = [("TokenIsElevated",wintypes.DWORD)]

    def __init__(self):
        self.advapi32 = ctypes.WinDLL('advapi32')
        self.ntdll = ctypes.WinDLL('ntdll')
        self.shell32 = ctypes.WinDLL('shell32')
        self._setup_struct()

    def _setup_struct(self):
        self.advapi32.AllocateAndInitializeSid.argtypes = [ctypes.POINTER(self.SID_IDENTIFIER_AUTHORITY),ctypes.c_byte,wintypes.DWORD,
        wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,ctypes.POINTER(ctypes.c_void_p)]
        self.advapi32.AllocateAndInitializeSid.restype = wintypes.BOOL

        self.advapi32.FreeSid.argtypes = [ctypes.c_void_p]
        self.advapi32.FreeSid.restype = ctypes.c_void_p

        self.advapi32.CheckTokenMembership.argtypes = [wintypes.HANDLE,ctypes.c_void_p,ctypes.POINTER(wintypes.BOOL)]
        self.advapi32.CheckTokenMembership.restype = wintypes.BOOL

        self.ntdll.NtOpenProcessToken.argtypes = [wintypes.HANDLE,wintypes.DWORD,ctypes.POINTER(wintypes.HANDLE)]
        self.ntdll.NtOpenProcessToken.restype = wintypes.LONG

        self.ntdll.NtQueryInformationToken.argtypes = [wintypes.HANDLE,ctypes.c_int,ctypes.c_void_p,wintypes.ULONG,ctypes.POINTER(wintypes.ULONG)]
        self.ntdll.NtQueryInformationToken.restype = wintypes.LONG

        self.ntdll.NtClose.argtypes = [wintypes.HANDLE]
        self.ntdll.NtClose.restype = wintypes.LONG

        self.shell32.ShellExecuteW.argtypes = [wintypes.HWND,wintypes.LPCWSTR,wintypes.LPCWSTR,
            wintypes.LPCWSTR,wintypes.LPCWSTR,ctypes.c_int]
        self.shell32.ShellExecuteW.restype = wintypes.HINSTANCE

    # ---------- 当前用户是否属于管理员组 ----------
    def local_admin(self):
        sid = ctypes.c_void_p()
        authority = self.SID_IDENTIFIER_AUTHORITY()
        authority.Value = (ctypes.c_byte * 6)(0,0,0,0,0,5)

        if not self.advapi32.AllocateAndInitializeSid(
            ctypes.byref(authority),2,
            self.SECURITY_BUILTIN_DOMAIN_RID,self.DOMAIN_ALIAS_RID_ADMINS,0,0,0,0,0,0,ctypes.byref(sid)):
            return False

        try:
            is_member = wintypes.BOOL()
            if not self.advapi32.CheckTokenMembership(None,sid,ctypes.byref(is_member)):
                return False
            return bool(is_member.value)
        finally:
            self.advapi32.FreeSid(sid)

    # ---------- 当前进程是否已提权 ----------
    def process_admin(self):
        h_token = wintypes.HANDLE()
        status = self.ntdll.NtOpenProcessToken(self.NtCurrentProcess,self.TOKEN_QUERY,ctypes.byref(h_token))
        if status != 0:
            return False

        try:
            elevation = self.TOKEN_ELEVATION()
            ret_len = wintypes.ULONG()
            status = self.ntdll.NtQueryInformationToken(h_token,self.TokenElevation,
                ctypes.byref(elevation),ctypes.sizeof(elevation),ctypes.byref(ret_len))
            if status != 0:
                return False
            return elevation.TokenIsElevated != 0
        finally:
            self.ntdll.NtClose(h_token)

    def relaunch_admin(self):
        self.shell32.ShellExecuteW(None,"runas",sys.executable,f'"{sys.argv[0]}"',None,1)
        sys.exit(0)