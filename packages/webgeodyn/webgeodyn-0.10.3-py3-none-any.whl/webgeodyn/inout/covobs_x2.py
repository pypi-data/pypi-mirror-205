import os
import h5py
import numpy as np
import glob

def load(dataDirectory, dataModel, keepRealisations=False):

    measures_to_load = ['MF', 'SV']

    hdf5_files = glob.glob(os.path.join(dataDirectory, '*.hdf5'))
    if len(hdf5_files) == 0:
        raise IOError('No hdf5 file was found in {} !'.format(dataDirectory))

    # Assuming that the file to read is the first one
    hdf_filename = hdf5_files[0]
    print('Reading:', hdf_filename)

    lmax = 14
 
    with h5py.File(hdf_filename) as hdf_file:
        times = np.array(hdf_file['times'])

        for measureName in measures_to_load:

            if measureName == "SV":
                measureData = hdf_file['dgnm']
                units = "nT/yr"
            elif measureName == "MF":
                measureData = hdf_file['gnm']
                units = "nT"

            # Move realisation axis to last place to have data of form [ntimes, ncoef, nreal] (originally [nreal, ntimes, ncoef])
            # Remove firstpoints
            formattedData = np.moveaxis(measureData, 0, -1)
            assert lmax * (lmax + 2) == formattedData.shape[1], 'lmax or shape of data is wrong'

            print('keepRealisations', keepRealisations)
            if keepRealisations:
                # If realisation must be kept, add the data to the model as read
                dataModel.addMeasure(measureName, measureName,
                                    lmax, units, formattedData, times=times)
            else:
                # Else, average the data read on realisations
                meanData = formattedData.mean(axis=2)
                rmsData = formattedData.std(axis=2)
                dataModel.addMeasure(measureName, measureName, lmax, units,
                                        meanData, rmsData, times)

    return 0