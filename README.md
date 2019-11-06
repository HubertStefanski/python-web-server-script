# python-web-server-script
AWS automation script for creating an instance and setting up a http server to display an image from a s3 bucket which was transfered from another url

# syntax for creation
* assuming credentials and .pem key has been changed in-code 
- python3 run_newwebserver.py http://address.com/image.jpg 
- If no jpg address has been specified, then a default image is set
