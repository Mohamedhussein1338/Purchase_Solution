Purchase request:
• Module integrates with Odoo purchase module and provide functionality for requesting
purchase orders and approving them before purchase orders are created .# Purchase_Solution
Purchase Request Cycle Solution
Task
You are required to create a module that integrates with Odoo purchase module. The module will provide
functionality for requesting purchase orders and approving them before purchase orders are created.
Task Details
Purchase Request module
1- Create New model “purchase request”.
2- Add new menu “Purchase Requests” to purchase module.
3- purchase request form will include:
• Field state containing two states draft and confirmed.
• Field relation with analytical account model.
• Field creation date. (Automatically set and read only can’t be modified in any sate)
• Field created by.(Automatically set and read only can’t be modified in any state)
• Requested by ( field related to the users model “Should be the user creating the record and
can be modified manually to select another user”)
• requested on (Date field user should select it manually and having default value of the
creation date).
• Field One2many Purchase Request Lines.
4- user should be able to add multiple lines to purchase request, each line contains the following
fields:
• Field relation with product model.
• Field “vendor” relation with res partner model.
• Field float Quantity.
• Field relation with uom.uom model with domain from the product defined uom. (see
purchase order line model)
5- On confirming the purchase request the system should loop on the Purchase Request lines and
group lines by vendor then create an RFQ (draft purchase order) for each group of lines related to
the same vendor.
6- After confirmation, all fields in the purchase request, including the lines, should be read-only.
7- for each purchase order should be a smart tab for the purchase request related to it.
8- in the purchase request smart tab for the purchase orders created from it.
