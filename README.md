# Connect Processor Template for Python


## Introduction

The Connect Processor Template for Python provides developers an complete skeleton to start their automation project using the Connect Open API Client.

In order to use this project, please ensure that you have read first the documentation available on Connect knowledge base article located here.
This documentation is exclusive and comprehensive that will provide information on the Connect Processor Template. 

The Connect Processor built from this template automates the fulfillment of product requests in CloudBlue Connect.
You will build a processor capable of automatically process your own Product Requests in Connect, including all use-cases like purchase/change/suspend/resume/cancel subscription requests along with usage reporting for Pay-as-you-go items, Tier Config requests, and Dynamic Validation.

Your code may use any scheduler to execute, from a simple cron to a cloud scheduler like the ones available in Azure, Google, Amazon or other cloud platforms.

**Requirements**

In order to use this project, you will need an environment capable to run Python scripts. Python 3.6 or later is supported.

**Installation**

Assuming that you have Python 3.6 or later installed, complete the steps below to install the required packages and to deploy Connect Processor Template for Python

    
1. Fork the connect-processor-template-for-python repository

Create a copy of a this repository or branch, using git:

```
    $ git clone https://github.com/{your_github_account}/connect-processor-template-for-python.git
```

2. Install Cookiecutter

Install in your local machine Cookiecutter, for example, you can do it using pip:

```
     $ pip install cookiecutter
```

3. Once Cookiecutter is installed you can instantiate it against your forked or copied repository:
```
    $ cookiecutter https://github.com/{your_github_account}/connect-processor-template-for-python
```
You'll be prompted for some values. Provide them and a Connect project will be created for you.

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

4.  Install the required dependencies 
Run this command to install the package requirements:
``` 
    $ pip install -r requirements/dev.txt
```

5. Set up your Environment
Assuming that you have python and virtualenv installed, you can reate a Virtual Environment inside the connector folder <processor application folder name> by running the following command:  
  ```
    $ cd my_connect_processor
    cd /usr/processor/<processor application folder name>.
    scl enable rh-python36 bash
    python -m venv venv
    source venv/bin/activate
```

6. Set up the configurations

Provide your own Connect API end point and token in config.json. 

Provide Product Ids and other data from Connect in Globals.py.

Please take a look to our oficial [documentation site](https://connect.cloudblue.com/community/modules/extensions/api-tokens/) for more information.


**Running tests**

The Connect Processor Template for Python uses unit tests for unit testing.

To run the entire tests suite, from the tests directory, execute:
```
    $ python -m unittest launcher.py
```

