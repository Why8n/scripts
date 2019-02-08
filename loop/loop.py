#!/usr/bin/python

import subprocess
import sys
import time

def usage():
    return r'usage: loop cmd'

def run(cmd):
    return subprocess.call(cmd)

def parseArgs():
    import argparse
    parser = argparse.ArgumentParser(description='auto execute commands until sucessfully')
    parser.add_argument('-t','--times',type=int,nargs='?',const=sys.maxsize,default=sys.maxsize,help='retry times (default:{})'.format(sys.maxsize))
    parser.add_argument('cmd',nargs=argparse.REMAINDER,metavar='command',help='original command')
    args = parser.parse_args()
    return args.times,args.cmd


def loop():
    retryCount,cmd = parseArgs()
    curCount = 0
    while curCount < retryCount:
        if run(cmd) == 0:
            break
        curCount+=1
        print('retry: %d,cmd=%s' %(curCount,cmd))    
        print()
        time.sleep(1)


if __name__ == '__main__':
    loop()
    print('loop command done!!!')
     
