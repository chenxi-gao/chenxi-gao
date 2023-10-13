#!/usr/bin/env python
# addKEGGPathways.py
"""
Append the KEGG Ortholog ID, KEGG Pathway ID, and KEGG Pathway Description for each of the SwissProt (Uniprot) IDs
Filter to only BLAST output where evalue < 1e-50

usage: $python3 addKEGGPathways.py --input alignPredicted.txt --evalue 1e-50 --output alignPredicted_addKEGGPathways.txt
"""

import argparse
import requests


def main():
    """ Business Logic """
    # get the infile
    args = get_args()
    filename = args.infile
    fh_in = get_filehandle(filename, "r")

    # get the outfile
    outfile = args.outfile
    fh_out = get_filehandle(outfile, "a")

    # add the KEGG pathways and descriptions to the input file and output it
    addKEGGPathways(fh_in, fh_out)

    # close the file
    fh_in.close()
    fh_out.close()


def get_args():
    """Return parsed command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Your script description (often top line of script's DocString; eg. Duplicate word n times)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--input',
                        dest='infile',
                        help='get the input filename',
                        type=str,
                        default='alignPredicted.txt',
                        required=False
                        )

    parser.add_argument('-e', '--evalue',
                        dest='threshold',
                        help='get the e-value threshold',
                        type=str,
                        default=1e-50,
                        required=False
                        )
    parser.add_argument('-o', '--output',
                        dest='outfile',
                        help='get the output filename',
                        type=str,
                        default='alignPredicted_addKEGGPathways.txt',
                        required=False
                        )

    return(parser.parse_args())


def get_filehandle(filename, mode):
    """
    To open the file name passed in or out, and passes back files object
    @param filenname: file to open
    @param mode: operation mode
    @return: the opened filehandle
    """
    try:
        filehandle = open(filename, mode)
    except OSError as err:
        print('OSError: the file cannot be opened, please check the format of the file')
        raise err
    except ValueError as err:
        print('ValueError: the file does not exist for opening, or the wrong open mode')
        raise err
    else:
        return filehandle


def getUniProtFromBlast(blast_line, threshold):
    """Return UniProt ID from the BLAST line if the evalue is below the threshold.

    Returns False if evalue is above threshold.
    """
    cleaned_line = blast_line.strip()
    blast_fields = cleaned_line.split("\t")
    
    # Check if blast_fields has enough elements before trying to access them
    if len(blast_fields) >= 8:
        try:
            if float(blast_fields[7]) < float(threshold):
                uniprot_field = blast_fields[1]
                # Split by the pipe "|" character and get the second element
                uniprot_id = uniprot_field.split("|")[1]
                return uniprot_id
        except ValueError:  # handle the case where conversion to float is not possible
            print(f"Warning: unable to convert {blast_fields[7]} to float.")
            return False
    else:
        print(f"Warning: expected at least 8 fields, but got {len(blast_fields)}")
        return False




def getKeggGenes(UniProt_ID):
    """Return a KEGG ID for a provided UniProtID."""
    KEGGID = []
    result = requests.get(f'https://rest.kegg.jp/conv/genes/uniprot:{UniProt_ID}')
    if result.status_code == 200:  # 检查HTTP响应码
        for entry in result.iter_lines():
            str_entry = entry.decode(result.encoding)  # convert from binary value to plain text
            fields = str_entry.split("\t")
            try:
                if fields[1]:
                    KEGGID.append(fields[1])
                    print(f"KEGGID:{KEGGID}")
                    return KEGGID
            except IndexError:
                continue
    else:
        print(f"Warning: Unable to retrieve data for UniProt_ID {UniProt_ID}. HTTP status code: {result.status_code}")
        return None


def getKeggOrthology(KEGG_ID):
    KeggOrthologyID = []
    result = requests.get(f'https://rest.kegg.jp/link/ko/{KEGG_ID}')
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)
        fields = str_entry.split("\t")
        try:
            if fields[1]:
                KeggOrthologyID.append(fields[1])
        except IndexError:
            continue
    print(f"KeggOrthologyID: {KeggOrthologyID}")  # 打印所有找到的ID
    return KeggOrthologyID



def getKeggPathIDs(KEGG_Orthology_ID):
    """Return a list of Kegg Path IDs for a provided Kegg Orthology ID."""
    KeggPathIDs = []
    result = requests.get(f'https://rest.kegg.jp/link/pathway/{KEGG_Orthology_ID}')
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)  # convert from binary value to plain text
        fields = str_entry.split("\t")
        try:
            if fields[1]:
                KeggPathIDs.append(fields[1])  # second field is the KeggPathIDs value
        except IndexError:
            continue
    return KeggPathIDs


def loadKeggPathways():
    keggPathways = {}
    result = requests.get('https://rest.kegg.jp/list/pathway/ko')
    if result.status_code == 200:
        for i, entry in enumerate(result.iter_lines()):
            str_entry = entry.decode(result.encoding)  # convert from binary value to plain text
            fields = str_entry.split("\t")
            print(f"Processing line {i}: {str_entry}")  # print the line being processed
            if len(fields) >= 2:
                keggPathways[fields[0]] = fields[1]
            else:
                print(f"Warning: unexpected format in line {i}: {str_entry}")
    else:
        print(f"Failed to retrieve data: {result.status_code}")
    return keggPathways

def addKEGGPathways(fh_in, fh_out):
    """Append the KEGG Ortholog ID, KEGG Pathway ID, and KEGG Pathway Description for each of the SwissProt (Uniprot) IDs"""
    keggPathways = loadKeggPathways()
    threshold = '1e-50'
    for line in fh_in:
        if getUniProtFromBlast(line, threshold):
            Prot_ID = getUniProtFromBlast(line, threshold)
            KEGG_data = getKeggGenes(Prot_ID)
            if KEGG_data is not None:  # 检查返回值是否为None
                KEGG_ID = KEGG_data[0]
            else:
                print(f"Warning: No KEGG data found for Prot_ID {Prot_ID}")
                continue  # 跳过这次循环的剩余部分
            KEGG_ID = getKeggGenes(Prot_ID)[0]
            KEGG_Orthology_ID = getKeggOrthology(KEGG_ID)[0]
            KeggPath_IDs = getKeggPathIDs(KEGG_Orthology_ID)
            ko_KeggPath_IDs = []
            for KeggPath_ID in KeggPath_IDs:
                if 'ko' in KeggPath_ID:
                    ko_KeggPath_IDs.append(KeggPath_ID.split(":")[1])
            try:
                for ko_KeggPath_ID in ko_KeggPath_IDs:
                    if ko_KeggPath_ID in keggPathways:
                        print(f"ko_path:{ko_KeggPath_ID}")
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
