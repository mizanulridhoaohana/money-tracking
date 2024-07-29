import streamlit as st
import json
import os

class RiwayatPengeluaran:
    def __init__(self, email):
        self.email = email
        self.json_file = f'{email}_expenses.json'

    def load_data(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []
        return data

    def format_number(self, number):
        return f"{number:,}".replace(',', '.')

    def show(self):
        st.header('Riwayat Pengeluaran')
        data = self.load_data()
        
        if data:
            for entry in data:
                st.subheader(f"Tanggal: {entry['date']}")
                
                st.write("Sumber Keuangan:")
                sources_df = {
                    'Sumber Keuangan': [source['source'] for source in entry['sources']],
                    'Jumlah (IDR)': [self.format_number(source['amount']) for source in entry['sources']]
                }
                st.table(sources_df)

                st.write("Pengeluaran:")
                expenses_df = {
                    'Nama Barang': [expense['item'] for expense in entry['expenses']],
                    'Nominal Pengeluaran (IDR)': [self.format_number(expense['amount']) for expense in entry['expenses']]
                }
                st.table(expenses_df)
                
                st.write("Ringkasan:")
                summary_df = {
                    'Deskripsi': ['Total Pemasukan', 'Total Pengeluaran', 'Sisa Uang'],
                    'Jumlah (IDR)': [
                        self.format_number(sum(source['amount'] for source in entry['sources'])),
                        self.format_number(entry['total']),
                        self.format_number(sum(source['amount'] for source in entry['sources']) - entry['total'])
                    ]
                }
                st.table(summary_df)

                st.write('---')
        else:
            st.write('Belum ada data pengeluaran.')
