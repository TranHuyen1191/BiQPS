# BiQPS
* This is an open software, called BiQPS, for bitstream-based quality prediction in adaptive video streaming.
BiQPS is inputed by .csv files containing data of streaming sessions. 
In particular, each line of a file is a record of each segment in a session. 
Each record consists of five parameters separated by commas, namely stalling duration SD, quantization parameter QP, bitrate BR, resolution RS, and frame-rate FR.
The predicted overall quality values of the sessions are saved in a .txt output file.  

## Installation
BiQPS was tested with 1) Ubuntu 16.04 LTS, python 3.5, pip 19.2.3, and tensorflow 1.13.1 and 2) Ubuntu 18.04.3 LTS, python 3.6, pip 9.0.1, and tensorflow 1.11.0.

- Download and install pip3 and python3
	```
	sudo apt update 
	sudo apt install python3-dev python3-pip
	```
- Download and install Tensorflow from https://www.tensorflow.org/install/pip
- Clone the BiQPS repository
	```
	git clone https://github.com/TranHuyen1191/BiQPS.git
	```
- Install BiQPS
	```
	pip3 install --user .
	```
  - Note: You can uninstall BiQPS software with ```	pip3 uninstall biQPS 	```
 
 ## Usage
	biQPS [-h] [-i I [I ...]] [--K K] [--lcMode {SQM}] [--gcMode {1,2,3}] [-o O]
	optional arguments:
	  -h, --help        show this help message and exit
	  -i I [I ...]      .csv input files
	  --K K             interval length (default: 20); only valid for gcMode=1 and gcMode=2
	  --lcMode {SQM}    local computation mode (default:'SQM')
	  --gcMode {1,2,3}  global computation mode (default:3)
	  -o O              .txt output file

## Example

The predicted ovarall quality value of a session can be obtained by the following command. 
  ```
	biQPS -i inputData.csv	
  ```
The output is saved in output.txt
  ```
	inputFiles	predictedValues
	inputData.csv	1.783356
  ```

## Authors

* **Tran Huyen** - *The University of Aizu, Japan* - tranhuyen1191@gmail.com

## Acknowledgments

If you use this source code in your research, please cite

1. The link to this repository.

## License

The source code is only used for non-commercial research purposes.
* If you have any questions, suggestions or corrections, please email to tranhuyen1191@gmail.com. 
