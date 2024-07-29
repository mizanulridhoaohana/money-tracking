import streamlit as st
from auth import Auth
from riwayat_pengeluaran import RiwayatPengeluaran
from catat_pengeluaran import CatatPengeluaran

auth = Auth()

def main():
    st.title('Aplikasi Pengeluaran Uang')

    # Initialize session state
    if 'email' not in st.session_state:
        st.session_state.email = None

    if 'mode' not in st.session_state:
        st.session_state.mode = 'login'

    if st.session_state.email is None:
        if st.session_state.mode == 'create_account':
            create_account()
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
        else:
            st.error(result)

    if st.button('Belum memiliki akun?'):
        st.session_state.mode = 'create_account'

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
        else:
            st.error(result)

    if st.button('Back to Login'):
        st.session_state.mode = 'login'

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

if __name__ == '__main__':
    main()
