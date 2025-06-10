# Qtile Configuration for CachyOS
# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage

import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.bar import Bar
from libqtile.widget import systray

screens = [
    Screen(
        top=Bar(
            [
                # your other widgets...
                widget.Systray(),
            ],
            24,
        ),
    ),
]


# Wayland startup hook
@hook.subscribe.startup_once
def autostart():
    """Run autostart commands for Wayland"""
    home = os.path.expanduser("~")

    # Run autostart script if it exists
    subprocess.call([home + "/.config/qtile/autostart.sh"])


mod = "mod4"  # Super key
terminal = "kitty"
browser = "thorium-browser"
file_manager = "thunar"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Application launchers
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal (Kitty)"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch web browser (Thorium)"),
    Key([mod], "e", lazy.spawn(file_manager), desc="Launch file manager (Thunar)"),
    # Application launcher
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Launch application launcher"),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Window management
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # Volume controls (Wayland)
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+"),
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
    # Brightness controls
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl set +10%"),
        desc="Increase brightness",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl set 10%-"),
        desc="Decrease brightness",
    ),
    # Screenshots (Wayland)
    Key(
        [],
        "Print",
        lazy.spawn(
            'grim -g "$(slurp)" ~/Pictures/Screenshots/screenshot-$(date +%Y%m%d-%H%M%S).png'
        ),
        desc="Take screenshot",
    ),
    Key(
        [mod],
        "Print",
        lazy.spawn("grim ~/Pictures/Screenshots/fullscreen-$(date +%Y%m%d-%H%M%S).png"),
        desc="Take fullscreen screenshot",
    ),
    # System controls
    Key([mod, "shift"], "q", lazy.spawn("powermenu"), desc="Power menu"),
]

# Workspaces/Groups
groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

# Layouts
layouts = [
    layout.Columns(
        border_focus="#9fafdf",
        border_normal="#4f4f4f",
        border_width=2,
        margin=8,
    ),
    layout.Max(),
    layout.Stack(
        num_stacks=2,
        border_focus="#9fafdf",
        border_normal="#4f4f4f",
        border_width=2,
        margin=8,
    ),
    layout.Bsp(
        border_focus="#9fafdf",
        border_normal="#4f4f4f",
        border_width=2,
        margin=8,
    ),
    layout.Matrix(
        border_focus="#9fafdf",
        border_normal="#4f4f4f",
        border_width=2,
        margin=8,
    ),
    layout.MonadTall(
        border_focus="#9fafdf",
        border_normal="#4f4f4f",
        border_width=2,
        margin=8,
    ),
    layout.MonadWide(
        border_focus="#9fafdf",
        border_normal="#4f4f4f",
        border_width=2,
        margin=8,
    ),
    layout.RatioTile(
        border_focus="#9fafdf",
        border_normal="#4f4f4f",
        border_width=2,
        margin=8,
    ),
    layout.Tile(
        border_focus="#9fafdf",
        border_normal="#4f4f4f",
        border_width=2,
        margin=8,
    ),
    layout.TreeTab(),
    layout.VerticalTile(
        border_focus="#9fafdf",
        border_normal="#4f4f4f",
        border_width=2,
        margin=8,
    ),
    layout.Zoomy(),
]

# Colors (Zenburn theme)
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

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(
                    foreground=colors[8],
                    background=colors[0],
                    padding=5,
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
                widget.Prompt(
                    foreground=colors[10],
                    background=colors[0],
                ),
                widget.WindowName(
                    foreground=colors[6],
                    background=colors[0],
                    padding=0,
                ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(
                    background=colors[0],
                    padding=5,
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    foreground=colors[2],
                    background=colors[0],
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
                widget.GenPollText(
                    func=lambda: subprocess.check_output(
                        ["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"]
                    )
                    .decode("utf-8")
                    .strip()
                    .replace("Volume: ", "Vol: "),
                    update_interval=1,
                    foreground=colors[7],
                    background=colors[0],
                    padding=5,
                    mouse_callbacks={
                        "Button3": lazy.spawn("pavucontrol"),
                        "Button4": lazy.spawn(
                            "wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+"
                        ),
                        "Button5": lazy.spawn(
                            "wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"
                        ),
                    },
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
                    func=lambda: (
                        subprocess.check_output(["bluetoothctl", "show"])
                        .decode("utf-8")
                        .split("\n")[4]
                        .split()[1]
                        if subprocess.run(
                            ["bluetoothctl", "show"], capture_output=True
                        ).returncode
                        == 0
                        else "Off"
                    ),
                    update_interval=5,
                    foreground=colors[8],
                    background=colors[0],
                    padding=5,
                    fmt="BT: {}",
                    mouse_callbacks={"Button1": lazy.spawn("blueman-manager")},
                ),
                widget.KeyboardLayout(
                    configured_keyboards=["se"],
                    foreground=colors[9],
                    background=colors[0],
                    padding=5,
                ),
                widget.Clock(
                    format="%Y-%m-%d %a %I:%M %p",
                    foreground=colors[10],
                    background=colors[0],
                    padding=5,
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn(
                            "calendar"
                        ),  # Launch calendar app
                        "Button3": lambda: qtile.cmd_spawn(
                            "calcurse"
                        ),  # Right-click for calcurse
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

# Drag floating layouts.
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

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="Thunar"),  # Make Thunar float by default
        Match(wm_class="pavucontrol"),  # Volume control
        Match(wm_class="blueman-manager"),  # Bluetooth manager
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this configures input devices
wl_input_rules = {
    "type:keyboard": {
        "xkb_layout": "se",  # Swedish keyboard layout
        "xkb_options": "caps:swapescape",  # Swap Caps Lock and Escape
    },
    "type:touchpad": {
        "tap": True,
        "natural_scroll": True,
    },
}

import subprocess


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["blueman-applet"])
    subprocess.Popen(["nm-applet"])
    subprocess.Popen(["volumeicon"])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
