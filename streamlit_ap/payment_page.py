import streamlit as st
import requests

# Title of the app
st.title("URL and Amount Input App")

# Input fields
receiver_url = st.text_input("Enter a receiver wallet URL:")
sender_url = st.text_input("Enter a sender wallet URL:")
amount = st.number_input("Enter an amount:", min_value=0.0, step=0.01)

# Display the inputs
st.write("Receiver URL entered:", receiver_url)
st.write("Sender URL entered:", sender_url)
st.write("Amount entered:", amount)

# Server URL where the Node.js server is running
server_url = "http://localhost:3000/create-payment"  # Change if your Node.js server is on a different URL or port
server_complete_payment = "http://localhost:3000/finish-payment"

import requests
import streamlit as st

# Initialize session state variables if not already set
if 'quote' not in st.session_state:
    st.session_state.quote = ""
if 'cont_uri' not in st.session_state:
    st.session_state.cont_uri = ""
if 'cont_token' not in st.session_state:
    st.session_state.cont_token = ""

# URL of the server endpoint
server_url = "http://localhost:3000/create-payment"
finish_url = "http://localhost:3000/finish-payment"  # Endpoint for finishing the payment

# Button to trigger the payment
if st.button('Create Payment'):
    if receiver_url and sender_url and amount > 0:
        # Create the data payload to send to the server
        payload = {
            "sender_url": sender_url,
            "receiver_url": receiver_url,
            "amount": amount
        }

        # Send a POST request to the server
        try:
            response = requests.post(server_url, json=payload)
            if response.status_code == 200:
                st.success("Payment request successful! Please check the redirect URL to proceed.")
                response_data = response.json()
                st.session_state.quote = response_data['response']['QUOTE_ID']
                st.session_state.cont_uri = response_data['response']['CONTINUE_URI']
                st.session_state.cont_token = response_data['response']['CONTINUE_ACCESS_TOKEN']

                st.write("QUOTE_ID:", st.session_state.quote)
                st.write("CONTINUE_URI:", st.session_state.cont_uri)
                st.write("CONTINUE_ACCESS_TOKEN:", st.session_state.cont_token)
                st.write("INTERACT_REDIRECT_URL:", response_data['response']['INTERACT_REDIRECT_URL'])
            else:
                st.error(f"Payment request failed with status code: {response.status_code}")
                st.write(response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with the server: {e}")

# Button to finalize the payment
if st.button('Finalize and create all Payments'):
    if st.session_state.quote and st.session_state.cont_uri and st.session_state.cont_token and sender_url:
        completion_payload = {
            "quoteId": st.session_state.quote,
            "continueUri": st.session_state.cont_uri,
            "continueAccessToken": st.session_state.cont_token,
            "sendingWalletAddressUrl": sender_url
        }

        # Send a POST request to finish the payment
        try:
            response = requests.post(finish_url, json=completion_payload)
            if response.status_code == 200:
                st.success("Payment finalized successfully!")
                st.write(response.json())
            else:
                st.error(f"Payment finalization failed with status code: {response.status_code}")
                st.write(response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with the server: {e}")
    else:
        st.error("Payment details are missing or incomplete.")
