# 1. What is a “Smart Button” in Odoo?
#  A. A button that opens an external website
#  B. A button that prints reports only
#  C. A quick-access button in the form header that opens related records
#  D. A special button used in the backend only for developers

# Correct Answers:
# 1. C. A quick-access button in the form header that opens related records

# 2.You only want to show a smart button when the sale order is in the “approved” state. What is the correct XML syntax?
# A.<button t-if="state == 'approved'" name="..." ... />
# B.<button attrs="{'invisible': [('state', '!=', 'approved')]}" name="..." ... />
# C. <field invisible="state != 'approved'" name="..." />
# D.<button visible="state == 'approved'" name="..." ... />

#Correct Answers: D.<button visible="state == 'approved'" name="..." ... />

# 3.You want to show a smart button that links to invoices related to a sale order. What is the key requirement in the backend?
# A. Add a method returning action_invoice_tree with filtered invoices
#  B. Set button type to print
#  C. Set target="new"
#  D. Use action_view_invoice_form from account.move.line

# Correct Answers:
# 3. A. Add a method returning action_invoice_tree with filtered invoices

# 4. In QWeb, which operator is used to check if a field is truthy (exists and not empty)?
#  A. == True
#  B. != None
#  C. is True
#  D. Just the field name: t-if="doc.field_name"
 
# Correct Answers: A. == True



