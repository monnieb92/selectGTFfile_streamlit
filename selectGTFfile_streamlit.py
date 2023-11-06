#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 14:16:50 2023

@author: monicabomber
"""
import streamlit as st
import requests
import pandas as pd
from io import StringIO
import gzip
from io import BytesIO

gene_list = st.file_uploader("Upload a tab delimited file of your selected gene list")
gene_id_name = st.text_area("How you are aligning the files, by gene_id", value="gene_id")
downloadpath = st.text_area("The filename to download the GTF file", value="download.gtf")

gtf_data = None

# Function to download GTF file from the selected URL
def download_gtf_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        if response.headers.get('content-encoding') == 'gzip':
            with gzip.GzipFile(fileobj=BytesIO(response.content)) as file:
                gtf_data = file.read().decode('utf-8')
                return gtf_data
        else: 
            return response.text        
    else:
        return None


# Dictionary mapping GTF versions to their respective URLs

gtf_urls = {
    "hg38": "https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/genes/hg38.ncbiRefSeq.gtf.gz",
    "hg19": "https://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/genes/hg19.ncbiRefSeq.gtf.gz",
    "mm10": "https://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/genes/mm10.ncbiRefSeq.gtf.gz",
    "mm39": "https://hgdownload.soe.ucsc.edu/goldenPath/mm39/bigZips/genes/mm39.ncbiRefSeq.gtf.gz"
}

# Create a dropdown to select the GTF version
selected_version = st.selectbox("Select GTF Version", list(gtf_urls.keys()))

# Display the selected version
st.write("You selected:", selected_version)

gtf_url = gtf_urls.get(selected_version)

if st.button("View GTF file"):
    gtf_df =download_gtf_file(gtf_url)
    if gtf_df is not None: 
        st.write("First few rows of the GTF file:")
        st.write(gtf_df.head())
    else: 
        st.write("Failed to download GTF file. FUCK.")
if gtf_url:
    gtf_data = download_gtf_file(gtf_url)
    if gtf_data:
        #Display the first 1000 characters of the file as an example
        st.write("First 1000 characters of the GTF file:")
        st.text(gtf_data[:1000])
    else:
        st.write("Failed to download the GTF file. Please check the URL.")
else:
    st.write("Invalid GTF version selected.")

# Empty list
selected_genes = []

github_file_url = 'https://raw.githubusercontent.com/monnieb92/selectGTFfile_streamlit/main/selectgenelist.txt'

# Split GTF data into lines if gtf_data is not None
if gtf_data:
    gtf_lines = gtf_data.splitlines()

    # Read gene IDs from the uploaded file
    if gene_list is not None:
        gene_list_df = pd.read_csv(gene_list, sep="\t")
        gene_id_list = gene_list_df[gene_id_name].tolist()
    else:
        response = requests.get(github_file_url)
        gene_list_df = pd.read_csv(StringIO(response.text), sep="\t")
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
st.write("Contents of Selected Genes GTF file")
if selected_genes:
    for entry in selected_genes:
        st.text(entry)

# Create a button for downloading the selected GTF
if st.button("Download Selected GTF"):
    with open(downloadpath, "w") as new_gtf_file:
        for entry in selected_genes:
            new_gtf_file.write(entry)
