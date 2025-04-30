from fastapi import FastAPI, HTTPException, Request, Depends, Body
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .database import get_db
from .models import URLMapping
from .utils import encode_id

app = FastAPI()
url_cache = {}

@app.post("/shorten")
async def shorten_url(request: Request, db: Session = Depends(get_db), long_url: str = Body(embed=True)):
    print(f"Received long_url: {long_url}")
    if long_url in url_cache:
        return {"short_url": f"{request.base_url}{url_cache[long_url]}"}

    db_url = db.query(URLMapping).filter(URLMapping.long_url == long_url).first()
    if db_url:
        url_cache[long_url] = db_url.short_url
        return {"short_url": f"{request.base_url}{db_url.short_url}"}

    url_id = db.query(URLMapping).count() + 1
    short_url = encode_id(url_id)
    db_url = URLMapping(long_url=long_url, short_url=short_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    url_cache[long_url] = short_url
    return {"short_url": f"{request.base_url}{short_url}"}

@app.get("/{short_url_path}")
async def redirect_url(short_url_path: str, db: Session = Depends(get_db)):
    long_url = None
    for long, short in url_cache.items():
        if short == short_url_path:
            long_url = long
            break

    if not long_url:
        db_url = db.query(URLMapping).filter(URLMapping.short_url == short_url_path).first()
        if db_url:
            url_cache[db_url.long_url] = db_url.short_url
            long_url = db_url.long_url

    if long_url:
        return RedirectResponse(url=long_url, status_code=301)
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")