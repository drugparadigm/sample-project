# ML/DL Inference as a Dockerized REST API
### Instruction to follow

* Install Docker engine.
*   Add the files/folders required only for inference in src directory
* Add the files required for input (if any) in src/data/input 
* Add the model checkpoints in src/checkpoints dir
* Generate a yaml file with your conda environment with the command:
```
conda env export > <environment-name>.yml
```
* Add the packages that are hard to install with the installation commands in additional-softwares.sh
* Rename the filenames and environment names in Dockerfile
* Rename the inference file name in api.py
* Change the inference file( that you call in api.py) so that it accepts input from arguments.
* In case of using input files from tmp change the code to read the input files from tmp directory.
* Run api.py with the above changes:
```
    python api.py
```
* If there are no errors then create a docker image with the command:
```
    docker build -t <image-name> .
```
* Run the image with:
```
    docker run -p 5000:5000 <image-name> 
```
