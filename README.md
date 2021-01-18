# Book Retrieval System (SI 650)

## How to run
The current project will need to be run using an IDE or the command line.
1. Clone the current repository to your local machine
2. Using the virtual environment to run the current application.

##### Install a virtual enviroment project4-env
        python3 -m pip install --user virtualenv    # For Mac/Linux...
        py -m pip install --user virtualenv    # For Windows

##### Create a new virtual environment called venv (will be in current folder)
        py -m venv venv    # For Mac/Linux... 
        python3 -m  venv venv     # For Windows
    
##### Activate project4-env
        source venv/bin/activate    # For Mac/Linux...
        venv\Scripts\activate    # For Windows
        (venv) # you've succeeded if you see this after!
        
##### Install all packages based on a list in a file called requirements.txt
        (venv) pip install -r requirements.txt

##### Run program
        flask run
        
#### Please make sure there is internet connection if the cache file is not in place.

#### How to use
1. Copy and paste the localhost base URL to a browser. Some localhost URL examples could be http://localhost:5000 or http://127.0.0.1:5000
2. Currently there are 3 pages on this web application. The URL and page contents are as the following:

#### Google chrome may not work. Edge usually work for this application
3. End the program with the instruction of your console and deactivate the virtual environment.

        
##### Deactivate the virtual environment
        (venv) deactivate
