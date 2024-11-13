from fastapi import FastAPI, UploadFile, File
import uvicorn
import os
import shutil
import main

app = FastAPI()


# Route to process audio
@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    file_location = f"temp_audio/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # Call your processCommand function from main.py
    command_text = main.recognize_speech_from_file(file_location)
    if command_text:
        response = main.processCommand(command_text)
    else:
        response = "Sorry, I couldn't understand the command."

    # Clean up temp files
    os.remove(file_location)

    return {"command": command_text, "response": response}


@app.post("/speak/")
async def speak_text(text: str):
    # Call the speak function from your main.py
    main.speak(text)
    return {"message": "Audio generated and spoken"}


# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
