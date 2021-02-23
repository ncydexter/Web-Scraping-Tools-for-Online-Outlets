import datetime
import os
import pandas as pd
import sys
#import itertools
import re

def chk3files(fpath, files, errorind):
    if len(files) < 3:
        print("Message: ")
        print("Not all 3 files (log, product spec and raw quotations) are in the output!")
        print("")
        errorind = 1

    if len(files) > 3:
        print("Message: ")
        print("More than 3 files are in the output. Please delete unused records and files.")
        print("")
        errorind = 1

    chklist = ["log", "ProductSpec", "RawQuotation"]
    for chk in chklist:
        if [i for i in os.listdir(fpath) if os.path.isfile(os.path.join(fpath, i)) and chk in i] == []:
            print("Message: ")
            print(chk + " file is missing.")
            print("")
            errorind = 1

    return errorind


def chklog(fpath, files, errorind):
    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    print("Log files " + files[0] + " Checking: ")

    file = [i for i in files if "log" in i]
    with open(os.path.join(fpath, file[0]), encoding = "utf-8") as f:

        if "Start of Program Run" not in f.read():
            print("Message:")
            print("Program did not start successfully.")
            print("")
            errorind = 1
        f.seek(0)

        if "End of Program Run" not in f.read():
            print("Message:")
            print("Program did not end successfully.")
            print("")
            errorind = 1
        f.seek(0)

        if "Successfully Output CSV files" not in f.read():
            print("Message:")
            print("CSV Files are not exported sucessfully.")
            print("")
            errorind = 1
        f.seek(0)

    print("Log files " + files[0] + " Checking Ends")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("")

    return errorind


def chkspec(fpath, curfiles, prvfiles, errorind):
    curfile = [i for i in curfiles if "Spec" in i]
    prvfile = [i for i in prvfiles if "Spec" in i]

    dfcur = pd.read_csv(os.path.join(fpath, curfile[0]))
    dfprv = pd.read_csv(os.path.join(fpath, prvfile[0]))

    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    print("Product Specification Checking: ")

    if len(dfcur.columns) == len(dfprv.columns):
        print("[OK] Column number checked.")
    else:
        print("[X] Invalid column number.")
        errorind = 1

    if len(dfcur.columns) == sum([1 for i, j in zip(dfcur.columns, dfprv.columns) if i == j]):
        print("[OK] Column names checked.")
    else:
        print("[X] Column names mismatch.")
        errorind = 1

    spec_ratio = len(dfcur)/len(dfprv)
    print("Product Spec Ratio (current date observations against compared date): ", spec_ratio)
    if spec_ratio < 0.5 or spec_ratio > 1.5:
        print("")
        print("The product spec ratio is largely deviated from 1.")
        print("A possible reason is product are replaced today.")
        print("")

    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("")
    return errorind


def chkquot(fpath, curfiles, prvfiles, errorind):
    curfile = [i for i in curfiles if "Quot" in i]
    prvfile = [i for i in prvfiles if "Quot" in i]

    dfcur = pd.read_csv(os.path.join(fpath, curfile[0]))
    dfprv = pd.read_csv(os.path.join(fpath, prvfile[0]))

    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    print("Raw Quotation Checking: ")

    if len(dfcur.columns) == len(dfprv.columns):
        print("[OK] Column number checked.")
    else:
        print("[X] Invalid column number.")
        errorind = 1

    if len(dfcur.columns) == sum([1 for i, j in zip(dfcur.columns, dfprv.columns) if i == j]):
        print("[OK] Column names checked.")
    else:
        print("[X] Column names mismatch.")
        errorind = 1

    quot_ratio = len(dfcur)/len(dfprv)
    print("Quotation Ratio (current date observations against compared date): ", quot_ratio)
    print("")
    if quot_ratio < 0.5 or quot_ratio > 1.5:
        print("The quotation ratio is deviated from 1.")
        print("A possible reason is product are replaced today.")
        print("")

    avail_cur = dfcur.pivot_table(index='Availability', values="RecordNo", aggfunc='count')
    avail_cur = avail_cur.rename(columns={"RecordNo": "Current_Count"})

    avail_prv = dfprv.pivot_table(index='Availability', values="RecordNo", aggfunc='count')
    avail_prv = avail_prv.rename(columns={"RecordNo": "Previous_Count"})

    avail = avail_cur.merge(avail_prv, left_on="Availability", right_on="Availability")

    print(avail)
    print("")

    avail_ratio = dfcur["Availability"].mean() - dfprv["Availability"].mean()

    print("Average availability ratio difference (current date observations against compared date): ", avail_ratio)
    if avail_ratio < 0.1 or avail_ratio > 0.1:
        print("There is a large difference in average availability.")
        print("Please double check the data.")
        print("")

    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("")
    return errorind


def chkall(fpath, curfiles, prvfiles, errorind, fname, cdate, ctime):
    OK = 0

    if chk3files(fpath, curfiles, errorind) == 1:
        print("Errors in current 3 files.")
        errorind = 1

    elif chk3files(fpath, prvfiles, errorind) == 1:
        print("Errors in previous 3 files.")
        errorind = 1

    elif chklog(fpath, curfiles, errorind) == 1:
        print("Errors in current log file.")
        errorind = 1

    elif chklog(fpath, prvfiles, errorind) == 1:
        print("Errors in previous log file.")
        errorind = 1

    elif chkspec(fpath, curfiles, prvfiles, errorind) == 1:
        print("Errors in Product Specification file.")
        errorind = 1

    elif chkquot(fpath, curfiles, prvfiles, errorind) == 1:
        print("Errors in Raw Quotation file.")
        errorind = 1

    OK = 1 - errorind

    if OK == 1:
        f = open(fname + "_" + cdate + "-" + ctime + ".ok", "a")
        f.write(" ")
        f.close()
        print("OK file ready.")

    else:
        f = open(fname + "_" + cdate + "-" + ctime + ".nok", "a")
        f.write(" ")
        f.close()
        print("NOK file ready.")

    return


def main(OutletName, fpath):
    # OutletName = "NEXT"
    # fpath = "R:/CPI_SD/Online Pricing/Regular Price Collection/" + OutletName + "/Data/"


    cdate = datetime.datetime.now().strftime("%Y%m%d")
    ctime = datetime.datetime.now().strftime("%H%M")
    # bdate = (datetime.date.today() + datetime.timedelta(days=-21)).strftime("%Y%m%d")
    # btime = "0000"

    sys.stdout = open(OutletName + '_' + cdate + '-' + ctime + '_OK_log.txt', 'w', encoding='utf-8-sig')

    print("**********************************************************************")
    print("Checking starts: ")
    print("**********************************************************************")

    print("Outlet: ", OutletName)

    fname = OutletName

    print("Current date: ", cdate)

    allfiles = [i for i in os.listdir(fpath) if os.path.isfile(os.path.join(fpath, i))]
    allfiles.sort(reverse=True)
    #print(allfiles)

    curfiles = allfiles[0:3]
    prvfiles = allfiles[3:6]

    # curfiles = [i for i in os.listdir(fpath) if
    #             os.path.isfile(os.path.join(fpath, i)) and str(cdate) + "-" + str(ctime) in i]
    #
    # rngdate = range(int(cdate), int(bdate), -1)
    # rngtime = range(int(ctime), int(btime), -1)
    # rngdatetime = [rngdate, rngtime]
    #
    # for idate, itime in itertools.product(*rngdatetime):
    #     prvfiles = [i for i in os.listdir(fpath) if
    #                 os.path.isfile(os.path.join(fpath, i)) and str(idate).rjust(4, '0') + "-" + str(itime).rjust(4,'0') in i]
    #     if prvfiles != [] and prvfiles != len(prvfiles) == sum([1 for i, j in zip(prvfiles, curfiles) if i == j]):
    #         break

    print("Current Files Checking: ", curfiles)
    print("against previous files: ", prvfiles)
    print("")


    errorind = 0

    cur = []
    prv = []
    for i in curfiles:
        match = re.search(r'\d{8}-\d{2}\d{2}', i)
        cur.append(datetime.datetime.strptime(match.group(), '%Y%m%d-%H%M').date())

    for i in prvfiles:
        match = re.search(r'\d{4}\d{2}\d{2}-\d{2}\d{2}', i)
        prv.append(datetime.datetime.strptime(match.group(), '%Y%m%d-%H%M').date())

    if len(set(cur)) != 1:
        print("Wrong current inputs.")
    elif len(set(prv)) != 1:
        print("Wrong previous inputs.")
    else:
        print("Correct Input files.")

    print("")

    chkall(fpath, curfiles, prvfiles, errorind, fname, cdate, ctime)

    sys.stdout.close()

    return


OutletName = "CDWarehouse"
fpath = "R:/CPI_SD/Online Pricing/Regular Price Collection/" + OutletName + "/Data/"

main(OutletName, fpath)

#main(sys.argv[1], sys.argv[2])