## README for Molecular Prediction Jupyter Notebook

### Overview:
This Jupyter notebook provides a workflow to predict molecular properties using graph-based neural networks with the PyTorch Geometric library. The ESOL dataset from MoleculeNet is utilized as the primary dataset, and molecule representations are visualized with the RDKit library.

### Key Sections:

1. **Library Imports**:
    - Essential libraries like RDKit for molecular processing and Torch Geometric for handling graph data are imported.

2. **Data Loading**:
    - The ESOL dataset from MoleculeNet is loaded.
    - The first molecule in the dataset is visualized using RDKit.

3. **Neural Network Model Definition**:
    - A Graph Convolutional Network (GCN) class is defined, encapsulating the model architecture.
    - The GCN model comprises multiple graph convolution layers and a linear output layer.
    - The model outputs both predictions and embeddings of the molecules.

4. **Training Preparation**:
    - A mean squared error loss function is chosen for regression.
    - Adam optimizer is selected with a learning rate of `0.0007`.
    - The dataset is split, and data loaders for training and testing are defined.
  
5. **Training Loop**:
    - The model is trained for 2000 epochs.
    - Loss values are printed every 100 epochs.
    - Training loss is tracked over epochs.

6. **Evaluation**:
    - A test batch is passed through the trained model to obtain predictions.
    - The real and predicted values are collected into a dataframe.
    - A scatter plot visualizes the relationship between true and predicted molecular properties.

### Requirements:

- **RDKit**: A collection of cheminformatics and machine learning tools. It's used here to handle and visualize molecular data.
- **Torch and Torch Geometric**: Libraries for deep learning on graphs and other irregular structures.
- **MoleculeNet**: A collection of molecular datasets from Torch Geometric. Here, the ESOL dataset is specifically used.
- **Pandas**: Required for data handling and manipulation, especially in the evaluation section.
- **Seaborn (sns)**: Used for data visualization, specifically the scatter plot.

### Usage:
To execute the notebook:
1. Ensure that all the required libraries are installed.
2. Run each cell in sequence.
3. Monitor the training loop for loss values.
4. Examine the scatter plot to assess the model's prediction performance on a test batch.

### Additional Notes:
- Always make sure to use appropriate computational resources as some graph-based models can be memory intensive.
- The dataset's size and the model's depth can affect training times significantly.
- Adjust hyperparameters (like learning rate, number of epochs, etc.) based on convergence and performance.