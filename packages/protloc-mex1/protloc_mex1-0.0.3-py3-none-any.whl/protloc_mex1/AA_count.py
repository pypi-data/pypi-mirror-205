






from Bio.SeqUtils.ProtParam import ProteinAnalysis

import numpy as np

import re



def protein_sequence_conduct(file_data, sequence_name="Sequence"):
    """
    Conduct protein sequence analysis and add relevant protein properties to an input pandas dataframe.

    Parameters
    ----------
        file_data : pd.DataFrame 
            Input pandas dataframe containing protein sequences.
        sequence_name : str 
            Column name of the protein sequences in the input dataframe (default is "Sequence").

    Returns:
    ----------
        pd.DataFrame: Output pandas dataframe with added protein properties columns.

    Raises:
    ----------
        ValueError: If the index of the input dataframe contains duplicates.

    Example:
    ----------
        >>> import pandas as pd
        >>> from protloc_mex1.AA_count import protein_sequence_conduct
        >>> df = pd.DataFrame({'Sequence': ['KKSAAEKKKKKKKKAH', 'AKDFLIEAELKDSFF']})
        >>> output_df = protein_sequence_conduct(df,sequence_name="Sequence")

    Notes:
    ----------
        This function utilizes the ProteinAnalysis function from the Bio.SeqUtils.ProtParam module in the Biopython
        package. The input dataframe should contain a column with protein sequences. The function will add columns with
        protein properties including amino acid frequencies, elemental properties, molecular weight, aromaticity,
        instability index, flexibility, isoelectric point, secondary structure fraction, molar extinction coefficient
        for reduced cysteines and disulfid bridges, gravy, and a boolean column indicating if the sequence contains
        only standard amino acids.
    """

    # Define a function to check if the sequence contains rare amino acids or unknown amino acids.
    # O stands for pyrrolysine, Pyl; U stands for selenocysteine, Sec.
    # def special_match(strg):
    #     pattern = re.compile(r'[U|X|O|Z]+')
    #     return not bool(pattern.findall(strg))
    
    if file_data.index.duplicated().sum() > 0:
        raise ValueError("Index contains duplicates")

    # Create columns for the 20 amino acids
    AA_columns = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
    # Create columns for elemental properties
    element_count = ["Oxygen","Sulfur","Carbon","Hydrogen","Nitrogen","Acid","Basic","Polar","Non_Polar"]
    # Create columns for protein properties
    protein_features = AA_columns + element_count + ["molecular_weight","aromaticity","instability_index",
                                                    "flexibility_mean","flexibility_max","flexibility_min",
                                                    "isoelectric_point"] + \
                        ["gravy", #"protein_scale",
                         "secondary_structure_fraction_a","secondary_structure_fraction_b1",
                         "secondary_structure_fraction_b2","molar_extinction_coefficient_reduced_cysteines",
                         "molar_extinction_coefficient_disulfid_bridges"] + ["normal_sequence"]
    
    # Define a function to determine if it contains only 20 standard amino acids and no other characters
    def special_match(strg):
        pattern = re.compile(r'[^' + ''.join(AA_columns) + ']')
        return not bool(pattern.search(strg))

    # Get the column names to be added
    new_columns = list(set(protein_features) - set(file_data.columns))
    new_columns = [col for col in protein_features if col in new_columns]

    # Add feature columns based on added column name
    if new_columns:
        file_data = file_data.reindex(columns=list(file_data.columns) + new_columns)

    
    # Determine if the sequence contains rare amino acids or unknown amino acids
    for i in file_data.index:
        file_data.loc[i, "normal_sequence"] = special_match(file_data.loc[i, sequence_name])
    
    

      
    for i in file_data.index:
        Seq_count = ProteinAnalysis(file_data.loc[i, sequence_name])
        # calculate frequency of 20 amino acids
        AA_conduct_output = Seq_count.get_amino_acids_percent()

        for AA_conduct in AA_columns:
            file_data.loc[i, AA_conduct] = AA_conduct_output[AA_conduct]
        if file_data.loc[i, "normal_sequence"]:
            # calculate molecular weight
            file_data.loc[i, "molecular_weight"] = Seq_count.molecular_weight()
            # calculate aromaticity
            file_data.loc[i, "aromaticity"] = Seq_count.aromaticity()
            # calculate isoelectric point
            file_data.loc[i, "isoelectric_point"] = Seq_count.isoelectric_point()
            # calculate secondary structure fraction
            file_data.loc[i, "secondary_structure_fraction_a"] = Seq_count.secondary_structure_fraction()[0]
            file_data.loc[i, "secondary_structure_fraction_b1"] = Seq_count.secondary_structure_fraction()[1]
            file_data.loc[i, "secondary_structure_fraction_b2"] = Seq_count.secondary_structure_fraction()[2]
            # calculate molar extinction coefficient for reduced cysteines and disulfid bridges
            file_data.loc[i, "molar_extinction_coefficient_reduced_cysteines"] = Seq_count.molar_extinction_coefficient()[0]
            file_data.loc[i, "molar_extinction_coefficient_disulfid_bridges"] = Seq_count.molar_extinction_coefficient()[1]
            # calculate instability index
            file_data.loc[i, "instability_index"] = Seq_count.instability_index()
            # calculate flexibility (mean, min, max)
            flexibility_vals = Seq_count.flexibility()
            if len(flexibility_vals) > 0:
                file_data.loc[i, "flexibility_mean"] = np.mean(flexibility_vals)
                file_data.loc[i, "flexibility_min"] = np.min(flexibility_vals)
                file_data.loc[i, "flexibility_max"] = np.max(flexibility_vals)
            else:
                file_data.loc[i, "flexibility_mean"] = np.nan
                file_data.loc[i, "flexibility_min"] = np.nan
                file_data.loc[i, "flexibility_max"] = np.nan
            
            # calculate gravy
            file_data.loc[i, "gravy"] = Seq_count.gravy(scale='KyteDoolitle')
            # calculate protein scale
            # file_data.loc[i, "protein_scale"] = Seq_count.protein_scale(edge=1.0,)



        

    ## Calculate amino acid elemental composition
    for i in file_data.index:
        ##计算Oxygen
        file_data.loc[i, "Oxygen"]=(file_data.loc[i, sequence_name].count("Y")+file_data.loc[i, sequence_name].count("S")+\
        file_data.loc[i, sequence_name].count("T")+file_data.loc[i, sequence_name].count("N")+\
        file_data.loc[i, sequence_name].count("Q")+2*file_data.loc[i, sequence_name].count("D")+\
        2*file_data.loc[i, sequence_name].count("E"))/len(file_data.loc[i, sequence_name])
        ##Calculate Sulfur
        file_data.loc[i,"Sulfur"]=(file_data.loc[i, sequence_name].count("M")+file_data.loc[i, sequence_name].count("C"))/len(file_data.loc[i, sequence_name])
        ##Calculate Carbon
        file_data.loc[i,"Carbon"]=(file_data.loc[i, sequence_name].count("A")+\
                              3*file_data.loc[i, sequence_name].count("V")+4*file_data.loc[i, sequence_name].count("L")+\
                              4*file_data.loc[i, sequence_name].count("I")+3*file_data.loc[i, sequence_name].count("M")+\
                              7*file_data.loc[i, sequence_name].count("F")+7*file_data.loc[i, sequence_name].count("Y")+\
                              9*file_data.loc[i, sequence_name].count("W")+\
                              file_data.loc[i, sequence_name].count("S")+3*file_data.loc[i, sequence_name].count("P")+\
                              2*file_data.loc[i, sequence_name].count("T")+file_data.loc[i, sequence_name].count("C")+\
                              2*file_data.loc[i, sequence_name].count("N")+3*file_data.loc[i, sequence_name].count("Q")+\
                              4*file_data.loc[i, sequence_name].count("K")+4*file_data.loc[i, sequence_name].count("H")+\
                              4*file_data.loc[i, sequence_name].count("R")+2*file_data.loc[i, sequence_name].count("D")+\
                              3*file_data.loc[i, sequence_name].count("E"))/len(file_data.loc[i, sequence_name])
        ##Calculate Hydrogen
        file_data.loc[i,"Hydrogen"]=(file_data.loc[i, sequence_name].count("G")+3*file_data.loc[i, sequence_name].count("A")+\
                              7*file_data.loc[i, sequence_name].count("V")+9*file_data.loc[i, sequence_name].count("L")+\
                              9*file_data.loc[i, sequence_name].count("I")+7*file_data.loc[i, sequence_name].count("M")+\
                              7*file_data.loc[i, sequence_name].count("F")+7*file_data.loc[i, sequence_name].count("Y")+\
                              8*file_data.loc[i, sequence_name].count("W")+\
                              3*file_data.loc[i, sequence_name].count("S")+6*file_data.loc[i, sequence_name].count("P")+\
                              5*file_data.loc[i, sequence_name].count("T")+3*file_data.loc[i, sequence_name].count("C")+\
                              4*file_data.loc[i, sequence_name].count("N")+6*file_data.loc[i, sequence_name].count("Q")+\
                              11*file_data.loc[i, sequence_name].count("K")+6*file_data.loc[i, sequence_name].count("H")+\
                              11*file_data.loc[i, sequence_name].count("R")+2*file_data.loc[i, sequence_name].count("D")+\
                              4*file_data.loc[i, sequence_name].count("E"))/len(file_data.loc[i, sequence_name])
        ##Calculate Nitrogen
        file_data.loc[i,"Nitrogen"]=(file_data.loc[i, sequence_name].count("K")+3*file_data.loc[i, sequence_name].count("R")+\
        2*file_data.loc[i, sequence_name].count("H")+file_data.loc[i, sequence_name].count("W")+\
        file_data.loc[i, sequence_name].count("N")+file_data.loc[i, sequence_name].count("Q"))/len(file_data.loc[i, sequence_name])
        ##Calculate Acid
        file_data.loc[i,"Acid"]=(file_data.loc[i, sequence_name].count("D")+file_data.loc[i, sequence_name].count("E"))/len(file_data.loc[i, sequence_name])
        ##Calculate Basic
        file_data.loc[i,"Basic"]=(file_data.loc[i, sequence_name].count("H")+file_data.loc[i, sequence_name].count("R")+\
                                file_data.loc[i, sequence_name].count("K"))/len(file_data.loc[i, sequence_name])
        ##Calculate Polar
        file_data.loc[i,"Polar"]=(file_data.loc[i, sequence_name].count("S")+file_data.loc[i, sequence_name].count("P")+\
                              file_data.loc[i, sequence_name].count("T")+file_data.loc[i, sequence_name].count("C")+\
                              file_data.loc[i, sequence_name].count("N")+file_data.loc[i, sequence_name].count("Q")+\
                              file_data.loc[i, sequence_name].count("K")+file_data.loc[i, sequence_name].count("H")+\
                              file_data.loc[i, sequence_name].count("R")+file_data.loc[i, sequence_name].count("D")+\
                              file_data.loc[i, sequence_name].count("E"))/len(file_data.loc[i, sequence_name])
        ##Calculate Non_Polar
        file_data.loc[i,"Non_Polar"]=(file_data.loc[i, sequence_name].count("G")+file_data.loc[i, sequence_name].count("A")+\
                              file_data.loc[i, sequence_name].count("V")+file_data.loc[i, sequence_name].count("L")+\
                              file_data.loc[i, sequence_name].count("I")+file_data.loc[i, sequence_name].count("M")+\
                              file_data.loc[i, sequence_name].count("F")+file_data.loc[i, sequence_name].count("Y")+\
                              file_data.loc[i, sequence_name].count("W"))/len(file_data.loc[i, sequence_name])
    return file_data
       