There is no built in requirements file yet

Python requirements:
- streamlit

Javascript requirements:
- express (is missing from the package.json file) - run npm install, then npm install express


Running the application

1. make sure you fill in the .env file with the required fields
2. make sure to generate/download a private key and move into in the request_redirect_test-main directory
3. run node step1-server.js to run the node server
4. create a new terminal - for python
5. CD into streamlit_ap
6. run front end py -m streamlit run payment_page.py
7. Make payments between accounts

flow:

1. enter payment details
2. click create payment
3. navigate to authenticate the payment
4. navigate back to front end to finalize the payment
5. refresh wallet tabs to see changes