
#############################################################################
# script for viewing cross-sections
#############################################################################
import matplotlib.pyplot as plt
import numpy as np

fnc = None
maintitle = ''

class Fence_viewer:

    def __init__(self,fence,title):
        global fnc
        maintitle = title
        fnc = fence
        
    def plot(self):
        plotProfiles()
        
        
#############################################################################
# Global functions
def plotProfiles():
    global fnc, maintitle
    fig = plt.figure(figsize=(12, 6), tight_layout=True) 
    fig.canvas.set_window_title('Cross-section view')
    # fig.canvas.mpl_connect('close_event', handle_close)
    ax = fig.add_subplot(111, autoscale_on=True)
    for i in xrange(fnc.nLy):
        c = np.array(fnc.cz[i])[:,0]
        z = np.array(fnc.cz[i])[:,1]
        ax.plot(c,z, color='black',linewidth=1,label=fnc.rnam[i])
        if i > 0:
            zlast = np.array(fnc.cz[i-1])[:,1]
            ax.fill_between(c,zlast,z,color=fnc.col[i-1],hatch=fnc.ptrn[i-1],edgecolor='black')
    
    ax.fill_between(np.array(fnc.cz[-1])[:,0],np.array(fnc.cz[-1])[:,1],ax.get_ylim()[0],color='grey',hatch='////', edgecolor='black')
    plt.title(maintitle)
    plt.xlabel('chainage')
    plt.ylabel('elevation')
    plt.grid(True)
    scale = 1.5
    zpk = ZoomPanKey(ax)
    ax.format_coord = format_coord
    figZoom = zpk.zoom_factory(ax, base_scale = scale)
    figPan = zpk.pan_factory(ax)
    figKey = zpk.key_factory(ax)
    plt.show()

def handle_close(evt):
    global fnc
    fnc = None

class ZoomPanKey:
    def __init__(self,ax):
        self.press = None
        self.ctrl = False
        self.orig_xlim = ax.get_xlim()
        self.orig_ylim = ax.get_ylim()        
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None

    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location
                        
            if event.button == 'down':
                # deal with zoom out
                scale_factor = base_scale
            elif event.button == 'up':
                # deal with zoom in
                scale_factor = 1 / base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print event.button

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            
            if self.ctrl:
                new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
                rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])
                ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])          
            
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            if event.dblclick:
                ax.set_xlim(self.orig_xlim)
                ax.set_ylim(self.orig_ylim)
                ax.figure.canvas.draw()
            else:
                if self.ctrl:
                    self.cur_xlim = ax.get_xlim()
                    self.cur_ylim = ax.get_ylim()
                    self.press = self.x0, self.y0, event.xdata, event.ydata
                    self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)
            ax.figure.canvas.draw()

        # get the figure of interest
        fig = ax.get_figure()

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion    
    
    def key_factory(self, ax):
        def onKeyPress(event):
            if event.key == 'control':
                self.ctrl = True
        
        def onKeyRelease(event):
            global fnc
            if event.key == 'control':
                self.ctrl = False
            elif event.key == 't':
                fnc.translateSection(1000,1000)
                plotProfiles()
        
        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('key_press_event', onKeyPress)
        fig.canvas.mpl_connect('key_release_event', onKeyRelease)

        #return the function
        return onKeyPress     
    
def format_coord(x,y):
    global fnc
    en = fnc.EN(x)
    return "E={0:1.0f}, N={1:1.0f}, c={2:1.3f}, z={3:1.3f}, Layer: {4}".format(en[0],en[1],x,y,fnc.LayerName(x,y))
    
