import random
class MockGateway:
   """"
   create payment
   verify payment

   """

   def createPayment(self,amount,booking_id):
      # fake reference id
      reference = f"mock reference {booking_id}-{random.randint(1000,9999)}"

      # fake checkout url
      checkout_url = f"/mock-checkout?reference={reference}&amount={amount}"

      return {
         'success':True,
         'reference':reference,
         'checkout_url':checkout_url
      }
   
   
   def verifyPayment(self,reference_id):
      pass
