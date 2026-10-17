# Qtile Configuration for CachyOS (Wayland, Swedish layout, laptop)
# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage

import os
import subprocess

from libqtile import bar, hook, layout, widget
from libqtile.backend.wayland import InputConfig
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"  # Super key
terminal = "kitty"
browser = "thorium-browser"
file_manager = "thunar"

# ---------------------------------------------------------------------------
# Autostart (single hook, non-blocking)
# ---------------------------------------------------------------------------
@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    if os.path.exists(script):
        subprocess.Popen([script])
    # Tray applets (shown via the StatusNotifier widget)
    subprocess.Popen(["nm-applet", "--indicator"])
    subprocess.Popen(["blueman-applet"])


# ---------------------------------------------------------------------------
# Keys
# ---------------------------------------------------------------------------
SCREENSHOT_DIR = "~/Pictures/Screenshots"

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
    # Screenshots (shell=True so $(...) and ~ are expanded)
    Key(
        [],
        "Print",
        lazy.spawn(
            f'mkdir -p {SCREENSHOT_DIR} && grim -g "$(slurp)" '
            f"{SCREENSHOT_DIR}/screenshot-$(date +%Y%m%d-%H%M%S).png",
            shell=True,
        ),
        desc="Screenshot (region)",
    ),
    Key(
        [mod],
        "Print",
        lazy.spawn(
            f"mkdir -p {SCREENSHOT_DIR} && grim "
            f"{SCREENSHOT_DIR}/fullscreen-$(date +%Y%m%d-%H%M%S).png",
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
groups = [Group(i) for i in "123456789"]

for g in groups:
    keys.extend(
        [
            Key(
                [mod],
                g.name,
                lazy.group[g.name].toscreen(),
                desc=f"Switch to group {g.name}",
            ),
            Key(
                [mod, "shift"],
                g.name,
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
def bluetooth_status():
    """One cheap call; reports On/Off for the default controller."""
    try:
        out = subprocess.check_output(
            ["bluetoothctl", "show"], text=True, timeout=2
        )
    except (subprocess.SubprocessError, FileNotFoundError):
        return "Off"
    for line in out.splitlines():
        if line.strip().startswith("Powered:"):
            return "On" if line.split()[-1] == "yes" else "Off"
    return "Off"


# ---------------------------------------------------------------------------
# Screens / bar
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
                ),
                widget.Prompt(foreground=colors[10], background=colors[0]),
                widget.WindowName(
                    foreground=colors[6], background=colors[0], padding=0
                ),
                widget.Chord(
                    chords_colors={"launch": ("#ff0000", "#ffffff")},
                    name_transform=lambda name: name.upper(),
                ),
                # Wayland-compatible tray (Systray is X11-only)
                widget.StatusNotifier(background=colors[0], padding=5),
                widget.Sep(
                    linewidth=0, padding=6, foreground=colors[2], background=colors[0]
                ),
                widget.CPU(
                    format="CPU: {load_percent}%",
                    foreground=colors[4],
                    background=colors[0],
                    padding=5,
                ),
                widget.Memory(
                    format="MEM: {MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
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
                widget.Wlan(
                    interface="wlan0",
                    format="WiFi: {essid} {percent:2.0%}",
                    foreground=colors[4],
                    background=colors[0],
                    padding=5,
                    mouse_callbacks={"Button1": lazy.spawn("nm-connection-editor")},
                ),
                widget.Net(
                    interface="wlan0",
                    format="{down} ↓↑ {up}",
                    foreground=colors[5],
                    background=colors[0],
                    padding=5,
                ),
                widget.GenPollText(
                    func=bluetooth_status,
                    update_interval=15,
                    fmt="BT: {}",
                    foreground=colors[8],
                    background=colors[0],
                    padding=5,
                    mouse_callbacks={"Button1": lazy.spawn("blueman-manager")},
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
        # Wayland app_ids are often lowercase; match both spellings
        Match(wm_class="Thunar"),
        Match(wm_class="thunar"),
        Match(wm_class="pavucontrol"),
        Match(wm_class="blueman-manager"),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

# ---------------------------------------------------------------------------
# Wayland input (InputConfig objects, kb_* option names)
# ---------------------------------------------------------------------------
wl_input_rules = {
    "type:keyboard": InputConfig(
        kb_layout="se",
        kb_options="caps:swapescape",
        kb_repeat_rate=40,
        kb_repeat_delay=200,
    ),
    "type:touchpad": InputConfig(
        tap=True,
        natural_scroll=True,
        dwt=True,
    ),
}
