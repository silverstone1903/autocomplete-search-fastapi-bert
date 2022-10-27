from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import torch
from annoy import AnnoyIndex
import transformers
import torch
import uvicorn

# copied model for fast loading (no need to download again)
model_name = "model/models--bert-base-multilingual-cased/snapshots/cf732291d5a8eace7b973ccd13c95ec07b19e734/"
# created annoy index and saved it
index_name = "data/movies_bert-base-multilingual-cased_euc.annoy"

index = AnnoyIndex(f = 768, metric="euclidean")
index.load(index_name)
model = transformers.BertModel.from_pretrained(model_name)
tokenizer = transformers.BertTokenizer.from_pretrained(model_name, do_lower_case=True)
movies = pd.read_feather("data/movies.feather")
documents = movies.movie_name.values.tolist()

templates = Jinja2Templates(directory="./templates")
app = FastAPI(title="BERT Based Search API") 

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def encode(document: str) -> torch.Tensor:
    tokens = tokenizer(document, return_tensors="pt")
    vector = model(**tokens)[0].detach().squeeze()
    return torch.mean(vector, dim=0)

@app.get("/search")
def search_annoy(query: str, k=5):
    if len(query) > 2:
        encoded_query = encode(query).unsqueeze(dim=0).numpy()[0]
        top_k = index.get_nns_by_vector(encoded_query, k, search_k = 10,  include_distances=True)
        scores = top_k[1]
        results = [documents[_id] for _id in top_k[0]]
        return results
    else:
        return "No Results Found"

@app.get("/health", status_code=200, summary="Returns HC Page.", tags=["hc"])
async def home():
    return {"message": "Still Alive"}


@app.get("/", status_code=200, summary="Returns Search Page.", tags=["search"])
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse(
        "home.html", context={"request": request, "result": result}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")