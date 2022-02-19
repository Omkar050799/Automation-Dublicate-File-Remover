'''
# 1)  ✔ Accept Directory name from user and delete all duplicate files from the specified directory by considering the checksum of files.
# 2)  ✔ Create one Directory and inside that directory create log file which maintains all names of duplicate files which are deleted.
# 3)  ✔ Name of that log file should contains the date and time at which that file gets created.
# 4)  ✔ Accept duration in minutes from user and perform task of duplicate file removal after the specific time interval.
# 5)  ✔ Accept Mail id from user and send the attachment of the log file.
# Mail body should contains below things :---------------
# 6)  ✔ Starting time of scanning
# 7)  ✔ Total number of files scanned
# 8)  ✔ Total number of duplicate files found
#        Note :-------
# 9)  ✔ For every separate task write separate function.
# 10) ✔ Write all user defined functions in one user defined module.
# 11) ✔ Use proper validation techniques.
# 12) ✔ Provide Help and usage option for script.
# 13) ✔ Mail body should contains statistics about the operation of duplicate file

'''
###################################################################################################################################################


from datetime import datetime
import os
import hashlib
import time
from urllib.request import urlopen
import smtplib
import schedule
from sys import *
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import datetime
import shutil


def is_connected():
    try:
        urlopen('http://www.kite.com', timeout=5)
        return True

    except Exception as err:
        return False


def MailSender(
                filename,
                time,
                MailID,
                FileCountX,
                FileCountX1
                ):
    try:
        fromaddr = "omimalpote9130@gmail.com"
        toaddr = MailID

        msg = MIMEMultipart()

        msg['from'] = fromaddr

        msg['To'] = toaddr

        body = """
        Hello %s,
        jumanji: welcome to the jungle......
        Please find attachedment Document which contains Log of Duplicate Deleted files.
        The Total Number of Scanned Files are : %s
        The Number of Files Which Are Duplicates : %s
        Log file Takes time : %s
        Log File created at : %s

        This is auto genereted mail.

        Thanks & Modakk Pathvun dyaa,
        Omkar K. Malpote
        Aplach master
          """ % (toaddr,FileCountX1,FileCountX, time,datetime.datetime.now())

        Subject = """
        Duplicate file log generated at : %s
        """ % (datetime.datetime.now())

        msg['Subject'] = Subject

        msg.attach(MIMEText(body, 'plain'))

        attachment = open(filename, "rb")

        p = MIMEBase('application', 'octet-stream')

        p.set_payload((attachment).read())

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()

        s.login(fromaddr, "89565580")

        text = msg.as_string()

        s.sendmail(fromaddr, toaddr, text)

        s.quit()

        print("Your Mail Delivered to your given adderess..")

        print("Log file Succefully send through Mail")

        return True
    except Exception as E:
        print("Error is Occured", E)


# Working of Function is to Delete the Duplicates
def DeleteFiles(
                dict1
                ):

    results = list(filter(lambda x: len(x) > 1, dict1.values()))

    dups2 = {}
    icnt = 0
    iCnt2 = 0
    i = 0

    if len(results) > 0:
        for result in results:
            for subresult in result:

                icnt += 1
                i += 1
                if icnt >= 2:
                    print(subresult)
                    dups2[i] = subresult
                    os.remove(subresult)
                    iCnt2 += 1

            icnt = 0
        '''  
        # Remove Extra Names
        temp = []
        res = dict()
        for key, val in dups2.items():
            if val not in temp:
                temp.append(val)
                res[key] = val
        '''
    else:
        print("No duplicate files found : ")
        dups2[i] = 'No duplicate files found : '

    print("Delete File:\n",dups2)
    return dups2,iCnt2

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Working of Function is to check file 1 by 1 and return the CheckSum of File

def hashfile(
             path,
             blocksize=1024
            ):
    afile = open(path, "rb")
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


# Working of Function is to Find Duplicates
def findDup(
            path
            ):
    flag = os.path.isabs(path)

    if flag == False:
        path = os.path.abspath(path)

    exists = os.path.isdir(path)

    dups = {}
    iCnt3 = 0

    if exists:
        for dirName, subdirs, fileList in os.walk(path):
            print("Current folder is : ", dirName)
            for filen in fileList:
                path = os.path.join(dirName, filen)
                file_hash = hashfile(path)
                iCnt3 += 1
                if file_hash in dups:
                    dups[file_hash].append(path)
                else:
                    dups[file_hash] = [path]

    return dups,iCnt3


# Working of Function is to Print Duplicate File With Absolute Path
def printResults(
                 dict1
                ):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))

    iCnt3 = 0

    NameX1 = 'log.txt-'
    NameX2 = datetime.datetime.now()
    NameX3 = NameX1 + str(NameX2)

    fd = open(NameX3, 'x')
    fd.write("Hey Boss Here your data,Please Check")
    fileName = NameX3

    if len(results) > 0:
        print('Duplicates Found: ')
        print('Following files are duplicate')
        fd.write('\nDuplicates Found: ')
        fd.write('\nFollowing files are duplicate')
        '''
        for result in results:
           for subresult in result:
            print("\t\t%s" % subresult)
            fd = open(NameX3, 'a')
            fd.write("\n")

            iCnt3 += 1
            LResult = str(results)
            fd.write(LResult)
        '''
        for x in range(len(results)):
            print("\t\t%s" % results[x])
            fd = open(NameX3, 'a')
            fd.write("\n")

            iCnt3 += 1
            fd.write(results[x])
    else:
        fd = open(NameX3, 'a')
        fd.write("\n")

        iCnt3 += 1
        fd.write("No duplicate files found.")
        print("No duplicate files found.")

    return fileName

# Working of Function is make 1 directory and move our created log file in it
def MakeDir(
            FileNameX,
            DirName='LogFiles'
            ):

    if not os.path.exists(DirName):
        os.mkdir(DirName)

    GivenDirPath = os.getcwd()
    CreatedDirPath = os.path.join(GivenDirPath, DirName)

    if os.path.exists(FileNameX):
        shutil.move(FileNameX, CreatedDirPath)
    print("Your File Gets Moved into folder")


'''
def Create(Name, DirName='LogFiles'):
    global abs, fd
    File_Name = DirName + datetime.now().strftime("%H-%M-%S") + ".txt"
    if not os.path.exists(DirName):
        os.mkdir(DirName)
    for root, dir, file in os.walk("."):
        for dirnames in dir:
            abs = os.path.join(os.getcwd(), DirName, File_Name)
            if not os.path.exists(abs):
                fd = open(abs, "a")
                Heading = "=" * 80
                fd.write(Heading)
                fd.write(f"\nRecords of Removed Duplicate Files From Directory : {Name} \n")
                fd.write(Heading)
                fd.write("\n")
 '''

# Callie Funcion
def CallX():

    try:

        arr = {}
        startTime = time.time()
        arr,TotalCount2 = findDup(argv[1])
        arr,DeleteCount1 = DeleteFiles(arr)
        FileNameX = printResults(arr)
        endTime = time.time()
        FinalTimeX = (endTime - startTime)

        print("Took %s seconds to evaluate." % (endTime - startTime))

        connected = is_connected()

        if connected:
            bRet = MailSender(FileNameX, FinalTimeX,argv[3],DeleteCount1,TotalCount2)
        else:
            print("Enable to connect internet...")

        if bRet == True:
            MakeDir(FileNameX)

    except ValueError:
        print("Error : Invalid datatype of input...")

    except Exception as E:
        print("Error : Invalid input", E)


# Main Function
def main():
    print("------------------- : Automation 1 ---------------------")
    print("Script Name : ", argv[0])

    if ((len(argv) != 4)):
        print("Invalid Number of Arguments.....")
        print("Use -u flag for ussage...")
        print("Use -h flag for Help.....")
        exit()

    if argv[1] == "-u" or argv[1] == "-U":
        print("Usage : Script is used to traverse the Specific Directory and delete duplicate files and send 1 log file to your given mail address")
        exit()

    if ((argv[1] == "-h") or (argv[1] == "-H")):
        print("First_Argument : ApplicationName AbsolutePath_of_Directory Extension....")
        print("Second_Argument : Time in minitus for Getting you delelted file records... ex- for 20 mini = '20'")
        print("Third_Argument : The mail Address Where you wants to send the log file of data...")

        exit()

    schedule.every(int(argv[2])).minutes.do(CallX)

    while True:
        schedule.run_pending()
        time.sleep(1)

    #CallX()

    print("Application gets Terminated.....")


# Starter of the automation script
if __name__ == '__main__':
    main()
