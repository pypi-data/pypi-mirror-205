import os
import re
import json
import base64
import pygame
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from binascii import a2b_hex
from Crypto.Cipher import AES
from urllib.parse import urlparse
from playwright._impl._page import Page
from playwright.sync_api import sync_playwright

# 解密后，去掉补足的空格用strip() 去掉


def aes_decrypt(text, key) -> str:
    key = key.encode("utf-8")
    mode = AES.MODE_ECB
    crypto = AES.new(key, mode)  # 以上均为固定写法
    plain_text = crypto.decrypt(a2b_hex(text))  # 将文本转为二进制之后参与解码
    return bytes.decode(plain_text).rstrip('\0')  # 返回解码后的数据


def get_len_num(text: str, num: int):
    lens = 0
    text_num = ''
    for strs in text:
        if len(strs.encode('utf-8')) == 3:
            lens += 2
        else:
            lens += 1
        text_num += strs
        if lens >= num+2:
            return text_num + '..'
    return text_num


def slicing_str(source_str: str, key: str, text_numbers=200, mode=1):
    if mode == 1:
        text_number = int(text_numbers/2)
        start = source_str.find(key)
        if start == -1:  # -1表示查询不到
            return source_str[:text_numbers]  # 字符不足200会保留最大长度,不会报错
        else:
            text_start = start - text_number
            if text_start < 0:
                text_start = 0
            text_end = start + len(key) + text_number
            if text_end > len(source_str)-1:
                text_end = len(source_str)-1
        text = source_str[text_start:text_end]
        return text
    elif mode == 2:
        text_start = source_str.find(key)
        text_end = text_start + len(key)

        return source_str[:text_start], source_str[text_start:text_end], source_str[text_end:]


def get_txt(capture_type: str, data: dict, keyword: str):

    if capture_type == 'headers':
        txt = ""
        request_headers_txt = data['request']['headers']
        response_headers_txt = data['response']['headers']
        txt += 'Request_Headers\n'
        for key in request_headers_txt:
            txt = txt + str(key) + ":" + str(request_headers_txt[key]) + '\n'

        txt += "\n"

        txt += 'Response_Headers\n'
        for key in response_headers_txt:
            txt = txt + str(key) + ":" + str(response_headers_txt[key]) + '\n'
        return txt

    elif capture_type == 'http':
        request_txt = data['request']
        method = request_txt["method"].upper()
        http_path = request_txt["path"].upper()

        http_scheme = request_txt["scheme"].upper()
        http_version = request_txt["http_version"].upper()
        http_host = request_txt["host"].upper()
        http_port = request_txt["port"]

        txt = f"{method} {http_path} {http_scheme}/{http_version}\nHost:{http_host}:{http_port}\n"

        request_headers_txt = data['request']['headers']
        for key in request_headers_txt:
            txt = txt + str(key) + ":" + str(request_headers_txt[key]) + '\n'
        return txt

    elif capture_type == 'response':
        txt = slicing_str(data['response']["response_body"], keyword)
    return str(txt)


def high_light_html(html5: str, lightwords: str = '') -> str:
    if lightwords == '':  # 如果没有需要高亮的关键字，则不处理页面
        return html5

    html5 = html5.replace(' />', '>')
    html = ''
    for i in re.findall(f'([\s\S]*?)?(<[/]?[a-zA-Z].*?>)', html5):
        for texts in i:
            if lightwords in texts:
                html += re.sub(lightwords,
                               f'<span style="background-color: yellow;">{lightwords}</span>', texts, flags=re.I)
            else:
                html += texts
    return html


def stitching_pictures(screen, message: str, outpath, ui):
    '''
    生成弹窗截图
    screen:底部图片
    '''
    ui_path = os.path.join(os.path.dirname(__file__), ui)
    font_path = os.path.join(os.path.dirname(__file__), 'mshei.ttf')
    pic_up = Image.open(ui_path)  # UI给的图
    setFont = ImageFont.truetype(font_path, 16)  # 設置字大小

    # 定义字体颜色
    black = (0, 0, 0)
    white = (255, 255, 255)

    if ui == 'dialogui.png':
        pic_down = Image.open(screen)
        pic_down_width = pic_down.width    # 获取底图的长度
        pic_up_width = pic_up.width    # 获取顶层图的长度
        pic_insert = int(pic_down_width/2 - pic_up_width /
                         2)   # 得出插入点的位置，转化为整数元组
        pic_down.paste(pic_up, (pic_insert, 0))  # 贴上UI

        draw = ImageDraw.Draw(pic_down)   # 贴上文字
        draw.text((pic_insert+20, 20),  # 设置字出現的位置
                  message,         # 文字
                  black,  # 字体颜色为黑色
                  font=setFont,         # 读取样式
                  direction=None)
        pic_down.save(outpath, format='PNG')  # 保存

    elif ui == 'titlegui.png':
        message = get_len_num(message, 94)
        draw = ImageDraw.Draw(pic_up)
        draw.text((0+177, 50),  # 设置URL
                  message,         # 文字
                  white,
                  font=setFont,         # 读取样式
                  direction=None)
        # pic_up 高80 宽1280
        # pic_down 高high 宽1280
        pic_down = Image.open(screen)
        pic_down_high = pic_down.height

        target = Image.new('RGB', (1280, 80+pic_down_high))
        target.paste(pic_up, (0, 0))  # 贴上UI
        target.paste(pic_down, (0, 80))  # 贴上UI
        target.save(outpath, format='PNG')


class TxtToImage:
    def __init__(self):
        pygame.init()
        self.cfg = {
            "width": 440,  # px
            "padding": (15, 18, 20, 18),
            "line-height": 20,  # px
            "font-size": 14,  # px
            "title-line-height": 32,  # px
            "title-font-size": 24,  # px
            "font-family": "mshei.ttf",  # 字体
            "font-color": (0, 0, 0),
            "font-antialiasing": True,  # 字体是否反锯齿
            "background-color": (255, 255, 255),
            "first-line-as-title":  False,  # 开启首行作为标题
            "break-word": False,  # 拆分单词
        }

        self.g_re_first_word = re.compile((u""
                                           + u"(%(prefix)s+\S%(postfix)s+)"  # 标点
                                           # 单词
                                           + u"|(%(prefix)s*\w+%(postfix)s*)"
                                           # 标点
                                           + u"|(%(prefix)s+\S)|(\S%(postfix)s+)"
                                           + u"|(\d+%%)"  # 百分数
                                           ) % {"prefix": u"['\"\(<\[\{‘“（《「『]", "postfix": u"[:'\"\)>\]\}：’”）》」』,;\.\?!，、；。？！]", })

    def getFontForPyGame(self, font_name="mshei.ttf", font_size=14):
        '''
        获取字体、字号
        '''
        font_path = os.path.join(os.path.dirname(__file__), font_name)
        return pygame.font.Font(font_path, font_size)

    def makeLineToWordsList(self, line, break_word=False):
        """
        将一行文本转为单词列表
        break_word: False保持单词完整性
        """
        if break_word:
            return [c for c in line]

        lst = []
        while line:
            ro = self.g_re_first_word.match(line)
            end = 1 if not ro else ro.end()
            lst.append(line[:end])
            line = line[end:]
        return lst

    def makeLongLineToLines(self, long_line, line_x, line_y, width, line_height, font, cn_char_width=0):
        """将一个长行分成多个可显示的短行"""

        if not long_line:
            return [None]

        words = self.makeLineToWordsList(long_line)
        lines = []

        if not cn_char_width:
            cn_char_width, h = font.size(u"汉")
        avg_char_per_line = int(width / cn_char_width)
        if avg_char_per_line <= 1:
            avg_char_per_line = 1

        while words:
            tmp_words = words[:avg_char_per_line]
            tmp_ln = "".join(tmp_words)
            w, h = font.size(tmp_ln)
            wc = len(tmp_words)
            while w < width and wc < len(words):
                wc += 1
                tmp_words = words[:wc]
                tmp_ln = "".join(tmp_words)
                w, h = font.size(tmp_ln)
            while w > width and len(tmp_words) > 1:
                tmp_words = tmp_words[:-1]
                tmp_ln = "".join(tmp_words)
                w, h = font.size(tmp_ln)

            if w > width and len(tmp_words) == 1:  # 处理一个长单词或长数字
                line_y = self.makeLongWordToLines(
                    tmp_words[0], line_x, line_y, width, line_height, font, lines)
                words = words[len(tmp_words):]
                continue

            line = {"x": line_x, "y": line_y, "text": tmp_ln, "font": font, }
            line_y += line_height
            words = words[len(tmp_words):]
            lines.append(line)

            if len(lines) >= 1:
                # 去掉长行的第二行开始的行首的空白字符
                while len(words) > 0 and not words[0].strip():
                    words = words[1:]
        return lines

    def makeLongWordToLines(self, long_word, line_x, line_y, width, line_height, font, lines):
        '''
        把超过最大宽度的字符,依据最大宽度拆成多个字符
        '''
        if not long_word:
            return line_y

        c = long_word[0]
        char_width, char_height = font.size(c)
        default_char_num_per_line = int(width / char_width)

        while long_word:
            tmp_ln = long_word[:default_char_num_per_line]
            w, h = font.size(tmp_ln)

            l = len(tmp_ln)
            while w < width and l < len(long_word):
                l += 1
                tmp_ln = long_word[:l]
                w, h = font.size(tmp_ln)
            while w > width and len(tmp_ln) > 1:
                tmp_ln = tmp_ln[:-1]
                w, h = font.size(tmp_ln)

            l = len(tmp_ln)
            long_word = long_word[l:]

            line = {"x": line_x, "y": line_y, "text": tmp_ln, "font": font, }
            line_y += line_height
            lines.append(line)
        return line_y

    def makeMatrix(self, txt, font, title_font, cfg):
        '''
        创建字体排列矩阵
        '''
        width = cfg["width"]
        data = {"width": width, "height": 0, "lines": [], }
        cur_x = cfg["padding"][3]
        cur_y = cfg["padding"][0]
        cn_char_width, h = font.size(u"汉")

        for ln_idx, ln in enumerate(txt.split("\n")):
            ln = ln.rstrip()
            if ln_idx == 0 and cfg["first-line-as-title"]:
                f = title_font
                line_height = cfg["title-line-height"]
            else:
                f = font
                line_height = cfg["line-height"]
            current_width = width - cur_x - cfg["padding"][1]
            lines = self.makeLongLineToLines(
                ln, cur_x, cur_y, current_width, line_height, f, cn_char_width=cn_char_width)
            cur_y += line_height * len(lines)

            data["lines"].extend(lines)

        data["height"] = cur_y + cfg["padding"][2]
        return data

    def makeImage(self, data, cfg):
        '''
        绘制文本
        '''
        width, height = data["width"], data["height"]
        im = Image.new("RGB", (width, height), cfg["background-color"])
        dr = ImageDraw.Draw(im)

        for ln_idx, line in enumerate(data["lines"]):
            self.__makeLine(im, line, cfg)

        return im

    def get_len(self, text):
        lens = 0
        for strs in text:
            if len(strs.encode('utf-8')) == 3:
                lens += 2
            else:
                lens += 1
        return lens

    def __makeLine(self, im, line, cfg):
        if not line:
            return
        x, y = line["x"], line["y"]
        text = line["text"]
        font = line["font"]
        if self.keyword in text:
            cn_char_width, h = font.size(u"汉")
            en_char_width, h = font.size(u"a")

            before, key, after = slicing_str(text, self.keyword, mode=2)

            if before != '':
                rtext_before = font.render(
                    before, cfg["font-antialiasing"], cfg["font-color"], cfg["background-color"])
                sio = BytesIO()
                pygame.image.save(rtext_before, sio)
                sio.seek(0)
                ln_im = Image.open(sio)
                im.paste(ln_im, (x, y))
                x += self.get_len(before)*en_char_width

            rtext_key = font.render(
                f'{key}', cfg["font-antialiasing"], cfg["font-color"], (255, 255, 0))
            sio = BytesIO()
            pygame.image.save(rtext_key, sio)
            sio.seek(0)
            ln_im = Image.open(sio)
            im.paste(ln_im, (x, y))
            x += self.get_len(key)*en_char_width

            if after != '':
                rtext_after = font.render(
                    after, cfg["font-antialiasing"], cfg["font-color"], cfg["background-color"])
                sio = BytesIO()
                pygame.image.save(rtext_after, sio)
                sio.seek(0)
                ln_im = Image.open(sio)
                im.paste(ln_im, (x, y))

        else:
            rtext = font.render(
                text, cfg["font-antialiasing"], cfg["font-color"], cfg["background-color"])
            sio = BytesIO()
            pygame.image.save(rtext, sio)
            sio.seek(0)
            ln_im = Image.open(sio)
            im.paste(ln_im, (x, y))

    def txt2im(self, txt, keyword, save=False, show=False):

        self.keyword = keyword
        font = self.getFontForPyGame(
            self.cfg["font-family"], self.cfg["font-size"])
        title_font = self.getFontForPyGame(
            self.cfg["font-family"], self.cfg["title-font-size"])

        data = self.makeMatrix(txt, font, title_font, self.cfg)
        image = self.makeImage(data, self.cfg)
        if save:
            image.save('test.png')
        if show:
            image.show()
        return image


class Capture:
    def __init__(self):
        self.keyword = ""
        self.screen = BytesIO()
        self.page: "Page" = None
        self.xss_flag = False
        self.send_payload = {}  # payload
        self.payload_url = ""  # payload_path
        self.html_new = ''  # 用于保存高亮后的页面，无需传参

    # 判断是否有弹窗，记录并关闭弹窗
    def handle_dialog(self, dialog):
        if self.keyword in str(dialog.message):  # 如果关键字 在 对话框（弹窗）中显示
            self.xss_flag = True  # 修改XSS标志为 True
            self.xss_message = str(dialog.message)
        dialog.dismiss()  # 关闭对话框

    # 删除请求头Host域和字段长度检测，之后加到page上
    def set_headers(self, headers):
        headers = headers.strip()  # 切掉可能的空字符
        if headers == '':
            return  # 切完为空则结束
        '''
        不为空则进行下一步，对请求头进行加工，剔除Host域和字段长度检测。Host、host、Content-Length 
        '''
        add_headers = json.loads(headers)
        if 'Host' in add_headers:
            del add_headers['Host']
        if 'host' in add_headers:
            del add_headers['host']
        if 'Content-Length' in add_headers:
            del add_headers['Content-Length']
        self.page.set_extra_http_headers(add_headers)  # 把请求头加载在page上

    def capture(self, url, method, headers, data, capture_type: str, keyword='', payload='', payload_path='', ):
        self.payload_url = payload_path
        self.keyword = keyword
        self.data = data
        self.url = url
        map_cookie = []  # <List[Dict]>
        domain = urlparse(url).netloc  # 确认当前域：1.增到cookie中2.防止调到外链
        cookie = json.loads(headers).get("Cookie", "")
        for i in cookie.split("; "):
            if "=" in i:
                k, v = i.split("=", 1)
                map_cookie.append(
                    {"name": k, "value": v, "path": "/", "domain": domain})
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, ignore_default_args=[
                                        "--mute-audio"])  # 禁用声音
            context = browser.new_context(
                ignore_https_errors=True, bypass_csp=True)
            if len(map_cookie) > 0:
                context.add_cookies(map_cookie)

            self.page = context.new_page()
            self.set_headers(headers=headers)  # 执行set_headers处理请求头头方法
            self.page.on("dialog", self.handle_dialog)  # 对弹窗执行handle_dialog方法
            self.page.goto(url)  # 打开页面
            if method.upper() == 'POST':  # 如果请求是post
                self.send_payload = payload
                self.page.locator("text=Submit").click()
            html = self.page.content()
            html = html.replace("b'", '')
            html = html.replace(r"\r", '')
            html = html.replace(r"\n", '')
            html = html.replace(r"\t", '')
            html_new = high_light_html(html, self.keyword)
            self.page.set_content(html_new)
            self.screenshot(capture_type)    # 调用screenshot方法，存贮图像至内存
            browser.close()  # 关闭整个浏览器（区别于关闭单个页面）

    def screenshot(self, capture_type):
        if capture_type == 'page':
            screen = BytesIO()
            if self.xss_flag != True:  # 如果沒有检测到弹窗
                screen.write(self.page.screenshot(full_page=True, type="png"))
            else:
                screen_diolog = BytesIO()
                screen_diolog.write(self.page.screenshot(
                    full_page=True, type="png"))
                stitching_pictures(screen_diolog, self.xss_message,
                                   outpath=screen, ui='dialogui.png')
            stitching_pictures(
                screen, self.url, self.screen, ui='titlegui.png')

        elif capture_type == 'headers':
            txt = get_txt(capture_type, self.data, self.keyword)
            txttoimage = TxtToImage()
            self.screen = txttoimage.txt2im(txt, self.keyword, show=False)

    def image(self, show=False):
        if show:
            img = Image.open(self.screen)
            img.show()
        screen = base64.b64encode(self.screen.getvalue()).decode("utf-8")
        return screen


def run_snapshot(url,
                 keyword='',
                 cookie = '',
                 method = 'GET',
                 capture_type='page',
                 ):
    '''
    url : aim url
    keyword : str
    '''
    data = {'request': {
        'url': url,
        'method': method,
        'headers': {'cookie': cookie},
        'body': '', },
        'response': {
        'headers': {'cookie': cookie}, }
    }
    request = data['request']
    request['headers']['cookie'] = 'security_level=0; PHPSESSID=gttrr52vcv5fpdm140afqher14; security=low'
    ca = Capture()
    ca.capture(url=request['url'],
               method=request['method'],
               headers=json.dumps(request['headers']),
               payload=request['body'],
               data=data,
               keyword=keyword,
               capture_type=capture_type)
    img = ca.image(show=False)
    if len(img) > 0:
        return img
    else:
        return None
