
from flask import Flask,request, Response,jsonify
import subprocess
from datetime import datetime
import json
import traceback
import os
import shutil
from src.data import main  # Replace with your inference function 
app = Flask(__name__)


@app.route('/score', methods=['POST'])
def score() -> Response:
    reqId=None

    try:

        data = request.form

        required_fields=['reqId','field1', 'field2', 'field3']  # Do not remove reqId and replace with your actual request body names

        missing_fields = [field for field in required_fields if field not in request.form]
        if missing_fields:
            raise ValueError(f"Missing fields in form data: {', '.join(missing_fields)}")
        
        reqId = request.form['reqId']
        
        with open(f"src/data/input/{reqId}-input.json", "w") as f:
            json.dump(data, f)
        
        # Replace with your actual inference function call and import function
        # For example, if you have a function named `main` in your inference file and main() returns the result of the inference:
        result=main() 

        return jsonify({"message": "Inference completed successfully", "output": result}), 200


    except ValueError as e:
        traceback.print_exc()
        return jsonify({"message":"Inference failed","error": f"{e}"}), 500
    
    finally:
        paths=[f'{reqId}-input.json','folder1', 'folder2']  # Add the files/folders created during the inference in src/data/input
        for path in paths:
            path = os.path.join('src/data/input', path)
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
            

@app.route('/health/<sample>', methods=['POST'])
def samplescore(sample) -> Response:
 
    if sample == "hi":
        date=datetime.now().strftime("%H:%M:%S")
        return f"Hello {date}"
    else:
        return jsonify({'error':"Unauthorized access"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)