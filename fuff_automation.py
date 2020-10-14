#!/usr/bin/env python

import optparse
import subprocess
from itertools import islice


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-l", "--urls", dest="url", help="list of urls to use")
    parser.add_option("-w", "--wordlist", dest="wordlist", help="path to wordlist")
    parser.add_option("-t", "--threads", dest="threads", help="number of threads")
    (options, arguments) = parser.parse_args()
    if not options.url:
        parser.error("please write url list")
    elif not options.wordlist:
        parser.error("please enter path to wordlist")
    elif not options.threads:
        parser.error("please define the number of threads")
    return options


def ffuf(urls, wordlist):
    processes = []
    print("inserting new 5 urls")
    for url in urls:
        fuzz = str(url) + "/FUZZ"
        text = str(url) + ".txt"
        p = subprocess.Popen(["ffuf", "-w", wordlist, "-u", url, "-o", text])
        processes.append(p)
    for p in processes:
        if p.wait() != 0:
            print("There was an error")
    print("the 5 urls finished fuzzing")


def first_urls(all_urls, start_line, end_line):
    with open(all_urls, "r") as urls:
        first_lines = islice(urls, int(start_line), int(end_line))
    return first_lines


options = get_arguments()
start = 1
end = options.threads
while True:
    five_urls = first_urls(options.url, start, end)
    if not five_urls:
        break
    else:
        ffuf(five_urls, options.wordlist)
        start = start + options.threads
        end = end + options.threads
print("finally finished ffufing")

