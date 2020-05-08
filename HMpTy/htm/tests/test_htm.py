from __future__ import print_function
from builtins import zip
from builtins import str
import os
import unittest
import shutil
import yaml
from HMpTy.utKit import utKit
from fundamentals import tools
from os.path import expanduser
from past.utils import old_div
home = expanduser("~")

packageDirectory = utKit("").get_project_root()
settingsFile = packageDirectory + "/test_settings.yaml"

su = tools(
    arguments={"settingsFile": settingsFile},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName=None,
    defaultSettingsFile=False
)
arguments, settings, log, dbConn = su.setup()

# SETUP PATHS TO COMMON DIRECTORIES FOR TEST DATA
moduleDirectory = os.path.dirname(__file__)
pathToInputDir = moduleDirectory + "/input/"
pathToOutputDir = moduleDirectory + "/output/"

try:
    shutil.rmtree(pathToOutputDir)
except:
    pass
# COPY INPUT TO OUTPUT DIR
shutil.copytree(pathToInputDir, pathToOutputDir)

# Recursively create missing directories
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

class test_htm(unittest.TestCase):

    def test_lookup01(self):

        raList1 = ["138.30789"]
        decList1 = ["+61.09267"]
        from HMpTy import HTM
        mesh16 = HTM(
            depth=16,
            log=log
        )
        print("LOOKUP")
        htmids = mesh16.lookup_id(raList1, decList1)
        for h, r, d in zip(htmids, raList1, decList1):
            print(r, d, " --> ", h)

    def test_htm_area_function(self):

        from HMpTy import HTM
        mesh24 = HTM(
            depth=24,
            log=log
        )
        mesh16 = HTM(
            depth=16,
            log=log
        )
        mesh15 = HTM(
            depth=15,
            log=log
        )
        mesh14 = HTM(
            depth=14,
            log=log
        )
        mesh13 = HTM(
            depth=13,
            log=log
        )
        mesh12 = HTM(
            depth=12,
            log=log
        )
        mesh11 = HTM(
            depth=11,
            log=log
        )
        mesh10 = HTM(
            depth=10,
            log=log
        )

        print("DEPTH24:", mesh24.depth)
        print("AREA24:", mesh24.area * 60 * 60 * 60 * 60, " arcsec^2")
        print("DEPTH16:", mesh16.depth)
        print("AREA16:", mesh16.area * 60 * 60 * 60 * 60, " arcsec^2")
        print("DEPTH15:", mesh15.depth)
        print("AREA15:", mesh15.area * 60 * 60 * 60 * 60, " arcsec^2")
        print("DEPTH14:", mesh14.depth)
        print("AREA14:", mesh14.area * 60 * 60 * 60 * 60, " arcsec^2")
        print("DEPTH13:", mesh13.depth)
        print("AREA13:", mesh13.area * 60 * 60 * 60 * 60, " arcsec^2")
        print("DEPTH12:", mesh12.depth)
        print("AREA12:", mesh12.area * 60 * 60, " arcmin^2")
        print("DEPTH11:", mesh11.depth)
        print("AREA11:", mesh11.area * 60 * 60, " arcmin^2")
        print("DEPTH10:", mesh10.depth)
        print("AREA10:", mesh10.area * 60 * 60, " arcmin^2")

    def test_htm_function(self):

        from HMpTy import HTM
        mesh16 = HTM(
            depth=16,
            log=log
        )
        mesh20 = HTM(
            depth=20,
            log=log
        )
        mesh24 = HTM(
            depth=24,
            log=log
        )
        print("DEPTH24:", mesh24.depth)
        print("AREA24:", mesh24.area * 60 * 60 * 60 * 60, " arcsec^2")
        print("DEPTH16:", mesh16.depth)
        print("AREA16:", mesh16.area * 60 * 60 * 60 * 60, " arcsec^2")
        print("DEPTH20:", mesh20.depth)
        print("AREA20:", mesh20.area * 60 * 60 * 60 * 60, " arcsec^2")

        overlappingTrixels = mesh24.intersect(
            ra="23:25:53.56",
            dec="+26:54:23.9",
            radius=0.01,
            inclusive=False
        )
        # print overlappingTrixels

        overlappingTrixels = mesh24.intersect(
            ra="23:25:53.56",
            dec="+26:54:23.9",
            radius=old_div(10, (60 * 60)),
            inclusive=True
        )
        # print overlappingTrixels

        twoArcsec = 2.0 / 3600.
        raList1 = [200.0, 200.0, 200.0, 175.23, 21.36]
        decList1 = [24.3,  24.3,  24.3,  -28.25, -15.32]
        raList2 = [200.0, 200.0, 200.0, 175.23, 55.25]
        decList2 = [24.3 + 0.75 * twoArcsec, 24.3 + 0.25 * twoArcsec,
                    24.3 - 0.33 * twoArcsec, -28.25 + 0.58 * twoArcsec, 75.22]
        matchIndices1, matchIndices2, seps = mesh16.match(
            ra1=raList1,
            dec1=decList1,
            ra2=raList2,
            dec2=decList2,
            radius=twoArcsec,
            maxmatch=0
        )

        for m1, m2, s in zip(matchIndices1, matchIndices2, seps):
            print(raList1[m1], decList1[m1], " -> ", s * 3600.,
                  " arcsec -> ", raList2[m2], decList2[m2])

    def test_matcher_object(self):

        raList1 = ["13:20:00.00", 200.0, "13:20:00.00", 175.23, 21.36]
        decList1 = ["+24:18:00.00",  24.3,  "+24:18:00.00",  -28.25, -15.32]

        from HMpTy import Matcher
        coordinateSet = Matcher(
            log=log,
            ra=raList1,
            dec=decList1,
            depth=16
        )

        twoArcsec = 2.0 / 3600.
        raList2 = [200.0, 200.0, 200.0, 175.23, 55.25]
        decList2 = [24.3 + 0.75 * twoArcsec, 24.3 + 0.25 * twoArcsec,
                    24.3 - 0.33 * twoArcsec, -28.25 + 0.58 * twoArcsec, 75.22]

        matchIndices1, matchIndices2, seps = coordinateSet.match(
            ra=raList2,
            dec=decList2,
            radius=twoArcsec,
            maxmatch=0
        )

        for m1, m2, s in zip(matchIndices1, matchIndices2, seps):
            print(raList1[m1], decList1[m1], " -> ", s * 3600.,
                  " arcsec -> ", raList2[m2], decList2[m2])

        print("NEARESRT MATCHES ONLY")
        matchIndices1, matchIndices2, seps = coordinateSet.match(
            ra=raList2,
            dec=decList2,
            radius=twoArcsec,
            maxmatch=1
        )
        for m1, m2, s in zip(matchIndices1, matchIndices2, seps):
            print(raList1[m1], decList1[m1], " -> ", s * 3600.,
                  " arcsec -> ", raList2[m2], decList2[m2])

    def test_lookup(self):

        raList1 = ["13:20:00.00", 200.0, "13:20:00.00", 175.23, 21.36]
        decList1 = ["+24:18:00.00",  24.3,  "+24:18:00.00",  -28.25, -15.32]
        from HMpTy import HTM
        mesh16 = HTM(
            depth=16,
            log=log
        )
        print("LOOKUP")
        htmids = mesh16.lookup_id(raList1, decList1)
        for h, r, d in zip(htmids, raList1, decList1):
            print(r, d, " --> ", h)

    def test_htm_function_exception(self):

        from HMpTy import htm
        try:
            this = htm(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.get()
            assert False
        except Exception as e:
            assert True
            print(str(e))

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
