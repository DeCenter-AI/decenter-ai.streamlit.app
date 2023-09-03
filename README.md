# decenter.streamlit.app
# DeCenter AI

Decentralized AI Model Training Infrastructure
Visit: https://decenter.streamlit.app

## Description

DeCenter AI is a PaaS infrastructure that empowers machine learning engineers to train AI models more quickly and affordably through decentralized parallel training mechanisms.

## Table of Contents
- [Prerequisites](#prerequisites)
- [How-to-run-with-python3](#How-to-run-with-python3)
-  [How-to-run-with-docker](#How-to-run-with-docker)
- [Overview](#overview)
- [Hackathon](#hackathon)
- [How-to](#how-to)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)
- [Support](#support)
- [Links](#links)

## Prerequisites

To run  project, you need to have the following prerequisites:

- Python (version 3.10 or higher) installed on your machine.
- The necessary Python packages and dependencies installed. You can find the required packages in the `requirements.txt`
  file of the project repository.


## How to Run with Python3

To run the OS-Chat project using `Python` and `make`, follow these steps:

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
DeCenter AI functions as a PaaS infrastructure, empowering machine learning engineers to expedite and make the training of AI models more cost-effective through decentralized parallel training methods.

The core objective of DeCenter AI is to democratize and decentralize AI model training. By offering a distributed training platform, it allows data scientists, machine learning engineers, researchers, and AI specialists to collaboratively contribute to the training of AI models.

Structured around a distributed parallel training mechanism, DeCenter AI has been designed to facilitate the training of various ML and DL models in a significantly reduced time frame and cost compared to the current norms.

Our platform incorporates a built-in incentive system, fueled by DCEN Tokens. This system not only rewards contributors and participants but also encourages them to undertake tasks such as reviewing, testing, and rating AI models.

### Features

- Intuitive AI model deployment UI
- Customizable node configuration
- Private decentralized infrastructure
- Scheduled model training

 ### Target Customers
- Machine learning engineers and data scientists
- Businesses and enterprises 
- Tech start-ups and scale-ups 

  
 ### Benefits 
- Rapid iteration
- Cost effective
- Seamless deployment
- Automated resource management

  
## Hackathon
For the hackathon, we built the PoC for project which is a distributed parallel training platform leveraging hyperledger fabric to train a single type of ML model. We also worked on the website, waitlist for erly access to generate EOI, Pitch deck, Customer profiles, Demo videos, Tokenomics, Go-to-market strategy, product pricing, token economy/usecase, market research, competitive analysis and advantage among others.

## How to use the demo
- User visits landing page 
- User views the Landing Page Opens
- User Clicks “Get Started”
- User is taken to the Sign up page
- Inputs email, username, password and Clicks “Sign Up”
- User is taken to the Dashboard page
- User Clicks on Train Model
- User is taken to the Model Upload and Configuration page
- User names the model, Uploads data sets and clicks on “Start Training”
- User is taken to Node Selection and Configuration page
- User selects a Node Package, 



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

For any inquiries or assistance, please contact our support team at decenterai.com@gmail.com or visit our [website](https://decenterai.com/).


## Links

/  [Pitch Deck](https://www.canva.com/design/DAFqtW99aQA/JaMUR8Gc23ODJXcEd6PGMw/view?utm_content=DAFqtW99aQA&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink)
