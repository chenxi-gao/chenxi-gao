start_time <- Sys.time()
set.seed(123)

options(stringsAsFactors = FALSE)

suppressPackageStartupMessages({
  library(optparse)
  library(tidyverse)
  library(future.apply)
  library(Seurat)
  library(RColorBrewer)
  library(reshape2)
  library(network)
  library(igraph)
})

#' Parse Command-Line Options
#'
#' This function specifies the command-line options and parses them, returning the parsed options.
#'
#' @return (`opt`): The parsed command-line options.
parse_options <- function() {
  option_list = list(
    make_option(c("-i", "--matrix"), type="character", default="./test_dataset_60M/2021-03-25_matrix.csv",
                help="Input matrix"),
    make_option(c("-a", "--metadata"), type="character", default="./test_dataset_60M/2021-03-25_metadata.csv",
                help="Input metadata"),
    make_option(c("-p", "--lrpair"), type="character", default="./annotation/Ligand_receptor_pair_high_confident_2021vs1_clean.txt",
                help="Annotation for ligand-receptor pairs"),
    make_option(c("-s", "--corecomponents"), type="character", default="./annotation/Pathway_core_components_2021vs1_clean.txt",
                help="Annotation for core components"),
    make_option(c("-c", "--cores"), type="integer", default=8,
                help="Number of cores for parallel processing"),
    make_option(c("-o", "--output"), type="character", default="./output_test_dataset_60M",
                help="Output directory name")
  )
  
  opt_parser = OptionParser(option_list=option_list)
  opt = parse_args(opt_parser)
  
  # Check if files exist
  if (!file.exists(opt$matrix)) {
    stop("Input matrix file does not exist.")
  }
  if (!file.exists(opt$metadata)) {
    stop("Input metadata file does not exist.")
  }
  if (!file.exists(opt$lrpair)) {
    stop("Ligand-receptor pair annotation file does not exist.")
  }
  if (!file.exists(opt$corecomponents)) {
    stop("Core components annotation file does not exist.")
  }
  
  # Check if the number of cores is a positive integer
  if (opt$cores <= 0 || round(opt$cores) != opt$cores) {
    stop("Number of cores must be a positive integer.")
  }

  
  print(paste0("Expression matrix input: ", opt$matrix))
  print(paste0("Cell metadata input: ", opt$metadata))
  print(paste0("L-R pairs input: ", opt$lrpair))
  print(paste0("Core components input: ", opt$corecomponents))
  print(paste0("Number of cores for parallel processing: ", opt$cores))
  print(paste0("Output directory: ", opt$output))
  
  return(opt)
}


#' Prepare Environment for Analysis
#'
#' This function sets up the working environment by creating the necessary output directories and 
#' configuring parallel processing based on the number of available cores.
#'
#' @param output_dir Directory where the output files will be saved.
#' @param cores The number of cores to be used for parallel processing.
prepare_environment <- function(output_dir, cores) {
  # Check if the specified output directory exists; create it if it doesn't
  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }
  
  # Define the names of required subdirectories to be created within the output directory
  sub_dirs <- c("heatmap", "dotplot", "circleplot")
  
  # Loop through the list of subdirectories
  for (sub_dir in sub_dirs) {
    # Construct the full path of the subdirectory
    full_path <- file.path(output_dir, sub_dir)
    # Check if the subdirectory exists; create it if it doesn't
    if (!dir.exists(full_path)) {
      dir.create(full_path, recursive = TRUE)
    }
  }
  
  # Ensure 'cores' is a valid number and does not exceed the number of available cores
  # Use the max of 1 and min of detected cores and input cores to avoid invalid core counts
  cores <- max(1, min(parallel::detectCores(), as.numeric(cores)))
  
  # Set up the parallel processing plan
  # First, attempt to use the 'multiprocess' plan
  # If that fails, use the 'multisession' plan as a fallback
  tryCatch(
    {
      # Try setting up parallel processing using 'multiprocess' 
      plan(multiprocess, workers = cores)
    },
    error = function(e) {
      # If an error occurs, print an error message and switch to 'multisession'
      cat("Error with multiprocess. Trying multisession...\n")
      plan(multisession, workers = cores)
    }
  )
}


#' Process Single-Cell RNA-seq Data
#'
#' This function reads the single-cell RNA-seq matrix and metadata, processes them, 
#' and returns the processed expression matrix and cell information.
#'
#' @param matrix_path Path to the expression matrix csv file.
#' @param metadata_path Path to the metadata csv file.
#' @return A list contains: (`expr_matrix`) The processed expression matrix, (`cell_info`) All cell information.
process_scRNA_data <- function(matrix_path, metadata_path) {
  # Read the metadata csv file into a data frame
  # Convert the 'celltype' column to character data type using mutate
  cell_info <- read.csv(metadata_path, row.names = 1) %>%
    mutate(celltype = as.character(celltype))
  
  # Read the expression matrix csv file into a data frame
  # Disable column name conversion by setting check.names to FALSE
  expr_matrix <- read.csv(matrix_path, row.names = 1, check.names = FALSE)
  
  # Check if all cell names in cell_info are also present in the expression matrix columns
  # If not, stop the function and show an error message
  if(!all(row.names(cell_info) %in% colnames(expr_matrix))) {
    stop("Error: Mismatch between cell_info and expr_matrix columns!")
  }
  
  # Subset the expression matrix columns based on the cell names present in cell_info
  expr_matrix <- expr_matrix[, row.names(cell_info)]
  
  # Normalize the expression matrix values by dividing each value by the sum of its column
  # Then multiply by 10000 for TPM (Transcripts Per Million) conversion
  expr_matrix <- sweep(expr_matrix, 2, colSums(expr_matrix), FUN = "/") * 10000
  
  # Return a list containing the processed expression matrix and cell metadata
  return(list(expr_matrix = expr_matrix,
              cell_info = cell_info))
}


#' Process Ligand-Receptor Pairs
#'
#' This function reads a ligand-receptor pair file and filters it based on the genes present in the 
#' expression matrix. It returns the filtered ligand-receptor pair data.
#'
#' @param lrpair_path The path to the ligand-receptor pair file.
#' @param expr_matrix The expression matrix containing gene expressions.
#' @return (`df_lr_pairs`): The filtered ligand-receptor pair data.
process_lrpair <- function(lrpair_path, expr_matrix) {
  # Read the ligand-receptor pair file into a data frame
  # The file is expected to be tab-separated
  df_lr_pairs <- read.csv(file = lrpair_path, sep = "\t")
  
  # Extract all unique secreted and receptor genes from the ligand-receptor pair data frame
  gene_list <- unique(c(df_lr_pairs$Gene_secreted, df_lr_pairs$Gene_receptor))
  
  # Find the common genes that exist both in the ligand-receptor pair file and the expression matrix
  common_genes <- intersect(gene_list, row.names(expr_matrix))
  
  # Filter the ligand-receptor pair data frame to only include the common genes
  df_lr_pairs <- subset(df_lr_pairs, Gene_secreted %in% common_genes & Gene_receptor %in% common_genes)
  
  # Return the filtered ligand-receptor pair data frame
  return(df_lr_pairs)
}


#' Extract Target Gene Expression
#'
#' This function takes an expression matrix
#' And a vector of target genes of interest, such as `df_lr_pairs$Gene_secreted`.
#' It then extracts the expression data of these target genes from the matrix.
#'
#' @param expr_matrix The expression matrix where rows represent genes and columns represent cells.
#' @param gene_type A vector of unique target genes of interest.
#' @return (`df_extracted_target_expr`): A data frame containing the expression values of target genes.
extract_target_expr <- function(expr_matrix, gene_type) {
  # Transpose the expression matrix to have genes as columns and cells as rows
  expr_matrix <- t(expr_matrix)
  
  # Extract the expression data of the target genes from the transposed expression matrix
  # Subset the matrix based on the unique target genes provided in gene_type
  df_extracted_target_expr <- expr_matrix[ , unique(gene_type)]
  
  # Return the data frame containing the expression values of the target genes
  return(df_extracted_target_expr)
}


#' Count Average Gene Expression
#'
#' This function calculates the average expression of target genes for each cell type. It adds 
#' cell type information to the gene expression data, groups by cell type, and then calculates 
#' the mean expression for each gene.
#'
#' @param cell_info Data frame containing cell information such as cell type.
#' @param gene_matrix Data frame containing gene expression data.
#' @param gene_type List of target genes for which average expression is calculated.
#' @return (`df_avg_expr`): Data frame containing the average expression of each target gene for each cell type.
count_avg_expr <- function(cell_info, gene_matrix, gene_type) {
  # Check for necessary columns
  if (!"celltype" %in% names(cell_info)) {
    stop("The 'cell_info' data frame must contain a 'celltype' column.")
  }
  
  # Add cell type information to the gene expression data
  df_with_celltype <- cbind(cell_info[, c("celltype"), drop = FALSE], gene_matrix)
  
  # Group by cell type and calculate the mean expression for each gene
  df_group_by_celltype <- df_with_celltype %>%
    group_by(celltype) %>%
    summarise_all(mean) %>%
    as.data.frame()
  
  # Set the 'celltype' as row names for easier identification
  row.names(df_group_by_celltype) <- df_group_by_celltype$celltype
  
  # Remove the 'celltype' column as it's redundant now
  df_group_by_celltype$celltype <- NULL
  
  # Transpose the data frame to have genes as rows and cell types as columns
  df_group_by_celltype <- t(df_group_by_celltype)
  
  # Align the data with the list of target genes
  # Subset the transposed data frame to only include the target genes
  df_avg_expr <- df_group_by_celltype[gene_type, ] %>% as.data.frame()
  
  return(df_avg_expr)
}


#' Generate Column Name for Interaction
#'
#' This function generates a column name based on the interaction between two cell types.
#' The name is formed by concatenating the source cell type, the target cell type, and a suffix.
#'
#' @param celltype_i Source cell type in the interaction.
#' @param celltype_j Target cell type in the interaction.
#' @param suffix A string suffix to append at the end of the column name.
#' @return A string representing the generated column name.
generate_column_name <- function(celltype_i, celltype_j, suffix) {
  # Concatenate the source cell type, an arrow '>', the target cell type, and the suffix
  # to generate the column name
  paste0(celltype_i, ">", celltype_j, suffix)
}


#' Add Interaction Score and P-value Columns
#'
#' This function adds interaction score and p-value columns to a target data frame based on the information 
#' from a source data frame. 
#' The new columns are named based on the interaction between two cell types.
#'
#' @param df_target The target data frame where the new columns will be added.
#' @param df_source The source data frame containing the score and p-value columns.
#' @param celltype_i Source cell type in the interaction.
#' @param celltype_j Target cell type in the interaction.
#' @return (`df_target`): The target data frame with added interaction score and p-value columns.
add_score_and_pvalue <- function(df_target, df_source, celltype_i, celltype_j) {
  # Generate the column names for score and p-value using the generate_column_name function
  # The names are based on the interaction between celltype_i and celltype_j
  score_column <- generate_column_name(celltype_i, celltype_j, "_score")
  pvalue_column <- generate_column_name(celltype_i, celltype_j, "_pvalues")
  
  # Add the score and p-value columns to the target data frame
  # Columns are extracted from the source data frame based on the generated names
  df_target <- cbind(df_target, df_source[, c(score_column, pvalue_column)])
  
  # Return the updated target data frame with the new score and p-value columns
  return(df_target)
}


#' Perform Permutation Test for Interaction Scores
#'
#' This function performs a permutation test to calculate interaction scores between two cell types.
#' It runs the test multiple times, reshuffling cell types each time, to obtain a distribution of scores.
#'
#' @param permutation_times The number of times to run the permutation test.
#' @param cell_info Data frame containing information about cell types.
#' @param df_ligand Data frame containing ligand gene expression data.
#' @param df_receptor Data frame containing receptor gene expression data.
#' @param df_lr_pairs Data frame containing ligand-receptor gene pairs.
#' @param celltype_i Source cell type in the interaction.
#' @param celltype_j Target cell type in the interaction.
#' @return (`permutation_results`) A list of interaction scores obtained from each permutation.
permutation <- function(permutation_times, cell_info, df_ligand, df_receptor, df_lr_pairs, celltype_i, celltype_j) {
  
  # Initialize a list to store the permutation results
  permutation_results <- future_lapply(1:permutation_times, function(ii) {
    
    # Randomly shuffle the cell types in the cell_info data frame
    cell_info$celltype <- sample(cell_info$celltype)
    
    # Calculate the average expression of ligand genes and group them by cell type
    ligand_avg <- count_avg_expr(cell_info = cell_info,
                                 gene_matrix = df_ligand,
                                 gene_type = df_lr_pairs$Gene_secreted)
    
    # Calculate the average expression of receptor genes and group them by cell type
    receptor_avg <- count_avg_expr(cell_info = cell_info,
                                   gene_matrix = df_receptor,
                                   gene_type = df_lr_pairs$Gene_receptor)
    
    # Calculate the interaction score based on the average ligand and receptor expressions for the specified cell types
    permutation_score <- calculate_interaction_score(ligand_avg = ligand_avg, 
                                                     receptor_avg = receptor_avg, 
                                                     celltype_i = celltype_i,
                                                     celltype_j = celltype_j)
    
    # Return the interaction score for this permutation
    return(permutation_score)
  }, future.seed = TRUE)  # Seed for reproducibility
  
  # Return the list of interaction scores from all permutations
  return(permutation_results)
}


#' Calculate Interaction Score Between Two Cell Types
#'
#' This function calculates the interaction score between two cell types based on the average 
#' expression levels of ligands and receptors.
#'
#' @param ligand_avg Data frame containing average expression levels of ligands for each cell type.
#' @param receptor_avg Data frame containing average expression levels of receptors for each cell type.
#' @param celltype_i Source cell type for the interaction (produces the ligand).
#' @param celltype_j Target cell type for the interaction (has the receptor).
#' @return (`interaction_score`) The calculated interaction score.
calculate_interaction_score <- function(ligand_avg, receptor_avg, celltype_i, celltype_j){
  
  # Compute the interaction score using the logarithm-plus-one transformation of the average expression
  # levels of ligands and receptors for the specified cell types.
  interaction_score <- log1p(ligand_avg[[celltype_i]]) * log1p(receptor_avg[[celltype_j]])
  
  # Return the calculated interaction score
  return(interaction_score)
}


#' Process Interaction Pairs Between Two Cell Types
#'
#' This function processes the interaction pairs between two given cell types based on ligand-receptor pairs,
#' calculates interaction scores, and performs permutation tests for significance.
#'
#' @param celltype_i First cell type (source).
#' @param celltype_j Second cell type (target).
#' @param df_lr_pairs Data frame containing ligand-receptor pairs.
#' @param cell_info Data frame containing cell metadata.
#' @param df_ligand Data frame containing expression levels for ligands.
#' @param df_receptor Data frame containing expression levels for receptors.
#' @param ligand_avg Data frame containing average expression levels of ligands.
#' @param receptor_avg Data frame containing average expression levels of receptors.
#' @return (`tmp_interaction_results`) Data frame containing interaction results, scores, and p-values.
process_pair <- function(celltype_i, celltype_j, df_lr_pairs, cell_info, df_ligand, df_receptor, ligand_avg, receptor_avg) {
  
  # Create a temporary data frame to store interaction results
  tmp_interaction_results <- df_lr_pairs
  
  # Generate column names for interaction score and p-value
  interaction_score <- generate_column_name(celltype_i, celltype_j, "_score")
  p_value <- generate_column_name(celltype_i, celltype_j, "_pvalues")
  
  # Calculate interaction scores using the function 'calculate_interaction_score'
  tmp_interaction_results[[interaction_score]] <- calculate_interaction_score(ligand_avg, 
                                                                              receptor_avg, 
                                                                              celltype_i,
                                                                              celltype_j)
  
  # Perform permutation tests to calculate p-values
  permutation_times <- 1000
  permutation_results <- permutation(permutation_times = permutation_times,
                                     cell_info = cell_info,
                                     df_ligand = df_ligand,
                                     df_receptor = df_receptor,
                                     df_lr_pairs = df_lr_pairs,
                                     celltype_i = celltype_i,
                                     celltype_j = celltype_j)
  
  # Convert list of permutation results to a transposed data frame
  transformed_permutation_results <- t(data.frame(matrix(unlist(permutation_results), 
                                                         nrow=length(permutation_results), 
                                                         byrow=TRUE)))
  
  # Combine the original data frame with the permutation results
  tmp_interaction_results <- cbind(tmp_interaction_results, transformed_permutation_results)
  
  # Count how many times the permutation score is greater than the actual score
  tmp_interaction_results$permutation_result <- rowSums(sapply(tmp_interaction_results[, 13:ncol(tmp_interaction_results)], 
                                                               function(x) x > tmp_interaction_results[interaction_score]))
  
  # Calculate p-value as the proportion of times permutation score > actual score
  tmp_interaction_results[[p_value]] <- tmp_interaction_results$permutation_result / permutation_times
  
  # For rows where the actual interaction score is 0, set the p-value to 1 (not significant)
  tmp_interaction_results[tmp_interaction_results[, interaction_score] == 0, p_value] <- 1
  
  return(tmp_interaction_results)
}


#' Iterate Through All Combinations of Cell Types
#'
#' This function iterates through all possible combinations of cell types to calculate interaction scores and p-values.
#' It then combines the results into a final data frame.
#'
#' @param df_lr_pairs Data frame containing ligand-receptor pairs.
#' @param cell_info Data frame containing cell metadata.
#' @param df_ligand Data frame containing expression levels for ligands.
#' @param df_receptor Data frame containing expression levels for receptors.
#' @param ligand_avg Data frame containing average expression levels of ligands.
#' @param receptor_avg Data frame containing average expression levels of receptors.
#' @return (`final_interaction_results`) Data frame containing final interaction results for all cell types.
iterate_all_type <- function(df_lr_pairs, cell_info, df_ligand, df_receptor, ligand_avg, receptor_avg) {
  
  # Get the unique and sorted cell types
  all_cell_types <- sort(unique(cell_info$celltype))
  
  # Create a copy of the original ligand-receptor pairs data frame to store final results
  final_interaction_results <- df_lr_pairs
  
  # Loop through each combination of cell types
  for (celltype_i in all_cell_types) {
    for (celltype_j in all_cell_types) {
      
      # Print current combination to the console
      print(paste0(celltype_i, ">", celltype_j))
      
      # Calculate interaction scores and p-values for the current combination using 'process_pair' function
      tmp_interaction_results <- process_pair(celltype_i, celltype_j, df_lr_pairs, cell_info, df_ligand, df_receptor, ligand_avg, receptor_avg)
      
      # Add the calculated scores and p-values to the final results using 'add_score_and_pvalue' function
      final_interaction_results = add_score_and_pvalue(final_interaction_results, tmp_interaction_results, celltype_i, celltype_j)
    }
  }
  
  # Return the final interaction results
  return(final_interaction_results)
}


#################################
######### Main Function #########
#################################


# Retrieve the user-supplied options
# ------------------------------------------------------------------------------------------------
opt = parse_options()


# Set up the working directory and parallel cores
# ------------------------------------------------------------------------------------------------
prepare_environment(opt$output, opt$cores)


# Process Experimental Data
# ------------------------------------------------------------------------------------------------
## Read and Process the scRNA-seq Data
processed_scRNA_data <- process_scRNA_data(matrix_path = opt$matrix,
                                           metadata_path = opt$metadata)

## Store the processed expression matrix into 'expr_matrix'
expr_matrix <- processed_scRNA_data$expr_matrix

## Store the cell metadata into 'cell_info'
cell_info <- processed_scRNA_data$cell_info


# Process the ligand-receptor pairs from the input file
# ------------------------------------------------------------------------------------------------
df_lr_pairs <- process_lrpair(lrpair_path = opt$lrpair, 
                              expr_matrix = expr_matrix)


# Extract Target Genes Data
# ------------------------------------------------------------------------------------------------
## Extract and store the ligand genes expression data
df_ligand <- extract_target_expr(expr_matrix = expr_matrix, 
                                 gene_type = df_lr_pairs$Gene_secreted)

## Extract and store the receptor genes expression data
df_receptor <- extract_target_expr(expr_matrix = expr_matrix,
                                   gene_type = df_lr_pairs$Gene_receptor)


# Calculate Average Ligand Expression by Cell Type
# ------------------------------------------------------------------------------------------------
## Compute the average expression of ligand genes for each cell type
ligand_avg <- count_avg_expr(cell_info = cell_info,
                             gene_matrix = df_ligand,
                             gene_type = df_lr_pairs$Gene_secreted)

## Compute the average expression of receptor genes for each cell type
receptor_avg <- count_avg_expr(cell_info = cell_info,
                               gene_matrix = df_receptor,
                               gene_type = df_lr_pairs$Gene_receptor)


# Iterate Through All Cell Type Combinations to Calculate Interactions
# Calculate interaction scores and p-values and combine the results
# ------------------------------------------------------------------------------------------------
final_interaction_results <- iterate_all_type(df_lr_pairs = df_lr_pairs,
                                              cell_info = cell_info,
                                              df_ligand = df_ligand,
                                              df_receptor = df_receptor,
                                              ligand_avg = ligand_avg,
                                              receptor_avg = receptor_avg)

# Save the 'final_interaction_results' data frame to a CSV file
# ------------------------------------------------------------------------------------------------
write.csv(final_interaction_results, file = paste0(opt$output, "/", "my_interaction_list_for_final_test.csv"))


# End of the Program
# ------------------------------------------------------------------------------------------------
## Capture the end time to calculate the program's total execution time
end_time <- Sys.time()

## Calculate and display the total execution time
time_diff <- difftime(end_time, start_time, units = "secs")
print(paste("Time use: ", round(time_diff, 2), " seconds"))
