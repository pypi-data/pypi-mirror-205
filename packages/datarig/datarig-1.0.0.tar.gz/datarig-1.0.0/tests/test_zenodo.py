from pathlib import Path
import tempfile
import pytest
import numpy as np

from datarig import Zenodo

# CHANGE DATARIG TO ACCEPT JUST A RECORD NUMBER FOR ZENODO
URL = 'http://zenodo.org/api/records/7868945'
RECORD = Zenodo(URL)


@pytest.fixture(scope='module', params=range(5))
def name(request):
    """The expected dataset names of this RECORD."""

    names = ['annotations_001.txt',
             'recording_001.edf',
             'sample_excel.xls', 
             'sample_arr.npy',
             'sample_text.txt'
             ]
    
    yield names[request.param]


def test_data(name):
    """Validates that the data method correctly identifies all available
    datasets in the repository."""

    in_record = [dset.name for dset in RECORD.datasets]
    assert name in set(in_record)


def test_locate(name):
    """Validate that the record returns the correct datasets from a 'locate'
    method call."""

    dset = RECORD.locate(name)
    assert name == dset.name


def test_locate_error():
    """Validate a ValueError is raised if a name is requested that does not
    exist in this Repository."""

    with pytest.raises(Exception) as e:
        RECORD.locate('missing.txt')


def test_dset_attrs(name):
    """Validates that each dataset in this record has all expected attrs of
    a dataset."""

    dset = RECORD.locate(name)
    assert all([hasattr(dset, a) for a in 'name link size file_type'.split()])


def test_doi():
    """Validate the doi property of this Record."""

    doi = '10.5281/zenodo.7868945'
    assert RECORD.doi == doi


def test_date():
    """Validate that the publication date of this Record is correct."""

    date = "2023-04-26"
    assert RECORD.date == date


def test_license():
    """Validate that the fetched license information is correct."""

    license = 'CC-BY-4.0'
    assert RECORD.license == license


def test_creators():
    """Validate that the fetched creators orcid is correct."""

    assert RECORD.creators[0]['orcid'] == '0000-0002-3656-9261'


def test_description():
    """Validates the description is present."""

    assert RECORD.description is not None


def test_download_array():
    """Verifies that the Record correctly downloads the numpy array."""

    tempdir = tempfile.mkdtemp()
    RECORD.download(tempdir, 'sample_arr.npy')

    # open the downloaded file and compare against expected
    path = Path(tempdir).joinpath('sample_arr.npy')
    downloaded = np.load(path)
    expected = np.arange(1000).reshape(4, -1)
    assert np.allclose(downloaded, expected)
