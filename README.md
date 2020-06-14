
# Blender Instant Denoise

Enable the incredible Intel AI denoiser in Blender **in a single click**. 

![Comparison with and without denoising](side_by_side_2.jpg)

### Requirements

Built and tested with Blender 2.82, but should work with any newer version too. Please report any issues above.

### How to install

 - **Download:** if you don't have experience with GitHub, simply click "Clone or Download" above, and then "Download ZIP"
- **Install:** install like any other blender plug-in, from Edit > Preferences > Add-ons > Install... and navigate to the plug-in (blender_instant_denoise.py). Make sure it is then ticked inside Blender

### Usage

After install, you should see a new panel in the render properties tab. Simply click the "denoise" button to set up the new Intel AI denoiser through the compositor for your scene. Please note that currently, this removes any existing compositing nodes, so only use with scenes with no other compositing.

### Acknowledgements 
Coffee model available under a CC-0 licence [here](https://3dmodelhaven.com/model/?c=appliances&m=CoffeeCart_01).
"Advanced Denoise" feature based on: https://www.youtube.com/watch?v=sLLndwUPUiw