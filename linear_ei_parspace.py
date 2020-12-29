## LINEAR E-I SYSTEM
## PARAMETER SPACE PLOTS

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import linear_ei_dynamics as dyn

class MidpointNormalize(colors.Normalize):
	def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
		self.midpoint = midpoint
		colors.Normalize.__init__(self, vmin, vmax, clip)
	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))
    
#%%
## COMPUTE WEIGHTS
## A: transformation matrix
## beta1, beta2: AR(2) parameter
def compute_weights(A,beta1,beta2):
    weights=[]
    weights.append((1/(A[0]*A[3]-A[1]*A[2]))*(A[3]*A[0]*beta1 + A[3]*A[1] - A[0]*A[2]*beta2))
    weights.append((1/(A[0]*A[3]-A[1]*A[2]))*(-A[1]*A[0]*beta1 - A[1]*A[1] + A[0]*A[0]*beta2))
    weights.append((1/(A[0]*A[3]-A[1]*A[2]))*(A[3]*A[2]*beta1 + A[3]*A[3] - A[2]*A[2]*beta2))
    weights.append((1/(A[0]*A[3]-A[1]*A[2]))*(-A[1]*A[2]*beta1 - A[1]*A[3] + A[0]*A[2]*beta2))
    return weights, [r'$v_{ee}$',r'$v_{ei}$',r'$v_{ie}$',r'$v_{ii}$']

#%%
## CREATE MASKS 
## create masks to show region of the phase space
## create_mask_weights: region of coupling weights smaller than 1
## create_mask_det: region of det = +/-1
def create_mask_weights(weights):
    mask = np.zeros_like(weights[0])
    for idx in np.ndenumerate(weights[0]):
        if  abs(weights[1][idx[0]]) <1 and abs(weights[2][idx[0]]) <1 : 
            mask[idx[0]] = 1         
    return mask
def create_mask_det(a,a2_span,a4_span):
    det = (a[0]*a4_span - a2_span*a[2])
    return np.where(abs(det)<1,1,0)

#%%
## FIG 2
## WEIGHTS IN THE (beta1,beta2) PARAMETER SPACE
## A: chosen affine transformation
## b1_range: minimum and maximum value for the beta1 span [b1_min,b1_max]
## b2_range: minimum and maximum value for the beta2 span [b2_min,b2_max]
## savedir: directory for saving

def weights_b1b2(A,b1_range,b2_range,span,savedir):
    
    ## define span of parameter space
    beta1_span = np.tile(np.linspace(b1_range[0],b1_range[1],span),(span,1))
    beta2_span = np.tile(np.linspace(b2_range[1],b2_range[0],span),(span,1)).transpose()
    ## compute values of the weights 
    ## Appendix, equation (20)
    weights, weights_name = compute_weights(A, beta1_span, beta2_span)

    ## plot
    fig = plt.figure(figsize=(10,8), dpi=300)
    for k in range(4):
        plt.subplot(2,2,k+1)
        plt.gca().set_title('{}'.format(weights_name[k]))
        plt.ylabel(r'$\beta_2$')
        plt.xlabel(r'$\beta_1$')
        plt.xticks(np.linspace(0,span,6),np.round(np.linspace(b1_range[0],b1_range[1],6),2).tolist())
        plt.yticks(np.linspace(0,span,6),np.round(np.linspace(b2_range[1],b2_range[0],6),2).tolist())
        plt.axhline(y=span/2,linewidth=.5, linestyle='dashed',color='xkcd:light grey')
        plt.axvline(x=span/2,linewidth=.5, linestyle='dashed',color='xkcd:light grey')
        plt.xlim(0,span)
        plt.ylim(span,0)
        plt.imshow(weights[k],aspect='auto',cmap='PRGn',norm=MidpointNormalize(midpoint=0))
        plt.colorbar()
        
        ## show region of parameter space based on the dynamical proprieties
        ## of the AR(2) model (see Hamilton 1994)
        plt.plot(np.arange(0,span,1),(2*np.arange(-span/2,span/2,1)),linewidth=.5,color='k')
        plt.plot(np.arange(0,span,1),-(2*np.arange(-span/2,span/2,1)),linewidth=.5,color='k')
        plt.plot(np.arange(0,span,1),span/2+(1/(span/2))*((np.arange(0,span,1)-span/2)**2),linewidth=.5,color='k')
              
    fig.tight_layout(rect=[0, 0.01, 1, 0.98]) 
    plt.savefig(savedir+'/weights_A_{}.png'.format(A), format='png', dpi=300)
    plt.close()
    return

#%%
## FIG 3
## PHASE SHIFT AND E-I BALANCE IN THE (a2,a4) SPACE
## beta1, beta2 : chosen AR(2) parameters
## A: chosen affine transformation
## a2_range: minimum and maximum value for the a2 span [a2_min,a2_max]
## a4_range: minimum and maximum value for the a4 span [a4_min,a4_max]
## savedir: directory for saving

## E-I BALANCE
def balance_a2a4(beta1,beta2,A,a2_range,a4_range,span,savedir):
    
    ## define span of parameter spac
    a2_span = np.tile(np.linspace(a2_range[0],a2_range[1],span),(span,1))
    a4_span = np.tile(np.linspace(a4_range[1],a4_range[0],span),(span,1)).transpose()
    ## compute values of the weights 
    ## Appendix, equation (20)
    weights=[]
    weights.append((1/(A[0]*a4_span - a2_span*A[2]))*(a4_span*A[0]*beta1 + np.multiply(a4_span,a2_span) - A[0]*A[2]*beta2))
    weights.append((1/(A[0]*a4_span - a2_span*A[2]))*(-a2_span*A[0]*beta1- np.multiply(a2_span,a2_span) + A[0]*A[0]*beta2))
    weights.append((1/(A[0]*a4_span - a2_span*A[2]))*(a4_span*A[2]*beta1 + np.multiply(a4_span,a4_span) - A[2]*A[2]*beta2))
    weights.append((1/(A[0]*a4_span - a2_span*A[2]))*(-a2_span*A[2]*beta1 - np.multiply(a2_span,a4_span) + A[0]*A[2]*beta2))  
    ## normalization of the weights
    ## when a_2 and a_4 approach each other the transformation tends
    ## to be non invertible and thus the weights diverge to infinite
    ## on the a_2 = a_4 line. This serve to avoid infty
    for k in range(4): weights[k][abs(weights[k]) >1e10]=np.nan
    
    ## PLOT
    fig = plt.figure(figsize=(6,6), dpi=300)
    plt.ylabel(r'$a_4$')
    plt.xlabel(r'$a_2$')
    plt.xticks(np.linspace(0,span,6),np.round(np.linspace(a2_range[0],a2_range[1],6),2).tolist())
    plt.yticks(np.linspace(0,span,6),np.round(np.linspace(a4_range[1],a4_range[0],6),2).tolist())
    
    plt.axhline(y=(np.abs(a4_span[:,0])).argmin(),linewidth=.5, linestyle='dashed',color='k')
    plt.axvline(x=(np.abs(a2_span[0,:])).argmin(),linewidth=.5, linestyle='dashed',color='k')
    plt.xlim(0,span)
    plt.ylim(span,0)
    ## show masks for region of the parameter space
    plt.contour(create_mask_weights(weights),colors='xkcd:navy blue',linewidths=.5,alpha=.7)
    plt.contour(create_mask_det(A,a2_span,a4_span),colors='xkcd:mauve',linewidths=.5,alpha=.7)
    plt.imshow(weights[2]+weights[1],aspect='auto',cmap='PRGn',norm=MidpointNormalize(midpoint=0),alpha=.9)
    plt.colorbar()
    ## show focal point
    plt.scatter((np.abs(a2_span[0,:]+A[0])).argmin(),(np.abs(a4_span[:,0]+A[2])).argmin(),c='xkcd:mauve',s=10)
      
    fig.tight_layout(rect=[0, 0.01, 1, 0.98]) 
    plt.savefig(savedir+'/EI_balance_b1_{}_b2_{}_A_{}.png'.format(beta1,beta2,A), format='png', dpi=300)
    plt.close()
    return

## PHASE SHIFT
def phase_a2a4(beta1,beta2,A,a2_range,a4_range,span,savedir):
    
    ## define span of parameter spac
    a2_span = np.tile(np.linspace(a2_range[0],a2_range[1],span),(span,1))
    a4_span = np.tile(np.linspace(a4_range[1],a4_range[0],span),(span,1)).transpose()
    ## compute values of the weights 
    ## Appendix, equation (20)
    weights=[]
    weights.append((1/(A[0]*a4_span - a2_span*A[2]))*(a4_span*A[0]*beta1 + np.multiply(a4_span,a2_span) - A[0]*A[2]*beta2))
    weights.append((1/(A[0]*a4_span - a2_span*A[2]))*(-a2_span*A[0]*beta1- np.multiply(a2_span,a2_span) + A[0]*A[0]*beta2))
    weights.append((1/(A[0]*a4_span - a2_span*A[2]))*(a4_span*A[2]*beta1 + np.multiply(a4_span,a4_span) - A[2]*A[2]*beta2))
    weights.append((1/(A[0]*a4_span - a2_span*A[2]))*(-a2_span*A[2]*beta1 - np.multiply(a2_span,a4_span) + A[0]*A[2]*beta2))  
    
    ## COMPUTE PHASE SHIFT
    ## for every (a_2,a_4) simulate the dynamics of the E-I system and 
    ## compute the mean angle between I and the AR(2) model, the mean angle
    ## between E and the AR(2) model and then compute the difference between
    ## the two estimated angles (default time = 1000)
    phase_shift = np.zeros_like(weights[0])
    for idx in np.ndenumerate(a2_span):
        A[1],A[3] = a2_span[idx[0]],a4_span[idx[0]]
        ar,E,I,_ = dyn.num_solution(1000,A,beta1,beta2)
        phase_shift[idx[0]] = np.mean(np.arctan2(I[5:],ar[5:-1])) - np.mean(np.arctan2(E[5:],ar[5:-1]))
    ## save phase shift data
    np.save(savedir+'/phase_shift',phase_shift)
    
    ## PLOT
    fig = plt.figure(figsize=(6,6), dpi=300)
    plt.ylabel(r'$a_4$')
    plt.xlabel(r'$a_2$')
    plt.xticks(np.linspace(0,span,6),np.round(np.linspace(a2_range[0],a2_range[1],6),2).tolist())
    plt.yticks(np.linspace(0,span,6),np.round(np.linspace(a4_range[1],a4_range[0],6),2).tolist())
    
    plt.axhline(y=span/2-(np.abs(a4_span[:,0])).argmin(),linewidth=.5, linestyle='dashed',color='xkcd:light grey')
    plt.axvline(x=(np.abs(a2_span[0,:])).argmin(),linewidth=.5, linestyle='dashed',color='xkcd:light grey')
    plt.xlim(0,span)
    plt.ylim(span,0)
    ## show masks for region of the parameter space
    plt.contour(create_mask_weights(weights),colors='xkcd:navy blue',linewidths=.5,alpha=.7)
    plt.contour(create_mask_det(A,a2_span,a4_span),colors='xkcd:mauve',linewidths=.5,alpha=.7)
    
    plt.imshow(phase_shift,aspect='auto',cmap='PRGn',norm=MidpointNormalize(midpoint=0),alpha=.9)
    plt.colorbar()
    ## show focal point
    plt.scatter((np.abs(a2_span[0,:]+A[0])).argmin(),(np.abs(a4_span[:,0]+A[2])).argmin(),c='xkcd:mauve',s=10)
    
    
    fig.tight_layout(rect=[0, 0.01, 1, 0.98]) 
    plt.savefig(savedir+'/phase_shift_b1_{}_b2_{}_A_{}.png'.format(beta1,beta2,A), format='png', dpi=300)
    plt.close()
    return

## WEIGHTS
def weights_a2a4(beta1,beta2,A,a2_range,a4_range,span,savedir):
    
    ## define span of parameter spac
    a2_span = np.tile(np.linspace(a2_range[0],a2_range[1],span),(span,1))
    a4_span = np.tile(np.linspace(a4_range[1],a4_range[0],span),(span,1)).transpose()
    ## compute values of the weights 
    ## Appendix, equation (20)
    weights=[]
    weights.append((1/(A[0]*a4_span - a2_span*A[2]))*(a4_span*A[0]*beta1 + np.multiply(a4_span,a2_span) - A[0]*A[2]*beta2))
    weights.append((1/(A[0]*a4_span - a2_span*A[2]))*(-a2_span*A[0]*beta1- np.multiply(a2_span,a2_span) + A[0]*A[0]*beta2))
    weights.append((1/(A[0]*a4_span - a2_span*A[2]))*(a4_span*A[2]*beta1 + np.multiply(a4_span,a4_span) - A[2]*A[2]*beta2))
    weights.append((1/(A[0]*a4_span - a2_span*A[2]))*(-a2_span*A[2]*beta1 - np.multiply(a2_span,a4_span) + A[0]*A[2]*beta2))  
    
    fig = plt.figure(figsize=(10,8), dpi=300)
    weights_name = [r'$v_{ee}$',r'$v_{ei}$',r'$v_{ie}$',r'$v_{ii}$']
    
    for k in range(4):
        plt.subplot(2,2,k+1)
        plt.gca().set_title('{}'.format(weights_name[k-1]))
        plt.ylabel(r'$a_4$')
        plt.xlabel(r'$a_2$')
        plt.xticks(np.linspace(0,span,6),np.round(np.linspace(a2_range[0],a2_range[1],6),2).tolist())
        plt.yticks(np.linspace(0,span,6),np.round(np.linspace(a4_range[1],a4_range[0],6),2).tolist())
        
        plt.axhline(y=(np.abs(a4_span[:,0])).argmin(),linewidth=.5, linestyle='dashed',color='k')
        plt.axvline(x=(np.abs(a2_span[0,:])).argmin(),linewidth=.5, linestyle='dashed',color='k')
        plt.xlim(0,span)
        plt.ylim(span,0)
        plt.contour(np.where(abs(weights[k])<1,1,0),colors='xkcd:navy blue',linewidths=.5,alpha=.7)
        plt.imshow(weights[k],aspect='auto',cmap='PRGn',norm=MidpointNormalize(midpoint=0), vmin=-20, vmax=20,alpha=.9)
        plt.colorbar()
        ## show focal point
        plt.scatter((np.abs(a2_span[0,:]+A[0])).argmin(),(np.abs(a4_span[:,0]+A[2])).argmin(),c='xkcd:mauve',s=10)
        
        
    fig.tight_layout(rect=[0, 0.01, 1, 0.96]) 
    plt.savefig(savedir+'/weights_b1_{}_b2_{}_A_{}.png'.format(beta1,beta2,A), format='png', dpi=300)
    plt.close()
    return