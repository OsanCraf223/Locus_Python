import pygame
import sys
from tkinter import Tk, filedialog, messagebox

# ----------------------- Helper Functions -----------------------

def new_file():
    global lines, cursor_x, cursor_y, file_path
    lines = [""]
    cursor_x = cursor_y = 0
    file_path = None
    push_undo()

def open_file():
    global lines, cursor_x, cursor_y, file_path
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="Open File",
        filetypes=[
            ("All Files", "*.*"),
            ("Text Files", "*.txt"),
            ("Python Files", "*.py"),
            ("Java Files", "*.java"),
            ("HTML Files", "*.html"),
            ("CSV Files", "*.csv"),
        ]
    )
    root.destroy()
    if path:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            lines[:] = content.splitlines() or [""]
            cursor_x = cursor_y = 0
            file_path = path
            push_undo()

def save_file_as():
    global file_path
    root = Tk()
    root.withdraw()
    path = filedialog.asksaveasfilename(
        defaultextension=".lcs",
        filetypes=[("LCS Files", "*.lcs"), ("All Files", "*.*")],
        title="Save As"
    )
    root.destroy()
    if path:
        with open(path, "w", encoding="utf-8") as file:
            file.write('\n'.join(lines))
        file_path = path

def save_file_quick():
    global file_path
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write('\n'.join(lines))
    else:
        save_file_as()

def show_about():
    root = Tk()
    root.withdraw()
    messagebox.showinfo(
        "About",
        "Locus_Python\nA text editor in Pygame.\nBy OsanCraft"
    )
    root.destroy()

def copy_text():
    root = Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append('\n'.join(lines))
    root.destroy()

def paste_text():
    global lines, cursor_x, cursor_y
    root = Tk()
    root.withdraw()
    try:
        paste_content = root.clipboard_get()
        for ch in paste_content:
            if ch == "\n":
                insert_newline()
            else:
                insert_char(ch)
    except Exception:
        pass
    root.destroy()

def cut_text():
    copy_text()
    new_file()

def push_undo():
    global undo_stack
    if len(undo_stack) > 100:
        undo_stack.pop(0)
    undo_stack.append((list(lines), cursor_x, cursor_y))

def undo():
    global lines, cursor_x, cursor_y, undo_stack, redo_stack
    if undo_stack:
        redo_stack.append((list(lines), cursor_x, cursor_y))
        prev = undo_stack.pop()
        lines[:] = prev[0]
        cursor_x, cursor_y = prev[1], prev[2]

def redo():
    global lines, cursor_x, cursor_y, undo_stack, redo_stack
    if redo_stack:
        push_undo()
        next_ = redo_stack.pop()
        lines[:] = next_[0]
        cursor_x, cursor_y = next_[1], next_[2]

def select_all_text():
    pass

def show_stats():
    num_lines = len(lines)
    num_chars = sum(len(line) for line in lines)
    num_words = sum(len(line.split()) for line in lines)
    root = Tk()
    root.withdraw()
    messagebox.showinfo(
        "Document Stats",
        f"Lines: {num_lines}\nWords: {num_words}\nCharacters: {num_chars}"
    )
    root.destroy()

def handle_shortcuts(event):
    if event.mod & pygame.KMOD_CTRL:
        if event.key == pygame.K_n:
            new_file()
        elif event.key == pygame.K_o:
            open_file()
        elif event.key == pygame.K_s:
            save_file_as()
        elif event.key == pygame.K_z:
            undo()
        elif event.key == pygame.K_y:
            redo()
        elif event.key == pygame.K_c:
            copy_text()
        elif event.key == pygame.K_v:
            paste_text()
        elif event.key == pygame.K_x:
            cut_text()
        elif event.key == pygame.K_a:
            select_all_text()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_m:
            toggle_dark_mode()

def toggle_dark_mode():
    global target_theme
    target_theme = "light" if THEME == "dark" else "dark"

def apply_theme_transition(dt):
    """Smoothly interpolate color values between dark and light mode."""
    global BG_COLOR, TEXT_COLOR, CURSOR_COLOR, MENU_BG, MENU_HOVER, MENU_ACTIVE, THEME, theme_progress
    # Define dark and light color sets
    dark = {
        "BG_COLOR": (35, 40, 48),
        "TEXT_COLOR": (230, 230, 230),
        "CURSOR_COLOR": (70, 170, 255),
        "MENU_BG": (50, 54, 65),
        "MENU_HOVER": (95, 110, 160),
        "MENU_ACTIVE": (115, 140, 200),
    }
    light = {
        "BG_COLOR": (245, 245, 245),
        "TEXT_COLOR": (45, 45, 60),
        "CURSOR_COLOR": (30, 120, 230),
        "MENU_BG": (235, 238, 246),
        "MENU_HOVER": (215, 225, 250),
        "MENU_ACTIVE": (190, 210, 250),
    }
    # Smoothly transition theme_progress to 0 (dark) or 1 (light)
    target = 1 if target_theme == "light" else 0
    speed = 3.5  # seconds for full transition
    if abs(theme_progress - target) > 0.01:
        theme_progress += (target - theme_progress) * min(dt * speed * 2, 1)
    else:
        theme_progress = target
        global THEME
        THEME = target_theme

    # Interpolate between dark and light for each color
    def lerp_color(c1, c2, t):
        return tuple(int(c1[i]*(1-t) + c2[i]*t) for i in range(3))

    BG_COLOR = lerp_color(dark["BG_COLOR"], light["BG_COLOR"], theme_progress)
    TEXT_COLOR = lerp_color(dark["TEXT_COLOR"], light["TEXT_COLOR"], theme_progress)
    CURSOR_COLOR = lerp_color(dark["CURSOR_COLOR"], light["CURSOR_COLOR"], theme_progress)
    MENU_BG = lerp_color(dark["MENU_BG"], light["MENU_BG"], theme_progress)
    MENU_HOVER = lerp_color(dark["MENU_HOVER"], light["MENU_HOVER"], theme_progress)
    MENU_ACTIVE = lerp_color(dark["MENU_ACTIVE"], light["MENU_ACTIVE"], theme_progress)

# ---------------------- Main Window Setup -----------------------

pygame.init()

WIDTH, HEIGHT = 900, 540
font_size = 18
FONT = pygame.font.SysFont("consolas", font_size, bold=False)
TEXT_COLOR = (230, 230, 230)
BG_COLOR = (35, 40, 48)
CURSOR_COLOR = (70, 170, 255)
LINE_SPACING = 6
PADDING_X, PADDING_Y = 14, 10
THEME = "dark"  # "dark" or "light"
target_theme = "dark"
theme_progress = 0.0

MENU_HEIGHT = 38
MENU_BG = (50, 54, 65)
MENU_HOVER = (95, 110, 160)
MENU_ACTIVE = (115, 140, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Locus_Python - Modern Text Editor")

try:
    icon_surface = pygame.image.load("locusImage.png")
    pygame.display.set_icon(icon_surface)
except Exception:
    pass

lines = [""]
cursor_x, cursor_y = 0, 0
show_cursor = True
cursor_timer = 0
scroll_offset = 0
file_path = None
undo_stack = []
redo_stack = []

# Menu bar definitions
menu_active = None
menu_transition = {"file": 0.0, "edit": 0.0, "help": 0.0}

file_menu_rect = pygame.Rect(0, 0, 66, MENU_HEIGHT)
edit_menu_rect = pygame.Rect(66, 0, 66, MENU_HEIGHT)
help_menu_rect = pygame.Rect(132, 0, 70, MENU_HEIGHT)

file_menu_items = [
    ("New", new_file),
    ("Open...", open_file),
    ("Save As...", save_file_as),
    ("Quick Save", save_file_quick),
    ("Exit", lambda: sys.exit(0)),
]
edit_menu_items = [
    ("Undo", undo),
    ("Redo", redo),
    ("Copy All", copy_text),
    ("Paste", paste_text),
    ("Cut All", cut_text),
    ("Stats", show_stats),
]
help_menu_items = [
    ("About", show_about),
]

def draw_menu_bar(dt):
    """Draw the menu bar and handle smooth color transitions with non-rounded buttons."""
    for mname, rect in zip(
        ["file", "edit", "help"],
        [file_menu_rect, edit_menu_rect, help_menu_rect]
    ):
        target = 1.0 if menu_active == mname or rect.collidepoint(pygame.mouse.get_pos()) else 0.0
        menu_transition[mname] += (target - menu_transition[mname]) * (dt * 12)
        menu_transition[mname] = max(0.0, min(menu_transition[mname], 1.0))

    # Draw menus - no rounded corners
    for mname, rect, label in zip(
        ["file", "edit", "help"],
        [file_menu_rect, edit_menu_rect, help_menu_rect],
        ["File", "Edit", "Help"]
    ):
        blend = menu_transition[mname]
        base = pygame.Color(*MENU_BG)
        active = pygame.Color(*MENU_ACTIVE)
        color = [int(base[i] * (1-blend) + active[i] * blend) for i in range(3)]
        pygame.draw.rect(screen, color, rect)
        text = FONT.render(label, True, (245,245,255) if theme_progress < 0.5 else (55,55,80))
        screen.blit(text, (rect.x + 12, rect.y + 8))

    # Draw dropdowns if active - no rounded corners
    if menu_active == "file":
        for i, (name, _) in enumerate(file_menu_items):
            item_rect = pygame.Rect(file_menu_rect.x, MENU_HEIGHT + i*MENU_HEIGHT, 180, MENU_HEIGHT)
            color = MENU_ACTIVE if item_rect.collidepoint(pygame.mouse.get_pos()) else MENU_HOVER
            pygame.draw.rect(screen, color, item_rect)
            screen.blit(FONT.render(name, True, (245,245,255) if theme_progress < 0.5 else (55,55,80)), (item_rect.x+18, item_rect.y+8))
    elif menu_active == "edit":
        for i, (name, _) in enumerate(edit_menu_items):
            item_rect = pygame.Rect(edit_menu_rect.x, MENU_HEIGHT + i*MENU_HEIGHT, 180, MENU_HEIGHT)
            color = MENU_ACTIVE if item_rect.collidepoint(pygame.mouse.get_pos()) else MENU_HOVER
            pygame.draw.rect(screen, color, item_rect)
            screen.blit(FONT.render(name, True, (245,245,255) if theme_progress < 0.5 else (55,55,80)), (item_rect.x+18, item_rect.y+8))
    elif menu_active == "help":
        for i, (name, _) in enumerate(help_menu_items):
            item_rect = pygame.Rect(help_menu_rect.x, MENU_HEIGHT + i*MENU_HEIGHT, 180, MENU_HEIGHT)
            color = MENU_ACTIVE if item_rect.collidepoint(pygame.mouse.get_pos()) else MENU_HOVER
            pygame.draw.rect(screen, color, item_rect)
            screen.blit(FONT.render(name, True, (245,245,255) if theme_progress < 0.5 else (55,55,80)), (item_rect.x+18, item_rect.y+8))

def handle_menu_click(pos):
    global menu_active
    if file_menu_rect.collidepoint(pos):
        menu_active = "file" if menu_active != "file" else None
    elif edit_menu_rect.collidepoint(pos):
        menu_active = "edit" if menu_active != "edit" else None
    elif help_menu_rect.collidepoint(pos):
        menu_active = "help" if menu_active != "help" else None
    else:
        if menu_active == "file":
            for i, (_, func) in enumerate(file_menu_items):
                item_rect = pygame.Rect(file_menu_rect.x, MENU_HEIGHT + i*MENU_HEIGHT, 180, MENU_HEIGHT)
                if item_rect.collidepoint(pos):
                    func()
                    menu_active = None
                    return
        if menu_active == "edit":
            for i, (_, func) in enumerate(edit_menu_items):
                item_rect = pygame.Rect(edit_menu_rect.x, MENU_HEIGHT + i*MENU_HEIGHT, 180, MENU_HEIGHT)
                if item_rect.collidepoint(pos):
                    func()
                    menu_active = None
                    return
        if menu_active == "help":
            for i, (_, func) in enumerate(help_menu_items):
                item_rect = pygame.Rect(help_menu_rect.x, MENU_HEIGHT + i*MENU_HEIGHT, 180, MENU_HEIGHT)
                if item_rect.collidepoint(pos):
                    func()
                    menu_active = None
                    return
        menu_active = None

def render_text():
    """Draw all lines of text and the cursor, handling scrolling."""
    pygame.draw.rect(screen, BG_COLOR, (0, MENU_HEIGHT, WIDTH, HEIGHT-MENU_HEIGHT))
    y = MENU_HEIGHT + PADDING_Y - scroll_offset
    for i, line in enumerate(lines):
        text_surface = FONT.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (PADDING_X, y))
        y += font_size + LINE_SPACING
    # Blue cursor
    if show_cursor:
        if MENU_HEIGHT + PADDING_Y + (cursor_y*(font_size+LINE_SPACING)) - scroll_offset >= MENU_HEIGHT:
            cursor_line = lines[cursor_y]
            cursor_px = FONT.size(cursor_line[:cursor_x])[0] + PADDING_X
            cursor_py = MENU_HEIGHT + PADDING_Y + cursor_y * (font_size + LINE_SPACING) - scroll_offset
            pygame.draw.rect(screen, CURSOR_COLOR, (cursor_px, cursor_py, 2, font_size))

def insert_char(ch):
    push_undo()
    global lines, cursor_x, cursor_y
    line = lines[cursor_y]
    lines[cursor_y] = line[:cursor_x] + ch + line[cursor_x:]
    cursor_x += 1

def delete_char():
    push_undo()
    global lines, cursor_x, cursor_y
    if cursor_x > 0:
        line = lines[cursor_y]
        lines[cursor_y] = line[:cursor_x-1] + line[cursor_x:]
        cursor_x -= 1
    elif cursor_y > 0:
        prev_line = lines[cursor_y - 1]
        this_line = lines[cursor_y]
        cursor_x = len(prev_line)
        lines[cursor_y - 1] = prev_line + this_line
        del lines[cursor_y]
        cursor_y -= 1

def insert_newline():
    push_undo()
    global lines, cursor_x, cursor_y
    line = lines[cursor_y]
    lines[cursor_y] = line[:cursor_x]
    lines.insert(cursor_y + 1, line[cursor_x:])
    cursor_y += 1
    cursor_x = 0

def ensure_cursor_visible():
    global scroll_offset
    cursor_pixel_y = MENU_HEIGHT + PADDING_Y + cursor_y * (font_size + LINE_SPACING)
    visible_min = scroll_offset + MENU_HEIGHT
    visible_max = scroll_offset + HEIGHT - font_size
    if cursor_pixel_y < visible_min:
        scroll_offset = max(0, cursor_pixel_y - MENU_HEIGHT - 2)
    elif cursor_pixel_y > visible_max:
        scroll_offset = cursor_pixel_y - (HEIGHT - font_size - 2)

# -------------------- Main Event Loop ----------------------

clock = pygame.time.Clock()
while True:
    dt = clock.tick(60) / 1000.0  # Delta time for smooth transitions

    apply_theme_transition(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_menu_click(event.pos)
        elif event.type == pygame.KEYDOWN and menu_active is None:
            handle_shortcuts(event)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_BACKSPACE:
                delete_char()
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                insert_newline()
            elif event.key == pygame.K_LEFT:
                if cursor_x > 0:
                    cursor_x -= 1
                elif cursor_y > 0:
                    cursor_y -= 1
                    cursor_x = len(lines[cursor_y])
            elif event.key == pygame.K_RIGHT:
                if cursor_x < len(lines[cursor_y]):
                    cursor_x += 1
                elif cursor_y < len(lines) - 1:
                    cursor_y += 1
                    cursor_x = 0
            elif event.key == pygame.K_UP:
                if cursor_y > 0:
                    cursor_y -= 1
                    cursor_x = min(cursor_x, len(lines[cursor_y]))
            elif event.key == pygame.K_DOWN:
                if cursor_y < len(lines) - 1:
                    cursor_y += 1
                    cursor_x = min(cursor_x, len(lines[cursor_y]))
            elif event.key == pygame.K_HOME:
                cursor_x = 0
            elif event.key == pygame.K_END:
                cursor_x = len(lines[cursor_y])
            elif event.unicode and event.unicode.isprintable():
                insert_char(event.unicode)

    # Blinking cursor logic
    cursor_timer += clock.get_time()
    if cursor_timer > 500:
        show_cursor = not show_cursor
        cursor_timer = 0

    ensure_cursor_visible()
    render_text()
    draw_menu_bar(dt)
    pygame.display.flip()
