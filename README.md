**_WebRec_**

**General**


The purpose of this code is to provide 
a REST-ful API on top of the Lenskit
package. 

**_Local verson_**

**Get started**

To test the API, you can follow next steps:

1) Download this code

2) Install 

2) Run app.py





**_Deployment_**

We used docker to wrap up the code
and its dependencies into a container.
The reason for this wrapping is to enable
a fast deployment on different servers.

The docker version used for testing is 
**18.03.0-ce** 

**Get started**

1. Install docker
2. Download the code
3. Go to the folder
```sh
$ cd path/to/Webrec
```
4. Remove the running docker (if needed)
```sh 
$ docker rm imagerun
```
5. Build the image
```sh 
$ docker build -t imagebuild .
```
6. Run the image
    a) interactive (debug)
    b) normal
    c) background
```sh 
$ docker run -it --name imagerun -p 4000:80 imagebuild /bin/bash
$ docker run --name imagerun -p 4000:80 imagebuild 
$ docker run -d -p 4000:80 imagebuild
```  
7. Test if it is working by checking
`localhost:4000/Home`
    
