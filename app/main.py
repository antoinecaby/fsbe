from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    main()
    return {"message": "Data initialized successfully!"}
