# Reveni Generic Module
This module has been created to be used as a base for other modules. It contains some generic features that are used in most of our modules.
1. Subscribe to webhooks **return.updated**  of reveni platform [_docs_](https://reveni.readme.io/reference/create-webhook)
2. When odoo receives a webhook from revei, a record is created in the **revei.webhook** model with the data from the webhook [data](https://reveni.readme.io/reference/event-data) if **status** == **in_progress** .
3. Automatically process the webhook data and create an RMA object in odoo.

## Developer Notes
1. In the model reveni event you need edit the method **process_return_created** to process the data from the webhook.
2. In the model reveni event you need edit the method **send_partial_validate** for send the data of validated or rejected RMA to reveni platform.


