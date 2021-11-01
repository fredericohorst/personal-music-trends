# personal-music-trends

## Nostalgia
This project started with the idea of remembering and old songs and albuns, which we used to listen but are forgetting to hear once again, because all algorithms does the same: suggest something new of age. But sometimes, *all we want is some nostalgia*.

That is why the goal of this project is to use our music history to suggest what we usually heared a lot.

## Sources
Main source of data to this project is [LastFM](http://last.fm). Other sources are being considered, such as Apple Music and Spotify. I don't use Spotify, and Apple charges 99USD/year to register an application so we can take the data through the API, so I'm focusing on LastFM. If you know how to bring data from these other sources, let me know! :)

## How to use this project

### LastFM Source Configuration
To use the LastFM API, you will need to:
1. have an account
2. register an application by applying for a key - [here](https://www.last.fm/api/account/create)
3. save your keys into a file called credentials.json inside the project folder.

The `credentials.json` file must follow this pattern:
``` 
{
    "application-name": "YOUR-APP-NAME",
    "API-key":"YOR-API-KEY",
    "Shared-secret":"YOUR-SHARED-SECRET",
    "user-name":"YOUR-USER-NAME"
} 
```

### Importing data from LastFM
Using the library lastfm you can call the function `import_historic_data` to import. The library here brings the following fields:
- artist_name
- album_name
- date_uts
- date
- track_name
- loved_track

Parameters:
- `file_path`: path of the file and/or prefix for the files name. The function will save the files in csv using as suffix the year. Must be string.
- `initial_year`: first year of the desired imported data, integer.
- `end_year`: last year of the desired imported data, integer.

## What now? 
Analyze it the way you want! You can take a look on the file `analyzing.ipynb` to see how I did it, but feel free to use it how you want :)
