<h1 align="center">
    <img src="https://github.com/mscaudill/datarig/blob/master/docs/imgs/logo.png" 
    style="width:700px;height:auto;"/>
</h1>

<p align="center">
  <a href="https://github.com/mscaudill/datarig/blob/master/LICENSE"><img
    src="https://img.shields.io/badge/License-BSD%203--Clause-teal" 
    alt="DataRig is released under the BSD 3-Clause license." />
  </a>
  <a href="https://github.com/mscaudill/datarig/tree/master#Dependencies"><img 
    src="https://img.shields.io/pypi/pyversions/datarig?logo=python&logoColor=gold" 
    alt="Python versions supported." />
  </a>
<a href="https://github.com/mscaudill/openseize/actions/workflows/test.yml"><img 
    src="https://img.shields.io/github/actions/workflow/status/mscaudill/datarig/test.yml?label=CI&logo=github" 
    alt="DataRig's test status" />
  </a>
 <a href="https://github.com/mscaudill/datarig/pulls"><img 
    src="https://img.shields.io/badge/PRs-welcome-F8A3A3"
    alt="Pull Request Welcomed!" />
  </a>
</p>

<p align="center"  style="font-size: 20px">
<a href="#Key-Features">Features</a>   |  
<a href="#Installation">Installation</a>   |  
<a href="#Dependencies">Dependencies</a>   |  
<a href="#Documentation">Documentation</a>   |  
<a href="#Attribution">Attribution</a>   |  
<a href="#Contributions">Contributions</a>   |  
<a href="#Issues">Issues</a>   |  
<a href="#Acknowledgements">Acknowledgements</a> 
</p>

# Features
Providing large testing and demo data alongside your package releases is
challenging for two reasons. First, code repositories have strict limits on file
sizes. Second, you don't want your users to wait forever to download your cool
package because you've included large data files.  If you're a python developer
and have hit these issues then <b><a href=https://github.com/mscaudill/datarig
target=_blank>DataRig</a></b> is for you.  DataRig allows you to
move data from web-based repositories into your user's local directories
post-installation. This "just-in-time" data fetching is perfect for users to
test or run your package's demos.

# Installation
DataRig can be installed into your projects environment using pip:

1. Activate the virtual or conda environment of your package
```Shell
$ source <YOUR_ENV>/bin/activate # python virtual environment
```

```Shell
$ conda activate <YOUR_ENV>
```

2. Install DataRig to your active environment
```Shell
(<YOUR_ENV>)$ pip install datarig
```

# Dependencies

DataRig is super lightweight requiring just <b>Python <span>&#8805;</span>
3.9</b> and the request library available here:

<table>

<tr>
    <th>package</th>
    <th>pypi</th>
    <th>conda</th>
  </tr>

<tr>
    <td><a href="https://requests.readthedocs.io/en/latest/" 
        target=_blank>requests</a></td>
    <td>https://pypi.org/project/requests/</td>
    <td align='center'><span>&#10003;</span></td>
  </tr>

</table>

# Documentation
Using DataRig to access a repository is simple. Just build a <b>Record</b>
instance and all the data will be at your fingertips. Here's how to do it for
a sample Zenodo repository:
```Shell
$ ipython
```
```python
>>> from datarig import Zenodo
>>> # set the url to the api endpoint url for the record id 7868945
>>> url = 'http://zenodo.org/api/records/7868945'
>>> record = Zenodo(url)
```
This record contains all of the repositories information stored as attributes.
To see everything at once, just print the record.
```python
>>> print(record)
```
You will see a datasets attribute with a list of Dataset objects. These Datasets
contain the name, url link, size and file type of the datasets that can be
downloaded from the repository record. Let's print each of them.
```python
>>> for dset in record.datasets:
...     print(dset)
```
Notice that a Dataset instance describes the data but does not contain the
actual data. To get the data to your machine, you call call the records
'download' method. Let's get help for this method before calling it.
```python
>>> help(record.download)
```
To call this method we need a directory to place the downloaded data, the name
of the dataset to download, the amount of memory to use during downloading
(chunksize) and a boolean of whether the download should be streamed to disk.
Streaming is usually the right choice since the files you will download are
likely large. Let's download the "sample_arr.npy" file from this record into
your current working dir.
```python
>>> from pathlib import Path
>>> record.download(directory=None, name='sample_arr.npy')
```

That's it! You've just downloaded a dataset from a Zenodo record :sunglasses:


# Attribution
If you find DataRig useful, please cite the Zenodo archive of this repository.

If you really like DataRig, you can also star the <a
href=https://github.com/mscaudill/datarig>repository</a> 
<span>&#11088;</span>!

# Contributions
Contributions are what makes open-source fun and we would love for you to
contribute. Please check out our [contribution guide](
https://github.com/mscaudill/datarig/blob/master/.github/CONTRIBUTING.md)
to get started.

# Issues

DataRig provides custom issue templates for filing bugs, requesting
feature enhancements, suggesting documentation changes, or just asking
questions. *Ready to discuss?* File an issue <a
href=https://github.com/mscaudill/datarig/issues/new/choose>here</a>. 

# Acknowledgements

**This work is generously supported through the Ting Tsung and Wei Fong Chao 
Foundation and the National Institute of Neurological Disorders and Stroke 
(Grant 2R01 NS100738-05A1).**



