# Connect Processor Template for Python


## Introduction

The Connect Processor Template for Python provides developers a complete skeleton to start their automation project using the Connect Open API Client.

In order to use this project, please ensure that you have read first the documentation available on Connect knowledge base article located here.
This documentation is exclusive and comprehensive that will provide information on the Connect Processor Template. 

The Connect Processor built from this template automates the fulfillment of product requests in CloudBlue Connect.
You will build a processor capable of automatically process your own Product Requests in Connect, including all use-cases like purchase/change/suspend/resume/cancel subscription requests along with usage reporting for Pay-as-you-go items, Tier Config requests, and Dynamic Validation.

Your code may use any scheduler to execute, from a simple cron to a cloud scheduler like the ones available in Azure, Google, Amazon, or other cloud platforms.

## Requirements

In order to use this project, you will need an environment capable to run Python scripts. Python 3.6 or later is supported.

## Installation

Assuming that you have Python 3.6 or later installed, complete the steps below to install the required packages and to deploy Connect Processor Template for Python


**1. Install Cookiecutter**

Install in your local machine Cookiecutter, for example, you can do it using pip:

```
     $ pip install cookiecutter
```

**2. Create your Connect Processor project**

Once Cookiecutter is installed you can instantiate it to create your Connect Processor project:
```
    $ cookiecutter https://github.com/cloudblue/connect-processor-template-for-python
```
You'll be prompted for some values. Provide them and a Connect Processor project will be created for you.

**Warning**: Please change sample data with your own desired information:
```
    project_name [My Connect Processor]: My Awesome Processor
    project_slug [my_connect_processor]: my_connect_processor
    description [My processor will auto-process subscription requests in CloudBlue Connect]:
    author: CloudBlue Vendor,
    Require_subscription_change_usecase [y/n]: y
    Require_subscription_cancel_usecase [y/n]: y
    Require_subscription_suspend_and_resume_usecases [y/n]: y
    Require_usage_reporting_for_Pay_as_you_go_usecase [y/n]: y
    Require_dynamic_validation_of_ordering_parameters_for_subscription [y/n]: y
    Require_reseller_information_for_provisioning [y/n]: y	
    Done! Your project is ready to go!
```

Now you can access your recently created project folder and take a look around it:
```
    $ cd my_connect_processor
    $ ls
```

**3.  Install the required dependencies**
Run this command to install the package requirements:
``` 
    $ pip install -r requirements/dev.txt
```

**4. Set up your Environment**
Assuming that you have python and virtualenv installed, you can create a virtual environment inside the connector folder <processor application folder name> by running the following command:  
  ```
    $ cd my_connect_processor
    cd /usr/processor/<processor application folder name>.
    scl enable rh-python36 bash
    python -m venv venv
    source venv/bin/activate
```

**5. Set up the configurations**

Provide your own Connect API endpoint and token in config.json.  If your processor support report_usage use case, configure the rootPathUsage to create and store the usage reports.

Provide Product Ids and other data from your Connect product in Globals.py.

Please take a look at our official [documentation site](https://connect.cloudblue.com/community/modules/extensions/api-tokens/) for more information.


## Running tests

The Connect Processor Template for Python uses unit tests for unit testing.

To run the entire tests suite, from the tests directory, execute:
```
    $ python -m unittest launcher.py
```

## Example Processor

Find in the Examples folder of this project some Connect Processor examples, created from this template, 
and completely developed with the basic Connect Product Requests use cases.