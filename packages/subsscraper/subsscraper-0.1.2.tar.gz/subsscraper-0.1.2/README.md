SubScraper
---------

Run command for generate urls
```commandline
search
search search.cnt=2 # for 2 urls
```

Run command for subscrape urls
```commandline
subscrape
```

Default configs
```commandline
search:
  output_folder: data
  result_file: urls.txt
  cnt: 10
  query: машинное обучение лекции таймкоды

scraper:
  output_folder: ${search.output_folder}/dataset
```

