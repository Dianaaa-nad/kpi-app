import mysql.connector
import streamlit as st

@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        database=st.secrets["mysql"]["database"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"]
    )

def fetch_cabang():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT branch_id, branch_name FROM branches ORDER BY branch_name")
    result = cursor.fetchall()
    cursor.close()
    return result

def fetch_kpi_variables():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT variable_id, var_code, variable_name, category_id, unit, type, weight FROM kpi_variables ORDER BY var_code")
    result = cursor.fetchall()
    cursor.close()
    return result

def fetch_key_result_categories():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT category_id, key_result_name FROM key_result_categories ORDER BY category_id")
    result = cursor.fetchall()
    cursor.close()
    return result

def fetch_kpi_detail():
    """Fetch KPI variables joined with their key result category, ordered by category then var_code."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            v.variable_id, v.var_code, v.variable_name,
            v.category_id, v.unit, v.type, v.weight,
            c.key_result_name
        FROM kpi_variables v
        JOIN key_result_categories c ON v.category_id = c.category_id
        ORDER BY c.category_id, v.var_code
    """)
    result = cursor.fetchall()
    cursor.close()
    return result