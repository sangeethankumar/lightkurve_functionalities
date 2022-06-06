from gettext import dpgettext
from matplotlib.pyplot import title
import periodogram_properties as pprop
import matplotlib.pylab as plt

def automator(ticid: int,save=False):
    """automates the plotter

    Args:
        ticid (int): 16 digit TESS target id
    """    
    fig = plt.subplots()
    
    lc = pprop.searchNstitch(ticid=ticid)
    ls,bls = pprop.genp(lc.flatten())
    
    lc.plot(title='Light curve')
    plt.tight_layout()
    if save:
        plt.savefig('TIC'+str(ticid)+'_lc.eps')
    
    fig2,ax = plt.subplots(2)
    ls.plot(scale='log',title='LS periodogram',ax=ax[0],color='k')
    bls.plot(scale='log',title='BLS periodogram',ax=ax[1],color='k',view='frequency')
    plt.tight_layout()
    if save:
        plt.savefig('TIC'+str(ticid)+'_per.eps')

    ls_period,bls_period,t0,dur = pprop.getLSparams(ls,bls)
    print("LS Period : {}\nBLS Period : {}\nT0 : {}\nTransit duration : {}".format(ls_period,bls_period,t0,dur))

    fig3,ax = plt.subplots(2)
    lc.fold(period=ls_period,normalize_phase=True).plot(ax=ax[0],color='k')
    lc.fold(period=bls_period,epoch_time=t0,normalize_phase=True).plot(ax=ax[1],color='k')
    plt.tight_layout()
    if save:
        plt.savefig('TIC'+str(ticid)+'_fold.eps')

    fig4,ax = plt.subplots()
    lc.fold(period=ls_period,epoch_time=t0).plot_river()
    if save:
        plt.savefig('TIC'+str(ticid)+'_ls_riverplot.eps',dpi=200)
            
    fig5,ax = plt.subplots()
    lc.fold(period=bls_period,epoch_time=t0).plot_river()
    plt.tight_layout()
    if save:
        plt.savefig('TIC'+str(ticid)+'_bls_riverplot.eps',dpi=200)