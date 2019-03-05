# web2m3c
An scrapping application based on nodejs for Google cloud functions example.
It parses the https://acelisting.in/ web in order to get show links for streaming watching.

To filter shows use the following body example in a POST request:
```
{
    filter: {
	    time: '22:30',
	    date: '20 Mar',
	    sport: 'soccer',
	    match: 'liverpool',
	    league: 'premier league'
    }
}
```

To customize the acestream url you can add your localIpDevice using the same body object as below:
```
{
    filter: {
	    time: '22:30',
	    date: '20 Mar',
	    sport: 'soccer',
	    match: 'liverpool',
	    league: 'premier league'
    },
    localIp: 'http://192.168.1.1:6879
}
```

A service response example:
```
[
   {
      "links":[
         {
            "name":"16 - SPA",
            "url":"acestream://e17daf17d71b941f82230cdc358c4ba02eed520a"
         },
         {
            "name":"7 - POR",
            "url":"acestream://857c7ab59305fdccd621b6525786fe925813568d"
         },
         {
            "name":"8 - POR",
            "url":"acestream://857c7ab59305fdccd621b6525786fe925813568d"
         }
      ],
      "time":"20:30",
      "date":"03 Mar",
      "sport":"BASKETBALL",
      "match":"BOSTON CELTICS-HOUSTON ROCKETS",
      "league":"USA NBA"
   }
]
```