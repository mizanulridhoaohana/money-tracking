import streamlit as st
from riwayat_pengeluaran import RiwayatPengeluaran
from catat_pengeluaran import CatatPengeluaran
from auth import Auth

auth = Auth()

def main():
    st.title('Aplikasi Pengeluaran Uang')

    # Initialize session state
    if 'email' not in st.session_state:
        st.session_state.email = None

    if 'mode' not in st.session_state:
        st.session_state.mode = 'login'

    query_params = st.query_params  # Use query_params to get current state

    if st.session_state.email is None:
        if query_params.get('mode') == 'create_account':
            st.session_state.mode = 'create_account'
            create_account()  # Ensure function is called
        elif st.session_state.mode == 'login':
            login()
        elif st.session_state.mode == 'logged_in':
            app()
    else:
        app()

def login():
    st.subheader('Login')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        result = auth.login(email, password)
        if result == "Login successful.":
            st.session_state.email = email
            st.session_state.mode = 'logged_in'
            st.query_params.update({'mode': 'logged_in'})  # Update query parameters
            st.experimental_rerun()  # Force rerun to reflect changes
        else:
            st.error(result)

    if st.button('Belum memiliki akun?'):
        st.session_state.mode = 'create_account'
        st.query_params.update({'mode': 'create_account'})  # Update query parameters
        st.experimental_rerun()  # Force rerun to show create_account form

def create_account():
    st.subheader('Create Account')
    new_email = st.text_input('New Email')
    new_password = st.text_input('New Password', type='password')
    new_password_confirm = st.text_input('Confirm New Password', type='password')

    if st.button('Create Account'):
        result = auth.create_account(new_email, new_password, new_password_confirm)
        if result == "Account created successfully.":
            st.success(result)
            st.session_state.mode = 'login'
            st.query_params.update({'mode': 'login'})  # Update query parameters
            st.experimental_rerun()  # Force rerun to go back to login
        else:
            st.error(result)

    if st.button('Back to Login'):
        st.session_state.mode = 'login'
        st.query_params.update({'mode': 'login'})  # Update query parameters
        st.experimental_rerun()  # Force rerun to go back to login

def app():
    st.sidebar.subheader('Menu')
    menu = st.sidebar.selectbox('Menu', ['Lihat Riwayat Pengeluaran', 'Catat Pengeluaran', 'Logout'])

    if menu == 'Lihat Riwayat Pengeluaran':
        RiwayatPengeluaran(st.session_state.email).show()
    elif menu == 'Catat Pengeluaran':
        CatatPengeluaran(st.session_state.email).show()
    elif menu == 'Logout':
        st.session_state.email = None
        st.session_state.mode = 'login'
        st.query_params.update({'mode': 'login'})  # Update query parameters
        st.experimental_rerun()  # Force rerun to go back to login

if __name__ == '__main__':
    main()
