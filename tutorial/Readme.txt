
================================
Below is a brief tutorial on the 
operation of GeoPicker v0.1
================================

0. (optional) load basemap vector for reference
	use basemap.shp

1. Import and order rasters accordingly (from top to bottom):
	1_Surface.asc
	2_Newmarket_Till.asc
	3_Lower Sediments_A.asc
	4_Lower_Sediments_B.asc
	5_Weathered_Bedrock.asc
	6_Bedrock.asc

2. Group imported layers and rename if needed

3. Draw (or import) polyline vector layer for cross-section
	for example, use GeoPickerTestXS.shp

4. Run GeoPicker, select cross-section vector layer and surface group

5. (optional) adjust labelling, colour scheme and texture from file layer_prop.txt
	Note: must be kept in same location as the surfaces.


Note: All layers are projected to NAD/83 UTM zone 17N (EPSG:26917)

** this is a beta version, please report any bugs **



================================
Mouse actions:
================================

scroll wheel: zoom (while preserving vertical axis)
scroll wheel + Ctrl: zoom on cursor
Click-and-Drag + Ctrl: pan
Double-click: reset cross-section
 







