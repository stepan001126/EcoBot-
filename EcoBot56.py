import pygame
import pygame.gfxdraw
import math
import random
import json
import os
import shutil
import sys
from enum import Enum
from datetime import datetime

# Инициализация Pygame и mixer для музыки
pygame.init()
pygame.mixer.init()

# ----- ПУТИ К ПАПКАМ (версия 56) -----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPDATA = os.environ.get("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
BACKUP_DIR = os.path.join(APPDATA, "EcoBot")

SAVES_DIR = os.path.join(BASE_DIR, "saves")
BACKUP_SAVES_DIR = os.path.join(BACKUP_DIR, "saves")

os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(SAVES_DIR, exist_ok=True)
try:
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(BACKUP_SAVES_DIR, exist_ok=True)
except PermissionError:
    pass

SETTINGS_FILE = os.path.join(SAVES_DIR, "settings.json")
BACKUP_SETTINGS = os.path.join(BACKUP_SAVES_DIR, "settings.json")

# Константы экрана
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
BACKGROUND_COLOR = (5, 5, 20)

# ----- ВРЕМЕННАЯ СИСТЕМА (версия 56) -----
REAL_SECONDS_PER_GAME_DAY = 3600
GAME_HOURS_PER_DAY = 24
GAME_MINUTES_PER_HOUR = 60
GAME_SECONDS_PER_MINUTE = 60

GAME_SECONDS_PER_REAL_SECOND = 24
GAME_SECONDS_PER_DAY = GAME_HOURS_PER_DAY * GAME_MINUTES_PER_HOUR * GAME_SECONDS_PER_MINUTE

# Текущий язык (по умолчанию русский)
current_lang = "ru"


# ---------------------- СИСТЕМА ЛОКАЛИЗАЦИИ ----------------------
LANGUAGES = {
    "ru": {
        "name": "Русский", "native": "Русский", "menu_title": "EcoBot 56",
        "subtitle": "Галактический уборщик", "play": "ИГРАТЬ", "settings": "НАСТРОЙКИ",
        "info": "ИНФОРМАЦИЯ", "exit": "ВЫХОД", "back": "НАЗАД", "save": "СОХРАНИТЬ",
        "close": "ЗАКРЫТЬ", "create": "СОЗДАТЬ", "cancel": "ОТМЕНА",
        "role_select": "ВЫБОР РОЛИ", "single": "Одиночная игра",
        "navigator": "Штурман", "engineer": "Инженер", "operator": "Оператор связи",
        "captain": "Капитан", "save_select": "ВЫБОР СОХРАНЕНИЯ",
        "new_save": "+ НОВОЕ СОХРАНЕНИЕ", "no_saves": "Нет сохранений. Создайте новое!",
        "new_save_title": "СОЗДАТЬ НОВОЕ СОХРАНЕНИЕ", "enter_name": "Введите название:",
        "containers": "Контейнеры с мусором", "metal": "Металл", "plastic": "Пластик",
        "glass": "Стекло", "radioactive": "Радиоактивный", "composite": "Композит",
        "processed": "Переработано", "no_resources": "Нет ресурсов",
        "sent_to_earth": "Отправлено на Землю", "total_score": "Всего баллов",
        "energy": "Энергия", "cargo": "Груз", "range": "Дальность", "xenon": "Ксенон",
        "controls": "УПРАВЛЕНИЕ:", "tab": "TAB - Сменить режим",
        "wasd": "WASD - Тяга / Пучок", "qe": "Q/E - Вертикальная тяга",
        "space": "SPACE - Сканирование", "beam": "C - Ионный пучок",
        "collect": "Y - Собрать мусор", "process": "P - Переработка",
        "send": "F - Отправить", "refuel": "G - Дозаправка",
        "reset": "R - Сброс цели", "containers_toggle": "1/2 - Контейнеры",
        "upgrades": "U - Улучшения", "pause": "ESC - Пауза",
        "mode_robot": "Режим: РОБОТ [TAB]", "mode_beam": "Режим: ПУЧОК [TAB]",
        "direction": "Напр", "upgrade_shop": "МАГАЗИН УЛУЧШЕНИЙ",
        "your_score": "Ваши баллы", "purchased": "КУПЛЕНО",
        "buy_hint": "Нажмите 1, 2, 3 для покупки или ESC для выхода",
        "pause_menu": "ПАУЗА", "continue": "ПРОДОЛЖИТЬ",
        "save_game": "СОХРАНИТЬ ИГРУ", "reset_game": "СБРОСИТЬ ИГРУ",
        "exit_menu": "ВЫЙТИ В МЕНЮ", "settings_title": "НАСТРОЙКИ",
        "language": "Язык", "search_language": "Поиск языка...",
        "day": "День", "night": "Ночь", "mission": "Миссия",
        "mission_complete": "МИССИЯ ВЫПОЛНЕНА!", "mission_progress": "Прогресс",
        "level": "Уровень", "level_progress": "Прогресс уровня",
        "all_missions_complete": "Все миссии выполнены!",
        "time_system": "1 день = 1 час, 1 час = 2.5 мин",
        "info_title": "ПРАВИЛА ИГРЫ",
        "rules": [
            "🌍 Миссия: Очистить галактику от космического мусора!",
            "",
            "🚀 ДВИЖЕНИЕ (нулевая гравитация):",
            "  • WASD - включить тягу в направлении",
            "  • Q/E - вертикальная тяга",
            "  • Корабль движется по инерции",
            "  • Для остановки включите тягу в обратном направлении",
            "  • Скорость отображается в статусе робота",
            "",
            "⏱ ВРЕМЯ:",
            "  • 1 игровой день (24 часа) = 1 реальный час",
            "  • 1 игровой час = 150 секунд (2.5 мин)",
            "  • Солнце восходит в 6:00, заходит в 18:00",
            "",
            "🤖 Управление роботом EcoBot:",
            "  • TAB - переключить режим управления",
            "  • WASD - тяга / управление пучком",
            "  • Q/E - вертикальная тяга / вертикаль пучка",
            "  • SPACE - сканирование", "  • C - ионный пучок (мелкий мусор)",
            "  • Y - собрать крупный мусор", "  • P - переработка",
            "  • F - отправка на Землю", "  • G - дозаправка ксеноном",
            "  • R - сброс цели", "  • 1/2 - вкл/выкл контейнеры",
            "  • U - магазин улучшений", "  • ESC - пауза/меню"
        ]
    },
    "en": {
        "name": "English", "native": "English", "menu_title": "EcoBot 56",
        "subtitle": "Galactic Cleaner", "play": "PLAY", "settings": "SETTINGS",
        "info": "INFO", "exit": "EXIT", "back": "BACK", "save": "SAVE",
        "close": "CLOSE", "create": "CREATE", "cancel": "CANCEL",
        "role_select": "SELECT ROLE", "single": "Single Player",
        "navigator": "Navigator", "engineer": "Engineer",
        "operator": "Comms Officer", "captain": "Captain",
        "save_select": "SELECT SAVE", "new_save": "+ NEW SAVE",
        "no_saves": "No saves. Create a new one!",
        "new_save_title": "CREATE NEW SAVE", "enter_name": "Enter name:",
        "containers": "Waste Containers", "metal": "Metal", "plastic": "Plastic",
        "glass": "Glass", "radioactive": "Radioactive", "composite": "Composite",
        "processed": "Processed", "no_resources": "No resources",
        "sent_to_earth": "Sent to Earth", "total_score": "Total score",
        "energy": "Energy", "cargo": "Cargo", "range": "Range", "xenon": "Xenon",
        "controls": "CONTROLS:", "tab": "TAB - Switch mode",
        "wasd": "WASD - Thrust / Beam", "qe": "Q/E - Vertical thrust",
        "space": "SPACE - Scan", "beam": "C - Ion beam",
        "collect": "Y - Collect debris", "process": "P - Process",
        "send": "F - Send", "refuel": "G - Refuel",
        "reset": "R - Reset target", "containers_toggle": "1/2 - Containers",
        "upgrades": "U - Upgrades", "pause": "ESC - Pause",
        "mode_robot": "Mode: ROBOT [TAB]", "mode_beam": "Mode: BEAM [TAB]",
        "direction": "Dir", "upgrade_shop": "UPGRADE SHOP",
        "your_score": "Your score", "purchased": "PURCHASED",
        "buy_hint": "Press 1, 2, 3 to buy or ESC to exit",
        "pause_menu": "PAUSE", "continue": "CONTINUE",
        "save_game": "SAVE GAME", "reset_game": "RESET GAME",
        "exit_menu": "EXIT TO MENU", "settings_title": "SETTINGS",
        "language": "Language", "search_language": "Search language...",
        "day": "Day", "night": "Night", "mission": "Mission",
        "mission_complete": "MISSION COMPLETE!", "mission_progress": "Progress",
        "level": "Level", "level_progress": "Level progress",
        "all_missions_complete": "All missions complete!",
        "time_system": "1 day = 1 hour, 1 hour = 2.5 min",
        "info_title": "GAME RULES",
        "rules": [
            "🌍 Mission: Clean the galaxy from space debris!",
            "",
            "🚀 MOVEMENT (zero gravity):",
            "  • WASD - apply thrust in direction",
            "  • Q/E - vertical thrust",
            "  • Ship moves by inertia",
            "  • To stop, apply thrust in opposite direction",
            "  • Speed displayed in robot status",
            "",
            "⏱ TIME: 1 game day (24 hours) = 1 real hour",
            "  • Sun rises at 6:00, sets at 18:00",
            "",
            "🤖 EcoBot controls:",
            "  • TAB - Switch mode", "  • WASD - Thrust / Beam",
            "  • Q/E - Vertical thrust", "  • SPACE - Scan",
            "  • C - Ion beam (small debris)", "  • Y - Collect large debris",
            "  • P - Process", "  • F - Send to Earth",
            "  • G - Refuel xenon", "  • R - Reset target",
            "  • 1/2 - Toggle containers", "  • U - Upgrade shop",
            "  • ESC - Pause/Menu"
        ]
    },
    "zh": {
        "name": "中文", "native": "中文", "menu_title": "EcoBot 56",
        "subtitle": "银河清洁工", "play": "开始游戏", "settings": "设置",
        "info": "信息", "exit": "退出", "back": "返回", "save": "保存",
        "close": "关闭", "create": "创建", "cancel": "取消",
        "role_select": "选择角色", "single": "单人游戏",
        "navigator": "领航员", "engineer": "工程师",
        "operator": "通讯官", "captain": "船长",
        "save_select": "选择存档", "new_save": "+ 新存档",
        "no_saves": "没有存档。创建一个新的！",
        "new_save_title": "创建新存档", "enter_name": "输入名称：",
        "containers": "垃圾容器", "metal": "金属", "plastic": "塑料",
        "glass": "玻璃", "radioactive": "放射性", "composite": "复合材料",
        "processed": "已处理", "no_resources": "没有资源",
        "sent_to_earth": "已发送到地球", "total_score": "总分",
        "energy": "能量", "cargo": "货物", "range": "范围", "xenon": "氙气",
        "controls": "控制：", "tab": "TAB - 切换模式",
        "wasd": "WASD - 推力 / 光束", "qe": "Q/E - 垂直推力",
        "space": "SPACE - 扫描", "beam": "C - 离子束",
        "collect": "Y - 收集碎片", "process": "P - 处理",
        "send": "F - 发送", "refuel": "G - 加注",
        "reset": "R - 重置目标", "containers_toggle": "1/2 - 容器",
        "upgrades": "U - 升级", "pause": "ESC - 暂停",
        "mode_robot": "模式：机器人 [TAB]", "mode_beam": "模式：光束 [TAB]",
        "direction": "方向", "upgrade_shop": "升级商店",
        "your_score": "您的分数", "purchased": "已购买",
        "buy_hint": "按 1, 2, 3 购买或 ESC 退出",
        "pause_menu": "暂停", "continue": "继续",
        "save_game": "保存游戏", "reset_game": "重置游戏",
        "exit_menu": "退出到菜单", "settings_title": "设置",
        "language": "语言", "search_language": "搜索语言...",
        "day": "白天", "night": "夜晚", "mission": "任务",
        "mission_complete": "任务完成！", "mission_progress": "进度",
        "level": "等级", "level_progress": "等级进度",
        "all_missions_complete": "所有任务已完成！",
        "time_system": "1天 = 1小时，1小时 = 2.5分钟",
        "info_title": "游戏规则",
        "rules": [
            "🌍 任务：清理银河系的太空垃圾！",
            "",
            "🚀 运动（零重力）：",
            "  • WASD - 施加推力",
            "  • Q/E - 垂直推力",
            "  • 飞船靠惯性移动",
            "  • 要停止，向相反方向施加推力",
            "  • 速度显示在机器人状态中",
            "",
            "⏱ 时间：1游戏日（24小时）= 1现实小时",
            "  • 太阳在6:00升起，18:00落下",
            "",
            "🤖 EcoBot控制：",
            "  • TAB - 切换模式", "  • WASD - 推力 / 光束",
            "  • Q/E - 垂直推力", "  • SPACE - 扫描",
            "  • C - 离子束（小碎片）", "  • Y - 收集大碎片",
            "  • P - 处理", "  • F - 发送到地球",
            "  • G - 加注氙气", "  • R - 重置目标",
            "  • 1/2 - 切换容器", "  • U - 升级商店",
            "  • ESC - 暂停/菜单"
        ]
    },
    "ja": {
        "name": "日本語", "native": "日本語", "menu_title": "EcoBot 56",
        "subtitle": "銀河の掃除屋", "play": "プレイ", "settings": "設定",
        "info": "情報", "exit": "終了", "back": "戻る", "save": "保存",
        "close": "閉じる", "create": "作成", "cancel": "キャンセル",
        "role_select": "役割選択", "single": "シングルプレイ",
        "navigator": "航海士", "engineer": "エンジニア",
        "operator": "通信士", "captain": "船長",
        "save_select": "セーブ選択", "new_save": "+ 新規セーブ",
        "no_saves": "セーブがありません。新しく作成してください！",
        "new_save_title": "新規セーブ作成", "enter_name": "名前を入力：",
        "containers": "ゴミコンテナ", "metal": "金属", "plastic": "プラスチック",
        "glass": "ガラス", "radioactive": "放射性", "composite": "複合材",
        "processed": "処理済み", "no_resources": "リソースがありません",
        "sent_to_earth": "地球に送信", "total_score": "合計スコア",
        "energy": "エネルギー", "cargo": "貨物", "range": "範囲", "xenon": "キセノン",
        "controls": "コントロール：", "tab": "TAB - モード切替",
        "wasd": "WASD - 推力 / ビーム", "qe": "Q/E - 垂直推力",
        "space": "SPACE - スキャン", "beam": "C - イオンビーム",
        "collect": "Y - 収集", "process": "P - 処理",
        "send": "F - 送信", "refuel": "G - 補給",
        "reset": "R - リセット", "containers_toggle": "1/2 - コンテナ",
        "upgrades": "U - アップグレード", "pause": "ESC - 一時停止",
        "mode_robot": "モード：ロボット [TAB]", "mode_beam": "モード：ビーム [TAB]",
        "direction": "方向", "upgrade_shop": "アップグレードショップ",
        "your_score": "あなたのスコア", "purchased": "購入済み",
        "buy_hint": "1, 2, 3 を押して購入、または ESC で終了",
        "pause_menu": "一時停止", "continue": "続行",
        "save_game": "ゲームを保存", "reset_game": "ゲームをリセット",
        "exit_menu": "メニューに戻る", "settings_title": "設定",
        "language": "言語", "search_language": "言語を検索...",
        "day": "昼", "night": "夜", "mission": "ミッション",
        "mission_complete": "ミッション完了！", "mission_progress": "進捗",
        "level": "レベル", "level_progress": "レベルの進捗",
        "all_missions_complete": "すべてのミッションが完了しました！",
        "time_system": "1日 = 1時間、1時間 = 2.5分",
        "info_title": "ゲームルール",
        "rules": [
            "🌍 ミッション：銀河からスペースデブリを掃除しよう！",
            "",
            "🚀 運動（ゼロ重力）：",
            "  • WASD - 推力をかける",
            "  • Q/E - 垂直推力",
            "  • 船は慣性で移動する",
            "  • 止めるには逆方向に推力をかける",
            "  • 速度はロボットステータスに表示",
            "",
            "⏱ 時間：1ゲーム日（24時間）= 1現実時間",
            "  • 太陽は6:00に昇り、18:00に沈む",
            "",
            "🤖 EcoBot操作：",
            "  • TAB - モード切替", "  • WASD - 推力 / ビーム",
            "  • Q/E - 垂直推力", "  • SPACE - スキャン",
            "  • C - イオンビーム（小さい debris）",
            "  • Y - 大きい debris を収集", "  • P - 処理",
            "  • F - 地球に送信", "  • G - キセノン補給",
            "  • R - 目標リセット", "  • 1/2 - コンテナ切替",
            "  • U - アップグレードショップ", "  • ESC - 一時停止/メニュー"
        ]
    }
}

LANGUAGE_LIST = [
    {"code": "ru", "name": "Русский"},
    {"code": "en", "name": "English"},
    {"code": "zh", "name": "中文"},
    {"code": "ja", "name": "日本語"},
]


def get_text(key):
    global current_lang
    return LANGUAGES.get(current_lang, LANGUAGES["ru"]).get(key, key)


def get_font(size):
    try:
        return pygame.font.SysFont('Arial', size)
    except:
        return pygame.font.Font(None, size)


# ---------------------- КЛАССЫ ДЛЯ МЕНЮ И ИНТЕРФЕЙСА ----------------------

class GameState(Enum):
    MENU = 1
    INFO = 2
    PLAYING = 3
    PAUSED = 4
    ROLE_SELECT = 5
    SAVE_SELECT = 6
    NEW_SAVE = 7
    SETTINGS = 8


class Button:
    def __init__(self, x, y, width, height, text_key, color, hover_color, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_key = text_key
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = get_font(font_size)
        self.animation_offset = 0
        self.animation_direction = 1

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        if is_hover:
            self.current_color = self.hover_color
            self.animation_offset += 0.01
            if self.animation_offset > 1:
                self.animation_direction = -1
            elif self.animation_offset < -1:
                self.animation_direction = 1
            self.animation_offset += self.animation_direction * 0.005
        else:
            self.current_color = self.color
            self.animation_offset = 0

        glow_size = int(5 + abs(self.animation_offset) * 3)
        pygame.draw.rect(screen, (*self.current_color, 100),
                         (self.rect.x - glow_size, self.rect.y - glow_size,
                          self.rect.width + glow_size * 2, self.rect.height + glow_size * 2), 3)
        pygame.draw.rect(screen, self.current_color, self.rect, 0, 10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, 10)
        text = get_text(self.text_key)
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        return is_hover

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 100
        self.size = random.uniform(2, 5)
        self.color = random.choice([(80, 180, 255), (100, 200, 255), (150, 150, 255)])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 2
        self.size = max(0, self.size - 0.1)

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))


class TextInput:
    def __init__(self, x, y, width, height, placeholder_key="enter_name"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder_key = placeholder_key
        self.active = False
        self.font = get_font(24)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 50 and event.unicode.isprintable():
                    self.text += event.unicode
        return False

    def draw(self, screen):
        color = (100, 200, 255) if self.active else (60, 60, 80)
        pygame.draw.rect(screen, color, self.rect, 0, 5)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, 5)
        if self.text:
            text_surf = self.font.render(self.text, True, (255, 255, 255))
        else:
            placeholder = get_text(self.placeholder_key)
            text_surf = self.font.render(placeholder, True, (150, 150, 150))
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))
        if self.active:
            pygame.draw.line(screen, (255, 255, 255),
                             (self.rect.x + 5 + text_surf.get_width(), self.rect.y + 5),
                             (self.rect.x + 5 + text_surf.get_width(), self.rect.y + self.rect.height - 5), 2)


class SettingsManager:
    def __init__(self):
        self.groq_api_key = ""
        self.openrouter_api_key = ""
        self.litellm_api_key = ""
        self.use_ollama = False
        self.ollama_model = "llama3"
        self.litellm_url = "http://localhost:4000"
        self.fullscreen = False
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.language = "ru"
        self.load()

    def load(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.groq_api_key = data.get("groq_api_key", "")
                    self.openrouter_api_key = data.get("openrouter_api_key", "")
                    self.litellm_api_key = data.get("litellm_api_key", "")
                    self.use_ollama = data.get("use_ollama", False)
                    self.ollama_model = data.get("ollama_model", "llama3")
                    self.litellm_url = data.get("litellm_url", "http://localhost:4000")
                    self.fullscreen = data.get("fullscreen", False)
                    self.music_volume = data.get("music_volume", 0.7)
                    self.sfx_volume = data.get("sfx_volume", 0.8)
                    self.language = data.get("language", "ru")
            except:
                pass

    def save(self):
        data = {
            "groq_api_key": self.groq_api_key,
            "openrouter_api_key": self.openrouter_api_key,
            "litellm_api_key": self.litellm_api_key,
            "use_ollama": self.use_ollama,
            "ollama_model": self.ollama_model,
            "litellm_url": self.litellm_url,
            "fullscreen": self.fullscreen,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "language": self.language
        }
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False


# ---------------------- ИГРОВЫЕ КЛАССЫ ----------------------

class Material:
    METAL = None
    PLASTIC = None
    GLASS = None
    RADIOACTIVE = None
    COMPOSITE = None

    def __init__(self, name, display_name_key, color, value=1):
        self.name = name
        self.display_name_key = display_name_key
        self.color = color
        self.value = value

Material.METAL = Material("metal", "metal", (180, 180, 200), 1)
Material.PLASTIC = Material("plastic", "plastic", (200, 200, 150), 1)
Material.GLASS = Material("glass", "glass", (150, 200, 220), 1)
Material.RADIOACTIVE = Material("radioactive", "radioactive", (0, 255, 0), 3)
Material.COMPOSITE = Material("composite", "composite", (200, 150, 200), 2)


class Container:
    def __init__(self, material, capacity=100):
        self.material = material
        self.capacity = capacity
        self.current = 0.0
        self.is_active = True

    def get_fill_percentage(self):
        if self.capacity == 0:
            return 0
        return self.current / self.capacity

    def add(self, amount):
        if not self.is_active:
            return 0
        added = min(amount, self.capacity - self.current)
        self.current += added
        return added

    def clear(self):
        amount = self.current
        self.current = 0
        return amount


class Debris:
    def __init__(self, x, y, z, debris_type="normal"):
        self.x = x
        self.y = y
        self.z = z
        self.debris_type = debris_type
        self.collected = False
        self.size = random.uniform(5, 15)
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-2, 2)
        self.orbit_phase = random.uniform(0, 2 * math.pi)
        self.orbital_decay = 0.0
        self.ion_beam_time = 0
        self.burned_for_score = False

        if debris_type == "rare":
            self.material = random.choice([Material.METAL, Material.PLASTIC, Material.GLASS])
            self.amount = random.uniform(5, 15) * 2
            self.color = (255, 215, 0)
            self.label = "[RARE]"
        elif debris_type == "toxic":
            self.material = Material.RADIOACTIVE
            self.amount = random.uniform(10, 20) * 3
            self.color = (0, 255, 0)
            self.label = "[TOXIC]"
        else:
            self.material = random.choice([Material.METAL, Material.PLASTIC, Material.GLASS])
            self.amount = random.uniform(2, 10)
            self.color = (200, 200, 200)
            self.label = ""

    def update(self):
        self.rotation += self.rot_speed
        self.orbit_phase += 0.01
        self.x += math.sin(self.orbit_phase) * 0.05
        self.y += math.cos(self.orbit_phase * 0.7) * 0.05
        if self.ion_beam_time > 0:
            self.z -= 0.03
            self.ion_beam_time -= 1
            if self.z < 0:
                self.z = 0
                self.collected = True
        self.z += math.sin(self.orbit_phase * 0.3) * 0.02

    def project_3d(self, cam_x, cam_y, cam_z):
        dx = self.x - cam_x
        dy = self.y - cam_y
        dz = self.z - cam_z
        if dz <= 0:
            return (0, 0, 0, False)
        factor = 300 / (dz + 300)
        screen_x = SCREEN_WIDTH // 2 + dx * factor
        screen_y = SCREEN_HEIGHT // 2 + dy * factor
        return (screen_x, screen_y, dz, True)

    def draw(self, screen, cam_x, cam_y, cam_z):
        sx, sy, dz, visible = self.project_3d(cam_x, cam_y, cam_z)
        if not visible:
            return
        size = max(3, int(15 * 300 / (dz + 300)))
        pygame.draw.circle(screen, self.color, (int(sx), int(sy)), size)
        pygame.draw.circle(screen, (255, 255, 255), (int(sx), int(sy)), size, 1)
        if self.label:
            font = get_font(16)
            label_surf = font.render(self.label, True, (255, 255, 255))
            screen.blit(label_surf, (int(sx) - 20, int(sy) - 20))
        if self.ion_beam_time > 0:
            pygame.draw.circle(screen, (0, 255, 255), (int(sx), int(sy)), size + 5, 2)


class EarthStation:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.beam_active = False
        self.beam_target = None
        self.radius = 30

    def draw(self, screen, cam_x, cam_y, cam_z):
        dx = self.x - cam_x
        dy = self.y - cam_y
        dz = self.z - cam_z
        if dz <= 0:
            return
        factor = 300 / (dz + 300)
        screen_x = SCREEN_WIDTH // 2 + dx * factor
        screen_y = SCREEN_HEIGHT // 2 + dy * factor
        size = max(10, int(self.radius * 300 / (dz + 300)))
        pygame.draw.circle(screen, (100, 200, 100), (int(screen_x), int(screen_y)), size)
        pygame.draw.circle(screen, (200, 255, 200), (int(screen_x), int(screen_y)), size - 3)
        pygame.draw.line(screen, (200, 200, 200),
                         (int(screen_x), int(screen_y) - size),
                         (int(screen_x), int(screen_y) - size - 20), 3)
        if self.beam_active and self.beam_target:
            tdx = self.beam_target.x - cam_x
            tdy = self.beam_target.y - cam_y
            tdz = self.beam_target.z - cam_z
            if tdz > 0:
                tfactor = 300 / (tdz + 300)
                target_sx = SCREEN_WIDTH // 2 + tdx * tfactor
                target_sy = SCREEN_HEIGHT // 2 + tdy * tfactor
                draw_dashed_line(screen, (int(screen_x), int(screen_y)),
                                 (int(target_sx), int(target_sy)),
                                 (0, 255, 0), 3, 8)

    def can_send_resources(self, robot):
        dist = math.hypot(robot.x - self.x, robot.y - self.y, robot.z - self.z)
        return dist < 150


class FuelStation:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.radius = 25
        self.active = False

    def draw(self, screen, cam_x, cam_y, cam_z):
        if not self.active:
            return
        dx = self.x - cam_x
        dy = self.y - cam_y
        dz = self.z - cam_z
        if dz <= 0:
            return
        factor = 300 / (dz + 300)
        screen_x = SCREEN_WIDTH // 2 + dx * factor
        screen_y = SCREEN_HEIGHT // 2 + dy * factor
        size = max(8, int(self.radius * 300 / (dz + 300)))
        pygame.draw.circle(screen, (255, 200, 50), (int(screen_x), int(screen_y)), size)
        pygame.draw.circle(screen, (255, 255, 200), (int(screen_x), int(screen_y)), size - 3)
        font = get_font(16)
        label = font.render("FUEL", True, (255, 255, 255))
        screen.blit(label, (int(screen_x) - 20, int(screen_y) - 20))

    def can_refuel(self, robot):
        if not self.active:
            return False
        dist = math.hypot(robot.x - self.x, robot.y - self.y, robot.z - self.z)
        return dist < 120


def draw_dashed_line(screen, start_pos, end_pos, color, width, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    steps = int(dist / dash_length) + 1
    for i in range(0, steps, 2):
        t1 = i / steps
        t2 = min(1, (i + 1) / steps)
        p1x = int(x1 + dx * t1)
        p1y = int(y1 + dy * t1)
        p2x = int(x1 + dx * t2)
        p2y = int(y1 + dy * t2)
        pygame.draw.line(screen, color, (p1x, p1y), (p2x, p2y), width)


class Upgrade:
    def __init__(self, name, cost, description):
        self.name = name
        self.cost = cost
        self.description = description
        self.purchased = False


class EcoBot:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
        # Новая система движения (инерционная)
        self.vx = 0.0  # скорость по X
        self.vy = 0.0  # скорость по Y
        self.vz = 0.0  # скорость по Z
        self.thrust_power = 0.15  # сила тяги
        self.friction = 0.9995  # очень маленькое трение (почти нулевое)
        self.max_speed = 8.0
        
        self.energy = 100.0
        self.current_cargo = 0.0
        self.cargo_capacity = 50.0
        self.collection_range = 50.0
        self.target_debris = None
        self.scanning = False
        self.processing = False
        self.xenon_fuel = 100.0
        self.max_xenon = 100.0
        self.ion_thrust = 0.0005
        self.beam_active = False
        self.beam_target = None
        self.processed_resources = {
            "metal": 0.0, "plastic": 0.0, "glass": 0.0,
            "radioactive": 0.0, "composite": 0.0
        }
        self.sent_to_earth = {
            "metal": 0.0, "plastic": 0.0, "glass": 0.0,
            "radioactive": 0.0, "composite": 0.0, "total_score": 0.0
        }
        self.reward_messages = []
        self.containers = {
            Material.METAL: Container(Material.METAL, 100),
            Material.PLASTIC: Container(Material.PLASTIC, 100),
            Material.GLASS: Container(Material.GLASS, 100),
            Material.RADIOACTIVE: Container(Material.RADIOACTIVE, 80),
            Material.COMPOSITE: Container(Material.COMPOSITE, 120)
        }
        self.upgrades = [
            Upgrade("Увеличение дальности", 50, "Дальность сбора +20"),
            Upgrade("Увеличение груза", 80, "Грузоподъёмность +30"),
            Upgrade("Усовершенствование буксира", 200, "Увеличение тяги ионного пучка")
        ]
        self.control_mode = 0
        self.beam_direction_x = 0
        self.beam_direction_y = 0
        self.beam_direction_z = 0
        self.beam_power = 0.5
        
        # Для отображения вектора скорости
        self.thrust_particles = []

    def add_reward_message(self, text, color):
        self.reward_messages.append({"text": text, "color": color})
        if len(self.reward_messages) > 20:
            self.reward_messages.pop(0)

    def toggle_control_mode(self):
        self.control_mode = (self.control_mode + 1) % 2
        if self.control_mode == 0:
            self.add_reward_message(get_text("mode_robot"), (100, 255, 100))
        else:
            self.add_reward_message(get_text("mode_beam"), (0, 200, 255))
            self.beam_direction_x = 0
            self.beam_direction_y = 0
            self.beam_direction_z = 0

    def apply_thrust(self, dx, dy, dz):
        """Применение тяги в направлении (инерционная система)"""
        self.vx += dx * self.thrust_power
        self.vy += dy * self.thrust_power
        self.vz += dz * self.thrust_power
        
        # Ограничение максимальной скорости
        speed = math.hypot(self.vx, self.vy, self.vz)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.vx *= scale
            self.vy *= scale
            self.vz *= scale
        
        # Расход энергии от тяги
        thrust_magnitude = abs(dx) + abs(dy) + abs(dz)
        if thrust_magnitude > 0:
            self.energy = max(0, self.energy - 0.05 * thrust_magnitude)

    def move(self):
        """Обновление позиции на основе скорости (инерция)"""
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        
        # Очень маленькое трение (почти нулевое)
        self.vx *= self.friction
        self.vy *= self.friction
        self.vz *= self.friction
        
        # Границы
        self.x = max(-600, min(600, self.x))
        self.y = max(-600, min(600, self.y))
        self.z = max(50, min(700, self.z))
        
        # Если на границе - гасим скорость
        if self.x <= -600 or self.x >= 600:
            self.vx *= 0.9
        if self.y <= -600 or self.y >= 600:
            self.vy *= 0.9
        if self.z <= 50 or self.z >= 700:
            self.vz *= 0.9
        
        # Расход энергии на движение
        speed = math.hypot(self.vx, self.vy, self.vz)
        if speed > 0.1:
            self.energy = max(0, self.energy - 0.002 * speed)

    def get_speed(self):
        return math.hypot(self.vx, self.vy, self.vz)

    def update(self):
        if self.energy < 100:
            self.energy = min(100, self.energy + 0.015)
        if self.target_debris and self.target_debris.collected:
            self.target_debris = None
            self.beam_active = False
        if self.beam_active and self.beam_target and not self.beam_target.collected:
            if self.beam_target.amount < 5:
                if self.xenon_fuel > 0 and self.energy > 5:
                    self.xenon_fuel -= 0.02
                    self.energy -= 0.0167
                    self.beam_target.ion_beam_time = 8
                    if self.xenon_fuel <= 0:
                        self.beam_active = False
                        self.add_reward_message("Ксенон закончился! Дозаправьтесь.", (255, 100, 100))
                else:
                    self.beam_active = False
            else:
                self.add_reward_message("Крупный мусор! Нажмите Y для сбора.", (255, 200, 100))
                self.beam_active = False
        if self.beam_target and self.beam_target.collected:
            if self.beam_target.amount < 5 and not self.beam_target.burned_for_score:
                self.beam_target.burned_for_score = True
                self.sent_to_earth["total_score"] += 5
                self.add_reward_message("Мелкий мусор сгорел! +5 баллов", (255, 255, 0))
            self.beam_active = False
            self.beam_target = None
        
        # Генерация частиц тяги для визуализации
        speed = self.get_speed()
        if speed > 0.3:
            if len(self.thrust_particles) < 20:
                self.thrust_particles.append({
                    "x": self.x - self.vx * 2,
                    "y": self.y - self.vy * 2,
                    "z": self.z - self.vz * 2,
                    "life": 30,
                    "size": random.uniform(2, 5)
                })
        
        # Обновление частиц
        for p in self.thrust_particles[:]:
            p["life"] -= 1
            p["x"] += random.uniform(-0.2, 0.2)
            p["y"] += random.uniform(-0.2, 0.2)
            p["z"] += random.uniform(-0.2, 0.2)
            if p["life"] <= 0:
                self.thrust_particles.remove(p)

    def scan_debris(self, debris_list):
        if self.energy < 5:
            return
        closest = None
        min_dist = float('inf')
        for debris in debris_list:
            if debris.collected:
                continue
            dist = math.hypot(self.x - debris.x, self.y - debris.y, self.z - debris.z)
            if dist < self.collection_range and dist < min_dist:
                min_dist = dist
                closest = debris
        if closest:
            self.target_debris = closest
            display_name = get_text(closest.material.display_name_key)
            self.add_reward_message(f"Найден {display_name} ({closest.amount:.1f})", (200, 200, 255))
            self.energy -= 0.8

    def start_ion_beam(self):
        if not self.target_debris or self.target_debris.collected:
            self.add_reward_message("Нет цели для облучения.", (255, 200, 100))
            return False
        if self.target_debris.amount >= 5:
            self.add_reward_message("Крупный мусор! Нажмите Y для сбора.", (255, 200, 100))
            return False
        if self.xenon_fuel <= 0:
            self.add_reward_message("Нет ксенона! Дозаправьтесь на станции.", (255, 100, 100))
            return False
        if self.energy < 10:
            self.add_reward_message("Недостаточно энергии для ионного пучка.", (255, 100, 100))
            return False
        self.beam_active = True
        self.beam_target = self.target_debris
        self.add_reward_message("Ионный пучок направлен на мелкий мусор", (0, 255, 255))
        return True

    def stop_ion_beam(self):
        self.beam_active = False
        self.beam_target = None
        self.add_reward_message("Ионный пучок отключён.", (200, 200, 200))

    def collect_large_debris(self):
        if not self.target_debris or self.target_debris.collected:
            self.add_reward_message("Нет цели для сбора.", (255, 200, 100))
            return False
        if self.target_debris.amount < 5:
            self.add_reward_message("Это мелкий мусор! Используйте ионный пучок (C).", (255, 200, 100))
            return False
        if self.energy < 10:
            self.add_reward_message("Недостаточно энергии!", (255, 100, 100))
            return False
        dist = math.hypot(self.x - self.target_debris.x, self.y - self.target_debris.y, self.z - self.target_debris.z)
        if dist > self.collection_range:
            self.add_reward_message("Слишком далеко! Подойдите ближе.", (255, 100, 100))
            return False
        container = self.containers.get(self.target_debris.material)
        if not container or not container.is_active:
            self.add_reward_message("Контейнер для этого материала отключён!", (255, 100, 100))
            return False
        if container.current >= container.capacity:
            self.add_reward_message("Контейнер полон! Переработайте мусор.", (255, 200, 100))
            return False
        added = container.add(self.target_debris.amount)
        if added > 0:
            self.target_debris.collected = True
            self.current_cargo += added
            self.energy -= 3
            display_name = get_text(self.target_debris.material.display_name_key)
            self.add_reward_message(f"Собран крупный мусор: {added:.1f} {display_name}", (100, 255, 100))
            self.target_debris = None
            return True
        return False

    def process_materials(self):
        if self.energy < 15:
            self.add_reward_message("Недостаточно энергии для переработки!", (255, 100, 100))
            return 0
        total_processed = 0
        for mat, container in self.containers.items():
            if container.is_active and container.current > 0:
                amount = container.clear()
                res_name = mat.name
                self.processed_resources[res_name] += amount
                total_processed += amount
                self.energy -= 1.2
        if total_processed > 0:
            self.add_reward_message(f"Переработано {total_processed:.1f} единиц", (100, 255, 255))
        else:
            self.add_reward_message("Нет мусора для переработки", (200, 200, 200))
        return total_processed

    def send_to_earth(self):
        total_sent = 0
        rewards = {}
        for res_name, amount in self.processed_resources.items():
            if amount > 0:
                self.sent_to_earth[res_name] += amount
                total_sent += amount
                rewards[res_name] = amount
                self.processed_resources[res_name] = 0
                if res_name == "radioactive":
                    score_mult = 3
                elif res_name == "composite":
                    score_mult = 2
                else:
                    score_mult = 1
                self.sent_to_earth["total_score"] += amount * score_mult
        if total_sent > 0:
            self.add_reward_message(f"Отправлено {total_sent:.1f} ресурсов на Землю!", (255, 255, 100))
        return total_sent, rewards

    def refuel_xenon(self, fuel_station):
        if not fuel_station.active:
            self.add_reward_message("Заправочная станция ещё не активна.", (255, 200, 100))
            return False
        if not fuel_station.can_refuel(self):
            self.add_reward_message("Подойдите ближе к заправочной станции (G)", (255, 200, 100))
            return False
        refill_amount = self.max_xenon - self.xenon_fuel
        if refill_amount > 0:
            self.xenon_fuel = self.max_xenon
            self.add_reward_message(f"Дозаправка ксеноном выполнена (+{refill_amount:.1f} кг)", (100, 255, 100))
            return True
        else:
            self.add_reward_message("Бак полон", (200, 200, 200))
            return False

    def draw(self, screen, cam_x, cam_y, cam_z):
        dx = self.x - cam_x
        dy = self.y - cam_y
        dz = self.z - cam_z
        if dz <= 0:
            return
        factor = 300 / (dz + 300)
        screen_x = SCREEN_WIDTH // 2 + dx * factor
        screen_y = SCREEN_HEIGHT // 2 + dy * factor
        size = max(8, int(20 * 300 / (dz + 300)))
        
        # Частицы тяги
        for p in self.thrust_particles:
            pdx = p["x"] - cam_x
            pdy = p["y"] - cam_y
            pdz = p["z"] - cam_z
            if pdz > 0:
                pf = 300 / (pdz + 300)
                psx = SCREEN_WIDTH // 2 + pdx * pf
                psy = SCREEN_HEIGHT // 2 + pdy * pf
                alpha = int(255 * (p["life"] / 30))
                pygame.draw.circle(screen, (255, 200, 100, alpha), (int(psx), int(psy)), int(p["size"]))
        
        # Корабль
        pygame.draw.circle(screen, (100, 200, 255), (int(screen_x), int(screen_y)), size)
        pygame.draw.circle(screen, (200, 240, 255), (int(screen_x), int(screen_y)), size - 2)
        
        # Вектор скорости (линия направления движения)
        speed = self.get_speed()
        if speed > 0.5:
            # Нормализованный вектор скорости
            norm = speed
            vx_n = self.vx / norm
            vy_n = self.vy / norm
            vz_n = self.vz / norm
            # Проекция на экран
            end_x = screen_x + vx_n * 50
            end_y = screen_y + vy_n * 50
            # Рисуем линию направления
            pygame.draw.line(screen, (255, 255, 100), (int(screen_x), int(screen_y)), (int(end_x), int(end_y)), 2)
            # Стрелка
            angle = math.atan2(vy_n, vx_n)
            arrow_len = 10
            for a in [-0.4, 0.4]:
                ax = end_x - arrow_len * math.cos(angle + a)
                ay = end_y - arrow_len * math.sin(angle + a)
                pygame.draw.line(screen, (255, 255, 100), (int(end_x), int(end_y)), (int(ax), int(ay)), 2)
        
        if self.beam_active and self.beam_target and not self.beam_target.collected:
            tdx = self.beam_target.x - cam_x
            tdy = self.beam_target.y - cam_y
            tdz = self.beam_target.z - cam_z
            if tdz > 0:
                tfactor = 300 / (tdz + 300)
                t_sx = SCREEN_WIDTH // 2 + tdx * tfactor
                t_sy = SCREEN_HEIGHT // 2 + tdy * tfactor
                draw_dashed_line(screen, (int(screen_x), int(screen_y)),
                                 (int(t_sx), int(t_sy)), (0, 200, 255), 2, 6)
        if self.target_debris and not self.target_debris.collected:
            tdx = self.target_debris.x - cam_x
            tdy = self.target_debris.y - cam_y
            tdz = self.target_debris.z - cam_z
            if tdz > 0:
                tfactor = 300 / (tdz + 300)
                t_sx = SCREEN_WIDTH // 2 + tdx * tfactor
                t_sy = SCREEN_HEIGHT // 2 + tdy * tfactor
                pygame.draw.line(screen, (0, 255, 0), (int(screen_x), int(screen_y)),
                                 (int(t_sx), int(t_sy)), 2)
                if self.target_debris.amount >= 5:
                    font = get_font(16)
                    hint = font.render("[Y]", True, (255, 255, 0))
                    screen.blit(hint, (int(t_sx) + 10, int(t_sy) - 10))
        if self.scanning:
            pygame.draw.circle(screen, (0, 255, 0), (int(screen_x), int(screen_y)), size + 10, 2)
        if self.processing:
            pygame.draw.circle(screen, (255, 255, 0), (int(screen_x), int(screen_y)), size + 15, 3)
        
        # Индикаторы энергии и топлива
        energy_width = size * 2
        energy_height = 4
        energy_x = screen_x - energy_width // 2
        energy_y = screen_y + size + 5
        pygame.draw.rect(screen, (80, 80, 80), (energy_x, energy_y, energy_width, energy_height))
        if self.energy > 0:
            fill = int(energy_width * (self.energy / 100))
            pygame.draw.rect(screen, (100, 255, 100), (energy_x, energy_y, fill, energy_height))
        fuel_width = size * 2
        fuel_height = 3
        fuel_x = screen_x - fuel_width // 2
        fuel_y = screen_y + size + 12
        pygame.draw.rect(screen, (80, 80, 80), (fuel_x, fuel_y, fuel_width, fuel_height))
        if self.xenon_fuel > 0:
            fill = int(fuel_width * (self.xenon_fuel / self.max_xenon))
            pygame.draw.rect(screen, (200, 200, 255), (fuel_x, fuel_y, fill, fuel_height))


# ---------------------- ИГРОВОЙ ИНТЕРФЕЙС (GameUI) ----------------------

class GameUI:
    def __init__(self):
        self.font = get_font(24)
        self.title_font = get_font(36)
        self.small_font = get_font(18)
        self.show_upgrades = False
        self.show_pause_menu = False
        self.lang_search_text = ""
        self.lang_search_active = False
        self.lang_scroll_offset = 0

    def draw_pause_menu(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        menu_width = 400
        menu_height = 420
        menu_x = SCREEN_WIDTH // 2 - menu_width // 2
        menu_y = SCREEN_HEIGHT // 2 - menu_height // 2
        pygame.draw.rect(screen, (40, 40, 60), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(screen, (100, 100, 150), (menu_x, menu_y, menu_width, menu_height), 3)
        title = self.title_font.render(get_text("pause_menu"), True, (255, 255, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, menu_y + 40))
        screen.blit(title, title_rect)
        button_width = 250
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        continue_btn = Button(button_x, menu_y + 100, button_width, button_height,
                              "continue", (50, 150, 50), (100, 255, 100), 28)
        save_btn = Button(button_x, menu_y + 165, button_width, button_height,
                          "save_game", (50, 100, 150), (100, 150, 255), 28)
        reset_btn = Button(button_x, menu_y + 230, button_width, button_height,
                           "reset_game", (150, 100, 50), (255, 150, 100), 28)
        menu_btn = Button(button_x, menu_y + 295, button_width, button_height,
                          "exit_menu", (150, 50, 50), (255, 100, 100), 28)
        continue_btn.draw(screen)
        save_btn.draw(screen)
        reset_btn.draw(screen)
        menu_btn.draw(screen)
        return continue_btn, save_btn, reset_btn, menu_btn

    def draw_container_status(self, screen, containers, x, y):
        pygame.draw.rect(screen, (40, 40, 60), (x, y, 250, 230))
        pygame.draw.rect(screen, (80, 80, 100), (x, y, 250, 230), 2)
        title = self.font.render(get_text("containers"), True, (220, 220, 255))
        screen.blit(title, (x + 10, y + 10))
        y_offset = 40
        for material, container in containers.items():
            fill_percent = container.get_fill_percentage()
            color = material.color
            pygame.draw.rect(screen, (60, 60, 80), (x + 10, y + y_offset, 180, 20))
            if fill_percent > 0:
                pygame.draw.rect(screen, color, (x + 10, y + y_offset, fill_percent * 1.8, 20))
            display_name = get_text(material.display_name_key)
            text = f"{display_name}: {container.current:.1f}/{container.capacity}"
            render = self.small_font.render(text, True, (240, 240, 255))
            screen.blit(render, (x + 15, y + y_offset + 2))
            if container.is_active:
                pygame.draw.circle(screen, (0, 255, 0), (x + 210, y + y_offset + 10), 5)
            else:
                pygame.draw.circle(screen, (255, 0, 0), (x + 210, y + y_offset + 10), 5)
            y_offset += 25

    def draw_processed_resources(self, screen, resources, x, y):
        pygame.draw.rect(screen, (40, 80, 40), (x, y, 200, 150))
        pygame.draw.rect(screen, (80, 120, 80), (x, y, 200, 150), 2)
        title = self.font.render(get_text("processed"), True, (220, 255, 220))
        screen.blit(title, (x + 10, y + 10))
        y_offset = 40
        total = 0
        for resource, amount in resources.items():
            if amount > 0:
                display_name = get_text(resource)
                text = f"{display_name}: {amount:.1f}"
                render = self.small_font.render(text, True, (200, 255, 200))
                screen.blit(render, (x + 15, y + y_offset))
                y_offset += 20
                total += amount
        if total == 0:
            text = get_text("no_resources")
            render = self.small_font.render(text, True, (200, 200, 200))
            screen.blit(render, (x + 15, y + 40))

    def draw_earth_stats(self, screen, sent_stats, x, y):
        pygame.draw.rect(screen, (60, 40, 80), (x, y, 250, 200))
        pygame.draw.rect(screen, (100, 80, 120), (x, y, 250, 200), 2)
        title = self.font.render(get_text("sent_to_earth"), True, (220, 200, 255))
        screen.blit(title, (x + 10, y + 10))
        y_offset = 40
        for resource, amount in sent_stats.items():
            if resource != "total_score" and amount > 0:
                display_name = get_text(resource)
                text = f"{display_name}: {amount:.1f}"
                render = self.small_font.render(text, True, (200, 200, 255))
                screen.blit(render, (x + 15, y + y_offset))
                y_offset += 20
        score_text = f"{get_text('total_score')}: {int(sent_stats['total_score'])}"
        score_render = self.font.render(score_text, True, (255, 255, 100))
        screen.blit(score_render, (x + 15, y + 160))

    def draw_robot_status(self, screen, robot, x, y):
        pygame.draw.rect(screen, (60, 40, 40), (x, y, 250, 140))
        pygame.draw.rect(screen, (100, 80, 80), (x, y, 250, 140), 2)
        pygame.draw.rect(screen, (80, 80, 80), (x + 10, y + 30, 180, 20))
        if robot.energy > 0:
            pygame.draw.rect(screen, (100, 200, 255), (x + 10, y + 30, robot.energy * 1.8, 20))
        if robot.cargo_capacity > 0:
            cargo_percent = (robot.current_cargo / robot.cargo_capacity) * 100
        else:
            cargo_percent = 0
        pygame.draw.rect(screen, (80, 80, 80), (x + 10, y + 60, 180, 20))
        if cargo_percent > 0:
            pygame.draw.rect(screen, (255, 200, 100), (x + 10, y + 60, cargo_percent * 1.8, 20))
        
        speed = robot.get_speed()
        text_energy = self.small_font.render(f"{get_text('energy')}: {robot.energy:.1f}%", True, (255, 255, 255))
        text_cargo = self.small_font.render(f"{get_text('cargo')}: {robot.current_cargo:.1f}/{robot.cargo_capacity}", True, (255, 255, 255))
        text_range = self.small_font.render(f"{get_text('range')}: {robot.collection_range}", True, (0, 255, 255))
        text_fuel = self.small_font.render(f"{get_text('xenon')}: {robot.xenon_fuel:.1f} кг", True, (200, 200, 255))
        text_speed = self.small_font.render(f"Скорость: {speed:.2f}", True, (255, 255, 100))
        
        screen.blit(text_energy, (x + 15, y + 32))
        screen.blit(text_cargo, (x + 15, y + 62))
        screen.blit(text_range, (x + 15, y + 92))
        screen.blit(text_fuel, (x + 130, y + 32))
        screen.blit(text_speed, (x + 15, y + 115))

    def draw_controls(self, screen, x, y):
        controls = [
            ("controls", (255, 255, 200)), ("tab", (255, 215, 0)),
            ("wasd", (0, 200, 255)), ("qe", (0, 200, 255)),
            ("space", (200, 200, 180)), ("beam", (0, 255, 255)),
            ("collect", (255, 255, 0)), ("process", (100, 255, 255)),
            ("send", (100, 255, 255)), ("refuel", (255, 255, 100)),
            ("reset", (200, 200, 180)), ("containers_toggle", (200, 200, 180)),
            ("upgrades", (255, 215, 0)), ("pause", (255, 215, 0))
        ]
        pygame.draw.rect(screen, (40, 40, 40), (x, y, 270, 360))
        pygame.draw.rect(screen, (100, 100, 100), (x, y, 270, 360), 2)
        for i, (key, color) in enumerate(controls):
            text = get_text(key)
            render = self.small_font.render(text, True, color)
            screen.blit(render, (x + 10, y + 10 + i * 24))

    def draw_control_mode(self, screen, robot, x, y):
        if robot.control_mode == 0:
            text = get_text("mode_robot")
            color = (100, 255, 100)
        else:
            text = get_text("mode_beam")
            color = (0, 200, 255)
        render = self.small_font.render(text, True, color)
        screen.blit(render, (x, y))
        if robot.control_mode == 1:
            dir_text = f"{get_text('direction')}: X{robot.beam_direction_x:+.1f} Y{robot.beam_direction_y:+.1f} Z{robot.beam_direction_z:+.1f}"
            dir_render = self.small_font.render(dir_text, True, (200, 200, 255))
            screen.blit(dir_render, (x, y + 22))

    def draw_upgrades_menu(self, screen, robot, x, y):
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        screen.blit(s, (0, 0))
        menu_width = 400
        menu_height = 350
        menu_x = SCREEN_WIDTH // 2 - menu_width // 2
        menu_y = SCREEN_HEIGHT // 2 - menu_height // 2
        pygame.draw.rect(screen, (40, 40, 60), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(screen, (100, 100, 150), (menu_x, menu_y, menu_width, menu_height), 3)
        title = self.font.render(get_text("upgrade_shop"), True, (255, 215, 0))
        screen.blit(title, (menu_x + menu_width // 2 - title.get_width() // 2, menu_y + 10))
        score_text = self.small_font.render(f"{get_text('your_score')}: {int(robot.sent_to_earth['total_score'])}", True, (255, 255, 100))
        screen.blit(score_text, (menu_x + 20, menu_y + 40))
        y_offset = 70
        for i, upgrade in enumerate(robot.upgrades):
            color = (150, 255, 150) if robot.sent_to_earth['total_score'] >= upgrade.cost else (255, 150, 150)
            if upgrade.purchased:
                color = (100, 100, 100)
            button_rect = pygame.Rect(menu_x + 20, menu_y + y_offset, 360, 40)
            pygame.draw.rect(screen, color, button_rect)
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)
            name_text = self.small_font.render(f"{i + 1}. {upgrade.name}", True, (255, 255, 255))
            cost_text = self.small_font.render(f"Цена: {upgrade.cost}", True, (255, 255, 255))
            desc_text = self.small_font.render(upgrade.description, True, (200, 200, 200))
            screen.blit(name_text, (menu_x + 25, menu_y + y_offset + 5))
            screen.blit(cost_text, (menu_x + 300, menu_y + y_offset + 5))
            screen.blit(desc_text, (menu_x + 25, menu_y + y_offset + 20))
            if upgrade.purchased:
                purchased_text = self.small_font.render(get_text("purchased"), True, (0, 255, 0))
                screen.blit(purchased_text, (menu_x + 200, menu_y + y_offset + 5))
            y_offset += 50
        instruction = self.small_font.render(get_text("buy_hint"), True, (200, 200, 200))
        screen.blit(instruction, (menu_x + menu_width // 2 - instruction.get_width() // 2, menu_y + menu_height - 25))

    def draw_reward_messages(self, screen, messages):
        y_offset = SCREEN_HEIGHT // 2 - 100
        for msg in messages[-5:]:
            text = self.font.render(msg["text"], True, msg["color"])
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 30

    def draw_timer(self, screen, game_time_seconds):
        total_game_seconds = int(game_time_seconds)
        days = total_game_seconds // 86400
        remaining = total_game_seconds % 86400
        hours = remaining // 3600
        remaining = remaining % 3600
        minutes = remaining // 60
        seconds = remaining % 60
        
        time_str = f"{get_text('day')} {days + 1}  {hours:02d}:{minutes:02d}:{seconds:02d}"
        timer_font = get_font(26)
        timer_surf = timer_font.render(time_str, True, (255, 255, 200))
        timer_rect = timer_surf.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        pygame.draw.rect(screen, (0, 0, 0, 180), (timer_rect.x - 10, timer_rect.y - 5, timer_rect.width + 20, timer_rect.height + 10))
        pygame.draw.rect(screen, (100, 100, 150), (timer_rect.x - 10, timer_rect.y - 5, timer_rect.width + 20, timer_rect.height + 10), 2)
        screen.blit(timer_surf, timer_rect)
        
        if 6 <= hours < 18:
            day_text = f"☀️ {get_text('day')}"
            day_color = (255, 255, 100)
        else:
            day_text = f"🌙 {get_text('night')}"
            day_color = (200, 200, 255)
        day_font = get_font(20)
        day_surf = day_font.render(day_text, True, day_color)
        day_rect = day_surf.get_rect(topright=(SCREEN_WIDTH - 20, 55))
        screen.blit(day_surf, day_rect)
        
        time_info = get_text("time_system")
        info_font = get_font(14)
        info_surf = info_font.render(time_info, True, (200, 200, 200))
        info_rect = info_surf.get_rect(topright=(SCREEN_WIDTH - 20, 75))
        screen.blit(info_surf, info_rect)


# ---------------------- ГЛАВНОЕ МЕНЮ (SplashScreen) ----------------------

class SplashScreen:
    def __init__(self, screen):
        self.screen = screen
        self.state = GameState.MENU
        self.clock = pygame.time.Clock()
        self.particles = []
        self.logo_scale = 1.0
        self.logo_scale_direction = 0.0005
        self.logo = self.load_spaceship_logo()
        self.settings = SettingsManager()
        self.selected_save = None
        self.selected_role = None
        self.lang_search_text = ""
        self.lang_search_active = False
        self.lang_scroll_offset = 0
        
        button_width = 220
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = SCREEN_HEIGHT // 2 + 50
        self.buttons = {
            "start": Button(button_x, start_y, button_width, button_height, "play", (50, 150, 50), (100, 255, 100), 28),
            "settings": Button(button_x, start_y + 60, button_width, button_height, "settings", (100, 100, 50), (200, 200, 100), 28),
            "info": Button(button_x, start_y + 120, button_width, button_height, "info", (50, 50, 150), (100, 100, 255), 28),
            "exit": Button(button_x, start_y + 180, button_width, button_height, "exit", (150, 50, 50), (255, 100, 100), 28)
        }
        self.info_scroll_offset = 0
        self.info_scroll_speed = 20
        self.info_max_offset = 0
        self.load_music()
        self.time = 0

    def load_spaceship_logo(self):
        logo_surface = pygame.Surface((500, 250), pygame.SRCALPHA)
        center_x = 250
        center_y = 125
        ship_points = [
            (center_x, center_y - 60), (center_x + 50, center_y + 20),
            (center_x + 30, center_y + 40), (center_x, center_y + 30),
            (center_x - 30, center_y + 40), (center_x - 50, center_y + 20)
        ]
        pygame.draw.polygon(logo_surface, (100, 150, 255), ship_points)
        pygame.draw.polygon(logo_surface, (150, 200, 255), ship_points, 3)
        pygame.draw.circle(logo_surface, (80, 180, 255), (center_x, center_y - 20), 20)
        pygame.draw.circle(logo_surface, (100, 200, 255), (center_x, center_y - 20), 15)
        pygame.draw.circle(logo_surface, (255, 255, 200), (center_x, center_y - 20), 8)
        pygame.draw.circle(logo_surface, (100, 100, 255), (center_x - 3, center_y - 22), 2)
        pygame.draw.circle(logo_surface, (100, 100, 255), (center_x + 3, center_y - 22), 2)
        pygame.draw.rect(logo_surface, (255, 100, 100), (center_x - 20, center_y + 25, 15, 15))
        pygame.draw.rect(logo_surface, (255, 100, 100), (center_x + 5, center_y + 25, 15, 15))
        flame_points = [
            (center_x - 12, center_y + 40), (center_x - 20, center_y + 60),
            (center_x - 5, center_y + 50), (center_x, center_y + 65),
            (center_x + 5, center_y + 50), (center_x + 20, center_y + 60),
            (center_x + 12, center_y + 40)
        ]
        pygame.draw.polygon(logo_surface, (255, 150, 50), flame_points)
        wing_color = (80, 130, 200)
        pygame.draw.polygon(logo_surface, wing_color, [
            (center_x + 50, center_y + 20), (center_x + 70, center_y + 35),
            (center_x + 55, center_y + 40)
        ])
        pygame.draw.polygon(logo_surface, wing_color, [
            (center_x - 50, center_y + 20), (center_x - 70, center_y + 35),
            (center_x - 55, center_y + 40)
        ])
        font = get_font(52)
        text = font.render("EcoBot 56", True, (255, 255, 100))
        text_rect = text.get_rect(center=(center_x, center_y + 90))
        logo_surface.blit(text, text_rect)
        small_font = get_font(28)
        subtitle = small_font.render(get_text("subtitle"), True, (200, 200, 255))
        subtitle_rect = subtitle.get_rect(center=(center_x, center_y + 130))
        logo_surface.blit(subtitle, subtitle_rect)
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(70, 120)
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius - 30
            pygame.draw.circle(logo_surface, (255, 255, 200), (int(x), int(y)), 2)
        return logo_surface

    def load_music(self):
        try:
            sample_rate = 22050
            duration = 5.0
            frequency = 440
            samples = int(sample_rate * duration)
            wave = [int(32767 * math.sin(2 * math.pi * frequency * t / sample_rate) *
                        math.exp(-t / duration)) for t in range(samples)]
            sound_bytes = bytes()
            for sample in wave:
                sound_bytes += sample.to_bytes(2, 'little', signed=True)
            sound = pygame.mixer.Sound(buffer=sound_bytes)
            sound.set_volume(self.settings.music_volume)
            sound.play(loops=-1, fade_ms=1000)
        except:
            pass

    def add_particles(self):
        if len(self.particles) < 50:
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            self.particles.append(Particle(x, y))

    def update_particles(self):
        self.add_particles()
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0 or particle.size <= 0:
                self.particles.remove(particle)

    def draw_background(self):
        self.screen.fill(BACKGROUND_COLOR)
        time = pygame.time.get_ticks() * 0.001
        for i in range(200):
            x = (i * 173) % SCREEN_WIDTH
            y = (i * 97) % SCREEN_HEIGHT
            brightness = int(150 + 100 * math.sin(time + i))
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (int(x), int(y)), 1)
        planet_x = SCREEN_WIDTH - 150
        planet_y = 100
        planet_radius = 80
        pygame.draw.circle(self.screen, (80, 100, 150), (planet_x, planet_y), planet_radius)
        pygame.draw.circle(self.screen, (100, 120, 170), (planet_x, planet_y), planet_radius - 5)
        for offset in range(2):
            pygame.draw.ellipse(self.screen, (120, 140, 190),
                                (planet_x - planet_radius - 20, planet_y - 20 + offset * 40,
                                 planet_radius * 2 + 40, 30), 2)
        for particle in self.particles:
            particle.draw(self.screen)

    def draw_logo(self):
        self.logo_scale += self.logo_scale_direction
        if self.logo_scale > 1.02:
            self.logo_scale = 1.02
            self.logo_scale_direction = -0.0005
        elif self.logo_scale < 0.98:
            self.logo_scale = 0.98
            self.logo_scale_direction = 0.0005
        scaled_logo = pygame.transform.smoothscale(self.logo,
            (int(self.logo.get_width() * self.logo_scale),
             int(self.logo.get_height() * self.logo_scale)))
        logo_x = SCREEN_WIDTH // 2 - scaled_logo.get_width() // 2
        logo_y = 50
        glow_surface = pygame.Surface((scaled_logo.get_width() + 20, scaled_logo.get_height() + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*self.buttons["start"].current_color, 50),
                         (10, 10, scaled_logo.get_width(), scaled_logo.get_height()), 20)
        self.screen.blit(glow_surface, (logo_x - 10, logo_y - 10))
        self.screen.blit(scaled_logo, (logo_x, logo_y))

    def draw_info_screen(self):
        self.draw_background()
        self.draw_logo()
        info_rect = pygame.Rect(100, 200, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 280)
        overlay = pygame.Surface((info_rect.width, info_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, info_rect)
        pygame.draw.rect(self.screen, (100, 100, 255), info_rect, 3)
        title_font = get_font(48)
        title = title_font.render(get_text("info_title"), True, (255, 255, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 240))
        self.screen.blit(title, title_rect)

        rules = get_text("rules")
        font = get_font(22)
        line_height = 28
        total_height = len(rules) * line_height
        if total_height > info_rect.height - 40:
            self.info_max_offset = total_height - (info_rect.height - 40)
        else:
            self.info_max_offset = 0
        self.info_scroll_offset = max(0, min(self.info_scroll_offset, self.info_max_offset))

        y_offset = 270 - self.info_scroll_offset
        for rule in rules:
            if rule == "":
                y_offset += 15
                continue
            color = (220, 220, 255) if rule.startswith(("🌍", "🚀", "⏱", "🤖")) else (200, 200, 200)
            text = font.render(rule, True, color)
            if 220 < y_offset < 220 + info_rect.height - 20:
                self.screen.blit(text, (150, y_offset))
            y_offset += line_height

        back_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 80, 300, 50,
                             "back", (80, 80, 80), (150, 150, 150), 28)
        back_button.draw(self.screen)
        return back_button

    def draw_menu(self):
        self.draw_background()
        self.draw_logo()
        for button in self.buttons.values():
            button.draw(self.screen)

    def draw_language_selector(self, screen, x, y):
        global current_lang
        title = self.font.render(get_text("language") + ":", True, (255, 255, 200))
        screen.blit(title, (x, y))
        y += 30
        
        search_rect = pygame.Rect(x, y, 300, 30)
        color = (100, 200, 255) if self.lang_search_active else (60, 60, 80)
        pygame.draw.rect(screen, color, search_rect, 0, 5)
        pygame.draw.rect(screen, (255, 255, 255), search_rect, 2, 5)
        
        if self.lang_search_active:
            search_text = self.lang_search_text + "|"
            text_color = (255, 255, 255)
        elif self.lang_search_text:
            search_text = self.lang_search_text
            text_color = (255, 255, 255)
        else:
            search_text = get_text("search_language")
            text_color = (150, 150, 150)
        search_surf = self.small_font.render(search_text, True, text_color)
        screen.blit(search_surf, (search_rect.x + 5, search_rect.y + 5))
        y += 40
        
        list_height = 280
        list_rect = pygame.Rect(x, y, 300, list_height)
        pygame.draw.rect(screen, (40, 40, 60), list_rect)
        pygame.draw.rect(screen, (80, 80, 100), list_rect, 2)
        
        search_lower = self.lang_search_text.lower()
        filtered_langs = []
        for lang in LANGUAGE_LIST:
            if search_lower in lang["name"].lower() or search_lower in lang["code"].lower():
                filtered_langs.append(lang)
        
        item_height = 25
        visible_items = list_height // item_height
        if len(filtered_langs) > visible_items:
            if self.lang_scroll_offset > len(filtered_langs) - visible_items:
                self.lang_scroll_offset = max(0, len(filtered_langs) - visible_items)
        
        for i in range(visible_items):
            idx = i + self.lang_scroll_offset
            if idx >= len(filtered_langs):
                break
            lang = filtered_langs[idx]
            item_rect = pygame.Rect(x + 5, y + i * item_height + 5, 290, item_height - 2)
            if lang["code"] == current_lang:
                pygame.draw.rect(screen, (80, 80, 150), item_rect)
            elif item_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (60, 60, 100), item_rect)
            lang_text = f"{lang['name']} ({lang['code']})"
            text_surf = self.small_font.render(lang_text, True, (255, 255, 255))
            screen.blit(text_surf, (item_rect.x + 5, item_rect.y + 2))
            if lang["code"] == current_lang:
                check = self.small_font.render("✓", True, (0, 255, 0))
                screen.blit(check, (item_rect.x + item_rect.width - 20, item_rect.y + 2))
        
        if len(filtered_langs) > visible_items:
            scroll_text = self.small_font.render("↓ прокрутка", True, (200, 200, 200))
            screen.blit(scroll_text, (x + 10, y + list_height - 20))
        
        return search_rect, list_rect, filtered_langs

    def draw_settings_menu(self, active_field):
        self.draw_background()
        self.draw_logo()
        info_rect = pygame.Rect(100, 180, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 240)
        overlay = pygame.Surface((info_rect.width, info_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, info_rect)
        pygame.draw.rect(self.screen, (100, 100, 150), info_rect, 3)
        title_font = get_font(36)
        title = title_font.render(get_text("settings_title"), True, (255, 255, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 210))
        self.screen.blit(title, title_rect)
        
        search_rect, list_rect, filtered_langs = self.draw_language_selector(self.screen, 450, 260)
        
        btn_save = Button(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT - 60, 150, 40,
                          "save", (50, 150, 50), (100, 255, 100), 24)
        btn_close = Button(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT - 60, 150, 40,
                          "close", (150, 50, 50), (255, 100, 100), 24)
        btn_save.draw(self.screen)
        btn_close.draw(self.screen)
        return btn_save, btn_close, search_rect, list_rect, filtered_langs

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if self.buttons["start"].is_clicked(event):
                self.state = GameState.ROLE_SELECT
                return True
            elif self.buttons["settings"].is_clicked(event):
                self.state = GameState.SETTINGS
                return True
            elif self.buttons["info"].is_clicked(event):
                self.state = GameState.INFO
                return True
            elif self.buttons["exit"].is_clicked(event):
                return False
        return True

    def handle_info_events(self, back_button):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.info_scroll_offset -= self.info_scroll_speed
                elif event.button == 5:
                    self.info_scroll_offset += self.info_scroll_speed
            if back_button.is_clicked(event):
                self.state = GameState.MENU
                return True
        return True

    def handle_settings_events(self, active_field):
        global current_lang
        btn_save, btn_close, search_rect, list_rect, filtered_langs = self.draw_settings_menu(active_field)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, active_field
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                    return None, active_field
                elif event.key == pygame.K_BACKSPACE:
                    if self.lang_search_active:
                        self.lang_search_text = self.lang_search_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.lang_search_active:
                        self.lang_search_active = False
                else:
                    if self.lang_search_active and event.unicode.isprintable():
                        self.lang_search_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_save.is_clicked(event):
                    self.settings.save()
                    return "saved", active_field
                elif btn_close.is_clicked(event):
                    self.state = GameState.MENU
                    return None, active_field
                elif search_rect.collidepoint(event.pos):
                    self.lang_search_active = True
                elif list_rect.collidepoint(event.pos):
                    item_height = 25
                    y_offset = event.pos[1] - list_rect.y - 5
                    idx = y_offset // item_height + self.lang_scroll_offset
                    if idx < len(filtered_langs):
                        selected_lang = filtered_langs[idx]["code"]
                        if selected_lang in LANGUAGES:
                            current_lang = selected_lang
                            self.settings.language = selected_lang
                            self.settings.save()
                else:
                    self.lang_search_active = False
                if event.button == 4:
                    self.lang_scroll_offset = max(0, self.lang_scroll_offset - 1)
                elif event.button == 5:
                    max_offset = max(0, len(filtered_langs) - (list_rect.height // 25))
                    self.lang_scroll_offset = min(max_offset, self.lang_scroll_offset + 1)
        return None, active_field

    def draw_role_selection(self):
        self.draw_background()
        self.draw_logo()
        info_rect = pygame.Rect(100, 220, SCREEN_WIDTH - 200, 300)
        overlay = pygame.Surface((info_rect.width, info_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, info_rect)
        pygame.draw.rect(self.screen, (100, 100, 255), info_rect, 3)
        title_font = get_font(36)
        title = title_font.render(get_text("role_select"), True, (255, 255, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 260))
        self.screen.blit(title, title_rect)

        roles = [("single", "single"), ("navigator", "navigator"), ("engineer", "engineer"), ("operator", "operator"), ("captain", "captain")]
        role_btns = []
        y = 310
        for name_key, role_id in roles:
            btn = Button(SCREEN_WIDTH // 2 - 150, y, 300, 40, name_key, (60, 60, 80), (100, 100, 150), 22)
            role_btns.append((btn, role_id))
            btn.draw(self.screen)
            y += 45
        back_btn = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 40, "back", (80, 80, 80), (150, 150, 150), 24)
        back_btn.draw(self.screen)
        return back_btn, role_btns

    def handle_role_selection(self):
        back_btn, role_btns = self.draw_role_selection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                    return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.is_clicked(event):
                    self.state = GameState.MENU
                    return None
                for btn, role_id in role_btns:
                    if btn.is_clicked(event):
                        self.selected_role = role_id
                        self.state = GameState.SAVE_SELECT
                        return None
        return None

    def get_save_files(self):
        saves = []
        if os.path.exists(SAVES_DIR):
            for f in os.listdir(SAVES_DIR):
                if f.endswith('.json') and f != "settings.json":
                    saves.append(f)
        return saves

    def get_save_info(self, save_name):
        path = os.path.join(SAVES_DIR, save_name)
        if not os.path.exists(path):
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {
                    "name": save_name.replace('.json', ''),
                    "timestamp": data.get("timestamp", "Неизвестно"),
                    "level": data.get("level", 1),
                    "score": data.get("robot", {}).get("sent_to_earth", {}).get("total_score", 0)
                }
        except:
            return None

    def delete_save(self, save_name):
        path = os.path.join(SAVES_DIR, save_name)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def draw_save_selection(self):
        self.draw_background()
        self.draw_logo()
        info_rect = pygame.Rect(100, 220, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 300)
        overlay = pygame.Surface((info_rect.width, info_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, info_rect)
        pygame.draw.rect(self.screen, (100, 100, 255), info_rect, 3)
        title_font = get_font(36)
        title = title_font.render(get_text("save_select"), True, (255, 255, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 260))
        self.screen.blit(title, title_rect)

        saves = self.get_save_files()
        y = 310
        new_btn = Button(SCREEN_WIDTH // 2 - 100, y, 200, 40, "new_save", (50, 150, 50), (100, 255, 100), 24)
        new_btn.draw(self.screen)
        y += 55

        save_btns = []
        for save_file in saves:
            info = self.get_save_info(save_file)
            if info:
                text = f"{info['name']} (Ур.{info['level']}, {int(info['score'])} очков)"
                btn = Button(SCREEN_WIDTH // 2 - 200, y, 400, 35, text, (60, 60, 80), (100, 100, 150), 18)
                del_btn = Button(SCREEN_WIDTH // 2 + 210, y, 30, 35, "X", (150, 50, 50), (255, 100, 100), 18)
                save_btns.append((btn, del_btn, save_file))
                btn.draw(self.screen)
                del_btn.draw(self.screen)
                y += 40

        if not saves:
            no_saves = get_font(24).render(get_text("no_saves"), True, (255, 200, 200))
            self.screen.blit(no_saves, (SCREEN_WIDTH // 2 - 150, y))

        back_btn = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 40, "back", (80, 80, 80), (150, 150, 150), 24)
        back_btn.draw(self.screen)
        return new_btn, back_btn, save_btns

    def handle_save_selection(self):
        new_btn, back_btn, save_btns = self.draw_save_selection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.ROLE_SELECT
                    return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.is_clicked(event):
                    self.state = GameState.ROLE_SELECT
                    return None
                if new_btn.is_clicked(event):
                    self.state = GameState.NEW_SAVE
                    return None
                for btn, del_btn, save_file in save_btns:
                    if btn.is_clicked(event):
                        return save_file
                    if del_btn.is_clicked(event):
                        self.delete_save(save_file)
                        return "refresh"
        return "none"

    def draw_new_save(self, text_input):
        self.draw_background()
        self.draw_logo()
        info_rect = pygame.Rect(100, 250, SCREEN_WIDTH - 200, 280)
        overlay = pygame.Surface((info_rect.width, info_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, info_rect)
        pygame.draw.rect(self.screen, (100, 100, 255), info_rect, 3)
        title_font = get_font(36)
        title = title_font.render(get_text("new_save_title"), True, (255, 255, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 290))
        self.screen.blit(title, title_rect)
        label = get_font(24).render(get_text("enter_name"), True, (220, 220, 255))
        self.screen.blit(label, (SCREEN_WIDTH // 2 - 150, 340))
        text_input.draw(self.screen)
        btn_y = 420
        create_btn = Button(SCREEN_WIDTH // 2 - 120, btn_y, 200, 40, "create", (50, 150, 50), (100, 255, 100), 24)
        cancel_btn = Button(SCREEN_WIDTH // 2 + 30, btn_y, 150, 40, "cancel", (150, 50, 50), (255, 100, 100), 24)
        create_btn.draw(self.screen)
        cancel_btn.draw(self.screen)
        return create_btn, cancel_btn

    def handle_new_save(self, text_input):
        create_btn, cancel_btn = self.draw_new_save(text_input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.SAVE_SELECT
                    return None
                text_input.handle_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if create_btn.is_clicked(event):
                    if text_input.text.strip():
                        save_name = text_input.text.strip() + ".json"
                        if save_name in self.get_save_files():
                            return "exists"
                        return save_name
                    else:
                        return "empty"
                if cancel_btn.is_clicked(event):
                    self.state = GameState.SAVE_SELECT
                    return None
                text_input.handle_event(event)
        return "none"

    def run(self):
        running = True
        text_input = TextInput(SCREEN_WIDTH // 2 - 150, 375, 300, 35)
        active_field = None
        while running and (self.selected_save is None or self.selected_role is None):
            self.update_particles()
            if self.state == GameState.MENU:
                running = self.handle_menu_events()
                self.draw_menu()
            elif self.state == GameState.INFO:
                back_button = self.draw_info_screen()
                running = self.handle_info_events(back_button)
            elif self.state == GameState.SETTINGS:
                result, active_field = self.handle_settings_events(active_field)
                if result == "saved":
                    self.draw_settings_menu(active_field)
                    success = get_font(20).render(get_text("save"), True, (100, 255, 100))
                    self.screen.blit(success, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 110))
                    pygame.display.flip()
                    pygame.time.wait(1000)
            elif self.state == GameState.ROLE_SELECT:
                result = self.handle_role_selection()
                if result is not None:
                    return None
            elif self.state == GameState.SAVE_SELECT:
                result = self.handle_save_selection()
                if result == "refresh":
                    continue
                elif result == "none":
                    pass
                elif result is not None:
                    self.selected_save = result
                    running = False
            elif self.state == GameState.NEW_SAVE:
                result = self.handle_new_save(text_input)
                if result == "exists":
                    self.draw_new_save(text_input)
                    error = get_font(20).render("Сохранение с таким именем уже существует!", True, (255, 100, 100))
                    self.screen.blit(error, (SCREEN_WIDTH // 2 - 180, 470))
                    pygame.display.flip()
                    pygame.time.wait(1500)
                elif result == "empty":
                    self.draw_new_save(text_input)
                    error = get_font(20).render("Введите название сохранения!", True, (255, 100, 100))
                    self.screen.blit(error, (SCREEN_WIDTH // 2 - 140, 470))
                    pygame.display.flip()
                    pygame.time.wait(1500)
                elif result is not None and result != "none":
                    self.selected_save = result
                    running = False
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.mixer.music.stop()
        return self.selected_role, self.selected_save


# ---------------------- ОСНОВНОЙ КЛАСС ИГРЫ (Game) ----------------------

class Game:
    GRAVITY_CONST = 6.674e-11
    EARTH_MASS = 5.972e24
    EARTH_RADIUS = 6371000

    def __init__(self, role=None, save_name=None):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("EcoBot 56 - Нулевая гравитация")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState.PLAYING
        self.role = role if role else "single"
        self.save_name = save_name
        self.settings = SettingsManager()
        self.init_game()
        if save_name:
            self.load_save_file(save_name)

    def init_game(self):
        self.camera_x = 0
        self.camera_y = 0
        self.camera_z = -300
        self.robot = EcoBot(0, 0, 200)
        self.earth_station = EarthStation(300, 300, 150)
        self.fuel_station = FuelStation(-200, -200, 180)
        self.space_size = 300
        self.new_debris_types = False
        self.debris_list = []
        self.generate_debris(20)
        self.ui = GameUI()
        self.collected_count = 0
        self.processed_count = 0
        self.score = 0
        self.mission_target = 50
        self.mission_progress = 0
        self.stars = [(random.randint(0, SCREEN_WIDTH),
                       random.randint(0, SCREEN_HEIGHT),
                       random.uniform(0.5, 1.5)) for _ in range(200)]
        self.game_time_seconds = 0.0
        self.last_time = pygame.time.get_ticks()
        self.time = 0
        self.event_timer = 0
        self.event_active = None
        self.event_data = {}
        self.level = 1
        self.level_mission_target = 10
        self.level_mission_progress = 0
        self.fuel_station_unlocked = False

    def load_save_file(self, save_name):
        path = os.path.join(SAVES_DIR, save_name)
        if not os.path.exists(path):
            return False
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.game_time_seconds = data.get("game_time_seconds", 0.0)
            self.level = data.get("level", 1)
            self.fuel_station_unlocked = data.get("fuel_station_unlocked", False)
            if self.fuel_station_unlocked:
                self.fuel_station.active = True
            robot_data = data.get("robot", {})
            self.robot.x = robot_data.get("x", 0)
            self.robot.y = robot_data.get("y", 0)
            self.robot.z = robot_data.get("z", 200)
            self.robot.vx = robot_data.get("vx", 0.0)
            self.robot.vy = robot_data.get("vy", 0.0)
            self.robot.vz = robot_data.get("vz", 0.0)
            self.robot.energy = robot_data.get("energy", 100.0)
            self.robot.current_cargo = robot_data.get("current_cargo", 0.0)
            self.robot.collection_range = robot_data.get("collection_range", 50.0)
            self.robot.xenon_fuel = robot_data.get("xenon_fuel", 100.0)
            self.robot.processed_resources = robot_data.get("processed_resources", {
                "metal": 0.0, "plastic": 0.0, "glass": 0.0, "radioactive": 0.0, "composite": 0.0
            })
            self.robot.sent_to_earth = robot_data.get("sent_to_earth", {
                "metal": 0.0, "plastic": 0.0, "glass": 0.0, "radioactive": 0.0, "composite": 0.0, "total_score": 0.0
            })
            for i, purchased in enumerate(robot_data.get("upgrades_purchased", [])):
                if i < len(self.robot.upgrades):
                    self.robot.upgrades[i].purchased = purchased
            game_data = data.get("game", {})
            self.space_size = game_data.get("space_size", 300)
            self.new_debris_types = game_data.get("new_debris_types", False)
            self.collected_count = game_data.get("collected_count", 0)
            self.processed_count = game_data.get("processed_count", 0)
            self.mission_progress = game_data.get("mission_progress", 0)
            self.mission_target = game_data.get("mission_target", 50)
            self.level_mission_progress = game_data.get("level_mission_progress", 0)
            self.level_mission_target = game_data.get("level_mission_target", 10)
            self.debris_list = []
            self.generate_debris(20)
            self.robot.add_reward_message("✅ Сохранение загружено!", (100, 255, 100))
            return True
        except Exception as e:
            self.robot.add_reward_message(f"❌ Ошибка загрузки: {e}", (255, 100, 100))
            return False

    def save_game(self):
        if not self.save_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.save_name = f"autosave_{timestamp}.json"
        save_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "game_time_seconds": self.game_time_seconds,
            "level": self.level,
            "fuel_station_unlocked": self.fuel_station_unlocked,
            "robot": {
                "x": self.robot.x, "y": self.robot.y, "z": self.robot.z,
                "vx": self.robot.vx, "vy": self.robot.vy, "vz": self.robot.vz,
                "energy": self.robot.energy, "current_cargo": self.robot.current_cargo,
                "collection_range": self.robot.collection_range, "xenon_fuel": self.robot.xenon_fuel,
                "processed_resources": self.robot.processed_resources,
                "sent_to_earth": self.robot.sent_to_earth,
                "upgrades_purchased": [u.purchased for u in self.robot.upgrades],
                "control_mode": self.robot.control_mode
            },
            "game": {
                "space_size": self.space_size, "new_debris_types": self.new_debris_types,
                "collected_count": self.collected_count, "processed_count": self.processed_count,
                "mission_progress": self.mission_progress, "mission_target": self.mission_target,
                "level_mission_progress": self.level_mission_progress,
                "level_mission_target": self.level_mission_target
            }
        }
        try:
            path = os.path.join(SAVES_DIR, self.save_name)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            self.robot.add_reward_message("💾 Игра сохранена!", (100, 255, 100))
            return True
        except Exception as e:
            self.robot.add_reward_message(f"❌ Ошибка сохранения: {e}", (255, 100, 100))
            return False

    def generate_debris(self, count):
        for _ in range(count):
            if self.new_debris_types:
                rand = random.random()
                if rand < 0.6:
                    debris_type = "normal"
                elif rand < 0.85:
                    debris_type = "rare"
                else:
                    debris_type = "toxic"
            else:
                debris_type = "normal"
            x = random.uniform(-self.space_size, self.space_size)
            y = random.uniform(-self.space_size, self.space_size)
            z = random.uniform(100, 400)
            self.debris_list.append(Debris(x, y, z, debris_type))

    def apply_gravity(self, obj):
        # Нулевая гравитация - ничего не делаем
        pass

    def get_time_of_day(self):
        game_hours = (self.game_time_seconds / 3600) % 24
        return game_hours

    def get_sky_color(self, hour):
        if hour < 5 or hour >= 21:
            return (5, 5, 20)
        elif 5 <= hour < 7:
            t = (hour - 5) / 2.0
            return (int(5 + 100 * t), int(5 + 80 * t), int(20 + 150 * t))
        elif 7 <= hour < 17:
            return (135, 206, 235)
        elif 17 <= hour < 19:
            t = (hour - 17) / 2.0
            return (int(135 - 100 * t), int(206 - 80 * t), int(235 - 150 * t))
        else:
            return (10, 10, 30)

    def draw_sun_moon(self, hour):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2 + 50
        radius = 250
        if 6 <= hour <= 18:
            angle = math.radians((hour - 6) / 12.0 * 180 - 90)
            sun_x = center_x + radius * math.cos(angle)
            sun_y = center_y - radius * math.sin(angle)
            for i in range(20, 0, -5):
                glow_color = (255, 255, 200, int(50 * (1 - i / 20)))
                pygame.draw.circle(self.screen, glow_color, (int(sun_x), int(sun_y)), 50 + i, 2)
            pygame.draw.circle(self.screen, (255, 255, 100), (int(sun_x), int(sun_y)), 40)
            pygame.draw.circle(self.screen, (255, 255, 200), (int(sun_x), int(sun_y)), 35)
            for i in range(12):
                angle_ray = math.radians(i * 30 + hour * 15)
                x1 = sun_x + 38 * math.cos(angle_ray)
                y1 = sun_y - 38 * math.sin(angle_ray)
                x2 = sun_x + 50 * math.cos(angle_ray)
                y2 = sun_y - 50 * math.sin(angle_ray)
                pygame.draw.line(self.screen, (255, 255, 150), (int(x1), int(y1)), (int(x2), int(y2)), 2)
        else:
            if hour >= 18:
                angle = math.radians((hour - 18) / 12.0 * 180 - 90)
            else:
                angle = math.radians((hour + 6) / 12.0 * 180 - 90)
            moon_x = center_x + radius * math.cos(angle)
            moon_y = center_y - radius * math.sin(angle)
            for i in range(15, 0, -5):
                glow_color = (200, 200, 255, int(30 * (1 - i / 15)))
                pygame.draw.circle(self.screen, glow_color, (int(moon_x), int(moon_y)), 35 + i, 2)
            pygame.draw.circle(self.screen, (220, 220, 255), (int(moon_x), int(moon_y)), 30)
            pygame.draw.circle(self.screen, (240, 240, 255), (int(moon_x), int(moon_y)), 25)
            craters = [(10, -8, 5), (-12, 5, 4), (5, 12, 3), (-5, -15, 3)]
            for cx, cy, cr in craters:
                pygame.draw.circle(self.screen, (180, 180, 200), (int(moon_x + cx), int(moon_y + cy)), cr)

    def generate_event(self):
        events = ["solar_storm", "debris_cloud", "gyro_failure", "sleeping_satellite"]
        choice = random.choice(events)
        if choice == "solar_storm":
            self.robot.add_reward_message("[SOLAR] СОЛНЕЧНЫЙ ШТОРМ!", (255, 200, 0))
            self.event_active = "solar_storm"
            self.event_data = {"duration": 15 * 60}
        elif choice == "debris_cloud":
            self.robot.add_reward_message("[DEBRIS] ОБЛАКО МУСОРА!", (255, 100, 0))
            self.event_active = "debris_cloud"
            for _ in range(30):
                x = random.uniform(-self.space_size, self.space_size)
                y = random.uniform(-self.space_size, self.space_size)
                z = random.uniform(100, 400)
                self.debris_list.append(Debris(x, y, z, "normal"))
            self.event_data = {"duration": 5 * 60}
        elif choice == "gyro_failure":
            self.robot.add_reward_message("[GYRO] ОТКАЗ ГИРОСКОПА!", (255, 100, 100))
            self.event_active = "gyro_failure"
            self.event_data = {"duration": 10 * 60}
        elif choice == "sleeping_satellite":
            self.robot.add_reward_message("[SLEEP] СПУТНИК ОЖИЛ!", (0, 200, 255))
            self.event_active = "sleeping_satellite"
            self.event_data = {"duration": 20 * 60}

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.ui.show_upgrades:
                        self.ui.show_upgrades = False
                    else:
                        self.ui.show_pause_menu = not self.ui.show_pause_menu
                elif not self.ui.show_pause_menu:
                    if event.key == pygame.K_TAB:
                        self.robot.toggle_control_mode()
                    elif event.key == pygame.K_SPACE:
                        self.robot.scanning = True
                        self.robot.scan_debris(self.debris_list)
                    elif event.key == pygame.K_c:
                        if self.robot.beam_active:
                            self.robot.stop_ion_beam()
                        else:
                            self.robot.start_ion_beam()
                    elif event.key == pygame.K_y:
                        self.robot.collect_large_debris()
                    elif event.key == pygame.K_p:
                        processed = self.robot.process_materials()
                        if processed > 0:
                            self.processed_count += processed
                            self.robot.processing = True
                    elif event.key == pygame.K_f:
                        if self.earth_station.can_send_resources(self.robot):
                            total_sent, rewards = self.robot.send_to_earth()
                            if total_sent > 0:
                                self.mission_progress += total_sent
                                self.score = self.robot.sent_to_earth["total_score"]
                                self.earth_station.beam_active = True
                                self.earth_station.beam_target = self.robot
                        else:
                            self.robot.add_reward_message("Подойдите ближе к станции!", (255, 100, 100))
                    elif event.key == pygame.K_g:
                        self.robot.refuel_xenon(self.fuel_station)
                    elif event.key == pygame.K_r:
                        self.robot.target_debris = None
                        self.robot.stop_ion_beam()
                    elif event.key == pygame.K_1:
                        self.robot.containers[Material.METAL].is_active = not self.robot.containers[Material.METAL].is_active
                    elif event.key == pygame.K_2:
                        self.robot.containers[Material.PLASTIC].is_active = not self.robot.containers[Material.PLASTIC].is_active
                    elif event.key == pygame.K_u:
                        self.ui.show_upgrades = not self.ui.show_upgrades
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.robot.scanning = False
                elif event.key == pygame.K_p:
                    self.robot.processing = False
                elif event.key == pygame.K_f:
                    self.earth_station.beam_active = False
                    self.earth_station.beam_target = None

        if self.ui.show_pause_menu:
            return

        keys = pygame.key.get_pressed()
        dx, dy, dz = 0, 0, 0

        if self.robot.control_mode == 0:
            # Режим управления тягой (инерционное движение)
            if keys[pygame.K_w]:
                dy -= 1
            if keys[pygame.K_s]:
                dy += 1
            if keys[pygame.K_a]:
                dx -= 1
            if keys[pygame.K_d]:
                dx += 1
            if keys[pygame.K_q]:
                dz -= 1
            if keys[pygame.K_e]:
                dz += 1
            if dx != 0 or dy != 0 or dz != 0:
                self.robot.apply_thrust(dx, dy, dz)
        else:
            # Режим управления пучком
            if keys[pygame.K_w]:
                self.robot.beam_direction_y -= 1
            if keys[pygame.K_s]:
                self.robot.beam_direction_y += 1
            if keys[pygame.K_a]:
                self.robot.beam_direction_x -= 1
            if keys[pygame.K_d]:
                self.robot.beam_direction_x += 1
            if keys[pygame.K_q]:
                self.robot.beam_direction_z -= 1
            if keys[pygame.K_e]:
                self.robot.beam_direction_z += 1
            max_dir = 50
            self.robot.beam_direction_x = max(-max_dir, min(max_dir, self.robot.beam_direction_x))
            self.robot.beam_direction_y = max(-max_dir, min(max_dir, self.robot.beam_direction_y))
            self.robot.beam_direction_z = max(-max_dir, min(max_dir, self.robot.beam_direction_z))
            if self.robot.target_debris and self.robot.beam_active:
                target = self.robot.target_debris
                target.x += self.robot.beam_direction_x * 0.02
                target.y += self.robot.beam_direction_y * 0.02
                target.z += self.robot.beam_direction_z * 0.02

    def update(self):
        if self.ui.show_pause_menu:
            return

        current_time = pygame.time.get_ticks()
        delta_ms = current_time - self.last_time
        self.last_time = current_time
        delta_sec = delta_ms / 1000.0
        
        GAME_SPEED = 24
        self.game_time_seconds += delta_sec * GAME_SPEED

        self.time += 1
        
        # Движение робота с инерцией
        self.robot.move()
        
        for debris in self.debris_list:
            debris.update()
            if debris.collected:
                if debris.amount < 5 and not debris.burned_for_score:
                    debris.burned_for_score = True
                    self.score += 5
                    self.level_mission_progress += 1
                    self.robot.add_reward_message("+5 баллов за сожжённый мусор!", (255, 255, 0))
                self.debris_list.remove(debris)
                continue

        if self.robot.sent_to_earth["total_score"] >= 50 and not self.new_debris_types:
            self.new_debris_types = True
            self.robot.add_reward_message("🔓 Открыты новые типы мусора!", (255, 215, 0))
        if self.robot.sent_to_earth["total_score"] >= 100 and not self.fuel_station_unlocked:
            self.fuel_station_unlocked = True
            self.fuel_station.active = True
            self.robot.add_reward_message("⛽ Заправочная станция активирована!", (255, 215, 0))

        if len(self.debris_list) < 10:
            self.generate_debris(random.randint(5, 15))

        if self.time % (60 * 30) == 0 and self.time > 0:
            self.generate_event()

        if self.event_active == "solar_storm":
            if self.event_data.get("duration", 0) > 0:
                self.event_data["duration"] -= 1
                self.robot.energy = max(0, self.robot.energy - 0.001)
            else:
                self.event_active = None
                self.robot.add_reward_message("[SOLAR] Шторм закончился!", (100, 255, 100))

        hour = self.get_time_of_day()
        if 6 <= hour < 18:
            self.robot.energy = min(100, self.robot.energy + 0.02)
        else:
            self.robot.energy = min(100, self.robot.energy + 0.005)

        self.robot.update()

    def draw(self):
        hour = self.get_time_of_day()
        sky_color = self.get_sky_color(hour)
        self.screen.fill(sky_color)
        self.draw_sun_moon(hour)

        star_brightness = 1.0 if hour < 6 or hour >= 18 else max(0, 1 - (hour - 6) / 4)
        for star in self.stars:
            brightness = int(star_brightness * (150 + 100 * math.sin(self.time * 0.01 + star[2])))
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (int(star[0]), int(star[1])), 2)

        for debris in self.debris_list:
            debris.draw(self.screen, self.camera_x, self.camera_y, self.camera_z)

        self.earth_station.draw(self.screen, self.camera_x, self.camera_y, self.camera_z)
        self.fuel_station.draw(self.screen, self.camera_x, self.camera_y, self.camera_z)
        self.robot.draw(self.screen, self.camera_x, self.camera_y, self.camera_z)

        # Левая панель
        self.ui.draw_container_status(self.screen, self.robot.containers, 10, 10)
        self.ui.draw_processed_resources(self.screen, self.robot.processed_resources, 270, 10)
        self.ui.draw_earth_stats(self.screen, self.robot.sent_to_earth, 10, 250)
        self.ui.draw_robot_status(self.screen, self.robot, 10, 460)

        # Правая панель
        self.ui.draw_controls(self.screen, SCREEN_WIDTH - 280, 10)
        self.ui.draw_control_mode(self.screen, self.robot, SCREEN_WIDTH - 280, SCREEN_HEIGHT - 60)
        self.ui.draw_reward_messages(self.screen, self.robot.reward_messages)
        self.ui.draw_timer(self.screen, self.game_time_seconds)

        if self.ui.show_upgrades:
            self.ui.draw_upgrades_menu(self.screen, self.robot, 0, 0)
        if self.ui.show_pause_menu:
            self.ui.draw_pause_menu(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


# ---------------------- ТОЧКА ВХОДА ----------------------

def main():
    global current_lang
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EcoBot 56 - Нулевая гравитация")
    
    settings = SettingsManager()
    if settings.language in LANGUAGES:
        current_lang = settings.language
    
    splash = SplashScreen(screen)
    role, save_name = splash.run()
    
    if role is not None and save_name is not None:
        game = Game(role, save_name)
        game.run()
    
    pygame.quit()

if __name__ == "__main__":
    main()