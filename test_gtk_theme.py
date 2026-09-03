#!/usr/bin/env python3
"""
Test viewer for Caelestia GTK Theme components:
- Sliders (Scales)
- Toggles (Switches, CheckButtons, Radios)
- Drop Downs (DropDown, SplitButton, ComboBox)
- Rollers (SpinButtons)
"""

import os
import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, GLib


class ThemeTestWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("Caelestia GTK Theme Preview")
        self.set_default_size(720, 750)

        # Apply GTK 4 user CSS
        self.load_css()

        # Scrolled container
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_child(scrolled)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        main_box.set_margin_top(28)
        main_box.set_margin_bottom(28)
        main_box.set_margin_start(32)
        main_box.set_margin_end(32)
        scrolled.set_child(main_box)

        # ---------------------------------------------------------------------
        # 1. Sliders (Scales)
        # ---------------------------------------------------------------------
        main_box.append(self._make_section_header("Sliders (Scales)"))

        slider_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        # Horizontal slider
        h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        h_label = Gtk.Label(label="Volume", xalign=0)
        h_label.set_hexpand(False)
        scale_h = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        scale_h.set_value(65)
        scale_h.set_hexpand(True)
        h_box.append(h_label)
        h_box.append(scale_h)
        slider_card.append(h_box)

        # Disabled slider
        h_box_dis = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        dis_label = Gtk.Label(label="Disabled", xalign=0)
        scale_dis = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        scale_dis.set_value(40)
        scale_dis.set_sensitive(False)
        scale_dis.set_hexpand(True)
        h_box_dis.append(dis_label)
        h_box_dis.append(scale_dis)
        slider_card.append(h_box_dis)

        main_box.append(slider_card)

        # ---------------------------------------------------------------------
        # 2. Toggles
        # ---------------------------------------------------------------------
        main_box.append(self._make_section_header("Toggles (Switches & Checks)"))

        toggle_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        
        # Switches
        sw_box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        sw_off = Gtk.Switch()
        sw_off.set_valign(Gtk.Align.CENTER)
        sw_off.set_active(False)
        sw_box1.append(sw_off)
        sw_box1.append(Gtk.Label(label="Off"))

        sw_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        sw_on = Gtk.Switch()
        sw_on.set_valign(Gtk.Align.CENTER)
        sw_on.set_active(True)
        sw_box2.append(sw_on)
        sw_box2.append(Gtk.Label(label="On"))

        # Checks & Radios
        chk = Gtk.CheckButton(label="Checkbox", active=True)
        chk.set_valign(Gtk.Align.CENTER)
        rad1 = Gtk.CheckButton(label="Radio 1", active=True)
        rad1.set_valign(Gtk.Align.CENTER)
        rad2 = Gtk.CheckButton(label="Radio 2")
        rad2.set_valign(Gtk.Align.CENTER)
        rad2.set_group(rad1)

        toggle_row.append(sw_box1)
        toggle_row.append(sw_box2)
        toggle_row.append(chk)
        toggle_row.append(rad1)
        toggle_row.append(rad2)
        main_box.append(toggle_row)

        # ---------------------------------------------------------------------
        # 3. Drop Downs
        # ---------------------------------------------------------------------
        main_box.append(self._make_section_header("Drop Downs (DropDown & SplitButton)"))

        dd_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

        # Standard DropDown
        options = Gtk.StringList.new(["DropDown", "Option B", "Option C"])
        dropdown = Gtk.DropDown(model=options)
        dropdown.set_selected(0)
        dropdown.set_valign(Gtk.Align.CENTER)
        dd_pop = dropdown.get_first_child().get_next_sibling()
        if hasattr(dd_pop, "set_has_arrow"):
            dd_pop.set_has_arrow(False)
            dd_pop.set_offset(-88, 0)
        dd_row.append(dropdown)

        split_btn = Adw.SplitButton(label="SplitButton")
        split_btn.set_valign(Gtk.Align.CENTER)
        menu = Gio.Menu()
        menu.append("Option 1", "app.noop")
        menu.append("Option 2", "app.noop")
        menu.append("Option 3", "app.noop")
        split_btn.set_menu_model(menu)
        sb_pop = split_btn.get_popover()
        sb_pop.set_has_arrow(False)
        sb_pop.set_offset(-88, 0)
        dd_row.append(split_btn)

        main_box.append(dd_row)

        # ---------------------------------------------------------------------
        # 4. Rollers (SpinButtons)
        # ---------------------------------------------------------------------
        main_box.append(self._make_section_header("Rollers (SpinButtons / Steppers)"))

        roller_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)

        # Horizontal SpinButton
        h_spin_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        h_spin_box.append(Gtk.Label(label="Value:"))
        spin_h = Gtk.SpinButton.new_with_range(0, 100, 1)
        spin_h.set_valign(Gtk.Align.CENTER)
        spin_h.set_alignment(0.5)
        spin_h.set_value(3)
        # Reorder so minus button is on the left, matching Caelestia
        text_w = spin_h.get_first_child()
        btn_down = text_w.get_next_sibling()
        btn_down.insert_before(spin_h, text_w)
        h_spin_box.append(spin_h)
        roller_row.append(h_spin_box)

        # Vertical SpinButton
        v_spin_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        v_spin_box.append(Gtk.Label(label="Vertical:"))
        spin_v = Gtk.SpinButton.new_with_range(0, 10, 1)
        spin_v.set_orientation(Gtk.Orientation.VERTICAL)
        spin_v.set_valign(Gtk.Align.CENTER)
        spin_v.set_alignment(0.5)
        spin_v.set_value(5)
        v_spin_box.append(spin_v)
        roller_row.append(v_spin_box)

        main_box.append(roller_row)

        # ---------------------------------------------------------------------
        # 5. Button Rows & Action Rows (Hyprmod Style)
        # ---------------------------------------------------------------------
        main_box.append(self._make_section_header("Button Rows & Action Rows (Hyprmod)"))

        pref_group = Adw.PreferencesGroup()
        pref_group.set_title("Managed Settings &amp; Actions")
        pref_group.set_description("ActionRows with suffix button strips, pill buttons, indicators &amp; chevrons")

        # Header suffix button (like in Hyprmod section headers)
        add_header_btn = Gtk.Button(icon_name="list-add-symbolic")
        add_header_btn.add_css_class("flat")
        add_header_btn.set_valign(Gtk.Align.CENTER)
        add_header_btn.set_tooltip_text("Add new item")
        pref_group.set_header_suffix(add_header_btn)

        # 1. ActionRow with Action Strip (Discard / Run / Delete) & option-managed
        row1 = Adw.ActionRow(
            title="Autostart Application",
            subtitle="kitty --hold fastfetch",
        )
        row1.add_prefix(Gtk.Image.new_from_icon_name("system-run-symbolic"))
        row1.add_css_class("option-managed")

        actions_box = Gtk.Box(spacing=4)
        actions_box.set_valign(Gtk.Align.CENTER)
        actions_box.add_css_class("reset-button")

        discard_btn = Gtk.Button(icon_name="edit-undo-symbolic")
        discard_btn.add_css_class("flat")
        discard_btn.set_valign(Gtk.Align.CENTER)
        discard_btn.set_tooltip_text("Discard changes")

        run_btn = Gtk.Button(icon_name="system-run-symbolic")
        run_btn.add_css_class("flat")
        run_btn.set_valign(Gtk.Align.CENTER)
        run_btn.set_tooltip_text("Run command now")

        trash_btn = Gtk.Button(icon_name="user-trash-symbolic")
        trash_btn.add_css_class("flat")
        trash_btn.set_valign(Gtk.Align.CENTER)
        trash_btn.set_tooltip_text("Remove entry")

        actions_box.append(discard_btn)
        actions_box.append(run_btn)
        actions_box.append(trash_btn)
        row1.add_suffix(actions_box)
        pref_group.add(row1)

        # 2. ActionRow with Suffix Pill Button & More MenuButton & option-dirty
        row2 = Adw.ActionRow(
            title="Active Profile (Modified)",
            subtitle="Unsaved changes pending disk write",
        )
        row2.add_prefix(Gtk.Image.new_from_icon_name("user-bookmarks-symbolic"))
        row2.add_css_class("option-dirty")

        save_pill = Gtk.Button(label="Save Current")
        save_pill.add_css_class("suggested-action")
        save_pill.add_css_class("pill")
        save_pill.set_valign(Gtk.Align.CENTER)
        row2.add_suffix(save_pill)

        more_mb = Gtk.MenuButton(icon_name="view-more-symbolic")
        more_mb.add_css_class("flat")
        more_mb.add_css_class("circular")
        more_mb.set_valign(Gtk.Align.CENTER)
        more_menu = Gio.Menu()
        more_menu.append("Rename Profile", "app.noop")
        more_menu.append("Duplicate Profile", "app.noop")
        more_menu.append("Export Configuration", "app.noop")
        more_mb.set_menu_model(more_menu)
        row2.add_suffix(more_mb)
        pref_group.add(row2)

        # 3. Activatable Navigation Row with Chevron
        row3 = Adw.ActionRow(
            title="Bezier Curve Editor",
            subtitle="Create and manage custom animation curves",
        )
        row3.add_prefix(Gtk.Image.new_from_icon_name("draw-arc-symbolic"))
        row3.set_activatable(True)
        chevron = Gtk.Image.new_from_icon_name("go-next-symbolic")
        chevron.set_valign(Gtk.Align.CENTER)
        row3.add_suffix(chevron)
        pref_group.add(row3)

        # 4. EntryRow with Apply Button & Browse Suffix Button
        entry_row = Adw.EntryRow(title="Config File Path")
        entry_row.set_text("~/.config/hypr/hyprland.conf")
        entry_row.set_show_apply_button(True)
        browse_btn = Gtk.Button(icon_name="document-open-symbolic")
        browse_btn.add_css_class("flat")
        browse_btn.set_valign(Gtk.Align.CENTER)
        browse_btn.set_tooltip_text("Browse…")
        entry_row.add_suffix(browse_btn)
        pref_group.add(entry_row)

        # 5. Adw.ButtonRow (if available in Libadwaita)
        if hasattr(Adw, "ButtonRow"):
            btn_row_add = Adw.ButtonRow(
                title="Add Workspace Rule",
                start_icon_name="list-add-symbolic",
            )
            btn_row_add.add_css_class("suggested-action")
            pref_group.add(btn_row_add)

            btn_row_clear = Adw.ButtonRow(
                title="Reset All Overrides to Default",
                start_icon_name="edit-clear-symbolic",
            )
            btn_row_clear.add_css_class("destructive-action")
            pref_group.add(btn_row_clear)

        # 6. ComboRow (SelectRow with SplitButton suffix)
        combo_row = Adw.ComboRow(
            title="Layout",
            subtitle="Which layout to use for tiling",
        )
        combo_model = Gtk.StringList.new(["Dwindle", "Master", "Scrolling", "Monocle"])
        combo_row.set_model(combo_model)
        combo_row.set_selected(0)
        pref_group.add(combo_row)

        # 7. ActionRow with SplitButton Suffix
        row_split = Adw.ActionRow(
            title="Profile Synchronization",
            subtitle="Save active settings with profile options",
        )
        row_split.add_prefix(Gtk.Image.new_from_icon_name("document-save-symbolic"))
        row_split.add_css_class("option-managed")

        split_suffix = Adw.SplitButton(label="Save now")
        split_suffix.add_css_class("suggested-action")
        split_suffix.set_valign(Gtk.Align.CENTER)
        save_menu = Gio.Menu()
        save_menu.append("Save without updating profile", "app.noop")
        save_menu.append("Save as new profile…", "app.noop")
        save_menu.append("Export to file…", "app.noop")
        split_suffix.set_menu_model(save_menu)
        ss_pop = split_suffix.get_popover()
        ss_pop.set_has_arrow(False)
        ss_pop.set_offset(-88, 0)
        row_split.add_suffix(split_suffix)
        pref_group.add(row_split)

        main_box.append(pref_group)

        # ---------------------------------------------------------------------
        # 6. Hyprmod Unsaved Changes Banner (SplitButton)
        # ---------------------------------------------------------------------
        main_box.append(self._make_section_header("Hyprmod Dirty Save Banner"))

        banner_card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        banner_card.add_css_class("card")
        banner_card.set_margin_top(4)
        banner_card.set_margin_bottom(8)
        banner_card.set_margin_start(2)
        banner_card.set_margin_end(2)

        warn_icon = Gtk.Image.new_from_icon_name("dialog-warning-symbolic")
        warn_icon.add_css_class("warning")
        warn_icon.set_valign(Gtk.Align.CENTER)
        banner_card.append(warn_icon)

        banner_label = Gtk.Label(label="Unsaved changes — applied live, not saved to disk")
        banner_label.set_hexpand(True)
        banner_label.set_xalign(0)
        banner_label.set_valign(Gtk.Align.CENTER)
        banner_card.append(banner_label)

        banner_discard = Gtk.Button(label="Discard")
        banner_discard.set_valign(Gtk.Align.CENTER)
        banner_card.append(banner_discard)

        banner_split = Adw.SplitButton(label="Save now")
        banner_split.add_css_class("suggested-action")
        banner_split.set_valign(Gtk.Align.CENTER)
        b_menu = Gio.Menu()
        b_menu.append("Save without updating profile", "app.noop")
        b_menu.append("Save as new profile", "app.noop")
        banner_split.set_menu_model(b_menu)
        b_pop = banner_split.get_popover()
        b_pop.set_has_arrow(False)
        b_pop.set_offset(-88, 0)
        banner_card.append(banner_split)

        main_box.append(banner_card)

    def _make_section_header(self, title: str) -> Gtk.Label:
        label = Gtk.Label(xalign=0)
        label.set_markup(f"<span size='large' weight='bold'>{GLib.markup_escape_text(title)}</span>")
        label.set_margin_top(8)
        return label

    def load_css(self):
        css_path = os.path.expanduser("~/.config/gtk-4.0/gtk.css")
        if os.path.exists(css_path):
            provider = Gtk.CssProvider()
            provider.load_from_path(css_path)
            Gtk.StyleContext.add_provider_for_display(
                self.get_display(),
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_USER
            )


def on_activate(app):
    win = ThemeTestWindow(application=app)
    win.present()


def main():
    app = Adw.Application(application_id="com.caelestia.themetest", flags=Gio.ApplicationFlags.FLAGS_NONE)
    
    # Dummy action for menu items
    action = Gio.SimpleAction.new("noop", None)
    app.add_action(action)

    app.connect("activate", on_activate)
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
