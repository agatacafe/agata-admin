"""Flat vector agate bean modelled on the illustrated packaging bean.

Regenerate: python scripts/make_logo.py assets/brand
"""
import math, random, sys
out = sys.argv[1]
CX, CY, RX, RY, TILT = 150, 200, 120, 160, 22
TOP, BOT = CY-RY, CY+RY
INK, ROAST, AMBER, HONEY, SAND, CREAM = "#3A1C0A", "#7A3E17", "#A9601F", "#CF923F", "#E8C98F", "#FBF1DC"
P = lambda pts: "M"+"L".join(f"{x:.1f} {y:.1f}" for x, y in pts)+"Z"
u = lambda y: (y-TOP)/(BOT-TOP)

def crease(y):
    # Based on the illustration: one smooth arc (a C, not an S) bowing to the left,
    # starting right of centre at the top and hooking back into the edge at the base.
    pts = [(-0.1, 40), (0.0, 32), (0.13, 18), (0.3, 4), (0.5, -8), (0.68, -14), (0.82, -13),
           (0.92, -4), (1.0, 14), (1.1, 36)]
    t = min(max(u(y), 0), 1)
    for i in range(1, len(pts)-2):
        (t0, p0), (t1, p1), (t2, p2), (t3, p3) = pts[i-1:i+3]
        if t <= t2:
            s = (t-t1)/(t2-t1)  # Catmull-Rom: smooth, with no flat spots at the points
            return CX+0.5*(2*p1+(p2-p0)*s+(2*p0-5*p1+4*p2-p3)*s*s+(3*p1-p0-3*p2+p3)*s**3)
    return CX+pts[-2][1]

def edge(y, side): return CX+side*RX*math.sqrt(max(0.0, 1-((y-CY)/RY)**2))
def ripple(y, seed, amp=1.0):
    return amp*(1.5*math.sin(0.15*y+seed)+0.8*math.sin(0.47*y+2.1*seed)+0.6*math.sin(1.21*y+3.3*seed)+0.35*math.sin(2.9*y+seed))

def strip(fa, fb, seed, n=140, y0=TOP-4, y1=BOT+4):
    """Region between two rippled curves x=fa(y) and x=fb(y)."""
    ys = [y0+(y1-y0)*i/n for i in range(n+1)]
    return P([(fa(y)+ripple(y, seed), y) for y in ys]+[(fb(y)+ripple(y, seed+0.7), y) for y in ys[::-1]])

# A few broad layers per half: about three visible stripes each (cream, roast, sand).
LEFT_BANDS = [(INK,.06),(ROAST,.07),(HONEY,.17),(CREAM,.04),(AMBER,.16),(ROAST,.07),(HONEY,.18),(SAND,.05),(AMBER,.3)]
RIGHT_BANDS = [(AMBER,.06),(HONEY,.16),(CREAM,.045),(AMBER,.15),(ROAST,.07),(HONEY,.18),(SAND,.05),(AMBER,.3)]

def contour_strip(side, f0, f1, seed, n=160):
    ys = [TOP-2+(BOT-TOP+4)*i/n for i in range(n+1)]
    def x(y, f, s):
        span = edge(y, side)-crease(y)
        return crease(y)+f*span+ripple(y, s)*min(1.0, abs(span)/90)
    return P([(x(y, f0, seed), y) for y in ys]+[(x(y, f1, seed+0.9), y) for y in ys[::-1]])

def layers():
    out = []
    for side, bands, s0 in ((-1, LEFT_BANDS, 0.0), (1, RIGHT_BANDS, 0.6)):
        f, group = -0.02, []
        for k, (c, w) in enumerate(bands):
            group.append((c, contour_strip(side, f, min(f+w+0.012, 1.1), seed=s0+k*1.37)))
            f += w
        out.append(group)
    return out

def half_clip(side):
    ys = [TOP-10+(BOT-TOP+20)*i/120 for i in range(121)]
    far = CX+side*200
    return P([(crease(y), y) for y in ys]+[(far, BOT+10), (far, TOP-10)])

def crease_band(extra=0.0):
    random.seed(11)
    n = 140; L, R = [], []
    for i in range(n+1):
        y = TOP-2+(BOT-TOP+4)*i/n
        w = 5+14*math.sin(math.pi*i/n)**0.6+extra
        x = crease(y)
        L.append((x-w*0.55-random.uniform(0, 2), y)); R.append((x+w*0.45+random.uniform(0, 1.4), y))
    return P(L+R[::-1])

def grains():
    random.seed(5); dots = []
    for i in range(46):
        y = TOP+40+(BOT-TOP-80)*random.random()
        x = crease(y)+random.uniform(-4, 3)
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(0.9, 1.9):.1f}"/>')
    return "".join(dots)

def gloss():
    n = 80; y0, y1 = TOP+34, BOT-60; G = []
    for i in range(n+1):
        y = y0+(y1-y0)*i/n; w = 10*math.sin(math.pi*i/n)**1.3
        x = crease(y)+16+5*math.sin(math.pi*u(y))
        G.append((x, y, w))
    return P([(x-w/2, y) for x, y, w in G]+[(x+w/2, y) for x, y, w in G][::-1])

def color_svg():
    left, right = layers()
    lg = "".join(f'<path fill="{c}" d="{d}"/>' for c, d in left)
    rg = "".join(f'<path fill="{c}" d="{d}"/>' for c, d in right)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="22 43 256 314" role="img" aria-labelledby="title">
  <title id="title">Ágata café agate bean</title>
  <defs>
    <clipPath id="bean"><ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}"/></clipPath>
    <clipPath id="lh"><path d="{half_clip(-1)}"/></clipPath>
    <clipPath id="rh"><path d="{half_clip(1)}"/></clipPath>
  </defs>
  <g transform="rotate({TILT} {CX} {CY})">
    <g clip-path="url(#bean)">
      <rect x="0" y="0" width="300" height="400" fill="{HONEY}"/>
      <g clip-path="url(#lh)">{lg}</g>
      <g clip-path="url(#rh)">{rg}</g>
      <path fill="{INK}" d="{crease_band()}"/>
      <g fill="{AMBER}">{grains()}</g>
      <path fill="#FFFFFF" fill-opacity=".55" d="{gloss()}"/>
    </g>
    <ellipse cx="{CX}" cy="{CY}" rx="{RX-1.5}" ry="{RY-1.5}" fill="none" stroke="{ROAST}" stroke-width="3"/>
  </g>
</svg>
'''

def mono_svg(color):
    """Same drawing in one colour: light bands, crease and gloss become cut-outs."""
    left, right = layers()
    light = {CREAM, SAND}
    cut = "".join(f'<path d="{d}"/>' for c, d in left if c in light)
    cutr = "".join(f'<path d="{d}"/>' for c, d in right if c in light)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="22 43 256 314" role="img" aria-labelledby="title">
  <title id="title">Ágata café agate bean</title>
  <defs>
    <clipPath id="lh"><path d="{half_clip(-1)}"/></clipPath>
    <clipPath id="rh"><path d="{half_clip(1)}"/></clipPath>
    <mask id="cut" maskUnits="userSpaceOnUse" x="0" y="0" width="300" height="400">
      <rect width="300" height="400" fill="#fff"/>
      <g fill="#000"><g clip-path="url(#lh)">{cut}</g><g clip-path="url(#rh)">{cutr}</g>
      <path d="{crease_band(1.5)}"/><path d="{gloss()}"/></g>
    </mask>
  </defs>
  <g transform="rotate({TILT} {CX} {CY})">
    <ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="{color}" mask="url(#cut)"/>
  </g>
</svg>
'''
open(f"{out}/agata-bean.svg", "w", encoding="utf-8").write(color_svg())
open(f"{out}/agata-bean-olive.svg", "w", encoding="utf-8").write(mono_svg("#6B7050"))
open(f"{out}/agata-bean-cream.svg", "w", encoding="utf-8").write(mono_svg("#FAF4EA"))
