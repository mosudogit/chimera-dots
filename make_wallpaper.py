#!/usr/bin/env python3
"""Generate a minimal clean wallpaper for chimera-rice."""
import os, math, random

W, H = 1920, 1080

# Catppuccin Mocha palette
BG     = "#1e1e2e"
CRUST  = "#11111b"
SURFACE= "#313244"
ACCENT = "#cba6f7"
BLUE   = "#89b4fa"
TEAL   = "#94e2d5"

random.seed(42)

def grid_lines():
    lines = []
    step = 80
    for x in range(0, W + step, step):
        lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{SURFACE}" stroke-width="0.5" opacity="0.4"/>')
    for y in range(0, H + step, step):
        lines.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{SURFACE}" stroke-width="0.5" opacity="0.4"/>')
    return "\n".join(lines)

def dots():
    items = []
    step = 80
    for xi in range(0, W // step + 1):
        for yi in range(0, H // step + 1):
            x = xi * step
            y = yi * step
            items.append(f'<circle cx="{x}" cy="{y}" r="1.5" fill="{SURFACE}" opacity="0.6"/>')
    return "\n".join(items)

def accent_lines():
    lines = []
    # a few subtle diagonal accent lines
    positions = [
        (200, 0, 0, 540, ACCENT, 0.08),
        (0, 200, 960, 0, BLUE,   0.06),
        (W, 600, 1200, H, TEAL,  0.07),
        (800, 0, W, 700, ACCENT, 0.05),
    ]
    for x1,y1,x2,y2,col,op in positions:
        lines.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{col}" stroke-width="1" opacity="{op}"/>'
        )
    return "\n".join(lines)

def corner_accent():
    # bottom-right corner decorative bracket
    cx, cy = W - 80, H - 80
    size = 40
    s = ACCENT
    op = 0.35
    return (
        f'<line x1="{cx}" y1="{cy+size}" x2="{cx}" y2="{cy}" stroke="{s}" stroke-width="1.5" opacity="{op}"/>'
        f'<line x1="{cx}" y1="{cy}" x2="{cx+size}" y2="{cy}" stroke="{s}" stroke-width="1.5" opacity="{op}"/>'
        # top-left
        f'<line x1="{80}" y1="{80-size+size}" x2="{80}" y2="{80}" stroke="{s}" stroke-width="1.5" opacity="{op}"/>'
        f'<line x1="{80}" y1="{80}" x2="{80+size}" y2="{80}" stroke="{s}" stroke-width="1.5" opacity="{op}"/>'
    )

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <!-- subtle gradient overlay -->
  <defs>
    <radialGradient id="glow" cx="50%" cy="50%" r="60%">
      <stop offset="0%"   stop-color="{SURFACE}" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="{BG}"       stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
  <!-- dot grid -->
  {dots()}
  <!-- accent lines -->
  {accent_lines()}
  <!-- corner brackets -->
  {corner_accent()}
</svg>'''

out = os.path.join(os.path.dirname(__file__), "wallpapers", "minimal.svg")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as f:
    f.write(svg)

# also convert to png if rsvg-convert or inkscape available
import subprocess, shutil
png = out.replace(".svg", ".png")
if shutil.which("rsvg-convert"):
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), out, "-o", png])
    print(f"wallpaper written: {png}")
elif shutil.which("inkscape"):
    subprocess.run(["inkscape", out, f"--export-filename={png}", f"-w={W}", f"-h={H}"])
    print(f"wallpaper written: {png}")
else:
    print(f"wallpaper SVG written: {out}")
    print("install rsvg-convert (librsvg) or inkscape to convert to PNG")
