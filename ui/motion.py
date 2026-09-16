"""
Motion (motion.dev) integration for Streamlit.

Loads the Motion vanilla-JS build from CDN and animates real
app elements by CSS selector. Because Streamlit's components
iframe is a child frame, scripts query `parent.document` to
reach the actual app DOM.

Design rules:
- Transform/opacity only (GPU friendly).
- Respects prefers-reduced-motion.
- Elements are marked data-motion-done so each animates once
  per browser session - Streamlit reruns never re-trigger.
- If Motion fails to load, code no-ops; elements are never
  hidden, so the UI still renders normally.
"""

import json

import streamlit.components.v1 as components


MOTION_CDN = (
    "https://cdn.jsdelivr.net/npm/"
    "motion@13.3.0/dist/motion.min.js"
)


def load_motion():
    """
    Pre-warm the Motion CDN so the browser caches the
    script before the first animation iframe runs.
    Call once at app startup.
    """

    components.html(
        f"""
        <script src="{MOTION_CDN}"></script>
        <script>
          window.__motionPrewarmed = true;
        </script>
        """,
        height=0,
    )


# ------------------------------------------
# Effect library (Motion keyframes)
# ------------------------------------------

_EFFECTS = {
    "fade-up": {
        "opacity": [0, 1],
        "transform": [
            "translateY(18px)",
            "translateY(0px)"
        ],
    },
    "fade-in": {
        "opacity": [0, 1],
    },
    "fade-scale": {
        "opacity": [0, 1],
        "transform": [
            "scale(0.94)",
            "scale(1)"
        ],
    },
    "slide-left": {
        "opacity": [0, 1],
        "transform": [
            "translateX(24px)",
            "translateX(0px)"
        ],
    },
    "fill-x": {
        "transform": [
            "scaleX(0)",
            "scaleX(1)"
        ],
    },
}


def _inject(selector, effect, duration, delay, stagger, amount):

    keyframes = json.dumps(
        _EFFECTS.get(effect, _EFFECTS["fade-in"])
    )

    components.html(
        f"""
        <script src="{MOTION_CDN}"></script>
        <script>
          (function () {{
            function run() {{
              try {{

                var doc = window.parent.document;

                var M = window.Motion || window.parent.Motion;
                if (!M) return;

                var reduced = (
                  doc.defaultView.matchMedia || window.matchMedia
                );

                if (
                  reduced &&
                  reduced.call(doc.defaultView,
                    "(prefers-reduced-motion: reduce)").matches
                ) return;

                var els = doc.querySelectorAll("{selector}");

                els.forEach(function (el, i) {{

                  if (el.dataset.motionDone) return;
                  el.dataset.motionDone = "1";

                  var opts = {{
                    duration: {duration},
                    ease: [0.22, 1, 0.36, 1],
                    delay: {delay} + i * {stagger}
                  }};

                  try {{
                    M.animate(el, {keyframes}, opts);
                  }} catch (e) {{
                    /* never break the app */
                  }}
                }});

              }} catch (e) {{
                /* parent not reachable yet - retry */
                setTimeout(run, 400);
              }}
            }}

            run();
          }})();
        </script>
        """,
        height=0
    )


def animate_selector(
    selector,
    effect="fade-up",
    duration=0.55,
    delay=0.0,
    stagger=0.07,
    amount=0.25
):
    """Animate every element matching selector (once each)."""

    _inject(
        selector,
        effect,
        duration,
        delay,
        stagger,
        amount
    )


def animate_capability_chips():
    """Hero source-capability chips (header)."""

    animate_selector(
        ".hf-chip",
        effect="fade-scale",
        duration=0.5,
        stagger=0.08
    )


def animate_confidence_meter():
    """Confidence meter fill inside answer headers."""

    animate_selector(
        ".hf-confidence-fill",
        effect="fill-x",
        duration=0.9,
        delay=0.15
    )


def apply_scroll_reveal():
    """Reveal heavy blocks (tables, charts, expanders)."""

    animate_selector(
        '[data-testid="stDataFrame"], '
        '[data-testid="stPyplot"], '
        "details, pre",
        effect="fade-up",
        duration=0.55,
        amount=0.15
    )


def animate_upload_zone():
    """Upload zone and success/error alerts."""

    animate_selector(
        '[data-testid="stFileUploaderDropzone"], '
        '[data-testid="stAlertContainer"], '
        '[data-testid="stAlert"]',
        effect="fade-up",
        duration=0.5,
        amount=0.1
    )
