**Connect Processor Template in Python**

The Connect Processor Template for Python provides developers an complete skeleton to start their automation project using the Connect Open API Client.

In order to use this library, please ensure that you have read first the documentation available on Connect knowledge base article located here.
This documentation is exclussive and comprehensive that will provide information on the Connect Processor Template. 
The Connect Processor built from this Template should automate the provisioning of subscription requests in Connect.

**Requirements**

In order to use this template you will need an environment capable to run Python scripts, Python 3.6 is supported.
Installation

The Example Connect Processor must be deployed on any environment with Python minimum required version: 3.6.

Complete the steps below to install the required packages and to deploy Example Connect Processor

    Run the following command to install Python 3 on CentOS 7:

sudo yum install centos-release-scl
sudo yum install rh-python36
scl enable rh-python36 bash

2. Install Development Tools by running this command:

sudo yum groupinstall 'Development Tools'


3. Save the Example Connect Processor on the desired location.
For example: /usr/processor/ExampleConnectProcessor/

Assuming that you have python and virtualenv installed, and forked the connect-python-sdk repository, set up your environment and install the required dependencies like this:

$ git clone https://github.com/{your_github_account}/connect-processor-template-for-python.git
$ cd connect-python-sdk
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements/test.txt


4. Powered by Cookiecutter, Cookiecutter for CloudBlue Connect Processor provides a framework for bootstrapping your custom processor for Connect.
With this project, you can write your own processor that is capable of processing the requests in Connect for use-cases like purchase/change/suspend/resume/cancel subscription requests along with usage reporting for Pay-as-you-go items and dynamic validation.
First of all, install in your local machine Cookiecutter, for example, you can do it using pip:

$ pip install cookiecutter

Once cookiecutter is installed you can instantiate it against this repository:

$ cookiecutter https://github.com/cloudblue/connect-processor-template-for-python

You'll be prompted for some values. Provide them and a Connect project will be created for you.

Warning: Please change sample data with your own desired information

project_name [My Connect Processor]: My Awesome Processor
project_slug [my_connect_processor]:
description [My processor will auto-process subscription requests in CloudBlue Connect]:
author: CloudBlue Vendor,
Require_subscription_change_usecase [y/n]: y
Require_subscription_cancel_usecase [y/n]: y
Require_subscription_suspend_and_resume_usecases [y/n]: y
Require_usage_reporting_for_Pay_as_you_go_usecase [y/n]: y
Require_dynamic_validation_of_ordering_parameters_for_subscription [y/n]: y
Require_reseller_information_for_provisioning [y/n]: y	
Done! Your project is ready to go!

Now you can access your recently created project folder and take a look around it:

$ cd my_connect_processor
$ ls


5. Create a Virtual Environment inside the connector folder <processor application folder name> by running the following command:
cd /usr/processor/<processor application folder name>.
scl enable rh-python36 bash
python -m venv venv
source venv/bin/activate

Run this command to install the package requirements:
venv/bin/pip install -r requirements.txt


6. Running tests

The connect-processor-template-for-python uses unittest for unit testing.

To run the entire tests suite, from the tests directory, execute:

$ python -m unittest launcher.py


7. Set up the configurations

Provide Connect API end point and token in config.json

Provide Product Id from Connect in Globals.py

Refer - 2. Configurations from Documentation
