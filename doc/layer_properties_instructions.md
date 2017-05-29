
# Layer properties file

The layer properties file `layer_prop.txt` is a means of customizing the labelling, colour and texture scheme of your cross-sections. The colour and texture (i.e., hatching) schemes follow the methods of the Python 2D plotting library named [Matplotlib](http://matplotlib.org).

From top to bottom, each layer must be described by the semicolon delimited details following:

`Layer Name` **;** `Layer colour` **;** `Layer texture`

Note: the third entry `Layer texture` can be omitted if no texture is desired.

For example, `Aquifer 1;goldenrod;+++` would label the layer as _Aquifer 1_, colour the layer as goldenrod and texture the layer with a dense vertical cross-hatch.

## Colour schemes

Colour can be either entered by their standard names, or by providing `[r, g, b]` or `[r, g, b, a]` unit colour codes on [0, 1]. For example, the colour orange can be defined as: `[1, 0.5, 0]`.

### standard colour names:

![standard named colours](/doc/images/colours_1.png)

## Texture schemes

GeoPicker texture schemes follow the same [hatching used in Matplotlib](http://matplotlib.org/examples/pylab_examples/hatch_demo.html). Hatching is fairly simple, and are based on the characters: `-`, `+`, `x`, `\`, `/`, `*`, `o`, `O`, `.`. The density of the hatching is controlled by the number of characters used in succession.

### sample textures:

![standard textures](/doc/images/textures_1.png)

### combined textures:

By combining the texture characters, unique hatching can be developed. For example, the texture code `oox+` would produce:

![combined texture](/doc/images/textures_2.png)