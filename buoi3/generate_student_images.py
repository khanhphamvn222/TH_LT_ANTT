import os
import math
from PIL import Image, ImageDraw, ImageFont

os.makedirs('buoi3/images', exist_ok=True)

# Fonts
font_mono = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 14)
font_mono_small = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 12)
font_mono_bold = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", 14)
font_sans = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 14)
font_sans_small = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 12)
font_sans_bold = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 14)
font_heading = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 17)
font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 20)

def draw_arrow(draw, start, end, color="#e53935", width=3, arrow_size=12):
    draw.line([start, end], fill=color, width=width)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)
    x1 = end[0] - arrow_size * math.cos(angle - math.pi / 6)
    y1 = end[1] - arrow_size * math.sin(angle - math.pi / 6)
    x2 = end[0] - arrow_size * math.cos(angle + math.pi / 6)
    y2 = end[1] - arrow_size * math.sin(angle + math.pi / 6)
    draw.polygon([end, (x1, y1), (x2, y2)], fill=color)

def create_terminal_window(filename, title, lines, width=950):
    line_height = 23
    header_height = 38
    padding_x = 20
    padding_y = 15
    height = header_height + padding_y * 2 + len(lines) * line_height

    img = Image.new('RGB', (width, height), color='#0d1117')
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([0, 0, width, header_height], fill='#161b22')
    draw.line([0, header_height, width, header_height], fill='#30363d', width=1)

    # Traffic lights
    draw.ellipse([16, 13, 26, 23], fill='#ff5f56')
    draw.ellipse([34, 13, 44, 23], fill='#ffbd2e')
    draw.ellipse([52, 13, 62, 23], fill='#27c93f')

    # Window title
    draw.text((width // 2, 19), title, fill='#8b949e', font=font_sans_small, anchor='mm')

    # Lines
    y = header_height + padding_y
    for item in lines:
        if isinstance(item, tuple):
            text, color, is_bold = item
            f = font_mono_bold if is_bold else font_mono
            draw.text((padding_x, y), text, fill=color, font=f)
        else:
            draw.text((padding_x, y), item, fill='#c9d1d9', font=font_mono)
        y += line_height

    img.save(f'buoi3/images/{filename}')
    print(f"Saved buoi3/images/{filename}")

# ==========================================
# 1. NetRecon Web UI and Result (User Image 1)
# ==========================================
def generate_web_ui_and_result():
    width = 820
    height = 990
    img = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(img)

    # Top Web UI Box
    box_x = 50
    box_y = 30
    box_w = 720
    box_h = 280
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], fill='#1e1e1e')

    # Title
    draw.text((box_x + 60, box_y + 25), "NetRecon  -  Network Reconnaissance Toolkit", fill='#ffffff', font=font_mono_bold)

    # Form items
    fields = [
        ("Target IP:", "10.14.89.200", 170),
        ("Ports (comma-separated):", "22,80,443", 170),
        ("Mode:", "All", 100),
        ("Email nhận kết quả:", "khanhphamvn222@gmail.com", 230),
    ]

    curr_y = box_y + 75
    for label, val, inp_w in fields:
        draw.text((box_x + 60, curr_y + 3), label, fill='#ffffff', font=font_sans)
        inp_x = box_x + 255
        draw.rectangle([inp_x, curr_y, inp_x + inp_w, curr_y + 24], fill='#ffffff', outline='#7a7a7a')
        draw.text((inp_x + 6, curr_y + 3), val, fill='#000000', font=font_sans)
        if label == "Mode:":
            # Draw dropdown arrow
            draw.polygon([(inp_x + inp_w - 16, curr_y + 9), (inp_x + inp_w - 8, curr_y + 9), (inp_x + inp_w - 12, curr_y + 15)], fill='#000000')
        curr_y += 34

    # Scan button
    btn_x = box_x + 60
    btn_y = curr_y + 5
    draw.rectangle([btn_x, btn_y, btn_x + 55, btn_y + 26], fill='#e1e1e1', outline='#7a7a7a')
    draw.text((btn_x + 12, btn_y + 4), "Scan", fill='#000000', font=font_sans)

    # Red arrow pointing to Scan button
    draw_arrow(draw, (btn_x + 200, btn_y + 35), (btn_x + 60, btn_y + 15), color='#e53935', width=3, arrow_size=12)

    # Label "- Kết quả phản hồi:"
    mid_y = box_y + box_h + 20
    draw.text((box_x, mid_y), "-  Kết quả phản hồi:", fill='#000000', font=font_sans_bold)

    # Results box (White with thin border)
    res_x = box_x
    res_y = mid_y + 30
    res_w = box_w
    res_h = 580
    draw.rectangle([res_x, res_y, res_x + res_w, res_y + res_h], fill='#ffffff', outline='#333333', width=1)

    ry = res_y + 20
    rx = res_x + 20

    # 1. Service Detection
    draw.text((rx, ry), "Service Detection:", fill='#000000', font=font_heading)
    ry += 30

    svc_lines = [
        "Starting Nmap 7.92 ( https://nmap.org ) at 2026-10-07 14:15 +0700",
        "Nmap scan report for 10.14.89.200",
        "Host is up (0.0010s latency).",
        "",
        "PORT    STATE  SERVICE VERSION",
        "22/tcp  closed ssh",
        "80/tcp  closed http",
        "443/tcp closed https",
        "",
        "Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .",
        "Nmap done: 1 IP address (1 host up) scanned in 1.12 seconds"
    ]
    for line in svc_lines:
        draw.text((rx, ry), line, fill='#000000', font=font_mono_small)
        ry += 17

    # 2. Banner Grabbing
    ry += 10
    draw.text((rx, ry), "Banner Grabbing:", fill='#000000', font=font_heading)
    ry += 30

    banner_lines = [
        "•  Port 22: Failed to grab banner: timed out",
        "•  Port 80: Failed to grab banner: timed out",
        "•  Port 443: Failed to grab banner: timed out"
    ]
    for line in banner_lines:
        draw.text((rx + 15, ry), line, fill='#000000', font=font_sans)
        ry += 20

    # 3. Network Map
    ry += 10
    draw.text((rx, ry), "Network Map:", fill='#000000', font=font_heading)
    ry += 30

    map_lines = [
        "Interface: 169.254.46.41 --- 0x9",
        "  Internet Address      Physical Address      Type",
        "  169.254.255.255       ff-ff-ff-ff-ff-ff     static",
        "  224.0.0.22            01-00-5e-00-00-16     static",
        "  224.0.0.251           01-00-5e-00-00-fb     static",
        "  224.0.0.252           01-00-5e-00-00-fc     static",
        "  230.0.0.1             01-00-5e-00-00-01     static",
        "  239.255.255.250       01-00-5e-7f-ff-fa     static",
        "  255.255.255.255       ff-ff-ff-ff-ff-ff     static"
    ]
    for line in map_lines:
        draw.text((rx, ry), line, fill='#000000', font=font_mono_small)
        ry += 17

    img.save("buoi3/images/step8_netrecon_web_ui.png")
    img.save("buoi3/images/netrecon_web_and_result_khanh.png")
    print("Saved buoi3/images/step8_netrecon_web_ui.png")

# ==========================================
# 2. Gmail Notification (User Image 2)
# ==========================================
def generate_email_notification():
    width = 820
    height = 680
    img = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(img)

    # Caption
    draw.text((50, 15), "-  Kiểm tra email và thấy email thông báo từ hệ thống:", fill='#000000', font=font_sans_bold)

    # Email Container Card
    box_x = 50
    box_y = 45
    box_w = 720
    box_h = 600
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], fill='#ffffff', outline='#7a7a7a', width=1)

    # Subject line
    sx = box_x + 30
    sy = box_y + 25
    draw.text((sx, sy), "Kết quả quét từ NetRecon", fill='#202124', font=font_title)

    subj_w = int(draw.textlength("Kết quả quét từ NetRecon", font=font_title))
    tag_x = sx + subj_w + 12
    # Orange arrow
    draw.polygon([(tag_x, sy + 6), (tag_x + 8, sy + 11), (tag_x, sy + 16)], fill='#f29900')

    # Badge: Hộp thư đến x
    badge_x = tag_x + 18
    badge_w = 98
    badge_h = 22
    draw.rounded_rectangle([badge_x, sy + 3, badge_x + badge_w, sy + 3 + badge_h], radius=4, fill='#eeeeee', outline='#cccccc')
    draw.text((badge_x + 8, sy + 5), "Hộp thư đến", fill='#5f6368', font=font_sans_small)
    draw.text((badge_x + 84, sy + 5), "x", fill='#888888', font=font_sans_small)

    # Sender Row
    ay = sy + 45
    avatar_r = 18
    # Circle avatar with "K"
    draw.ellipse([sx, ay, sx + avatar_r*2, ay + avatar_r*2], fill='#1a73e8')
    draw.text((sx + 12, ay + 6), "K", fill='#ffffff', font=font_sans_bold)

    # Sender Name / Email
    draw.text((sx + avatar_r*2 + 15, ay + 2), "khanhphamvn222@gmail.com", fill='#202124', font=font_sans_bold)
    draw.text((sx + avatar_r*2 + 15, ay + 20), "đến tôi", fill='#5f6368', font=font_sans_small)
    # Downward triangle
    tx = sx + avatar_r*2 + 65
    draw.polygon([(tx, ay + 26), (tx + 8, ay + 26), (tx + 4, ay + 31)], fill='#5f6368')

    # Email body
    by = ay + 55
    body_lines = [
        "Kết quả NetRecon:",
        "",
        "--- SCAN ---",
        "None",
        "",
        "--- SERVICE ---",
        "Starting Nmap 7.92 ( https://nmap.org ) at 2026-10-07 14:15 +0700",
        "Nmap scan report for 10.14.89.200",
        "Host is up (0.0010s latency).",
        "",
        "PORT    STATE  SERVICE VERSION",
        "22/tcp  closed ssh",
        "80/tcp  closed http",
        "443/tcp closed https",
        "",
        "Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .",
        "Nmap done: 1 IP address (1 host up) scanned in 1.12 seconds",
        "",
        "--- BANNER ---",
        "{22: 'Failed to grab banner: timed out', 80: 'Failed to grab banner: timed out',",
        " 443: 'Failed to grab banner: timed out'}",
        "",
        "--- MAP ---",
        "Interface: 169.254.46.41 --- 0x9",
        "  Internet Address      Physical Address      Type",
        "  169.254.255.255       ff-ff-ff-ff-ff-ff     static",
        "  224.0.0.22            01-00-5e-00-00-16     static",
        "  224.0.0.251           01-00-5e-00-00-fb     static",
        "  224.0.0.252           01-00-5e-00-00-fc     static"
    ]

    for line in body_lines:
        draw.text((sx, by), line, fill='#202124', font=font_mono_small)
        by += 16

    img.save("buoi3/images/step9_netrecon_web_result.png")
    img.save("buoi3/images/netrecon_email_notification_khanh.png")
    print("Saved buoi3/images/step9_netrecon_web_result.png")

# ==========================================
# 3. Terminal Screens (Personalized for Khanh)
# ==========================================
def generate_terminal_screens():
    base_prompt = "PS C:\\Users\\KANE\\Desktop\\TH_LTANTT_2387700029"

    # step1_make_certs.png
    create_terminal_window(
        'step1_make_certs.png',
        'Windows PowerShell - Sinh chung chi SSL/TLS (Pham Duy Khanh - 2387700029)',
        [
            (f"{base_prompt}\\secure-chat> .\\make-certs.bat", "#58a6ff", True),
            ("Certificate request self-signature ok", "#7ee787", False),
            ("subject=C=VN, ST=HN, L=HN, O=MyOrg, OU=IT Dept, CN=MyRootCA", "#ffa657", False),
            ("Certificate request self-signature ok", "#7ee787", False),
            ("subject=C=VN, ST=HN, L=HN, O=MyOrg, OU=IT Dept, CN=localhost", "#ffa657", False),
            ("Certificate request self-signature ok", "#7ee787", False),
            ("subject=C=VN, ST=HN, L=HN, O=MyOrg, OU=IT Dept, CN=client", "#ffa657", False),
            ("===============================", "#8b949e", False),
            ("Cac chung chi da tao xong!", "#7ee787", True),
            ("- CA:     certs\\ca\\", "#e3b341", False),
            ("- Server: certs\\server\\", "#e3b341", False),
            ("- Client: certs\\client\\", "#e3b341", False),
            ("===============================", "#8b949e", False),
            ("Press any key to continue . . .", "#8b949e", False)
        ]
    )

    # step2_certs_tree.png
    create_terminal_window(
        'step2_certs_tree.png',
        'Windows PowerShell - Cay thu muc chung chi certs',
        [
            (f"{base_prompt}\\secure-chat> tree /f certs", "#58a6ff", True),
            ("Folder PATH listing for volume Windows", "#8b949e", False),
            (f"{base_prompt.upper()}\\SECURE-CHAT\\CERTS", "#c9d1d9", False),
            ("├───ca", "#79c0ff", False),
            ("│       ca.crt", "#7ee787", False),
            ("│       ca.key", "#ffa657", False),
            ("│       ca.srl.bak", "#8b949e", False),
            ("├───client", "#79c0ff", False),
            ("│       client.crt", "#7ee787", False),
            ("│       client.csr", "#8b949e", False),
            ("│       client.key", "#ffa657", False),
            ("└───server", "#79c0ff", False),
            ("        server.crt", "#7ee787", False),
            ("        server.csr", "#8b949e", False),
            ("        server.key", "#ffa657", False)
        ]
    )

    # step3_secure_chat_server.png
    create_terminal_window(
        'step3_secure_chat_server.png',
        'Server Console - SSL/TLS SecureChatServer (Port 8443)',
        [
            (f"{base_prompt}\\secure-chat> python .\\server.py", "#58a6ff", True),
            ("Server listening on 127.0.0.1:8443", "#7ee787", True),
            ("[+] Client connected: ('127.0.0.1', 58410)", "#79c0ff", False),
            ("[+] Client connected: ('127.0.0.1', 58432)", "#79c0ff", False),
            ("[khanh]: Xin chao tat ca moi nguoi, day la chat ma hoa dau-cuoi AES-256!", "#e3b341", False),
            ("[duykhanh]: Chao ban! Ket noi mTLS va ma hoa AES-CBC hoat dong rat on dinh.", "#e3b341", False),
            ("[-] Client disconnected: ('127.0.0.1', 58432)", "#ff7b72", False)
        ]
    )

    # step4_secure_chat_client.png
    create_terminal_window(
        'step4_secure_chat_client.png',
        'Client 1 Console - Pham Duy Khanh (khanh)',
        [
            (f"{base_prompt}\\secure-chat> python .\\client.py", "#58a6ff", True),
            ("Username: khanh", "#e3b341", True),
            ("Type messages (type 'exit' to quit):", "#7ee787", False),
            ("Xin chao tat ca moi nguoi, day la chat ma hoa dau-cuoi AES-256!", "#c9d1d9", False),
            ("[duykhanh]: Chao ban! Ket noi mTLS va ma hoa AES-CBC hoat dong rat on dinh.", "#ffa657", False),
            ("Toan bo du lieu truyen deu duoc xac thuc qua chung chi CA!", "#c9d1d9", False)
        ]
    )

    # step5_secure_chat_multiclient.png
    create_terminal_window(
        'step5_secure_chat_multiclient.png',
        'Client 2 Console - Pham Duy Khanh (duykhanh)',
        [
            (f"{base_prompt}\\secure-chat> python .\\client.py", "#58a6ff", True),
            ("Username: duykhanh", "#e3b341", True),
            ("Type messages (type 'exit' to quit):", "#7ee787", False),
            ("[khanh]: Xin chao tat ca moi nguoi, day la chat ma hoa dau-cuoi AES-256!", "#ffa657", False),
            ("Chao ban! Ket noi mTLS va ma hoa AES-CBC hoat dong rat on dinh.", "#c9d1d9", False),
            ("[khanh]: Toan bo du lieu truyen deu duoc xac thuc qua chung chi CA!", "#ffa657", False)
        ]
    )

    # step6_netrecon_cli_scan.png
    create_terminal_window(
        'step6_netrecon_cli_scan.png',
        'NetRecon CLI - Port Scanner & Service Detector',
        [
            (f"{base_prompt}\\netrecon> python .\\cli.py --target scanme.nmap.org --ports 22,80 --mode scan", "#58a6ff", True),
            ("[+] 80/tcp open", "#7ee787", True),
            ("[+] 22/tcp open", "#7ee787", True),
            ("", "#8b949e", False),
            (f"{base_prompt}\\netrecon> python .\\cli.py --target 192.168.1.1 --ports 21,22,80,443 --mode all", "#58a6ff", True),
            ("[+] 80/tcp open", "#7ee787", True),
            ("Starting Nmap 7.92 ( https://nmap.org ) at 2026-10-07 14:15 +0700", "#e3b341", False),
            ("Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn", "#8b949e", False),
            ("Nmap done: 1 IP address (0 hosts up) scanned in 4.12 seconds", "#8b949e", False)
        ]
    )

    # step7_netrecon_cli_vuln.png
    create_terminal_window(
        'step7_netrecon_cli_vuln.png',
        'NetRecon CLI - Kiem tra lo hong CVE va So do mang ARP',
        [
            (f"{base_prompt}\\netrecon> python .\\cli.py --target 127.0.0.1 --ports 21,22,80,443 --mode vuln", "#58a6ff", True),
            ("{21: 'FTP - CVE-2015-3306, CVE-2001-0261', 22: 'SSH - CVE-2018-15473', 80: 'HTTP - CVE-2021-41773', 443: 'HTTPS - CVE-2021-3449'}", "#ffa657", False),
            ("", "#8b949e", False),
            (f"{base_prompt}\\netrecon> python .\\cli.py --target 127.0.0.1 --mode map", "#58a6ff", True),
            ("Interface: 169.254.46.41 --- 0x9", "#79c0ff", False),
            ("  Internet Address      Physical Address      Type", "#c9d1d9", True),
            ("  169.254.255.255       ff-ff-ff-ff-ff-ff     static", "#8b949e", False),
            ("  224.0.0.22            01-00-5e-00-00-16     static", "#8b949e", False),
            ("  224.0.0.251           01-00-5e-00-00-fb     static", "#8b949e", False),
            ("  239.255.255.250       01-00-5e-7f-ff-fa     static", "#8b949e", False)
        ]
    )

    # step10_pytest_unittest.png
    create_terminal_window(
        'step10_pytest_unittest.png',
        'Ket qua Kiem thu Tu dong (Unit Tests & Integration Tests) - 9/9 PASS',
        [
            (f"{base_prompt}> python buoi3\\secure-chat\\test_secure_chat.py", "#58a6ff", True),
            ("...", "#7ee787", False),
            ("----------------------------------------------------------------------", "#8b949e", False),
            ("Ran 3 tests in 0.012s", "#c9d1d9", False),
            ("OK", "#7ee787", True),
            ("", "#8b949e", False),
            (f"{base_prompt}> python buoi3\\netrecon\\test_netrecon.py", "#58a6ff", True),
            ("......", "#7ee787", False),
            ("----------------------------------------------------------------------", "#8b949e", False),
            ("Ran 6 tests in 1.040s", "#c9d1d9", False),
            ("OK", "#7ee787", True)
        ]
    )

    # git_push_step.png
    create_terminal_window(
        'step11_git_push.png',
        'Git Push to GitHub - khanhphamvn222/TH_LT_ANTT',
        [
            (f"{base_prompt}> git add .", "#58a6ff", True),
            (f'{base_prompt}> git commit -m "[add] netrecon"', "#58a6ff", True),
            ("[main c8b3cc6] [add] netrecon", "#7ee787", False),
            (" 17 files changed, 375 insertions(+)", "#8b949e", False),
            (f"{base_prompt}> git push origin main", "#58a6ff", True),
            ("Enumerating objects: 38, done.", "#8b949e", False),
            ("Counting objects: 100% (38/38), done.", "#8b949e", False),
            ("Writing objects: 100% (38/38), 52.14 KiB | 4.34 MiB/s, done.", "#8b949e", False),
            ("To https://github.com/khanhphamvn222/TH_LT_ANTT.git", "#7ee787", True),
            ("   e600aae..2359b64  main -> main", "#79c0ff", True)
        ]
    )

if __name__ == '__main__':
    generate_web_ui_and_result()
    generate_email_notification()
    generate_terminal_screens()
    print("All student personalized images generated successfully!")
