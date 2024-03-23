import streamlit as st 
import pandas as pd
import botocore.exceptions
import boto3
import json
import time
from streamlit_extras.switch_page_button import switch_page

 

st.set_page_config(
    page_title="CLOUDTRAIL ANALYTICS",
    page_icon="📲", 
    initial_sidebar_state ="collapsed"
)
st.markdown("""
 
<style>
[data-testid="stSidebarNav"] {
visibility: hidden;
}
</style>""",unsafe_allow_html=True)

 
st.image('aws.png',width=166)
st.markdown("<h1 style='color:#ff9900;'>CLOUDTRAIL ANALYTICS</h1>", unsafe_allow_html=True)
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown("<h3 style='color:#242f3d;'>AWS CONNECTION</h3>", unsafe_allow_html=True)
st.image("CAS.gif", caption='')

st.markdown("<h3 style='color:#242f3d;'>AWS CONNECTION</h3>", unsafe_allow_html=True)


access_key=st.text_input('Access_key','AKIA3757D6ILCDUZGGLJ')
secret_key=st.text_input('Secret_key','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')
region_name=st.selectbox('Region_name', ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2'])

if access_key and secret_key and region_name:
    s3 = boto3.resource(
            service_name='s3',
            region_name=region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key  
        )  
    st.success("Successfully connected to AWS.")
   
    bucket_names = ['please select the Bucket']

    for bucket_name in s3.buckets.all():

        bucket_names.append(bucket_name.name)

    buckets = st.selectbox('Bucket Name', bucket_names)

    if buckets!='please select the Bucket':
        try:
            f_list=['please select the File']
            
            f_list = [obj.key for obj in s3.Bucket(buckets).objects.all()]
        
            files = st.selectbox('Select file', f_list)
            if files!= 'please select the File':
                obj = s3.Bucket(buckets).Object(files).get()
              
                file_type = files.split('.')[-1]
                if file_type == 'csv':
                    df = pd.read_csv(obj['Body'])
                elif file_type == 'xlsx':
                    df = pd.read_excel(obj['Body'])
                elif file_type == 'json':
                    df = pd.read_json(obj['Body'])
                else:
                    st.write('Unsupported file type.')
                    df = None
                if df is not None:
                    df.to_csv('Data.csv', index=False)
                    st.dataframe(df)
                # df = pd.read_csv(obj['Body']) 
                # df.to_csv('Data.csv', index=False)
                # st.dataframe(df)
            
                
            next_button = st.button('Next')
            if next_button:
                switch_page('Connect to Snowflake')
        except botocore.exceptions.NoCredentialsError:
         st.error("Please check your AWS credentials")

    else:
                st.error("Could not connect to AWS")
# st.markdown("""
 
# <style>
# [data-testid="stSidebarNav"] {
# visibility: hidden;
# }
# </style>""",unsafe_allow_html=True)






    
