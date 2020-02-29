# BiQPS
* This is an open software, called BiQPS, for bitstream-based quality prediction in adaptive streaming.
BiQPS is inputed by a .csv file containing data of a streaming session. 
In particular, each line of the file is a record of each segment in the session. 
Each record consists of five parameters separated by commas, namely stalling durations SD, quantization parameter QP, bitrate BR, resolution RS, and frame-rate FR.
The output Qo is the predicted overall quality of the session.  

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
	biQPS [-h] [--K K] [--QsiModel {SQM}] [--QoMode {1,2,3}] csvFile
	positional arguments:
	  csvFile			Input .csv file

	optional arguments:
	  -h, --help        Show this help text
	  --K 				Interval length (default: 20); only valid for QoMode=1 and QoMode=2				
	  --LcMode 			Local computation mode (default:'SQM')
	  --GcMode			Global computation mode (default:3)
	

## Example

The predicted ovarall quality value of a session can be obtained by the following command. 
  ```
	biQPS inputData.csv	
  ```
Output:
  ```
	Qo: 1.6416281
  ```

## Authors

* **Tran Huyen** - *The University of Aizu, Japan* - tranhuyen1191@gmail.com

## Acknowledgments

If you use this source code in your research, please cite

1. The link to this repository.

## License

The source code is only used for non-commercial research purposes.
* If you have any questions, suggestions or corrections, please email to tranhuyen1191@gmail.com. 
