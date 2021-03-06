#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A simple script to create a public bucket in S3 for hosting 
static content. For more information please read the s3 documentation:
http://docs.amazonwebservices.com/AmazonS3/latest/dev/WebsiteHosting.html

The heavy lifting is done by the excellent boto library:
http://boto.cloudhackers.com/en/latest/index.html


Copyright: André Kelpe <efeshundertelf at googlemail dot com>
Licence: MIT
"""
import sys

from boto.s3.connection import S3Connection

# policy for the bucket so that keys are world readable by
# default as described in the docs
POLICY_TEMPLATE = '''{
  "Version":"2008-10-17",
  "Statement":[{
    "Sid":"PublicReadForGetBucketObjects",
        "Effect":"Allow",
      "Principal": {
            "AWS": "*"
         },
      "Action":["s3:GetObject"],
      "Resource":["arn:aws:s3:::%s/*"
      ]
    }
  ]
}'''

def main():
    """main method to run the little script"""
    if len(sys.argv) != 2:
        print "usage: create_open_bucket.py 'bucketname'"
        sys.exit(1)
    
    bucket_name = sys.argv[1]
    connection = S3Connection()
    
    bucket = connection.create_bucket(bucket_name)
    bucket.set_policy(POLICY_TEMPLATE % (bucket_name))
    
    bucket.configure_website("index.html", error_key="404.html")

    for key, content in ("index.html", "Hello S3"), ("404.html", "Not found"):
        newKey = bucket.new_key(key)
        newKey.metadata.update({"Content-Type" : "text/html"})
        newKey.set_contents_from_string('''
               <html>
                   <head><title>%s</title></head>
                   <body><p>%s</p></body>
               </html>''' % (content, content))

    print "To finish the setup, create a CNAME entry for %s pointing to %s " % (
               bucket_name,
                   bucket.get_website_endpoint())


if __name__ == "__main__":
    main()
