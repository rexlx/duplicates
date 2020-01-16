import os
import argparse
import pathlib
from collections import defaultdict

user_source = "./"

def get_args():
    """
    gets cli args via the argparse module
    """
    msg = "This script organizes photos by year"
    # create an instance of parser from the argparse module
    parser = argparse.ArgumentParser(description=msg)
    # add expected arguments
    parser.add_argument('-s', dest='source', required=False, help="source dir")
    # parser.add_argument('-g', dest='get_size', required=False, help="compare sizes")
    args = parser.parse_args()
    if args.source:
        source = args.source
    else:
        source = user_source
    return source


def get_files(source):
    """
    utilizes the os module walk function to create
    a list of files recursively
    """
    # list comprehension the joins the direcctory
    # path and file name
    file_list = [os.path.join(dir_path, x)
                 for dir_path, dirs, files in os.walk(source)
                 for x in files]
    return file_list


def get_dups(files):
    """
    creates a dictionary of duplicate files and their sizes
    """
    # this create a dict we can append to
    results = defaultdict(list)
    for i in files:
        # get the pure path of each file
        p = pathlib.PurePath(i)
        try:
            # try and get the size of it
            size = pathlib.Path(i).stat().st_size
        except Exception as e:
            # or set to zero
            size = 0
            # restart at top of loop
            continue
        # extract filename from full path
        f = p.parts[-1]
        # throw the path and size into its own dict
        data = {"path": i, "size": size}
        # append the list with the filename as the key
        results[f].append(data)
    return results

def main():
    # init this to keep track of total size
    total_size = 0
    # get the args
    src = get_args()
    # walk the specified dir creating the file list
    files = get_files(src)
    # get our results dict
    results = get_dups(files)
    # iter over it
    for k, v in results.items():
        # if the value (list of dictionaries) containes more than one
        if len(v) > 1:
            # create a nice border to separate the data
            print("_"*80)
            print("found duplicates for {}:".format(k).upper())
            print("-"*80)
            # print the dups for that key
            for i in range(0, len(v)):
                print("path: {} | size: {}".format(v[i]["path"], v[i]["size"]))
                # increase the totalsize accordingly
                total_size += v[i]["size"]
    usg_msg = "total size of duplicates (for all files) is {}MiB"
    print(usg_msg.format(total_size / (1024 ** 2)))
                




if __name__ == "__main__":
    main()

