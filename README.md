# bioschemas-scraper
Web scrapper to harverst Data items using bioschemas specifications markup. This project is based in Scrapy, a Python library to crawl web resources.


## Dependencies
You will need **pip** to install the script requirements, [over here](https://pip.pypa.io/en/stable/installing/) you will find documentation about installing **pip** in your OS. The safer way to get your requirements installed without affecting any other Python project you have is using [**virtualenv**](http://docs.python-guide.org/en/latest/dev/virtualenvs/). You will also need an Elastic Search instance running so you can save the crawled records.

## Installation
```{r, engine='bash', count_lines}
git clone https://github.com/BioSchemas/bioschemas-scraper.git
cd bioschemas-scraper
viartualenv .venv
source activate .venv/bin/activate
pip install -r requirements.txt
```

After you finish the script execution you will need to deactivate your virtual environment:
```{r, engine='bash', count_lines}
deactivate
```

## Configuration

In order to configure the Elastic Search instance information in the scraper you need to modify the last lines in the file bioschemas_scraper/settings.py. This scraper is set to crawl Tess Events web site by default. If you want to generate a new spider for a different web site please take a look of bioschemas_scraper/spiders/bioschemas_spider_xml.py. If you want to add aditional processing to the crawled records you will need to check the pipelines defined in bioschemas_scraper/pipelines, for now there is only one pipeline that take every crawled Bioschemas object and the it validate it agains the Bioschemas Event specificication available as a JSON Schema file at bioschemas_scraper/utils/schemas/Event.json the validation logic is available at bioschemas_scraper/utils/validators.py.

## Running


## Supported formats
* Microdata

