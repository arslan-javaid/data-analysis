# Search Engine for word specific research

## How to get it up and running (locally)

* Clone the repository using `git clone https://github.com/arslan-javaid/data-analysis.git` ;
* Go to `data-analysis` and execute these lines:
```
cd data-analysis


pip install virtualenv
mkdir env
virtualenv env/
source env/bin/activate

pip install -r requirements.txt
```

#### Run Scrapy Server (locally)
```
cd scrapy_app
scrapyd
```