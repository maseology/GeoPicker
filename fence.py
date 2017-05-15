
#############################################################################
# script for building dem profiles
# based on: www.portailsig.org/content/python-utilisation-des-couches-vectorielles-et-matricielles-dans-une-perspective-geologique-
# (in english): gis.stackexchange.com/questions/59316/python-script-for-getting-elevation-difference-between-two-points
#############################################################################
import os
import gdal
import math
from osgeo import ogr

class Fence:
    def __init__(self,sections,rasters_FP):
        self.sec = []
        self.secv = []
        self.secid = 0
        self.raster = []
        self.rnam = []
        self.nLy = 0
        self.cz = []
        self.name = []
        self.col = []
        self.ptrn = []
                
        # load rasters
        for rfp in rasters_FP:
            self.addProfile(rfp)
            self.rnam.append(os.path.basename(rfp))
                    
        # load sections
        gridsize = math.fabs(self.raster[0].GetGeoTransform()[1])
        for f in sections:
            self.sec.append(addIntervals(f,gridsize/2))
            self.secv.append(vertexChainage(f))
                
        # create profiles
        for r in self.raster:
            self.buildChain(r,self.sec[self.secid])
                
        # load layer properties
        prop_fp = rasters_FP[0].replace(os.path.basename(rasters_FP[0]),'layer_prop.txt')
        if os.path.isfile(prop_fp):
            input_file=open(prop_fp,'r')
            for line in input_file:
                p = line.split(';')
                self.name.append(str(p[0].rstrip()))
                self.col.append(textToColourTuple(str(p[1].rstrip()))) if len(p)>1 else self.col.append('none')
                self.ptrn.append(str(p[2].rstrip())) if len(p)>2 else self.ptrn.append('')
            input_file.close()
        else:
            for i in xrange(self.nLy):
                self.name.append('layer_' + str(i))
                if i % 2 == 0: 
                    self.col.append('orange') 
                else: 
                    self.col.append('green')
                self.ptrn.append('')
    
    def addProfile(self,rasterFP):
        rast = gdal.Open(rasterFP)
        self.raster.append(rast)
        self.nLy += 1
    
    def buildChain(self,raster,section):
        # load DEM
        gt = raster.GetGeoTransform()
        bands = raster.RasterCount
        xyz = []
        for c in section:
            z = rasterXY(c[0],c[1],raster,bands,gt)
            if not z==0:
                xyz.append([c[0],c[1],z[0]])

        # plot profile
        cz = []
        dsum = 0.0
        cz.append([0.0,xyz[0][2]])
        for i in xrange(1,len(xyz)):
            dsum += lenxy(xyz[i-1],xyz[i])
            cz.append([dsum,xyz[i][2]])
        self.cz.append(cz)   
    
    # layer information
    def EN(self,c):
        for i in range(1,len(self.secv[self.secid])):
            if self.secv[self.secid][i][0] > c:
                xy1 = self.secv[self.secid][i-1][1:]
                xy2 = self.secv[self.secid][i][1:]
                dist = c - self.secv[self.secid][i-1][0]
                return xyinterp(xy1,xy2,dist)
        return 0,0

    def LayerName(self,x,y):
        lid = 0
        for c in self.cz:
            if self.isLeftOf(c,x,y) > 0: break
            lid += 1
        lid -= 1
        if 0 <= lid < self.nLy-1: return self.name[lid]
        return ''
        
    def isLeftOf(self,cz,x,y):
        for i in xrange(len(cz)-1):
            if math.fabs(x-cz[i][0]) < 0.0001:
                if y == cz[i][1]: return 0  # colinear
                if cz[i+1][0] < cz[i][0]:
                    if y < cz[i][1]:
                        return -1
                    else:
                        return 1
                else:
                    if y > cz[i][1]: 
                        return -1
                    else:
                        return 1
            if x > cz[i][0] and x < cz[i+1][0]:
                test = ((cz[i+1][0] - cz[i][0]) * (y - cz[i][1]) - (cz[i+1][1] - cz[i][1]) * (x - cz[i][0]))
                if test == 0: return
                if test < 0: return -1
                return 1
        if y == cz[-1][1]: return 0  # colinear
        if cz[-1][0] > cz[-2][0]:
            if y < cz[-1][1]: 
                return -1
            else:
                return 1
        else:
            if y < cz[-1][1]:
                return -1
            else:
                return 1
        return 0
    
    # section 
    def translateSection(self,dx,dy):
        self.sec[self.secid] = [(xy[0]+dx, xy[1]+dy) for xy in self.sec[self.secid]]
        self.rebuildChain()
        
    def rebuildChain(self):
        self.cz = []
        for r in self.raster:
            self.buildChain(r,self.sec[self.secid])
            


####################################################
# global functions
def rasterXY(x,y,layer,bands,gt):
    col=[]
    # transform to raster point coordinates
    px = int((x - gt[0]) / gt[1])
    if not (0 <= px <= layer.RasterXSize):
        return 0
    py =int((y - gt[3]) / gt[5])
    if not (0 <= py <= layer.RasterYSize):
        return 0  
    for j in range(bands):
        band = layer.GetRasterBand(j+1)
        data = band.ReadAsArray(px,py, 1, 1)
        col.append(data[0][0])
    return col

def vertexChainage(xy):
    cxyout=[]
    dist = 0.0
    for i in xrange(len(xy)-1):
        cxyout.append((dist,xy[i][0],xy[i][1]))
        dist += lenxy(xy[i],xy[i+1])
    cxyout.append((dist,xy[-1][0],xy[-1][1]))
    return cxyout

def addIntervals(xy,stepsize):
    xyout=[]
    for i in xrange(len(xy)-1):
        dist = lenxy(xy[i],xy[i+1])
        nstp = int(math.ceil(dist/stepsize))
        stepsize_adj = dist/nstp
        xyout.append(xy[i])
        for j in range(1,nstp):
            xyout.append(xyinterp(xy[i],xy[i+1],j*stepsize_adj))
    xyout.append(xy[-1])
    return xyout
    
def lenxy(xy1,xy2):
    d1=xy1[0]-xy2[0]
    d2=xy1[1]-xy2[1]
    return math.sqrt(d1**2 + d2**2)
    
def xyinterp(xy1,xy2,dist):
    dx=xy2[0]-xy1[0]
    dy=xy2[1]-xy1[1]
    len=math.sqrt(dx**2 + dy**2)
    f = dist/len
    return xy1[0]+f*dx,xy1[1]+f*dy
    
def textToColourTuple(Line):
    if not '[' in Line: return Line
    p = Line.replace("[", "").replace("]", "").strip().split(',')
    if not (3 <= len(p) <= 4): return 'none'
    if len(p) == 3: return [float(p[0]),float(p[1]),float(p[2])]
    return [float(p[0]),float(p[1]),float(p[2]),float(p[3])]