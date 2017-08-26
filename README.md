# Giveme5W

Giveme5W(1H) is a state of the art open-source 5W Question Answering system for news articles. It can either be used through a simple RESTapi or directly included in existing Python projects. Depending on the configuration Giveme5W parses each document for the answers to the following  questions:

* **Who** is involved?
* **What** happened?
* **Where** did it take place?
* **When** did it happen?
* **Why** did it happen?
* **How** did it happen?

## Getting started
Before you can use Giveme5W, you need to make sure you have a CoreNLP-server runtimes.

In the case you first to have to install CoreNLP please refer to the CoreNLPs extensive [documentation](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html) and follow the instructions on how to install CoreNLP and start a server.

 * download the server itself from [here](https://stanfordnlp.github.io/CoreNLP/index.html#download)
    * at the time of writing [this](http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip) was the newest version
 * download also the english language package on the same page
    * at the time of writing [this](http://nlp.stanford.edu/software/stanford-english-corenlp-2017-06-09-models.jar) was the newest version
 * extract the server zip,
 * extract the language zip, copy it inside the server directory
 * copy it into [Giveme5W-runtime-resources](#Giveme5W-runtime-resources) next to your repository folder

Run environment_enhancer.py to start up coreNLP.

## Configuration
All configurations are optional.

### CoreNLP Host
By default, Giveme5W tries to start the server with default port.

You can prevent this by setting up a preprocessor with another url in case you run it on another masch:
(Bsp: extractor/examples/simple_api.py)
```python
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor
preprocessor = Preprocessor('localhost:9000')
FiveWExtractor(preprocessor=preprocessor)
```

Then start up CoreNLP by:
```
$ nohup java -mx4g edu.stanford.nlp.pipeline.StanfordCoreNLPServer 9000 &
```


### Output Configuration

- For file based data - every input is transferred to the output
    -  For instance, annotated is already a part of the provided example files
- REST service and file based input have the same output and configuration
- Fields or their parents indicate with a prefix their origin, if no from giveme5W itself
  - nlp, from CoreNLP



```json
"who": {
      "annotated": [
        {
          "text": "UK"
        }
      ],
      "label": "who",
      "extracted": [
        {
          "score": 1.0,
          "words": [
            {
              "text": "The",
              "nlpTag": "DT"
            },
            {
              "text": "UK",
              "nlpTag": "NNP"
            }
          ],
          "nlpIndexSentence": 5
        },
        {
          "score": 0.2,
          "words": [
            {
              "text": "The",
              "nlpTag": "DT"
            },
            {
              "text": "UK",
              "nlpTag": "NNP"
            }
          ],
          "nlpIndexSentence": 6
        }
       ]
```
>This is the output of one question;
    - inclusive the golden standard annotation
    - 2 extracted candidates with some additional information


Additional information can be added to the output by setting them as true in the config object.
- information per candidate: like nlpIndexSentence or score
- information per token like: lemma, tag

```python
{
  'information': {
        'nlpIndexSentence': true
        'candidate':{
            'nlpTag': true
        }
   },
   'onlyTopCandidate': False
   'enhancer': {
    'see': 'Enhancements'
   }
}
```
> see configuration.py for all available settings


Use the configuration Singleton to make adjustments
```python
from extractor.configuration import Configuration as Config
Config.get()['information']['nlpIndexSentence'] = False
```


> Not all extractors support config so far

## File based usage
Giveme5W can read and write news in a json format [example](https://github.com/fhamborg/news-please/blob/master/newsplease/examples/sample.json).
There is also a converter script to convert gate.xml files to json.

Files can be processed like a stream (parse_documents_simple.py) or can be loaded in advance and kept in memory (parse_documents.py).
Because CoreNLP server has a long execution time, it is possible to cache the result on the filesystem to speed up multiple executions.
The raw result is attached to each document under clp_result.

The included example files already preprocessed. So you can process them without a running CoreNLP server instance.
Delete all files in "/cache", if you want to precess them again.


## REST-Service
Its also possible to use giveme5W as rest service.

```
$ python extractor/examples/simple_api.py
```
> Check the code for more details, it is well documented


* GET AND POST requests are supported
    * Keep in mind that GET has a limited request length and special character encoding can be tricky
* Input Field
    * title (mandatory)
    * description
    * text
* Output
    * [news-please format](https://github.com/fhamborg/news-please/blob/master/newsplease/examples/sample.json)


## Learn_Weights
Learn_Weights is running the extractor with different weights.
The best candidate is compared with the best annotation to get a score.
The calculated score, document id and the used weights are saved per question under ./results.

Because of the combined_scorer, each document is evaluated in each step. 
This can lead to entries with the same weights, but with different scores.


# Giveme5W Enhancer
This extension can perform further feature extraction and selection. Install Giveme5_enhancer to use this features.


## AIDA
- OSX
    - brew install postgres
    - brew services start postgresql
- createuser postgres -s
- psql CREATE DATABASE AIDA;
- bzcat [AIDA_entity_repository_2014-01-02v7.sql.bz2](http://resources.mpi-inf.mpg.de/yago-naga/aida/download/entity-repository/) | psql aida

> - Warning database dump has 26GB
  - Import takes up to 24h and around 100 GB disc space
  - Drop the database, if you have to restart import

Use environment_enhancer.py to startup CoreNLP and AIDA together.

## Heideltime
[Heideltime](https://github.com/HeidelTime/heideltime) works out of the box with the 'Giveme5W-runtime-resources'.
This enhancement parse further the "when" answers to get precise time definitions.


# Giveme5W-runtime-resources
Giveme5W expects all libraries to be located in the same directory and next to the Giveme5W folder.


You can change this with:
```shell
Config.get()['Giveme5W-runtime-resources'] = './../Giveme5W-runtime-resources'
```
# License
The project is licensed under the Apache License 2.0. Make sure that you use Giveme5W in compliance with applicable law. Copyright 2016 The Giveme5W team
