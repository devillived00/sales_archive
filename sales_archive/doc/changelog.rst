v15.0.1.1
=========
* Added unit tests.

v15.0.1.0
=========
* Added Transient model for Custom Sale Reports.
* Created wizard views.
* Updated access rights.

v15.0.0.3
=========
* Added controller which prevents not Admin users from going debug mode.

v15.0.0.2
=========
* Created SaleOrderArchive model with required fields.
* Created Cron with function which gathers Sale Orders in state 'sale' or 'cancel and checks if any of them was last modified more than 30 days ago.
  For Sale Orders last modified later than 30 days ago, new SaleOrderArchive is created and then SaleOrder is being removed.
* Created acces rights.
* Created Tree and Form view for the model.

v15.0.0.1
=========
* Module initializaiton.
