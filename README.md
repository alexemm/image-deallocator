# Image Deallocator

This project takes an image file, divides it based on the chars of a given name for the image and 'deallocates' the image based on a new wished name, i.e. it assembles the image divisions into a new image. This functionality can e.g. be used for creation of memes from a specific format.

![Original Image: "lena"](https://github.com/alexemm/image_deallocator/blob/master/src/image_deallocator/img/0-lena.jpeg) becomes ![Generated image: "eeeeee"](https://github.com/alexemm/image_deallocator/blob/master/src/image_deallocator/new_img/lena/0/eeeeee/1/0.png)

<!--- https://images.pexels.com/photos/2092709/pexels-photo-2092709.jpeg?auto=compress&amp%3Bcs=tinysrgb&amp%3Bfit=crop&amp%3Bh=1200&amp%3Bw=800 --->

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
<!--- See deployment for notes on how to deploy the project on a live system. --->

### Prerequisites

To create a development environment similar to the environment used for initial development, follow these steps:

0. Install Python:

Install Python and PIP. You can do it in https://www.python.org/downloads/. Additionally, you have to install the virtual environment functionality with:
```
pip install virtualenv
```

1. Receive the code:

Go to a directory where you want to clone the code into and clone it:
```
git clone https://github.com/alexemm/image_deallocator.git
```
2. Create virtual environment:

Next, you should create a virtual environment for the dependencies which will be installed. The name of the virtual environment used for development is "venv" but it can be named otherwise. However, it is recommended to use venv as a name because this environment is included in the .gitignore:
```
cd image_deallocation
virtualenv venv
```
3. Install dependencies:

Go into the root folder of the project and install the python packages given in the requirements.txt
```
pip install -r requirements.txt
```

Now, that every installing step is covered, we are able to start the REST API.

### Installing

To make the development environment running in you local machine, you have to start the REST API:
Starting the REST API:
First, you go into the folder, where app.py is located. Then, you start the REST API:
```
cd src/image_deallocator
python app.py
```
If the REST API started successfully, then you see a console output like this:
```
* Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Now, you can use the REST API on localhost:5000. 
1. Upload an image:

To initially upload a picture, you can send a POST request to the REST API, e.g. with Postman. You include in form-data of the body a key "name" with the name of the person in your image and a key "file" with your image file (allowed endings: .jpg/ .jpeg, .png, .gif).

Then, you can send the request to "/upload".
If you receive "file successfully saved", the file was saved successfully. This file is served in the /img route.

2. Do an image deallocation:

You can deallocate an uploaded image by sending a POST request to the deallocate route. In the body of the request in the form-data, you include the keys: name, id, new_name and axis. 
After you sent the request and received the response "Task done", you can access the new image (or new images) in the /new_imgs route

Note: you can access the meta data which consists of the directories to the different images in the /meta route.

### Defined routes

GET routes
* "/meta": Get meta data with directories for the uploaded and generated images
* "/img": Access the uploaded images
* "/new_img": Access the generated images

POST routes
* "/upload": Upload image
* "/deallocate": Trigger image deallocation task

## Deployment

Currently, this project is mainly developed for prototype. Therefore, I only provide information for testing and using it.

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used to create the REST-API
* [Postman](https://www.postman.com/) - Used for sending REST requests and using the REST API, e.g. for testing

## Authors

* **Alexander Emmerich** - *Initial work* - [alexemm](https://github.com/alexemm)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to all the Memes which inspired me to do this.
* Thanks to [Tim Savage](https://www.instagram.com/timsavage/) for letting me use his image to have an example for this project.
* etc
