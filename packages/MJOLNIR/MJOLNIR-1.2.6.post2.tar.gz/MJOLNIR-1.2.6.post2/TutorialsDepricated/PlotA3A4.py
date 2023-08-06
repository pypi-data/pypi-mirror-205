import sys,os
sys.path.append('/home/lass/Dropbox/PhD/Software/MJOLNIR/')

from MJOLNIR.Data import DataSet
def test_PlotA3A4(save=False):
    import matplotlib.pyplot as plt
    import numpy as np

    File = 'Data/camea2018n000137.hdf'
    DS = DataSet.DataSet(dataFiles=File)
    DS.convertDataFile()
    files = DS.convertedFiles


    planes2 = list(np.arange(64).reshape(8,8)) # Plot all planes binned with 8 pixels together
    ax = [DS.createRLUAxes() for _ in range(len(planes2))] # Create custom axes for plotting

    ax2 = DS.plotA3A4(files,planes=planes2,ax=ax)

    counter = 0
    for ax in ax2: # loop through axes to increase size and save
        fig = ax.get_figure()
        fig.set_size_inches(10.5, 10.5, forward=True)
        
        if save:
            fig.savefig('A3A4/{:03d}.png'.format(counter),format='png')
        counter+=1
    if save:
        plt.show()
    else:
        if os.path.exists('Data/camea2018n000137.nxs'):
            os.remove('Data/camea2018n000137.nxs')

if __name__=='__main__':
    test_PlotA3A4(True)


