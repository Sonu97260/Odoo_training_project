# Part 1 – Multiple Choice Questions 
# Which Odoo decorator is used to compute a field only when dependencies change?
# a) @api.onchange
# b) @api.depends
# c) @api.constrains
# d) @api.model

#answer: b) @api.depends

# In Odoo, ir.model.access.csv defines:
# a) Data records 
# b) Record rules
# c) Access control lists (ACLs)
# d) Scheduled actions

#answer: c) Access control lists (ACLs)

# Which field type is best suited to store a file in Odoo?
# a) Char
# b) Binary
# c) Text
# d) Selection

#answer: b) Binary

# The chatter functionality is enabled by inheriting which mixin?
# a) mail.thread
# b) mail.channel
# c) mail.activity
# d) mail.partnern

#answer: a) mail.thread


# Part 2 – Short Answer Questions 

# Explain the difference between related fields and computed fields in Odoo.

#answer: Related fields in Odoo are fields that directly reference another field in a related model,
# allowing you to access data from that model without duplicating it. 
# Computed fields, on the other hand, are fields whose values are calculated based on other fields or logic defined in the model.
# Computed fields can be dynamic and change based on the underlying data, 
# while related fields simply reflect the value of the referenced field.


# What is the role of Record Rules compared to Access Rights?
#answer: Access Rights in Odoo define the basic permissions (read, write, create, delete)
# that a user or group has on a model level, determining what actions they can perform on the records of that model.
# Record Rules, on the other hand, provide a more granular level
# of access control by defining conditions that restrict access to specific records within a model based on certain criteria.

# What is the return of some orm method add any 5 orm return.

#answer: 1. browse(): Returns a recordset of the records matching the given IDs.
#2. search(): Returns a recordset of records that match the search criteria.
#3. create(): Returns the newly created record as a recordset.
#4. write(): Returns a boolean indicating whether the write operation was successful.
#5. unlink(): Returns a boolean indicating whether the records were successfully deleted.

# Define the purpose of @api.onchange and give a practical example.

#answer: The @api.onchange decorator in Odoo is used to define methods that are triggered
# when a specific field's value changes in the user interface.
# This allows for dynamic updates to other fields based on user input without needing to save the record.
# Practical example: In a sales order form, when the user selects a different product in a line item,
# an @api.onchange method can automatically update the unit price and description fields based
# based on the selected product.

# Explain the difference between search and browse methods..
#answer: The search method in Odoo is used to find records that match specific criteria
# and returns a recordset of those records. It allows for filtering based on conditions.
# The browse method, on the other hand, is used to access records by their IDs.