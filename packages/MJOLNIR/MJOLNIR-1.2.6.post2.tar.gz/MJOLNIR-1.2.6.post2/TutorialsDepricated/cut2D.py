import sys,os
sys.path.append('/home/lass/Dropbox/PhD/Software/MJOLNIR/')
from MJOLNIR.Data import DataFile
DataFile.assertFile('Data/camea2018n000137.nxs')
from MJOLNIR.Data import DataSet
from MJOLNIR import _tools
def test_cut2D(show=False):
    import numpy as np
    import matplotlib.pyplot as plt
    file = 'Data/camea2018n000137.hdf'
    DataObj = DataSet.DataSet(dataFiles=file)
    DataObj.convertDataFile()
    energy = DataObj.energy

    EnergyBins = _tools.binEdges(energy,tolerance=0.125)
    q1 = np.array([1.0,0])
    q2 = np.array([0,1.0])
    width = 0.1 # 1/A
    minPixel = 0.01

    ax,DataList,qBnLit,centerPos,binDIstance = DataObj.plotCutQE(q1,q2,width,minPixel,EnergyBins,rlu=False)
    plt.colorbar(ax.pmeshs[0])

    ax.set_clim(0,10)
    plt.tight_layout()

    ## Cut and plot 1D
    ax2,DataList,Bins,binCenter,binDistance = DataObj.plotCut1D(q1,q2,width,minPixel,rlu=False,Emin = 0.2, Emax = 1.7,plotCoverage=True)
    if show:
        plt.show()
    else:
        if os.path.exists('Data/camea2018n000137.nxs'):
            os.remove('Data/camea2018n000137.nxs')


if __name__ == '__main__':
    test_cut2D(True)