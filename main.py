import sqlite3
import xlsxwriter
import os
from datetime import datetime
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.core.window import Window

# Xử lý platform Android - dùng try/except để tránh lỗi khi build
if platform == 'android':
    try:
        from android.permissions import request_permissions, Permission
        from android.storage import primary_external_storage_path
        from android import mActivity
        import android
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, 
                            Permission.READ_EXTERNAL_STORAGE])
    except ImportError:
        # Nếu không import được (khi build), bỏ qua
        pass

class Tab(MDFloatLayout, MDTabsBase):
    pass

KV = '''
MDBoxLayout:
    orientation: 'vertical'
    md_bg_color: "#F0F4F4"

    MDTopAppBar:
        title: "Quản lý dịch vụ - BS Thành"
        elevation: 2
        right_action_items: [["file-excel", lambda x: app.export_to_excel()]]

    MDTabs:
        id: tabs
        on_tab_switch: app.on_tab_switch(*args)

        Tab:
            title: "NHẬP LIỆU"
            MDScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(20)
                    adaptive_height: True

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(15)
                        radius: [15, ]
                        elevation: 1
                        adaptive_height: True
                        md_bg_color: "#FFFFFF"

                        MDLabel:
                            text: "THÔNG TIN CHI TIẾT"
                            font_style: "Button"
                            halign: "center"
                            theme_text_color: "Secondary"

                        MDTextField:
                            id: ma_kcb
                            hint_text: "Mã KCB"
                            mode: "rectangle"
                        
                        MDTextField:
                            id: ho_ten
                            hint_text: "Tên bệnh nhân"
                            mode: "rectangle"

                        MDTextField:
                            id: ngay_vao
                            hint_text: "Ngày (DD/MM/YYYY)"
                            mode: "rectangle"
                            on_focus: if self.focus: app.show_date_picker()

                        MDTextField:
                            id: ten_dich_vu
                            hint_text: "Dịch vụ thủ thuật"
                            mode: "rectangle"
                            on_focus: if self.focus: app.open_menu_service()

                        MDGridLayout:
                            cols: 2
                            spacing: dp(10)
                            adaptive_height: True
                            MDTextField:
                                id: gia_tien
                                hint_text: "Đơn giá"
                                mode: "rectangle"
                                readonly: True
                            MDTextField:
                                id: so_luong
                                hint_text: "SL"
                                text: "1"
                                mode: "rectangle"
                                input_filter: "int"
                                on_text: app.calculate_total()

                        MDTextField:
                            id: nguoi_lam
                            hint_text: "Người thực hiện"
                            mode: "rectangle"
                            on_focus: if self.focus: app.open_menu_staff("do")
                        
                        MDTextField:
                            id: nguoi_tu_van
                            hint_text: "Người tư vấn"
                            mode: "rectangle"
                            on_focus: if self.focus: app.open_menu_staff("consult")

                        MDTextField:
                            id: tong_tien
                            hint_text: "Thành tiền (VNĐ)"
                            mode: "rectangle"
                            readonly: True
                            fill_color_normal: "#F1F8E9"

                    MDBoxLayout:
                        spacing: dp(10)
                        adaptive_height: True
                        padding: [0, dp(10)]
                        MDRaisedButton:
                            text: "LƯU MỚI"
                            on_release: app.save_data()
                        MDRaisedButton:
                            text: "CẬP NHẬT"
                            md_bg_color: "orange"
                            on_release: app.update_data()
                        MDRaisedButton:
                            text: "XOÁ"
                            md_bg_color: "red"
                            on_release: app.show_confirm_delete()
                        MDRaisedButton:
                            text: "LÀM TRỐNG"
                            md_bg_color: "gray"
                            on_release: app.clear_inputs()

        Tab:
            title: "DANH SÁCH"
            MDBoxLayout:
                id: table_container
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(10)

        Tab:
            title: "THỐNG KÊ NV"
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(12)
                spacing: dp(12)

                MDCard:
                    adaptive_height: True
                    padding: dp(15)
                    radius: [12,]
                    elevation: 1
                    MDTextField:
                        id: filter_staff_name
                        hint_text: "Nhấn chọn tên nhân viên"
                        mode: "rectangle"
                        readonly: True
                        on_focus: if self.focus: app.open_menu_filter_staff()
                
                MDBoxLayout:
                    id: filter_table_container
                
                MDRaisedButton:
                    text: "XUẤT FILE EXCEL RIÊNG"
                    pos_hint: {"center_x": .5}
                    on_release: app.export_individual_excel()

        Tab:
            title: "CÀI ĐẶT"
            MDScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(20)
                    spacing: dp(15)
                    adaptive_height: True
                    
                    MDLabel:
                        text: "QUẢN LÝ DỊCH VỤ"
                        font_style: "H6"
                        halign: "center"
                    
                    MDTextField:
                        id: set_service_name
                        hint_text: "Tên dịch vụ mới"
                        mode: "rectangle"
                    MDTextField:
                        id: set_service_price
                        hint_text: "Đơn giá"
                        mode: "rectangle"
                        input_filter: "int"
                    MDRaisedButton:
                        text: "THÊM DỊCH VỤ"
                        on_release: app.add_config('service', app.root.ids.set_service_name.text, app.root.ids.set_service_price.text)
                    
                    MDSeparator:
                        height: dp(20)
                    
                    MDLabel:
                        text: "QUẢN LÝ NHÂN VIÊN"
                        font_style: "H6"
                        halign: "center"
                    
                    MDTextField:
                        id: set_staff_name
                        hint_text: "Tên nhân viên mới"
                        mode: "rectangle"
                    MDRaisedButton:
                        text: "THÊM NHÂN VIÊN"
                        on_release: app.add_config('staff', app.root.ids.set_staff_name.text)
                    
                    MDSeparator:
                        height: dp(20)
                    
                    MDLabel:
                        text: "THÔNG TIN ỨNG DỤNG"
                        font_style: "H6"
                        halign: "center"
                    
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(15)
                        spacing: dp(10)
                        radius: [10,]
                        elevation: 1
                        adaptive_height: True
                        
                        MDLabel:
                            text: "Phiên bản: 1.0.0"
                            halign: "center"
                        MDLabel:
                            text: "Nhà phát triển: BS Thành"
                            halign: "center"
                        MDLabel:
                            id: storage_info
                            text: "Đường dẫn: Đang tải..."
                            halign: "center"
                            font_style: "Caption"
'''

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        Window.softinput_mode = "pan"
        self.selected_row_id = None
        self.db_path = None
        self.app_folder = None
        return Builder.load_string(KV)

    def on_start(self):
        """Khởi tạo khi app bắt đầu chạy"""
        self.get_app_folder()
        self.db_init()
        self.load_sample_data()
        self.update_storage_info()

    def get_app_folder(self):
        """Lấy đường dẫn thư mục lưu trữ phù hợp với từng nền tảng"""
        try:
            if platform == 'android':
                # Trên Android, cố gắng lấy đường dẫn bộ nhớ ngoài
                try:
                    from android.storage import primary_external_storage_path
                    base = primary_external_storage_path()
                except:
                    base = '/storage/emulated/0'
                self.app_folder = os.path.join(base, 'Documents', 'QuanLyDichVu')
            else:
                # Trên máy tính
                self.app_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
            
            if not os.path.exists(self.app_folder):
                os.makedirs(self.app_folder)
            
            self.db_path = os.path.join(self.app_folder, 'medical_data.db')
            return self.app_folder
        except Exception as e:
            print(f"Lỗi tạo thư mục: {e}")
            # Fallback
            self.app_folder = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(self.app_folder, 'medical_data.db')
            return self.app_folder

    def update_storage_info(self):
        try:
            if hasattr(self.root, 'ids') and 'storage_info' in self.root.ids:
                self.root.ids.storage_info.text = f"Lưu tại: {self.app_folder}"
        except:
            pass

    def db_init(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS records 
                                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                  ma_kcb TEXT, 
                                  ngay TEXT, 
                                  ho_ten TEXT, 
                                  dich_vu TEXT, 
                                  gia REAL, 
                                  so_luong INTEGER, 
                                  nguoi_lam TEXT, 
                                  nguoi_tv TEXT, 
                                  tong REAL)''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS config 
                                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                  type TEXT, 
                                  name TEXT, 
                                  value TEXT)''')
            self.conn.commit()
            print(f"Database initialized at: {self.db_path}")
        except Exception as e:
            print(f"Lỗi khởi tạo database: {e}")
            self.show_info(f"Lỗi database: {e}")

    def load_sample_data(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM config")
            count = self.cursor.fetchone()[0]
            if count == 0:
                sample_services = [
                    ('service', 'Khám tổng quát', '200000'),
                    ('service', 'Siêu âm', '300000'),
                    ('service', 'Xét nghiệm máu', '150000'),
                    ('service', 'Chụp X-quang', '400000'),
                ]
                self.cursor.executemany("INSERT INTO config (type, name, value) VALUES (?,?,?)", sample_services)
                sample_staff = [
                    ('staff', 'BS Thành', ''),
                    ('staff', 'BS An', ''),
                    ('staff', 'Điều dưỡng Mai', ''),
                ]
                self.cursor.executemany("INSERT INTO config (type, name, value) VALUES (?,?,?)", sample_staff)
                self.conn.commit()
                print("Đã thêm dữ liệu mẫu")
        except Exception as e:
            print(f"Lỗi load dữ liệu mẫu: {e}")

    def show_info(self, message, duration=2):
        try:
            snackbar = Snackbar(
                text=message,
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=0.8,
                duration=duration
            )
            snackbar.open()
        except Exception as e:
            print(f"Lỗi hiển thị thông báo: {e}")

    def format_currency(self, value):
        try:
            if value is None:
                return "0"
            str_value = str(value).replace(',', '')
            num_value = float(str_value)
            return "{:,.0f}".format(num_value)
        except:
            return "0"

    def fix_date_format(self, date_str):
        if not date_str:
            return ""
        try:
            if "-" in date_str and len(date_str) == 10:
                return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
            return date_str
        except:
            return date_str

    def calculate_total(self):
        try:
            gia_text = self.root.ids.gia_tien.text
            gia = float(gia_text.replace(',', '')) if gia_text else 0
            sl_text = self.root.ids.so_luong.text
            sl = int(sl_text) if sl_text and sl_text.isdigit() else 1
            tong = gia * sl
            self.root.ids.tong_tien.text = self.format_currency(tong)
        except Exception as e:
            print(f"Lỗi tính tổng: {e}")

    # Các phương thức khác (load_table, show_confirm_delete, delete_data, open_menu_filter_staff, ...)
    # Giữ nguyên như code trước, không thay đổi.
    # Để tiết kiệm không gian, tôi không paste lại toàn bộ, bạn có thể giữ nguyên các phương thức còn lại từ code cũ.
    # Lưu ý: các phương thức này không phụ thuộc vào android, nên không ảnh hưởng.

    # ... (các phương thức còn lại giữ nguyên)
    # Để tránh dài dòng, tôi sẽ không copy lại toàn bộ. Bạn hãy copy các phương thức từ code cũ vào đây.
    # Quan trọng nhất là phần trên đã sửa import android.

# Lưu ý: Các phương thức còn lại như load_table, open_menu_service, set_service, open_menu_staff, set_staff, show_date_picker, save_data, on_row_press, update_data, add_config, clear_inputs, on_tab_switch, export_to_excel, export_individual_excel v.v. giữ nguyên.

if __name__ == '__main__':
    MainApp().run()
