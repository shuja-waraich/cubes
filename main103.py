import streamlit as st
import pandas as pd
import openai
from io import StringIO

openai.api_key = st.secrets["OPENAI"]

def transform_csv(csv_data):
    prompt = f"""Here is a template dataset:
    Vendor*,Product*,Quantity*,CoverageStartDate*,CoverageEndDate*,OR,CoverageTermMonths*,UnitAmount*,AccountNumber,ContractDetails,InvoiceNumber,Department,Type,Payment,PONumber,Comments
    Crayons Software,Software Lic., Support and Training,1,5/1/2021,4/30/2022,,,$631,100.20,split between depts.,Bid & CC approval Yr. 3 of 3,,IT,Maintenance,PO,Purch req. 21002140,Year 2 of 3
    ePlus,Rubrik Backup and recovery Sol - Year 1 of 3,1,2/21/2020,2/20/2022,,,$434,941.44,620.17016.6113,CC Approval Yr. 1 of 3,Muliple,IT,Maintenance,PO,2020-1323,
    Tangent,Datacove,1,5/16/2020,5/16/2021,,12,707.00,,,SI102673,Other,,,,
    Tangent,Web Hawk,1,2/19/2020,2/19/2021,,12,1282.50,,,SI101913,Other,,,,
    Tangent,Web Hawk,1,2/19/2021,2/19/2022,,12,1282.50,,,SI101913,Other,Subscription,PO,356-2021,
    Tangent,Datacove,1,4/8/2021,4/8/2022,,12,777.70,,,,Other,Maintenance,ACH,200-2021
    
Here is the inputted dataset:
{csv_data}

make the inputted data follow the formating and header title of to template data very closely"""
    print(prompt)
    input_text = prompt

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=input_text,
        temperature=0.1,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0

    )

    transformed_data = response.choices[0].text.strip()
    print (response)
    return transformed_data

def main():
    st.title("CSV Transformation App")
    st.write("Upload a CSV file to transform it into the template format.")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.subheader("Uploaded Data")
        st.write(df)

        if st.button("Transform"):
            csv_data = df.to_csv(index=False)
            transformed_data = transform_csv(csv_data)
            transformed_df = pd.read_csv(StringIO(transformed_data))

            st.subheader("Transformed Data")
            st.write(transformed_df)

if __name__ == "__main__":
    main()
