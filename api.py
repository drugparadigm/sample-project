
from flask import Flask,request, Response,jsonify
import subprocess
from datetime import datetime
import json
import traceback
import os
import shutil
from src.data import main  # Replace with your inference function 
app = Flask(__name__)

UPLOAD_FOLDER = 'src/data/input'  # Folder where files will be uploaded
@app.route('/score', methods=['POST'])
def score() -> Response:
    reqId=None

    try:

        ## If your inputs are not files

        data = request.form

        required_fields=['reqId','field1', 'field2', 'field3']  # Do not remove reqId and replace with your actual request body names

        missing_fields = [field for field in required_fields if field not in request.form]
        if missing_fields:
            raise ValueError(f"Missing fields in form data: {', '.join(missing_fields)}")
        
        reqId = request.form.get('reqId')
        
        with open(f"src/data/input/{reqId}-input.json", "w") as f:
            json.dump(data, f)

        ## If your inputs also includes files, you can use the below code

        data = request.files
        if 'reqId' not in request.form:
            raise ValueError ("Missing reqId in form data")

        reqId = request.form.get('reqId')

        values=['file1', 'file2', 'file3']  # Replace with your actual file names
        for value in values:
            if value not in data:
                raise ValueError (f"Missing {value} in form data")
        
        # Create a json object to store file names to access the files for inference
        json_data = {}
        file_paths = []
        for value in values:
            file = request.files[value]
            if file: 
                json_data[value] = reqId+'_'+file.filename
                file_path = os.path.join(UPLOAD_FOLDER, reqId+'_'+file.filename)
                file_paths.append(file_path)
                file.save(file_path)
            else:
                raise ValueError (f"Missing {value} in form data")
            
        with open(f"src/data/input/{reqId}_input.json", "w") as f:
            json.dump(json_data, f)

        result=main() 

        return jsonify({"message": "Inference completed successfully", "output": result}), 200

    except ValueError as e:
        traceback.print_exc()
        return jsonify({"message":"Inference failed","error": f"{e}"}), 500
    
    finally:
        if len(os.listdir(UPLOAD_FOLDER)) > 0:
            for file in os.listdir(UPLOAD_FOLDER):
                if os.path.isfile(os.path.join(UPLOAD_FOLDER, file)):
                    if file.startswith(reqId+'_'):
                        file_path = os.path.join(UPLOAD_FOLDER, file)
                        if os.path.exists(file_path):
                            os.remove(file_path)
                else:
                    if file.startswith(reqId+'_'):
                        dir_path = os.path.join(UPLOAD_FOLDER, file)
                        if os.path.exists(dir_path):
                            shutil.rmtree(dir_path)
                            

@app.route('/health/<sample>', methods=['POST'])
def samplescore(sample) -> Response:
 
    if sample == "hi":
        date=datetime.now().strftime("%H:%M:%S")
        return f"Hello {date}"
    else:
        return jsonify({'error':"Unauthorized access"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
