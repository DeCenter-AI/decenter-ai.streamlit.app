# decenter.streamlit.app

# DeCenter AI

Decentralized AI Model Training Infrastructure
Visit: https://decenter.streamlit.app

## Description

DeCenter AI is a PaaS infrastructure that empowers machine learning engineers to train AI models more quickly and
affordably through decentralized parallel training mechanisms.

## Table of Contents

- [decenter.streamlit.app](#decenterstreamlitapp)
- [DeCenter AI](#decenter-ai)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [How to Run with Python3](#how-to-run-with-python3)
  - [How to Run via Docker](#how-to-run-via-docker)
  - [Overview](#overview)
    - [Features](#features)
    - [Target Customers](#target-customers)
    - [Benefits](#benefits)
  - [Hackathon](#hackathon)
  - [How to use the demo](#how-to-use-the-demo)
  - [Backend Workflow](#backend-workflow)
- [DeCenter AI Model Training Workflow](#decenter-ai-model-training-workflow)
    - [Organization (Data Scientists, ML Engineers, AI Engineers, Model Trainers)](#organization-data-scientists-ml-engineers-ai-engineers-model-trainers)
    - [NFTs Certifications](#nfts-certifications)
    - [Hyperledger](#hyperledger)
    - [Execution Nodes](#execution-nodes)
    - [DeCenter AI Validator Node](#decenter-ai-validator-node)
    - [Hyperledger Fabric](#hyperledger-fabric)
    - [BNB Greenfield](#bnb-greenfield)
    - [User](#user)
  - [How to Contribute](#how-to-contribute)
  - [License](#license)
  - [Authors](#authors)
  - [Acknowledgments](#acknowledgments)
  - [Support](#support)
  - [Links](#links)

## Prerequisites

To run project, you need to have the following prerequisites:

- Python (version 3.10 or higher) installed on your machine.
- The necessary Python packages and dependencies installed. You can find the required packages in the `requirements.txt`
  file of the project repository.
- Download and extract the sample python code (model training code), Dataset, requirement text and pre-trained model for
  the demo [sample1.zip](https://github.com/Nasfame/decenter.streamlit.app/files/12517829/sample1.zip)

## How to Run with Python3

To run using `Python` and `make`, follow these steps:

```shell
   git clone <repository_url> decenter.app
   cd decenter.app
   make install
#   create .env file and fill in the environment variables
   make run
```

## How to Run via Docker

To run the project using `Docker`, follow these steps:

```shell
docker build -t app .
docker run -p 8501:8501 app
```

> For developers,
> I recommend <br>
> ```docker run -it -e "mode=development" -p 8501:8501 decenter``` <br>
> playaround and test your code!


> Please note that you will need to replace `<repository_url>` with the actual URL of this/forked repo

I hope this helps! Raise issues to clarify your doubts and notify bugs.

## Overview

DeCenter AI functions as a PaaS infrastructure, empowering machine learning engineers to expedite and make the training
of AI models more cost-effective through decentralized parallel training methods.

The core objective of DeCenter AI is to democratize and decentralize AI model training. By offering a distributed
training platform, it allows data scientists, machine learning engineers, researchers, and AI specialists to
collaboratively contribute to the training of AI models. Structured around a distributed parallel training mechanism,
DeCenter AI has been designed to facilitate the training of various ML and DL models in a significantly reduced time
frame and cost compared to the current norms.
Our platform incorporates a built-in incentive system, fueled by DCEN Tokens. This system not only rewards contributors
and participants but also encourages them to undertake tasks such as reviewing, testing, and rating AI models.

### Features

- Intuitive AI model deployment UI
- Customizable node configuration
- Private decentralized infrastructure
- Scheduled model training

### Target Customers

- Data scientists
- Machine learning engineers
- AI Engineers
  View
  our [Customer profile](https://www.canva.com/design/DAFri_nB4wo/eI4WrI2aQGyfy6T1bx4ZTQ/view?utm_content=DAFri_nB4wo&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink).

### Benefits

- Rapid iteration
- Cost effective
- Seamless deployment
- Automated resource management

## Hackathon

For the hackathon, we built the PoC for project which is a distributed parallel training platform leveraging hyperledger
fabric to train a single type of ML model. We also worked on the website, waitlist for erly access to generate EOI,
Pitch deck, Customer profiles, Demo videos, Tokenomics, Go-to-market strategy, product pricing, token economy/usecase,
market research, competitive analysis and advantage among others.

## How to use the demo

- Visit: https://decenter.streamlit.app
- Enter a model name
- Upload python code (model training code)
- Upload dataset
- Upload requirement texts
- Upload pre-trained model
- click on train
- Download your trained model once the model training process is complete

## Backend Workflow

![Decenter Ai Deck (4)](https://github.com/Nasfame/decenter.streamlit.app/assets/131058062/d233ea0c-e09e-4787-a9f5-997bde5902a7)

# DeCenter AI Model Training Workflow

This provides an overview of the DeCenter AI model training workflow, outlining the interactions between various
components and actors involved in the process.

### Organization (Data Scientists, ML Engineers, AI Engineers, Model Trainers)

1. Initiates model training on the DeCenter AI platform.
2. Provides model name, uploads datasets, pre-trained models, and requirements.
3. Model-related data, including metadata in `metadata.json`, is stored in a folder within the DeCenter AI bucket on BNB
   Greenfield.
4. If datasets or models exceed 2GB, they are sharded and stored on DeCenter for efficient handling.
5. Access to the folder in the DeCenter AI bucket is granted only to the wallet that initiated the training.

### NFTs Certifications

- NFTs (Non-Fungible Tokens) certifications are generated and issued to trainers and contributors as a form of
  recognition for their contributions to the model training process.

### Hyperledger

1. Retrieves model-related data, including model name, datasets, models, pre-trained models, and `metadata.json`.
2. Sends this data through the model training nodes (Execution Nodes) for model training.

### Execution Nodes

1. Receive the model-related data from Hyperledger.
2. Train the models using the provided data.
3. Once training is complete, all trained models are sent to the DeCenter AI validator Node for evaluation.

### DeCenter AI Validator Node

1. Receives trained models from the Execution Nodes.
2. Evaluates and scores each model.
3. Selects the best-performing model based on the evaluation results.
4. Sends the selected model back to Hyperledger Fabric.

### Hyperledger Fabric

1. Records and maintains the selected trained model.
2. Sends the trained model to BNB Greenfield for storage.

### BNB Greenfield

- Receives the trained model from Hyperledger Fabric and securely stores it.

### User

- Retrieves the trained model from BNB Greenfield for downloading and testing.

This workflow outlines how DeCenter AI manages the training, evaluation, and storage of AI models, ensuring that the
best-performing model is selected and made available for users. NFTs certifications add an additional layer of
recognition for contributors and trainers.

## How to Contribute

We welcome contributions from the community! To get started, follow these steps:

1. Fork the repository on GitHub.
2. Clone your fork of the repository to your local machine.
3. Create a new branch for your changes: `git checkout -b <your-username>/your-feature-branch`.
4. Make your changes and commit them to your branch.
5. Push your changes to your fork on GitHub.
6. Open a pull request from your fork's branch to the main repository.

Please make sure to follow the [Code of Conduct](./CODE_OF_CONDUCT.md) when contributing to this project.

## License

DeCenter AI is released under the [MIT License](https://opensource.org/licenses/MIT).

## Authors

- Victor Kaycee [Email](victorkaycee17@gmail.com).  [Linkedln](https://www.linkedin.com/in/victor-kaycee).
- Glory Lucas  [Email](lucasgold24@gmail.com).  [Linkedln](https://www.linkedin.com/in/glorylucas/).
- Hiro Hamada  [Email](laciferin@gmail.com).  [Linkedln](http://linkedin.com/in/laciferin/).
- William Ikeji  [Email](williamikeji@gmail.com).  [Linkedln](https://www.linkedin.com/in/codypharm/).

## Acknowledgments

We would like to thank the following individuals and organizations for their contributions to DeCenter AI:

- Caleb Lucas for his support and encouragement
- Our dedicated community developers for their valuable feedback and support.

## Support

For any inquiries or assistance, please contact our support team at admin@decenterai.com or visit
our [website](https://decenterai.com/).

## Links

/  [Pitch Deck](https://www.canva.com/design/DAFqtW99aQA/JaMUR8Gc23ODJXcEd6PGMw/view?utm_content=DAFqtW99aQA&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink)
