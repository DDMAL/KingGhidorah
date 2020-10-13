# Welcome to King Ghidorah's Documentation

A scripting interface for the Rodan API that allows more granular control over your **projects**, **workflows**, and **resources** and the three queues for RodanTasks, **Python2**, **Python3**, and **core rodan**. It is named for each of the 3 heads of the famous Kaiju, **King Ghidorah**. You may be wondering why all the examples use `kd` instead of `kg` as the abbreviation.

## Installation

- `poetry install` preferred method.
  - or `pip install .`

## Usage

- Fill in the user credentials and the Rodan API domain.
  - You can use a proxy to connect to the server too, just make sure that you replace `false` with the proxy information: `"socks5://localhost:5000"`
- Learn by example by using the calls in the `EXAMPLES.md` file.

## Codestyle

Just run `yapf -ir .`
