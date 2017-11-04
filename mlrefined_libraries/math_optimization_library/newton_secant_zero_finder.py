# import custom JS animator
from mlrefined_libraries.JSAnimation_slider_only import IPython_display_slider_only

# import standard plotting and animation
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# import autograd functionality
from autograd import grad as compute_grad   # The only autograd function you may ever need
import autograd.numpy as np
import math
from IPython.display import clear_output
import time
import copy

class visualizer:
    '''
    Illustrate Newton's and Secant method for zero-finding with a customized slider mechanism
    to let user control progression of algorithms.
    ''' 
    def __init__(self,**args):
        self.g = args['g']                            # input function
        self.grad = compute_grad(self.g)              # gradient of input function
        self.w_init =float( -3)                       # input initial point
        self.w_hist = []
        self.colorspec = []                           # container for colors --> when algorithm begins, colored green, as it ends color turns yellow, then red
        
    # run newton's method
    def run_newtons(self):
        w = self.w_init
        self.w_hist = []
        self.w_hist.append(w)
        w_old = np.inf
        j = 0
        while (w_old - w)**2 > 10**-4 and j < 20:
            # update old w and index
            w_old = w
            j+=1
            
            # plug in value into func and derivative
            g_eval = self.g(w)
            grad_eval = float(self.grad(w))
            
            # take newtons step
            w = w - g_eval/(grad_eval + 10**-4)
            
            # record
            self.w_hist.append(w)

    # animate the method
    def draw_it_newton(self,**args):
        if 'w_init' in args:
            self.w_init = float(args['w_init'])
        
        # initialize figure
        fig = plt.figure(figsize = (4,4))
        artist = fig
        ax = fig.add_subplot(111)
        
        # run newtons method and collect path history
        self.w_hist = []
        self.run_newtons()
        
        # set viewing range
        wmax = max([v for v in self.w_hist])
        wmin = min([v for v in self.w_hist])
        wgap = (wmax - wmin)*0.5
        wmax += wgap
        wmin -= wgap
        
        w_plot = np.linspace(wmin,wmax,200)
        g_plot = self.g(w_plot)
        width = 30
        
        # set range for function plotting
        w_plot1 = np.linspace(-3,3)
        g_plot1 = self.g(w_plot1)
        gmin = min(copy.deepcopy(g_plot1))
        gmax = max(copy.deepcopy(g_plot1))
        ggap = (gmax - gmin)*0.2
        gmin -= ggap
        gmax += ggap
        
        # colors for points
        s = np.linspace(0,1,len(self.w_hist[:round(len(self.w_hist)/2)]))
        s.shape = (len(s),1)
        t = np.ones(len(self.w_hist[round(len(self.w_hist)/2):]))
        t.shape = (len(t),1)
        s = np.vstack((s,t))
        self.colorspec = []
        self.colorspec = np.concatenate((s,np.flipud(s)),1)
        self.colorspec = np.concatenate((self.colorspec,np.zeros((len(s),1))),1)
        
        # animation sub-function
        print ('beginning animation rendering...')
        def animate(k):
            ax.cla()
            
            # print rendering update
            if k == len(self.w_hist):
                print ('animation rendering complete!')
                time.sleep(1.5)
                clear_output()
 
            # plot function
            ax.plot(w_plot1,g_plot1,color = 'k',zorder = 1)                           # plot function

            # plot all input/output pairs generated by algorithm thus far
            if k > 0:
                # plot all points up to this point
                for j in range(0,min(k+1,len(self.w_hist))):  
                    w_val = self.w_hist[j]
                    g_val = self.g(w_val)
                    

                    if j == k-1 or j == k:
                        # draw guide line to visua
                        s = np.linspace(0,g_val)
                        o = np.ones((len(s)))
                        ax.plot(o*w_val,s,'k--',linewidth=1,zorder = 1)
                        
                        ax.scatter(w_val,g_val,s = 90,c = self.colorspec[j],edgecolor = 'k',linewidth = 0.7,zorder = 3)            # plot point of tangency
                        ax.scatter(w_val,0,s = 90,facecolor = self.colorspec[j],marker = 'X',edgecolor = 'k',linewidth = 0.7, zorder = 2)
                       

            # plot surrogate function and travel-to point
            if k > 0 and k < len(self.w_hist) + 1:
                # grab historical weight, compute function and derivative evaluations
                w = self.w_hist[k-1]
                g_eval = self.g(w)
                grad_eval = float(self.grad(w))

                # determine width to plot the approximation -- so its length == width defined above
                div = float(1 + grad_eval**2)
                w1 = w - math.sqrt(width/div)
                w2 = w + math.sqrt(width/div)

                # use point-slope form of line to plot
                wrange = np.linspace(w1,w2, 100)
                h = g_eval + grad_eval*(wrange - w)

                # plot tangent line
                ax.plot(wrange,h,color = 'b',linewidth = 2,zorder = 1)      # plot approx

                # plot tangent point
                #ax.scatter(w,g_eval,s = 100,c = 'm',edgecolor = 'k',linewidth = 0.7,zorder = 2)            # plot point of tangency

                # plot go-too line on surrogate
                w_zero = -g_eval/grad_eval + w
                #ax.scatter(w_zero,0,s = 100,c = 'm',edgecolor = 'k',linewidth = 0.7, zorder = 2, marker = 'X')
                
                '''
                # plot next point learned from surrogate
                if k > 0:
                    # draw dashed lines to highlight zero crossing point
                    g_zero = self.g(w_zero)

                    s = np.linspace(0,g_zero)
                    o = np.ones((len(s)))
                    ax.plot(o*w_zero,s,'k--',linewidth=1,zorder = 1)

                    
                    # draw associated point on cost function you hop back too
                    #ax.scatter(w_zero,g_zero,s = 100,c = 'm',edgecolor = 'k',linewidth = 0.7,zorder = 2)            # plot point of tangency
               '''
            # fix viewing limits
            ax.set_xlim([wmin,wmax])
            ax.set_ylim([gmin,gmax])

            # draw axes
            # ax.grid(True, which='both')
            ax.axhline(y=0, color='k',zorder = 0,linewidth = 0.5)
            # ax.axvline(x=0, color='k')

            # place title
            ax.set_title("Newton's method (zero finding)",fontsize = 12)
            
            return artist,

        anim = animation.FuncAnimation(fig, animate ,frames=len(self.w_hist)+1, interval=len(self.w_hist)+1, blit=True)

        return(anim)
                
    # secant method
    def run_secant(self):
        # get initial point
        w2 = self.w_init
        
        # create second point nearby w_old
        w1 = w2 - 0.5
        g2 = self.g(w2)
        g1 = self.g(w1)
        if g1 > g2:
            w1 = w2 + 0.5
        
        # setup container for history
        self.w_hist = []
        self.w_hist.append(w2)
        self.w_hist.append(w1)
        
        # start loop
        w_old = np.inf
        j = 0
        while abs(w1 - w2) > 10**-5 and j < 20:  
            # plug in value into func and derivative
            g1 = float(self.g(w1))
            g2 = float(self.g(w2))
                        
            # take newtons step
            w = w1 - g1*(w1 - w2)/(g1 - g2 + 10**-4)
            
            # record
            self.w_hist.append(w)
            
            # update old w and index
            j+=1
            w2 = w1
            w1 = w

    # animate the method
    def draw_it_secant(self,**args):
        if 'w_init' in args:
            self.w_init = float(args['w_init'])
            
        # initialize figure
        fig = plt.figure(figsize = (6,6))
        artist = fig
        ax = fig.add_subplot(111)

        # generate function for plotting on each slide
        w_plot = np.linspace(-3.1,3.1,200)
        g_plot = self.g(w_plot)
        g_range = max(g_plot) - min(g_plot)
        ggap = g_range*0.1
        width = 30
        
        # run newtons method
        self.w_hist = []
        self.run_secant()
        
        # colors for points
        s = np.linspace(0,1,len(self.w_hist[:round(len(self.w_hist)/2)]))
        s.shape = (len(s),1)
        t = np.ones(len(self.w_hist[round(len(self.w_hist)/2):]))
        t.shape = (len(t),1)
        s = np.vstack((s,t))
        self.colorspec = []
        self.colorspec = np.concatenate((s,np.flipud(s)),1)
        self.colorspec = np.concatenate((self.colorspec,np.zeros((len(s),1))),1)
        
        # animation sub-function
        print ('beginning animation rendering...')
        def animate(t):
            ax.cla()
            k = math.floor((t+1)/float(2))
            
            # print rendering update
            if k == 2*len(self.w_hist)-1:
                print ('animation rendering complete!')
                time.sleep(1.5)
                clear_output()
            
            # plot function
            ax.plot(w_plot,g_plot,color = 'k',zorder = 2)                           # plot function
           
            # plot initial point and evaluation
            if k == 0:
                w_val = self.w_init
                g_val = self.g(w_val)
                ax.scatter(w_val,g_val,s = 100,c = 'm',edgecolor = 'k',linewidth = 0.7,zorder = 2)            # plot point of tangency
                ax.scatter(w_val,0,s = 100,c = 'm',edgecolor = 'k',linewidth = 0.7, zorder = 2, marker = 'X')

            # plot all input/output pairs generated by algorithm thus far
            if k > 0:
                # plot all points up to this point
                for j in range(min(k-1,len(self.w_hist))):  
                    w_val = self.w_hist[j]
                    g_val = self.g(w_val)
                    
                    ax.scatter(w_val,g_val,s = 90,c = self.colorspec[j],edgecolor = 'k',linewidth = 0.7,zorder = 3)            # plot point of tangency
                    ax.scatter(w_val,0,s = 90,facecolor = self.colorspec[j],marker = 'X',edgecolor = 'k',linewidth = 0.7, zorder = 2)

            # plot surrogate function and travel-to point
            if k > 0 and k < len(self.w_hist):
            
                # grab historical weights, form associated secant line
                w2 = self.w_hist[k-1]
                w1 = self.w_hist[k]
                g2 = self.g(w2)
                g1 = self.g(w1)
                m = (g1 - g2)/(w1 - w2)
            
                # determine width to plot the approximation -- so its length == width defined above
                div = float(1 + m**2)
                wa = w1 - math.sqrt(width/div)
                wb = w1 + math.sqrt(width/div)
            
                # use point-slope form of line to plot
                wrange = np.linspace(wa,wb, 100)
                h = g1 + m*(wrange - w1)

                # plot secant line 
                ax.plot(wrange,h,color = 'b',linewidth = 2,zorder = 1)      # plot approx

                # plot intersection points
                ax.scatter(w2, g2, s = 100, c='m',edgecolor = 'k',linewidth = 0.7,zorder = 3)
                ax.scatter(w1, g1, s = 100, c='m',edgecolor = 'k',linewidth = 0.7,zorder = 3)

                # plot next point learned from surrogate
                if np.mod(t,2) == 0:
          
                    # draw dashed lines to highlight zero crossing point
                    w_zero = -g1/m + w1
                    g_zero = self.g(w_zero)
                    s = np.linspace(0,g_zero)
                    o = np.ones((len(s)))
                    ax.plot(o*w_zero,s,'k--',linewidth=1,zorder = 1)

                    # draw zero intersection, and associated point on cost function you hop back too
                    ax.scatter(w_zero,g_zero,s = 100,c = 'm',edgecolor = 'k',linewidth = 0.7,zorder = 3)            # plot point of tangency
                    ax.scatter(w_zero,0,s = 100,c = 'm',edgecolor = 'k',linewidth = 0.7, zorder = 3, marker = 'X')

            # fix viewing limits
            ax.set_xlim([-3.1,3.1])
            ax.set_ylim([min(g_plot) - ggap,max(g_plot) + ggap])

            # draw axes
            # ax.grid(True, which='both')
            ax.axhline(y=0, color='k',zorder = 0,linewidth = 0.5)
            # ax.axvline(x=0, color='k',linewidth = 0.5)
            
            return artist,

        anim = animation.FuncAnimation(fig, animate ,frames=2*len(self.w_hist), interval=2*len(self.w_hist), blit=True)

        return(anim)