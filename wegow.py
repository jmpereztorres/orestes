# gcloud functions deploy wegow --project orestes --region europe-west1 --runtime python37 --trigger-http
import json
import urllib.request
import time
from functional import seq
from collections import namedtuple
import flask
from google.cloud import firestore

db = firestore.Client()
replaceTag = "#####"
ticketsUrl = "https://www.wegow.com/api/ticket-types/?event="
eventsUrl = "https://www.wegow.com/api/search/events/?query="+replaceTag+"&page_size=5&page=1&web=false"

# pojos
class TicketType:
	title = ""
	description = ""
	price = 0
	currency = ""
	commission = 0
	available = 0

class Event:
	numType = 0
	ticketTypes = []
	
class Execution:
	userAgent = ""
	functionExecutionId = ""
	city = ""
	citylatlong = ""
	country = ""
	userIp = ""
	event = ""
	location = ""

# timing decorator
def timing(f):
	def wrap(*args):
		time1 = time.time()
		ret = f(*args)
		time2 = time.time()
		print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))
		
		return ret
	return wrap

# utils
def jsonify(self): return json.dumps(self, default=lambda o: o.__dict__)
def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
def dict_from_class(cls): return dict((key, value) for (key, value) in cls.__dict__.items())
def formatUrl(string): return str.replace(string, " ", "%20")
	
def parseTickets(tickets):
	myEvent = Event()
	
	if("ticket_types" in tickets):
		myEvent.ticketTypes = seq(tickets["ticket_types"])\
			.filter(lambda x: x["enabled"])\
			.map(str)\
			.map(json.dumps)\
			.list()
			
			#.map(print) \
			#.map(str) \
			
		myEvent.numType = len(myEvent.ticketTypes)
	
	return myEvent

# printers
def printTicketType(ticketType):
	if(ticketType.available == 0):
		print("NO QUEDAN ENTRADAS "+ ticketType.title+" a "+str(ticketType.price)+"(+ "+str(ticketType.commission)+") "+ticketType.currency)
	else:
		print("Quedan "+str(ticketType.available)+ " " +ticketType.title+": "+str(ticketType.price)+"(+ "+str(ticketType.commission)+") "+ticketType.currency)

def printEvent(event): seq(event.ticketTypes).for_each(printTicketType)

@timing
def getFromUrl(url):
	request = urllib.request.Request(formatUrl(url))
	response = urllib.request.urlopen(request)
	data_content = response.read().decode('utf-8')
	return json.loads(data_content)

def findEventId(nombre, city):
	eventSearchUrl = str.replace(eventsUrl,replaceTag, nombre+" "+city)
	eventList = getFromUrl(eventSearchUrl)

	events = seq(eventList["events"]).filter(lambda x: (str.upper(x["city"]["name"]) == str.upper(city)) & (str.upper(x["title"]).find(str.upper(nombre))>-1))
	
	if(not events):
		return None
	else: 
		return str(events.first()["id"])

def storeRequestMetadata(request):
	body = request.get_json()
	headers = request.headers
		
	execution = Execution()
	if "User-Agent" in headers:
		execution.userAgent = headers["User-Agent"]
		
	if "Function-Execution-Id" in headers:
		execution.functionExecutionId = headers["Function-Execution-Id"]
	
	if "X-Appengine-Country" in headers:
		execution.country = headers["X-Appengine-Country"]
	
	if "X-Appengine-City" in headers:
		execution.city = headers["X-Appengine-City"]
	
	if "X-Appengine-Citylatlong" in headers:
		execution.citylatlong = headers["X-Appengine-Citylatlong"]
	
	if "X-Appengine-User-Ip" in headers:
		execution.userIp = headers["X-Appengine-User-Ip"]
	
	execution.event = body.get("eventName")
	execution.location = body.get("city")
	
	db.collection(u'executions').add(dict_from_class(execution))

#main
def wegow(request):
	storeRequestMetadata(request)

	request_json = request.get_json()
	#request_json = request
	
	if "eventName" not in request_json:
		raise ValueError("eventName field is mandatory")
		
	if "city" not in request_json:
		raise ValueError("city field is mandatory")
	
	eventName = request_json.get("eventName")
	city = request_json.get("city")
    
	if(eventName is None or city is None):
		return flask.make_response("KO - Missing fields", 500)
	else:
		# get event id
		eventId = findEventId(eventName, city)
		parsedTickets = []
		# get tickets from its id
		
		if(eventId is None):
			print("EVENTO NO ENCONTRADO")
		else:
			parsedTickets = parseTickets(getFromUrl(ticketsUrl+eventId))
		
		if(not parsedTickets and not parsedTickets.ticketTypes):
			print("ENTRADAS NO DISPONIBLES EN WEGOW")
		else:
			print("ENTRADAS DISPONIBLES!!!")

		print(jsonify(parsedTickets))
		return flask.make_response(jsonify(parsedTickets), 200)
		

#request_body = {'city': 'valencia', 'eventName': 'festival de les arts'}
#wegow(request_body)