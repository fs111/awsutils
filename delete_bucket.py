#!/usr/bin/env python
"""
script to delete an entire S3 bucket including all it's content. The data is
deleted forever and cannot be restored. Be careful with this script!

Copyright: André Kelpe <efeshundertelf at googlemail dot com>
Licence: MIT
"""

import sys
from boto.s3.connection import S3Connection

def main():
    """main method to run the little script"""
    if len(sys.argv) != 2:
        print "usage: delete_bucket.py 'bucketname'"
        sys.exit(1)

    bucket_name = sys.argv[1]

    connection = S3Connection()
    bucket = connection.get_bucket(bucket_name)

    for key in bucket.list():
        key.delete()
    
    connection.delete_bucket(bucket_name)

if __name__ == "__main__":
    main()
