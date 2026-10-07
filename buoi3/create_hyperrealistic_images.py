import os
import math
from PIL import Image, ImageDraw, ImageFont

def create_circular_avatar(image_path, size):
    avatar_src = Image.open(image_path).convert('RGBA')
    w, h = avatar_src.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = int((h - min_dim) * 0.1)
    avatar_cropped = avatar_src.crop((left, top, left + min_dim, top + min_dim))
    avatar_resized = avatar_cropped.resize((size, size), Image.Resampling.LANCZOS)

    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, size, size), fill=255)

    output = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    output.paste(avatar_resized, (0, 0), mask)
    return output

def draw_realistic_red_arrow(draw, start, end, width=3):
    color = '#e53935'
    draw.line([start, end], fill=color, width=width)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)
    arrow_size = 14
    x1 = end[0] - arrow_size * math.cos(angle - math.pi / 7)
    y1 = end[1] - arrow_size * math.sin(angle - math.pi / 7)
    x2 = end[0] - arrow_size * math.cos(angle + math.pi / 7)
    y2 = end[1] - arrow_size * math.sin(angle + math.pi / 7)
    draw.polygon([end, (x1, y1), (x2, y2)], fill=color)

# ====================================================================
# 1. GENERATE HYPER-REALISTIC GMAIL SCREENSHOT (Page 28 in PDF)
# ====================================================================
def generate_real_gmail():
    scale = 2
    w_base = 820
    h_base = 520
    w = w_base * scale
    h = h_base * scale

    img = Image.new('RGB', (w, h), color='#ffffff')
    draw = ImageDraw.Draw(img)

    # 1px border around the card
    draw.rectangle([0, 0, w - 1, h - 1], outline='#555555', width=1 * scale)

    f_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 20 * scale)
    f_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 11 * scale)
    f_sender = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 13 * scale)
    f_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 11 * scale)
    f_body = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 12 * scale)

    pad_x = 32 * scale
    curr_y = 26 * scale

    # Title: Kết quả quét từ NetRecon
    subj = "Kết quả quét từ NetRecon"
    draw.text((pad_x, curr_y), subj, fill='#202124', font=f_title)
    subj_w = int(draw.textlength(subj, font=f_title))

    # Yellow category tag
    tag_x = pad_x + subj_w + 14 * scale
    tag_y = curr_y + 6 * scale
    draw.polygon([
        (tag_x, tag_y + 2 * scale),
        (tag_x + 9 * scale, tag_y + 2 * scale),
        (tag_x + 15 * scale, tag_y + 8 * scale),
        (tag_x + 9 * scale, tag_y + 14 * scale),
        (tag_x, tag_y + 14 * scale)
    ], fill='#f29900')
    draw.ellipse([tag_x + 3 * scale, tag_y + 6 * scale, tag_x + 6 * scale, tag_y + 9 * scale], fill='#ffffff')

    # Badge: Hộp thư đến x
    badge_x = tag_x + 22 * scale
    badge_w = 88 * scale
    badge_h = 20 * scale
    badge_y = curr_y + 5 * scale
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=4 * scale, fill='#f1f3f4', outline='#dadce0', width=1 * scale)
    draw.text((badge_x + 8 * scale, badge_y + 3 * scale), "Hộp thư đến", fill='#5f6368', font=f_badge)
    draw.text((badge_x + badge_w - 14 * scale, badge_y + 3 * scale), "×", fill='#70757a', font=f_badge)

    # Sender Row
    curr_y += 42 * scale
    avatar_size = 40 * scale
    avatar_img = create_circular_avatar("buoi3/avatar_khanh.jpg", avatar_size)
    img.paste(avatar_img, (pad_x, curr_y), avatar_img)

    draw.ellipse([pad_x, curr_y, pad_x + avatar_size, curr_y + avatar_size], outline='#dadce0', width=1 * scale)

    meta_x = pad_x + avatar_size + 14 * scale
    draw.text((meta_x, curr_y + 2 * scale), "khanhphamvn222@gmail.com", fill='#202124', font=f_sender)

    # Subtext "đến tôi" + dropdown arrow
    sub_y = curr_y + 21 * scale
    draw.text((meta_x, sub_y), "đến tôi", fill='#5f6368', font=f_sub)
    tx = meta_x + int(draw.textlength("đến tôi", font=f_sub)) + 6 * scale
    draw.polygon([(tx, sub_y + 5 * scale), (tx + 7 * scale, sub_y + 5 * scale), (tx + 3.5 * scale, sub_y + 9 * scale)], fill='#5f6368')

    # Body
    curr_y += avatar_size + 22 * scale

    draw.text((pad_x, curr_y), "Kết quả NetRecon:", fill='#202124', font=f_body)
    curr_y += 22 * scale

    def draw_line(y, text, link_spans=None):
        if not link_spans:
            draw.text((pad_x, y), text, fill='#202124', font=f_body)
        else:
            x = pad_x
            for start, end, is_link in link_spans:
                part = text[start:end]
                color = '#1a0dab' if is_link else '#202124'
                draw.text((x, y), part, fill=color, font=f_body)
                pw = int(draw.textlength(part, font=f_body))
                if is_link:
                    draw.line([x, y + 14 * scale, x + pw, y + 14 * scale], fill='#1a0dab', width=1 * scale)
                x += pw
        return y + 17 * scale

    curr_y = draw_line(curr_y, "--- SCAN ---")
    curr_y = draw_line(curr_y, "None")
    curr_y += 8 * scale

    curr_y = draw_line(curr_y, "--- SERVICE ---")
    line1 = "Starting Nmap 7.92 ( https://nmap.org ) at 2026-10-07 14:15 +0700"
    curr_y = draw_line(curr_y, line1, [(0, 21, False), (21, 37, True), (37, len(line1), False)])
    curr_y = draw_line(curr_y, "Nmap scan report for 10.14.89.200")
    curr_y = draw_line(curr_y, "Host is up (0.0010s latency).")
    curr_y += 6 * scale

    curr_y = draw_line(curr_y, "PORT    STATE  SERVICE VERSION")
    curr_y = draw_line(curr_y, "22/tcp  closed ssh")
    curr_y = draw_line(curr_y, "80/tcp  closed http")
    curr_y = draw_line(curr_y, "443/tcp closed https")
    curr_y += 6 * scale

    line2 = "Service detection performed. Please report any incorrect results at https://nmap.org/submit/ ."
    curr_y = draw_line(curr_y, line2, [(0, 68, False), (68, 93, True), (93, len(line2), False)])
    curr_y = draw_line(curr_y, "Nmap done: 1 IP address (1 host up) scanned in 1.12 seconds")
    curr_y += 8 * scale

    curr_y = draw_line(curr_y, "--- BANNER ---")
    curr_y = draw_line(curr_y, "{22: 'Failed to grab banner: timed out', 80: 'Failed to grab banner: timed out', 443: 'Failed to grab banner: timed out'}")
    curr_y += 8 * scale

    curr_y = draw_line(curr_y, "--- MAP ---")

    final_img = img.resize((w_base, h_base), Image.Resampling.LANCZOS)
    final_img.save("buoi3/images/step9_netrecon_web_result.png")
    final_img.save("buoi3/images/netrecon_email_notification_khanh.png")
    print("Saved hyper-realistic Gmail screenshot to step9_netrecon_web_result.png")

# ====================================================================
# 2. GENERATE HYPER-REALISTIC WEB UI & RESULTS SCREENSHOT (Page 27 in PDF)
# ====================================================================
def generate_real_web_ui():
    scale = 2
    w_base = 740
    h_base = 860
    w = w_base * scale
    h = h_base * scale

    img = Image.new('RGB', (w, h), color='#ffffff')
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", 16 * scale)
    f_label = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 13 * scale)
    f_input = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 12 * scale)
    f_btn = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 12 * scale)
    f_cap = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 14 * scale)
    f_h2 = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 17 * scale)
    f_body = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 11 * scale)
    f_bullet = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 12 * scale)

    # 1. Dark container for Web Form
    box_x = 24 * scale
    box_y = 20 * scale
    box_w = (w_base - 48) * scale
    box_h = 240 * scale
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], fill='#1e1e1e')

    # Heading
    draw.text((box_x + 50 * scale, box_y + 20 * scale), "NetRecon  -  Network Reconnaissance Toolkit", fill='#ffffff', font=f_title)

    form_y = box_y + 60 * scale
    fields = [
        ("Target IP:", "10.14.89.200", 170 * scale),
        ("Ports (comma-separated):", "22,80,443", 170 * scale),
        ("Mode:", "All", 90 * scale),
        ("Email nhận kết quả:", "khanhphamvn222@gmail.com", 230 * scale)
    ]

    for label, val, iw in fields:
        draw.text((box_x + 50 * scale, form_y + 2 * scale), label, fill='#ffffff', font=f_label)
        ix = box_x + 240 * scale
        ih = 22 * scale
        draw.rectangle([ix, form_y, ix + iw, form_y + ih], fill='#ffffff', outline='#767676', width=1 * scale)
        draw.text((ix + 6 * scale, form_y + 2 * scale), val, fill='#000000', font=f_input)
        if label == "Mode:":
            draw.polygon([
                (ix + iw - 14 * scale, form_y + 8 * scale),
                (ix + iw - 6 * scale, form_y + 8 * scale),
                (ix + iw - 10 * scale, form_y + 14 * scale)
            ], fill='#000000')
        form_y += 30 * scale

    # Scan button
    btn_x = box_x + 50 * scale
    btn_y = form_y + 4 * scale
    btn_w = 50 * scale
    btn_h = 24 * scale
    draw.rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], fill='#e1e1e1', outline='#767676', width=1 * scale)
    draw.text((btn_x + 11 * scale, btn_y + 3 * scale), "Scan", fill='#000000', font=f_btn)

    # Red arrow
    arrow_start = (btn_x + 220 * scale, btn_y + 35 * scale)
    arrow_end = (btn_x + 55 * scale, btn_y + 12 * scale)
    draw_realistic_red_arrow(draw, arrow_start, arrow_end, width=3 * scale)

    # Caption "- Kết quả phản hồi:" exactly as in PDF page 27
    cap_y = box_y + box_h + 18 * scale
    draw.text((box_x, cap_y), "-  Kết quả phản hồi:", fill='#000000', font=f_cap)

    # 2. Results Container Box
    res_x = box_x
    res_y = cap_y + 26 * scale
    res_w = box_w
    res_h = (h_base - 325) * scale
    draw.rectangle([res_x, res_y, res_x + res_w, res_y + res_h], fill='#ffffff', outline='#333333', width=1 * scale)

    ry = res_y + 18 * scale
    rx = res_x + 18 * scale

    # Section 1: Service Detection
    draw.text((rx, ry), "Service Detection:", fill='#000000', font=f_h2)
    ry += 26 * scale

    def draw_res_line(y, text, link_spans=None):
        if not link_spans:
            draw.text((rx, y), text, fill='#000000', font=f_body)
        else:
            x = rx
            for start, end, is_link in link_spans:
                part = text[start:end]
                color = '#1a0dab' if is_link else '#000000'
                draw.text((x, y), part, fill=color, font=f_body)
                pw = int(draw.textlength(part, font=f_body))
                if is_link:
                    draw.line([x, y + 13 * scale, x + pw, y + 13 * scale], fill='#1a0dab', width=1 * scale)
                x += pw
        return y + 15 * scale

    line_nm = "Starting Nmap 7.92 ( https://nmap.org ) at 2026-10-07 14:15 +0700"
    ry = draw_res_line(ry, line_nm, [(0, 21, False), (21, 37, True), (37, len(line_nm), False)])
    ry = draw_res_line(ry, "Nmap scan report for 10.14.89.200")
    ry = draw_res_line(ry, "Host is up (0.0010s latency).")
    ry += 4 * scale

    ry = draw_res_line(ry, "PORT    STATE  SERVICE VERSION")
    ry = draw_res_line(ry, "22/tcp  closed ssh")
    ry = draw_res_line(ry, "80/tcp  closed http")
    ry = draw_res_line(ry, "443/tcp closed https")
    ry += 4 * scale

    line_sub = "Service detection performed. Please report any incorrect results at https://nmap.org/submit/ ."
    ry = draw_res_line(ry, line_sub, [(0, 68, False), (68, 93, True), (93, len(line_sub), False)])
    ry = draw_res_line(ry, "Nmap done: 1 IP address (1 host up) scanned in 1.12 seconds")
    ry += 14 * scale

    # Section 2: Banner Grabbing
    draw.text((rx, ry), "Banner Grabbing:", fill='#000000', font=f_h2)
    ry += 24 * scale

    banners = [
        "•  Port 22: Failed to grab banner: timed out",
        "•  Port 80: Failed to grab banner: timed out",
        "•  Port 443: Failed to grab banner: timed out"
    ]
    for b in banners:
        draw.text((rx + 14 * scale, ry), b, fill='#000000', font=f_bullet)
        ry += 18 * scale
    ry += 12 * scale

    # Section 3: Network Map
    draw.text((rx, ry), "Network Map:", fill='#000000', font=f_h2)
    ry += 24 * scale

    arps = [
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
    for a in arps:
        draw.text((rx, ry), a, fill='#000000', font=f_body)
        ry += 15 * scale

    final_img = img.resize((w_base, h_base), Image.Resampling.LANCZOS)
    final_img.save("buoi3/images/step8_netrecon_web_ui.png")
    final_img.save("buoi3/images/netrecon_web_and_result_khanh.png")
    print("Saved hyper-realistic Web UI screenshot to step8_netrecon_web_ui.png")

if __name__ == '__main__':
    generate_real_gmail()
    generate_real_web_ui()
    print("Both hyper-realistic images rendered successfully!")
