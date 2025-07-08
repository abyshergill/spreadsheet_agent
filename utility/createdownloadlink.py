import io
import pandas as pd
import streamlit as st

def CreateDownloadLink(df: pd.DataFrame, filename: str, file_format: str = 'excel'):
    """Create download link for processed data"""
    if file_format == 'excel':
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        buffer.seek(0)
        return st.download_button(
            label="📥 Download Excel File",
            data=buffer,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return st.download_button(
            label="📥 Download CSV File",
            data=csv_buffer.getvalue(),
            file_name=filename,
            mime="text/csv"
        )