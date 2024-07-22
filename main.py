from typing import Annotated
from datetime import date
from fastapi import FastAPI, HTTPException, Query, Path, Depends
from sqlmodel import Session, select

from models import GenreURLChoices, BandBase, BandCreate, Band, Album
from db import init_db, get_session


app = FastAPI()

# BANDS = [
#     {'id': 0, 'name': 'The Kinks', 'genre': 'Rock'},
#     {'id': 1, 'name': 'Aphex Twin', 'genre': 'Electronic'},
#     {'id': 2, 'name': 'Black Sabbath', 'genre': 'Metal', 'albums': [
#         {'title': 'Master of Reality', 'date': '1971-07-21'}
#     ]},
#     {'id': 3, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
#     {'id': 4, 'name': 'Eminem', 'genre': 'Hip-Hop'},
# ]

@app.get("/bands")
async def get_bands(
    genre: GenreURLChoices | None = None,
    q: Annotated[str | None, Query(max_length=10)] = None,
    session: Session = Depends(get_session)
) -> list[Band]:
    band_list = session.exec(select(Band)).all()

    if genre:
        band_list = [ b for b in band_list if b.genre.value.lower() == genre.value ]
    if q:
        band_list = [ b for b in band_list if q.lower() in b.name.lower() ]
    return band_list


@app.get("/bands/{band_id}")
async def get_bands_by_id(
    band_id: Annotated[int, Path(title="The band ID")],
    session: Session = Depends(get_session)
) -> Band:
    band = session.get(Band, band_id)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found")
    return band


@app.post("/bands")
async def create_band(
    band_data: BandCreate,
    session: Session = Depends(get_session)
) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)

    if band_data.albums:
        for album in band_data.albums:
            release_date = tuple(int(e) for e in album.release_date.split("-"))
            album_obj = Album(title=album.title, release_date=date(*release_date), band=band)
            session.add(album_obj)

    session.commit()
    session.refresh(band)

    return band