#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 14:16:50 2023

@author: monicabomber
"""
import streamlit as st
import requests
import pandas as pd
import io
import gzip
from io import BytesIO
from io import StringIO

gene_list = st.file_uploader("Upload a tab delimited file of your selected gene list")
gene_id_name = st.text_area("How you are aligning the files, by gene_id", value="gene_id")
downloadpath = st.text_area("The filename to download the GTF file", value="download.gtf")

gtf_data = None

# Function to download GTF file from the selected URL
def download_gtf_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        if url.endswith(".gz"):
            with gzip.open(io.BytesIO(response.content), 'rt', encoding='utf-8') as file:
                gtf_data = file.read()
        else:
            gtf_data = response.text
        return gtf_data
    else:
        return None

# Dictionary mapping GTF versions to their respective URLs

gtf_urls = {
    "hg38": "https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fhgdownload.soe.ucsc.edu%2FgoldenPath%2Fhg38%2FbigZips%2Fgenes%2Fhg38.ncbiRefSeq.gtf.gz&data=05%7C02%7Cmonica.l.bomber%40vanderbilt.edu%7Cef56b00c4922499b719408dc177ccbc0%7Cba5a7f39e3be4ab3b45067fa80faecad%7C0%7C0%7C638411071955335445%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=4hLMpwj%2Fr0jHMw7eOKqC99MqlARWwrmHTakZOcJrkgA%3D&reserved=0",
    "hg19": "https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fhgdownload.soe.ucsc.edu%2FgoldenPath%2Fhg19%2FbigZips%2Fgenes%2Fhg19.ncbiRefSeq.gtf.gz&data=05%7C02%7Cmonica.l.bomber%40vanderbilt.edu%7Cef56b00c4922499b719408dc177ccbc0%7Cba5a7f39e3be4ab3b45067fa80faecad%7C0%7C0%7C638411071955344192%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=Dnenzxlj5ZUifvW3I3o49vQaBRQSdXUIDHqTm1GJGPQ%3D&reserved=0",
    "mm10": "https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fhgdownload.soe.ucsc.edu%2FgoldenPath%2Fmm10%2FbigZips%2Fgenes%2Fmm10.ncbiRefSeq.gtf.gz&data=05%7C02%7Cmonica.l.bomber%40vanderbilt.edu%7Cef56b00c4922499b719408dc177ccbc0%7Cba5a7f39e3be4ab3b45067fa80faecad%7C0%7C0%7C638411071955350420%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=x%2BrvMF9LlMqnwnXF%2FNCgSCJ7LE81V5RPPbhizHgINeo%3D&reserved=0",
    "mm39": "https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fhgdownload.soe.ucsc.edu%2FgoldenPath%2Fmm39%2FbigZips%2Fgenes%2Fmm39.ncbiRefSeq.gtf.gz&data=05%7C02%7Cmonica.l.bomber%40vanderbilt.edu%7Cef56b00c4922499b719408dc177ccbc0%7Cba5a7f39e3be4ab3b45067fa80faecad%7C0%7C0%7C638411071955355979%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=HJy6JH2PVMbzmb51n%2FWjx2H6RBWWjyJKz0PdLCUVo5E%3D&reserved=0"
}

# Create a dropdown to select the GTF version
selected_version = st.selectbox("Select GTF Version", list(gtf_urls.keys()))

# Display the selected version
st.write("You selected:", selected_version)

gtf_url = gtf_urls.get(selected_version)

if st.button("View GTF file"):
    gtf_df = pd.read_csv(StringIO(download_gtf_file(gtf_url)), sep='\t')
    if gtf_df is not None:
        st.write("First few rows of the GTF file:")
        st.write(gtf_df.head())
    else:
        st.write("Failed to download GTF file.")
if gtf_url:
    gtf_data = download_gtf_file(gtf_url)
    if gtf_data:
        # Display the first 1000 characters of the file as an example
        st.write("First 1000 characters of the GTF file:")
        st.text(gtf_data[:1000])
    else:
        st.write("Failed to download the GTF file. Please check the URL.")
else:
    st.write("Invalid GTF version selected.")

# Empty list
selected_genes = []

github_file_url = 'https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmonnieb92%2FselectGTFfile_streamlit%2Fmain%2Fselectgenelist.txt&data=05%7C02%7Cmonica.l.bomber%40vanderbilt.edu%7Cef56b00c4922499b719408dc177ccbc0%7Cba5a7f39e3be4ab3b45067fa80faecad%7C0%7C0%7C638411071955361047%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=PzLzT%2BFAulp0mlD7AvtzCrP4fkiW3I14A0tz%2BOuwNRE%3D&reserved=0'

# Split GTF data into lines if gtf_data is not None
if gtf_data:
    gtf_lines = gtf_data.splitlines()

    # Read gene IDs from the uploaded file
    if gene_list is not None:
        gene_list_df = pd.read_csv(StringIO(gene_list.getvalue()), sep='\t')
        gene_id_list = gene_list_df[gene_id_name].tolist()
    else:
        response = requests.get(github_file_url)
        gene_list_df = pd.read_csv(StringIO(response.text), sep='\t')
        gene_id_list = gene_list_df[gene_id_name].tolist()

    # Loop through the GTF data
    for line in gtf_lines:
        elements = line.split("\t")

        if len(elements) < 9:
            continue
        attributes = elements[8]
        if gene_id_name in attributes:
            gene_id = attributes.split(gene_id_name)[1].split('";')[0].strip(' "')
            if gene_id in gene_id_list:
                selected_genes.append(line)

st.write("Debug info:")
st.write(f"Length of selected_genes: {len(selected_genes)}")
st.write(f"First entry in selected_genes: {selected_genes[0] if selected_genes else 'No entries'}")

# Create a button for downloading the selected GTF
if st.button("Download Selected GTF"):
    with open(downloadpath, "w") as new_gtf_file:
        for entry in selected_genes:
            new_gtf_file.write(entry)
