import tkinter as tk
import customtkinter as ctk
import threading
import socket
import requests
import upnpy
import os
import time
from datetime import datetime
from flask import Flask, send_from_directory, request
from tkinter import filedialog, messagebox

# 메타 정보
__author__ = "Rheehose (Rhee Creative)"
__year__ = "2008-2026"
__license__ = "Apache License 2.0 (아파치 라이선스 2.0)"

class SimpleServerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 창 기본 설정
        self.title("Simple Server Premium - Rheehose")
        self.geometry("700x850")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # 변수 데이터
        self.server_thread = None
        self.is_running = False
        self.server_port = tk.IntVar(value=8080)
        self.serve_path = tk.StringVar(value=os.getcwd())
        self.access_scope = tk.StringVar(value="로컬 네트워크")
        self.hosting_mode = tk.StringVar(value="스마트 호스팅") # "스마트 호스팅", "파일 공유", "정적 사이트"
        
        self.local_ip = self.get_local_ip()
        self.public_ip = "가져오는 중..."
        
        # UI 스타일
        self.main_font = ("Pretendard", 14)
        self.title_font = ("Pretendard", 22, "bold")
        self.log_font = ("Cascadia Code", 12)

        self.setup_ui()
        
        # 비동기 정보 업데이트
        threading.Thread(target=self.fetch_public_ip, daemon=True).start()

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except: return "127.0.0.1"

    def fetch_public_ip(self):
        try:
            response = requests.get("https://api.ipify.org", timeout=5)
            self.public_ip = response.text
            self.update_status_labels()
        except:
            self.public_ip = "알 수 없음"
            self.update_status_labels()

    def add_log(self, message, type="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{type}] {message}\n"
        self.log_area.configure(state="normal")
        self.log_area.insert("end", log_entry)
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def setup_ui(self):
        # 1. 상단 헤더 (가장 먼저 상단에 고정)
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(side="top", pady=(30, 10), padx=40, fill="x")
        
        self.title_label = ctk.CTkLabel(self.header, text="SIMPLE SERVER", font=self.title_font, text_color="#3B8ED0")
        self.title_label.pack(side="left")
        
        self.version_label = ctk.CTkLabel(self.header, text="Premium Edition", font=("Pretendard", 12, "italic"), text_color="gray")
        self.version_label.pack(side="left", padx=10, pady=(5, 0))

        # 2. 하단 제어부 (아래쪽에 먼저 고정하여 중앙 영역 확보)
        self.footer_container = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_container.pack(side="bottom", fill="x", padx=40, pady=(0, 10))

        self.footer = ctk.CTkButton(self.footer_container, text=f"© {__year__} {__author__} | Apache 2.0", 
                                   fg_color="transparent", text_color="gray", hover=False, command=self.show_disclaimer)
        self.footer.pack(side="bottom", pady=5)

        self.toggle_btn = ctk.CTkButton(self.footer_container, text="서버 시작", font=("Pretendard", 16, "bold"), 
                                       height=50, fg_color="#1f6aa5", hover_color="#144870", command=self.toggle_server)
        self.toggle_btn.pack(side="bottom", fill="x", pady=10)

        self.control_panel = ctk.CTkFrame(self.footer_container, fg_color="transparent")
        self.control_panel.pack(side="bottom", fill="x")
        
        self.status_dot = ctk.CTkLabel(self.control_panel, text="●", text_color="red", font=("Pretendard", 20))
        self.status_dot.pack(side="left", padx=(0, 5))
        
        self.status_txt = ctk.CTkLabel(self.control_panel, text="서버 중지됨", font=self.main_font)
        self.status_txt.pack(side="left")

        # 3. 중앙 메인 스크롤 영역 (남은 모든 영역 차지)
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        # --- 스크롤 내부 카드들 ---
        # 1. 경로 설정 카드
        self.create_card("📂 경로 및 포트 설정")
        
        path_label = ctk.CTkLabel(self.current_card, text="공유 폴더 경로", font=self.main_font)
        path_label.pack(anchor="w", padx=20, pady=(10, 0))
        
        path_frame = ctk.CTkFrame(self.current_card, fg_color="transparent")
        path_frame.pack(fill="x", padx=20, pady=5)
        
        self.path_entry = ctk.CTkEntry(path_frame, textvariable=self.serve_path, font=self.main_font, height=35)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.path_btn = ctk.CTkButton(path_frame, text="검색", width=80, height=35, command=self.browse_path)
        self.path_btn.pack(side="right")

        port_frame = ctk.CTkFrame(self.current_card, fg_color="transparent")
        port_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(port_frame, text="서버 포트", font=self.main_font).pack(side="left", padx=(0, 10))
        self.port_entry = ctk.CTkEntry(port_frame, textvariable=self.server_port, width=100, font=self.main_font)
        self.port_entry.pack(side="left")

        # 2. 호스팅 모드 및 범위 카드
        self.create_card("🌐 서비스 구성")
        
        ctk.CTkLabel(self.current_card, text="호스팅 모드", font=self.main_font).pack(anchor="w", padx=20, pady=(10, 0))
        self.mode_selector = ctk.CTkSegmentedButton(self.current_card, values=["파일 공유", "정적 사이트", "스마트 호스팅"], 
                                                   variable=self.hosting_mode, font=self.main_font)
        self.mode_selector.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(self.current_card, text="네트워크 접근 범위", font=self.main_font).pack(anchor="w", padx=20, pady=(10, 0))
        self.scope_selector = ctk.CTkSegmentedButton(self.current_card, values=["내 PC", "로컬 네트워크", "외부 인터넷"], 
                                                   variable=self.access_scope, command=self.update_status_labels, font=self.main_font)
        self.scope_selector.pack(fill="x", padx=20, pady=10)

        # 3. 상태 및 주소 카드
        self.create_card("📊 실시간 상태 및 주소")
        
        self.addr_frame = ctk.CTkFrame(self.current_card, fg_color="#1a1a1a")
        self.addr_frame.pack(fill="x", padx=20, pady=15)
        
        self.addr_label = ctk.CTkLabel(self.addr_frame, text="서버를 시작하면 주소가 표시됩니다", font=self.log_font, text_color="#3B8ED0")
        self.addr_label.pack(pady=10)
        
        self.copy_btn = ctk.CTkButton(self.addr_frame, text="주소 복사", width=100, height=28, fg_color="#2b2b2b", 
                                     hover_color="#3b3b3b", command=self.copy_address, state="disabled")
        self.copy_btn.pack(pady=(0, 15)) # 패딩 조정하여 잘림 방지

        # 4. 로그 영역
        self.create_card("📝 서버 로그")
        self.log_area = ctk.CTkTextbox(self.current_card, height=180, font=self.log_font, state="disabled", fg_color="#0d0d0d")
        self.log_area.pack(fill="both", padx=10, pady=10)

    def create_card(self, title):
        self.current_card = ctk.CTkFrame(self.scroll_frame, fg_color="#242424")
        self.current_card.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(self.current_card, text=title, font=("Pretendard", 14, "bold"), text_color="#888").pack(anchor="w", padx=15, pady=(10, 5))

    def update_status_labels(self, _=None):
        scope = self.access_scope.get()
        port = self.server_port.get()
        
        if not self.is_running:
            if scope == "외부 인터넷":
                self.addr_label.configure(text=f"접속 예정: http://{self.public_ip}:{port}")
            elif scope == "로컬 네트워크":
                self.addr_label.configure(text=f"접속 예정: http://{self.local_ip}:{port}")
            else:
                self.addr_label.configure(text=f"접속 예정: http://127.0.0.1:{port}")
        else:
            current_addr = self.get_current_url()
            self.addr_label.configure(text=current_addr)

    def get_current_url(self):
        scope = self.access_scope.get()
        port = self.server_port.get()
        if scope == "외부 인터넷": return f"http://{self.public_ip}:{port}"
        if scope == "로컬 네트워크": return f"http://{self.local_ip}:{port}"
        return f"http://127.0.0.1:{port}"

    def copy_address(self):
        url = self.get_current_url()
        self.clipboard_clear()
        self.clipboard_append(url)
        self.add_log(f"주소가 클립보드에 복사되었습니다: {url}", "UI")

    def browse_path(self):
        path = filedialog.askdirectory()
        if path: self.serve_path.set(path)

    def show_disclaimer(self):
        disclaimer = (
            "Simple Server Premium Edition\n\n"
            "이 소프트웨어는 아파치 라이선스 2.0에 따라 배포됩니다.\n"
            "웹사이트 호스팅 및 파일 공유 기능을 제공하며, 사용 시 보안 설정에 주의가 필요합니다.\n\n"
            "저자: Rheehose (Rhee Creative)\n"
            "연도: 2008-2026"
        )
        messagebox.showinfo("정보 및 면책 조항", disclaimer)

    def start_flask(self, path, port, host):
        app = Flask(__name__)
        mode = self.hosting_mode.get()

        @app.before_request
        def log_request():
            self.add_log(f"{request.remote_addr} -> {request.method} {request.path}", "REQ")

        @app.route('/')
        @app.route('/<path:filename>')
        def serve_file(filename=''):
            full_path = os.path.join(path, filename)
            
            # 파일 직접 요청
            if os.path.isfile(full_path):
                return send_from_directory(path, filename)

            # 디렉토리 요청
            if os.path.isdir(full_path):
                # 정적 사이트 모드 또는 스마트 모드에서 index.html 검색
                if mode in ["정적 사이트", "스마트 호스팅"]:
                    index_path = os.path.join(full_path, 'index.html')
                    if os.path.exists(index_path):
                        return send_from_directory(os.path.dirname(index_path), 'index.html')
                
                # 정적 사이트 전용 모드인데 index가 없으면 403/404
                if mode == "정적 사이트":
                    return "<h1>403 Forbidden</h1><p>index.html 파일이 없습니다.</p>", 403

                # 파일 공유 모드 또는 스마트 모드(index 없을 때) 파일 목록 표시
                try:
                    files = os.listdir(full_path)
                    prefix = filename + "/" if filename and not filename.endswith('/') else filename
                    file_links = "".join([f'<li><a href="/{prefix}{f}">{f}</a></li>' for f in files])
                    up_link = '<li><a href="..">.. (상위 폴더)</a></li>' if filename else ''
                    
                    return f"""
                    <html><head><meta charset="UTF-8"><title>Simple Server - {os.path.basename(path)}</title>
                    <style>
                        body {{ font-family: sans-serif; padding: 50px; background: #121212; color: #e0e0e0; }}
                        .container {{ max-width: 900px; margin: 0 auto; background: #1e1e1e; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
                        h1 {{ color: #3B8ED0; border-bottom: 1px solid #333; padding-bottom: 15px; }}
                        ul {{ list-style: none; padding: 0; }}
                        li {{ padding: 12px; border-bottom: 1px solid #2a2a2a; transition: 0.2s; }}
                        li:hover {{ background: #252525; }}
                        a {{ color: #64b5f6; text-decoration: none; display: block; }}
                        .footer {{ margin-top: 30px; font-size: 12px; color: #666; text-align: center; }}
                    </style></head>
                    <body><div class="container"><h1>📂 {os.path.abspath(full_path)}</h1><ul>{up_link}{file_links}</ul></div>
                    <div class="footer">Powered by Simple Server Premium © Rheehose</div></body></html>
                    """
                except Exception as e:
                    return f"<h1>Error: {e}</h1>", 500

            # Next.js clean URLs 지원
            if mode in ["정적 사이트", "스마트 호스팅"]:
                html_fallback = full_path + ".html"
                if os.path.exists(html_fallback):
                    return send_from_directory(path, filename + ".html")

            return "<h1>404 Not Found</h1>", 404

        try:
            self.add_log(f"서버 엔진 시작 중... ({host}:{port})")
            app.run(host=host, port=port, debug=False, use_reloader=False)
        except Exception as e:
            self.is_running = False
            self.add_log(f"서버 실행 중 치명적 오류: {e}", "ERR")

    def toggle_server(self):
        if not self.is_running:
            try:
                port = int(self.server_port.get())
                path = self.serve_path.get()
                if not os.path.exists(path): raise Exception("폴더가 존재하지 않음")
                
                scope = self.access_scope.get()
                host = '127.0.0.1' if scope == "내 PC" else '0.0.0.0'
                
                # 포트 체크
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    if s.connect_ex(('localhost', port)) == 0: raise Exception(f"{port} 포트 사용 중")

                # 외부 접속 시 UPnP
                if scope == "외부 인터넷":
                    self.add_log("UPnP 포트 포워딩 시도 중...")
                    if not self.enable_upnp(port):
                        if not messagebox.askyesno("경고", "UPnP 설정 실패. 계속할까요?"): return

                self.is_running = True
                self.toggle_btn.configure(text="서버 중지 (프로그램 종료)", fg_color="#a51f1f", hover_color="#701414")
                self.status_dot.configure(text_color="green")
                self.status_txt.configure(text=f"서버 실행 중 ({scope} / {self.hosting_mode.get()})")
                self.copy_btn.configure(state="normal")
                
                # UI 잠금
                self.path_entry.configure(state="disabled")
                self.port_entry.configure(state="disabled")
                self.mode_selector.configure(state="disabled")
                self.scope_selector.configure(state="disabled")
                self.path_btn.configure(state="disabled")

                self.update_status_labels()
                self.add_log(f"서버가 시작되었습니다. 모드: {self.hosting_mode.get()}")
                
                self.server_thread = threading.Thread(target=self.start_flask, args=(path, port, host), daemon=True)
                self.server_thread.start()
                
            except Exception as e:
                messagebox.showerror("오류", str(e))
                self.add_log(f"시작 실패: {e}", "ERR")
        else:
            self.quit()

    def enable_upnp(self, port):
        try:
            upnp = upnpy.UPnP()
            devices = upnp.discover()
            if not devices: return False
            device = upnp.get_igd()
            if not device: return False
            service = None
            for s in device.get_services():
                if 'WANIPConnection' in s.service_id or 'WANPPPConnection' in s.service_id:
                    service = s; break
            if not service: return False
            self.public_ip = service.GetExternalIPAddress().get('NewExternalIPAddress')
            service.AddPortMapping(NewRemoteHost='', NewExternalPort=port, NewProtocol='TCP', NewInternalPort=port, NewInternalClient=self.local_ip, NewEnabled=1, NewPortMappingDescription='SimpleServerPremium', NewLeaseDuration=0)
            self.add_log(f"UPnP 성공: 외부 IP {self.public_ip}")
            return True
        except Exception as e:
            self.add_log(f"UPnP 실패: {e}", "WARN")
            return False

if __name__ == "__main__":
    app = SimpleServerApp()
    app.mainloop()
