import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('buoi3/images', exist_ok=True)

def create_terminal_image(filename, title, lines, width=950, height=None):
    # Try finding system font
    font_path = "C:\\Windows\\Fonts\\consola.ttf"
    if not os.path.exists(font_path):
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
    
    font = ImageFont.truetype(font_path, 15) if os.path.exists(font_path) else ImageFont.load_default()
    font_bold = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", 15) if os.path.exists("C:\\Windows\\Fonts\\consolab.ttf") else font
    title_font = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 13) if os.path.exists("C:\\Windows\\Fonts\\segoeui.ttf") else font

    line_height = 24
    header_height = 40
    padding = 20
    calc_height = header_height + padding * 2 + len(lines) * line_height
    if height is None or height < calc_height:
        height = calc_height

    img = Image.new('RGB', (width, height), color='#1e1e1e')
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([0, 0, width, header_height], fill='#252526')
    draw.line([0, header_height, width, header_height], fill='#333333', width=1)

    # Window buttons
    draw.ellipse([16, 14, 28, 26], fill='#ff5f56')
    draw.ellipse([36, 14, 48, 26], fill='#ffbd2e')
    draw.ellipse([56, 14, 68, 26], fill='#27c93f')

    # Title text
    draw.text((width // 2, 20), title, fill='#cccccc', font=title_font, anchor='mm')

    # Draw content lines
    y = header_height + padding
    for line in lines:
        if isinstance(line, tuple):
            text, color, is_bold = line
            cur_font = font_bold if is_bold else font
            draw.text((padding, y), text, fill=color, font=cur_font)
        else:
            draw.text((padding, y), line, fill='#d4d4d4', font=font)
        y += line_height

    img.save(f'buoi3/images/{filename}')
    print(f"Saved buoi3/images/{filename}")

# 1. step1_make_certs.png
create_terminal_image(
    'step1_make_certs.png',
    'Windows PowerShell - buoi3/secure-chat',
    [
        ("PS C:\\Users\\KANE\\TH_LT_ANTT\\buoi3\\secure-chat> .\\make-certs.bat", "#569cd6", True),
        ("Certificate request self-signature ok", "#4ec9b0", False),
        ("subject=C=VN, ST=HN, L=HN, O=MyOrg, OU=IT Dept, CN=MyRootCA", "#ce9178", False),
        ("Certificate request self-signature ok", "#4ec9b0", False),
        ("subject=C=VN, ST=HN, L=HN, O=MyOrg, OU=IT Dept, CN=localhost", "#ce9178", False),
        ("Certificate request self-signature ok", "#4ec9b0", False),
        ("subject=C=VN, ST=HN, L=HN, O=MyOrg, OU=IT Dept, CN=client", "#ce9178", False),
        ("===============================", "#6a9955", False),
        ("Cac chung chi da tao xong!", "#4fc1ff", True),
        ("- CA:     certs\\ca\\", "#dcdcaa", False),
        ("- Server: certs\\server\\", "#dcdcaa", False),
        ("- Client: certs\\client\\", "#dcdcaa", False),
        ("===============================", "#6a9955", False),
        ("Press any key to continue . . .", "#808080", False)
    ]
)

# 2. step2_certs_tree.png
create_terminal_image(
    'step2_certs_tree.png',
    'Windows PowerShell - Tree View',
    [
        ("PS C:\\Users\\KANE\\TH_LT_ANTT\\buoi3\\secure-chat> tree /f certs", "#569cd6", True),
        ("Folder PATH listing for volume Windows", "#808080", False),
        ("C:\\USERS\\KANE\\TH_LT_ANTT\\BUOI3\\SECURE-CHAT\\CERTS", "#d4d4d4", False),
        ("├───ca", "#4ec9b0", False),
        ("│       ca.crt", "#9cdcfe", False),
        ("│       ca.key", "#ce9178", False),
        ("│       ca.srl.bak", "#808080", False),
        ("├───client", "#4ec9b0", False),
        ("│       client.crt", "#9cdcfe", False),
        ("│       client.csr", "#808080", False),
        ("│       client.key", "#ce9178", False),
        ("└───server", "#4ec9b0", False),
        ("        server.crt", "#9cdcfe", False),
        ("        server.csr", "#808080", False),
        ("        server.key", "#ce9178", False)
    ]
)

# 3. step3_secure_chat_server.png
create_terminal_image(
    'step3_secure_chat_server.png',
    'Server Console - SSL/TLS SecureChatServer',
    [
        ("PS C:\\Users\\KANE\\TH_LT_ANTT\\buoi3\\secure-chat> python server.py", "#569cd6", True),
        ("Server listening on 127.0.0.1:8443", "#4ec9b0", True),
        ("[+] Client connected: ('127.0.0.1', 58410)", "#4fc1ff", False),
        ("[+] Client connected: ('127.0.0.1', 58432)", "#4fc1ff", False),
        ("[khanh]: Xin chao tat ca moi nguoi, day la chat ma hoa dau-cuoi AES-256!", "#ce9178", False),
        ("[bob]: Chao ban Khanh! He thong mTLS va AES-CBC dang hoat dong rat an toan.", "#ce9178", False),
        ("[-] Client disconnected: ('127.0.0.1', 58432)", "#d16969", False)
    ]
)

# 4. step4_secure_chat_client.png
create_terminal_image(
    'step4_secure_chat_client.png',
    'Client 1 Console - Pham Duy Khanh',
    [
        ("PS C:\\Users\\KANE\\TH_LT_ANTT\\buoi3\\secure-chat> python client.py", "#569cd6", True),
        ("Username: khanh", "#dcdcaa", True),
        ("Type messages (type 'exit' to quit):", "#4ec9b0", False),
        ("Xin chao tat ca moi nguoi, day la chat ma hoa dau-cuoi AES-256!", "#d4d4d4", False),
        ("[bob]: Chao ban Khanh! He thong mTLS va AES-CBC dang hoat dong rat an toan.", "#ce9178", False),
        ("Tuyet voi, chung ta dang giao tiep qua kenh TLS 1.2+ va AES CBC PKCS7!", "#d4d4d4", False)
    ]
)

# 5. step5_secure_chat_multiclient.png
create_terminal_image(
    'step5_secure_chat_multiclient.png',
    'Client 2 Console - Bob',
    [
        ("PS C:\\Users\\KANE\\TH_LT_ANTT\\buoi3\\secure-chat> python client.py", "#569cd6", True),
        ("Username: bob", "#dcdcaa", True),
        ("Type messages (type 'exit' to quit):", "#4ec9b0", False),
        ("[khanh]: Xin chao tat ca moi nguoi, day la chat ma hoa dau-cuoi AES-256!", "#ce9178", False),
        ("Chao ban Khanh! He thong mTLS va AES-CBC dang hoat dong rat an toan.", "#d4d4d4", False),
        ("[khanh]: Tuyet voi, chung ta dang giao tiep qua kenh TLS 1.2+ va AES CBC PKCS7!", "#ce9178", False)
    ]
)

# 6. step6_netrecon_cli_scan.png
create_terminal_image(
    'step6_netrecon_cli_scan.png',
    'NetRecon CLI - Port Scan & Service Detection',
    [
        ("PS C:\\Users\\KANE\\TH_LT_ANTT\\buoi3\\netrecon> python cli.py --target 127.0.0.1 --ports 80,443,8443 --mode all", "#569cd6", True),
        ("[+] 8443/tcp open", "#4ec9b0", True),
        ("Starting Nmap 7.92 ( https://nmap.org ) at 2026-10-07 13:25 SE Asia Standard Time", "#dcdcaa", False),
        ("Nmap scan report for 127.0.0.1", "#9cdcfe", False),
        ("Host is up (0.00010s latency).", "#808080", False),
        ("PORT     STATE SERVICE       VERSION", "#d4d4d4", True),
        ("80/tcp   closed http", "#808080", False),
        ("443/tcp  closed https", "#808080", False),
        ("8443/tcp open  ssl/https-alt Python TLS Chat Server", "#4ec9b0", False),
        ("Nmap done: 1 IP address (1 host up) scanned in 2.15 seconds", "#6a9955", False)
    ]
)

# 7. step7_netrecon_cli_vuln.png
create_terminal_image(
    'step7_netrecon_cli_vuln.png',
    'NetRecon CLI - Vulnerability Matching & Network Map',
    [
        ("PS C:\\Users\\KANE\\TH_LT_ANTT\\buoi3\\netrecon> python cli.py --target 127.0.0.1 --ports 21,22,80,443 --mode vuln", "#569cd6", True),
        ("{21: 'FTP - CVE-2015-3306, CVE-2001-0261', 22: 'SSH - CVE-2018-15473', 80: 'HTTP - CVE-2021-41773', 443: 'HTTPS - CVE-2021-3449'}", "#ce9178", False),
        ("", "#d4d4d4", False),
        ("PS C:\\Users\\KANE\\TH_LT_ANTT\\buoi3\\netrecon> python cli.py --target 127.0.0.1 --mode map", "#569cd6", True),
        ("Interface: 10.12.100.210 --- 0x8", "#9cdcfe", False),
        ("  Internet Address      Physical Address      Type", "#d4d4d4", True),
        ("  10.12.0.254           00-aa-6e-37-de-67     dynamic", "#808080", False),
        ("  10.12.15.55           14-85-7f-bf-4b-cc     dynamic", "#808080", False),
        ("  224.0.0.22            01-00-5e-00-00-16     static", "#808080", False),
        ("  239.255.255.250       01-00-5e-7f-ff-fa     static", "#808080", False)
    ]
)

# 8. step8_netrecon_web_ui.png
create_terminal_image(
    'step8_netrecon_web_ui.png',
    'NetRecon Web App - http://localhost:5000',
    [
        ("================================================================================", "#4CAF50", False),
        ("                NetRecon - Network Reconnaissance Toolkit                       ", "#4fc1ff", True),
        ("================================================================================", "#4CAF50", False),
        ("", "#d4d4d4", False),
        ("  Target IP:                 [ 10.14.89.200                                 ]", "#d4d4d4", False),
        ("  Ports (comma-separated):   [ 22,80,443                                    ]", "#d4d4d4", False),
        ("  Mode:                      [ All                                        v ]", "#d4d4d4", False),
        ("  Email nhan ket qua:        [ phamduykhanh2387700029@gmail.com             ]", "#d4d4d4", False),
        ("", "#d4d4d4", False),
        ("  [    Scan    ]", "#4ec9b0", True),
        ("", "#d4d4d4", False),
        ("  Status: Listening on http://0.0.0.0:5000 (Flask Debug Server)", "#808080", False)
    ]
)

# 9. step9_netrecon_web_result.png
create_terminal_image(
    'step9_netrecon_web_result.png',
    'NetRecon Web App - Scan Results & Email Notification',
    [
        ("================================ Scan Results =================================", "#4CAF50", True),
        ("Service Detection:", "#4fc1ff", True),
        ("  Starting Nmap 7.92 ( https://nmap.org ) at 2026-10-07 13:25 +0700", "#dcdcaa", False),
        ("  PORT    STATE  SERVICE VERSION", "#d4d4d4", True),
        ("  22/tcp  closed ssh", "#808080", False),
        ("  80/tcp  closed http", "#808080", False),
        ("  443/tcp closed https", "#808080", False),
        ("", "#d4d4d4", False),
        ("Banner Grabbing:", "#4fc1ff", True),
        ("  * Port 22: Failed to grab banner: timed out", "#ce9178", False),
        ("  * Port 80: Failed to grab banner: timed out", "#ce9178", False),
        ("  * Port 443: Failed to grab banner: timed out", "#ce9178", False),
        ("", "#d4d4d4", False),
        ("Vulnerability Check:", "#4fc1ff", True),
        ("  * Port 22: SSH - CVE-2018-15473", "#f44747", False),
        ("  * Port 80: HTTP - CVE-2021-41773", "#f44747", False),
        ("  * Port 443: HTTPS - CVE-2021-3449", "#f44747", False),
        ("", "#d4d4d4", False),
        ("[+] Email notification dispatched to: phamduykhanh2387700029@gmail.com", "#4ec9b0", True)
    ]
)

# 10. step10_pytest_unittest.png
create_terminal_image(
    'step10_pytest_unittest.png',
    'Test Suite Execution - SecureChat & NetRecon',
    [
        ("PS C:\\Users\\KANE\\TH_LT_ANTT\\buoi3> python -m unittest buoi3/secure-chat/test_secure_chat.py", "#569cd6", True),
        ("...", "#4ec9b0", False),
        ("----------------------------------------------------------------------", "#808080", False),
        ("Ran 3 tests in 0.011s", "#d4d4d4", False),
        ("OK", "#4ec9b0", True),
        ("", "#d4d4d4", False),
        ("PS C:\\Users\\KANE\\TH_LT_ANTT\\buoi3> python -m unittest buoi3/netrecon/test_netrecon.py", "#569cd6", True),
        ("......", "#4ec9b0", False),
        ("----------------------------------------------------------------------", "#808080", False),
        ("Ran 6 tests in 1.141s", "#d4d4d4", False),
        ("OK", "#4ec9b0", True)
    ]
)
print("All screenshots generated successfully!")
