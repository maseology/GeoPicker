
# GeoPicker tutorial

Below is a brief tutorial on the operation of GeoPicker (v0.1)

 1. (optional) load basemap vector for reference  
	use: `basemap.shp`  
	**Note: All tutorial layers are projected to NAD/83 UTM zone 17N (EPSG:26917)**

 2. Import and order surface rasters accordingly (from top to bottom):  
	`1_Surface.asc`  
	`2_Newmarket_Till.asc`  
	`3_Lower_Sediments_A.asc`  
	`4_Lower_Sediments_B.asc`  
	`5_Weathered_Bedrock.asc`  
	`6_Bedrock.asc`  

 3. Group imported rasters and rename group if needed

 4. Draw (or import) polyline vector layer for cross-section  
	for example, use `GeoPickerTestXS.shp`

 5. Run GeoPicker (`Plugins->Geo Picker->GeoPicker`), select cross-section vector layer and raster group, click `OK`

 6. (optional) adjust labelling, colour scheme and texture from file `layer_prop.txt`  
	Note: layer property file must be kept in same location/directory as the rasters.  
	For more information on the layer property file, [click here](../doc/layer_properties_instructions.md).


*this is a beta version, please report any bugs*

## Interactive Mouse and Keyboard actions:

`scroll wheel`: zoom (while preserving vertical axis)  
`scroll wheel + Ctrl`: zoom on cursor  
`Click-and-Drag + Ctrl`: pan  
`Double-click`: reset cross-section  
 







