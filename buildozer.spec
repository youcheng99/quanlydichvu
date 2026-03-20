[app]

# (str) Title of your application
title = Quản lý dịch vụ

# (str) Package name
package.name = quanlydichvu

# (str) Package domain (needed for android/ios packaging)
package.domain = org.quanlydichvu

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt,db

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.1.0,kivymd==1.1.1,xlsxwriter,pyjnius,android

# (str) Custom source folders for requirements
#requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# OSX Specific
#
#
# author = © Copyright Info
# Author credit
author = BS Thành

# Copyright notice
copyright = 2024

# Comment out the following to prevent signing a with debug key
#android.debug = 1

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy package data to buffer instead of reading from source
#android.copy_package_data = True

# (str) Extra Android manifest package arguments
#android.extra_manifest_arguments = --allow-backup --network-security-config

# (str) Android app theme
android.theme = "@android:style/Theme.DeviceDefault"

# (str) Gstreamer support
#android.gstreamer = 1

# (int) Android SDK version to use
android.api = 33

# (int) Android minimum API required
android.minapi = 21

# (int) Android SDK target version
android.target_api = 33

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it's usually better to not set this and use the one automatically set by python-for-android
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) Android ant directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
#android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) Android entry point, default is 'org.kivy.android.PythonActivity'
#android.entrypoint = org.quanlydichvu.MainActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build. Allows wildcards matching, for example:
# android.add_src = "java/android/**/*.java"

# (list) List of Java classes to add as activities
#android.add_activities =

# (str) Add extra XML features to the manifest
#android.extra_features =

# (str) Add extra XML permissions to the manifest
# android.extra_permissions = android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE

# (list) Android permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# (int) Override the default loading progress bar background
#android.loading_color = #FF0000

# (list) Android add libraries (if any).
#android.add_libs_armeabi = foo.so
#android.add_libs_armeabi_v7a = foo.so
#android.add_libs_arm64_v8a = foo.so
#android.add_libs_x86 = foo.so
#android.add_libs_mips = foo.so

# (bool) Indicate whether the application should be fullscreen or not
fullscreen = 0

# (str) The title in the app title bar of the osx
#title = My Application

# (str) OSX application category
#osx.category = public.app-category.utilities

# (str) Extra plist items
#osx.plist.info =

# (str) URL scheme
#osx.url_scheme =

# iOS specific
#
#
# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (XXXXXXXXXX)"

# (str) The development team to use for signing the debug version
#ios.codesign.development_team = <teamid>

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s

# (bool) Should add the resource dir to the skin
#ios.add_skins = True

# (str) URL scheme
#ios.url_scheme =

# (str) Native libraries to add
#ios.native_libraries =

# (list) Additional packages to add to the ios project
#ios.extra_packages =


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage in absolute or relative to cwd
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as sections with each as components.
#    Each line will be concatenated with the others, to have human readable lists.
#    The options with a list and a human reading can be stored like this:
#
#    android add_src =
#        java/org/test
#        java/org/my
#
#    It will be converted to ["java/org/test", "java/org/my"]
#    with the previous config.

# (str) android extra manifest arguments
# android.extra_manifest_arguments = --allow-backup --network-security-config