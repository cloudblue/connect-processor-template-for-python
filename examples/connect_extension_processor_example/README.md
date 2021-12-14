# Welcome to ConnectExtensionProcessorExampleExtension !


Connect Extension as a Service Processor Example using a Mock API Endpoint 


## Connect Product Configuration
This are the Connect Product configuration details  which requests are processed by this Extension used in Connect DevOps Module.
* **API Endpoint**: this Extension process Connect fulfillment requests via the Mock API created with Apiary.io tool to be used in this Processor Example
is https://vendorexample.docs.apiary.io/# . This API does not require any Authorization
to make the API calls.

* **Use cases**:
This Example Processor supports the following use cases:
    * Purchase
    * Cancel
    * Suspend
    * Resume
    * Change

* **Product capabilities**: In order to be able to support suspend and resume use cases, this product has enabled
the Administrative Hold capability in Connect general product menu.

* **Items**: This Mock product offers only one MPN or SKU: MPN-A, and upgrades and downgrades
are not allowed.

* **Parameters**: Only one fulfillment phase parameter named subscription_id, for reconciliation, must be
completed for each purchase request.
The parameter name is used in the processor to call the Connect API and complete the
value, before approving a purchase request, or retrieve the value to validate the change
requests.

## DevOps Service Configuration
The service using this  Extension should have two environment variables:
* API_ENDPOINT: Enter the endpoint URL from https://vendorexample.docs.apiary.io/#. Like "https://private-anon-9e7487c9df-vendorexample.apiary-mock.com"
* ACTIVATION_TEMPLATE_NAME: "Default Activation Template"

## License

**ConnectExtensionProcessorExampleExtension** is licensed under the *Apache Software License 2.0* license.

