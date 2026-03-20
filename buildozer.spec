[app]

title = Quản lý dịch vụ
package.name = quanlydichvu
package.domain = org.quanlydichvu
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,db
version = 1.0.0
requirements = python3,kivy==2.1.0,kivymd==1.1.1,xlsxwriter
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0

[buildozer]
log_level = 2

[android]
api = 33
minapi = 21
ndk = 25b
archs = arm64-v8a
permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.accept_sdk_license = True
