# Wegow events ticket
An parser application to get event tickets prices from the wegow platform

To search events use the json below:
```
{
   eventName: "festival de les arts",
   city: "valencia
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