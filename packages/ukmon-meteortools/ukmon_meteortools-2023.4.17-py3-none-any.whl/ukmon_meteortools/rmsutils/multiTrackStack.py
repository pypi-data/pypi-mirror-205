# Copyright (C) 2018-2023 Mark McIntyre

# python script to call TrackStack to stack several nights/cameras

import os
import glob
import datetime
from Utils.TrackStack import trackStack
import RMS.ConfigReader as cr
import argparse


def multiTrackStack(camlist, start, end, outdir=None, shwr=None, scalefactor=None, draw_constellations=False):
    """
    create a multi camera and/or multi night trackstack

    Arguments:
        camlist: a list of one or more cameras 
        start: start date as a string yyyymmdd 
        end: end date as a string yyyymmdd 
    
    Keyword Arguments: 
        outdir: where to save the output, default same location as camera 1.
        shwr: filter for a specific shower eg PER. Default all showers.
        scalefactor: scale the image to avoid cropping. Default none.
        draw_constellations: True = draw constellation stick figures. 
    """
    locfld = os.getenv('LOCALFOLDER', default='f:/videos/meteorcam/fireballs')
    datadir, _ = os.path.split(locfld)
    if outdir is None:
        outdir = '.'
    print(f'stacking {camlist} for dates {start},{end}, reading from {datadir}, saving to {outdir}')

    sdt = datetime.datetime.strptime(start, '%Y%m%d')
    edt = datetime.datetime.strptime(end, '%Y%m%d')
    d = sdt
    dir_paths = []
    while d <= edt:
        dtstr = d.strftime('%Y%m%d')
        for cam in camlist:
            cam = cam.upper()
            camdir = os.path.join(datadir, cam, 'ConfirmedFiles')
            dirs = glob.glob1(camdir, f'{cam}_{dtstr}*')
            if len(dirs) > 0: 
                srcdir = os.path.join(camdir, dirs[0])
                ftpdet = os.path.join(srcdir, f'FTPdetectinfo_{dirs[0]}.txt')
                if os.path.isfile(ftpdet):
                    print(f'using {ftpdet}')
                    dir_paths.append(srcdir)
        d = d + datetime.timedelta(days=1)

    config = cr.loadConfigFromDirectory('.config', dir_paths[0])
    if shwr is not None:
        shwr = [shwr]

    trackStack(dir_paths, config, border=5, background_compensation=True, 
        hide_plot=False, showers=shwr, darkbackground=False, out_dir=outdir, scalefactor=scalefactor,
        draw_constellations=draw_constellations)

    return


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description="Perform multiday/camera trackstack.")

    arg_parser.add_argument('cams', metavar='CAMS', nargs='+', type=str,
        help='List of cameras, comma-separated.')

    arg_parser.add_argument('dates', metavar='DATES', nargs='+', type=str,
        help='Start and end date, comma-separated in yyyymmdd format.')

    arg_parser.add_argument('-s', '--shower', metavar='SHOWER', type=str,
        help="Associate just this single shower given its code (e.g. PER, ORI, ETA).")

    arg_parser.add_argument('-o', '--outdir', metavar='OUTDIR', type=str,
        help="Where to save the output file.")

    arg_parser.add_argument('-f', '--scalefactor', metavar='SCALEFACTOR', type=int,
        help="Scale factor to apply when creating canvas.")

    arg_parser.add_argument('--constellations', help="Overplot constellations", action="store_true")

    cml_args = arg_parser.parse_args()
    cams = cml_args.cams[0]
    if ',' in cams:
        cams = cams.split(',')
    else:
        cams = [cams]

    dates = cml_args.dates[0]
    if ',' in dates:
        start, end = dates.split(',')
    else:
        start = dates
        end = start

    shwr = None
    if cml_args.shower:
        shwr = cml_args.shower
        if shwr == 'ALL': # special case for ALLs
            shwr = None
    
    outdir = '.'
    if cml_args.outdir:
        outdir = cml_args.outdir

    scalefactor = 1
    if cml_args.scalefactor:
        scalefactor = cml_args.scalefactor

    multiTrackStack(cams, start, end, outdir, shwr, scalefactor,draw_constellations=cml_args.constellations)
