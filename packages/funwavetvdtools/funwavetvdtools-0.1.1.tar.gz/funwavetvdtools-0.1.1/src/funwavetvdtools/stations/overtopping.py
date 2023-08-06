
import numpy as np

def compute_flux(t, h, min_depth, t_min=None, t_max=None):
    
    if not t_min is None:
        idx = t_min < t
        t = t[idx]
        h = h[idx]
        
    if not t_max is None:
        idx = t < t_max
        t = t[idx]
        h = h[idx]
        
    wl = eta - h
    wl[wl<min_depth] = min_depth
    
    flux = wl*u

    return t, flux