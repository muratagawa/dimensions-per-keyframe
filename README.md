# Dimensions Per Keyframe

If you're a comic artist or such, you'll want to render each keyframe with a different resolution. But Blender does not allow you to save render dimensions at each keyframe.

With this small add-on, you can save the X and Y values of the rendering resolution as markers in the timeline.


Installation
----

1. Download ZIP package
2. In Blender, install via **"Edit > Preferences... > Add-ons > Install..."**


Usage
----

1. In Timeline window, add marker. (shortcut: M)
2. Change the marker name (shorcut: Ctrl+M) to `X RESOLUTION:Y RESOLUTION`. (colon separated)
    - e.g.: `1920:1080`
3. With changing keyframe, the render dimension is set by the marker if exists.
