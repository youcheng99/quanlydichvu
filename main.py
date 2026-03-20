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

# Xử lý platform Android
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    from android import mActivity
    import android
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, 
                        Permission.READ_EXTERNAL_STORAGE])

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
        # Load dữ liệu mẫu nếu cần
        self.load_sample_data()
        # Cập nhật thông tin lưu trữ
        self.update_storage_info()

    def get_app_folder(self):
        """Lấy đường dẫn thư mục lưu trữ phù hợp với từng nền tảng"""
        try:
            if platform == 'android':
                # Trên Android - sử dụng thư mục Documents
                self.app_folder = os.path.join(primary_external_storage_path(), 'Documents', 'QuanLyDichVu')
            elif platform == 'ios':
                # Trên iOS
                from plyer import storagepath
                self.app_folder = os.path.join(storagepath.get_documents_dir(), 'QuanLyDichVu')
            else:
                # Trên máy tính
                self.app_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
            
            # Tạo thư mục nếu chưa tồn tại
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
        """Cập nhật thông tin đường dẫn lưu trữ"""
        try:
            if hasattr(self.root, 'ids') and 'storage_info' in self.root.ids:
                self.root.ids.storage_info.text = f"Lưu tại: {self.app_folder}"
        except:
            pass

    def db_init(self):
        """Khởi tạo database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # Tạo bảng records
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
            
            # Tạo bảng config
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
        """Load dữ liệu mẫu nếu database trống"""
        try:
            # Kiểm tra xem có dữ liệu chưa
            self.cursor.execute("SELECT COUNT(*) FROM config")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                # Thêm dịch vụ mẫu
                sample_services = [
                    ('service', 'Khám tổng quát', '200000'),
                    ('service', 'Siêu âm', '300000'),
                    ('service', 'Xét nghiệm máu', '150000'),
                    ('service', 'Chụp X-quang', '400000'),
                ]
                self.cursor.executemany("INSERT INTO config (type, name, value) VALUES (?,?,?)", sample_services)
                
                # Thêm nhân viên mẫu
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
        """Hiển thị thông báo"""
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
        """Định dạng tiền tệ"""
        try:
            if value is None:
                return "0"
            # Xóa dấu phẩy cũ nếu có
            str_value = str(value).replace(',', '')
            # Chuyển thành số và định dạng
            num_value = float(str_value)
            return "{:,.0f}".format(num_value)
        except:
            return "0"

    def fix_date_format(self, date_str):
        """Chuẩn hóa định dạng ngày tháng"""
        if not date_str:
            return ""
        try:
            # Nếu là định dạng YYYY-MM-DD (từ database)
            if "-" in date_str and len(date_str) == 10:
                return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
            return date_str
        except:
            return date_str

    def calculate_total(self):
        """Tính tổng tiền"""
        try:
            gia_text = self.root.ids.gia_tien.text
            if gia_text:
                gia = float(gia_text.replace(',', ''))
            else:
                gia = 0
            
            sl_text = self.root.ids.so_luong.text
            if sl_text and sl_text.isdigit():
                sl = int(sl_text)
            else:
                sl = 1
            
            tong = gia * sl
            self.root.ids.tong_tien.text = self.format_currency(tong)
        except Exception as e:
            print(f"Lỗi tính tổng: {e}")

    # --- LOAD TABLE & DASHBOARD ---
    def load_table(self):
        """Load bảng dữ liệu"""
        try:
            container = self.root.ids.table_container
            container.clear_widgets()
            
            self.cursor.execute("SELECT id, ma_kcb, ngay, ho_ten, dich_vu, so_luong, nguoi_lam, nguoi_tv, tong FROM records ORDER BY id DESC")
            rows = self.cursor.fetchall()
            total_ca = len(rows)
            total_money = sum([r[8] for r in rows]) if rows else 0

            # Card Dashboard
            card = MDCard(
                size_hint_y=None,
                height=dp(50),
                md_bg_color="#E0F2F1",
                radius=[10],
                padding=dp(10),
                elevation=1
            )
            dash_text = f"📊 TỔNG: {total_ca} CA | DOANH THU: {self.format_currency(total_money)} VNĐ"
            card.add_widget(MDLabel(
                text=dash_text,
                halign="center",
                bold=True,
                theme_text_color="Primary"
            ))
            container.add_widget(card)

            if rows:
                # Bảng dữ liệu
                processed_rows = []
                for r in rows:
                    processed_rows.append((
                        str(r[0]),  # ID
                        r[1],  # Mã KCB
                        self.fix_date_format(r[2]),  # Ngày
                        r[3],  # Họ Tên
                        r[4],  # Dịch Vụ
                        str(r[5]),  # SL
                        r[6],  # Người Làm
                        r[7],  # Tư Vấn
                        self.format_currency(r[8])  # Tổng
                    ))
                
                table = MDDataTable(
                    use_pagination=True,
                    rows_num=10,
                    column_data=[
                        ("ID", dp(10)),
                        ("Mã KCB", dp(20)),
                        ("Ngày", dp(25)),
                        ("Họ Tên", dp(35)),
                        ("Dịch Vụ", dp(35)),
                        ("SL", dp(12)),
                        ("Người Làm", dp(25)),
                        ("Tư Vấn", dp(25)),
                        ("Tổng", dp(25))
                    ],
                    row_data=processed_rows
                )
                table.bind(on_row_press=self.on_row_press)
                container.add_widget(table)
            else:
                # Thông báo không có dữ liệu
                container.add_widget(MDLabel(
                    text="Chưa có dữ liệu",
                    halign="center",
                    theme_text_color="Hint"
                ))
        except Exception as e:
            print(f"Lỗi load table: {e}")
            self.show_info(f"Lỗi: {e}")

    # --- XÁC NHẬN XOÁ ---
    def show_confirm_delete(self):
        """Hiển thị dialog xác nhận xóa"""
        if not self.selected_row_id:
            self.show_info("Bạn chưa chọn dòng nào!")
            return
        
        self.dialog = MDDialog(
            title="Xác nhận xoá?",
            text="Dữ liệu này sẽ mất vĩnh viễn.",
            buttons=[
                MDFlatButton(
                    text="HUỶ",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="XOÁ",
                    md_bg_color="red",
                    on_release=self.delete_data
                ),
            ],
        )
        self.dialog.open()

    def delete_data(self, *args):
        """Xóa dữ liệu"""
        try:
            self.cursor.execute("DELETE FROM records WHERE id=?", (self.selected_row_id,))
            self.conn.commit()
            self.dialog.dismiss()
            self.show_info("✅ Đã xoá!")
            self.clear_inputs()
            self.load_table()
        except Exception as e:
            self.show_info(f"Lỗi: {e}")

    # --- THỐNG KÊ NV ---
    def open_menu_filter_staff(self):
        """Mở menu chọn nhân viên để lọc"""
        try:
            self.cursor.execute("SELECT DISTINCT name FROM config WHERE type='staff' ORDER BY name")
            staffs = self.cursor.fetchall()
            
            items = []
            for s in staffs:
                items.append({
                    "viewclass": "OneLineListItem",
                    "text": s[0],
                    "on_release": lambda x=s[0]: self.filter_by_staff(x)
                })
            
            self.menu_filter = MDDropdownMenu(
                caller=self.root.ids.filter_staff_name,
                items=items,
                width_mult=4
            )
            self.menu_filter.open()
        except Exception as e:
            self.show_info(f"Lỗi: {e}")

    def filter_by_staff(self, staff_name):
        """Lọc dữ liệu theo nhân viên"""
        try:
            self.root.ids.filter_staff_name.text = staff_name
            self.menu_filter.dismiss()
            
            container = self.root.ids.filter_table_container
            container.clear_widgets()
            
            self.cursor.execute("SELECT ma_kcb, ngay, ho_ten, dich_vu, so_luong, tong FROM records WHERE nguoi_lam=? ORDER BY ngay DESC", (staff_name,))
            rows = self.cursor.fetchall()
            
            if rows:
                data = []
                for r in rows:
                    data.append((
                        r[0],
                        self.fix_date_format(r[1]),
                        r[2],
                        r[3],
                        str(r[4]),
                        self.format_currency(r[5])
                    ))
                
                # Tính tổng
                total = sum([r[5] for r in rows])
                
                table = MDDataTable(
                    use_pagination=True,
                    rows_num=10,
                    column_data=[
                        ("Mã KCB", dp(25)),
                        ("Ngày", dp(25)),
                        ("Bệnh Nhân", dp(35)),
                        ("Dịch Vụ", dp(35)),
                        ("SL", dp(12)),
                        ("Tiền", dp(25))
                    ],
                    row_data=data
                )
                container.add_widget(table)
                
                # Hiển thị tổng
                container.add_widget(MDLabel(
                    text=f"Tổng doanh thu: {self.format_currency(total)} VNĐ",
                    halign="right",
                    theme_text_color="Primary",
                    bold=True
                ))
            else:
                container.add_widget(MDLabel(
                    text="Không có dữ liệu",
                    halign="center"
                ))
        except Exception as e:
            self.show_info(f"Lỗi: {e}")

    def export_individual_excel(self):
        """Xuất Excel riêng cho từng nhân viên"""
        name = self.root.ids.filter_staff_name.text
        if not name or "chọn" in name:
            self.show_info("Chọn nhân viên trước!")
            return
        
        try:
            # Tạo tên file an toàn
            safe_name = name.replace(" ", "_").replace("/", "_")
            filename = os.path.join(self.app_folder, f"Bao_Cao_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
            
            wb = xlsxwriter.Workbook(filename)
            ws = wb.add_worksheet()
            
            # Format
            fmt_h = wb.add_format({'bold': True, 'bg_color': '#00796B', 'color': 'white', 'border': 1, 'align': 'center'})
            fmt_m = wb.add_format({'num_format': '#,##0', 'border': 1})
            fmt_title = wb.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
            
            # Title
            ws.merge_range('A1:F1', f'BÁO CÁO DOANH THU - {name}', fmt_title)
            
            # Header
            headers = ['Mã KCB', 'Ngày', 'Bệnh Nhân', 'Dịch Vụ', 'Số Lượng', 'Thành Tiền']
            ws.write_row(2, 0, headers, fmt_h)
            
            # Data
            self.cursor.execute("SELECT ma_kcb, ngay, ho_ten, dich_vu, so_luong, tong FROM records WHERE nguoi_lam=?", (name,))
            rows = self.cursor.fetchall()
            total = 0
            
            for i, r in enumerate(rows, 3):
                ws.write(i, 0, r[0])
                ws.write(i, 1, self.fix_date_format(r[1]))
                ws.write(i, 2, r[2])
                ws.write(i, 3, r[3])
                ws.write(i, 4, r[4])
                ws.write(i, 5, r[5], fmt_m)
                total += r[5]
            
            # Total
            last_row = len(rows) + 3
            ws.write(last_row, 4, "TỔNG CỘNG:", fmt_h)
            ws.write(last_row, 5, total, fmt_m)
            
            # Thông tin thêm
            ws.write(last_row + 2, 0, f"Ngày xuất: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            
            # Auto-fit columns
            for col_num, _ in enumerate(headers):
                ws.set_column(col_num, col_num, 15)
            
            wb.close()
            
            # Thông báo đường dẫn file
            if platform == 'android':
                self.show_info(f"✅ Đã lưu tại: {filename}")
            else:
                self.show_info(f"✅ Đã lưu: {os.path.basename(filename)}")
                
        except Exception as e:
            self.show_info(f"❌ Lỗi: {str(e)}")

    # --- HÀM PHỤ ---
    def open_menu_service(self):
        """Mở menu chọn dịch vụ"""
        try:
            self.cursor.execute("SELECT name, value FROM config WHERE type='service' ORDER BY name")
            services = self.cursor.fetchall()
            
            items = []
            for s in services:
                items.append({
                    "viewclass": "OneLineListItem",
                    "text": f"{s[0]} ({self.format_currency(s[1])} VNĐ)",
                    "on_release": lambda x=s: self.set_service(x)
                })
            
            self.menu_service = MDDropdownMenu(
                caller=self.root.ids.ten_dich_vu,
                items=items,
                width_mult=4
            )
            self.menu_service.open()
        except Exception as e:
            self.show_info(f"Lỗi: {e}")

    def set_service(self, data):
        """Chọn dịch vụ"""
        self.root.ids.ten_dich_vu.text = data[0]
        self.root.ids.gia_tien.text = self.format_currency(data[1])
        self.menu_service.dismiss()
        self.calculate_total()

    def open_menu_staff(self, role):
        """Mở menu chọn nhân viên"""
        try:
            self.cursor.execute("SELECT name FROM config WHERE type='staff' ORDER BY name")
            staffs = self.cursor.fetchall()
            
            items = []
            for s in staffs:
                items.append({
                    "viewclass": "OneLineListItem",
                    "text": s[0],
                    "on_release": lambda x=s[0]: self.set_staff(x, role)
                })
            
            if role == "do":
                caller = self.root.ids.nguoi_lam
            else:
                caller = self.root.ids.nguoi_tu_van
                
            self.menu_staff = MDDropdownMenu(
                caller=caller,
                items=items,
                width_mult=4
            )
            self.menu_staff.open()
        except Exception as e:
            self.show_info(f"Lỗi: {e}")

    def set_staff(self, name, role):
        """Chọn nhân viên"""
        if role == "do":
            self.root.ids.nguoi_lam.text = name
        else:
            self.root.ids.nguoi_tu_van.text = name
        self.menu_staff.dismiss()

    def show_date_picker(self):
        """Hiển thị date picker"""
        try:
            from datetime import datetime
            dp_picker = MDDatePicker(
                year=datetime.now().year,
                month=datetime.now().month,
                day=datetime.now().day
            )
            dp_picker.bind(on_save=self.on_date_save)
            dp_picker.open()
        except Exception as e:
            self.show_info(f"Lỗi: {e}")

    def on_date_save(self, instance, value, date_range):
        """Lưu ngày được chọn"""
        self.root.ids.ngay_vao.text = value.strftime('%d/%m/%Y')

    def save_data(self):
        """Lưu dữ liệu mới"""
        try:
            d = self.root.ids
            if not d.ma_kcb.text:
                self.show_info("Vui lòng nhập Mã KCB!")
                return
            
            # Kiểm tra dữ liệu bắt buộc
            if not d.ho_ten.text:
                self.show_info("Vui lòng nhập tên bệnh nhân!")
                return
            
            if not d.ten_dich_vu.text:
                self.show_info("Vui lòng chọn dịch vụ!")
                return
            
            data = (
                d.ma_kcb.text,
                d.ngay_vao.text,
                d.ho_ten.text,
                d.ten_dich_vu.text,
                float(d.gia_tien.text.replace(',', '') or 0),
                int(d.so_luong.text or 1),
                d.nguoi_lam.text,
                d.nguoi_tu_van.text,
                float(d.tong_tien.text.replace(',', '') or 0)
            )
            
            self.cursor.execute("""
                INSERT INTO records 
                (ma_kcb, ngay, ho_ten, dich_vu, gia, so_luong, nguoi_lam, nguoi_tv, tong) 
                VALUES (?,?,?,?,?,?,?,?,?)
            """, data)
            self.conn.commit()
            self.show_info("✅ Đã lưu!")
            self.clear_inputs()
        except Exception as e:
            self.show_info(f"❌ Lỗi: {e}")

    def on_row_press(self, table, row):
        """Xử lý khi chọn dòng trong bảng"""
        try:
            # Lấy index của dòng được chọn
            idx = int(row.index / len(table.column_data))
            row_id = table.row_data[idx][0]
            
            self.cursor.execute("SELECT * FROM records WHERE id=?", (row_id,))
            res = self.cursor.fetchone()
            
            if res:
                self.selected_row_id = res[0]
                d = self.root.ids
                
                d.ma_kcb.text = str(res[1] or "")
                d.ngay_vao.text = str(res[2] or "")
                d.ho_ten.text = str(res[3] or "")
                d.ten_dich_vu.text = str(res[4] or "")
                d.gia_tien.text = self.format_currency(res[5] or 0)
                d.so_luong.text = str(res[6] or 1)
                d.nguoi_lam.text = str(res[7] or "")
                d.nguoi_tu_van.text = str(res[8] or "")
                d.tong_tien.text = self.format_currency(res[9] or 0)
                
                # Chuyển sang tab nhập liệu
                self.root.ids.tabs.switch_tab(self.root.ids.tabs.get_slides()[0])
                self.show_info("Đã chọn dữ liệu để cập nhật")
        except Exception as e:
            print(f"Lỗi chọn dòng: {e}")

    def update_data(self):
        """Cập nhật dữ liệu"""
        try:
            if not self.selected_row_id:
                self.show_info("Chưa chọn dữ liệu để cập nhật!")
                return
            
            d = self.root.ids
            data = (
                d.ma_kcb.text,
                d.ngay_vao.text,
                d.ho_ten.text,
                d.ten_dich_vu.text,
                float(d.gia_tien.text.replace(',', '') or 0),
                int(d.so_luong.text or 1),
                d.nguoi_lam.text,
                d.nguoi_tu_van.text,
                float(d.tong_tien.text.replace(',', '') or 0),
                self.selected_row_id
            )
            
            self.cursor.execute("""
                UPDATE records 
                SET ma_kcb=?, ngay=?, ho_ten=?, dich_vu=?, gia=?, 
                    so_luong=?, nguoi_lam=?, nguoi_tv=?, tong=? 
                WHERE id=?
            """, data)
            self.conn.commit()
            self.show_info("✅ Đã cập nhật!")
            self.clear_inputs()
        except Exception as e:
            self.show_info(f"❌ Lỗi: {e}")

    def add_config(self, type, name, value=""):
        """Thêm cấu hình (dịch vụ/nhân viên)"""
        try:
            if not name:
                self.show_info("Vui lòng nhập tên!")
                return
            
            # Kiểm tra trùng
            self.cursor.execute("SELECT id FROM config WHERE type=? AND name=?", (type, name))
            if self.cursor.fetchone():
                self.show_info("Tên đã tồn tại!")
                return
            
            self.cursor.execute("INSERT INTO config (type, name, value) VALUES (?,?,?)", 
                              (type, name, value))
            self.conn.commit()
            self.show_info(f"✅ Đã thêm {name}")
            
            # Xóa input
            if type == 'service':
                self.root.ids.set_service_name.text = ""
                self.root.ids.set_service_price.text = ""
            else:
                self.root.ids.set_staff_name.text = ""
                
        except Exception as e:
            self.show_info(f"❌ Lỗi: {e}")

    def clear_inputs(self):
        """Xóa tất cả input"""
        try:
            for tid in ['ma_kcb', 'ngay_vao', 'ho_ten', 'ten_dich_vu', 
                       'gia_tien', 'nguoi_lam', 'nguoi_tu_van', 'tong_tien']:
                if tid in self.root.ids:
                    self.root.ids[tid].text = ""
            
            if 'so_luong' in self.root.ids:
                self.root.ids.so_luong.text = "1"
            
            self.selected_row_id = None
        except Exception as e:
            print(f"Lỗi clear inputs: {e}")

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """Xử lý khi chuyển tab"""
        if tab_text == "DANH SÁCH":
            self.load_table()
        elif tab_text == "THỐNG KÊ NV":
            self.root.ids.filter_staff_name.text = ""
            self.root.ids.filter_table_container.clear_widgets()

    def export_to_excel(self):
        """Xuất Excel tổng hợp"""
        try:
            filename = os.path.join(self.app_folder, f"Bao_Cao_Tong_Hop_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
            
            wb = xlsxwriter.Workbook(filename)
            ws = wb.add_worksheet()
            
            # Format
            fmt_h = wb.add_format({'bold': True, 'bg_color': '#008080', 'color': 'white', 'border': 1, 'align': 'center'})
            fmt_m = wb.add_format({'num_format': '#,##0', 'border': 1})
            fmt_title = wb.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
            
            # Title
            ws.merge_range('A1:I1', 'BÁO CÁO TỔNG HỢP DOANH THU', fmt_title)
            
            # Headers
            headers = ['Mã KCB', 'Ngày', 'Họ Tên', 'Dịch Vụ', 'Đơn Giá', 'SL', 'Người Làm', 'Tư Vấn', 'Tổng']
            ws.write_row(2, 0, headers, fmt_h)
            
            # Data
            self.cursor.execute("SELECT ma_kcb, ngay, ho_ten, dich_vu, gia, so_luong, nguoi_lam, nguoi_tv, tong FROM records ORDER BY ngay DESC")
            rows = self.cursor.fetchall()
            
            total_all = 0
            for i, r in enumerate(rows, 3):
                ws.write(i, 0, r[0])
                ws.write(i, 1, self.fix_date_format(r[1]))
                ws.write(i, 2, r[2])
                ws.write(i, 3, r[3])
                ws.write(i, 4, r[4], fmt_m)
                ws.write(i, 5, r[5])
                ws.write(i, 6, r[6])
                ws.write(i, 7, r[7])
                ws.write(i, 8, r[8], fmt_m)
                total_all += r[8]
            
            # Total
            last_row = len(rows) + 3
            ws.write(last_row, 7, "TỔNG CỘNG:", fmt_h)
            ws.write(last_row, 8, total_all, fmt_m)
            
            # Thông tin thống kê
            ws.write(last_row + 2, 0, f"Tổng số ca: {len(rows)}")
            ws.write(last_row + 3, 0, f"Ngày xuất: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            
            # Auto-fit columns
            for col_num, _ in enumerate(headers):
                ws.set_column(col_num, col_num, 15)
            
            wb.close()
            
            if platform == 'android':
                self.show_info(f"✅ Đã lưu tại: {filename}")
            else:
                self.show_info(f"✅ Đã lưu: {os.path.basename(filename)}")
                
        except Exception as e:
            self.show_info(f"❌ Lỗi: {e}")

    def on_stop(self):
        """Đóng database khi thoát app"""
        try:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
        except:
            pass

if __name__ == '__main__':
    MainApp().run()