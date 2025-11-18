import pygame, random, os, sys, time, math, psutil
import tkinter as tk
from tkinter import messagebox


def get_memory_info():
    # 获取内存信息
    memory = psutil.virtual_memory()
    
    print("=== 内存信息 ===")
    print(f"总内存: {memory.total / (1024**3):.2f} GB")
    print(f"可用内存: {memory.available / (1024**3):.2f} GB")
    print(f"已用内存: {memory.used / (1024**3):.2f} GB")
    print(f"内存使用率: {memory.percent}%")
    
    return {
        'total': memory.total,
        'available': memory.available,
        'used': memory.used,
        'percent': memory.percent
    }

mem_info = get_memory_info()

if float(f"{mem_info["available"] / (1024**3):.2f}") <= 2:
    messagebox.showerror("方块吃方块",f"唐死我了学校电脑！\n可使用内存不足！\n剩余：{mem_info["available"] / (1024**3):.2f}GB！",icon=['warning'])


PLAYER_SKINS = {
    "0.png": "姚明",
    "1.png": "毛毛",
    "2.png": "熊大",
    "3.png": "请输入文本",
    "4.png": "稻妻亲王殿下",
    "5.png": "苏少羽",
    "6.png": "胃袋这一块",
    "7.png": "点击输入文本",
    "8.png": "熊二"
}
current_player_skin = "default"  # 默认使用绿色方块
current_player2_skin = "default"  # 玩家二默认使用绿色方块
# 性能监控变量
frame_count = 0
frame_times = []
last_frame_time = time.time()
def monitor_performance():
    """监控帧率"""
    global frame_count, frame_times, last_frame_time
    current_time = time.time()
    frame_time = current_time - last_frame_time
    frame_times.append(frame_time)
    last_frame_time = current_time
    
    frame_count += 1
    if frame_count % 60 == 0:  # 每60帧输出一次性能信息
        avg_frame_time = sum(frame_times) / len(frame_times)
        fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
        return fps
        frame_times = []
# 初始化pygame模块
version = "v2.2.3"
pygame.init() 
pygame.mixer.init()
died_range = float('inf')
player2_died_range = float('inf')
player_ai_died_range = float('inf')
def key_customization_menu():
    """键位自定义菜单 - 支持翻页和冲刺键"""
    global current_player1_keys, current_player2_keys
    
    # 创建字体
    title_font = pygame.font.Font(font_path, 60)
    player_font = pygame.font.Font(font_path, 40)
    key_font = pygame.font.Font(font_path, 30)
    button_font = pygame.font.Font(font_path, 35)
    hint_font = pygame.font.Font(font_path, 24)
    page_font = pygame.font.Font(font_path, 25)
    
    # 控制项定义（分页）
    control_pages = [
        # 第一页：移动和攻击
        [
            ("向左移动", 'left'),
            ("向右移动", 'right'), 
            ("向上移动", 'up'),
            ("向下移动", 'down'),
            ("攻击", 'attack')
        ],
        # 第二页：武器和冲刺
        [
            ("装备剑", 'sword'),
            ("装备枪", 'gun'),
            ("冲刺", 'dash')  # 新增冲刺键
        ]
    ]
    
    # 当前页码
    current_page = 0
    control_labels, control_keys = zip(*control_pages[current_page])
    control_labels = list(control_labels)
    control_keys = list(control_keys)
    
    # 按钮文本
    prev_text = button_font.render("上一页", True, WHITE)
    next_text = button_font.render("下一页", True, WHITE)
    reset_text = button_font.render("恢复默认", True, WHITE)
    back_text = button_font.render("返回", True, WHITE)
    
    # 计算位置
    center_x = window.get_rect().centerx
    center_y = window.get_rect().centery
    
    # 玩家标题位置
    player1_title = player_font.render("玩家一控制", True, BLUE)
    player2_title = player_font.render("玩家二控制", True, GREEN)
    player1_title_rect = player1_title.get_rect(center=(center_x - 300, center_y - 200))
    player2_title_rect = player2_title.get_rect(center=(center_x + 300, center_y - 200))
    
    # 控制项位置
    control_rects = []
    for i, label in enumerate(control_labels):
        label_surface = key_font.render(label, True, WHITE)
        rect = label_surface.get_rect(center=(center_x - 400, center_y - 100 + i * 50))
        control_rects.append(rect)
    
    # 玩家一键位显示位置
    player1_key_rects = []
    for i, key in enumerate(control_keys):
        key_name = key_names.get(current_player1_keys.get(key, ''), 
                               str(current_player1_keys.get(key, '未设置')))
        key_surface = key_font.render(key_name, True, YELLOW)
        rect = key_surface.get_rect(center=(center_x - 200, center_y - 100 + i * 50))
        player1_key_rects.append(rect)
    
    # 玩家二键位显示位置
    player2_key_rects = []
    for i, key in enumerate(control_keys):
        key_name = key_names.get(current_player2_keys.get(key, ''), 
                               str(current_player2_keys.get(key, '未设置')))
        key_surface = key_font.render(key_name, True, YELLOW)
        rect = key_surface.get_rect(center=(center_x + 200, center_y - 100 + i * 50))
        player2_key_rects.append(rect)
    
    # 按钮位置
    prev_rect = prev_text.get_rect(center=(center_x - 300, center_y + 250))
    next_rect = next_text.get_rect(center=(center_x - 150, center_y + 250))
    reset_rect = reset_text.get_rect(center=(center_x, center_y + 250))
    back_rect = back_text.get_rect(center=(center_x + 150, center_y + 250))
    
    # 按钮背景
    prev_bg = pygame.Rect(prev_rect.left - 20, prev_rect.top - 10, 
                         prev_rect.width + 40, prev_rect.height + 20)
    next_bg = pygame.Rect(next_rect.left - 20, next_rect.top - 10, 
                         next_rect.width + 40, next_rect.height + 20)
    reset_bg = pygame.Rect(reset_rect.left - 20, reset_rect.top - 10, 
                          reset_rect.width + 40, reset_rect.height + 20)
    back_bg = pygame.Rect(back_rect.left - 20, back_rect.top - 10, 
                         back_rect.width + 40, back_rect.height + 20)
    
    # 标题
    title_text = title_font.render("自定义键位", True, GOLD)
    title_rect = title_text.get_rect(center=(center_x, center_y - 280))
    
    # 页码显示
    page_text = page_font.render(f"第 {current_page + 1}/{len(control_pages)} 页", True, WHITE)
    page_rect = page_text.get_rect(center=(center_x, center_y + 200))
    
    # 提示文本
    hint_text = hint_font.render("点击键位进行修改，按ESC取消修改", True, WHITE)
    hint_rect = hint_text.get_rect(center=(center_x, center_y + 300))
    
    # 当前正在修改的键位
    editing_player = None
    editing_key = None
    editing_index = -1
    
    # 内部函数定义
    def update_control_page():
        """更新控制页面显示"""
        nonlocal control_labels, control_keys, control_rects, player1_key_rects, player2_key_rects
        
        control_labels, control_keys = zip(*control_pages[current_page])
        control_labels = list(control_labels)
        control_keys = list(control_keys)
        
        # 更新控制项位置
        control_rects.clear()
        for i, label in enumerate(control_labels):
            label_surface = key_font.render(label, True, WHITE)
            rect = label_surface.get_rect(center=(center_x - 400, center_y - 100 + i * 50))
            control_rects.append(rect)
        
        # 更新键位显示
        update_key_display()
    
    def update_key_display():
        """更新键位显示"""
        nonlocal player1_key_rects, player2_key_rects
        
        player1_key_rects.clear()
        player2_key_rects.clear()
        
        for i, key in enumerate(control_keys):
            # 玩家一
            key_name = key_names.get(current_player1_keys.get(key, ''), 
                                   str(current_player1_keys.get(key, '未设置')))
            key_surface = key_font.render(key_name, True, YELLOW)
            rect = key_surface.get_rect(center=(center_x - 200, center_y - 100 + i * 50))
            player1_key_rects.append(rect)
            
            # 玩家二
            key_name = key_names.get(current_player2_keys.get(key, ''), 
                                   str(current_player2_keys.get(key, '未设置')))
            key_surface = key_font.render(key_name, True, YELLOW)
            rect = key_surface.get_rect(center=(center_x + 200, center_y - 100 + i * 50))
            player2_key_rects.append(rect)
    
    # 初始化显示
    update_control_page()
    
    waiting = True
    while waiting:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if editing_player is not None:
                        # 取消编辑
                        editing_player = None
                        editing_key = None
                        editing_index = -1
                    else:
                        return True
                elif editing_player is not None:
                    # 正在编辑键位，保存新键位
                    if editing_player == 1:
                        current_player1_keys[editing_key] = event.key
                    else:
                        current_player2_keys[editing_key] = event.key
                    
                    # 重置编辑状态
                    editing_player = None
                    editing_key = None
                    editing_index = -1
                    
                    # 更新显示
                    update_key_display()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if editing_player is not None:
                    # 如果正在编辑，鼠标点击设置为攻击键
                    if event.button == 1:  # 左键
                        mouse_key = 'mouse_left'
                    elif event.button == 2:  # 中键
                        mouse_key = 'mouse_middle'
                    elif event.button == 3:  # 右键
                        mouse_key = 'mouse_right'
                    else:
                        mouse_key = None
                    
                    if mouse_key:
                        if editing_player == 1:
                            current_player1_keys[editing_key] = mouse_key
                        else:
                            current_player2_keys[editing_key] = mouse_key
                        
                        # 重置编辑状态
                        editing_player = None
                        editing_key = None
                        editing_index = -1
                        
                        # 更新显示
                        update_key_display()
                
                # 检查点击了哪个键位
                for i, rect in enumerate(player1_key_rects):
                    if rect.collidepoint(event.pos):
                        editing_player = 1
                        editing_key = control_keys[i]
                        editing_index = i
                        break
                
                for i, rect in enumerate(player2_key_rects):
                    if rect.collidepoint(event.pos):
                        editing_player = 2
                        editing_key = control_keys[i]
                        editing_index = i
                        break
                
                # 检查按钮点击
                if prev_bg.collidepoint(event.pos) and current_page > 0:
                    current_page -= 1
                    update_control_page()
                    
                elif next_bg.collidepoint(event.pos) and current_page < len(control_pages) - 1:
                    current_page += 1
                    update_control_page()
                    
                elif reset_bg.collidepoint(event.pos):
                    # 恢复默认键位
                    current_player1_keys = player1_keys.copy()
                    current_player2_keys = player2_keys.copy()
                    update_key_display()
                
                elif back_bg.collidepoint(event.pos):
                    return True
        
        # 绘制背景
        window.fill(SETTINGS_BG)
        
        # 绘制标题和页码
        window.blit(title_text, title_rect)
        page_text = page_font.render(f"第 {current_page + 1}/{len(control_pages)} 页", True, WHITE)
        window.blit(page_text, page_rect)
        
        # 绘制玩家标题
        window.blit(player1_title, player1_title_rect)
        window.blit(player2_title, player2_title_rect)
        
        # 绘制控制项标签
        for i, rect in enumerate(control_rects):
            label_surface = key_font.render(control_labels[i], True, WHITE)
            window.blit(label_surface, rect)
        
        # 绘制玩家一键位
        for i, rect in enumerate(player1_key_rects):
            key_name = key_names.get(current_player1_keys.get(control_keys[i], ''), 
                                   str(current_player1_keys.get(control_keys[i], '未设置')))
            if editing_player == 1 and editing_index == i:
                key_surface = key_font.render("按下新键...", True, RED)
                highlight_rect = pygame.Rect(rect.left - 10, rect.top - 5, rect.width + 20, rect.height + 10)
                pygame.draw.rect(window, (80, 80, 80), highlight_rect, border_radius=5)
            else:
                key_surface = key_font.render(key_name, True, YELLOW)
            window.blit(key_surface, rect)
        
        # 绘制玩家二键位
        for i, rect in enumerate(player2_key_rects):
            key_name = key_names.get(current_player2_keys.get(control_keys[i], ''), 
                                   str(current_player2_keys.get(control_keys[i], '未设置')))
            if editing_player == 2 and editing_index == i:
                key_surface = key_font.render("按下新键...", True, RED)
                highlight_rect = pygame.Rect(rect.left - 10, rect.top - 5, rect.width + 20, rect.height + 10)
                pygame.draw.rect(window, (80, 80, 80), highlight_rect, border_radius=5)
            else:
                key_surface = key_font.render(key_name, True, YELLOW)
            window.blit(key_surface, rect)
        
        # 绘制按钮
        prev_color = (80, 80, 80) if prev_bg.collidepoint(mouse_pos) and current_page > 0 else (50, 50, 50)
        next_color = (80, 80, 80) if next_bg.collidepoint(mouse_pos) and current_page < len(control_pages) - 1 else (50, 50, 50)
        reset_color = (80, 80, 80) if reset_bg.collidepoint(mouse_pos) else (50, 50, 50)
        back_color = (80, 80, 80) if back_bg.collidepoint(mouse_pos) else (50, 50, 50)
        
        pygame.draw.rect(window, prev_color, prev_bg, border_radius=10)
        pygame.draw.rect(window, BLUE, prev_bg, 3, border_radius=10)
        window.blit(prev_text, prev_rect)
        
        pygame.draw.rect(window, next_color, next_bg, border_radius=10)
        pygame.draw.rect(window, BLUE, next_bg, 3, border_radius=10)
        window.blit(next_text, next_rect)
        
        pygame.draw.rect(window, reset_color, reset_bg, border_radius=10)
        pygame.draw.rect(window, YELLOW, reset_bg, 3, border_radius=10)
        window.blit(reset_text, reset_rect)
        
        pygame.draw.rect(window, back_color, back_bg, border_radius=10)
        pygame.draw.rect(window, BLUE, back_bg, 3, border_radius=10)
        window.blit(back_text, back_rect)
        
        # 绘制提示文本
        window.blit(hint_text, hint_rect)
        
        pygame.display.flip()
    
    return True
def is_pyinstaller_bundle():
    """检测当前是否在PyInstaller打包后的环境中运行"""
    return hasattr(sys, '_MEIPASS') or getattr(sys, 'frozen', False)
def is_nuitka_bundle():
    """检测当前是否在Nuitka打包后的环境中运行"""
    return hasattr(sys, '__compiled__') or ('nuitka' in sys.modules)

def resource_path(relative_path):
    """
    获取资源的正确路径，适用于开发环境、PyInstaller和Nuitka打包后环境
    参数:
        relative_path: 资源文件的相对路径
    返回:
        资源的完整绝对路径
    """
    # 处理路径分隔符，确保跨平台兼容性
    if '\\' in relative_path:
        relative_path = relative_path.replace('\\', os.sep)
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        # Nuitka打包环境
        elif is_nuitka_bundle():
            # Nuitka中，资源文件通常与可执行文件在同一目录或子目录中
            if hasattr(sys, '_nuitka_binary_dir'):
                base_path = sys._nuitka_binary_dir
            else:
                # 如果没有_nuitka_binary_dir属性，使用可执行文件所在目录
                base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        else:
            base_path = os.path.abspath(".")
    except Exception:
        base_path = os.path.abspath(".")
    # 如果相对路径已经包含基础路径，直接返回
    if relative_path.startswith(base_path):
        return relative_path
    # 否则拼接路径
    full_path = os.path.join(base_path, relative_path)
    # 如果路径不存在，尝试在assets目录中查找
    if not os.path.exists(full_path):
        # 尝试直接在当前目录查找
        alt_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), relative_path)
        if os.path.exists(alt_path):
            return alt_path
        # 尝试在assets子目录查找
        assets_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "assets", os.path.basename(relative_path))
        if os.path.exists(assets_path):
            return assets_path
    return full_path
def load_player_skin(skin_name, player_num=1):
    """加载玩家贴图"""
    if skin_name == "default":
        return None  # 使用默认绿色方块
    
    try:
        skin_path = resource_path(os.path.join("assets", "Player", skin_name))
        if os.path.exists(skin_path):
            image = pygame.image.load(skin_path)
            # 统一缩放为50x50
            return pygame.transform.scale(image, (50,50))
        else:
            print(f"贴图文件不存在: {skin_path}")
            return None
    except Exception as e:
        print(f"加载贴图失败: {e}")
        return None
def get_available_skins():
    """获取所有可用的贴图"""
    skins = {}
    
    # 添加默认选项
    skins["default"] = "默认绿色方块"
    
    # 获取assets/Player目录下的所有文件
    player_dir = resource_path("assets\\Player")
    
    if os.path.exists(player_dir):
        for filename in os.listdir(player_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                # 如果字典中有定义显示名称，使用定义的名称，否则使用文件名
                display_name = PLAYER_SKINS.get(filename, os.path.splitext(filename)[0])
                skins[filename] = display_name
    
    return skins
# 修改skin_selection_menu函数，移除对is_player2的依赖
# 修改 settings_menu 函数，删除英雄选择相关代码
def settings_menu():
    """设置菜单 - 删除英雄选择选项"""
    global music_volume, melee_enabled, ranged_enabled, fullscreen, window
    
    # 创建字体
    title_font = pygame.font.Font(font_path, 60)
    option_font = pygame.font.Font(font_path, 40)
    slider_font = pygame.font.Font(font_path, 30)
    
    # 创建选项文本
    fullscreen_text = option_font.render("全屏模式", True, WHITE)
    music_text = option_font.render("音乐音量", True, WHITE)
    melee_text = option_font.render("近战武器", True, WHITE)
    ranged_text = option_font.render("远程武器", True, WHITE)
    keys_text = option_font.render("自定义键位", True, WHITE)
    # 删除皮肤选择选项
    
    # 计算位置 - 调整垂直间距（因为删除了一个选项）
    center_x = window.get_rect().centerx
    center_y = window.get_rect().centery
    
    # 选项位置 - 调整间距
    fullscreen_rect = fullscreen_text.get_rect(center=(center_x - 150, center_y - 200))
    music_rect = music_text.get_rect(center=(center_x - 150, center_y - 120))
    melee_rect = melee_text.get_rect(center=(center_x - 150, center_y - 40))
    ranged_rect = ranged_text.get_rect(center=(center_x - 150, center_y + 40))
    keys_rect = keys_text.get_rect(center=(center_x - 150, center_y + 120))
    # 删除皮肤选择位置
    
    # 返回按钮位置 - 向上移动（因为少了一个选项）
    back_text = option_font.render("返回", True, WHITE)
    back_rect = back_text.get_rect(center=(center_x, center_y + 200))
    
    # 全屏按钮背景
    fullscreen_button = pygame.Rect(fullscreen_rect.right + 20, fullscreen_rect.top, 30, 30)
    
    # 滑块位置和大小
    slider_width = 200
    slider_height = 20
    slider_x = center_x + 50
    
    # 调整滑块和复选框的位置
    music_slider_rect = pygame.Rect(slider_x, center_y - 130, slider_width, slider_height)
    melee_checkbox = pygame.Rect(slider_x, center_y - 50, 30, 30)
    ranged_checkbox = pygame.Rect(slider_x, center_y + 30, 30, 30)
    
    # 键位自定义按钮背景
    keys_button = pygame.Rect(keys_rect.right + 20, keys_rect.top, 
                             keys_rect.width + 40, keys_rect.height + 20)
    
    # 删除皮肤选择按钮背景
    
    # 返回按钮背景
    back_button = pygame.Rect(back_rect.left - 20, back_rect.top - 10, 
                             back_rect.width + 40, back_rect.height + 20)
    
    # 滑块手柄
    handle_radius = 10
    music_handle_x = slider_x + int(music_volume * slider_width)
    
    # 添加拖动状态变量
    dragging_volume = False
    
    waiting = True
    while waiting:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                elif event.key == pygame.K_F11:
                    toggle_fullscreen()
                    # 重新计算位置
                    center_x = window.get_rect().centerx
                    center_y = window.get_rect().centery
                    # 更新所有UI元素位置
                    fullscreen_rect.center = (center_x - 150, center_y - 200)
                    music_rect.center = (center_x - 150, center_y - 120)
                    melee_rect.center = (center_x - 150, center_y - 40)
                    ranged_rect.center = (center_x - 150, center_y + 40)
                    keys_rect.center = (center_x - 150, center_y + 120)
                    back_rect.center = (center_x, center_y + 200)
                    
                    fullscreen_button = pygame.Rect(fullscreen_rect.right + 20, fullscreen_rect.top, 30, 30)
                    music_slider_rect = pygame.Rect(center_x + 50, center_y - 130, slider_width, slider_height)
                    melee_checkbox = pygame.Rect(center_x + 50, center_y - 50, 30, 30)
                    ranged_checkbox = pygame.Rect(center_x + 50, center_y + 30, 30, 30)
                    keys_button = pygame.Rect(keys_rect.right + 20, keys_rect.top, 
                                             keys_rect.width + 40, keys_rect.height + 20)
                    back_button = pygame.Rect(back_rect.left - 20, back_rect.top - 10, 
                                             back_rect.width + 40, back_rect.height + 20)
                    music_handle_x = center_x + 50 + int(music_volume * slider_width)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 返回按钮
                if back_button.collidepoint(event.pos):
                    return True
                # 全屏切换按钮
                elif fullscreen_button.collidepoint(event.pos):
                    toggle_fullscreen()
                    # 重新计算位置
                    center_x = window.get_rect().centerx
                    center_y = window.get_rect().centery
                    # 更新所有UI元素位置
                    fullscreen_rect.center = (center_x - 150, center_y - 200)
                    music_rect.center = (center_x - 150, center_y - 120)
                    melee_rect.center = (center_x - 150, center_y - 40)
                    ranged_rect.center = (center_x - 150, center_y + 40)
                    keys_rect.center = (center_x - 150, center_y + 120)
                    back_rect.center = (center_x, center_y + 200)
                    
                    fullscreen_button = pygame.Rect(fullscreen_rect.right + 20, fullscreen_rect.top, 30, 30)
                    music_slider_rect = pygame.Rect(center_x + 50, center_y - 130, slider_width, slider_height)
                    melee_checkbox = pygame.Rect(center_x + 50, center_y - 50, 30, 30)
                    ranged_checkbox = pygame.Rect(center_x + 50, center_y + 30, 30, 30)
                    keys_button = pygame.Rect(keys_rect.right + 20, keys_rect.top, 
                                             keys_rect.width + 40, keys_rect.height + 20)
                    back_button = pygame.Rect(back_rect.left - 20, back_rect.top - 10, 
                                             back_rect.width + 40, back_rect.height + 20)
                    music_handle_x = center_x + 50 + int(music_volume * slider_width)
                # 复选框点击
                elif melee_checkbox.collidepoint(event.pos):
                    melee_enabled = not melee_enabled
                elif ranged_checkbox.collidepoint(event.pos):
                    ranged_enabled = not ranged_enabled
                # 键位自定义按钮
                elif keys_button.collidepoint(event.pos):
                    key_customization_menu()
                    # 重新绘制菜单
                    continue
                # 删除皮肤选择按钮点击处理
                # 音量滑块点击
                elif music_slider_rect.collidepoint(event.pos):
                    dragging_volume = True
                    # 直接设置音量
                    relative_x = event.pos[0] - slider_x
                    music_volume = max(0, min(1, relative_x / slider_width))
                    pygame.mixer.music.set_volume(music_volume)
                    music_handle_x = slider_x + int(music_volume * slider_width)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 左键释放
                    dragging_volume = False
            elif event.type == pygame.MOUSEMOTION:
                # 音量滑块拖动
                if dragging_volume:
                    # 确保鼠标在滑块范围内
                    mouse_x = max(slider_x, min(slider_x + slider_width, event.pos[0]))
                    relative_x = mouse_x - slider_x
                    music_volume = max(0, min(1, relative_x / slider_width))
                    pygame.mixer.music.set_volume(music_volume)
                    music_handle_x = slider_x + int(music_volume * slider_width)
        
        # 绘制背景
        window.fill(SETTINGS_BG)
        
        # 绘制标题
        title_surface = title_font.render("游戏设置", True, GOLD)
        title_rect = title_surface.get_rect(center=(center_x, center_y - 300))
        window.blit(title_surface, title_rect)
        
        # 绘制全屏选项
        window.blit(fullscreen_text, fullscreen_rect)
        fullscreen_color = GREEN if fullscreen else RED
        pygame.draw.rect(window, fullscreen_color, fullscreen_button, border_radius=5)
        
        # 绘制音乐音量
        window.blit(music_text, music_rect)
        pygame.draw.rect(window, SLIDER_COLOR, music_slider_rect, border_radius=10)
        
        # 确保滑块手柄在正确位置
        music_handle_x = slider_x + int(music_volume * slider_width)
        # 确保手柄不超出滑块边界
        music_handle_x = max(slider_x, min(slider_x + slider_width, music_handle_x))
        pygame.draw.circle(window, SLIDER_HANDLE, (music_handle_x, music_slider_rect.centery), handle_radius)
        
        # 显示音量数值
        volume_percent = int(music_volume * 100)
        volume_text = slider_font.render(f"{volume_percent}%", True, WHITE)
        window.blit(volume_text, (music_slider_rect.right + 20, music_slider_rect.top - 5))
        
        # 绘制近战武器选项
        window.blit(melee_text, melee_rect)
        melee_color = GREEN if melee_enabled else RED
        pygame.draw.rect(window, melee_color, melee_checkbox, border_radius=5)
        
        # 绘制远程武器选项
        window.blit(ranged_text, ranged_rect)
        ranged_color = GREEN if ranged_enabled else RED
        pygame.draw.rect(window, ranged_color, ranged_checkbox, border_radius=5)
        
        # 绘制键位自定义按钮
        keys_color = (80, 80, 80) if keys_button.collidepoint(mouse_pos) else (50, 50, 50)
        pygame.draw.rect(window, keys_color, keys_button, border_radius=10)
        pygame.draw.rect(window, GOLD, keys_button, 3, border_radius=10)
        window.blit(keys_text, keys_rect)
        
        # 删除皮肤选择按钮绘制
        
        # 绘制返回按钮
        back_color = (80, 80, 80) if back_button.collidepoint(mouse_pos) else (50, 50, 50)
        pygame.draw.rect(window, back_color, back_button, border_radius=10)
        pygame.draw.rect(window, BLUE, back_button, 3, border_radius=10)
        window.blit(back_text, back_rect)
        
        pygame.display.flip()
    
    return True

# 修改 skin_selection_menu 函数，添加 is_start_menu 参数
def skin_selection_menu(is_start_menu=False):
    """贴图选择菜单 - 支持玩家一和玩家二，可以设置为开始前的选择菜单"""
    global current_player_skin, current_player2_skin
    
    # 创建字体
    title_font = pygame.font.Font(font_path, 60)
    player_font = pygame.font.Font(font_path, 40)
    skin_font = pygame.font.Font(font_path, 15)
    button_font = pygame.font.Font(font_path, 40)
    min_title_font = pygame.font.Font(font_path, 20)
    description_font = pygame.font.Font(font_path, 18)  # 新增：描述字体
    
    # 皮肤描述字典 - 支持使用\n换行
    playerskin_text = {
        "default": "默认绿色方块\n速度(4/4)血量100\n无特殊效果",
        "0.png": "姚明 - 200+\n方块刷新数量加倍\n但移动速度减半",
        "1.png": "毛毛 - 可爱角色\n购买所需要的价格减半",
        "2.png": "熊大 - 森林守护者\n速度（3/4）血量150\n《熊熊羁绊》\n与熊二同时在场时速度翻倍",
        "3.png": "请输入文本 - 糖姐\n受到伤害时获得加速(bushi兴奋)",
        "4.png": "稻妻亲王殿下 - 神秘角色\n受到肥波伤害降低至5点",
        "5.png": "苏少羽 - 武侠风格\n按Alt向鼠标方向冲刺一定距离",
        "6.png": "胃袋这一块 - 搞笑角色\n血量300",
        "7.png": "点击输入文本 - 唐\n白板",
        "8.png": "熊二 - 熊大的伙伴\n在场时概率刷新可以回血的蜂蜜\n《熊熊羁绊》\n与熊大同时在场时速度翻倍"
    }
    
    # 获取所有可用的贴图
    available_skins = get_available_skins()
    skin_list = list(available_skins.items())
    
    # 计算布局
    skins_per_row = 10
    skin_size = 80
    skin_spacing = 30
    start_x = 100
    start_y = 325  # 向下移动为玩家预览留出空间
    
    # 创建返回/继续按钮 - 根据模式显示不同文本
    if is_start_menu:
        back_text = button_font.render("继续", True, WHITE)
    else:
        back_text = button_font.render("返回", True, WHITE)
    back_rect = back_text.get_rect(center=(window.get_rect().centerx, window.get_rect().bottom - 100))
    back_bg = pygame.Rect(back_rect.left - 20, back_rect.top - 10, 
                         back_rect.width + 40, back_rect.height + 20)
    
    # 当前选中的玩家（1或2）
    selected_player = 1
    
    # 新增：悬停状态变量
    hovered_skin = None
    hovered_description = ""
    
    waiting = True
    while waiting:
        mouse_pos = pygame.mouse.get_pos()
        
        # 重置悬停状态
        hovered_skin = None
        hovered_description = ""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 如果是开始前的菜单，不允许ESC退出
                    if not is_start_menu:
                        return True
                # 按1或2切换选中的玩家
                elif event.key == pygame.K_1:
                    selected_player = 1
                elif event.key == pygame.K_2:
                    selected_player = 2
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_bg.collidepoint(event.pos):
                    return True  # 无论是返回还是继续，都返回True
                
                # 检查点击了玩家选择区域
                player1_preview_rect = pygame.Rect(150, 150, 100, 100)
                player2_preview_rect = pygame.Rect(window.get_rect().centerx + 50, 150, 100, 100)
                
                if player1_preview_rect.collidepoint(event.pos):
                    selected_player = 1
                elif player2_preview_rect.collidepoint(event.pos):
                    selected_player = 2
                
                # 检查点击了哪个皮肤
                for i, (skin_id, display_name) in enumerate(skin_list):
                    row = i // skins_per_row
                    col = i % skins_per_row
                    x = start_x + col * (skin_size + skin_spacing)
                    y = start_y + row * (skin_size + skin_spacing + 35)
                    
                    skin_rect = pygame.Rect(x, y, skin_size, skin_size)
                    if skin_rect.collidepoint(event.pos):
                        if selected_player == 1:
                            current_player_skin = skin_id
                            # 如果玩家一存在，立即更新其皮肤
                            try:
                                if 'player' in globals() and player:
                                    skin_image = None
                                    if current_player_skin != "default":
                                        skin_image = load_player_skin(current_player_skin)
                                    player.set_skin(skin_image)
                            except:
                                pass  # 如果player不存在，忽略错误
                        else:
                            current_player2_skin = skin_id
                            # 如果玩家二存在，立即更新其皮肤
                            try:
                                if 'player2' in globals() and player2:
                                    skin_image = None
                                    if current_player2_skin != "default":
                                        skin_image = load_player_skin(current_player2_skin)
                                    player2.set_skin(skin_image)
                            except:
                                pass  # 如果player2不存在，忽略错误
        
        # 检查鼠标悬停在哪个皮肤上
        for i, (skin_id, display_name) in enumerate(skin_list):
            row = i // skins_per_row
            col = i % skins_per_row
            x = start_x + col * (skin_size + skin_spacing)
            y = start_y + row * (skin_size + skin_spacing + 35)
            
            skin_rect = pygame.Rect(x, y, skin_size, skin_size)
            if skin_rect.collidepoint(mouse_pos):
                hovered_skin = skin_id
                hovered_description = playerskin_text.get(skin_id, "暂无描述")
                break
        
        # 绘制
        window.fill(SETTINGS_BG)
        
        # 绘制标题
        if is_start_menu:
            title_text = title_font.render("请选择您的英雄：", True, GOLD)
        else:
            title_text = title_font.render("请选择您的英雄：", True, GOLD)
        title_rect = title_text.get_rect(center=(window.get_rect().centerx, 80))
        window.blit(title_text, title_rect)
        
        # 绘制玩家选择区域
        # 玩家一预览
        player1_title = player_font.render("玩家一:", True, BLUE)
        window.blit(player1_title, (15, 150))
        
        player1_preview_rect = pygame.Rect(150, 150, 100, 100)
        pygame.draw.rect(window, (80, 80, 80), player1_preview_rect, border_radius=8)
        if selected_player == 1:
            pygame.draw.rect(window, GOLD, player1_preview_rect, 3, border_radius=8)
        
        # 绘制玩家一当前皮肤
        if current_player_skin == "default":
            preview_surface = pygame.Surface((90, 90))
            preview_surface.fill(GREEN)
            window.blit(preview_surface, (155, 155))
        else:
            skin_image = load_player_skin(current_player_skin)
            if skin_image:
                scaled_skin = pygame.transform.scale(skin_image, (90, 90))
                window.blit(scaled_skin, (155, 155))
            else:
                error_surface = pygame.Surface((90, 90))
                error_surface.fill(RED)
                window.blit(error_surface, (155, 155))
        
        # 玩家一当前皮肤名称
        player1_skin_name = available_skins.get(current_player_skin, "未知")
        name_text = skin_font.render(player1_skin_name, True, WHITE)
        window.blit(name_text, (150, 255))
        
        # 玩家二预览
        player2_title = player_font.render("玩家二:", True, GREEN)
        player2_title_rect = player2_title.get_rect(left=window.get_rect().centerx -100, top=150)
        window.blit(player2_title, player2_title_rect)
        
        player2_preview_rect = pygame.Rect(window.get_rect().centerx + 50, 150, 100, 100)
        pygame.draw.rect(window, (80, 80, 80), player2_preview_rect, border_radius=8)
        if selected_player == 2:
            pygame.draw.rect(window, GOLD, player2_preview_rect, 3, border_radius=8)
        
        # 绘制玩家二当前皮肤
        if current_player2_skin == "default":
            preview_surface = pygame.Surface((90, 90))
            preview_surface.fill(FOREST)
            window.blit(preview_surface, (window.get_rect().centerx + 55, 155))
        else:
            skin_image = load_player_skin(current_player2_skin)
            if skin_image:
                scaled_skin = pygame.transform.scale(skin_image, (90, 90))
                window.blit(scaled_skin, (window.get_rect().centerx + 55, 155))
            else:
                error_surface = pygame.Surface((90, 90))
                error_surface.fill(RED)
                window.blit(error_surface, (window.get_rect().centerx + 55, 155))
        
        # 玩家二当前皮肤名称
        player2_skin_name = available_skins.get(current_player2_skin, "未知")
        name_text = skin_font.render(player2_skin_name, True, WHITE)
        name_rect = name_text.get_rect(left=window.get_rect().centerx + 50, top=255)
        window.blit(name_text, name_rect)
        
        # 绘制提示文本
        hint_text = min_title_font.render("点击玩家预览区域切换玩家，点击皮肤进行设置 (按1/2快速切换)", True, WHITE)
        hint_rect = hint_text.get_rect(center=(window.get_rect().centerx, 125))
        window.blit(hint_text, hint_rect)
        
        # 绘制所有贴图
        for i, (skin_id, display_name) in enumerate(skin_list):
            row = i // skins_per_row
            col = i % skins_per_row
            x = start_x + col * (skin_size + skin_spacing)
            y = start_y + row * (skin_size + skin_spacing + 100)
            
            # 绘制贴图背景（高亮当前选择的）
            bg_rect = pygame.Rect(x - 5, y - 5, skin_size + 10, skin_size + 10)
            
            # 检查是否是当前选中的玩家的皮肤
            is_player1_current = (selected_player == 1 and skin_id == current_player_skin)
            is_player2_current = (selected_player == 2 and skin_id == current_player2_skin)
            
            if is_player1_current or is_player2_current:
                pygame.draw.rect(window, GOLD, bg_rect, border_radius=8)
            else:
                pygame.draw.rect(window, (80, 80, 80), bg_rect, border_radius=8)
            
            # 绘制贴图
            if skin_id == "default":
                # 默认绿色方块
                skin_surface = pygame.Surface((skin_size - 10, skin_size - 10))
                # 根据选中的玩家显示不同的默认颜色
                if selected_player == 1:
                    skin_surface.fill(GREEN)
                else:
                    skin_surface.fill(FOREST)
                window.blit(skin_surface, (x, y))
            else:
                # 加载并显示贴图
                skin_image = load_player_skin(skin_id)
                if skin_image:
                    # 调整贴图大小以适应预览
                    preview_size = skin_size - 10
                    scaled_skin = pygame.transform.scale(skin_image, (preview_size, preview_size))
                    window.blit(scaled_skin, (x, y))
                else:
                    # 贴图加载失败，显示红色方块
                    error_surface = pygame.Surface((skin_size - 10, skin_size - 10))
                    error_surface.fill(RED)
                    window.blit(error_surface, (x, y))
            
            # 绘制贴图名称
            name_text = skin_font.render(display_name, True, WHITE)
            name_rect = name_text.get_rect(center=(x + skin_size // 2, y + skin_size + 15))
            window.blit(name_text, name_rect)
        
        # 绘制返回/继续按钮
        back_color = (80, 80, 80) if back_bg.collidepoint(mouse_pos) else (50, 50, 50)
        pygame.draw.rect(window, back_color, back_bg, border_radius=10)
        pygame.draw.rect(window, BLUE, back_bg, 3, border_radius=10)
        window.blit(back_text, back_rect)
        
        # 新增：绘制悬停描述（支持换行和半透明背景）
        if hovered_skin and hovered_description:
            # 分割描述文本为多行
            lines = hovered_description.split('\n')
            
            # 计算每行文本的尺寸
            line_surfaces = []
            max_width = 0
            total_height = 0
            line_height = description_font.get_linesize()
            
            for line in lines:
                line_surface = description_font.render(line, True, WHITE)
                line_surfaces.append(line_surface)
                max_width = max(max_width, line_surface.get_width())
                total_height += line_height
            
            # 计算描述框尺寸
            padding = 10
            desc_width = max_width + padding * 2
            desc_height = total_height + padding * 2
            
            # 计算描述框位置（在鼠标下方）
            desc_bg_rect = pygame.Rect(
                mouse_pos[0] - padding, 
                mouse_pos[1] + 20, 
                desc_width, 
                desc_height
            )
            
            # 确保描述框不会超出屏幕边界
            if desc_bg_rect.right > win_kuan:
                desc_bg_rect.right = win_kuan - 10
            if desc_bg_rect.bottom > win_gao:
                desc_bg_rect.bottom = win_gao - 10
            if desc_bg_rect.left < 0:
                desc_bg_rect.left = 10
            if desc_bg_rect.top < 0:
                desc_bg_rect.top = 10
            
            # 创建半透明表面
            desc_surface = pygame.Surface((desc_width, desc_height), pygame.SRCALPHA)
            
            # 绘制半透明背景 (RGBA: 前三个是颜色，第四个是bu透明度)
            pygame.draw.rect(desc_surface, (40, 40, 40, 150), (0, 0, desc_width, desc_height), border_radius=5)
            
            # 绘制边框
            pygame.draw.rect(desc_surface, (255, 215, 0, 200), (0, 0, desc_width, desc_height), 2, border_radius=5)
            
            # 将半透明表面绘制到窗口
            window.blit(desc_surface, desc_bg_rect)
            
            # 绘制多行描述文本
            y_offset = desc_bg_rect.y + padding
            for line_surface in line_surfaces:
                window.blit(line_surface, (desc_bg_rect.x + padding, y_offset))
                y_offset += line_height
        
        pygame.display.flip()
    
    return True
def apply_advanced_blur(surface, iterations=2, blur_radius=5):
    """
    应用高级模糊效果到表面
    参数:
        surface: 要模糊的pygame表面
        iterations: 模糊迭代次数
        blur_radius: 模糊半径
    返回:
        模糊后的表面
    """
    blurred_surface = surface.copy()
    for i in range(iterations):
        # 计算降采样尺寸
        scale_factor = 1.0 / (blur_radius / (i + 1))
        small_size = (int(blurred_surface.get_width() * scale_factor), 
                      int(blurred_surface.get_height() * scale_factor))
        # 确保尺寸不为0
        small_size = (max(1, small_size[0]), max(1, small_size[1]))
        # 降采样
        small_surface = pygame.transform.smoothscale(blurred_surface, small_size)
        # 升采样回原始尺寸
        blurred_surface = pygame.transform.smoothscale(small_surface, surface.get_size())
    return blurred_surface

def wait_for_key_press(screen, message="请按任意键继续", message2="", font_size1=36, font_size2=18, 
                      text_color=(255, 255, 255), text2_color=(255, 255, 255), blur_radius=25, show_main_menu_button=False):
    """
    显示提示并等待按键
    参数:
        screen: Pygame显示表面
        message: 主提示消息
        message2: 副提示消息
        font_size1: 主消息字体大小
        font_size2: 副消息字体大小
        text_color: 主消息文本颜色
        text2_color: 副消息文本颜色
        blur_radius: 高斯模糊半径
        show_main_menu_button: 是否显示返回主界面按钮
    返回:
        True如果用户按键继续，False如果用户关闭窗口，2如果用户点击返回主界面
    """
    # 记录暂停开始时间
    pause_start_time = pygame.time.get_ticks()
    # 创建字体
    font = pygame.font.Font(font_path, font_size1)
    font2 = pygame.font.Font(font_path, font_size2)
    # 创建屏幕的副本并应用高斯模糊
    screen_copy = screen.copy()
    blurred_bg = apply_advanced_blur(screen_copy, 10, blur_radius)
    # 计算文本位置
    center_rect = screen.get_rect().center
    rect_fix = (center_rect[0], center_rect[1]-100)
    rect2_fix = (center_rect[0], center_rect[1])
    # 渲染提示文本
    text_surface = font.render(message, True, text_color)
    text_rect = text_surface.get_rect(center=rect_fix)
    text2_surface = font2.render(message2, True, text2_color)
    text2_rect = text2_surface.get_rect(center=rect2_fix)
    
    # 如果显示返回主界面按钮，创建按钮
    main_menu_button = None
    if show_main_menu_button:
        button_font = pygame.font.Font(font_path, 40)
        button_text = button_font.render("返回主界面", True, GOLD)
        button_rect = button_text.get_rect(center=(center_rect[0], center_rect[1] + 100))
        button_bg = pygame.Rect(button_rect.left - 20, button_rect.top - 10, 
                               button_rect.width + 40, button_rect.height + 20)
    
    # 绘制模糊背景和文本
    screen.blit(blurred_bg, (0, 0))
    screen.blit(text_surface, text_rect)
    screen.blit(text2_surface, text2_rect)
    
    # 绘制返回主界面按钮
    if show_main_menu_button:
        # 获取鼠标位置
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        # 检查鼠标悬停
        if button_bg.collidepoint(mouse_pos):
            button_color = (80, 80, 80)  # 悬停时的颜色
            if mouse_click[0]:  # 鼠标左键点击
                button_color = (100, 100, 100)  # 点击时的颜色
        else:
            button_color = (50, 50, 50)  # 正常颜色
            
        pygame.draw.rect(screen, button_color, button_bg, border_radius=10)
        pygame.draw.rect(screen, GOLD, button_bg, 3, border_radius=10)
        screen.blit(button_text, button_rect)
    
    pygame.display.flip()
    # 等待任意按键
    waiting = True
    while waiting:
        time.sleep(0.05)  # 减少CPU使用率
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # 用户关闭窗口
            elif event.type == pygame.KEYDOWN:
                # 暂停结束，更新所有玩家的状态效果开始时间
                pause_duration = pygame.time.get_ticks() - pause_start_time
                _adjust_player_effect_timers(pause_duration)
                return True   # 用户按键继续
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_main_menu_button and button_bg.collidepoint(event.pos):
                    # 暂停结束，更新所有玩家的状态效果开始时间
                    pause_duration = pygame.time.get_ticks() - pause_start_time
                    _adjust_player_effect_timers(pause_duration)
                    return 2   # 用户点击返回主界面
                else:
                    # 暂停结束，更新所有玩家的状态效果开始时间
                    pause_duration = pygame.time.get_ticks() - pause_start_time
                    _adjust_player_effect_timers(pause_duration)
                    return True   # 用户点击鼠标继续
    return True

def _adjust_player_effect_timers(pause_duration):
    """
    调整所有玩家的状态效果开始时间，以补偿暂停时间
    参数:
        pause_duration: 暂停持续时间（毫秒）
    """
    # 调整玩家一的计时器
    if player.boosted:
        player.boost_start_time += pause_duration
    if player.slowed:
        player.slowly_start_time += pause_duration
    if player.iced:
        player.icely_start_time += pause_duration
    # 调整玩家二的计时器（如果存在）
    if is_player2 and player2:
        if player2.boosted:
            player2.boost_start_time += pause_duration
        if player2.slowed:
            player2.slowly_start_time += pause_duration
        if player2.iced:
            player2.icely_start_time += pause_duration
    # 调整AI玩家的计时器（如果存在）
    if is_vsai and player_ai:
        if player_ai.boosted:
            player_ai.boost_start_time += pause_duration
        if player_ai.slowed:
            player_ai.slowly_start_time += pause_duration
        if player_ai.iced:
            player_ai.icely_start_time += pause_duration

def starter_menu(screen, messages=["请按任意键继续"], font_sizes=[36], 
                 text_color=(255, 255, 255), choose=True):
    """
    显示开始菜单并等待用户选择
    参数:
        screen: Pygame显示表面
        messages: 提示消息列表
        font_sizes: 字体大小列表
        text_color: 文本颜色
        choose: 是否允许选择模式
    返回:
        0-3表示不同的按键选择，4表示退出，5表示继续
    """
    # 获取屏幕中心
    screen_rect = screen.get_rect()
    center_x = screen_rect.centerx
    center_y = screen_rect.centery
    # 行间距
    line_spacing = 20
    # 创建所有文本表面并计算总高度
    text_surfaces = []
    text_heights = []
    for i, message in enumerate(messages):
        # 获取对应的字体大小，如果没有则使用第一个
        font_size = font_sizes[i] if i < len(font_sizes) else font_sizes[0]
        font = pygame.font.Font(font_path, font_size)
        # 渲染文本
        text_surface = font.render(message, True, text_color)
        text_surfaces.append(text_surface)
        text_heights.append(text_surface.get_height())
    # 计算总高度（包括行间距）
    total_height = sum(text_heights) + (len(messages) - 1) * line_spacing
    # 计算每个文本的位置（垂直居中）
    current_y = center_y - total_height // 2
    for text_surface in text_surfaces:
        # 计算文本位置
        text_rect = text_surface.get_rect()
        text_rect.centerx = center_x
        text_rect.y = current_y
        # 绘制文本
        screen.blit(text_surface, text_rect)
        # 更新下一行的起始位置
        current_y += text_rect.height + line_spacing
    pygame.display.flip()
    # 等待特定按键
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if choose:
                if event.type == pygame.QUIT:
                    return 4
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 0
                    elif event.key == pygame.K_2:
                        return 1
                    elif event.key == pygame.K_3:
                        return 3
                    elif event.key == pygame.K_4:
                        return 6
            else:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return 5
                if event.type == pygame.QUIT:
                    return 4
    return 4

def main_menu():
    """显示主菜单"""
    global window
    
    # 创建字体
    title_font = pygame.font.Font(font_path, 80)
    button_font = pygame.font.Font(font_path, 50)
    
    # 创建按钮
    start_button_text = button_font.render("开始游戏", True, WHITE)
    settings_button_text = button_font.render("设置", True, WHITE)
    quit_button_text = button_font.render("退出游戏", True, WHITE)
    
    # 计算按钮位置
    center_x = window.get_rect().centerx
    center_y = window.get_rect().centery
    
    start_button_rect = start_button_text.get_rect(center=(center_x, center_y - 50))
    settings_button_rect = settings_button_text.get_rect(center=(center_x, center_y + 50))
    quit_button_rect = quit_button_text.get_rect(center=(center_x, center_y + 150))
    
    # 按钮背景
    start_button_bg = pygame.Rect(start_button_rect.left - 20, start_button_rect.top - 10, 
                                 start_button_rect.width + 40, start_button_rect.height + 20)
    settings_button_bg = pygame.Rect(settings_button_rect.left - 20, settings_button_rect.top - 10, 
                                    settings_button_rect.width + 40, settings_button_rect.height + 20)
    quit_button_bg = pygame.Rect(quit_button_rect.left - 20, quit_button_rect.top - 10, 
                                quit_button_rect.width + 40, quit_button_rect.height + 20)
    
    # 游戏标题
    title_text = title_font.render("方块吃方块", True, GOLD)
    title_rect = title_text.get_rect(center=(center_x, center_y - 200))
    
    # 版本信息
    version_font = pygame.font.Font(font_path, 24)
    version_text = version_font.render(version, True, WHITE)
    version_rect = version_text.get_rect(center=(center_x, center_y - 150))
    
    waiting = True
    while waiting:
        # 获取鼠标位置和点击状态
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # 添加F11快捷键
                    toggle_fullscreen()
                    # 更新位置信息
                    center_x = window.get_rect().centerx
                    center_y = window.get_rect().centery
                    # 更新所有位置
                    start_button_rect.center = (center_x, center_y - 50)
                    settings_button_rect.center = (center_x, center_y + 50)
                    quit_button_rect.center = (center_x, center_y + 150)
                    title_rect.center = (center_x, center_y - 200)
                    version_rect.center = (center_x, center_y - 150)
                    start_button_bg = pygame.Rect(start_button_rect.left - 20, start_button_rect.top - 10, 
                                                 start_button_rect.width + 40, start_button_rect.height + 20)
                    settings_button_bg = pygame.Rect(settings_button_rect.left - 20, settings_button_rect.top - 10, 
                                                    settings_button_rect.width + 40, settings_button_rect.height + 20)
                    quit_button_bg = pygame.Rect(quit_button_rect.left - 20, quit_button_rect.top - 10, 
                                                quit_button_rect.width + 40, quit_button_rect.height + 20)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_bg.collidepoint(event.pos):
                    return 0
                elif settings_button_bg.collidepoint(event.pos):
                    # 调用设置菜单
                    settings_result = settings_menu()
                    if not settings_result:  # 如果设置菜单返回False，退出游戏
                        return 1
                    # 重新绘制菜单
                    continue
                elif quit_button_bg.collidepoint(event.pos):
                    return 1
        
        # 绘制背景
        window.fill(BLACK)
        
        # 绘制标题
        window.blit(title_text, title_rect)
        window.blit(version_text, version_rect)
        
        # 绘制开始按钮（带悬停效果）
        if start_button_bg.collidepoint(mouse_pos):
            start_button_color = (80, 80, 80)
            if mouse_click[0]:
                start_button_color = (100, 100, 100)
        else:
            start_button_color = (50, 50, 50)
            
        pygame.draw.rect(window, start_button_color, start_button_bg, border_radius=10)
        pygame.draw.rect(window, BLUE, start_button_bg, 3, border_radius=10)
        window.blit(start_button_text, start_button_rect)
        
        # 绘制设置按钮（带悬停效果）
        if settings_button_bg.collidepoint(mouse_pos):
            settings_button_color = (80, 80, 80)
            if mouse_click[0]:
                settings_button_color = (100, 100, 100)
        else:
            settings_button_color = (50, 50, 50)
            
        pygame.draw.rect(window, settings_button_color, settings_button_bg, border_radius=10)
        pygame.draw.rect(window, YELLOW, settings_button_bg, 3, border_radius=10)
        window.blit(settings_button_text, settings_button_rect)
        
        # 绘制退出按钮（带悬停效果）
        if quit_button_bg.collidepoint(mouse_pos):
            quit_button_color = (80, 80, 80)
            if mouse_click[0]:
                quit_button_color = (100, 100, 100)
        else:
            quit_button_color = (50, 50, 50)
            
        pygame.draw.rect(window, quit_button_color, quit_button_bg, border_radius=10)
        pygame.draw.rect(window, RED, quit_button_bg, 3, border_radius=10)
        window.blit(quit_button_text, quit_button_rect)
        
        pygame.display.flip()
    
    return 1

def mode_select_menu(screen):
    """
    显示模式选择菜单
    参数:
        screen: Pygame显示表面
    返回:
        0: 单人模式
        1: 双人模式
        3: 对战人机
        4: 退出
        6: 隐藏模式
    """
    # 创建字体
    title_font = pygame.font.Font(font_path, 60)
    button_font = pygame.font.Font(font_path, 40)
    hint_font = pygame.font.Font(font_path, 24)
    
    # 创建按钮
    single_button_text = button_font.render("单人模式", True, WHITE)
    double_button_text = button_font.render("双人模式", True, WHITE)
    ai_button_text = button_font.render("对战人机", True, WHITE)
    
    # 计算按钮位置
    center_x = screen.get_rect().centerx
    center_y = screen.get_rect().centery
    
    single_button_rect = single_button_text.get_rect(center=(center_x, center_y - 100))
    double_button_rect = double_button_text.get_rect(center=(center_x, center_y))
    ai_button_rect = ai_button_text.get_rect(center=(center_x, center_y + 100))
    
    # 按钮背景
    single_button_bg = pygame.Rect(single_button_rect.left - 20, single_button_rect.top - 10, 
                                  single_button_rect.width + 40, single_button_rect.height + 20)
    double_button_bg = pygame.Rect(double_button_rect.left - 20, double_button_rect.top - 10, 
                                  double_button_rect.width + 40, double_button_rect.height + 20)
    ai_button_bg = pygame.Rect(ai_button_rect.left - 20, ai_button_rect.top - 10, 
                              ai_button_rect.width + 40, ai_button_rect.height + 20)
    
    # 标题
    title_text = title_font.render("请选择游戏模式", True, WHITE)
    title_rect = title_text.get_rect(center=(center_x, center_y - 200))
    
    # 提示文本
    hint_text = hint_font.render("也可以使用键盘数字键选择: 1-单人  2-双人  3-对战人机", True, WHITE)
    hint_rect = hint_text.get_rect(center=(center_x, center_y + 280))
    
    waiting = True
    while waiting:
        # 获取鼠标位置和点击状态
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 4
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 0
                elif event.key == pygame.K_2:
                    return 1
                elif event.key == pygame.K_3:
                    return 3
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if single_button_bg.collidepoint(event.pos):
                    return 0
                elif double_button_bg.collidepoint(event.pos):
                    return 1
                elif ai_button_bg.collidepoint(event.pos):
                    return 3
        
        # 绘制背景
        screen.fill(BLACK)
        
        # 绘制标题
        screen.blit(title_text, title_rect)
        
        # 绘制单人模式按钮（带悬停效果）
        if single_button_bg.collidepoint(mouse_pos):
            single_button_color = (80, 80, 80)  # 悬停时的颜色
            if mouse_click[0]:  # 鼠标左键点击
                single_button_color = (100, 100, 100)  # 点击时的颜色
        else:
            single_button_color = (50, 50, 50)  # 正常颜色
            
        pygame.draw.rect(screen, single_button_color, single_button_bg, border_radius=10)
        pygame.draw.rect(screen, BLUE, single_button_bg, 3, border_radius=10)
        screen.blit(single_button_text, single_button_rect)
        
        # 绘制双人模式按钮（带悬停效果）
        if double_button_bg.collidepoint(mouse_pos):
            double_button_color = (80, 80, 80)  # 悬停时的颜色
            if mouse_click[0]:  # 鼠标左键点击
                double_button_color = (100, 100, 100)  # 点击时的颜色
        else:
            double_button_color = (50, 50, 50)  # 正常颜色
            
        pygame.draw.rect(screen, double_button_color, double_button_bg, border_radius=10)
        pygame.draw.rect(screen, GREEN, double_button_bg, 3, border_radius=10)
        screen.blit(double_button_text, double_button_rect)
        
        # 绘制对战人机按钮（带悬停效果）
        if ai_button_bg.collidepoint(mouse_pos):
            ai_button_color = (80, 80, 80)  # 悬停时的颜色
            if mouse_click[0]:  # 鼠标左键点击
                ai_button_color = (100, 100, 100)  # 点击时的颜色
        else:
            ai_button_color = (50, 50, 50)  # 正常颜色
            
        pygame.draw.rect(screen, ai_button_color, ai_button_bg, border_radius=10)
        pygame.draw.rect(screen, RED, ai_button_bg, 3, border_radius=10)
        screen.blit(ai_button_text, ai_button_rect)
        
        
        # 绘制提示文本
        screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()
    
    return 4

def is_overlapping_with_bombs(sprite, bombs, min_distance=100):
    """
    检查精灵是否与任何炸弹重叠或距离过近
    参数:
        sprite: 要检查的精灵
        bombs: 炸弹精灵组
        min_distance: 最小安全距离
    返回:
        True如果重叠，False否则
    """
    for bomb in bombs:
        dx = bomb.rect.centerx - sprite.rect.centerx
        dy = bomb.rect.centery - sprite.rect.centery
        distance = (dx**2 + dy**2)**0.5
        if distance < min_distance:
            return True
    return False

def generate_non_overlapping_position(sprite_class, bombs, max_attempts=50):
    """
    生成不与炸弹重叠的位置
    参数:
        sprite_class: 精灵类
        bombs: 炸弹精灵组
        max_attempts: 最大尝试次数
    返回:
        不重叠的精灵实例
    """
    for attempt in range(max_attempts):
        sprite = sprite_class()
        if not is_overlapping_with_bombs(sprite, bombs):
            return sprite
    # 如果尝试多次仍然找不到合适位置，返回一个随机位置
    return sprite_class()

def update_hits(players):
    """
    更新玩家与各种物体的碰撞检测
    """
    global score, score2, score3, need_to_win, player2_need_to_win, ai_need_to_win, game_range,died_range,player2_died_range,player_ai_died_range, explosions, version
    fengmi_hits = pygame.sprite.spritecollide(players,fengmis,False)
    for hit in fengmi_hits:
        players.heal(100, players.rect.centerx, players.rect.top)
        hit.kill()
    xionger_hits = pygame.sprite.spritecollide(players,xiongers,False)
    for hit in xionger_hits:
        hedam = random.randint(1,50)
        if players == player:
            if is_plz1:
                players.activate_boost()
            players.take_damage(hedam, players.rect.centerx, players.rect.top)
            score += hedam
        elif players == player2:
            if is_plz2:
                players.activate_boost()

            players.take_damage(hedam, players.rect.centerx, players.rect.top)
            score2 += hedam
        elif players == player_ai:
            players.take_damage(hedam, players.rect.centerx,players.rect.top)
            score3 += hedam
        hit.kill()

    # 检测与障碍物的碰撞
    hits = pygame.sprite.spritecollide(players, obstacles, False)
    for hit in hits:
        # 移除装备武器的检查，让玩家始终可以与障碍物碰撞
        if players == player:
            score += 1
        elif is_player2 and players == player2:
            score2 += 1
        elif is_vsai and players == player_ai:
            score3 += 1
        hit.kill()
    
    # 检测与加速道具的碰撞
    speed_hits = pygame.sprite.spritecollide(players, speeds, False)
    for speed in speed_hits:
        players.activate_boost()
        speed.kill()
    
    # 检测与需求道具的碰撞
    needs_hits = pygame.sprite.spritecollide(players, needes, False)
    for need in needs_hits:
        if players == player:
            need_to_win += 15
        elif is_player2 and players == player2:
            player2_need_to_win += 15
        elif is_vsai and players == player_ai:
            ai_need_to_win += 15
        need.kill()
    
    # 检测与减速道具的碰撞 - 添加扣血效果
    slows_hits = pygame.sprite.spritecollide(players, slows, False)
    for slow in slows_hits:
        
        # 受到伤害并显示伤害数字
        if players == player and is_plz1:
            players.take_damage(10, players.rect.centerx, players.rect.top)
            players.activate_boost()
        elif players == player2 and is_plz2:
            players.take_damage(10, players.rect.centerx, players.rect.top)
            players.activate_boost()
        else:
            players.activate_slowly()
            players.take_damage(10, players.rect.centerx, players.rect.top)
        slow.kill()
    
    # 检测与加强障碍物的碰撞
    obsplus_hits = pygame.sprite.spritecollide(players, obspluses, False)
    for obs_hit in obsplus_hits:
        if players == player:
            if not is_tomato1:
                players.heal(25, players.rect.centerx, players.rect.top)
            else:
                players.heal(10, players.rect.centerx, players.rect.top)
            score += 5
        elif is_player2 and players == player2:
            if not is_tomato2:
                players.heal(25, players.rect.centerx, players.rect.top)
            else:
                players.heal(10, players.rect.centerx, players.rect.top)

            score2 += 5
        elif is_vsai and players == player_ai:
            players.heal(25, players.rect.centerx, players.rect.top)
            score3 += 5
        obs_hit.kill()
    
    # 检测与炸弹的碰撞 - 添加扣血效果
    bomb_hits = pygame.sprite.spritecollide(players, bombs, False)
    for bombhit in bomb_hits:
        # 受到大量伤害
        players.take_damage(100, players.rect.centerx, players.rect.top)
        # 创建爆炸特效
        explosions.append(create_explosion(bombhit.rect.centerx, bombhit.rect.centery))
        bombhit.kill()
    
    # 检测与冰冻道具的碰撞 - 添加扣血效果
    ice_hits = pygame.sprite.spritecollide(players, icese, False)
    for ice_hit in ice_hits:
        if players == player and is_plz1:
            players.take_damage(15, players.rect.centerx, players.rect.top)
            players.activate_boost()
        elif players == player2 and is_plz2:
            players.take_damage(15, players.rect.centerx, players.rect.top)
            players.activate_boost()
        else:
            players.activate_ice()
            players.take_damage(15, players.rect.centerx, players.rect.top)
        # 受到伤害并显示伤害数字
        ice_hit.kill()
    
    # 检测武器与物体的碰撞
    if players.equipped_weapon == 'sword' and players.sword.is_attacking:
        # 检测剑与所有物体的碰撞
        sword_range = players.sword.get_attack_range()
        
        # 检测与障碍物的碰撞
        for obstacle in obstacles:
            if sword_range.colliderect(obstacle.rect):
                if obstacle.take_damage(players.sword.damage):
                    obstacle.kill()

        
        # 检测与炸弹的碰撞
        for bomb in bombs:
            if sword_range.colliderect(bomb.rect):
                if bomb.take_damage(players.sword.damage):
                    # 炸弹爆炸
                    bomb.kill()
                    # 创建爆炸特效
                    explosions.append(create_explosion(bomb.rect.centerx, bomb.rect.centery))
                    # 玩家受到伤害
                    players.take_damage(25, players.rect.centerx, players.rect.top)
                    # 摧毁附近的方块
                    for obstacle in obstacles:
                        dx = obstacle.rect.centerx - bomb.rect.centerx
                        dy = obstacle.rect.centery - bomb.rect.centery
                        distance = (dx**2 + dy**2)**0.5
                        if distance < 25:  # 爆炸范围
                            obstacle.kill()
        
        # 检测与肥波的碰撞
        for feibo in feibos:
            if sword_range.colliderect(feibo.rect):
                if feibo.take_damage(players.sword.damage):
                    feibo.kill()

    
    # 检测枪与物体的碰撞
    if players.equipped_weapon == 'gun':
        # 修改枪与物体的碰撞检测部分
        for bullet in players.gun.bullets[:]:
            # 检测子弹与所有物体的碰撞
            bullet_rect = pygame.Rect(bullet['x'] - 8, bullet['y'] - 8, 16, 16)  # 放大子弹碰撞区域
            
            # 检测与障碍物的碰撞
            for obstacle in obstacles:
                if bullet_rect.colliderect(obstacle.rect):
                    if obstacle.take_damage(players.gun.damage):
                        obstacle.kill()

                    
                    # 移除子弹
                    if bullet in players.gun.bullets:
                        players.gun.bullets.remove(bullet)
                    break
            
            # 检测与炸弹的碰撞
            for bomb in bombs:
                if bullet_rect.colliderect(bomb.rect):
                    if bomb.take_damage(players.gun.damage):
                        # 炸弹爆炸
                        bomb.kill()
                        # 创建爆炸特效
                        explosions.append(create_explosion(bomb.rect.centerx, bomb.rect.centery))
                        # 玩家受到伤害
                        players.take_damage(25, players.rect.centerx, players.rect.top)
                        # 摧毁附近的方块
                        for obstacle in obstacles:
                            dx = obstacle.rect.centerx - bomb.rect.centerx
                            dy = obstacle.rect.centery - bomb.rect.centery
                            distance = (dx**2 + dy**2)**0.5
                            if distance < 25:  # 爆炸范围
                                obstacle.kill()
                    
                    # 移除子弹
                    if bullet in players.gun.bullets:
                        players.gun.bullets.remove(bullet)
                    break
            
            # 检测与肥波的碰撞
            for feibo in feibos:
                if bullet_rect.colliderect(feibo.rect):
                    if feibo.take_damage(players.gun.damage):
                        feibo.kill()
                    
                    # 移除子弹
                    if bullet in players.gun.bullets:
                        players.gun.bullets.remove(bullet)
                    break
            
            # 检测与其他道具的碰撞
            for speed in speeds:
                if bullet_rect.colliderect(speed.rect):
                    if speed.take_damage(players.gun.damage):
                        speed.kill()
                    # 移除子弹
                    if bullet in players.gun.bullets:
                        players.gun.bullets.remove(bullet)
                    break
            
            for need in needes:
                if bullet_rect.colliderect(need.rect):
                    if need.take_damage(players.gun.damage):
                        need.kill()
                    # 移除子弹
                    if bullet in players.gun.bullets:
                        players.gun.bullets.remove(bullet)
                    break
            
            for slow in slows:
                if bullet_rect.colliderect(slow.rect):
                    if slow.take_damage(players.gun.damage):
                        slow.kill()
                    # 移除子弹
                    if bullet in players.gun.bullets:
                        players.gun.bullets.remove(bullet)
                    break
            
            for obsplus in obspluses:
                if bullet_rect.colliderect(obsplus.rect):
                    if obsplus.take_damage(players.gun.damage):
                        obsplus.kill()
                    
                    # 移除子弹
                    if bullet in players.gun.bullets:
                        players.gun.bullets.remove(bullet)
                    break
            
            for ice in icese:
                if bullet_rect.colliderect(ice.rect):
                    if ice.take_damage(players.gun.damage):
                        ice.kill()
                    # 移除子弹
                    if bullet in players.gun.bullets:
                        players.gun.bullets.remove(bullet)
                    break
    
    # 检测肥波与玩家的碰撞
    feibo_hits = pygame.sprite.spritecollide(players, feibos, False)
    feibo_damage1 = 25 if not is_tomato1 else 5
    feibo_damage2 = 25 if not is_tomato2 else 5
    for feibo in feibo_hits:
        # 肥波碰到玩家，玩家受到伤害（只在冷却结束后）
        if feibo.can_attack():
            if players == player:
                if is_plz1:
                    players.activate_boost()
                players.take_damage(feibo_damage1, players.rect.centerx, players.rect.top)
                feibo.reset_attack_cooldown()  # 重置冷却时间
            elif players == player2:
                if is_plz2:
                    players.activate_boost()
                players.take_damage(feibo_damage2, players.rect.centerx, players.rect.top)
                feibo.reset_attack_cooldown()  # 重置冷却时间
            else:
                players.take_damage(25, players.rect.centerx, players.rect.top)
                feibo.reset_attack_cooldown()  # 重置冷却时间

    
    # 检测孔畅帆
    kcf_hits = pygame.sprite.spritecollide(players,孔畅帆们,False)
    for hit in kcf_hits:
        if players == player:
            score += 75
            died_range = game_range + 1
        elif players == player2:
            score2 += 75
            player2_died_range = game_range + 1
        hit.kill()
    
    # 死亡检测

    if players.health <= 0 or (died_range == game_range or player2_died_range == game_range):
        if players == player:
            if died_range == game_range:
                if not is_player2:
                    root = tk.Tk()
                    root.withdraw()

                    # 直接显示错误弹窗
                    messagebox.showerror("方块吃方块"+version,f"Traceback (most recent call last):\n  File '{resource_path('main.py')}', line 1355, in <module>\n    if died_range == game_range:\n    ^^^^^^^^^^^^^^^^^^^\n孔畅帆Error: 方块吃方块.孔畅帆：\"下课去办公室！\"",icon=['warning'])
                    os._exit(-1)
                else:
                    if wait_for_key_press(window, f"{get_player_skin(1)["name"]}惨了!", "下课得去办公室！", 78, 78, GOLD, RED):
                        time.sleep(1)
                        score = 0
                        need_to_win = 150
                        game_range = 1
                        player.rect.x = win_kuan // 2
                        player.rect.y = win_gao // 2
                        player.health = player.max_health  # 重置血量
                        skin_image = None
                        if current_player_skin != "default":
                            skin_image = load_player_skin(current_player_skin)
                        player.set_skin(skin_image)
                        for bob in bombs:
                            bob.kill()

            else:
                if wait_for_key_press(window, f"{get_player_skin(1)["name"]}死了!", "按任意键复活", 78, 78, GOLD, GOLD):
                    time.sleep(1)
                    # 只重置玩家一的状态
                    score = 0
                    need_to_win = 150
                    player.rect.x = win_kuan // 2
                    player.rect.y = win_gao // 2
                    player.health = player.max_health  # 重置血量
                    skin_image = None
                    if current_player_skin != "default":
                        skin_image = load_player_skin(current_player_skin)
                    player.set_skin(skin_image)
                    for bob in bombs:
                        bob.kill()
        elif is_player2 and players == player2:
            if player2_died_range == game_range:
                if wait_for_key_press(window, f"{get_player_skin(2)["name"]}惨了!", "下课得去办公室！", 78, 78, GOLD, RED):
                    time.sleep(1)
                    # 只重置玩家二的状态
                    score2 = 0
                    player2_need_to_win = 150
                    player2.rect.x = win_kuan // 2
                    player2.rect.y = win_gao // 2
                    player2.health = player2.max_health  # 重置血量
                    skin_image2 = None
                    if current_player2_skin != "default":
                        skin_image2 = load_player_skin(current_player2_skin)
                    player2.set_skin(skin_image2)
                    for bob in bombs:
                        bob.kill()
            else:
                if wait_for_key_press(window, f"{get_player_skin(2)["name"]}死了!", "按任意键复活", 78, 78, GOLD, GOLD):
                    # 只重置玩家二的状态
                    time.sleep(1)
                    score2 = 0
                    player2_need_to_win = 150
                    player2.rect.x = win_kuan // 2
                    player2.rect.y = win_gao // 2
                    player2.health = player2.max_health  # 重置血量
                    for bob in bombs:
                        bob.kill()
        elif is_vsai and players == player_ai:
            if died_range == game_range:
                if wait_for_key_press(window, "AI惨了!", "但是下课去不了办公室！", 78, 78, GOLD, RED):
                    # 只重置AI的状态
                    score3 = 0
                    ai_need_to_win = 150
                    player_ai.rect.x = win_kuan // 2
                    player_ai.rect.y = win_gao // 2
                    player_ai.health = player_ai.max_health  # 重置血量
                    for bob in bombs:
                        bob.kill()
            else:
                if wait_for_key_press(window, "AI死了!", "按任意键复活", 78, 78, GOLD, GOLD):
                    # 只重置AI的状态
                    score3 = 0
                    ai_need_to_win = 150
                    player_ai.rect.x = win_kuan // 2
                    player_ai.rect.y = win_gao // 2
                    player_ai.health = player_ai.max_health  # 重置血量
                    for bob in bombs:
                        bob.kill()
def draw_health_bar(sprite, surface):
    """为精灵绘制血条 - 只在血量不满时显示"""
    if not hasattr(sprite, 'health') or not hasattr(sprite, 'max_health'):
        return
        
    # 只在血量不满时显示血条
    if sprite.health >= sprite.max_health:
        return
        
    bar_width = sprite.rect.width
    bar_height = 5
    bar_x = sprite.rect.x
    bar_y = sprite.rect.top - 10
    
    # 绘制血条背景
    pygame.draw.rect(surface, HEALTH_BG, (bar_x, bar_y, bar_width, bar_height))
    
    # 绘制当前血量
    health_width = int((sprite.health / sprite.max_health) * bar_width)
    health_color = HEALTH_GREEN if sprite.health > sprite.max_health * 0.3 else HEALTH_RED
    pygame.draw.rect(surface, health_color, (bar_x, bar_y, health_width, bar_height))
    
    # 绘制血条边框
    pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
def create_explosion(x, y):
    """创建爆炸特效"""
    # 创建爆炸粒子
    explosion_particles = []
    for _ in range(20):
        particle = {
            'x': x,
            'y': y,
            'dx': random.uniform(-5, 5),
            'dy': random.uniform(-5, 5),
            'radius': random.randint(3, 8),
            'color': (random.randint(200, 255), random.randint(100, 165), 0),
            'life': random.randint(20, 40)
        }
        explosion_particles.append(particle)
    
    # 返回粒子列表，需要在主循环中更新和绘制
    return explosion_particles

def update_explosions(explosions):
    """更新所有爆炸特效"""
    for explosion in explosions[:]:
        for particle in explosion[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            
            # 逐渐缩小粒子
            particle['radius'] = max(0, particle['radius'] - 0.1)
            
            # 移除生命结束的粒子
            if particle['life'] <= 0 or particle['radius'] <= 0:
                explosion.remove(particle)
        
        # 移除空的爆炸
        if not explosion:
            explosions.remove(explosion)

def draw_explosions(surface, explosions):
    """绘制所有爆炸特效"""
    for explosion in explosions:
        for particle in explosion:
            pygame.draw.circle(
                surface, 
                particle['color'], 
                (int(particle['x']), int(particle['y'])), 
                int(particle['radius'])
            )
def kill_sprite(sprite):
    """安全地移除精灵"""
    if sprite in all_sprites:
        all_sprites.remove(sprite)
    if sprite in obstacles:
        obstacles.remove(sprite)
    if sprite in speeds:
        speeds.remove(sprite)
    if sprite in needes:
        needes.remove(sprite)
    if sprite in slows:
        slows.remove(sprite)
    if sprite in obspluses:
        obspluses.remove(sprite)
    if sprite in bombs:
        bombs.remove(sprite)
    if sprite in icese:
        icese.remove(sprite)
    if sprite in feibos:
        feibos.remove(sprite)
    if sprite in 孔畅帆们:
        孔畅帆们.remove(sprite)
def update_visible_damage_numbers():
    """只更新屏幕内或活跃的伤害数字"""
    visible_rect = window.get_rect()
    
    # 障碍物伤害数字更新（只在需要时更新）
    for obstacle in obstacles:
        if visible_rect.colliderect(obstacle.rect):
            obstacle.update_damage_numbers()
    for speed in speeds:
        if visible_rect.colliderect(speed.rect):
            speed.update_damage_numbers()
    for need in needes:
        if visible_rect.colliderect(need.rect):
            need.update_damage_numbers()

    for slow in slows:
        if visible_rect.colliderect(slow.rect):
            slow.update_damage_numbers()
    for obsplus in obspluses:
        if visible_rect.colliderect(obsplus.rect):
            obsplus.update_damage_numbers()

    for bomb in bombs:
        if visible_rect.colliderect(bomb.rect):
            bomb.update_damage_numbers()
    for ice in icese:
        if visible_rect.colliderect(ice.rect):
            ice.update_damage_numbers()

    for feibo in feibos:
        if visible_rect.colliderect(feibo.rect):
            feibo.update_damage_numbers()

    for kcf in 孔畅帆们:
        if visible_rect.colliderect(kcf.rect):
            kcf.update_damage_numbers()
def draw_visible_health_bars(surface):
    """只绘制可见区域内且需要显示血条的方块"""
    visible_rect = surface.get_rect()
    
    # 只绘制屏幕内且血量不满的方块
    for obstacle in obstacles:
        if visible_rect.colliderect(obstacle.rect) and obstacle.health < obstacle.max_health:
            draw_health_bar(obstacle, surface)
    
    for speed in speeds:
        if visible_rect.colliderect(speed.rect) and speed.health < speed.max_health:
            draw_health_bar(speed, surface)
    
    for need in needes:
        if visible_rect.colliderect(need.rect) and need.health < need.max_health:
            draw_health_bar(need, surface)
    
    for slow in slows:
        if visible_rect.colliderect(slow.rect) and slow.health < slow.max_health:
            draw_health_bar(slow, surface)
    
    for obsplus in obspluses:
        if visible_rect.colliderect(obsplus.rect) and obsplus.health < obsplus.max_health:
            draw_health_bar(obsplus, surface)
    
    for bomb in bombs:
        if visible_rect.colliderect(bomb.rect) and bomb.health < bomb.max_health:
            draw_health_bar(bomb, surface)
    
    for ice in icese:
        if visible_rect.colliderect(ice.rect) and ice.health < ice.max_health:
            draw_health_bar(ice, surface)
    
    for feibo in feibos:
        if visible_rect.colliderect(feibo.rect) and feibo.health < feibo.max_health:
            draw_health_bar(feibo, surface)
    
    for kcf in 孔畅帆们:
        if visible_rect.colliderect(kcf.rect) and kcf.health < kcf.max_health:
            draw_health_bar(kcf, surface)
def draw_visible_damage_numbers(surface):
    """只绘制可见区域内的伤害数字"""
    visible_rect = surface.get_rect()
    
    # 绘制屏幕内方块的伤害数字
    for obstacle in obstacles:
        if visible_rect.colliderect(obstacle.rect):
            obstacle.draw_damage_numbers(surface)
    
    for speed in speeds:
        if visible_rect.colliderect(speed.rect):
            speed.draw_damage_numbers(surface)
    
    for need in needes:
        if visible_rect.colliderect(need.rect):
            need.draw_damage_numbers(surface)
    
    for slow in slows:
        if visible_rect.colliderect(slow.rect):
            slow.draw_damage_numbers(surface)
    
    for obsplus in obspluses:
        if visible_rect.colliderect(obsplus.rect):
            obsplus.draw_damage_numbers(surface)
    
    for bomb in bombs:
        if visible_rect.colliderect(bomb.rect):
            bomb.draw_damage_numbers(surface)
    
    for ice in icese:
        if visible_rect.colliderect(ice.rect):
            ice.draw_damage_numbers(surface)
    
    for feibo in feibos:
        if visible_rect.colliderect(feibo.rect):
            feibo.draw_damage_numbers(surface)
    
    for kcf in 孔畅帆们:
        if visible_rect.colliderect(kcf.rect):
            kcf.draw_damage_numbers(surface)    
def update_visible_damage_numbers_optimized():

    """优化版：只更新屏幕内或活跃的伤害数字"""
    visible_rect = window.get_rect()
    
    # 批量更新，减少函数调用
    for group in [obstacles, speeds, needes, slows, obspluses, bombs, icese, feibos, 孔畅帆们]:
        for sprite in group:
            if visible_rect.colliderect(sprite.rect):
                # 简化的更新逻辑
                for damage_num in sprite.damage_numbers[:]:
                    damage_num['x'] += damage_num.get('velocity_x', 0)
                    damage_num['y'] += damage_num.get('velocity_y', 0)
                    damage_num['life'] -= 1
                    
                    if damage_num['life'] <= 0:
                        sprite.damage_numbers.remove(damage_num)
def get_player_skin(player_num=1):
    """
    获取玩家当前使用的皮肤信息
    参数:
        player_num: 玩家编号 (1=玩家一, 2=玩家二)
    返回:
        字典包含皮肤ID和显示名称
    """
    available_skins = get_available_skins()
    
    if player_num == 1:
        skin_id = current_player_skin
    elif player_num == 2:
        skin_id = current_player2_skin
    else:
        return None
    
    display_name = available_skins.get(skin_id, "未知皮肤")
    
    return {
        'id': skin_id,
        'name': display_name,
        'is_default': skin_id == "default"
    }
def get_all_player_skins():
    """
    获取所有玩家的皮肤信息
    返回:
        包含玩家一和玩家二皮肤信息的字典
    """
    return {
        'player1': get_player_skin(1),
        'player2': get_player_skin(2)
    }
def print_current_skins():
    """打印当前玩家皮肤信息（用于调试）"""
    player1_skin = get_player_skin(1)
    player2_skin = get_player_skin(2)
    
    print("=== 当前玩家皮肤 ===")
    print(f"玩家一: {player1_skin['name']} (ID: {player1_skin['id']})")
    print(f"玩家二: {player2_skin['name']} (ID: {player2_skin['id']})")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
GOLD = (255, 215, 0)
YELLOW = (255, 255, 0)
ICE = (173, 216, 230)
FOREST = (34, 139, 34)
HEALTH_RED = (220, 60, 60)      # 血条红色
HEALTH_GREEN = (60, 220, 60)    # 血条绿色
HEALTH_BG = (40, 40, 40)        # 血条背景色
DAMAGE_COLOR = (255, 100, 100)  # 伤害数字颜色
HEAL_GREEN = (100, 255, 100)    # 治疗数字颜色
FEIBO_COLOR = (139, 69, 19)     # 肥波颜色
SWORD_COLOR = (200, 200, 200)   # 剑颜色
BULLET_COLOR = (255, 255, 0)    # 子弹颜色
EXPLOSION_COLOR = (255, 165, 0) # 爆炸颜色
SETTINGS_BG = (30, 30, 40)      # 设置菜单背景色
SLIDER_COLOR = (100, 100, 200)  # 滑块颜色
SLIDER_HANDLE = (200, 200, 255) # 滑块手柄颜色

# 全局变量
fullscreen = False
music_volume = 0.25
melee_enabled = True
ranged_enabled = True
player1_keys = {
    'left': pygame.K_a,
    'right': pygame.K_d,
    'up': pygame.K_w,
    'down': pygame.K_s,
    'sword': pygame.K_e,
    'gun': pygame.K_q,
    'attack': pygame.K_TAB,
    'dash': pygame.K_LALT  
}

player2_keys = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'sword': pygame.K_QUOTE,  # 引号键
    'gun': pygame.K_BACKSLASH,  # 反斜杠键
    'attack': pygame.K_DELETE,
    'dash': pygame.K_RALT  # Delete键
}

# 当前键位配置（初始化为默认值）
current_player1_keys = player1_keys.copy()
current_player2_keys = player2_keys.copy()

# 键位显示名称映射
key_names = {
    pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D", pygame.K_e: "E",
    pygame.K_f: "F", pygame.K_g: "G", pygame.K_h: "H", pygame.K_i: "I", pygame.K_j: "J",
    pygame.K_k: "K", pygame.K_l: "L", pygame.K_m: "M", pygame.K_n: "N", pygame.K_o: "O",
    pygame.K_p: "P", pygame.K_q: "Q", pygame.K_r: "R", pygame.K_s: "S", pygame.K_t: "T",
    pygame.K_u: "U", pygame.K_v: "V", pygame.K_w: "W", pygame.K_x: "X", pygame.K_y: "Y",
    pygame.K_z: "Z", pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3",
    pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8",
    pygame.K_9: "9", pygame.K_LEFT: "←", pygame.K_RIGHT: "→", pygame.K_UP: "↑", 
    pygame.K_DOWN: "↓", pygame.K_SPACE: "空格", pygame.K_LSHIFT: "左Shift", 
    pygame.K_RSHIFT: "右Shift", pygame.K_LCTRL: "左Ctrl", pygame.K_RCTRL: "右Ctrl",
    pygame.K_LALT: "左Alt", pygame.K_RALT: "右Alt", pygame.K_TAB: "Tab", 
    pygame.K_CAPSLOCK: "CapsLock", pygame.K_ESCAPE: "Esc", pygame.K_RETURN: "回车",
    pygame.K_BACKSPACE: "退格", pygame.K_INSERT: "Insert", pygame.K_DELETE: "Delete",
    pygame.K_HOME: "Home", pygame.K_END: "End", pygame.K_PAGEUP: "PageUp", 
    pygame.K_PAGEDOWN: "PageDown", pygame.K_QUOTE: "引号", pygame.K_BACKSLASH: "反斜杠",
    pygame.K_SEMICOLON: "分号", pygame.K_EQUALS: "等号", pygame.K_COMMA: "逗号",
    pygame.K_PERIOD: "句号", pygame.K_SLASH: "斜杠", pygame.K_LEFTBRACKET: "左括号",
    pygame.K_RIGHTBRACKET: "右括号", pygame.K_BACKQUOTE: "反引号",
    'mouse_left': "鼠标左键", 'mouse_right': "鼠标右键", 'mouse_middle': "鼠标中键"
}
# 初始化资源路径
font_path = resource_path("assets\\msyh.ttc")
win_sound_path = resource_path("assets\\win_sound.mp3")
music_path = resource_path("assets\\music.mp3")
ico_path = resource_path("assets\\ico.ico")
feibo_path = resource_path("assets\\Feibo.jpg")
sword_path = resource_path("assets\\sword.png")
ak47_path = resource_path("assets\\ak47.png")
孔畅帆_path = resource_path("assets\\孔畅帆.png")
# 设置DEBUG模式
DEBUG = not (is_pyinstaller_bundle() or is_nuitka_bundle())
# 加载图标和音乐
try:
    icon = pygame.image.load(ico_path)
    pygame.mixer.music.load(music_path)
    sound = pygame.mixer.Sound(win_sound_path)
except Exception as e:
    print(f"资源加载错误: {e}")
    # 创建空的Sound对象避免崩溃
    sound = pygame.mixer.Sound(buffer=bytearray())

# 初始化游戏
clock = pygame.time.Clock()
win_kuan, win_gao = 1280, 720
window = pygame.display.set_mode((win_kuan, win_gao))
pygame.display.set_caption("方块吃方块"+version)
pygame.display.set_icon(icon)

def toggle_fullscreen():
    """切换全屏模式"""
    global fullscreen, window
    fullscreen = not fullscreen
    if fullscreen:
        window = pygame.display.set_mode((win_kuan, win_gao), pygame.FULLSCREEN)
    else:
        window = pygame.display.set_mode((win_kuan, win_gao))
    # 确保窗口标题和图标也被设置
    pygame.display.set_caption("方块吃方块"+version)
    pygame.display.set_icon(icon)
    return window


class BasePlayer(pygame.sprite.Sprite):
    """玩家基类，包含所有玩家的通用功能"""
    def __init__(self, color, player_num=1):
        """初始化玩家"""
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (win_kuan // 2, win_gao // 2)
        
        # 基础速度设置
        self.base_normal_speed = 4
        self.normal_speed = self.base_normal_speed
        self.speed = self.normal_speed
        
        self.boosted = False
        self.boost_start_time = 0
        self.boost_duration = 3000
        self.slowed = False
        self.slowly_start_time = 0
        self.slowly_duration = 5000
        self.icely_start_time = 0
        self.icely_duration = 5000
        self.iced = False
        self.player_num = player_num
        self.original_color = color
        
        # 新增血量属性
        self.max_health = 100
        self.health = self.max_health
        self.damage_numbers = []
        self.heal_numbers = []
        
        # 添加武器系统
        self.sword = Sword(self)
        self.gun = Gun(self)
        self.equipped_weapon = None
        self.attack_cooldown = 0
        
        # 保存原始图像（用于状态效果叠加）
        self.original_image = self.image.copy()
        self.current_skin = None  # 当前使用的皮肤
        # 冲刺功能
        self.dash_speed = 15  # 冲刺速度
        self.dash_duration = 10  # 冲刺持续时间（帧数）
        self.dash_cooldown = 60  # 冲刺冷却时间（帧数）
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.is_dashing = False
        self.dash_direction = (0, 0)
        
        # 苏少羽英雄标识
        self.is_sushaoyu = False
        
    def update(self, keys=None, events=None):
        """更新玩家状态和位置"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        # 检查各种状态效果是否过期
        current_time = pygame.time.get_ticks()
        need_score1 = 50 if not is_maomao1 else 25
        need_score2 = 50 if not is_maomao2 else 25
        # 重置速度到基础速度
        if not self.iced and not self.slowed and not self.boosted:
            self.speed = self.normal_speed
        
        # 加速效果过期检查
        if self.boosted and current_time - self.boost_start_time > self.boost_duration:
            if not self.slowed and not self.iced:
                self.speed = self.normal_speed
                self.boosted = False
                self._update_appearance()
        
        # 减速效果过期检查
        if self.slowed and current_time - self.slowly_start_time > self.slowly_duration:
            if not self.iced:
                self.speed = self.normal_speed
                self.slowed = False
                self._update_appearance()
        
        # 冰冻效果过期检查
        if self.iced and current_time - self.icely_start_time > self.icely_duration:
            self.speed = self.normal_speed
            self.iced = False
            self._update_appearance()
        
        # 如果没有状态效果，设置基础速度
        if not self.iced and not self.slowed and not self.boosted:
            self.speed = self.normal_speed
        
        # 更新冲刺状态
        self._update_dash()
        
        # 处理键盘输入 - 武器切换、攻击和冲刺
        if keys is not None:
            # 根据玩家编号使用对应的键位配置
            if self.player_num == 1:
                keys_config = current_player1_keys
            else:
                keys_config = current_player2_keys
                
            # 冲刺功能（苏少羽英雄专属）
            if (self.is_sushaoyu and 
                keys[keys_config.get('dash', pygame.K_LALT if self.player_num == 1 else pygame.K_RALT)] and 
                self.dash_cooldown_timer <= 0 and 
                not self.is_dashing):
                self.activate_dash()
                
            # 武器切换
            if keys[keys_config['sword']] and melee_enabled:
                if self.player_num == 1 and score >= need_score1:
                    self.equip_sword()
                elif self.player_num == 2 and score2 >= need_score2:
                    self.equip_sword()
                    
            if keys[keys_config['gun']] and ranged_enabled:
                if self.player_num == 1 and score >= need_score1:
                    self.equip_gun()
                elif self.player_num == 2 and score2 >= need_score2:
                    self.equip_gun()
            
            # 移动控制
            if keys[keys_config['left']]:
                self.rect.x -= self.speed
            if keys[keys_config['right']]:
                self.rect.x += self.speed
            if keys[keys_config['up']]:
                self.rect.y -= self.speed
            if keys[keys_config['down']]:
                self.rect.y += self.speed

        # 处理攻击输入（需要事件处理）
        if events is not None:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    # 统一处理玩家一和玩家二的键盘攻击
                    keys_config = current_player1_keys if self.player_num == 1 else current_player2_keys
                    if event.key == keys_config['attack']:
                        self.attack()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 只处理玩家一的鼠标攻击
                    if self.player_num == 1:
                        keys_config = current_player1_keys
                        # 检查鼠标攻击键配置
                        if keys_config['attack'] == 'mouse_left' and event.button == 1:
                            self.attack()
                        elif keys_config['attack'] == 'mouse_middle' and event.button == 2:
                            self.attack()
                        elif keys_config['attack'] == 'mouse_right' and event.button == 3:
                            self.attack()

        # 确保玩家在屏幕边界内
        self.rect.x = max(0, min(self.rect.x, win_kuan - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, win_gao - self.rect.height))
        
        # 更新冲刺冷却计时器
        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= 1
    def _update_appearance(self):
        """更新玩家外观，处理皮肤和状态效果的叠加"""
        # 如果有皮肤，使用皮肤
        if self.current_skin:
            self.image = self.current_skin.copy()
        else:
            # 否则使用默认颜色
            self.image = pygame.Surface((50, 50))
            self.image.fill(self.original_color)
        
        # 如果有状态效果，添加颜色叠加
        if self.boosted:
            # 创建金色叠加层
            overlay = pygame.Surface((50, 50), pygame.SRCALPHA)
            overlay.fill((255, 215, 0, 100))  # 半透明金色
            self.image.blit(overlay, (0, 0))
        elif self.slowed:
            # 创建黑色叠加层
            overlay = pygame.Surface((50, 50), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))  # 半透明黑色
            self.image.blit(overlay, (0, 0))
        elif self.iced:
            # 创建冰蓝色叠加层
            overlay = pygame.Surface((50, 50), pygame.SRCALPHA)
            overlay.fill((173, 216, 230, 150))  # 半透明冰蓝色
            self.image.blit(overlay, (0, 0))
    
    def _update_dash(self):
        """更新冲刺状态"""
        if self.is_dashing:
            self.dash_timer -= 1
            
            # 应用冲刺移动（忽略边界检查）
            new_x = self.rect.x + self.dash_direction[0] * self.dash_speed
            new_y = self.rect.y + self.dash_direction[1] * self.dash_speed
            
            # 冲刺时允许稍微超出边界
            self.rect.x = max(-10, min(new_x, win_kuan - self.rect.width + 10))
            self.rect.y = max(-10, min(new_y, win_gao - self.rect.height + 10))
            
            # 冲刺结束
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.dash_cooldown_timer = self.dash_cooldown
                
    def activate_dash(self):
        """激活冲刺"""
        if not self.is_sushaoyu or self.dash_cooldown_timer > 0 or self.is_dashing:
            return False
            
        # 获取鼠标位置计算冲刺方向
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        distance = max(1, (dx**2 + dy**2)**0.5)
        
        # 标准化方向
        self.dash_direction = (dx / distance, dy / distance)
        self.is_dashing = True
        self.dash_timer = self.dash_duration
        
        # 添加冲刺视觉效果
        self._add_dash_effect()
        return True
        
    def _add_dash_effect(self):
        """添加冲刺视觉效果"""
        global dash_particles
        # 创建冲刺粒子效果
        for _ in range(10):
            particle = {
                'x': self.rect.centerx,
                'y': self.rect.centery,
                'dx': -self.dash_direction[0] * random.uniform(2, 5),
                'dy': -self.dash_direction[1] * random.uniform(2, 5),
                'radius': random.randint(2, 4),
                'color': (255, 255, 200),
                'life': 15
            }
            # 添加到全局粒子效果列表（需要在游戏主循环中处理）
            dash_particles.append(particle)
    
    def set_skin(self, skin_image):
        """设置玩家皮肤"""
        if skin_image:
            self.current_skin = skin_image.copy()
        else:
            self.current_skin = None
            
        # 检查是否是苏少羽英雄
        skin_info = get_player_skin(self.player_num)
        self.is_sushaoyu = (skin_info and skin_info['id'] == "5.png")
        
        self._update_appearance()
    
    def activate_boost(self):
        """激活加速效果"""
        self.speed = self.normal_speed * 2
        self.boosted = True
        self.boost_start_time = pygame.time.get_ticks()
        self._update_appearance()
        
    def activate_slowly(self):
        """激活减速效果"""
        self.speed = self.normal_speed // 2
        self.slowed = True
        self.slowly_start_time = pygame.time.get_ticks()
        self._update_appearance()
        
    def activate_ice(self):
        """激活冰冻效果"""
        self.speed = 0
        self.iced = True
        self.icely_start_time = pygame.time.get_ticks()
        self._update_appearance()    
    def take_damage(self, damage, x, y):
        """受到伤害并创建伤害数字"""
        self.health = max(0, self.health - damage)
        
        # 创建伤害数字
        damage_number = {
            'value': damage,
            'x': x,
            'y': y,
            'velocity_x': random.uniform(-2, 2),  # 随机水平速度
            'velocity_y': -4,  # 初始向上速度
            'gravity': 0.1,    # 重力加速度
            'life': 90,        # 生命周期（帧数）
            'alpha': 255,      # 透明度
            'type': 'damage'   # 类型：伤害
        }
        self.damage_numbers.append(damage_number)
        
    def heal(self, amount, x, y):
        """治疗并创建治疗数字"""
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        actual_heal = self.health - old_health  # 实际治疗量（考虑血量上限）
        
        if actual_heal > 0:
            # 创建治疗数字
            heal_number = {
                'value': actual_heal,
                'x': x,
                'y': y,
                'velocity_x': random.uniform(-4, 4),  # 随机水平速度
                'velocity_y': -4,  # 初始向上速度
                'gravity': 0.1,    # 重力加速度
                'life': 90,        # 生命周期（帧数）
                'alpha': 255,      # 透明度
                'type': 'heal'     # 类型：治疗
            }
            self.heal_numbers.append(heal_number)
            
    def update_damage_numbers(self):
        """更新伤害和治疗数字的位置和状态"""
        # 更新伤害数字
        for damage_num in self.damage_numbers[:]:
            # 更新水平位置
            damage_num['x'] += damage_num['velocity_x']
            
            # 应用重力
            damage_num['velocity_y'] += damage_num['gravity']
            damage_num['y'] += damage_num['velocity_y']
            
            # 减少生命周期
            damage_num['life'] -= 1
            
            # 逐渐淡出
            if damage_num['life'] < 30:
                damage_num['alpha'] = max(0, damage_num['alpha'] - 8)
            
            # 移除过期伤害数字
            if damage_num['life'] <= 0 or damage_num['alpha'] <= 0:
                self.damage_numbers.remove(damage_num)
        
        # 更新治疗数字
        for heal_num in self.heal_numbers[:]:
            # 更新水平位置
            heal_num['x'] += heal_num['velocity_x']
            
            # 应用重力
            heal_num['velocity_y'] += heal_num['gravity']
            heal_num['y'] += heal_num['velocity_y']
            
            # 减少生命周期
            heal_num['life'] -= 1
            
            # 逐渐淡出
            if heal_num['life'] < 30:
                heal_num['alpha'] = max(0, heal_num['alpha'] - 8)
            
            # 移除过期治疗数字
            if heal_num['life'] <= 0 or heal_num['alpha'] <= 0:
                self.heal_numbers.remove(heal_num)        
                
    def draw_damage_numbers(self, surface):
        """绘制伤害和治疗数字"""
        damage_font = pygame.font.Font(font_path, 45)
        
        # 绘制伤害数字
        for damage_num in self.damage_numbers:
            # 创建带透明度的文本表面
            text_surface = damage_font.render(f"-{damage_num['value']}", True, DAMAGE_COLOR)
            text_surface.set_alpha(damage_num['alpha'])
            
            # 绘制文本
            text_rect = text_surface.get_rect(center=(damage_num['x'], damage_num['y']))
            surface.blit(text_surface, text_rect)
        
        # 绘制治疗数字
        for heal_num in self.heal_numbers:
            # 创建带透明度的文本表面
            text_surface = damage_font.render(f"+{heal_num['value']}", True, HEAL_GREEN)
            text_surface.set_alpha(heal_num['alpha'])
            
            # 绘制文本
            text_rect = text_surface.get_rect(center=(heal_num['x'], heal_num['y']))
            surface.blit(text_surface, text_rect)
            
    def draw_health_bar(self, surface):
        """在玩家头上绘制血条"""
        bar_width = 60
        bar_height = 8
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 15

        # 绘制血条背景
        pygame.draw.rect(surface, HEALTH_BG, (bar_x, bar_y, bar_width, bar_height))

        # 绘制当前血量
        health_width = int((self.health / self.max_health) * bar_width)
        health_color = HEALTH_GREEN if self.health > self.max_health * 0.3 else HEALTH_RED
        pygame.draw.rect(surface, health_color, (bar_x, bar_y, health_width, bar_height))

        # 绘制血条边框
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        
# 在 BasePlayer 类的 equip_sword 和 equip_gun 方法中，修改分数扣除逻辑：

    def equip_sword(self):
        """装备近战武器"""
        global score, score2, score3, is_maomao1, is_maomao2
        need_score1 = 50 if not is_maomao1 else 25
        need_score2 = 50 if not is_maomao2 else 25
        if self.equipped_weapon != 'sword':
            # 检查对应玩家的分数是否足够
            if self == player and score >= need_score1:
                # 如果之前装备了枪，先卸下
                if self.equipped_weapon == 'gun':
                    self.unequip_weapon()
                
                score -= need_score1
                self.equipped_weapon = 'sword'
                self.sword.active = True
                return True
            elif is_player2 and self == player2 and score2 >= need_score2:
                # 如果之前装备了枪，先卸下
                if self.equipped_weapon == 'gun':
                    self.unequip_weapon()
                
                score2 -= need_score2
                self.equipped_weapon = 'sword'
                self.sword.active = True
                return True
            elif is_vsai and self == player_ai and score3 >= 50:
                # 如果之前装备了枪，先卸下
                if self.equipped_weapon == 'gun':
                    self.unequip_weapon()
                
                score3 -= 50
                self.equipped_weapon = 'sword'
                self.sword.active = True
                return True
        elif self.equipped_weapon == 'sword':
            # 如果已经装备了剑，卸下
            self.unequip_weapon()
            return True
        return False
        
    def equip_gun(self):
        """装备远程武器"""
        global score, score2, score3
        need_score1 = 100 if not is_maomao1 else 50
        need_score2 = 100 if not is_maomao2 else 50
        if self.equipped_weapon != 'gun':
            # 检查对应玩家的分数是否足够
            if self == player and score >= need_score1:
                # 如果之前装备了剑，先卸下
                if self.equipped_weapon == 'sword':
                    self.unequip_weapon()
                
                score -= 100
                self.equipped_weapon = 'gun'
                self.gun.active = True
                return True
            elif is_player2 and self == player2 and score2 >= need_score2:
                # 如果之前装备了剑，先卸下
                if self.equipped_weapon == 'sword':
                    self.unequip_weapon()
                
                score2 -= 100
                self.equipped_weapon = 'gun'
                self.gun.active = True
                return True
            elif is_vsai and self == player_ai and score3 >= 100:
                # 如果之前装备了剑，先卸下
                if self.equipped_weapon == 'sword':
                    self.unequip_weapon()
                
                score3 -= 100
                self.equipped_weapon = 'gun'
                self.gun.active = True
                return True
        elif self.equipped_weapon == 'gun':
            # 如果已经装备了枪，卸下
            self.unequip_weapon()
            return True
        return False
    def unequip_weapon(self):
        """卸下当前武器"""
        if self.equipped_weapon == 'sword':
            self.sword.active = False
        elif self.equipped_weapon == 'gun':
            self.gun.active = False
            self.gun.bullets.clear()  # 清除所有子弹
        self.equipped_weapon = None
        
    def attack(self):
        """使用当前装备的武器攻击"""
        print(f"玩家{self.player_num} 尝试攻击，冷却: {self.attack_cooldown}")  # 调试信息
        
        if self.attack_cooldown > 0:
            print(f"玩家{self.player_num} 攻击冷却中")  # 调试信息
            return False
            
        result = False
        if self.equipped_weapon == 'sword':
            result = self.sword.attack()
            if result:
                self.attack_cooldown = 10  # 玩家攻击冷却
                print(f"玩家{self.player_num} 剑攻击成功")  # 调试信息
        elif self.equipped_weapon == 'gun':
            result = self.gun.shoot()
            if result:
                self.attack_cooldown = 15  # 玩家攻击冷却
                print(f"玩家{self.player_num} 枪射击成功")  # 调试信息
        else:
            print(f"玩家{self.player_num} 未装备武器")  # 调试信息
            
        return result
    def draw_weapons(self, surface):
        """绘制武器"""
        if self.equipped_weapon == 'sword' and self.sword.active:
            surface.blit(self.sword.image, self.sword.rect)
            self.sword.draw_attack_effect(surface)
            
        if self.equipped_weapon == 'gun' and self.gun.active:
            surface.blit(self.gun.image, self.gun.rect)
            self.gun.draw_bullets(surface)

class Player(BasePlayer):
    """玩家一，使用WASD控制"""
    def __init__(self):
        # 先调用父类初始化
        super().__init__(GREEN, 1)
        
        # 加载选择的贴图
        skin_image = None
        if current_player_skin != "default":
            skin_image = load_player_skin(current_player_skin)
        
        # 设置皮肤
        self.set_skin(skin_image)
class Player2(BasePlayer):
    """玩家二，使用方向键控制"""
    def __init__(self):
        super().__init__(FOREST, 2)
        
        # 加载选择的贴图
        skin_image = None
        if current_player2_skin != "default":
            skin_image = load_player_skin(current_player2_skin, 2)
        
        # 设置皮肤
        self.set_skin(skin_image)
class Player_AI(BasePlayer):
    """AI玩家，由AI控制器控制"""
    def __init__(self):
        super().__init__(FOREST)
        # AI玩家不需要控制键

class Sword(pygame.sprite.Sprite):
    """近战武器 - 修复版"""
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.orbit_radius = 60  # 轨道半径
        self.orbit_speed = 15   # 增加轨道速度，使攻击更快
        self.current_angle = 0  # 当前角度
        self.damage = 10         # 伤害值
        self.active = False
        self.is_attacking = False
        self.attack_angle = 0   # 攻击方向角度
        self.attack_range = 80  # 攻击范围
        self.attack_cooldown = 0  # 攻击冷却
        
        try:
            # 加载剑贴图并放大到64x64
            original_image = pygame.image.load(sword_path)
            # 创建原始图像副本用于旋转
            self.original_image = pygame.transform.scale(original_image, (64, 64))
            self.image = self.original_image.copy()
        except:
            # 如果加载失败，使用颜色方块
            self.original_image = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.polygon(self.original_image, SWORD_COLOR, [
                (32, 0), (64, 32), (32, 64), (0, 32)
            ])
            self.image = self.original_image.copy()
        
        self.rect = self.image.get_rect()
        self.update_position()
        
    def update_position(self):
        """更新剑的位置，使其围绕玩家旋转"""
        if not self.active:
            return
            
        # 更新攻击冷却
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # 如果正在攻击，剑围绕玩家旋转
        if self.is_attacking:
            self.current_angle += self.orbit_speed
                
            # 如果旋转完成一圈，停止攻击
            if self.current_angle >= self.attack_angle + 360:
                self.current_angle = self.attack_angle
                self.is_attacking = False
                self.attack_cooldown = 20  # 攻击冷却
        else:
            # 获取鼠标位置
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # 计算玩家到鼠标的方向
            dx = mouse_x - self.player.rect.centerx
            dy = mouse_y - self.player.rect.centery
            distance = max(1, (dx**2 + dy**2)**0.5)
            
            # 标准化方向向量
            dx = dx / distance
            dy = dy / distance
            
            # 计算攻击角度
            self.attack_angle = math.degrees(math.atan2(dy, dx))
            
            # 设置剑的角度与鼠标方向一致
            self.current_angle = self.attack_angle
        
        # 计算剑在轨道上的位置
        angle_rad = math.radians(self.current_angle)
        self.rect.centerx = self.player.rect.centerx + math.cos(angle_rad) * self.orbit_radius
        self.rect.centery = self.player.rect.centery + math.sin(angle_rad) * self.orbit_radius
        
        # 旋转剑图像
        self.image = pygame.transform.rotate(self.original_image, -self.current_angle)
        self.rect = self.image.get_rect(center=self.rect.center)            
    def update(self):
        """更新剑的状态"""
        self.update_position()
        
    def attack(self):
        """开始攻击"""
        if not self.is_attacking and self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 60  # 攻击后冷却1秒（60帧）
            print(f"剑攻击开始，冷却时间: {self.attack_cooldown}")  # 调试信息
            return True
        else:
            print(f"剑攻击失败 - 正在攻击: {self.is_attacking}, 冷却: {self.attack_cooldown}")  # 调试信息
            return False
    def get_attack_range(self):
        """获取攻击范围（圆形）"""
        return pygame.Rect(
            self.rect.centerx - 40, 
            self.rect.centery - 40, 
            80, 80
        )        
    def detect_collisions(self):
        """检测剑与物体的碰撞"""
        if not self.is_attacking:
            return
            
        sword_range = self.get_attack_range()
        
        # 统一的碰撞检测逻辑
        targets = [
            (obstacles, 10),
            (speeds, 10),
            (needes, 10),
            (slows, 10),
            (obspluses, 10),
            (bombs, 15),
            (icese, 10),
            (feibos, 10),
            (孔畅帆们, 10),
            (xiongers, 10)
        ]
        
        for target_group, damage in targets:
            for target in target_group:
                if sword_range.colliderect(target.rect):
                    if target.take_damage(damage):
                        target.kill()
    def draw_attack_effect(self, surface):
        """绘制攻击特效"""
        if self.is_attacking:
            # 绘制攻击范围指示器
            attack_range_rect = self.get_attack_range()
            pygame.draw.rect(surface, (255, 255, 0, 50), attack_range_rect, 2)
            
            # 绘制攻击轨迹
            center_x, center_y = self.player.rect.center
            for angle in range(0, 360, 45):  # 每45度绘制一个点
                rad = math.radians(angle)
                x = center_x + math.cos(rad) * self.orbit_radius
                y = center_y + math.sin(rad) * self.orbit_radius
                pygame.draw.circle(surface, (255, 255, 0), (int(x), int(y)), 3)
class Gun(pygame.sprite.Sprite):
    """远程武器 - 修复版"""
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.attack_distance = 50  # 攻击距离
        self.damage = 10            # 伤害值
        self.active = False
        self.bullets = []          # 子弹列表
        
        try:
            # 加载AK47贴图
            original_image = pygame.image.load(ak47_path)
            # 创建原始图像副本用于旋转
            self.original_image = pygame.transform.scale(original_image, (60, 30))
            # 水平翻转图像修复枪口方向
            self.original_image = pygame.transform.flip(self.original_image, True, False)
            self.image = self.original_image.copy()
        except:
            # 如果加载失败，使用颜色方块
            self.original_image = pygame.Surface((60, 30))
            self.original_image.fill((100, 100, 100))
            self.image = self.original_image.copy()
        
        self.rect = self.image.get_rect()
        self.update_position()
        
    def update_position(self):
        """更新枪的位置"""
        if not self.active:
            return
            
        # 获取鼠标位置
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # 计算玩家到鼠标的方向
        dx = mouse_x - self.player.rect.centerx
        dy = mouse_y - self.player.rect.centery
        distance = max(1, (dx**2 + dy**2)**0.5)
        
        # 标准化方向向量
        dx = dx / distance
        dy = dy / distance
        
        # 计算枪的位置（在玩家周围的圆形上）
        self.rect.centerx = self.player.rect.centerx + dx * self.attack_distance
        self.rect.centery = self.player.rect.centery + dy * self.attack_distance
        
        # 计算攻击角度
        angle = math.degrees(math.atan2(dy, dx))
        
        # 旋转枪图像
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)
            
    def update(self):
        """更新枪的状态"""
        # 更新子弹位置
        for bullet in self.bullets[:]:
            bullet['x'] += bullet['dx'] * 10
            bullet['y'] += bullet['dy'] * 10
            bullet['life'] -= 1
            
            # 移除超出生命周期的子弹
            if bullet['life'] <= 0:
                self.bullets.remove(bullet)
                
        self.update_position()
    def draw_bullets(self, surface):
        """绘制子弹"""
        for bullet in self.bullets:
            # 绘制子弹（放大显示）
            pygame.draw.circle(surface, BULLET_COLOR, 
                            (int(bullet['x']), int(bullet['y'])), 8)    
    def shoot(self):
        """发射子弹"""
        if not self.active:
            print("枪未激活")  # 调试信息
            return False
            
        # 限制子弹数量防止卡顿
        if len(self.bullets) >= 10:
            print("子弹数量已达上限")  # 调试信息
            return False
            
        # 获取鼠标位置
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.player.rect.centerx
        dy = mouse_y - self.player.rect.centery
        distance = max(1, (dx**2 + dy**2)**0.5)
        
        # 标准化方向向量
        dx = dx / distance
        dy = dy / distance
        
        # 发射子弹
        self.bullets.append({
            'x': self.rect.centerx,
            'y': self.rect.centery,
            'dx': dx,
            'dy': dy,
            'life': 60  # 子弹生命周期
        })
        print(f"发射子弹，当前子弹数: {len(self.bullets)}")  # 调试信息
        return True
class Obstacle(pygame.sprite.Sprite):
    """障碍物类"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(win_kuan - self.rect.width)
        self.rect.y = random.randrange(win_gao - self.rect.height)
        
        # 添加血量属性
        self.health = 10
        self.max_health = 10
        
        # 添加伤害数字
        self.damage_numbers = []
    def kill(self):
        """安全地移除障碍物"""
        kill_sprite(self)
        super().kill()
        
    def take_damage(self, damage):
        """障碍物受到伤害"""
        self.health -= damage
        return self.health <= 0
        

# 为其他所有方块类也添加相同的方法（Speed, Needs, Slows, ObsPlus, Bomb, Ice, Feibo, 孔畅帆Obs）
# 这里以Feibo为例，其他类也需要添加相同的方法
class Feibo(pygame.sprite.Sprite):
    """肥波追杀者"""
    def __init__(self):
        super().__init__()
        try: 
            # 加载贴图并缩放到50x50
            original_image = pygame.image.load(feibo_path)
            self.image = pygame.transform.scale(original_image, (50, 50))
        except:
            # 如果加载失败，使用颜色方块
            self.image = pygame.Surface((50, 50))
            self.image.fill(FEIBO_COLOR)
        
        self.rect = self.image.get_rect()
        # 初始位置随机
        self.rect.x = random.randrange(win_kuan - self.rect.width)
        self.rect.y = random.randrange(win_gao - self.rect.height)
        
        
        self.speed = 2
        
        # 添加攻击冷却时间
        self.attack_cooldown = 0
        self.attack_cooldown_max = 60  # 1秒冷却时间（60帧）
        
        # 添加血量系统
        self.health = 50
        self.max_health = 50
        
        # 添加伤害数字
        self.damage_numbers = []
    def kill(self):
        """安全地移除障碍物"""
        kill_sprite(self)
        super().kill()
        
# 修改肥波的update方法
    def update(self, players):
        """更新肥波位置，追踪最近的玩家"""
        # 更新攻击冷却
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        
        # 找到最近的玩家
        nearest_player = None
        min_distance = float('inf')
        
        # 确保players是一个列表，即使只有一个玩家
        if not isinstance(players, list):
            players_list = [players] if players else []
        else:
            players_list = players
        
        for player in players_list:
            if hasattr(player, 'health') and player.health > 0:  # 只追踪活着的玩家
                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery
                distance = (dx**2 + dy**2)**0.5
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_player = player
        
        if nearest_player:
            # 向最近玩家移动
            dx = nearest_player.rect.centerx - self.rect.centerx
            dy = nearest_player.rect.centery - self.rect.centery
            distance = max(1, (dx**2 + dy**2)**0.5)
            
            # 标准化方向向量
            dx = dx / distance
            dy = dy / distance
            
            # 移动肥波
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            
            # 确保肥波在屏幕边界内
            self.rect.x = max(0, min(self.rect.x, win_kuan - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, win_gao - self.rect.height))
        else:
            # 如果没有活着的玩家，随机移动
            if random.random() < 0.02:  # 2%的几率改变方向
                self.random_dx = random.uniform(-1, 1)
                self.random_dy = random.uniform(-1, 1)
                
            self.rect.x += self.random_dx * self.speed
            self.rect.y += self.random_dy * self.speed
            
            # 确保肥波在屏幕边界内
            self.rect.x = max(0, min(self.rect.x, win_kuan - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, win_gao - self.rect.height))
            
            # 如果碰到边界，改变方向
            if self.rect.x <= 0 or self.rect.x >= win_kuan - self.rect.width:
                self.random_dx = -self.random_dx
            if self.rect.y <= 0 or self.rect.y >= win_gao - self.rect.height:
                self.random_dy = -self.random_dy            
    def can_attack(self):
        """检查肥波是否可以攻击"""
        return self.attack_cooldown <= 0
        
    def reset_attack_cooldown(self):
        """重置攻击冷却时间"""
        self.attack_cooldown = self.attack_cooldown_max
        
    def take_damage(self, damage):
        """肥波受到伤害"""
        self.health -= damage
        return self.health <= 0
        
class Speed(pygame.sprite.Sprite):
    """加速道具类"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 45))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(win_kuan - self.rect.width)
        self.rect.y = random.randrange(win_gao - self.rect.height)
        
        # 添加血量属性
        self.health = 10
        self.max_health = 10
        # 添加伤害数字
        self.damage_numbers = []
        
    def take_damage(self, damage):
        """障碍物受到伤害"""
        self.health -= damage
        return self.health <= 0
        

class Needs(pygame.sprite.Sprite):
    """需求道具类"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 45))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(win_kuan - self.rect.width)
        self.rect.y = random.randrange(win_gao - self.rect.height)
        
        # 添加血量属性
        self.health = 10
        self.max_health = 10
        # 添加伤害数字
        self.damage_numbers = []
    def kill(self):
        """安全地移除障碍物"""
        kill_sprite(self)
        super().kill()
        
    def take_damage(self, damage):
        """障碍物受到伤害"""
        self.health -= damage
        return self.health <= 0
        

class Slows(pygame.sprite.Sprite):
    """减速道具类"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(win_kuan - self.rect.width)
        self.rect.y = random.randrange(win_gao - self.rect.height)
        
        # 添加血量属性
        self.health = 10
        self.max_health = 10
        # 添加伤害数字
        self.damage_numbers = []
    def kill(self):
        """安全地移除障碍物"""
        kill_sprite(self)
        super().kill()
        
    def take_damage(self, damage):
        """障碍物受到伤害"""
        self.health -= damage
        return self.health <= 0
        
class ObsPlus(pygame.sprite.Sprite):
    """加强障碍物类"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(win_kuan - self.rect.width)
        self.rect.y = random.randrange(win_gao - self.rect.height)
        
        # 添加血量属性
        self.health = 20
        self.max_health = 20
        # 添加伤害数字
        self.damage_numbers = []
    def kill(self):
        """安全地移除障碍物"""
        kill_sprite(self)
        super().kill()
        
    def take_damage(self, damage):
        """障碍物受到伤害"""
        self.health -= damage
        return self.health <= 0
        
class Bomb(pygame.sprite.Sprite):
    """炸弹类"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK, (25, 25), 25)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(win_kuan - self.rect.width)
        self.rect.y = random.randrange(win_gao - self.rect.height)
        
        # 添加血量属性
        self.health = 15
        self.max_health = 15
        # 添加伤害数字
        self.damage_numbers = []
    def kill(self):
        """安全地移除障碍物"""
        kill_sprite(self)
        super().kill()
        
    def take_damage(self, damage):
        """障碍物受到伤害"""
        self.health -= damage
        return self.health <= 0
        
class Ice(pygame.sprite.Sprite):
    """冰冻道具类"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 45))
        self.image.fill(ICE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(win_kuan - self.rect.width)
        self.rect.y = random.randrange(win_gao - self.rect.height)
        
        # 添加血量属性
        self.health = 10
        self.max_health = 10
        # 添加伤害数字
        self.damage_numbers = []
    def kill(self):
        """安全地移除障碍物"""
        kill_sprite(self)
        super().kill()
        
    def take_damage(self, damage):
        """障碍物受到伤害"""
        self.health -= damage
        return self.health <= 0
        
class 孔畅帆Obs(pygame.sprite.Sprite):
    """孔畅帆 - 迫真"""
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(孔畅帆_path)
        except:
            self.image = pygame.Surface((50, 50))
            self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(win_kuan - self.rect.width)
        self.rect.y = random.randrange(win_gao - self.rect.height)
        
        # 添加血量属性
        self.health = 30
        self.max_health = 30
        # 添加伤害数字
        self.damage_numbers = []
    def kill(self):
        """安全地移除障碍物"""
        kill_sprite(self)
        super().kill()
        
    def take_damage(self, damage):
        """障碍物受到伤害"""
        self.health -= damage
        return self.health <= 0
class 熊二_Obs(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(resource_path("assets\\Player\\8.png"))
            self.image = pygame.transform.scale(self.image,(50,50))
        except:
            self.image = pygame.Surface((50,50))
            self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(win_kuan - self.rect.width)
        self.rect.y = random.randrange(win_gao - self.rect.height)
        
        # 添加血量属性
        self.health = 30
        self.max_health = 30
         # 添加伤害数字
        self.damage_numbers = []
    def kill(self):
        """安全地移除障碍物"""
        kill_sprite(self)
        super().kill()
        
    def take_damage(self, damage):
        """障碍物受到伤害"""
        self.health -= damage
        return self.health <= 0 
class 蜂蜜(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(resource_path("assets\\蜂蜜.png"))
            self.image = pygame.transform.scale(self.image,(50,50))
        except:
            self.image = pygame.Surface((50,50))
            self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(win_kuan - self.rect.width)
        self.rect.y = random.randrange(win_gao - self.rect.height)
        
        # 添加血量属性
        self.health = 30
        self.max_health = 30
         # 添加伤害数字
        self.damage_numbers = []
    def kill(self):
        """安全地移除障碍物"""
        kill_sprite(self)
        super().kill()
        
    def take_damage(self, damage):
        """障碍物受到伤害"""
        self.health -= damage
        return self.health <= 0             
# AI控制器类（简化版）
class AIController:
    """AI控制器，控制AI玩家的行为"""
    def __init__(self, player_ai, obstacles, speeds, needes, slows, obspluses, bombs, icese):
        """
        初始化AI控制器
        参数:
            player_ai: AI玩家实例
            obstacles: 障碍物精灵组
            speeds: 加速道具精灵组
            needes: 需求道具精灵组
            slows: 减速道具精灵组
            obspluses: 加强障碍物精灵组
            bombs: 炸弹精灵组
            icese: 冰冻道具精灵组
        """
        self.player = player_ai
        self.obstacles = obstacles
        self.speeds = speeds
        self.needes = needes
        self.slows = slows
        self.obspluses = obspluses
        self.bombs = bombs
        self.icese = icese
        # AI状态变量
        self.target = None
        self.target_type = None
        self.safe_distance = 80
        self.stuck_timer = 0
        self.last_position = (player_ai.rect.x, player_ai.rect.y)
        self.no_safe_target_counter = 0
        self.emergency_mode = False
        self.emergency_timer = 0
        self.last_safe_direction = (0, 0)
        # 振荡检测
        self.oscillation_timer = 0
        self.oscillation_positions = []
        self.oscillation_threshold = 20
        self.teleport_cooldown = 0
        # 安全参数
        self.boundary_margin = 50
        self.bomb_danger_radius = 120
        self.bomb_critical_radius = 80
    def update(self):
        """更新AI行为"""
        if self.player.iced:
            return
        # 更新冷却时间
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= 1
        # 更新AI速度
        self.speed = self.player.speed
        # 振荡检测
        self._detect_oscillation_improved()
        # 如果检测到振荡且冷却结束，传送到中心
        if (self.oscillation_timer > self.oscillation_threshold and 
            self.teleport_cooldown == 0 and 
            self._is_trapped_by_bombs()):
            self._teleport_to_center()
            return
        # 检查是否卡住
        current_pos = (self.player.rect.x, self.player.rect.y)
        if current_pos == self.last_position:
            self.stuck_timer += 1
        else:
            self.stuck_timer = 0
        self.last_position = current_pos
        # 如果卡住超过1秒，进入紧急模式
        if self.stuck_timer > 60:
            self.emergency_mode = True
            self.emergency_timer = 90
            self.stuck_timer = 0
        # 处理紧急模式
        if self.emergency_mode:
            self.emergency_timer -= 1
            if self.emergency_timer <= 0:
                self.emergency_mode = False
            else:
                self._emergency_move()
                return
        # 检查紧急避障
        emergency_bomb = self._find_emergency_bomb()
        if emergency_bomb:
            self._emergency_avoid(emergency_bomb)
            return
        # 寻找目标并移动
        self._find_and_move_to_target()
        # 边界检查
        self._enforce_boundaries()
    def _detect_oscillation_improved(self):
        """改进的振荡检测"""
        current_pos = (self.player.rect.x, self.player.rect.y)
        # 记录位置和移动模式
        self.oscillation_positions.append({
            'pos': current_pos,
            'time': pygame.time.get_ticks()
        })
        # 只保留最近1秒内的位置数据
        current_time = pygame.time.get_ticks()
        self.oscillation_positions = [
            p for p in self.oscillation_positions 
            if current_time - p['time'] < 1000
        ]
        # 如果有足够的数据点，分析移动模式
        if len(self.oscillation_positions) >= 10:
            # 计算移动范围
            positions = [p['pos'] for p in self.oscillation_positions]
            min_x = min(pos[0] for pos in positions)
            max_x = max(pos[0] for pos in positions)
            min_y = min(pos[1] for pos in positions)
            max_y = max(pos[1] for pos in positions)
            range_x = max_x - min_x
            range_y = max_y - min_y
            # 计算移动距离
            total_distance = 0
            for i in range(1, len(positions)):
                dx = positions[i][0] - positions[i-1][0]
                dy = positions[i][1] - positions[i-1][1]
                total_distance += (dx**2 + dy**2)**0.5
            # 计算净移动距离（从起点到终点的距离）
            net_distance = ((positions[-1][0] - positions[0][0])**2 + 
                           (positions[-1][1] - positions[0][1])**2)**0.5
            # 计算效率比（净移动/总移动）
            if total_distance > 0:
                efficiency_ratio = net_distance / total_distance
            else:
                efficiency_ratio = 0
            # 检测真正的振荡：移动范围小且效率低
            is_oscillating = (
                range_x < 40 and
                range_y < 40 and
                efficiency_ratio < 0.3 and
                total_distance > 50
            )
            # 检测周期性模式
            has_periodic_pattern = self._detect_periodic_pattern(positions)
            # 真正的振荡：小范围低效率移动或有周期性模式
            if (is_oscillating or has_periodic_pattern) and self._is_trapped_by_bombs():
                self.oscillation_timer += 1
            else:
                self.oscillation_timer = max(0, self.oscillation_timer - 2)
        else:
            self.oscillation_timer = max(0, self.oscillation_timer - 1)
    def _detect_periodic_pattern(self, positions):
        """检测周期性移动模式"""
        if len(positions) < 8:
            return False
        # 将位置四舍五入到网格，减少微小变化的干扰
        grid_size = 10
        grid_positions = [
            (round(x / grid_size) * grid_size, round(y / grid_size) * grid_size)
            for x, y in positions
        ]
        # 计算唯一位置数量
        unique_positions = len(set(grid_positions))
        # 如果AI只在很少的几个点之间移动（2-3个），可能是周期性抽搐
        if unique_positions <= 3:
            # 检查这些点是否很接近
            if unique_positions > 1:
                # 计算所有点之间的最大距离
                max_distance = 0
                for i in range(unique_positions):
                    for j in range(i+1, unique_positions):
                        pos1 = list(set(grid_positions))[i]
                        pos2 = list(set(grid_positions))[j]
                        distance = ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5
                        max_distance = max(max_distance, distance)
                # 如果所有点都在小范围内，认为是周期性抽搐
                if max_distance < 60:
                    return True
        return False
    def _is_trapped_by_bombs(self):
        """检查是否被炸弹困住"""
        if len(self.bombs) < 2:
            return False
        # 计算附近的炸弹数量
        nearby_bombs = 0
        for bomb in self.bombs:
            dx = bomb.rect.centerx - self.player.rect.centerx
            dy = bomb.rect.centery - self.player.rect.centery
            distance = (dx**2 + dy**2)**0.5
            if distance < 100:
                nearby_bombs += 1
        # 如果有2个或更多炸弹在附近，且它们形成夹击之势
        if nearby_bombs >= 2:
            # 检查炸弹是否在玩家两侧
            left_bombs = 0
            right_bombs = 0
            top_bombs = 0
            bottom_bombs = 0
            for bomb in self.bombs:
                dx = bomb.rect.centerx - self.player.rect.centerx
                dy = bomb.rect.centery - self.player.rect.centery
                distance = (dx**2 + dy**2)**0.5
                if distance < 100:
                    if dx < -30:
                        left_bombs += 1
                    elif dx > 30:
                        right_bombs += 1
                        
                    if dy < -30:
                        top_bombs += 1
                    elif dy > 30:
                        bottom_bombs += 1
            # 如果炸弹在两侧形成夹击，认为被困住
            if (left_bombs >= 1 and right_bombs >= 1) or (top_bombs >= 1 and bottom_bombs >= 1):
                return True
        return False
    def _teleport_to_center(self):
        """传送到窗口中心"""
        # 传送到中心
        self.player.rect.centerx = win_kuan // 2
        self.player.rect.centery = win_gao // 2
        # 重置状态
        self.oscillation_timer = 0
        self.oscillation_positions = []
        self.emergency_mode = False
        self.stuck_timer = 0
        self.target = None
        # 设置传送冷却时间（5秒）
        self.teleport_cooldown = 300
        # 清除所有状态效果
        self.player.boosted = False
        self.player.slowed = False
        self.player.iced = False
        self.player.speed = self.player.normal_speed
        self.player.image.fill(FOREST)
    def _find_emergency_bomb(self):
        """寻找需要紧急避开的炸弹"""
        for bomb in self.bombs:
            dx = bomb.rect.centerx - self.player.rect.centerx
            dy = bomb.rect.centery - self.player.rect.centery
            distance = (dx**2 + dy**2)**0.5
            if distance < self.bomb_critical_radius:
                return bomb
        return None
    def _emergency_avoid(self, bomb):
        """紧急避开炸弹"""
        dx = self.player.rect.centerx - bomb.rect.centerx
        dy = self.player.rect.centery - bomb.rect.centery
        distance = max(1, (dx**2 + dy**2)**0.5)
        dx = dx / distance * self.speed * 1.5
        dy = dy / distance * self.speed * 1.5
        safe_dx, safe_dy = self._adjust_direction_for_other_bombs(dx, dy)
        self.player.rect.x += safe_dx
        self.player.rect.y += safe_dy
        self.last_safe_direction = (safe_dx, safe_dy)
    def _emergency_move(self):
        """紧急移动模式"""
        directions = [
            (self.speed, 0),
            (-self.speed, 0),
            (0, self.speed),
            (0, -self.speed),
            (self.speed * 0.7, self.speed * 0.7),
            (self.speed * 0.7, -self.speed * 0.7),
            (-self.speed * 0.7, self.speed * 0.7),
            (-self.speed * 0.7, -self.speed * 0.7),
        ]
        if self.last_safe_direction != (0, 0):
            directions.insert(0, self.last_safe_direction)
        for dx, dy in directions:
            if self._is_move_safe(self.player.rect.x + dx, self.player.rect.y + dy):
                self.player.rect.x += dx
                self.player.rect.y += dy
                self.last_safe_direction = (dx, dy)
                return
        # 如果所有方向都不安全，尝试向中心移动
        center_x, center_y = win_kuan // 2, win_gao // 2
        dx = center_x - self.player.rect.centerx
        dy = center_y - self.player.rect.centery
        distance = max(1, (dx**2 + dy**2)**0.5)
        dx = dx / distance * self.speed
        dy = dy / distance * self.speed
        self.player.rect.x += dx
        self.player.rect.y += dy
    def _find_and_move_to_target(self):
        """寻找目标并移动到目标"""
        self.target, self.target_type = self._find_best_target()
        if not self.target:
            self.no_safe_target_counter += 1
            
            if self.no_safe_target_counter > 30:
                self._move_to_safe_area()
            return
        self.no_safe_target_counter = 0
        dx = self.target.rect.centerx - self.player.rect.centerx
        dy = self.target.rect.centery - self.player.rect.centery
        distance = max(1, (dx**2 + dy**2)**0.5)
        dx = dx / distance
        dy = dy / distance
        if self._is_direct_path_safe(dx, dy, distance):
            self.player.rect.x += dx * self.speed
            self.player.rect.y += dy * self.speed
        else:
            self._move_around_obstacles(dx, dy)
    def _is_direct_path_safe(self, dx, dy, distance):
        """检查直接路径是否安全"""
    # 如果速度为0，直接返回False（无法移动）
        if self.speed <= 0:
            return False
        # 确保不会除以0
        if self.speed == 0:
            return False
        steps = max(1, int(distance / self.speed))  # 至少1步
        for i in range(1, steps + 1):
            check_x = self.player.rect.centerx + dx * self.speed * i
            check_y = self.player.rect.centery + dy * self.speed * i
            for bomb in self.bombs:
                bomb_distance = ((bomb.rect.centerx - check_x) ** 2 + 
                                (bomb.rect.centery - check_y) ** 2) ** 0.5
                if bomb_distance < self.bomb_danger_radius:
                    return False
        return True
    def _move_around_obstacles(self, target_dx, target_dy):
        """绕过障碍物移动"""
        directions = []
        # 生成多个可能的方向
        for angle in [-45, 45, -90, 90, -135, 135]:
            rad = math.radians(angle)
            cos_a = math.cos(rad)
            sin_a = math.sin(rad)
            rotated_dx = target_dx * cos_a - target_dy * sin_a
            rotated_dy = target_dx * sin_a + target_dy * cos_a
            directions.append((rotated_dx, rotated_dy))
        # 添加一些随机方向
        for _ in range(4):
            angle = random.uniform(0, 2 * math.pi)
            directions.append((math.cos(angle), math.sin(angle)))
        # 寻找最佳方向
        best_dx, best_dy = 0, 0
        best_score = -float('inf')
        for dx, dy in directions:
            if dx == 0 and dy == 0:
                continue
            length = max(0.001, (dx**2 + dy**2)**0.5)
            dx = dx / length
            dy = dy / length
            new_x = self.player.rect.x + dx * self.speed
            new_y = self.player.rect.y + dy * self.speed
            safety_score = self._calculate_position_safety(new_x, new_y)
            target_score = (dx * target_dx + dy * target_dy) * 0.5
            total_score = safety_score + target_score
            if total_score > best_score and safety_score > 0:
                best_score = total_score
                best_dx, best_dy = dx, dy
        if best_score > -float('inf'):
            self.player.rect.x += best_dx * self.speed
            self.player.rect.y += best_dy * self.speed
            self.last_safe_direction = (best_dx * self.speed, best_dy * self.speed)
        else:
            self._move_to_safe_area()
    def _move_to_safe_area(self):
        """移动到安全区域"""
        safe_x, safe_y = self._find_safe_position()
        dx = safe_x - self.player.rect.centerx
        dy = safe_y - self.player.rect.centery
        distance = max(1, (dx**2 + dy**2)**0.5)
        dx = dx / distance * self.speed
        dy = dy / distance * self.speed
        if self._is_move_safe(self.player.rect.x + dx, self.player.rect.y + dy):
            self.player.rect.x += dx
            self.player.rect.y += dy
            self.last_safe_direction = (dx, dy)
        else:
            self.emergency_mode = True
            self.emergency_timer = 60
    def _find_safe_position(self):
        """寻找安全位置"""
        candidates = [
            (win_kuan // 2, win_gao // 2),  # 中心
            (self.boundary_margin, self.boundary_margin),  # 左上角
            (win_kuan - self.boundary_margin, self.boundary_margin),  # 右上角
            (self.boundary_margin, win_gao - self.boundary_margin),  # 左下角
            (win_kuan - self.boundary_margin, win_gao - self.boundary_margin),  # 右下角
        ]
        # 添加一些随机位置
        for _ in range(5):
            candidates.append((
                random.randint(self.boundary_margin, win_kuan - self.boundary_margin),
                random.randint(self.boundary_margin, win_gao - self.boundary_margin)
            ))
        # 寻找最安全的位置
        safest_pos = candidates[0]
        best_safety = -float('inf')
        for pos in candidates:
            safety = self._calculate_position_safety(pos[0], pos[1])
            if safety > best_safety:
                best_safety = safety
                safest_pos = pos
        return safest_pos
    def _calculate_position_safety(self, x, y):
        """计算位置的安全性评分"""
        safety_score = 0
        # 边界安全性
        border_x = min(x, win_kuan - x)
        border_y = min(y, win_gao - y)
        border_safety = min(border_x, border_y) / 100
        safety_score += border_safety
        # 炸弹安全性
        for bomb in self.bombs:
            dx = bomb.rect.centerx - x
            dy = bomb.rect.centery - y
            distance = (dx**2 + dy**2)**0.5
            if distance < self.bomb_critical_radius:
                safety_score -= 100
            elif distance < self.bomb_danger_radius:
                safety_score -= (self.bomb_danger_radius - distance) / 10
            else:
                safety_score += 1
        return safety_score
    def _adjust_direction_for_other_bombs(self, dx, dy):
        """调整方向以避免其他炸弹"""
        new_dx, new_dy = dx, dy
        for bomb in self.bombs:
            bomb_dx = bomb.rect.centerx - self.player.rect.centerx
            bomb_dy = bomb.rect.centery - self.player.rect.centery
            bomb_distance = (bomb_dx**2 + bomb_dy**2)**0.5
            if bomb_distance < self.bomb_danger_radius:
                dot_product = (dx * bomb_dx + dy * bomb_dy) / (max(0.001, (dx**2 + dy**2)**0.5) * bomb_distance)
                if dot_product > 0.7:
                    # 计算垂直方向
                    perpendicular_dx = -dy
                    perpendicular_dy = dx
                    perpendicular_dot = (perpendicular_dx * bomb_dx + perpendicular_dy * bomb_dy) / bomb_distance
                    if perpendicular_dot > 0:
                        new_dx, new_dy = perpendicular_dx, perpendicular_dy
                    else:
                        new_dx, new_dy = -perpendicular_dx, -perpendicular_dy
                    length = max(0.001, (new_dx**2 + new_dy**2)**0.5)
                    new_dx = new_dx / length * self.speed
                    new_dy = new_dy / length * self.speed
                    break
        return new_dx, new_dy
    def _is_move_safe(self, new_x, new_y):
        """检查移动是否安全"""
        # 边界检查
        if (new_x < 0 or new_x > win_kuan - self.player.rect.width or
            new_y < 0 or new_y > win_gao - self.player.rect.height):
            return False
        # 炸弹检查
        for bomb in self.bombs:
            dx = bomb.rect.centerx - (new_x + self.player.rect.width // 2)
            dy = bomb.rect.centery - (new_y + self.player.rect.height // 2)
            distance = (dx**2 + dy**2)**0.5
            if distance < self.safe_distance:
                return False
        return True
    def _enforce_boundaries(self):
        """确保AI在边界内"""
        self.player.rect.x = max(0, min(self.player.rect.x, win_kuan - self.player.rect.width))
        self.player.rect.y = max(0, min(self.player.rect.y, win_gao - self.player.rect.height))
    def _find_best_target(self):
        """寻找最佳目标"""
        all_targets = []
        # 定义目标类型和优先级
        target_groups = [
            (list(self.obstacles), "obstacle", 100),
            (list(self.speeds), "speed", 200),
            (list(self.obspluses), "obsplus", 150),
            (list(self.needes), "need", 1),
            (list(self.slows), "slow", 5),
            (list(self.icese), "ice", 1)
        ]
        for target_list, target_type, base_priority in target_groups:
            for target in target_list:
                if self._is_target_safe(target):
                    distance = self._calculate_distance(target)
                    priority = base_priority / (distance + 1)
                    all_targets.append((target, target_type, priority))
        if not all_targets:
            return None, None
        # 返回优先级最高的目标
        best_target = max(all_targets, key=lambda x: x[2])
        return best_target[0], best_target[1]
    def _is_target_safe(self, target):
        """检查目标是否安全"""
        bomb_count = 0
        for bomb in self.bombs:
            dx = bomb.rect.centerx - target.rect.centerx
            dy = bomb.rect.centery - target.rect.centery
            distance = (dx**2 + dy**2)**0.5
            if distance < self.bomb_danger_radius:
                bomb_count += 1
                if bomb_count >= 2:
                    return False
        return True
    def _calculate_distance(self, target):
        """计算到目标的距离"""
        dx = target.rect.centerx - self.player.rect.centerx
        dy = target.rect.centery - self.player.rect.centery
        return (dx**2 + dy**2)**0.5

# 游戏主循环
running = True
in_game = False  # 标记是否在游戏中
dash_particles = []
while running:
    # 显示主菜单
    menu_choice = main_menu()
    
    if menu_choice == 1:  # 退出游戏
        running = False
        break
    elif menu_choice == 0:  # 开始游戏
        # 重置游戏状态
        # 创建精灵组
        all_sprites = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        speeds = pygame.sprite.Group()
        needes = pygame.sprite.Group()
        slows = pygame.sprite.Group()
        obspluses = pygame.sprite.Group()
        bombs = pygame.sprite.Group()
        icese = pygame.sprite.Group()
        孔畅帆们 = pygame.sprite.Group()
        feibos = pygame.sprite.Group()
        xiongers = pygame.sprite.Group()
        fengmis = pygame.sprite.Group()
        # 创建玩家
        player = Player()
        all_sprites.add(player)
        skin_image = None
        if current_player_skin != "default":
            skin_image = load_player_skin(current_player_skin)
        player.set_skin(skin_image)
        # 游戏变量初始化
        game_range = 1
        score = 0
        score2 = 0
        score3 = 0
        need_to_win = 150
        player2_need_to_win = 150
        ai_need_to_win = 150
        font = pygame.font.Font(font_path, 50)
        
        # 初始化玩家变量（防止未定义错误）
        player2 = None
        player_ai = None
        ai_controller = None
        
        # 爆炸特效
        explosions = []
        
        # 显示模式选择菜单
        user_choose = mode_select_menu(window)
        
        # 根据用户选择设置游戏模式
        if user_choose == 0:
            is_vsai = False
            is_player2 = False
        elif user_choose == 1:
            is_vsai = False
            is_player2 = True
        elif user_choose == 3:
            is_player2 = False
            is_vsai = True
        elif user_choose == 4:
            continue  # 返回主菜单
        if not skin_selection_menu(is_start_menu=True):
    # 如果英雄选择菜单返回False（比如用户关闭窗口），则退出游戏
            running = False
            break
        # 显示制作组信息
        window.fill(BLACK)
        makers = starter_menu(window, [
            'BY 西岗中学七年八班:齐博文[CORE DEV]王昊然[音乐]Deepseek-r1[技术支持]',
            "肥波[贡献]宋辰皓[吉祥物]孔畅帆[贡献]杨铭俊[贡献]许恒志[贡献]",
            "满俊臣[贡献]苏帅宇[贡献]王昊然[贡献]任雅琪[贡献]",
            "还有玩家们！"
        ], [36, 36, 36], GOLD, choose=False)
        if makers != 5:
            continue  # 返回主菜单
        
        window.fill(BLACK)
        ming_ju = starter_menu(window,["黑发不知勤学早,",
                                       "               我越不学我越屌",
                                       "                      --孔畅帆《赠七八班》"],[50,50,36],(255,255,255),False)
        if ming_ju != 5:
            continue  # 返回主菜单
        # 根据游戏模式初始化游戏元素
        game_by_block = 1
        is_maomao1 = True if get_player_skin(1)['id'] == "1.png" else False
        is_maomao2 = True if get_player_skin(2)['id'] == "1.png" else False
        is_plz1 = True if get_player_skin(1)['id'] == "3.png" else False
        is_plz2 = True if get_player_skin(2)['id'] == "3.png" else False
        is_xiongda1 = True if get_player_skin(1)['id'] == "2.png" else False
        is_xiongda2 = True if get_player_skin(2)['id'] == "2.png" else False
        is_weidai1 = True if get_player_skin(1)["id"] == "6.png" else False
        is_weidai2 = True if get_player_skin(2)["id"] == "6.png" else False
        is_xionger1 = True if get_player_skin(1)["id"] == "8.png" else False
        is_xionger2 = True if get_player_skin(2)["id"] == "8.png" else False
        is_tomato1 = True if get_player_skin(1)["id"] == "4.png" else False
        is_tomato2 = True if get_player_skin(2)["id"] == "4.png" else False
        is_yaoming1 = True if get_player_skin(1)["id"] == "0.png" else False
        game_by_block = game_by_block + 1 if is_yaoming1 else game_by_block
        is_yaoming2 = True if get_player_skin(2)["id"] == "0.png" else False
        game_by_block = game_by_block + 1 if is_yaoming2 else game_by_block
        is_jiban = True if (is_xiongda1 and is_xionger2 and is_player2) or (is_xionger1 and is_xiongda2 and is_player2) else False
        player.normal_speed = 4 if not is_yaoming1 else 2
        player.normal_speed = player.normal_speed if not is_xiongda1 else 3
        player.normal_speed = player.normal_speed if not is_jiban else 8
        player.max_health = 100 if not is_weidai1 else 300
        player.max_health = player.max_health if not is_xiongda1 else 150
        player.health = player.max_health
        if is_player2:
            player.normal_speed = 4 if not is_yaoming1 else 2
            player.normal_speed = player.normal_speed if not is_xiongda1 else 3
            player.normal_speed = player.normal_speed if not is_jiban else 8
            player.max_health = 100 if not is_weidai1 else 300
            player.max_health = player.max_health if not is_xiongda1 else 150
            player.health = player.max_health
            player2 = Player2()
            player2.normal_speed = 4 if not is_yaoming2 else 2
            player2.normal_speed = player2.normal_speed if not is_xiongda2 else 3
            player2.normal_speed = player2.normal_speed if not is_jiban else 8
            player2.max_health = 100 if not is_weidai2 else 300
            player2.max_health = player2.max_health if not is_xiongda2 else 150
            player2.health = player2.max_health
            all_sprites.add(player2)
            skin_image2 = None
            if current_player2_skin != "default":
                skin_image2 = load_player_skin(current_player2_skin)
            player2.set_skin(skin_image2)
            for i in range(20*game_by_block):
                obstacle = generate_non_overlapping_position(Obstacle, bombs)
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
        elif is_vsai:
            player_ai = Player_AI()
            all_sprites.add(player_ai)
            ai_controller = AIController(player_ai, obstacles, speeds, needes, slows, obspluses, bombs, icese)
            for i in range(20*game_by_block):
                obstacle = generate_non_overlapping_position(Obstacle, bombs)
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
        else:
            for i in range(15*game_by_block):
                obstacle = generate_non_overlapping_position(Obstacle, bombs)
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
        
        # 播放背景音乐
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)
        
        rect = [(0,win_kuan//2),(50,win_kuan//2),(100,win_kuan//2),(150,win_kuan//2),(200,win_kuan//2),(250,win_kuan//20),(300,win_kuan//2),(350,win_kuan//2),(400,win_kuan//2),(500,win_kuan//2)]
        max_fps = 60
        # 游戏内循环
        in_game = True
        while in_game and running:
            clock.tick(max_fps)
            keys = pygame.key.get_pressed()
            events = pygame.event.get()
            fps = clock.get_fps()
            if not is_vsai:
                player.update(keys, events)  # 传递events参数
                if is_player2:
                    player2.update(keys, events)  # 传递events参数
            else:
                player.update(keys, events)  # 传递events参数
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    in_game = False
                elif event.type == pygame.KEYDOWN:
                    # 空格键暂停游戏
                    if event.key == pygame.K_SPACE:
                        pause_result = wait_for_key_press(window, "游戏暂停", "按任意键继续", 78, 78, GOLD, GOLD, show_main_menu_button=True)
                        if pause_result == 2:  # 返回主界面
                            in_game = False
                            pygame.mixer.music.stop()
                            break
                        elif not pause_result:  # 关闭窗口
                            running = False
                            in_game = False
                            break
                    
                    # 玩家一攻击键
                    if event.key == current_player1_keys['attack']:
                        print("玩家一攻击键按下")  # 调试信息
                        player.attack()
                    
                    # 玩家二攻击键
                    if is_player2 and event.key == current_player2_keys['attack']:
                        print("玩家二攻击键按下")  # 调试信息
                        player2.attack()
                    
                    # F11切换全屏
                    elif event.key == pygame.K_F11:
                        toggle_fullscreen()
                        window = pygame.display.get_surface()  # 更新窗口引用
                    
                    # ESC键退出游戏
                    elif event.key == pygame.K_ESCAPE:
                        if not DEBUG:
                            pause_result = wait_for_key_press(window, "游戏暂停", "按任意键继续", 78, 78, GOLD, GOLD, show_main_menu_button=True)
                            if pause_result == 2:  # 返回主界面
                                in_game = False
                                pygame.mixer.music.stop()
                                break
                            elif not pause_result:  # 关闭窗口
                                running = False
                                in_game = False
                                break
                        else:
                            running = False
                            in_game = False
                            break
                
                # 鼠标点击攻击（玩家一）
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 检查是否是玩家一的攻击鼠标键
                    mouse_attack = False
                    if current_player1_keys['attack'] == 'mouse_left' and event.button == 1:
                        mouse_attack = True
                    elif current_player1_keys['attack'] == 'mouse_middle' and event.button == 2:
                        mouse_attack = True
                    elif current_player1_keys['attack'] == 'mouse_right' and event.button == 3:
                        mouse_attack = True
                        
                    if mouse_attack and not player.iced:
                        print("玩家一鼠标攻击")  # 调试信息
                        player.attack()
                    
                    # 调试功能 - 中键生成炸弹
                    elif event.button == 2 and DEBUG:
                        bomb = generate_non_overlapping_position(Bomb, bombs)
                        all_sprites.add(bomb)
                        bombs.add(bomb)
            if not in_game:  # 如果退出游戏内循环，回到主菜单
                break
    

                # AI玩家更新
            if is_vsai:
                player_ai.update(keys)
                ai_controller.update()
            
            # 胜利条件检查
            if score >= need_to_win:
                try:
                    pygame.mixer.music.stop()
                    sound.play()
                except:
                    pass
                if not is_player2:
                    if wait_for_key_press(window, "你赢了!", f"您最终得分{score}!", 100, 100, GOLD, GOLD):
                        time.sleep(2)
                        skin_image = None
                        if current_player_skin != "default":
                            skin_image = load_player_skin(current_player_skin)
                        player.set_skin(skin_image)
                        in_game = False
                    else:
                        in_game = False
                else:
                    if wait_for_key_press(window, f"{get_player_skin(1)['name']}赢了!", f"以{score}的成绩胜过{get_player_skin(2)['name']}!", 100, 100, GOLD, GOLD):
                        time.sleep(2)
                        skin_image = None
                        if current_player_skin != "default":
                            skin_image = load_player_skin(current_player_skin)
                        player.set_skin(skin_image)
                        in_game = False
                    else:
                        time.sleep(2)
                        in_game = False
            
            if is_player2 and score2 >= player2_need_to_win:
                try:
                    pygame.mixer.music.stop()
                    sound.play()
                except:
                    pass
                if wait_for_key_press(window, f"{get_player_skin(2)['name']}赢了!", f"以{score2}的成绩胜过{get_player_skin(1)['name']}!", 100, 100, GOLD, GOLD):
                    time.sleep(2)
                    in_game = False
                else:
                    in_game = False
            
            if is_vsai and score3 >= ai_need_to_win:
                try:
                    pygame.mixer.music.stop()
                    sound.play()
                except:
                    pass
                if wait_for_key_press(window, "AI赢了!", f"以{score3}的成绩胜过你!", 100, 100, GOLD, GOLD):
                    time.sleep(2)
                    in_game = False
                else:
                    in_game = False
            
            if not in_game:  # 如果游戏结束，回到主菜单
                break
                
            # 生成新障碍物和道具
            if len(obstacles) <= 1:
                game_range += 1
                # 根据游戏模式生成不同数量的障碍物
                if is_player2:
                    for i in range(20*game_by_block):
                        obstacle = generate_non_overlapping_position(Obstacle, bombs)
                        all_sprites.add(obstacle)
                        obstacles.add(obstacle)
                else:
                    for i in range(15*game_by_block):
                        obstacle = generate_non_overlapping_position(Obstacle, bombs)
                        all_sprites.add(obstacle)
                        obstacles.add(obstacle)
                # 根据游戏阶段生成不同道具
                if game_range >= 2:
                    # 生成肥波
                    if is_xionger1 or is_xionger2:
                        for i in range(random.randint(0,1)*game_by_block):
                            fengmi = 蜂蜜()
                            all_sprites.add(fengmi)
                            fengmis.add(fengmi)
                    if len(feibos) == 0:
                        feibo = Feibo()
                        all_sprites.add(feibo)
                        feibos.add(feibo)
                    for i in range(random.randint(0,1)*game_by_block):
                        xionger = 熊二_Obs()
                        xiongers.add(xionger)
                        all_sprites.add(xionger)    
                    for i in range(random.randint(0, 2)*game_by_block):
                        speed = generate_non_overlapping_position(Speed, bombs)
                        all_sprites.add(speed)
                        speeds.add(speed)
                    for i in range(random.randint(0, 2)*game_by_block):
                        slow = generate_non_overlapping_position(Slows, bombs)
                        all_sprites.add(slow)
                        slows.add(slow)
                    for i in range(random.randint(1, 3)*game_by_block):
                        obsplus = generate_non_overlapping_position(ObsPlus, bombs)
                        all_sprites.add(obsplus)
                        obspluses.add(obsplus)
                    for i in range(random.randint(0, 2)*game_by_block):
                        ice = generate_non_overlapping_position(Ice, bombs)
                        all_sprites.add(ice)
                        icese.add(ice)
                if game_range >= 5:
                    for i in range(random.randint(0, 2)*game_by_block):
                        needs = generate_non_overlapping_position(Needs, bombs)
                        all_sprites.add(needs)
                        needes.add(needs)
                    if not is_vsai:
                        random_num = random.randint(0,10)
                        print(random_num)
                        if random_num <= 3 and len(孔畅帆们) == 0:
                            for i in range(1*game_by_block):
                                孔畅帆_obs = generate_non_overlapping_position(孔畅帆Obs, bombs)
                                all_sprites.add(孔畅帆_obs)
                                孔畅帆们.add(孔畅帆_obs)
                        random_num = None
                if game_range >= 10:
                    for i in range(random.randint(0, 2)):
                        bomb = generate_non_overlapping_position(Bomb, bombs)
                        all_sprites.add(bomb)
                        bombs.add(bomb)
                    # 限制炸弹数量
                    if len(bombs) >= 4:
                        for bob in bombs:
                            bob.kill()
            
            # 更新精灵
            if not is_vsai:
                player.update(keys)
                if is_player2:
                    player2.update(keys)
            else:
                player.update(keys)
            # 更新武器系统
            if player.equipped_weapon == 'sword':
                player.sword.update()
            elif player.equipped_weapon == 'gun':
                player.gun.update()

            if is_player2 and player2:
                if player2.equipped_weapon == 'sword':
                    player2.sword.update()
                elif player2.equipped_weapon == 'gun':
                    player2.gun.update()

            if is_vsai and player_ai:
                if player_ai.equipped_weapon == 'sword':
                    player_ai.sword.update()
                elif player_ai.equipped_weapon == 'gun':
                    player_ai.gun.update()

            # 武器碰撞检测（统一处理）
            if player.equipped_weapon == 'sword' and player.sword.is_attacking:
                player.sword.detect_collisions()

            if is_player2 and player2 and player2.equipped_weapon == 'sword' and player2.sword.is_attacking:
                player2.sword.detect_collisions()

            if is_vsai and player_ai and player_ai.equipped_weapon == 'sword' and player_ai.sword.is_attacking:
                player_ai.sword.detect_collisions()
            if game_range >= 2:
                players_list = [player]
                if is_player2 and player2:
                    players_list.append(player2)
                if is_vsai and player_ai:
                    players_list.append(player_ai)
                    
                for feibo in feibos:
                    feibo.update(players_list)
            
            # 更新爆炸特效
            update_explosions(explosions)
            
            # 绘制游戏画面
# 绘制游戏画面
            window.fill(WHITE)
            all_sprites.draw(window)
            update_hits(player)
            # 只更新可见区域内的伤害数字
            update_visible_damage_numbers_optimized()
# 更新和绘制冲刺粒子效果
# 更新和绘制冲刺粒子效果
            for particle in dash_particles[:]:
                particle['x'] += particle['dx']
                particle['y'] += particle['dy']
                particle['life'] -= 1
                
                # 绘制粒子
                if particle['life'] > 0:
                    pygame.draw.circle(
                        window, 
                        particle['color'], 
                        (int(particle['x']), int(particle['y'])), 
                        int(particle['radius'])
                    )
                else:
                    dash_particles.remove(particle)


            # 更新和绘制玩家伤害数字
            player.update_damage_numbers()
            player.draw_damage_numbers(window)
            if is_player2:
                update_hits(player2)
                player2.update_damage_numbers()
                player2.draw_damage_numbers(window)
            if is_vsai:
                update_hits(player_ai)
                player_ai.update_damage_numbers()
                player_ai.draw_damage_numbers(window)

            # 绘制玩家血条
            player.draw_health_bar(window)
            if is_player2:
                player2.draw_health_bar(window)
            if is_vsai:
                player_ai.draw_health_bar(window)

            # 绘制武器
            player.draw_weapons(window)
            if is_player2:
                player2.draw_weapons(window)
            if is_vsai:
                player_ai.draw_weapons(window)

            # 绘制爆炸特效
            draw_explosions(window, explosions)

            # 只绘制可见且需要显示血条的方块血条
            #draw_visible_health_bars(window)

            # 只绘制可见区域内的伤害数字
            #draw_visible_damage_numbers(window)
            # 显示玩家状态
            if player.boosted:
                time_left = max(0, (player.boost_duration - (pygame.time.get_ticks() - player.boost_start_time)) // 1000)
                boost_text = font.render(f"加速: {time_left}秒", True, RED)
                window.blit(boost_text, (10, 70))
            if player.slowed:
                time2_left = max(0, (player.slowly_duration - (pygame.time.get_ticks() - player.slowly_start_time)) // 1000)
                slow_text = font.render(f"减速: {time2_left}秒", True, BLACK)
                window.blit(slow_text, (10, 120))
            if player.iced:
                time3_left = max(0, (player.icely_duration - (pygame.time.get_ticks() - player.icely_start_time)) // 1000)
                ice_text = font.render(f"冻结：{time3_left}秒", True, ICE)
                window.blit(ice_text, (10, 170))
            
            # 显示分数
            score_text = font.render(f"分数：{score}/{need_to_win}", True, BLUE)
            window.blit(score_text, (10, 10))
            fps_text = font.render(f"FPS:{fps:.1f}/{max_fps}",True,BLUE)
            window.blit(fps_text,(10,650))
            # 显示玩家二或AI的状态和分数
            if is_player2:
                if player2.boosted:
                    time_left2 = max(0, (player2.boost_duration - (pygame.time.get_ticks() - player2.boost_start_time)) // 1000)
                    boost_text2 = font.render(f"加速: {time_left2}秒", True, RED)
                    window.blit(boost_text2, (950, 70))
                if player2.slowed:
                    time2_left2 = max(0, (player2.slowly_duration - (pygame.time.get_ticks() - player2.slowly_start_time)) // 1000)
                    slow_text2 = font.render(f"减速: {time2_left2}秒", True, BLACK)
                    window.blit(slow_text2, (950, 120))
                if player2.iced:
                    time3_left2 = max(0, (player2.icely_duration - (pygame.time.get_ticks() - player2.icely_start_time)) // 1000)
                    ice_text2 = font.render(f"冻结：{time3_left2}秒", True, ICE)
                    window.blit(ice_text2, (950, 170))
                score2_text = font.render(f"分数：{score2}/{player2_need_to_win}", True, BLUE)
                window.blit(score2_text, (925, 10))
            
            if is_vsai:
                if player_ai.boosted:
                    time_left3 = max(0, (player_ai.boost_duration - (pygame.time.get_ticks() - player_ai.boost_start_time)) // 1000)
                    boost_text3 = font.render(f"加速: {time_left3}秒", True, RED)
                    window.blit(boost_text3, (950, 70))
                if player_ai.slowed:
                    time2_left3 = max(0, (player_ai.slowly_duration - (pygame.time.get_ticks() - player_ai.slowly_start_time)) // 1000)
                    slow_text3 = font.render(f"减速: {time2_left3}秒", True, BLACK)
                    window.blit(slow_text3, (950, 120))
                if player_ai.iced:
                    time3_left3 = max(0, (player_ai.icely_duration - (pygame.time.get_ticks() - player_ai.icely_start_time)) // 1000)
                    ice_text3 = font.render(f"冻结：{time3_left3}秒", True, ICE)
                    window.blit(ice_text3, (950, 170))
                score3_text = font.render(f"分数：{score3}/{ai_need_to_win}", True, BLUE)
                window.blit(score3_text, (925, 10))
            
            pygame.display.flip()

# 退出游戏
pygame.quit()
