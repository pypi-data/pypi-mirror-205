import os
import pytest
from ..conftest import FIXTURE_DIR
from pathlib import Path
import requests
from geovisio_cli import sequence, exception, model
from datetime import timedelta
import re


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
)
def test_valid_upload(geovisio, datafiles):
    collection = sequence.upload(path=Path(datafiles), geovisio=geovisio)

    assert len(collection.uploaded_pictures) == 3
    assert len(collection.errors) == 0

    sequence.wait_for_sequence(collection.location, timeout=timedelta(minutes=1))
    status = sequence.status(collection.location)
    sequence_info = sequence.info(collection.location)
    # 3 pictures should have been uploaded
    assert len(status.pictures) == 3

    for i in status.pictures:
        assert i.status == "ready"

    # the collection should also have 3 items
    collection = requests.get(f"{collection.location}/items")
    collection.raise_for_status()

    features = collection.json()["features"]
    assert len(features) == 3

    assert sequence_info.title == "test_valid_upload0"
    assert sequence_info.interior_orientation == [
        sequence.InteriorOrientation(
            make="SONY", model="FDR-X1000V", field_of_view=None
        )
    ]


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
    os.path.join(FIXTURE_DIR, "invalid_pic.jpg"),
)
def test_upload_with_invalid_file(geovisio, datafiles):
    collection = sequence.upload(path=Path(datafiles), geovisio=geovisio)

    # Only 3 pictures should have been uploaded, 1 is in error
    assert len(collection.uploaded_pictures) == 3
    assert len(collection.errors) == 1

    # But the collection status should have 3 items (and be valid)
    sequence.wait_for_sequence(collection.location, timeout=timedelta(minutes=1))
    status = sequence.status(collection.location)
    # 3 pictures should have been uploaded
    assert len(status.pictures) == 3

    assert all([i.status == "ready" for i in status.pictures])

    # the collection should also have 3 items
    collection = requests.get(f"{collection.location}/items")
    collection.raise_for_status()
    features = collection.json()["features"]
    assert len(features) == 3


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "invalid_pic.jpg"),
)
def test_upload_with_no_valid_file(geovisio, datafiles):
    collection = sequence.upload(path=Path(datafiles), geovisio=geovisio)

    assert len(collection.uploaded_pictures) == 0
    assert len(collection.errors) == 1

    status = requests.get(f"{collection.location}/geovisio_status")
    assert (
        status.status_code == 404
    )  # TODO: For the moment geovisio return a 404, we it should return a valid status response with the sequence status

    items = requests.get(f"{collection.location}/items")
    items.raise_for_status()
    features = items.json()["features"]
    assert len(features) == 0


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
)
def test_upload_on_invalid_url_host(datafiles):
    with pytest.raises(exception.CliException) as e:
        sequence.upload(
            path=Path(datafiles), geovisio=model.Geovisio(url="http://some_invalid_url")
        )
    msg = str(e.value)
    assert msg.startswith(
        """The API is not reachable. Please check error and used URL below, and retry later if the URL is correct.

[bold]Used URL:[/bold] http://some_invalid_url/api/collections
[bold]Error:[/bold]"""
    )
    assert "Failed to establish a new connection:" in msg


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
)
def test_upload_on_invalid_url_path(geovisio, datafiles):
    with pytest.raises(exception.CliException) as e:
        sequence.upload(
            path=Path(datafiles),
            geovisio=model.Geovisio(url=geovisio.url + "/some_additional_path"),
        )
    msg = str(e.value)
    assert msg.startswith(
        f"""The API URL is not valid.

Note that your URL should be the API root (something like https://geovisio.fr, https://panoramax.ign.fr or any other geovisio instance).
Please make sure you gave the correct URL and retry.

[bold]Used URL:[/bold] {geovisio.url}/some_additional_path/api/collections
[bold]Error:[/bold]"""
    )


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
)
def test_upload_on_invalid_url_schema(datafiles):
    with pytest.raises(exception.CliException) as e:
        sequence.upload(
            path=Path(datafiles),
            geovisio=model.Geovisio(url="a non valid url at all"),
        )
    assert str(e.value).startswith(
        """Error while connecting to the API. Please check error and used URL below

[bold]Used URL:[/bold] a non valid url at all/api/collections
[bold]Error:[/bold]"""
    )
