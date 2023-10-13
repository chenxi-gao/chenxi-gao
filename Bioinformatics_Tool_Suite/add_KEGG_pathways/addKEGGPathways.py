#!/usr/bin/env python
# addKEGGPathways.py

"""
Append the KEGG Ortholog ID, KEGG Pathway ID, and KEGG Pathway Description for each of the SwissProt (Uniprot) IDs.
Filter to only BLAST output where evalue < 1e-50.

Usage:
$python3 addKEGGPathways.py --input alignPredicted.txt --evalue 1e-50 --output alignPredicted_addKEGGPathways.txt
"""

import argparse
import requests


def main():
    """Main function to execute the script logic."""
    # Parse command-line arguments
    args = get_args()

    # Get the input file handle
    filename = args.infile
    fh_in = get_filehandle(filename, "r")

    # Get the output file handle
    outfile = args.outfile
    fh_out = get_filehandle(outfile, "a")

    # Add the KEGG pathways and descriptions to the input file and write it to the output file
    addKEGGPathways(fh_in, fh_out)

    # Close the file handles
    fh_in.close()
    fh_out.close()


def get_args():
    """Return parsed command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Append KEGG Pathway information to BLAST output",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--input',
                        dest='infile',
                        help='Specify the input filename',
                        type=str,
                        default='alignPredicted.txt',
                        required=False
                        )

    parser.add_argument('-e', '--evalue',
                        dest='threshold',
                        help='Specify the e-value threshold',
                        type=str,
                        default=1e-50,
                        required=False
                        )
    parser.add_argument('-o', '--output',
                        dest='outfile',
                        help='Specify the output filename',
                        type=str,
                        default='alignPredicted_addKEGGPathways.txt',
                        required=False
                        )

    return(parser.parse_args())


def get_filehandle(filename, mode):
    """
    Open and return a file handle.
    
    Parameters:
        filename (str): The name of the file to open.
        mode (str): The mode in which to open the file ('r' for read, 'a' for append, etc.)

    Returns:
        filehandle: The file handle for the opened file.
    """
    try:
        filehandle = open(filename, mode)
    except OSError as err:
        print('OSError: Cannot open file. Please check the file format.')
        raise err
    except ValueError as err:
        print('ValueError: File does not exist for opening, or wrong open mode specified.')
        raise err
    else:
        return filehandle


def getUniProtFromBlast(blast_line, threshold):
    """
    Extract and return the UniProt ID from a line of BLAST output if the e-value is below a threshold.
    
    Parameters:
        blast_line (str): A line of BLAST output.
        threshold (float): The e-value threshold.
        
    Returns:
        str or False: The UniProt ID if the e-value is below the threshold, otherwise False.
    """
    cleaned_line = blast_line.strip()
    blast_fields = cleaned_line.split("\t")
    
    # Ensure there are enough fields to prevent IndexError
    if len(blast_fields) >= 8:
        try:
            if float(blast_fields[7]) < float(threshold):
                uniprot_field = blast_fields[1]
                uniprot_id = uniprot_field.split("|")[1]
                return uniprot_id
        except ValueError:  # Handle cases where conversion to float is not possible
            print(f"Warning: Unable to convert {blast_fields[7]} to float.")
            return False
    else:
        print(f"Warning: Expected at least 8 fields, but got {len(blast_fields)}")
        return False


def getKeggGenes(UniProt_ID):
    """
    Retrieve and return KEGG ID(s) corresponding to a given UniProt ID.

    Parameters:
        UniProt_ID (str): The UniProt ID for which to find corresponding KEGG ID(s).

    Returns:
        list or None: A list of KEGG ID(s) if found, otherwise None.
    """
    KEGGID = []
    # Request conversion from UniProt ID to KEGG ID via KEGG API
    result = requests.get(f'https://rest.kegg.jp/conv/genes/uniprot:{UniProt_ID}')
    if result.status_code == 200:  # Check for successful HTTP response
        for entry in result.iter_lines():
            str_entry = entry.decode(result.encoding)  # Convert from binary to text
            fields = str_entry.split("\t")
            try:
                if fields[1]:
                    KEGGID.append(fields[1])
                    return KEGGID  # Return KEGGID as soon as it is found
            except IndexError:
                continue
    else:
        print(f"Warning: Unable to retrieve data for UniProt_ID {UniProt_ID}. HTTP status code: {result.status_code}")
        return None


def getKeggOrthology(KEGG_ID):
    """
    Retrieve and return KEGG Orthology ID(s) corresponding to a given KEGG gene ID.

    Parameters:
        KEGG_ID (str): The KEGG gene ID for which to find corresponding Orthology ID(s).

    Returns:
        list: A list of KEGG Orthology ID(s).
    """
    KeggOrthologyID = []
    # Request links from gene to KO (KEGG Orthology)
    result = requests.get(f'https://rest.kegg.jp/link/ko/{KEGG_ID}')
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)  # Convert from binary to text
        fields = str_entry.split("\t")
        try:
            if fields[1]:
                KeggOrthologyID.append(fields[1])
        except IndexError:
            continue
    return KeggOrthologyID


def getKeggPathIDs(KEGG_Orthology_ID):
    """
    Retrieve and return KEGG Pathway ID(s) corresponding to a given KEGG Orthology ID.

    Parameters:
        KEGG_Orthology_ID (str): The KEGG Orthology ID for which to find corresponding Pathway ID(s).

    Returns:
        list: A list of KEGG Pathway ID(s).
    """
    KeggPathIDs = []
    # Request links from KO (KEGG Orthology) to pathways
    result = requests.get(f'https://rest.kegg.jp/link/pathway/{KEGG_Orthology_ID}')
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)  # Convert from binary to text
        fields = str_entry.split("\t")
        try:
            if fields[1]:
                KeggPathIDs.append(fields[1])
        except IndexError:
            continue
    return KeggPathIDs


def loadKeggPathways():
    """
    Retrieve and return a dictionary mapping KEGG Pathway IDs to their descriptions.

    Returns:
        dict: A dictionary where the keys are KEGG Pathway IDs and the values are pathway names/descriptions.
    """
    keggPathways = {}
    # Request list of KEGG pathways for KEGG Orthology (KO)
    result = requests.get('https://rest.kegg.jp/list/pathway/ko')
    if result.status_code == 200:
        for entry in result.iter_lines():
            str_entry = entry.decode(result.encoding)  # Convert from binary to text
            fields = str_entry.split("\t")
            if len(fields) >= 2:  # Ensure there are enough fields
                keggPathways[fields[0].split(":")[1]] = fields[1]  # Use part after 'path:' as key
            else:
                print(f"Warning: unexpected format: {str_entry}")
    else:
        print(f"Failed to retrieve data: {result.status_code}")
    return keggPathways


def addKEGGPathways(fh_in, fh_out):
    """
    Append KEGG Ortholog ID, Pathway ID, and Pathway Description for each SwissProt (Uniprot) ID.
    
    For each line in the input file, retrieve KEGG information, append it to the line, 
    and write the extended line to the output file.

    Parameters:
        fh_in (file handle): The input file handle.
        fh_out (file handle): The output file handle.
    """
    # Load KEGG pathways into a dictionary for later lookup
    keggPathways = loadKeggPathways()
    threshold = '1e-50'  # Threshold for filtering BLAST output by e-value
    
    # Iterate through each line in the input file
    for line in fh_in:
        # Extract UniProt ID if e-value is below threshold
        if getUniProtFromBlast(line, threshold):
            Prot_ID = getUniProtFromBlast(line, threshold)
            
            # Retrieve KEGG gene data for the UniProt ID
            KEGG_data = getKeggGenes(Prot_ID)
            if KEGG_data is not None:
                KEGG_ID = KEGG_data[0]
            else:
                print(f"Warning: No KEGG data found for Prot_ID {Prot_ID}")
                continue
            
            # Retrieve KEGG Orthology ID for the KEGG gene ID
            KEGG_Orthology_ID = getKeggOrthology(KEGG_ID)[0]
            
            # Retrieve KEGG Pathway IDs for the KEGG Orthology ID
            KeggPath_IDs = getKeggPathIDs(KEGG_Orthology_ID)
            ko_KeggPath_IDs = []
            
            # Filter for pathway IDs with 'ko'
            for KeggPath_ID in KeggPath_IDs:
                if 'ko' in KeggPath_ID:
                    ko_KeggPath_IDs.append(KeggPath_ID.split(":")[1])  # Store only the ID part, not the 'ko' prefix
                    
            try:
                # Append KEGG data to line and write to output file
                for ko_KeggPath_ID in ko_KeggPath_IDs:
                    if ko_KeggPath_ID in keggPathways:
                        Description = keggPathways[ko_KeggPath_ID]
                        fh_out.write(f"{line.strip()}\t{KEGG_Orthology_ID}\t{ko_KeggPath_ID}\t{Description}\n")
                    else:
                        print(f"Warning: {ko_KeggPath_ID} not found in keggPathways")
            except TypeError:
                continue
        else:
            continue


if __name__ == "__main__":
    main()

