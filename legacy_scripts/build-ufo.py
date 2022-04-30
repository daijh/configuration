#! /usr/bin/python

# @author	jianhui.j.dai@intel.com
# @brief	build ufo for android
# @version	0.1
# @date		2014/07/03

import os
import sys
import getopt
import re

ufo_build_config = 'UFO_OGL=y UFO_OCL=n UFO_MEDIA=y UFO_RS=n UFO_PAVP=y UFO_COREU=y BUILD_TYPE=release ARCH=32 JOBS=8'

UFO_MAINLINE = '/opt/WorkDir/android/ufo/mainline'
UFO_INT_15_33_ANDROID = '/opt/WorkDir/android/ufo/INT_15_33_Android'
UFO_INT_L_MR1 = '/opt/WorkDir/android/ufo/INT_L_MR1'

GEN_7 = '7'
GEN_8 = '8'

ANDROID_SRC_DIR_GMIN = '/opt/WorkDir/android/gmin-android'
ANDROID_SRC_DIR_IMIN = '/opt/WorkDir/android/imin-android'

builds = []

'''
builds += [{
	'name': 'byt_t_crv2',

	'gen': GEN_7,
	'source': ANDROID_SRC_DIR_MCG,
	'target': 'byt_t_crv2',
	'ufo': UFO_INT_15_33_ANDROID,
	}]
'''

builds += [{
    'name': 'ecs_e7-gmin',

    'gen': GEN_7,
    'source': ANDROID_SRC_DIR_GMIN,
    'target': 'ecs_e7',
    'ufo': UFO_INT_15_33_ANDROID,
}]

'''
builds += [{
	'name': 'coho-irda',

	'gen': GEN_7,
	'source': ANDROID_SRC_DIR_IRDA,
	'target': 'coho',
	'ufo': UFO_INT_15_33_ANDROID,
	}]

builds += [{
    'name': 'ffrd8-r44b',

    'gen': GEN_7,
    'source': ANDROID_SRC_DIR_IMIN,
    'target': 'byt_t_ffrd8',
    'ufo': UFO_INT_15_33_ANDROID,
}]
'''

builds += [{
    'name': 'ffrd8-64-imin-legacy',

    'gen': GEN_7,
    'source': ANDROID_SRC_DIR_IMIN,
    'target': 'byt_t_ffrd8_64',
    'ufo': UFO_INT_15_33_ANDROID,
}]

'''
builds += [{
	'name': 'bdw_wsb-gmin',

	'gen': GEN_8,
	'source': ANDROID_SRC_DIR_GMIN,
	'target': 'bdw_wsb',
	'ufo': UFO_MAINLINE,
	}]
'''

builds += [{
    'name': 'cht_rvp-gmin',

    'gen': GEN_8,
    'source': ANDROID_SRC_DIR_GMIN,
    'target': 'cht_rvp',
    #'ufo': UFO_MAINLINE,
    'ufo': UFO_INT_L_MR1,
}]

builds += [{
    'name': 'cht_ffd-imin-lmr1',

    'gen': GEN_8,
    'source': ANDROID_SRC_DIR_IMIN,
    'target': 'cht_ffd',
    #'ufo': UFO_MAINLINE,
    'ufo': UFO_INT_L_MR1,
}]

builds += [{
    'name': 'cht_ffd-imin-mainline',

    'gen': GEN_8,
    'source': ANDROID_SRC_DIR_IMIN,
    'target': 'cht_ffd',
    'ufo': UFO_MAINLINE,
}]

builds += [{
    'name': 'cht_rvp-imin-lmr1',

    'gen': GEN_8,
    'source': ANDROID_SRC_DIR_IMIN,
    'target': 'cht_rvp',
    #'ufo': UFO_MAINLINE,
    'ufo': UFO_INT_L_MR1,
}]

builds += [{
    'name': 'cht_rvp-imin-mainline',

    'gen': GEN_8,
    'source': ANDROID_SRC_DIR_IMIN,
    'target': 'cht_rvp',
    'ufo': UFO_MAINLINE,
}]

builds += [{
    'name': 'cht_cr_rvp-imin',

    'gen': GEN_8,
    'source': ANDROID_SRC_DIR_IMIN,
    'target': 'cht_cr_rvp',
    #'ufo': UFO_MAINLINE,
    'ufo': UFO_INT_L_MR1,
}]


def clean(source, target):

    print '==========clean=========='

    paths = []

    paths += ['/gen/UFO_BUILD_MAKEFILES']
    paths += ['/obj/FAKE/ufo_intermediates']
    paths += ['/obj/include/ufo']

    paths += ['/obj/SHARED_LIBRARIES/libgrallocgmm_intermediates']
    paths += ['/obj_x86/SHARED_LIBRARIES/libgrallocgmm_intermediates']

    paths += ['/obj/SHARED_LIBRARIES/libgrallocclient_intermediates']
    paths += ['/obj_x86/SHARED_LIBRARIES/libgrallocclient_intermediates']

    paths += ['/obj/STATIC_LIBRARIES/libgmm_umd_intermediates']
    paths += ['/obj_x86/STATIC_LIBRARIES/libgmm_umd_intermediates']

    paths += ['/obj/SHARED_LIBRARIES/libgrallocgmm_intermediates']
    paths += ['/obj_x86/SHARED_LIBRARIES/libgrallocgmm_intermediates']

    paths += ['/obj/STATIC_LIBRARIES/libskuwa0_intermediates']
    paths += ['/obj_x86/STATIC_LIBRARIES/libskuwa0_intermediates']

    paths += ['/obj/SHARED_LIBRARIES/libskuwa_intermediates']
    paths += ['/obj_x86/SHARED_LIBRARIES/libskuwa_intermediates']

    paths += ['/obj/SHARED_LIBRARIES/skuwa']
    paths += ['/obj_x86/SHARED_LIBRARIES/skuwa']

    paths += ['/obj/SHARED_LIBRARIES/libcoreuinterface_intermediates']
    paths += ['/obj_x86/SHARED_LIBRARIES/libcoreuinterface_intermediates']

    paths += ['/obj/SHARED_LIBRARIES/libcoreuclient_intermediates']
    paths += ['/obj_x86/SHARED_LIBRARIES/libcoreuclient_intermediates']

    paths += ['/obj/SHARED_LIBRARIES/libcoreuservice_intermediates']
    paths += ['/obj_x86/SHARED_LIBRARIES/libcoreuservice_intermediates']

    paths += ['/obj/SHARED_LIBRARIES/hwcomposer.ufo_intermediates']
    paths += ['/obj_x86/SHARED_LIBRARIES/hwcomposer.ufo_intermediates']

    paths += ['/obj/SHARED_LIBRARIES/hwcomposer.ufo_intermediates']
    paths += ['/obj_x86/SHARED_LIBRARIES/hwcomposer.ufo_intermediates']

    paths += ['/obj/SHARED_LIBRARIES/libhwcservice_intermediates']
    paths += ['/obj_x86/SHARED_LIBRARIES/libhwcservice_intermediates']

    paths += ['/obj/SHARED_LIBRARIES/libhwcwidi_intermediates']
    paths += ['/obj_x86/SHARED_LIBRARIES/libhwcwidi_intermediates']

    paths += ['/obj/STATIC_LIBRARIES/libhwccommon_intermediates']
    paths += ['/obj_x86/STATIC_LIBRARIES/libhwccommon_intermediates']

    for p in paths:
        print p

        path = source + '/out/target/product/' + target + p
        cmd = 'rm -rfv ' + path

        print cmd
        stream = os.popen(cmd)
        lines = stream.readlines()

        for line in lines:
            print line

    print '===================='


def compile(gen, source, target, ufo, need_clean):
    make_opts = ' ' + ufo_build_config \
        + ' GFXGEN=' + gen \
        + ' ANDROID_SRC=' + source \
        + ' TARGET_PRODUCT=' + target \
        + ' -C ' + ufo + '/Tools/Linux'

    if need_clean:
        clean(source, target)

        cmd_clean = 'make' + make_opts + ' ufo-clean'

        print cmd_clean
        os.system(cmd_clean)

    cmd_build = 'make' + make_opts + ' all android'
    print cmd_build
    os.system(cmd_build)


def PrintUsage():
    print "Usage: " + sys.argv[0] + " [-ci] " + " name"
    print "Options:"
    print "\t-c",
    print "\t" + 'make clean'
    print "\t-i",
    print "\t" + 'interactive'
    print "\tname"
    for b in builds:
        print "\t\t" + b['name']

    sys.exit(1)

if __name__ == '__main__':

    try:
        options, arguments = getopt.getopt(sys.argv[1:-1], 'ci', [])
    except getopt.GetoptError, error:
        PrintUsage()

    # if len(arguments) != 1:
    #	PrintUsage()

    need_clean = False
    need_interactive = False

    for option, value in options:
        if option == "-c":
            need_clean = True
        elif option == "-i":
            need_interactive = True
        else:
            print 'error'
            PrintUsage()

    for build in builds:
        if sys.argv[-1] == build['name']:
            print 'you chose build ', build['name']

            print '\tclean:\t', need_clean
            print '\tsource:\t', build['source']
            print '\tufo:\t', build['ufo']
            print '\ttarget:\t', build['target']
            print '\tgen:\t', build['gen']
            print '\tconfig:\t', ufo_build_config

            do_build = True
            if need_interactive:
                confirm = raw_input('Continue[y]?')

                if not confirm == 'y':
                    do_build = False
                    print 'Abord'

            if do_build:
                compile(build['gen'], build['source'], build[
                        'target'], build['ufo'], need_clean)

            sys.exit(1)

    print 'undefined name: ' + sys.argv[-1] + '\n'

    PrintUsage()

    sys.exit(1)
