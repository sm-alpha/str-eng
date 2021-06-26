# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:23:07 2019

@author: srikr
"""
import matplotlib.pyplot as plt
import numpy as np

def hysteresis(x, k, xi, yi, FY, X_plotlist, Y_plotlist, x_lim):
    
    if x == xi:
        print("Value repeated. Same ordinate returned.")
        y = yi
        
    elif x > xi:
        if yi == FY:
            y = flat(x, xi, yi)
        if yi == -FY:
            x_lim = get_x_limit(xi, FY, k)
        if -FY <= yi < FY:
            if x > x_lim:
                y = jump(FY, x_lim, X_plotlist, Y_plotlist)
            else:
                y = walk(x, xi, yi, k)
            
    elif x < xi:
        if yi == -FY:
            y = flat(x, xi, yi)
        if yi == FY:
            x_lim = get_x_limit(xi, -FY, k)
        if -FY < yi <= FY:
            if x < x_lim:
                y = jump(-FY, x_lim, X_plotlist, Y_plotlist)
            else:
                y = walk(x, xi, yi, k)
                
    return y, x_lim

            
def flat(x, xi, yi):
    return yi

def get_x_limit(xi, FY, k):
    x_limit = xi + 2*FY/k
    return x_limit

def jump(FY, x_limit, X_plotlist, Y_plotlist):
    X_plotlist.append(x_limit)
    Y_plotlist.append(FY)
    return FY

def walk(x, xi, yi, k):
    y = k*(x-xi)+yi
    return y



if __name__ == "__main__":
    
    k = 1
    x0 = 0
    y0 = 0
    FY = 1
    x_lim = FY/k
    X_plotlist = [0]
    Y_plotlist = [0]
    #xarr = [0.5, 1, 1.5, 4, 3, -1, -2, 0.5, 3, -3]
    xx = np.arange(np.pi/4, 2*np.pi, np.pi/4)
    yy = np.sin(xx)
    xarr = np.concatenate([i*yy for i in range(1,24,6)])
    yarr = []
    xi = 0
    yi = 0
    for i in xarr:
        y, x_lim = hysteresis(i, k, xi, yi, FY, X_plotlist, Y_plotlist, x_lim)
        X_plotlist.append(i)
        Y_plotlist.append(y)
        xi = i
        yi = y
    
    #fig = plt.figure(figsize = (10,12))
    plt.plot(X_plotlist,Y_plotlist)
    plt.grid(True)
    #plt.xlim([-6,6])
    #plt.ylim([-1.2,1.2])
    plt.xlabel("Strain", fontsize = 16)
    plt.ylabel("Stress", fontsize = 16)
    
    index = 0
    
    def on_keyboard(event):
        global index      
        if index+1 >= len(X_plotlist):
            plt.close()
            print("Loop Ended")
            return None
        x0 = X_plotlist[index]
        y0 = Y_plotlist[index]
        x1 = X_plotlist[index+1]
        y1 = Y_plotlist[index+1]
        plt.grid(True)
        #plt.xlim([-6,6])
        #plt.ylim([-1.2,1.2])
        plt.xlabel("Strain", fontsize = 16)
        plt.ylabel("Stress", fontsize = 16)
        plt.plot([x0,x1],[y0,y1], color = 'black', marker = 'o')
        plt.draw()
        
        if event.key == 'right':
            index += 1
        elif event.key == 'left':
            index -= 1
    
    plt.gcf().canvas.mpl_connect('key_press_event', on_keyboard)
    plt.show()