#!/usr/bin/env python3
"""Generate button-design-editor.html — run once, output beside this script."""
import json
from pathlib import Path

OUT = Path(__file__).with_name("button-design-editor.html")

VARIANTS = {
    "solid": ["primary"],
    "soft": ["primary", "secondary"],
    "surface": ["primary", "secondary"],
    "outline": ["primary", "secondary"],
    "ghost": ["primary", "secondary", "tertiary", "quaternary"],
    "text": ["primary", "secondary", "tertiary", "quaternary"],
}
LINK_HIERARCHIES = ["primary", "secondary", "tertiary", "quaternary"]
STATES = ["default", "hover", "pressed", "disabled", "focus"]

SIZE_DEFAULTS = {
    "--btn-height-xs": "24px",
    "--btn-height-sm": "28px",
    "--btn-height-default": "32px",
    "--btn-height-lg": "40px",
    "--btn-padding-x-xs": "8px",
    "--btn-padding-x-sm": "12px",
    "--btn-padding-x-default": "16px",
    "--btn-padding-x-lg": "20px",
    "--btn-padding-y-xs": "0px",
    "--btn-padding-y-sm": "0px",
    "--btn-padding-y-default": "0px",
    "--btn-padding-y-lg": "0px",
    "--btn-radius-xs": "6px",
    "--btn-radius-sm": "6px",
    "--btn-radius-default": "8px",
    "--btn-radius-lg": "8px",
    "--btn-font-size-xs": "12px",
    "--btn-font-size-sm": "12px",
    "--btn-font-size-default": "14px",
    "--btn-font-size-lg": "16px",
    "--btn-line-height-xs": "22px",
    "--btn-line-height-sm": "26px",
    "--btn-line-height-default": "30px",
    "--btn-line-height-lg": "38px",
    "--btn-icon-size-xs": "14px",
    "--btn-icon-size-sm": "14px",
    "--btn-icon-size-default": "16px",
    "--btn-icon-size-lg": "18px",
    "--btn-gap": "4px",
    "--btn-border-width": "1px",
    "--btn-font-weight": "400",
    "--btn-font-weight-solid": "500",
    "--btn-transition": "0.2s ease",
    "--btn-focus-ring-width": "2px",
    "--btn-focus-ring-color": "rgb(var(--fc-fill-5-rgb) / 0.35)",
}


def combo_defaults(variant, hierarchy, destructive=False):
    if variant == "solid" and hierarchy == "primary":
        if destructive:
            rows = [
                ("var(--fc-red-9)", "transparent", "#fff"),
                ("var(--fc-red-10)", "transparent", "#fff"),
                ("var(--fc-red-11)", "transparent", "#fff"),
                ("var(--fc-red-3)", "transparent", "var(--fc-red-6)"),
                ("transparent", "var(--fc-red-9)", "var(--fc-red-9)"),
            ]
        else:
            rows = [
                ("var(--fc-violet-9)", "transparent", "#fff"),
                ("var(--fc-violet-10)", "transparent", "#fff"),
                ("var(--fc-violet-11)", "transparent", "#fff"),
                ("var(--fc-fill-3)", "transparent", "var(--fc-text-5)"),
                ("transparent", "var(--fc-violet-9)", "var(--fc-violet-9)"),
            ]
        return {st: rows[i] for i, st in enumerate(STATES)}
    if variant in ("soft", "surface"):
        if hierarchy == "primary":
            if destructive:
                rows = [
                    ("var(--fc-red-3)", "var(--fc-red-8)", "var(--fc-red-11)"),
                    ("var(--fc-red-4)", "var(--fc-red-9)", "var(--fc-red-12)"),
                    ("var(--fc-red-5)", "var(--fc-red-9)", "var(--fc-red-12)"),
                    ("transparent", "var(--fc-border-color)", "var(--fc-text-5)"),
                    ("transparent", "var(--fc-red-9)", "var(--fc-red-11)"),
                ]
            else:
                base = "var(--fc-violet-3)" if variant == "soft" else "var(--fc-fill-2)"
                rows = [
                    (base, "var(--fc-border-color2)", "var(--fc-violet-11)"),
                    ("var(--fc-violet-4)", "var(--fc-violet-8)", "var(--fc-violet-12)"),
                    ("var(--fc-violet-5)", "var(--fc-violet-9)", "var(--fc-violet-12)"),
                    ("transparent", "var(--fc-border-color)", "var(--fc-text-5)"),
                    ("transparent", "var(--fc-violet-9)", "var(--fc-violet-11)"),
                ]
        elif destructive:
            rows = [
                ("var(--fc-red-3)", "var(--fc-red-8)", "var(--fc-red-11)"),
                ("var(--fc-red-4)", "var(--fc-red-9)", "var(--fc-red-12)"),
                ("var(--fc-red-5)", "var(--fc-red-9)", "var(--fc-red-12)"),
                ("transparent", "var(--fc-border-color)", "var(--fc-text-5)"),
                ("transparent", "var(--fc-red-9)", "var(--fc-red-11)"),
            ]
        else:
            rows = [
                ("var(--fc-fill-2)", "var(--fc-border-color2)", "var(--fc-text-2)"),
                ("rgb(var(--fc-fill-5-rgb) / 0.2)", "var(--fc-border-color2)", "var(--fc-text-1)"),
                ("rgb(var(--fc-fill-5-rgb) / 0.4)", "var(--fc-border-color2)", "var(--fc-text-1)"),
                ("transparent", "var(--fc-border-color)", "var(--fc-text-5)"),
                ("transparent", "var(--fc-border-color2)", "var(--fc-text-2)"),
            ]
        return {st: rows[i] for i, st in enumerate(STATES)}
    if variant == "outline":
        if hierarchy == "primary":
            rows = (
                [
                    ("transparent", "var(--fc-red-8)", "var(--fc-red-11)"),
                    ("var(--fc-red-3)", "var(--fc-red-9)", "var(--fc-red-12)"),
                    ("var(--fc-red-4)", "var(--fc-red-9)", "var(--fc-red-12)"),
                    ("transparent", "var(--fc-border-color)", "var(--fc-text-5)"),
                    ("transparent", "var(--fc-red-9)", "var(--fc-red-11)"),
                ]
                if destructive
                else [
                    ("transparent", "var(--fc-violet-8)", "var(--fc-violet-11)"),
                    ("var(--fc-violet-3)", "var(--fc-violet-9)", "var(--fc-violet-12)"),
                    ("var(--fc-violet-4)", "var(--fc-violet-9)", "var(--fc-violet-12)"),
                    ("transparent", "var(--fc-border-color)", "var(--fc-text-5)"),
                    ("transparent", "var(--fc-violet-9)", "var(--fc-violet-11)"),
                ]
            )
        elif destructive:
            rows = [
                ("transparent", "var(--fc-red-8)", "var(--fc-red-11)"),
                ("var(--fc-red-3)", "var(--fc-red-9)", "var(--fc-red-12)"),
                ("var(--fc-red-4)", "var(--fc-red-9)", "var(--fc-red-12)"),
                ("transparent", "var(--fc-border-color)", "var(--fc-text-5)"),
                ("transparent", "var(--fc-red-9)", "var(--fc-red-11)"),
            ]
        else:
            rows = [
                ("transparent", "var(--fc-border-color2)", "var(--fc-text-2)"),
                ("rgb(var(--fc-fill-5-rgb) / 0.2)", "var(--fc-border-color2)", "var(--fc-text-1)"),
                ("rgb(var(--fc-fill-5-rgb) / 0.4)", "var(--fc-border-color2)", "var(--fc-text-1)"),
                ("transparent", "var(--fc-border-color)", "var(--fc-text-5)"),
                ("transparent", "var(--fc-border-color2)", "var(--fc-text-2)"),
            ]
        return {st: rows[i] for i, st in enumerate(STATES)}
    if variant in ("ghost", "text"):
        if hierarchy == "primary":
            rows = (
                [
                    ("transparent", "transparent", "var(--fc-red-11)"),
                    ("var(--fc-red-3)", "transparent", "var(--fc-red-11)"),
                    ("var(--fc-red-4)", "transparent", "var(--fc-red-12)"),
                    ("transparent", "transparent", "var(--fc-red-6)"),
                    ("transparent", "var(--fc-red-9)", "var(--fc-red-11)"),
                ]
                if destructive
                else [
                    ("transparent", "transparent", "var(--fc-violet-11)"),
                    ("var(--fc-violet-3)", "transparent", "var(--fc-violet-11)"),
                    ("var(--fc-violet-4)", "transparent", "var(--fc-violet-12)"),
                    ("transparent", "transparent", "var(--fc-violet-6)"),
                    ("transparent", "var(--fc-violet-9)", "var(--fc-violet-11)"),
                ]
            )
        elif hierarchy == "secondary":
            rows = [
                ("transparent", "transparent", "var(--fc-text-2)"),
                ("rgb(var(--fc-fill-5-rgb) / 0.2)", "transparent", "var(--fc-text-1)"),
                ("rgb(var(--fc-fill-5-rgb) / 0.4)", "transparent", "var(--fc-text-1)"),
                ("transparent", "transparent", "var(--fc-text-5)"),
                ("transparent", "var(--fc-border-color2)", "var(--fc-text-2)"),
            ]
        elif hierarchy == "tertiary":
            rows = [
                ("transparent", "transparent", "var(--fc-text-3)"),
                ("rgb(var(--fc-fill-5-rgb) / 0.2)", "transparent", "var(--fc-text-2)"),
                ("rgb(var(--fc-fill-5-rgb) / 0.4)", "transparent", "var(--fc-text-1)"),
                ("transparent", "transparent", "var(--fc-text-5)"),
                ("transparent", "var(--fc-border-color2)", "var(--fc-text-3)"),
            ]
        else:
            rows = [
                ("transparent", "transparent", "var(--fc-text-4)"),
                ("rgb(var(--fc-fill-5-rgb) / 0.4)", "transparent", "var(--fc-text-2)"),
                ("rgb(var(--fc-fill-5-rgb) / 0.7)", "transparent", "var(--fc-text-1)"),
                ("transparent", "transparent", "var(--fc-text-5)"),
                ("transparent", "var(--fc-border-color2)", "var(--fc-text-4)"),
            ]
        return {st: rows[i] for i, st in enumerate(STATES)}
    return {st: ("transparent", "transparent", "var(--fc-text-3)") for st in STATES}


def link_defaults(hierarchy):
    colors = {
        "primary": ("var(--fc-violet-11)", "var(--fc-violet-12)", "var(--fc-violet-6)"),
        "secondary": ("var(--fc-text-2)", "var(--fc-text-1)", "var(--fc-text-5)"),
        "tertiary": ("var(--fc-text-3)", "var(--fc-text-2)", "var(--fc-text-5)"),
        "quaternary": ("var(--fc-text-4)", "var(--fc-text-2)", "var(--fc-text-5)"),
    }
    d, h, dis = colors[hierarchy]
    return {
        "default-text": d,
        "hover-text": h,
        "pressed-text": h,
        "disabled-text": dis,
        "default-underline": "transparent",
        "hover-underline": "currentColor",
        "always-underline": "currentColor",
    }


COLOR_DEFAULTS = dict(SIZE_DEFAULTS)
SPEC_ROWS = []
for sk, _ in SIZE_DEFAULTS.items():
    SPEC_ROWS.append(["尺寸", sk, sk.replace("--btn-", "")])

for variant, hierarchies in VARIANTS.items():
    for h in hierarchies:
        for destructive in [False, True]:
            if destructive and variant == "solid" and h != "primary":
                continue
            if destructive and variant in ("ghost", "text") and h in ("tertiary", "quaternary"):
                continue
            tag = f"{variant} · {h}" + (" · destructive" if destructive else "")
            defs = combo_defaults(variant, h, destructive)
            suffix = "-destructive" if destructive else ""
            for state in STATES:
                bg, border, text = defs[state]
                for prop, val in [("bg", bg), ("border", border), ("text", text)]:
                    key = f"--btn-{variant}-{h}{suffix}-{state}-{prop}"
                    COLOR_DEFAULTS[key] = val
                    SPEC_ROWS.append([tag, key, f"{state} · {prop}"])

for h in LINK_HIERARCHIES:
    tag = f"link · {h}"
    for k, v in link_defaults(h).items():
        key = f"--btn-link-{h}-{k}"
        COLOR_DEFAULTS[key] = v
        SPEC_ROWS.append([tag, key, k])

SHARED_KEYS = set(SIZE_DEFAULTS)
UNIFIED_COLOR_KEYS = set(COLOR_DEFAULTS) - SHARED_KEYS
GOLD_DEFAULTS = {
    "--btn-solid-primary-default-bg": "#ffbc0d",
    "--btn-solid-primary-hover-bg": "#ffcd36",
    "--btn-solid-primary-pressed-bg": "#e6a800",
    "--btn-solid-primary-default-text": "rgba(0,0,0,0.85)",
    "--btn-link-primary-default-text": "#db0007",
}

css_root = "\n".join(f"      {k}: {v};" for k, v in COLOR_DEFAULTS.items())
css_rules = []
for variant, hierarchies in VARIANTS.items():
    for h in hierarchies:
        for destructive in [False, True]:
            if destructive and variant == "solid" and h != "primary":
                continue
            if destructive and variant in ("ghost", "text") and h in ("tertiary", "quaternary"):
                continue
            suffix = "-destructive" if destructive else ""
            sel = f'.fc-btn[data-variant="{variant}"][data-hierarchy="{h}"]'
            sel += '[data-destructive="true"]' if destructive else ':not([data-destructive="true"])'
            css_rules.append(
                f"""    {sel} {{
      background: var(--btn-{variant}-{h}{suffix}-default-bg);
      border-color: var(--btn-{variant}-{h}{suffix}-default-border);
      color: var(--btn-{variant}-{h}{suffix}-default-text);
    }}
    {sel}:hover:not(:disabled), {sel}.is-hover {{
      background: var(--btn-{variant}-{h}{suffix}-hover-bg);
      border-color: var(--btn-{variant}-{h}{suffix}-hover-border);
      color: var(--btn-{variant}-{h}{suffix}-hover-text);
    }}
    {sel}:active:not(:disabled), {sel}.is-pressed {{
      background: var(--btn-{variant}-{h}{suffix}-pressed-bg);
      border-color: var(--btn-{variant}-{h}{suffix}-pressed-border);
      color: var(--btn-{variant}-{h}{suffix}-pressed-text);
    }}
    {sel}:disabled, {sel}.is-disabled {{
      background: var(--btn-{variant}-{h}{suffix}-disabled-bg);
      border-color: var(--btn-{variant}-{h}{suffix}-disabled-border);
      color: var(--btn-{variant}-{h}{suffix}-disabled-text);
      cursor: not-allowed;
    }}
    {sel}:focus-visible, {sel}.is-focus {{
      outline: var(--btn-focus-ring-width) solid var(--btn-focus-ring-color);
      outline-offset: 1px;
    }}"""
            )

link_css = []
for h in LINK_HIERARCHIES:
    link_css.append(
        f"""    .fc-link[data-hierarchy="{h}"] {{
      color: var(--btn-link-{h}-default-text);
      text-decoration-color: var(--btn-link-{h}-default-underline);
    }}
    .fc-link[data-hierarchy="{h}"][data-underline="always"] {{
      text-decoration: underline;
      text-decoration-color: var(--btn-link-{h}-always-underline);
    }}
    .fc-link[data-hierarchy="{h}"][data-underline="hover"]:hover,
    .fc-link[data-hierarchy="{h}"].is-hover {{
      color: var(--btn-link-{h}-hover-text);
      text-decoration: underline;
      text-decoration-color: var(--btn-link-{h}-hover-underline);
    }}
    .fc-link[data-hierarchy="{h}"]:disabled, .fc-link[data-hierarchy="{h}"].is-disabled {{
      color: var(--btn-link-{h}-disabled-text);
      cursor: not-allowed;
    }}"""
    )

# Read template from pagination for shared theme blocks - inline minimal version
html = Path(__file__).read_text(encoding="utf-8")
# This file is only the generator; full HTML built below
if __name__ == "__main__":
    spec_rows_json = json.dumps(SPEC_ROWS, ensure_ascii=False)
    color_defaults_json = json.dumps(COLOR_DEFAULTS, ensure_ascii=False)
    gold_json = json.dumps(GOLD_DEFAULTS, ensure_ascii=False)
    variants_json = json.dumps(VARIANTS, ensure_ascii=False)
    link_json = json.dumps(LINK_HIERARCHIES, ensure_ascii=False)
    shared_json = json.dumps(list(SHARED_KEYS))
    unified_json = json.dumps(list(UNIFIED_COLOR_KEYS))

    content = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>FC 按钮 · 设计调参稿</title>
  <style>
    :root {{
{css_root}
    }}
    html[data-theme="light"], html:not([data-theme]) {{
      --fc-fill-1-rgb: 252 252 253; --fc-fill-1: rgb(var(--fc-fill-1-rgb));
      --fc-fill-2-rgb: 255 255 255; --fc-fill-2: rgb(var(--fc-fill-2-rgb));
      --fc-fill-3-rgb: 244 244 246; --fc-fill-3: rgb(var(--fc-fill-3-rgb));
      --fc-fill-5-rgb: 228 228 231; --fc-fill-5: rgb(var(--fc-fill-5-rgb));
      --fc-text-1: #0c1018; --fc-text-2: #181c25; --fc-text-3: #3f4856;
      --fc-text-4: #657386; --fc-text-5: #65738666;
      --fc-border-color: hsla(240, 5%, 89%, 0.7); --fc-border-color2: hsla(240, 5%, 89%);
      --fc-violet-3: #2500ed0e; --fc-violet-4: #2800ff1a; --fc-violet-5: #2a00ff25;
      --fc-violet-8: #2700bd64; --fc-violet-9-rgb: 108, 83, 177; --fc-violet-9: rgb(var(--fc-violet-9-rgb));
      --fc-violet-10-rgb: 95, 69, 161; --fc-violet-10: rgb(var(--fc-violet-10-rgb));
      --fc-violet-11-rgb: 107, 81, 175; --fc-violet-11: rgb(var(--fc-violet-11-rgb));
      --fc-violet-12-rgb: 52, 38, 89; --fc-violet-12: rgb(var(--fc-violet-12-rgb));
      --fc-red-3: #ff00000e; --fc-red-4: #ff0d001a; --fc-red-5: #ff150025;
      --fc-red-6: #ff0f0034; --fc-red-8: #ff4d4d64; --fc-red-9: #e5484d;
      --fc-red-10: #dc3e43; --fc-red-11: #ce2c31; --fc-red-12: #641723;
    }}
    html[data-theme="dark"] {{
      color-scheme: dark;
      --fc-fill-1-rgb: 12 12 14; --fc-fill-2-rgb: 22 22 24; --fc-fill-2: rgb(var(--fc-fill-2-rgb));
      --fc-fill-5-rgb: 44 44 48; --fc-text-1: rgb(242,242,242); --fc-text-2: rgb(201,201,207);
      --fc-text-3: rgb(135,135,146); --fc-text-4: rgb(109,109,120); --fc-text-5: rgb(68,68,75);
      --fc-border-color: rgba(255,255,255,0.06); --fc-border-color2: rgba(255,255,255,0.08);
      --fc-violet-3: #683bfc38; --fc-violet-4: #7138ff54; --fc-violet-5: #7a49fd64;
      --fc-violet-8: #8f6cffb2; --fc-violet-9-rgb: 148,112,255; --fc-violet-9: rgb(var(--fc-violet-9-rgb));
      --fc-violet-10-rgb: 136,99,241; --fc-violet-10: rgb(var(--fc-violet-10-rgb));
      --fc-violet-11-rgb: 184,164,255; --fc-violet-11: rgb(var(--fc-violet-11-rgb));
      --fc-violet-12-rgb: 225,220,255; --fc-violet-12: rgb(var(--fc-violet-12-rgb));
      --fc-red-9: #ff6b6b; --fc-red-10: #ff5252; --fc-red-11: #ff8a8a;
      --btn-focus-ring-color: rgb(var(--fc-fill-5-rgb) / 0.5);
    }}
    [data-theme="gold"] {{
      --preview-page-bg: #fcfcfd; --preview-panel-bg: #fff; --preview-text: #181c25; --preview-muted: #657386;
      --btn-solid-primary-default-bg: #ffbc0d; --btn-solid-primary-hover-bg: #ffcd36;
      --btn-solid-primary-default-text: rgba(0,0,0,0.85); --btn-link-primary-default-text: #db0007;
    }}
    html[data-theme="light"] body, html:not([data-theme]) body {{
      --preview-page-bg: var(--fc-fill-1); --preview-panel-bg: var(--fc-fill-2);
      --preview-text: var(--fc-text-2); --preview-muted: var(--fc-text-4); --preview-border: var(--fc-border-color2);
    }}
    html[data-theme="dark"] body {{
      --preview-page-bg: var(--fc-fill-1); --preview-panel-bg: var(--fc-fill-2);
      --preview-text: var(--fc-text-2); --preview-muted: var(--fc-text-4); --preview-border: var(--fc-border-color2);
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; background: var(--preview-page-bg); color: var(--preview-text);
      font-family: "PingFang SC", -apple-system, sans-serif; font-size: 12px; }}
    main {{ width: min(1100px, calc(100vw - 48px)); margin: 32px auto 64px; }}
    h1 {{ margin: 0 0 8px; font-size: 22px; font-weight: 600; }}
    .intro {{ margin: 0 0 20px; color: var(--preview-muted); font-size: 13px; line-height: 1.65; }}
    .intro code {{ padding: 1px 6px; border-radius: 4px; background: var(--fc-fill-3); }}
    section {{ margin-bottom: 24px; padding: 20px 24px; border: 1px solid var(--preview-border);
      border-radius: 8px; background: var(--preview-panel-bg); }}
    section h2 {{ margin: 0 0 6px; font-size: 15px; font-weight: 600; }}
    section .desc {{ margin: 0 0 14px; color: var(--preview-muted); font-size: 12px; line-height: 1.5; }}
    .theme-toggle, .filter-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; align-items: center; }}
    .theme-toggle button, .filter-row button, .filter-row select {{
      padding: 6px 12px; border: 1px solid var(--preview-border); border-radius: 6px;
      background: var(--preview-panel-bg); color: var(--preview-muted); font: inherit; font-size: 12px; cursor: pointer;
    }}
    .theme-toggle button.is-on, .filter-row button.is-on {{
      border-color: var(--fc-violet-9); color: var(--fc-violet-11);
      background: color-mix(in srgb, var(--fc-violet-9) 8%, var(--preview-panel-bg));
    }}
    .filter-row label {{ color: var(--preview-muted); font-size: 12px; }}
    .filter-row select {{ min-width: 110px; }}
    .theme-note {{ margin: 0 0 12px; padding: 10px 12px; border-radius: 6px;
      background: color-mix(in srgb, var(--fc-violet-9) 6%, var(--preview-panel-bg));
      color: var(--preview-muted); font-size: 12px; }}
    .fc-btn {{ display: inline-flex; align-items: center; justify-content: center; gap: var(--btn-gap);
      border: var(--btn-border-width) solid transparent; font: inherit; font-weight: var(--btn-font-weight);
      line-height: 1; cursor: pointer; white-space: nowrap;
      transition: background var(--btn-transition), border-color var(--btn-transition), color var(--btn-transition);
    }}
    .fc-btn[data-variant="solid"] {{ font-weight: var(--btn-font-weight-solid); }}
    .fc-btn[data-size="xs"] {{ height: var(--btn-height-xs); padding: var(--btn-padding-y-xs) var(--btn-padding-x-xs);
      border-radius: var(--btn-radius-xs); font-size: var(--btn-font-size-xs); line-height: var(--btn-line-height-xs); }}
    .fc-btn[data-size="sm"] {{ height: var(--btn-height-sm); padding: var(--btn-padding-y-sm) var(--btn-padding-x-sm);
      border-radius: var(--btn-radius-sm); font-size: var(--btn-font-size-sm); line-height: var(--btn-line-height-sm); }}
    .fc-btn[data-size="default"] {{ height: var(--btn-height-default); padding: var(--btn-padding-y-default) var(--btn-padding-x-default);
      border-radius: var(--btn-radius-default); font-size: var(--btn-font-size-default); line-height: var(--btn-line-height-default); }}
    .fc-btn[data-size="lg"] {{ height: var(--btn-height-lg); padding: var(--btn-padding-y-lg) var(--btn-padding-x-lg);
      border-radius: var(--btn-radius-lg); font-size: var(--btn-font-size-lg); line-height: var(--btn-line-height-lg); }}
    .fc-btn .lucide {{ width: var(--btn-icon-size-default); height: var(--btn-icon-size-default); flex: none; }}
    .fc-btn[data-size="xs"] .lucide {{ width: var(--btn-icon-size-xs); height: var(--btn-icon-size-xs); }}
    .fc-btn[data-variant="text"] {{ background: transparent !important; border-color: transparent !important; }}
{chr(10).join(css_rules)}
{chr(10).join(link_css)}
    .fc-link {{ display: inline-flex; align-items: center; gap: var(--btn-gap); border: none; background: none;
      font: inherit; font-size: var(--btn-font-size-default); cursor: pointer; text-decoration: none; padding: 0; }}
    .state-grid {{ display: flex; flex-wrap: wrap; gap: 16px; align-items: flex-end; }}
    .state-cell {{ display: flex; flex-direction: column; gap: 6px; }}
    .state-label {{ color: var(--preview-muted); font-size: 11px; }}
    .matrix-title {{ margin: 14px 0 8px; font-size: 13px; font-weight: 600; color: var(--preview-muted); }}
    .matrix-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 6px; }}
    .spec-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    .spec-table th, .spec-table td {{ border-bottom: 1px solid var(--preview-border); padding: 8px 10px; vertical-align: top; }}
    .value-editor {{ display: flex; align-items: center; gap: 8px; }}
    .spec-input {{ flex: 1; min-width: 140px; padding: 6px 8px; border: 1px solid var(--preview-border);
      border-radius: 6px; background: var(--preview-panel-bg); font: inherit; font-size: 12px; }}
    .spec-color-picker {{ width: 28px; height: 28px; padding: 0; border-radius: 6px; cursor: pointer; }}
    .swatch {{ width: 14px; height: 14px; border-radius: 3px; border: 1px solid rgba(0,0,0,.08); }}
    .action-bar {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 20px;
      padding: 14px 16px; border: 1px solid var(--preview-border); border-radius: 8px; background: var(--preview-panel-bg); }}
    .btn-primary-action {{ padding: 8px 18px; border: none; border-radius: 6px; background: var(--fc-violet-9);
      color: #fff; font: inherit; font-size: 13px; font-weight: 500; cursor: pointer; }}
    .btn-secondary-action {{ padding: 8px 14px; border: 1px solid var(--preview-border); border-radius: 6px;
      background: var(--preview-panel-bg); font: inherit; font-size: 13px; cursor: pointer; }}
    .copy-hint {{ color: var(--preview-muted); font-size: 12px; }}
    .code-output {{ width: 100%; min-height: 220px; margin-top: 10px; padding: 12px; border-radius: 8px;
      background: #1e1e22; color: #e8e8ed; font-family: ui-monospace, Menlo, monospace; font-size: 11px; }}
    #output-section {{ display: none; }} #output-section.is-visible {{ display: block; }}
    #color-probe {{ position: fixed; left: -9999px; visibility: hidden; }}
    .taxonomy-table td {{ padding: 4px 12px 4px 0; color: var(--preview-muted); font-size: 12px; }}
  </style>
</head>
<body data-theme="light">
  <main>
    <h1>FC 按钮 · 设计调参稿</h1>
    <p class="intro">
      分类以 <strong>Figma「设计规范 - 按钮」</strong> 为准：<code>variant</code> × <code>hierarchy</code> × <code>size</code> × <code>icon</code> × <code>destructive</code>；Link 单独。<br />
      初值来自 <code>fe/src/theme/table-design-system.less</code>（ghost 24px）与 Meow UI（default/primary/outline/ghost/link/danger）。填表 → <strong>预览</strong> → <strong>生效</strong> 出代码。
    </p>
    <div class="action-bar">
      <button type="button" class="btn-primary-action" id="btn-preview">预览</button>
      <button type="button" class="btn-primary-action" id="btn-apply-code">生效（生成样式代码）</button>
      <button type="button" class="btn-secondary-action" id="btn-reset-vars">恢复本模式默认</button>
      <button type="button" class="btn-secondary-action" id="btn-filter-all">显示全部参数</button>
      <button type="button" class="btn-secondary-action" id="btn-filter-focus">仅当前组合</button>
      <span class="copy-hint" id="copy-hint"></span>
    </div>
    <div id="preview-scope">
      <div id="color-probe" aria-hidden="true"></div>
      <section>
        <h2>1. 分类与单按钮预览</h2>
        <table class="taxonomy-table">
          <tr><td><strong>variant</strong></td><td>soft · solid · surface · outline · ghost · text</td></tr>
          <tr><td><strong>hierarchy</strong></td><td>tertiary/quaternary 仅 ghost & text；solid 仅 primary</td></tr>
          <tr><td><strong>size</strong></td><td>xs(24) · sm(28) · default(32) · lg(40)</td></tr>
          <tr><td><strong>icon</strong></td><td>none · inline-start · inline-end</td></tr>
        </table>
        <div class="theme-toggle">
          <button type="button" id="theme-light" class="is-on">浅色</button>
          <button type="button" id="theme-dark">深色</button>
          <button type="button" id="theme-gold">金拱门</button>
        </div>
        <p class="theme-note" id="theme-note"></p>
        <div class="filter-row">
          <label>variant <select id="sel-variant"></select></label>
          <label>hierarchy <select id="sel-hierarchy"></select></label>
          <label>size <select id="sel-size"><option value="xs">xs</option><option value="sm">sm</option>
            <option value="default" selected>default</option><option value="lg">lg</option></select></label>
          <label>icon <select id="sel-icon"><option value="none">none</option>
            <option value="inline-start">inline-start</option><option value="inline-end">inline-end</option></select></label>
          <label><input type="checkbox" id="chk-destructive" /> destructive</label>
        </div>
        <p class="desc" id="combo-hint"></p>
        <div id="live-btn-wrap"></div>
      </section>
      <section>
        <h2>2. 状态条（当前组合）</h2>
        <div class="state-grid" id="state-strip"></div>
      </section>
      <section>
        <h2>3. 全量变体矩阵</h2>
        <div id="matrix-all"></div>
      </section>
      <section>
        <h2>4. Link</h2>
        <div class="matrix-row" id="link-strip"></div>
        <div class="state-grid" id="link-state-strip" style="margin-top:12px"></div>
      </section>
    </div>
    <section>
      <h2>5. 参数表</h2>
      <p class="desc">支持 <code>var(--fc-violet-11)</code>、<code>rgb(var(--fc-fill-5-rgb) / 0.4)</code>。默认「仅当前组合」便于逐项调。</p>
      <table class="spec-table" id="spec-table"></table>
      <div id="output-section">
        <h2>6. 生成代码</h2>
        <textarea class="code-output" id="code-output" readonly></textarea>
        <button type="button" class="btn-secondary-action" id="btn-copy-output" style="margin-top:10px">复制</button>
      </div>
    </section>
  </main>
  <style id="runtime-preview-styles"></style>
  <script src="https://cdn.jsdelivr.net/npm/lucide@0.511.0/dist/umd/lucide.min.js"></script>
  <script>
    const VARIANTS = {variants_json};
    const LINK_HIERARCHIES = {link_json};
    const SPEC_ROWS = {spec_rows_json};
    const COLOR_DEFAULTS = {color_defaults_json};
    const SHARED_KEYS = new Set({shared_json});
    const UNIFIED_COLOR_KEYS = new Set({unified_json});
    const STORAGE_KEY = "fc-button-design-editor-v1";
    const userState = {{ shared: {{}}, gold: {{}} }};
    let filterMode = "focus";
    let live = {{ variant: "ghost", hierarchy: "primary", size: "xs", icon: "none", destructive: false }};

    function validHierarchies(v) {{ return VARIANTS[v] || ["primary"]; }}
    function isDestructiveAllowed(v, h) {{
      if (v === "solid") return h === "primary";
      if (v === "ghost" || v === "text") return h === "primary" || h === "secondary";
      return true;
    }}
    function rowMatchesFilter(group) {{
      if (filterMode === "all") return true;
      if (group === "尺寸") return true;
      if (group.startsWith("link")) return true;
      const dest = live.destructive ? " · destructive" : "";
      return group === `${{live.variant}} · ${{live.hierarchy}}${{dest}}`;
    }}
    function renderButtonHtml(o = {{}}) {{
      const v = o.variant ?? live.variant, h = o.hierarchy ?? live.hierarchy, sz = o.size ?? live.size;
      const ic = o.icon ?? live.icon, d = o.destructive ?? live.destructive;
      const cls = o.extraClass || "", dis = o.disabled ? " disabled" : "";
      const dest = d ? ' data-destructive="true"' : "";
      const label = o.text || (h.charAt(0).toUpperCase() + h.slice(1));
      let i0 = ic === "inline-start" ? '<i data-lucide="plus"></i>' : "";
      let i1 = ic === "inline-end" ? '<i data-lucide="chevron-right"></i>' : "";
      return `<button type="button" class="fc-btn ${{cls}}" data-variant="${{v}}" data-hierarchy="${{h}}" data-size="${{sz}}"${{dest}}${{dis}}>${{i0}}${{label}}${{i1}}</button>`;
    }}
    function renderLive() {{
      document.getElementById("live-btn-wrap").innerHTML =
        renderButtonHtml({{ icon: live.icon }}) + " " + renderButtonHtml({{ size: "default", icon: live.icon }});
      document.getElementById("combo-hint").textContent =
        `variant=${{live.variant}} hierarchy=${{live.hierarchy}} size=${{live.size}} icon=${{live.icon}} destructive=${{live.destructive}}`;
      document.getElementById("state-strip").innerHTML = [
        ["默认",""],["Hover","is-hover"],["Pressed","is-pressed"],["Focus","is-focus"],["Disabled","is-disabled"]
      ].map(([l,c]) => `<div class="state-cell"><span class="state-label">${{l}}</span>${{renderButtonHtml({{ extraClass:c, disabled:c==="is-disabled", icon:"inline-start" }})}}</div>`).join("");
      refreshLucide(document.getElementById("preview-scope"));
    }}
    function renderMatrix() {{
      let html = "";
      for (const [variant, list] of Object.entries(VARIANTS)) {{
        html += `<h3 class="matrix-title">${{variant}}</h3><div class="matrix-row">`;
        for (const h of list) html += renderButtonHtml({{ variant, hierarchy: h, size: "default", text: h }});
        html += "</div>";
        const dest = list.filter((h) => isDestructiveAllowed(variant, h));
        if (dest.length) {{
          html += '<div class="matrix-row">';
          for (const h of dest) html += renderButtonHtml({{ variant, hierarchy: h, size: "default", destructive: true, text: "Delete" }});
          html += "</div>";
        }}
      }}
      document.getElementById("matrix-all").innerHTML = html;
      document.getElementById("link-strip").innerHTML =
        LINK_HIERARCHIES.map((h) => `<button type="button" class="fc-link" data-hierarchy="${{h}}" data-underline="hover">${{h}}</button>`).join("") +
        LINK_HIERARCHIES.map((h) => `<button type="button" class="fc-link" data-hierarchy="${{h}}" data-underline="always">${{h}} underline</button>`).join("");
      document.getElementById("link-state-strip").innerHTML = [
        ["默认",""],["Hover","is-hover"],["Disabled","is-disabled"]
      ].map(([l,c]) => `<div class="state-cell"><span class="state-label">${{l}}</span><button type="button" class="fc-link ${{c}}" data-hierarchy="primary" data-underline="hover"${{c==="is-disabled"?" disabled":""}}>Link</button></div>`).join("");
      refreshLucide(document.getElementById("matrix-all"));
    }}
    function refreshLucide(root) {{
      if (typeof lucide !== "undefined" && lucide.createIcons) lucide.createIcons({{ attrs: {{ "stroke-width": 2 }}, root }});
    }}
    function populateSelectors() {{
      const v = document.getElementById("sel-variant");
      v.innerHTML = Object.keys(VARIANTS).map((k) => `<option value="${{k}}">${{k}}</option>`).join("");
      v.value = live.variant;
      updateHierarchySelect();
    }}
    function updateHierarchySelect() {{
      const list = validHierarchies(live.variant);
      const h = document.getElementById("sel-hierarchy");
      h.innerHTML = list.map((x) => `<option value="${{x}}">${{x}}</option>`).join("");
      if (!list.includes(live.hierarchy)) live.hierarchy = list[0];
      h.value = live.hierarchy;
      const chk = document.getElementById("chk-destructive");
      chk.disabled = !isDestructiveAllowed(live.variant, live.hierarchy);
      if (!isDestructiveAllowed(live.variant, live.hierarchy)) live.destructive = false;
      chk.checked = live.destructive;
    }}
    function saveStorage() {{
      try {{ localStorage.setItem(STORAGE_KEY, JSON.stringify({{ userState, filterMode, lastTheme: document.body.getAttribute("data-theme") }})); }} catch (_) {{}}
    }}
    function loadStorage() {{
      try {{
        const d = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{{}}");
        if (d.userState) Object.assign(userState, d.userState);
        if (d.filterMode) filterMode = d.filterMode;
      }} catch (_) {{}}
    }}
    function isPlainHexColor(v) {{ return /^#[0-9a-f]{{3,6}}$/i.test((v||"").trim()); }}
    function hexForColorPicker(v) {{
      if (/^#[0-9a-f]{{6}}$/i.test(v)) return v;
      if (/^#[0-9a-f]{{3}}$/i.test(v)) {{ const h=v.slice(1); return `#${{h[0]}}${{h[0]}}${{h[1]}}${{h[1]}}${{h[2]}}${{h[2]}}`; }}
      return "#6c53b1";
    }}
    function resolveDisplayColor(v) {{
      const p = document.getElementById("color-probe");
      const t = (s, pr) => {{ p.style.cssText=s; const o=getComputedStyle(p)[pr]; return o&&o!=="transparent"&&o!=="rgba(0,0,0,0)"?o:""; }};
      v=(v||"").trim();
      return t(`background:${{v}}`,"backgroundColor")||t(`color:${{v}}`,"color")||"";
    }}
    function getStoredValue(key, theme) {{
      if (SHARED_KEYS.has(key)) return userState.shared?.[key];
      if (theme !== "gold") return userState.shared?.[key];
      return userState.gold?.[key];
    }}
    function persistFieldFromInput(input) {{
      const theme = document.body.getAttribute("data-theme");
      const key = input.dataset.var, val = input.value.trim();
      if (SHARED_KEYS.has(key) || theme !== "gold") {{
        if (val) {{ if (!userState.shared) userState.shared={{}}; userState.shared[key]=val; }} else delete userState.shared?.[key];
      }} else if (val) {{ userState.gold[key]=val; }} else delete userState.gold?.[key];
      saveStorage();
    }}
    function collectInputValues() {{
      const vars = {{}};
      document.querySelectorAll(".spec-input").forEach((i) => {{ const v=i.value.trim(); if(v) vars[i.dataset.var]=v; }});
      return vars;
    }}
    function applyPreviewStyles(vars) {{
      const lines = Object.entries(vars).map(([k,v]) => `  ${{k}}: ${{v}};`);
      document.getElementById("runtime-preview-styles").textContent = lines.length ? `#preview-scope {{\\n${{lines.join("\\n")}}\\n}}` : "";
      renderLive(); renderMatrix();
    }}
    function readVar(key) {{ return getComputedStyle(document.documentElement).getPropertyValue(key).trim(); }}
    function renderSpecTableStructure() {{
      const tbody = SPEC_ROWS.filter(([g]) => rowMatchesFilter(g)).map(([group, key, label]) => {{
        const tag = SHARED_KEYS.has(key) ? "（尺寸共用）" : "（色值）";
        return `<tr><td>${{group}} · ${{label}}${{tag}}</td><td><code>${{key}}</code></td><td><div class="value-editor">
          <input class="spec-input" data-var="${{key}}" spellcheck="false" />
          <input type="color" class="spec-color-picker" hidden /><span class="swatch"></span></div></td></tr>`;
      }}).join("");
      document.getElementById("spec-table").innerHTML = `<thead><tr><th>分组</th><th>变量</th><th>值</th></tr></thead><tbody>${{tbody}}</tbody>`;
      loadInputsFromState(document.body.getAttribute("data-theme"));
    }}
    function loadInputsFromState(theme) {{
      document.querySelectorAll(".spec-input").forEach((input) => {{
        const key = input.dataset.var;
        let val = getStoredValue(key, theme) || readVar(key) || COLOR_DEFAULTS[key] || "";
        input.value = val;
        const picker = input.closest(".value-editor")?.querySelector(".spec-color-picker");
        if (picker) {{ picker.hidden = !isPlainHexColor(val); if (!picker.hidden) picker.value = hexForColorPicker(val); }}
        const sw = input.closest(".value-editor")?.querySelector(".swatch");
        const c = resolveDisplayColor(val);
        if (sw) {{ sw.style.background = c || "transparent"; sw.style.display = c ? "inline-block" : "none"; }}
      }});
    }}
    function bindSpecTable() {{
      document.getElementById("spec-table").addEventListener("input", (e) => {{
        const input = e.target.closest(".spec-input");
        if (input) persistFieldFromInput(input);
        const picker = e.target.closest(".spec-color-picker");
        if (picker) {{
          const t = picker.closest(".value-editor")?.querySelector(".spec-input");
          if (t) {{ t.value = picker.value; persistFieldFromInput(t); }}
        }}
      }});
    }}
    const THEME_NOTES = {{
      light: "浅色 — ghost xs 24px 对齐 table-design-system.less",
      dark: "深色 — 建议色值写 var(--fc-*)",
      gold: "金拱门 — solid / link 可独立覆盖",
    }};
    function setTheme(theme) {{
      document.documentElement.setAttribute("data-theme", theme === "gold" ? "light" : theme);
      document.body.setAttribute("data-theme", theme);
      ["light","dark","gold"].forEach((t) => document.getElementById(`theme-${{t}}`)?.classList.toggle("is-on", t===theme));
      document.getElementById("theme-note").textContent = THEME_NOTES[theme];
      loadInputsFromState(theme);
      applyPreviewStyles(collectInputValues());
      saveStorage();
    }}
    function generateStyleCode() {{
      const theme = document.body.getAttribute("data-theme");
      const lines = Object.entries(collectInputValues()).map(([k,v]) => `  ${{k}}: ${{v}};`).join("\\n");
      const stamp = new Date().toLocaleString("zh-CN");
      return theme === "gold"
        ? `/* FC 按钮 金拱门 ${{stamp}} */\\n.theme-light-gold {{\\n${{lines}}\\n}}\\n`
        : `/* FC 按钮 浅/深 ${{stamp}} */\\n.theme-light,\\n.theme-dark {{\\n${{lines}}\\n}}\\n`;
    }}
    document.getElementById("btn-preview").onclick = () => {{
      applyPreviewStyles(collectInputValues());
      document.getElementById("copy-hint").textContent = "已预览";
      document.getElementById("preview-scope").scrollIntoView({{ behavior: "smooth" }});
    }};
    document.getElementById("btn-apply-code").onclick = () => {{
      applyPreviewStyles(collectInputValues());
      document.getElementById("code-output").value = generateStyleCode();
      document.getElementById("output-section").classList.add("is-visible");
    }};
    document.getElementById("btn-copy-output").onclick = async () => {{
      try {{ await navigator.clipboard.writeText(document.getElementById("code-output").value);
        document.getElementById("copy-hint").textContent = "已复制"; }} catch {{ window.prompt("复制", document.getElementById("code-output").value); }}
    }};
    document.getElementById("btn-reset-vars").onclick = () => {{
      const theme = document.body.getAttribute("data-theme");
      if (theme === "gold") userState.gold = {{}}; else userState.shared = {{}};
      loadInputsFromState(theme); applyPreviewStyles(collectInputValues()); saveStorage();
    }};
    document.getElementById("btn-filter-all").onclick = () => {{ filterMode = "all"; renderSpecTableStructure(); saveStorage(); }};
    document.getElementById("btn-filter-focus").onclick = () => {{ filterMode = "focus"; renderSpecTableStructure(); saveStorage(); }};
    document.getElementById("theme-light").onclick = () => setTheme("light");
    document.getElementById("theme-dark").onclick = () => setTheme("dark");
    document.getElementById("theme-gold").onclick = () => setTheme("gold");
    ["sel-variant","sel-hierarchy","sel-size","sel-icon"].forEach((id) => {{
      document.getElementById(id).onchange = (e) => {{
        live[id.replace("sel-","")] = e.target.value;
        if (id === "sel-variant") updateHierarchySelect();
        renderSpecTableStructure(); renderLive();
      }};
    }});
    document.getElementById("chk-destructive").onchange = (e) => {{
      live.destructive = e.target.checked; renderSpecTableStructure(); renderLive();
    }};
    bindSpecTable(); loadStorage(); populateSelectors();
    document.getElementById("sel-variant").value = "ghost";
    document.getElementById("sel-size").value = "xs";
    live.variant = "ghost"; live.size = "xs";
    updateHierarchySelect(); renderMatrix(); renderLive(); setTheme("light");
  </script>
</body>
</html>
"""
    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT} ({len(content)} bytes)")
