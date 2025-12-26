# Computer Networks Project - Part 1
In this folder, you can find the files for the first part of our final project.
We created a simulation of Application Layer messages (HTTP), encapsulated them into TCP/IP packets using Python, and captured the traffic using Wireshark.

## Files
* **`groupAvitalNaor_http_input.csv`** - The CSV file with the HTTP messages we created (using AI tools).
* **`project_notebook.ipynb`** - The Jupyter Notebook containing our code. It reads the CSV, builds the packet headers (TCP/IP), and sends them over the network.
* **`capture.pcap`** - The Wireshark recording showing that the packets were successfully sent and captured.
* **`Part1_Report.pdf`** - The final report with explanations and screenshots.

## How to run the code
1. Open the Jupyter Notebook file.
2. Make sure the CSV file path in the first cell is correct.
3. Run the cells step by step to see the packet generation and transmission.
