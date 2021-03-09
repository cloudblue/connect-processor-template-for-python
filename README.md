# Cookiecutter for CloudBlue Connect Processor  
  
Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), Cookiecutter for CloudBlue Connect Processor provides a framework for boostraping your custom processor for Connect.

With this project you can write your own processor that is capable of processing the requests in Connect for usecases like purchase/change/suspend/resume/cancel subscription requests along with usage reporting for Pay-as-you-go items and dynamic validation.

In order to create your own custom processor you will need to get familiar with the [Connect Rest API](https://connect.cloudblue.com/community/api/) and it's OpenAPI implementation using the [connect-openapi-client](https://github.com/cloudblue/connect-python-openapi-client).

## Features

* Works fit python 3.8 and 3.9
* Bootstraps a custom processor project within seconds
* Provides all needed dependencies
* Provides basic testing functionality including right mockers
* Compatible with github Actions
* Configures project licensing

## Usage

Creating a project that provides a connectprocessor package that could be run either using the [Connect CLI](https://github.com/cloudblue/connect-cli) or directly in [Connect](https://connect.cloudblue.com) is simple.

First of all, install in your local machine Cookiecutter, for example you can do it using pip:

	$ pip install cookiecutter

Once cookiecutter is installed you can instantiate it against this repository:

	$ cookiecutter https: https://github.com/cloudblue/connect-processor-template-for-python
 
 You'll be prompted for some values. Provide them and a Connect project will be created for you.

**Warning**: Please change sample data with your own desired information

	project_name [My Awesome Project]: My Awesome Processor
	project_slug [my_awesome_project]:
	description [My reports are really usefull!]:
	author: CloudBlue Vendor,
	version: 0.1.0,
    	license: [
      	  "Apache Software License 2.0",
     	   "MIT",
   	   "BSD” ],
    	Require_subscription_change_usecase: "y/n",
	Require_subscription_cancel_usecase: "y/n",
	Require_subscription_suspend_and_resume_usecase: "y/n"
	Require usage reporting for Pay-as-you-go usecase: "y/n"
	Require dynamic validation of ordering parameters for subscription: "y/n"
	Require reseller/customer information for provisioning: "y/n	
Done! Your project is ready to go!

Now you can access your recently created project folder and take a look arround it:

	$ cd my_awesome_report
	$ ls

Starting here, if you want you can put your project on a git repository, for example at github:

	$ git init
	$ git add .
	$ git commit -m "first commit"
	$ git remote add origin https://github.com/cloudblue/my_custom_processor.git
	$ git push -u origin master

Please take a look to our oficial [documentation site](https://connect.cloudblue.com) for more information on how to work with connect and this processor
