# decenter.streamlit.app

Visit: https://decenter.streamlit.app

## How

1. 

## Prerequisites

To run  project, you need to have the following prerequisites:

- Python (version 3.10 or higher) installed on your machine.
- The necessary Python packages and dependencies installed. You can find the required packages in the `requirements.txt`
  file of the project repository.


## How to Run with Python3 and `make`

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

## How to Contribute

We welcome contributions from the community! To get started, follow these steps:

1. Fork the repository on GitHub.
2. Clone your fork of the repository to your local machine.
3. Create a new branch for your changes: `git checkout -b <your-username>/your-feature-branch`.
4. Make your changes and commit them to your branch.
5. Push your changes to your fork on GitHub.
6. Open a pull request from your fork's branch to the main repository.

Please make sure to follow the [Code of Conduct](./CODE_OF_CONDUCT.md) when contributing to this project.