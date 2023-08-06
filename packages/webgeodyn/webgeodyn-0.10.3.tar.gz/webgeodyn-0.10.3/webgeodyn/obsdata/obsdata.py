import numpy as np
import os
from .observatory import ObservatoryGroup
import cdflib

class ObsData:
    """
    Class handling the list of ObservatoryGroups and interfaces it with the webpage.
    """
    def __init__(self, obs_directory=None):
        """
        Creates the obsGroups dict and loads the data from the current directory.
        """
        self.obsGroups = {}
        if obs_directory is None:
            obs_directory = os.path.dirname(__file__)
        self.loadFromDirectory(obs_directory)

    def getDataInfo(self):
        """
        Returns a JSON with group names as keys.

        The Values of the JSON are also dictionaries with the following keys,values :

         - 'coordinates': coordinates of the observatories of the group
         - 'search_radius': search radius of the group
         - 'display_r': display radius of the group

        """
        jsondata = {}
        for obsGroupName in self.obsGroups:
            jsondata[obsGroupName] = {
                "coordinates": self.obsGroups[obsGroupName].coordinates,
                "search_radius": self.obsGroups[obsGroupName].search_radius,
                "display_r": self.obsGroups[obsGroupName].display_r
            }
        return jsondata

    def addObsGroup(self, groupName, display_r, search_radius=None):
        """
        Creates a new ObservatoryGroup.

        :param groupName: name of the group to create. Raises an Error if it already exists.
        :type groupName: str
        :param display_r: radius where the group data should be displayed
        :type display_r: float or None
        :param search_radius: ?
        :type search_radius:
        """
        if groupName in self.obsGroups:
            raise ValueError("An observatories group named %s already exists." % groupName)
        self.obsGroups[groupName] = ObservatoryGroup(groupName, display_r, search_radius)

    def getObsR(self, th, ph, groupName):
        """
        :param th: colatitude at which the r should be fetched.
        :type th: float
        :param ph: azimuth at which the r should be fetched.
        :type ph: float
        :param groupName: name of the group in which the data should be fetched.
        :type groupName:
        :return: radius of the group
        :rtype: float
        """
        return self.obsGroups[groupName].getObsR(th, ph)

    def getData(self, measureName, th, ph, groupName):
        """
        Gets the observed data for the given parameters.

        :param measureName: name of the measure to fetch
        :type measureName: str
        :param th: colatitude at which the data should be fetched.
        :type th: float
        :param ph: azimuth at which the data should be fetched.
        :type ph: float
        :param groupName: name of the group for which the data should be fetched
        :type groupName: str
        :return: Temporal array of the observed data at th,ph.
        :rtype: np.array
        """
        return self.obsGroups[groupName].getObservatoryData(th, ph, measureName)

    def find_cdf_files(self, path):
        """
        find all files with .cdf extension in path directory and
        returns the list of 4-month data and the 1-month data.
        """
        brut_files_1M, brut_files_4M = [], []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in [f for f in filenames if f.endswith(".cdf")]:
                name = os.path.join(dirpath, filename)
                if '4M' in filename:
                    brut_files_4M.append(name)
                elif '1M' in filename:
                    brut_files_1M.append(name)
                else:
                    print('file {} do not match requirements'.format(filename))
        return brut_files_1M, brut_files_4M

    def loadFromDirectory(self, dataDirectory, cdf_type='4M'):
        """
        Reads VO files into CHAMP, SWARM, GO and other satellites files in Magnetic ObservatoryGroups.

        :param dataDirectory: directory where the files are located
        :type dataDirectory: str
        """
        # Read CHAMP, SWARM, Oersted, Cryosat and Composite cdf data files
        possible_ids = np.array(['GROUND', 'CHAMP', 'SWARM', 'OERSTED', 'CRYOSAT', 'COMPOSITE'])
        cdf_name_shortcuts = ['GO', 'CH', 'SW', 'OR', 'CR', 'CO']

        # find all cdf filenames in data directory
        cdf_files_1M, cdf_files_4M = self.find_cdf_files(dataDirectory)

        for obsGroupName, cdf_shortcut in zip(possible_ids, cdf_name_shortcuts):
            GO = True if obsGroupName == 'GROUND' else False

            if cdf_type == '4M':
                cdf_files = cdf_files_4M
            elif cdf_type == '1M':
                cdf_files = cdf_files_1M
            else:
                raise ValueError('cdf_type {} not recognized'.format(cdf_type))
            # extract file that starts with the cdf name shortcut, i.e. GO, CH, SW....
            try:
                idx = [name.split('/')[-1][:2] for name in cdf_files].index(cdf_shortcut)
            except ValueError:
                print('{} not found'.format(possible_ids[cdf_name_shortcuts.index(cdf_shortcut)]))
            cdf_filename = cdf_files[idx]

            cdf_file = cdflib.CDF(cdf_filename)

            print("Reading {} data from {}".format(obsGroupName, cdf_filename))

            thetas = 90 - cdf_file.varget("Latitude") # convert in colatitude
            if np.any(thetas > 180) or np.any(thetas < 0):
                raise ValueError('angle th {} represent the colatitude, did you use latitudes instead?'.format(th))
            phis = cdf_file.varget("Longitude")
            radii = cdf_file.varget('Radius') / 1000 # to convert in km
            if GO:
                locs = [''.join([l[0] for l in loc]) for loc in cdf_file.varget('Obs')]

            # because VOs circles should be bigger than GOs
            if GO:
                self.addObsGroup(obsGroupName, display_r=6371.2, search_radius=None)
            else:
                # assume unique radius for all VOs through time
                self.addObsGroup(obsGroupName, display_r=radii[0], search_radius=850)

            times_stamp = cdf_file.varget('Timestamp')
            dec_times = []
            for t in times_stamp:
                year, month = cdflib.cdfepoch.breakdown_epoch(t)[:2]
                dec_times.append(year + month / 12)

            Bs, SVs = cdf_file.varget('B_CF'), cdf_file.varget('B_SV')
            if GO:
                Bs -= cdf_file.varget('bias_crust')

            for i, (B, SV, r, th, ph, time) in enumerate(zip(Bs, SVs, radii, thetas, phis, dec_times)):
                if self.obsGroups[obsGroupName].display_r is None and not GO:
                    self.obsGroups[obsGroupName].display_r = r

                if GO:
                    self.obsGroups[obsGroupName].addObservatory(locs[i], r, th, ph)
                else:
                    self.obsGroups[obsGroupName].addObservatory(obsGroupName, r, th, ph)  # Add if not exists

                if np.any(np.isnan(B)):
                    continue
                else:
                    self.obsGroups[obsGroupName].addObservatoryData(th, ph, 'MF', time, B[0], B[1], B[2])

                if np.any(np.isnan(SV)):
                    continue
                else:
                    self.obsGroups[obsGroupName].addObservatoryData(th, ph, 'SV', time, SV[0], SV[1], SV[2])
