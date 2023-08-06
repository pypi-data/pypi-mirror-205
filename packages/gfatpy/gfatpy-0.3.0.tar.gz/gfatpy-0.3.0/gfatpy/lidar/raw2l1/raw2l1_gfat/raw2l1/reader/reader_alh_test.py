#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
reader for raw data from ALHAMBRA LIDAR
the file format is based on LICEL file format
"""

from __future__ import print_function, absolute_import, division

import sys
import ast
import datetime as dt

import numpy as np
import netCDF4 as nc

# brand and model of the LIDAR
BRAND = "Raymetrics"
MODEL = "ALHAMBRA"

DATETIME_FMT = "{} {}"
DATE_FMT = "%d/%m/%Y %H:%M:%S"
TIME_FMT = "%H:%M:%S"

# DATE_ROTATIONAL_RAMAN355 = '15/12/2016 00:00:00'
# DATE_ROTATIONAL_RAMAN532 = '04/05/2017 00:00:00'

N_HEADER_LINE = 3

MISSING_FLOAT = np.nan
MISSING_INT = -9

BCK_MIN_ALT_KEY = "bckgrd_min_alt"
BCK_MAX_ALT_KEY = "bckgrd_max_alt"
BCK_MIN_ALT = 100
BCK_MAX_ALT = 600

POLARIZATION = {"o": 0, "p": 1, "s": 2}

DEFAULT_RESOLUTION = 3.75

BCK_COMMENT_FMT = "calcultated between {:5d} m and {:5d} m"

NUMBER_OF_CHANNELS = 54


def date_to_dt(date_num, date_units):
    """convert date np.array from datenum to datetime.datetime"""

    return nc.num2date(date_num, units=date_units, calendar="standard")


def get_channel_conf(conf, logger):
    """check configuration of channels and build the conf dict"""

    # associate channels to a number
    try:
        tmp_rcs = ast.literal_eval(conf["rcs"])
    except ValueError:
        logger.critical(
            "error parsing 'rcs' option in [reader_conf] in config file. quitting"
        )
        sys.exit(1)

    logger.debug("rcs %s %s", tmp_rcs)

    try:
        tmp_chan = ast.literal_eval(conf["channels"])
    except ValueError:
        logger.critical(
            "error parsing 'channels' option in [reader_conf] in config file. quitting"
        )
        sys.exit(1)

    logger.debug("channels id %s", tmp_chan)

    # check if the lists have the same number of elements
    if len(tmp_rcs) != len(tmp_chan):
        logger.critical(
            "error in configuration: 'channel' and 'rcs' options don't have the same number of elements. quitting"
        )
        sys.exit(1)

    # when we know the order of the variables in files we well need to add an index
    chan_conf = {
        "var_names": ["rcs_{:02d}".format(x) for x in tmp_rcs],
        "channels": tmp_chan,
        "index": [None] * len(tmp_rcs),
    }

    logger.debug("list of channels  : %s", chan_conf["channels"])
    logger.debug("list of variables : %s", chan_conf["var_names"])

    return chan_conf


def get_bck_alt(conf, logger):
    """get value of maximum and minimum altitude for background signal calculation
    if not define, use default value"""

    try:
        min_alt = ast.literal_eval(conf[BCK_MIN_ALT_KEY])
    except KeyError:
        min_alt = BCK_MIN_ALT
        logger.warning(
            "%s not defined in conf file using default value %d",
            BCK_MIN_ALT_KEY,
            BCK_MIN_ALT,
        )
    except ValueError:
        logger.critical(
            "error parsing '%s' option in [reader_conf] in config file. quitting",
            BCK_MIN_ALT_KEY,
            conf[BCK_MIN_ALT_KEY],
        )
        sys.exit(1)

    try:
        max_alt = ast.literal_eval(conf[BCK_MAX_ALT_KEY])
    except KeyError:
        min_alt = BCK_MAX_ALT
        logger.warning(
            "%s not defined in conf file using default value %d",
            BCK_MAX_ALT_KEY,
            BCK_MAX_ALT,
        )
    except ValueError:
        logger.critical(
            "error parsing '%s' option in [reader_conf] in config file. quitting",
            BCK_MAX_ALT_KEY,
            conf[BCK_MAX_ALT_KEY],
        )
        sys.exit(1)

    return min_alt, max_alt


def get_channel_index(file_id, n_chan, chan_conf, logger):
    """associate id of channel with rcs_XX variable of channels"""

    # skip header
    for i in range(N_HEADER_LINE):
        line = file_id.readline()
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        print(i, line.strip())

    for i_chan in range(n_chan):

        line = file_id.readline()
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        line_id = line.split()[-1]

        try:
            index = chan_conf["channels"].index(line_id)
        except ValueError:
            logger.warning("id %s not found in raw data", line_id)
            continue

        chan_conf["index"][index] = i_chan

    # check if we found at least one channel:
    uniq_index = set(chan_conf["index"])

    if len(uniq_index) == 1 and list(uniq_index) == [None]:
        logger.critical(
            "No requested channels in conf file could be identified." "stopping code"
        )
        sys.exit(1)

    return chan_conf


def get_data_size(list_files, logger):
    """determine size of data to read"""

    # create dimensions dict
    data_dim = {}
    data_dim["time"] = 0
    data_dim["range"] = 0
    data_dim["range_std"] = 0
    data_dim["n_chan"] = NUMBER_OF_CHANNELS
    data_dim["nv"] = 2  # size for time bounds

    logger.info("number of channels : %d", data_dim["n_chan"])

    # loop over list of files
    for i_file, file_ in enumerate(list_files):

        try:
            f_id = open(file_, "rb")
        except IOError:
            logger.error("error trying to open %s", file_)
            continue

        # line 1 : name of file, we don't need it
        f_id.readline()

        # line 2 : date and time, we need it
        line = f_id.readline()
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        elts = line.split()
        datetime_str = DATETIME_FMT.format(elts[1], elts[2])

        # try to parse date to check file is valid
        try:
            dt.datetime.strptime(datetime_str, DATE_FMT)
        except ValueError:
            logger.error("wrong time format in " + file_)
            continue

        data_dim["time"] += 1

        # line 3 : number of channels, we need it
        line = f_id.readline()

        # line 4 : get range from first channel description
        line = f_id.readline()
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        elts = line.split()
        if i_file == 0:
            data_dim["range"] = int(elts[3])
            logger.info("size of rcs range: %d", data_dim["range"])
        else:
            tmp = int(elts[3])
            if tmp != data_dim["range"]:
                logger.critical(
                    "size of rcs range was %d in previous file and is now %d in %s",
                    data_dim["range"],
                    tmp,
                    file_,
                )
                sys.exit(1)
        # line 5 : get range std from second channel description
        line = f_id.readline()
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        elts = line.split()
        if i_file == 0:
            data_dim["range_std"] = int(elts[3])
            logger.info("size of std range: %d", data_dim["range_std"])
        else:
            tmp = int(elts[3])
            if tmp != data_dim["range_std"]:
                logger.critical(
                    "size of std range was %d in previous file and is now %d in %s",
                    data_dim["range_std"],
                    tmp,
                    file_,
                )
                sys.exit(1)

        f_id.close()

    # log dimensions
    logger.debug("dim time     : %d", data_dim["time"])
    logger.debug("dim rcs range    : %d", data_dim["range"])
    logger.debug("dim std range    : %d", data_dim["range_std"])
    logger.debug("dim channels : %d", data_dim["n_chan"])
    logger.debug("dim nv       : %d", data_dim["nv"])

    return data_dim


def init_data(data_dim, logger):
    """initialize dict containing ndarrays based on data dimension"""
    n_chan = data_dim["n_chan"]
    tsize = data_dim["time"]
    data = {}

    # dimensions
    data["time"] = np.empty((data_dim["time"],), dtype=np.dtype(dt.datetime))
    data["time_bounds"] = np.empty(
        (data_dim["time"], data_dim["nv"]), dtype=np.dtype(dt.datetime)
    )
    data["range"] = np.empty((data_dim["range"],), dtype=np.float32)
    data["range_std"] = np.empty((data_dim["range_std"],), dtype=np.float32)

    # scalar values
    data["frequency"] = MISSING_FLOAT
    data["time_resol"] = MISSING_FLOAT
    data["zenith"] = MISSING_FLOAT
    data["range_resol"] = MISSING_FLOAT
    data["longitude"] = MISSING_FLOAT
    data["latitude"] = MISSING_FLOAT
    data["altitude"] = MISSING_FLOAT
    data["custom_comment"] = MISSING_FLOAT

    # Constant in time
    data["telescope"] = np.ones((n_chan,), dtype=np.int)
    data["dataset_type"] = np.zeros((n_chan,), dtype=np.int)
    data["laser_source"] = np.zeros((n_chan,), dtype=np.int)
    data["detection_mode"] = np.array(["None"] * n_chan)
    data["range_resol_vect"] = np.ones((n_chan,), dtype=np.float32) * MISSING_FLOAT
    data["wavelength"] = np.ones((n_chan,), dtype=np.float32) * MISSING_FLOAT
    data["powermeter"] = np.ones((n_chan,), dtype=np.float32) * MISSING_FLOAT
    data["polarization"] = np.array(["o"] * n_chan, dtype=np.str)
    data["n_range"] = np.ones((n_chan,), dtype=np.int) * MISSING_INT
    data["n_shots"] = np.ones((n_chan,), dtype=np.int) * MISSING_INT

    logger.info("telescope number: %s" % data["telescope"])
    logger.info("detection_mode number: %s" % data["dataset_type"])

    # unused column
    data["bin_shift"] = np.ones((n_chan,), dtype=np.int) * MISSING_INT
    data["bin_shift_dec"] = np.ones((n_chan,), dtype=np.int) * MISSING_INT
    data["adc_bits"] = np.ones((n_chan,), dtype=np.int) * MISSING_INT
    data["discriminator_level"] = np.ones((n_chan,), dtype=np.int) * MISSING_FLOAT
    data["adc_range"] = np.ones((n_chan,), dtype=np.float32) * MISSING_FLOAT
    data["number_one"] = np.ones((n_chan,), dtype=np.int) * MISSING_INT

    # multi_dim vars
    data["active"] = np.zeros((tsize, n_chan), dtype=np.int)
    data["voltage"] = np.ones((tsize, n_chan), dtype=np.int) * MISSING_FLOAT
    data["n_chan_vector"] = np.ones((tsize,), dtype=np.int) * MISSING_INT

    logger.info("Size of voltage [%d %d]" % (tsize, n_chan))

    # for i_chan in xrange(data_dim['n_chan']):
    for i_chan in range(data_dim["n_chan"]):
        data["rcs_{:02d}".format(i_chan)] = (
            np.ones((data_dim["time"], data_dim["range"]), dtype=np.float32)
            * MISSING_FLOAT
        )
        data["std_{:02d}".format(i_chan)] = (
            np.ones((data_dim["time"], data_dim["range_std"]), dtype=np.float32)
            * MISSING_FLOAT
        )
        data["bckgrd_rcs_{:02d}".format(i_chan)] = (
            np.ones((data_dim["time"],), dtype=np.float32) * MISSING_FLOAT
        )
        data["units_{:02d}".format(i_chan)] = "MHz"
        data["units_std_{:02d}".format(i_chan)] = "MHz"

    data["laser_power_01"] = (
        np.ones((data_dim["time"],), dtype=np.float32) * MISSING_FLOAT
    )
    data["laser_power_02"] = (
        np.ones((data_dim["time"],), dtype=np.float32) * MISSING_FLOAT
    )

    return data


def read_header(file_id, data, data_dim, index, logger, date_only=False):
    """Extract data from file ASCII header"""

    # first line: filename (we don't need it)
    # ------------------------------------------------------------------------
    file_id.readline()

    # second line : datetime, localization and meteo
    # ------------------------------------------------------------------------
    logger.debug("reading header second line")
    line = file_id.readline()
    if isinstance(line, bytes):
        line = line.decode("utf-8")
    logger.debug("parsing : %s", line)
    elts = line.split()

    logger.debug("reading dates")
    datetime_start = DATETIME_FMT.format(elts[1], elts[2])
    datetime_end = DATETIME_FMT.format(elts[3], elts[4])

    data["time"][index] = dt.datetime.strptime(datetime_start, DATE_FMT)
    logger.debug("datetime: %s", data["time"][index])
    data["time_bounds"][index, 0] = data["time"][index]
    data["time_bounds"][index, 1] = dt.datetime.strptime(datetime_end, DATE_FMT)

    if date_only:
        logger.debug("reading only date from header")
        return data
    else:
        data["time_resol"] = (
            data["time_bounds"][index, 1] - data["time_bounds"][index, 0]
        ).total_seconds()
        data["altitude"] = np.float(elts[5])
        data["longitude"] = np.float(elts[6])
        data["latitude"] = float(elts[7])
        data["zenith"] = float(elts[8])
        if len(elts) > 10:
            data["custom_comment"] = elts[10]

    # third line: nothing interesting to read ??
    # ------------------------------------------------------------------------
    line = file_id.readline()
    if isinstance(line, bytes):
        line = line.decode("utf-8")
    elts = line.split()
    # data["laser1_shots"] = np.float(elts[0])
    data["laser1_frequency"] = np.float(elts[1])
    # data["laser2_shots"] = np.float(elts[2])
    data["laser2_frequency"] = np.float(elts[3])
    tmp_n_chan = np.int(elts[4])
    print("Number of channels: %d" % tmp_n_chan)
    data["n_chan_vector"][index] = tmp_n_chan

    # channels description
    # ------------------------------------------------------------------------
    # for i_chan in xrange(tmp_n_chan):
    for i_chan in range(tmp_n_chan):

        var_name = "rcs_{:02d}".format(i_chan)

        line = file_id.readline()
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        logger.debug("parsing : %s", line.strip())
        elts = line.split()

        # Change with time
        # logger.info('index: %d' % index)
        # logger.info('i_chan: %d' % i_chan)
        # logger.info('data[voltage]: %d' % int(elts[5]))
        # pdb.set_trace()
        data["active"][index, i_chan] = int(elts[0])
        data["dataset_type"][i_chan] = int(elts[1])
        data["laser_source"][i_chan] = int(elts[2])
        data["n_range"][i_chan] = int(elts[3])
        data["polarization"][i_chan] = int(elts[4])
        data["voltage"][index, i_chan] = int(elts[5])
        data["range_resol_vect"][i_chan] = float(elts[6])
        data["wavelength"][i_chan] = int(elts[7].split(".")[0])
        data["powermeter"][i_chan] = int(elts[8])

        # unused
        data["bin_shift"][i_chan] = float(elts[10])
        data["bin_shift_dec"][i_chan] = float(elts[11])
        data["adc_bits"][i_chan] = int(elts[12])
        data["n_shots"][i_chan] = int(elts[13])

        tmp = elts[15][0:2]
        if data["dataset_type"][i_chan] == 0 or data["dataset_type"][i_chan] == 2:
            data["detection_mode"][i_chan] = "analog"
            data["adc_range"][i_chan] = float(elts[14])
        elif data["dataset_type"][i_chan] == 1 or data["dataset_type"][i_chan] == 3:
            data["detection_mode"][i_chan] = "photocounting"
            data["discriminator_level"][i_chan] = float(elts[14])

    # check all range_resol is the same
    current_range_resol_vector = data["range_resol_vect"][
        data["powermeter"] == 0
    ]  # those channels not powermeter
    # logger.info('current current_range_resol_vector: %s' % current_range_resol_vector)
    sort_range_resol = np.unique(current_range_resol_vector[:tmp_n_chan])
    if len(sort_range_resol) == 1:
        data["range_resol"] = list(sort_range_resol)[0]
        logger.debug("range_resol: %s", data["range_resol"])
    else:
        logger.critical("%s" % data["range_resol_vect"])
        logger.critical(
            "all channel don't have the same resolution : %s", sort_range_resol
        )
        sys.exit(1)

    return data


def read_profiles(file_id, data, data_dim, index, logger):
    """read profile for each channel"""

    tmp_n_chan = data["n_chan_vector"][index]

    # skip header and channels descriptions
    for i in range(N_HEADER_LINE + tmp_n_chan + 1):
        line = file_id.readline()
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        logger.debug("%2d %s", i, line.strip())

    for i_chan in range(tmp_n_chan):

        # check of channel is active
        #        if data['active'][index,i_chan] == 0:
        #            continue

        tmp_data = np.fromfile(file_id, dtype="i4", count=int(data["n_range"][i_chan]))
        # if i_chan == 1:
        #    print ("asdf", tmp_data)
        shots = data["n_shots"][i_chan]
        # print (shots)
        if data["dataset_type"][i_chan] == 0:
            max_range = data["adc_range"][i_chan]
            adc = data["adc_bits"][i_chan]
            scalefactor = ((max_range * 1000.0) / shots) / (2**adc - 1)
            # scalefactor=1
            # print (scalefactor)
            data["rcs_{:02d}".format(i_chan)][index, :] = tmp_data * scalefactor
            data["units_rcs_{:02d}".format(i_chan)] = "mV"
        elif data["dataset_type"][i_chan] == 1:
            # It coincides with the ASCII converted by the Advanced Licel.exe by it has no sense.
            # See Licel programming manual.pdf. Bins-per-microseconds number
            # from technical specifications 20 bins/microsec.
            reduction_factor = DEFAULT_RESOLUTION / data["range_resol"]
            scalefactor = (reduction_factor * 20) / shots
            # scalefactor=1
            data["rcs_{:02d}".format(i_chan)][index, :] = tmp_data * scalefactor
            data["units_rcs_{:02d}".format(i_chan)] = "MHz"

            # print (scalefactor)
            # jump over space between profiles
        elif data["dataset_type"][i_chan] == 2:
            data["std_{:02d}".format(i_chan)][index, :] = tmp_data
            data["units_std_{:02d}".format(i_chan)] = "mV"
        elif data["dataset_type"][i_chan] == 3:
            data["std_{:02d}".format(i_chan)][index, :] = tmp_data
            data["units_std_{:02d}".format(i_chan)] = "MHz"
        elif data["laser_source"][i_chan] == 1:
            data["laser_power_01"] = tmp_data
            data["units_laser_power_{:02d}".format(i_chan)] = "a.u."
        elif data["laser_source"][i_chan] == 2:
            data["laser_power_02"] = tmp_data
            data["units_laser_power{:02d}".format(i_chan)] = "a.u."
        file_id.seek(file_id.tell() + 2)

    return data


def read_data(list_files, conf, logger):
    """Raw2L1 plugin to read raw data of SIRTA IPRAL LIDAR"""

    logger.info("Start reading of data using reader for %s %s", BRAND, MODEL)

    # get conf parameters
    # ------------------------------------------------------------------------
    conf["missing_float"]
    conf["missing_int"]

    # min and max alt for background signal calculation
    bck_min_alt, bck_max_alt = get_bck_alt(conf, logger)

    # associate channels and var_names
    # chan_conf = get_channel_conf(conf, logger)

    # determine size of data to read
    # ------------------------------------------------------------------------
    logger.info("determining size of var to read")
    logger.info("%s" % list_files)
    data_dim = get_data_size(list_files, logger)

    for ind, file_ in enumerate(list_files):
        logger.info("reading %s", file_)
        try:
            f_id = open(file_, "rb")
        except IOError:
            logger.error("error trying to open " + file_)
            continue

        # identify line of channel in file
        # --------------------------------------------------------------------
        if ind == 0:
            # chan_conf = get_channel_index(f_id, data_dim['n_chan'], chan_conf, logger)
            # initialize data array
            logger.info("initializing data output array")
            data = init_data(data_dim, logger)
            # f_id.seek(0)

        logger.info("Number of file %s: %d" % (file_, ind))
        # read header
        # --------------------------------------------------------------------
        #        if ind != 0:
        #            date_only = True
        #        else:
        #              date_only = False
        date_only = False
        data = read_header(f_id, data, data_dim, ind, logger, date_only=date_only)

        # read data
        # --------------------------------------------------------------------
        logger.info("read data")

        # go back to start of file
        f_id.seek(0)

        # read profiles
        data = read_profiles(f_id, data, data_dim, ind, logger)

        # end of reading
        # --------------------------------------------------------------------
        f_id.close()

    # final calculations
    # --------------------------------------------------------------------

    # determine range
    data["range"] = np.arange(1, data_dim["range"] + 1) * data["range_resol"]
    data["range_std"] = np.arange(1, data_dim["range_std"] + 1) * data["range_resol"]

    # add necessary dimensions
    data["n_chan"] = data_dim["n_chan"]
    data["nv"] = data_dim["nv"]  # for time bounds

    # convert polarization in values
    # logger.info('Polarization values: %s' % data['polarization'])

    # data['polarization'] = [POLARIZATION[val_] for val_ in data['polarization']]

    # logger.info('New polarization values: %s' % data['polarization'])

    # bacground alt filter
    bck_filter = (data["range"] > bck_min_alt) & (data["range"] < bck_max_alt)
    data["bckgrd_rcs_comment"] = BCK_COMMENT_FMT.format(bck_min_alt, bck_max_alt)

    # PR2 and background
    # for i_chan in xrange(data_dim['n_chan']):
    for i_chan in range(data_dim["n_chan"]):

        profiles = data["rcs_{:02d}".format(i_chan)]
        square = np.square(data["range"])

        data["bckgrd_rcs_{:02d}".format(i_chan)] = np.mean(
            profiles[:, bck_filter], axis=1
        )
        data["rcs_{:02d}".format(i_chan)] = profiles * square
        data["units_rcs_{:02d}".format(i_chan)] = (
            data["units_{:02d}".format(i_chan)] + ".m^2"
        )

    return data
