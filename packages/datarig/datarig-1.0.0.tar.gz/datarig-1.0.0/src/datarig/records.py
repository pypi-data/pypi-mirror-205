"""Records are the primary data type in DataRig. A Record is a representation of
all the data and metadata associated with a data repository. Each Record type,
no matter the repository server, has a Datasets sequence attribute. Each Dataset 
object in the Datasets sequence represents a single data file in the repository. 

All concrete Record types are expected to inherit the Record ABC. Currently,
this module contains the following concrete record types:
```
    - Zenodo
```

The corresponding API url endpoints needed to retrieve a specific record are:
```
    Zenodo:
        https://zenodo.org/api/records/:id
        please see https://developers.zenodo.org/#records
        No authentication required.
```

Examples:

    >>> # All Records need a url for the data repository
    >>> url = 'http://zenodo.org/api/records/7868945'
    >>> from datarig import Zenodo
    >>> record = Zenodo(url)
    >>> # print the record
    >>> print(record)
    >>> # locate and print the 'annotations_001.txt' dataset
    >>> print(record.locate('annotations_001.txt'))
    >>> # download the annotations_001.txt to a temp dir
    >>> import tempfile
    >>> tmpdir = tempfile.mkdtemp()
    >>> record.download(tmpdir, 'annotations_001.txt')
    >>> print(f'saved file to {tmpdir}') 
"""

import abc
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import requests

from datarig.mixins import ViewContainer
from datarig.mixins import ViewInstance


class Record(abc.ABC, ViewInstance):
    """Abstract base class for reading records from a data repository with a 
    RESTful API.

    This ABC defines a protocol for reading data repositories from any websource
    utilizing a RESTful API. Inheritors are required to override the data
    abstract method in their concrete Record classes. 
    """

    def __init__(self, url: str, **kwargs) -> None:
        """Initialize this Record with a repository url where all datasets are
        housed & all additional parameters for a properly authorized GET
        request.

        Args:
            url:
                A string url for the API endpoint to a specific record.
            params:
                Additional information to include in the URL string with GETs
                request such as search terms that appear in the URL. For details
                see https://requests.readthedocs.io/en/latest/user/quickstart/
            kwargs:
                Any additional kwargs for requests GET method. This may include
                parameters for the URL string sent with GET. For details see
                https://requests.readthedocs.io/en/latest/user/quickstart/
        """

        self.url = url
        # if no timeout -> set to (5s, 30s) for (connection, retrieval)
        self.timeout = kwargs.pop('timeout', (5, 30))
        self.response = requests.get(url, timeout=self.timeout, **kwargs)
        self._json: Dict[str, Any] = self.response.json()
        self.datasets = self.data()

    @abc.abstractmethod
    def data(self) -> Sequence['Dataset']:
        """Returns a sequence of Dataset instances one per data file in this
        Record."""

    def locate(self, name: str) -> 'Dataset':
        """Returns a dataset whose name attribute matches name.

        Args:
            name:
                The name of the dataset to locate in this Record.

        Returns: A Dataset instance whose name attr. matches name.

        Raises:
            A ValueError is raised if no dataset in this Record has a name
            attribute matching name.
        """

        for dset in self.datasets:
            if dset.name.lower() == name.lower():
                return dset

        msg = 'No dataset with name {} is present in this Record.'
        raise ValueError(msg.format(name))

    def download(self,
                 directory: Optional[str],
                 name: Optional[str],
                 chunksize: int = 2048,
                 stream: bool = True,
                 **kwargs,
    ) -> None:
        """Downloads dataset(s) from this Record.
        
        Args:
            directory:
                The location where dataset(s) should be saved to. The filenames
                will match the names as they appear in the repository. If None,
                the directory will be set to the current working dir.
            name:
                The string name of a dataset to download. If None, all datasets
                in this Record will be downloaded to directory.
            chunksize:
                If stream is True, chunksize controls the number of bytes of
                memory to use during writing of the file the local disk.
            stream:
                A boolean indicating if the data should be iteratively
                downloaded (True) or fetched all at once (False).
            kwargs:
                Any valid kwarg for requests get method.
        """

        save_dir = Path(directory) if directory else Path().cwd()

        timeout = kwargs.pop('timeout', self.timeout)
        dsets = [self.locate(name)] if name else self.datasets
        for dset in dsets:
            print(f'Saving {dset.name} to {save_dir}')
            dset.download(save_dir, chunksize, stream, timeout=timeout, **kwargs)


# Dataset is a simple container type with only download method
# pylint: disable-next=too-few-public-methods
class Dataset(ViewContainer):
    """A container for describing & downloading a single dataset from a
    RESTful api Repository.

    Attributes:
        name:
            The string name of this datum.
        link:
            The url to this datum in the Repository.
        size:
            The size of this datum.
        filetype:
            The file type (extension) of this datum.
    """

    def __init__(self,
                 name: str,
                 link: str,
                 size: int,
                 file_type: str,
                 **kwargs,
    ) -> None:
        """Initialize this Dataset.

        Args:
            name:
                The name of the dataset as it appears in the repository (eg.
                annotations_001.txt)
            link:
                The url to this Dataset in the repository.
            size:
                The size in bytes of this Dataset.
            file_type:
                The type of file (i.e. extension) of this Dataset.
            kwargs:
                Any additional metadata to add to this Datasets attrs.
        """

        self.name = name
        self.link = link
        self.size = size
        self.file_type = file_type
        self.__dict__.update(**kwargs)

    def download(self,
                 directory: str,
                 chunksize: Optional[int] = 2048,
                 stream: bool = True,
                 **kwargs,
    ) -> None:
        """Downloads this dataset to directory.

        Args:
            directory:
                A directory location where this dataset will be saved to.
                If None, the current working directory will be used.
            chunksize:
                The number of bytes that should be read into memory at any time
                during the saving process. If None it will use whatever size
                chunks are received from the server.
            stream:
                Boolean indicating if the dataset should be iteratively
                downloaded.
            kwargs:
                Additional information to include in the URL string with GETs
                request such as search terms that appear in the URL. For details
                see https://requests.readthedocs.io/en/latest/user/quickstart/
        """

        save_dir = Path(directory) if directory else Path().cwd()
        target = Path(save_dir).joinpath(self.name)

        # get the dataset url's response & write
        timeout = kwargs.pop('timeout', (5, 30))
        r = requests.get(self.link, stream=stream, timeout=timeout, **kwargs)
        with open(target, 'wb') as outfile:

            if stream:
                for chunk in r.iter_content(chunk_size=chunksize):
                    outfile.write(chunk)
            else:
                outfile.write(r.content)


class Zenodo(Record):
    """A Zenodo Repository Record for reading datasets stored on Zenodo.

    This Record type extends the base Record type to include additional
    properties pulled from the server's response.
    
    Attributes:
        doi:
            The string doi associated with this repository.
        date:
            The publication date of this repository.
        license:
            The license under which this data repository was published.
        creators:
            The authors of this repository and their respective affiliations.
        description:
            A string description of the contents of this repository.
        statistics;
            The usage statistics of this repository.
    """

    def data(self) -> List['Dataset']:
        """Returns Dataset instances one per data file in this repository.

        Returns: A list of Dataset instances.
        """

        datafiles = self._json['files']

        results = []
        for dic in datafiles:
            name = dic['key']
            link = dic['links']['self']
            size = dic['size']
            file_type = dic['type']
            results.append(Dataset(name, link, size, file_type))
        return results

    @property
    def doi(self):
        """Returns the DOI of this Record."""

        return self._json['doi']

    @property
    def date(self):
        """Returns the publication date of this Record."""

        return self._json['metadata']['publication_date']

    @property
    def license(self):
        """Returns the license of this Record."""

        return self._json['metadata']['license']['id']

    @property
    def creators(self):
        """Returns a sequence of dictionaries with author information."""

        return self._json['metadata']['creators']

    @property
    def description(self):
        """Returns a string description of this data Record."""

        return self._json['metadata']['description']

    @property
    def statistics(self):
        """Returns a dict containing this Record's statistics."""

        return self._json['stats']
