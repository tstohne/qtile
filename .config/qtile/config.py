# Qtile Configuration for CachyOS (X11/Xorg, Swedish layout, laptop)
# Based on the Qtile default config:
# Copyright (c) 2010 Aldo Cortesi, 2010/2014 dequis, 2012 Randall Ma,
# 2012-2014 Tycho Andersen, 2012 Craig Barnes, 2013 horsik, 2013 Tao Sauvage

import os
import shutil
import subprocess

from libqtile import bar, hook, layout, widget
from libqtile.backend.base import Window
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"  # Super key
terminal = "kitty"
browser = "thorium-browser"
file_manager = "thunar"

HOME = os.path.expanduser("~")
SCREENSHOT_DIR = "~/Pictures/Screenshots"
WALLPAPER = os.path.join(HOME, ".config/qtile/wallpaper.png")


# ---------------------------------------------------------------------------
# Autostart (runs once per X session, never blocks, skips missing programs)
# ---------------------------------------------------------------------------
# Workspace names, in order (mod+1 .. mod+5)
GROUP_NAMES = ["Web", "Term", "Emacs", "Chat", "Etc"]

# (group, command) pairs launched at session start
WORKSPACE_APPS = [
    ("Web", ["/usr/bin/thorium-browser"]),
    ("Term", ["/usr/bin/kitty"]),
    ("Emacs", ["/usr/bin/emacsclient", "-c"]),
    ("Chat", ["/usr/bin/mattermost-desktop"]),
]

# Lower-case WM_CLASS -> group, consumed once as each window appears
_pending_windows = {
    "thorium-browser": "Web",
    "kitty": "Term",
    "emacs": "Emacs",
    "mattermost": "Chat",
}


def run_once(*cmd: str) -> None:
    """Spawn a program if it is installed; silently skip otherwise."""
    if shutil.which(cmd[0]):
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@hook.subscribe.startup_once
def autostart() -> None:
    # Keyboard: Swedish layout, Caps <-> Escape swapped, fast key repeat
    run_once("setxkbmap", "-layout", "se", "-option", "caps:swapescape")
    run_once("xset", "r", "rate", "200", "40")
    run_once("xset", "s", "off", "-dpms")  # drop this line if you want DPMS blanking

    # Touchpad: tap-to-click, natural scrolling, disable-while-typing is a libinput default
    # (see the xorg.conf.d snippet for a persistent version)
    run_once("xsetroot", "-cursor_name", "left_ptr")

    # Compositor (vsync, no tearing on UMA graphics)
    run_once("picom"," --config ~/.config/picom/picom.conf -b")

    # Wallpaper
    if os.path.exists(WALLPAPER):
        run_once("feh", "--bg-fill", WALLPAPER)

    # Policy kit agent (try common ones, first installed wins)
    for agent in (
        "/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1",
        "/usr/lib/mate-polkit/polkit-mate-authentication-agent-1",
    ):
        if os.path.exists(agent):
            subprocess.Popen([agent])
            break

    # Tray applets (shown in the Systray widget)
    run_once("nm-applet")
    run_once("blueman-applet")
    # Notifications
    run_once("dunst")

    # Workspace apps: each window is sent to its group by on_new_client() below
    for _group, cmd in WORKSPACE_APPS:
        run_once(*cmd)

    # User script for anything else
    script = os.path.join(HOME, ".config/qtile/autostart.sh")
    if os.path.exists(script):
        subprocess.Popen([script])


@hook.subscribe.client_new
def on_new_client(window: Window) -> None:
    """Send the first window of each autostarted app to its workspace.

    Only windows from the autostart list are moved; apps you launch later
    open on whatever workspace you are on.
    """
    try:
        classes = [c.lower() for c in window.get_wm_class() or ()]
    except Exception:
        return
    for wm_class, group in list(_pending_windows.items()):
        if wm_class in classes:
            window.togroup(group)
            del _pending_windows[wm_class]
            break


# Java GUI apps misbehave unless the WM identifies as LG3D
wmname = "LG3D"

# ---------------------------------------------------------------------------
# Keys
# ---------------------------------------------------------------------------
SHOT = os.path.expanduser(SCREENSHOT_DIR)

keys = [
    # Application launchers
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal (Kitty)"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch web browser (Thorium)"),
    Key([mod], "e", lazy.spawn(file_manager), desc="Launch file manager (Thunar)"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Launch application launcher"),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Window management
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # Volume (PipeWire)
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("wpctl set-volume -l 1.0 @DEFAULT_AUDIO_SINK@ 5%+"),
        desc="Increase volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"),
        desc="Decrease volume",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"),
        desc="Mute/unmute volume",
    ),
    # Brightness
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl set 10%+"),
        desc="Increase brightness",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl set 10%-"),
        desc="Decrease brightness",
    ),
    # Screenshots (maim + slop; also copied to clipboard via xclip)
    Key(
        [],
        "Print",
        lazy.spawn(
            f'mkdir -p "{SHOT}" && f="{SHOT}/screenshot-$(date +%Y%m%d-%H%M%S).png" '
            '&& maim -s "$f" && xclip -selection clipboard -t image/png "$f"',
            shell=True,
        ),
        desc="Screenshot (region)",
    ),
    Key(
        [mod],
        "Print",
        lazy.spawn(
            f'mkdir -p "{SHOT}" && f="{SHOT}/fullscreen-$(date +%Y%m%d-%H%M%S).png" '
            '&& maim "$f" && xclip -selection clipboard -t image/png "$f"',
            shell=True,
        ),
        desc="Screenshot (full screen)",
    ),
    # System
    Key([mod, "shift"], "q", lazy.spawn("powermenu"), desc="Power menu"),
]

# ---------------------------------------------------------------------------
# Groups
# ---------------------------------------------------------------------------
groups = [Group(name) for name in GROUP_NAMES]

for index, g in enumerate(groups, start=1):
    keys.extend(
        [
            Key(
                [mod],
                str(index),
                lazy.group[g.name].toscreen(),
                desc=f"Switch to group {g.name}",
            ),
            Key(
                [mod, "shift"],
                str(index),
                lazy.window.togroup(g.name, switch_group=True),
                desc=f"Switch to & move focused window to group {g.name}",
            ),
        ]
    )

# ---------------------------------------------------------------------------
# Layouts
# ---------------------------------------------------------------------------
layout_theme = dict(
    border_focus="#9fafdf",
    border_normal="#4f4f4f",
    border_width=2,
    margin=8,
)

layouts = [
    layout.Columns(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Max(),
]

# ---------------------------------------------------------------------------
# Colors (Zenburn)
# ---------------------------------------------------------------------------
colors = [
    ["#3f3f3f", "#3f3f3f"],  # 0 - background
    ["#4f4f4f", "#4f4f4f"],  # 1 - darker background
    ["#dcdccc", "#dcdccc"],  # 2 - foreground
    ["#709080", "#709080"],  # 3 - comment/inactive
    ["#8cd0d3", "#8cd0d3"],  # 4 - cyan
    ["#7f9f7f", "#7f9f7f"],  # 5 - green
    ["#dfaf8f", "#dfaf8f"],  # 6 - orange/yellow
    ["#dc8cc3", "#dc8cc3"],  # 7 - pink/magenta
    ["#9fafdf", "#9fafdf"],  # 8 - blue
    ["#cc9393", "#cc9393"],  # 9 - red
    ["#f0dfaf", "#f0dfaf"],  # 10 - bright yellow
]

widget_defaults = dict(
    font="SauceCodePro Nerd Font",
    fontsize=12,
    padding=3,
    foreground=colors[2],
)
extension_defaults = widget_defaults.copy()


# ---------------------------------------------------------------------------
# Bar helpers
# ---------------------------------------------------------------------------
def bluetooth_status() -> str:
    """One cheap call; reports On/Off for the default controller."""
    try:
        out = subprocess.check_output(
            ["bluetoothctl", "show"], text=True, timeout=2, stderr=subprocess.DEVNULL
        )
    except (subprocess.SubprocessError, FileNotFoundError):
        return "Off"
    for line in out.splitlines():
        if line.strip().startswith("Powered:"):
            return "On" if line.split()[-1] == "yes" else "Off"
    return "Off"


# ---------------------------------------------------------------------------
# Screens / bar
# Polling intervals are deliberately relaxed to save battery.
# ---------------------------------------------------------------------------
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(
                    foreground=colors[8], background=colors[0], padding=5
                ),
                widget.GroupBox(
                    font="SauceCodePro Nerd Font",
                    fontsize=11,
                    margin_y=3,
                    margin_x=0,
                    padding_y=5,
                    padding_x=3,
                    borderwidth=3,
                    active=colors[8],
                    inactive=colors[3],
                    rounded=False,
                    highlight_color=colors[1],
                    highlight_method="line",
                    this_current_screen_border=colors[8],
                    this_screen_border=colors[4],
                    other_current_screen_border=colors[7],
                    other_screen_border=colors[4],
                    foreground=colors[2],
                    background=colors[0],
                    disable_drag=True,
                ),
                widget.Prompt(foreground=colors[10], background=colors[0]),
                widget.WindowName(
                    foreground=colors[6], background=colors[0], padding=0
                ),
                widget.Chord(
                    chords_colors={"launch": ("#ff0000", "#ffffff")},
                    name_transform=lambda name: name.upper(),
                ),
                # X11 tray (nm-applet, blueman-applet, etc.)
                widget.Systray(background=colors[0], padding=5, icon_size=16),
                widget.Sep(
                    linewidth=0, padding=6, foreground=colors[2], background=colors[0]
                ),
                widget.CPU(
                    format="CPU: {load_percent}%",
                    update_interval=3.0,
                    foreground=colors[4],
                    background=colors[0],
                    padding=5,
                ),
                widget.Memory(
                    format="MEM: {MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
                    update_interval=5.0,
                    foreground=colors[5],
                    background=colors[0],
                    padding=5,
                ),
                # Event-driven; needs `pulsectl-asyncio` (works with PipeWire-Pulse)
                widget.PulseVolume(
                    fmt="Vol: {}",
                    step=5,
                    foreground=colors[7],
                    background=colors[0],
                    padding=5,
                    mouse_callbacks={"Button3": lazy.spawn("pavucontrol")},
                ),
                # Needs `python-iwlib`; check your interface name with `ip link`
                widget.Wlan(
                    interface="wlan0",
                    format="WiFi: {essid} {percent:2.0%}",
                    update_interval=5,
                    foreground=colors[4],
                    background=colors[0],
                    padding=5,
                    mouse_callbacks={"Button1": lazy.spawn("nm-connection-editor")},
                ),
                widget.Net(
                    interface="wlan0",
                    format="{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}",
                    update_interval=3,
                    foreground=colors[5],
                    background=colors[0],
                    padding=5,
                ),
                widget.GenPollText(
                    func=bluetooth_status,
                    update_interval=30,
                    fmt="BT: {}",
                    foreground=colors[8],
                    background=colors[0],
                    padding=5,
                    mouse_callbacks={"Button1": lazy.spawn("blueman-manager")},
                ),
                widget.Battery(
                    format="BAT: {char}{percent:2.0%}",
                    charge_char="+",
                    discharge_char="-",
                    full_char="=",
                    empty_char="!",
                    unknown_char="?",
                    update_interval=30,
                    low_percentage=0.15,
                    low_foreground=colors[9],
                    foreground=colors[6],
                    background=colors[0],
                    padding=5,
                ),
                widget.Clock(
                    format="%Y-%m-%d %a %H:%M",
                    foreground=colors[10],
                    background=colors[0],
                    padding=5,
                    mouse_callbacks={
                        "Button1": lazy.spawn("calendar"),
                        "Button3": lazy.spawn(f"{terminal} -e calcurse"),
                    },
                ),
                widget.QuickExit(
                    default_text="[X]",
                    countdown_format="[{}]",
                    foreground=colors[9],
                    background=colors[0],
                    padding=5,
                ),
            ],
            24,
            background=colors[0],
        ),
    ),
]

# ---------------------------------------------------------------------------
# Mouse
# ---------------------------------------------------------------------------
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# ---------------------------------------------------------------------------
# Misc behavior
# ---------------------------------------------------------------------------
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        # X11 WM_CLASS values are usually capitalized
        Match(wm_class="Thunar"),
        Match(wm_class="Pavucontrol"),
        Match(wm_class="Blueman-manager"),
        Match(wm_class="Nm-connection-editor"),
        Match(wm_class="Arandr"),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = False  # X11: avoids unexpected minimizing of fullscreen apps
