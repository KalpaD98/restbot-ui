
# from _typeshed import Self
from typing import Dict, Text, Any, List, Union
from bson import int64

from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import SlotSet
from pprint import pprint
from pymongo import MongoClient
import pymongo 
import certifi
import logging
import json
from bson.json_util import dumps

import sys
sys.path.append("/Users/rajithabandara/Desktop/MyWork/Project/FYP - Copy/formbot/actions/submodules")
import dbQuery,ontologyQuery,Utils 


import sys
# For macbook uncomment to porint to the directory file
sys.path.append("/Users/rajithabandara/Desktop/MyWork")

# For windows lap uncomment to porint to the directory file
# sys.path.append("C:/")
from owlready2 import *

# -------------------------------------------------------------------------------------------------

# Ontology file in macbook | uncomment when use in macbook
ONTOLOGY_PATH = "file:///Users/rajithabandara/Desktop/MyWork/Project/FYP - Copy/HotelOntology16.owl"

# Ontology file in windowslaptop |  uncomment when use in windows laptop & comment above
# ONTOLOGY_PATH = "file://F:/FYP - Copy/HotelOntology.owl"

knowledge=[]
hotelslist=[]
resultObj=None
hotelSearchList=[]

# ######################################################################################################################################
# Repository Codes here 
# ######################################################################################################################################

# ontology creation and managing
class OntologyRepository:

  
    # get Ontology after Ontology initialization 
    def ontologyInit(path):
        onto = get_ontology(path).load()
        print("ontology name = "+onto.name)
        return onto

    # Ontology inferencing and saving 
    def startInference(onto,save=False,start=True):
        
        if onto is not None and start == True:
            with onto:
                print("Reasoner HermiT is running on < "+onto.name+" >")
                logging.info("ontology < "+onto.name+" > Reasoner Starting....")
                sync_reasoner()
            if save == True:
                onto.save("infered","owl")
                print(onto.name+" is saved...!")
                logging.info("ontology < "+ontology.name+" > SAVED")
    # Run on starting action server 
    ontology = ontologyInit(ONTOLOGY_PATH)
    logging.info("ontology < "+ontology.name+" > initialized on starting Action Server")
    startInference(ontology)

# mongoDB connection establishment and managing
class DatabaseRepository:
    
    # logging.info("Initiating Database connection...")
    # client = MongoClient("mongodb+srv://deveoloper:admin@cluster0.fwege.mongodb.net/hotel_db?retryWrites=true&w=majority")
    # db=client.hotel_db

    # Sample Query | Issue in the data set  not getting the Star values as Integers but getting as Strings
    # fiveStarHotels = db.Hotels.find_one({'starRate': 2})
    # pprint(fiveStarHotels)

    def getHotelDbConnection():
        logging.info("Initiating Hotel Database connection...")
        
        # old connection without food records
        # client = MongoClient("mongodb+srv://deveoloper:admin@cluster0.fwege.mongodb.net/hotel_db?retryWrites=true&w=majority")
        
        # new connection in 95Rajithalbandara@gmail.com account
        # client = MongoClient("mongodb+srv://dev:admin@cluster0.9xdgc.mongodb.net/hotel_db?retryWrites=true&w=majority")

        #   new connection in 95Rajithalbandara@gmail.com account  with SSL certification flags 
        client = pymongo.MongoClient("mongodb+srv://dev:admin@cluster0.9xdgc.mongodb.net/hotel_dbV2?retryWrites=true&w=majority",tlsCAFile=certifi.where())
        db = client.hotel_dbV2
        db=client.hotel_dbV2
        print(client.list_database_names())
        return db
    


# ######################################################################################################################################
# Form validations and slot accessing codes goes here 
# ######################################################################################################################################

class ValidateRestaurantForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_restaurant_form"

    @staticmethod
    def cuisine_db() -> List[Text]:
        """Database of supported cuisines."""

        return [
            "caribbean",
            "chinese",
            "french",
            "greek",
            "indian",
            "italian",
            "mexican",
        ]

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_cuisine(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if value.lower() in self.cuisine_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"cuisine": value}
        else:
            dispatcher.utter_message(response="utter_wrong_cuisine")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"cuisine": None}

    def validate_num_people(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""

        if self.is_int(value) and int(value) > 0:
            return {"num_people": value}
        else:
            dispatcher.utter_message(response="utter_wrong_num_people")
            # validation failed, set slot to None
            return {"num_people": None}

    def validate_outdoor_seating(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate outdoor_seating value."""

        if isinstance(value, str):
            if "out" in value:
                # convert "out..." to True
                return {"outdoor_seating": True}
            elif "in" in value:
                # convert "in..." to False
                return {"outdoor_seating": False}
            else:
                dispatcher.utter_message(response="utter_wrong_outdoor_seating")
                # validation failed, set slot to None
                return {"outdoor_seating": None}

        else:
            # affirm/deny was picked up as True/False by the from_intent mapping
            return {"outdoor_seating": value}


# ######################################################################################################################################
# Custom actions goes here 
# ######################################################################################################################################

#testing Action class  works on saying Hi to bot
class Testing(Action):

    def name(self) -> Text:
        return "action_testing"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text = "Hi, User this is testing action response!")
        
        # printing the preset slot value from the First executed action class SlotService
        print("Slots pre set check >>>> "+str(tracker.get_slot("cuisine")))
        print("Slots pre set check >>>> "+str(tracker.get_slot("num_people")))

        print( tracker.sender_id)
        
        # calling Ontology repo methods
        # ontology = OntologyRepository.ontologyInit(ONTOLOGY_PATH)
        # OntologyRepository.startInference(ontology,True)


        # this is to the chat widget which is NOT in React
        # dataJson ={
        #         "payload":"quickReplies",
        #            "data":[{
        #                 "paylaod":"type",
        #                 "title":"nice to meet you"
        #             }]
                        
        #         }
        # this is to the chat widget which is NOT in React
        # dataJson2 ={
        #         "payload":"cardsCarousel",
        #            "data":[{
        #                 "name":"hotel 1",
        #                 "ratings":100,
        #                 "image":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg"
        #             },{
        #                 "name":"hotel 2",
        #                 "ratings":100,
        #                 "image":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg"
        #             },{
        #                 "name":"hotel 3",
        #                 "ratings":100,
        #                 "image":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg"
        #             },{
        #                 "name":"hotel 1",
        #                 "ratings":100,
        #                 "image":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg"
        #             }]         
        #         }

        # this is to the chat widget which is  in React
        # dispatcher.utter_message(json_message = dataJson2)
        # dispatcher.utter_message(image = "https://i.imgur.com/nGF1K8f.jpg")


        # dispatcher.utter_message(component={"name":"hi"})
        # dispatcher.utter_message(text= 'This is a Dummy Component!')
        
        # dispatcher.utter_message(text="Hii new ", quick_replies = [
        #         {"payload": "/affirm", "title": "Yes"},
        #         {"payload": "/deny", "title": "No"},
        #     ])
        # dispatcher.utter_message(attachment={"type":"template","payload":{"template_type":"generic","elements":[
        #     {
        #     "default_action":{"type":"web_url","url":"https://stackoverflow.com/questions/23368575/pymongo-find-and-modify/23369162"},   
        #     "image_url":"https://i.imgur.com/nGF1K8f.jpg",
        #     "title":"title1",
        #     "subtitle":"subtitle1",
        #     "buttons":[{"url":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg","title":"Tittletemp"},
        #                 {"url":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg","title":"Tittletemp"},
        #                ]
        #     },
        #     {
        #     "default_action":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg",   
        #     "image_url":"https://i.imgur.com/nGF1K8f.jpg",
        #     "title":"title1",
        #     "subtitle":"subtitle1",
        #     "buttons":[{"url":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg","title":"Tittletemp"},
        #                 {"url":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg","title":"Tittletemp"},
        #                ]
        #     },
        #     {
        #     "default_action":"http://donsmaps.com/clickphotos/dolnivi200x100.jpg",   
        #     "image_url":"https://i.imgur.com/nGF1K8f.jpg",
        #     "title":"title1",
        #     "subtitle":"subtitle1",
        #     "buttons":[{"url":"https://stackoverflow.com/questions/23368575/pymongo-find-and-modify/23369162","title":"Tittletemp","type":"web_url"},
        #                 {"url":"https://stackoverflow.com/questions/23368575/pymongo-find-and-modify/23369162","title":"Tittletemp","type":"web_url"},
        #                ]
        #     }
        # ]}})


        return []

class SearchOntology(Action):
    def name(self) -> Text:
        return "action_search_ontology"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        logging.info("action [SearchOntology class]: inside action_search_ontology")

        dispatcher.utter_message(text="Let me see.... ")
       


        location =  tracker.get_slot("location_activity")
        cuisine = tracker.get_slot("cuisine")

        ontology =  OntologyRepository.ontology
        hotelDbConnection = DatabaseRepository.getHotelDbConnection()

        
        global hotelslist
        criteria = {}

        if location is not None and not '':
            criteria["location"] = location
        
        if cuisine is not None and not '':
            criteria["cuisine"] =  cuisine
        
        criteriaBasedHotelList = ontologyQuery.getInstancesfromOntology(criteria,ontology)        
        criteriaBasedHotelIdList = ontologyQuery.getHotelIds(criteriaBasedHotelList)
        criteriaBasedHotelDocuments = dbQuery.getHotels(criteriaBasedHotelIdList,hotelDbConnection)
        hotelSearchList = criteriaBasedHotelDocuments


        # setting the global List making the searched list available for action_service_manager functions
        hotelslist = criteriaBasedHotelDocuments


# ---------------------------- USE WITH THE REACT WIDGET ELSE COMMENT THIS SECTION ------------------------------------

        response= Utils.responseGenerator(criteriaBasedHotelDocuments)

        dispatcher.utter_message(attachment=response)
        dispatcher.utter_message(text="do you want me to book a hotel?", quick_replies = [
                 {"payload": "/request_hotel_selectForm_intent", "title": "Yes"},
                {"payload": "/stop", "title": "No"}, ])

# ---------------------------- REACT RESPONSE SECTION ENDS -------------------------------------------------------------


# ---------------------------- USE WITH SHELL DEMO ELSE COMMENT OUT ----------------------------------------------------

        # responseShell= Utils.responseGenerator_Shell(criteriaBasedHotelDocuments)
        # dispatcher.utter_message(text=responseShell)
        # dispatcher.utter_message(text="do you want me to book a hotel?", buttons = [
        #     {"payload": "/request_hotel_selectForm_intent", "title": "Yes"},
        #     {"payload": "/stop", "title": "No"}, ])

# ---------------------------- SHELL RESPONSE SECTION ENDS --------------------------------------------------------------        


#  search food category when user inputs tastes or category
class CuisineSearchOntology(Action):
    def name(self) -> Text:
        return "action_cuisine_search_ontology"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        logging.info("action [CuisineSearchOntology class]: inside action_cuisine_search_ontology")

    
        criteria = {}

        cuisine = tracker.get_slot("cuisine")
        
        # > unmached tastes types ---- DONE
        # cuisine = ["bitter","spicy"]
        # > Chinese matching taste combination ---- DONE
        # cuisine = ["sour","spicy"]
        # > category  and category test ---- DONE
        # cuisine = ["chinese","Italian"]
        # > category and taste test ---- DONE 
        # cuisine = ["chinese","spicy"]
        # > single taste test ---- DONE
        # cuisine = ["spicy"]
        #  > single category test ---- DONE
        # cuisine = ["chinese"]
        #  > testing for 3 and 4 casses ---- NOT DONE 
        # cuisine = ["bitter","spicy","sour"]
        

        ontology =  OntologyRepository.ontology
        hotelDbConnection = DatabaseRepository.getHotelDbConnection()

        if cuisine is not None and not '':
            criteria["cuisine"] =  cuisine
            print(criteria)

        global resultObj    
        resultObj = ontologyQuery.cuisineSuggestionsFromOntology(criteria,ontology)
        print(str(resultObj))
        utterance = resultObj.get("utterance")


        dispatcher.utter_message(text=utterance)

        dispatcher.utter_message(text="Do you want me to find a perfect hotel that can you can fit in for a dine ? ", 
                                 quick_replies = [{"payload": "/request_hotel", "title": "Yes"},{"payload": "/stop", "title": "No"}])



# Search hotesl from the hotel form data
class HotelSearch(Action):
    def name(self) -> Text:
        return "action_search_hotels"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        logging.info("action_search_hotels")
        area =tracker.get_slot("area")
        people_count=tracker.get_slot("num_people")
        # room_count=tracker.get_slot("num_room")

       
        hotelDB = DatabaseRepository.getHotelDbConnection()

        
        # print(" >>>>>>>>>>>>> "+str(resultObj))

        global hotelSearchList
       
        if area is not None and people_count is not None and resultObj is not None:
            finalCuisineCategorySet = resultObj.get("finalCuisineCategorySet")
            print(finalCuisineCategorySet)
           
            tempList = []
            for i in finalCuisineCategorySet:
                queryObj = {'area': area, 'available_space' : { '$gte' : int(people_count) }, "foods.category":i.lower() }
                x = dbQuery.getMatchingHotelList(queryObj, hotelDB)
                print(x)
                tempList.append(dbQuery.getMatchingHotelList(queryObj, hotelDB))

            print("tempList"+str(tempList))
            tempList =  Utils.getTotalElementsinList(tempList)
            hotelDocuments = list(tempList)
            hotelDocuments = Utils.removeDuplicateDictionariesOnHotel_id(hotelDocuments)
            hotelSearchList = hotelDocuments

        elif area is not None and people_count is not None:
            print("people_count"+str(people_count))
            queryObj = {'area': area, 'available_space' : { '$gte' : int(people_count) } }
            hotelDocuments= dbQuery.getMatchingHotelList(queryObj, hotelDB)
            print("hotelDocuments"+hotelDocuments)

            # global hotelSearchList
            hotelSearchList = hotelDocuments
            

        


# ---------------------------- USE WITH THE REACT WIDGET ELSE COMMENT THIS SECTION ------------------------------------
            
        response= Utils.responseGenerator(hotelDocuments)
            
        dispatcher.utter_message(attachment=response)
        dispatcher.utter_message(text="do you want me to book a hotel?", quick_replies = [
                {"payload": "/request_hotel_selectForm_intent", "title": "Yes"},
                {"payload": "/stop", "title": "No"}, ])

# ---------------------------- REACT RESPONSE SECTION ENDS -------------------------------------------------------------

# ---------------------------- USE WITH SHELL DEMO ELSE COMMENT OUT ----------------------------------------------------

            # responseShell= Utils.responseGenerator_Shell(hotelDocuments)
            # dispatcher.utter_message(text=responseShell)
            # dispatcher.utter_message(text="do you want me to book a hotel?", buttons = [
            #     {"payload": "/request_hotel_selectForm_intent", "title": "Yes"},
            #     {"payload": "/deny", "title": "No"}, ])

# ---------------------------- SHELL RESPONSE SECTION ENDS --------------------------------------------------------------
   

    
        

# class which the services like hotel booking managed EX: story direct hotel booking and suggestion booking stories crossing this to places bookimg 
class ServiceManagement(Action):
    def name(self) -> Text:
        return "action_service_management"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:            
        logging.info("action_service_management")



        print(hotelslist)
        result = []

        # request suggestion story crossing this logic layer to handle the case where the hotel select first goes and get the selected hotel area to set in the 
        # area slot which getting checked when hotel booking form activated.
        if tracker.get_slot("booking_place") is not None and tracker.get_slot("area") is None and tracker.get_slot("num_people") is None:
            
            hotelName = tracker.get_slot("booking_place")
            logging.info("action_service_management : Booking_place slot set ")
            selectedHotelDocument = Utils.searchDocument(hotelslist,"name",hotelName)
            
            if selectedHotelDocument is not None:
                logging.info("action_service_management : setting area information to the slot area from the selected hotel")
                result.append(SlotSet("area",selectedHotelDocument.get("area")))
                
                dispatcher.utter_message(text="do you want me to book the hotel "+hotelName+" ?", buttons = [
                {"payload": "/request_hotel", "title": "Yes"},
                {"payload": "/deny", "title": "No"}, ])

        #  direct booking story crossing this logic layer and book the hotel
        if tracker.get_slot("booking_place") is not None and tracker.get_slot("area") is not None and tracker.get_slot("num_people") is not None:

            logging.info("action_service_management : Direct hotel booking story slots[booking_place,area,num_room] found")
            
            hotelName = tracker.get_slot("booking_place")
            print(hotelName)
            area =tracker.get_slot("area")
            num_people=tracker.get_slot("num_people")
            
            hotelDB= DatabaseRepository.getHotelDbConnection()

            if area is not None and num_people is not None:
           

                queryObj = {'area': area, 'available_space' : { '$gte' : int(num_people) } }
                hotelslistTemp= dbQuery.getMatchingHotelList(queryObj, hotelDB)
               

                if hotelslistTemp:
                    selectedHotel = Utils.searchDocument(hotelslistTemp,"name",hotelName)

                    if selectedHotel is None:
                        logging.info("ServiceManagement : Hotel booking failed due to not enough available rooms")
                        dispatcher.utter_message(text="Bad Luck...! The hotel "+hotelName+" can not accomadate the space for your booking...! ")
                
                    if selectedHotel:
                        dbQuery.hotelBookingProcess(selectedHotel,hotelName,num_people, hotelDB)

        return result    


class Menu(Action):
   
    def name(self) -> Text:
        return "action_getresturantmenu"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:            
        logging.info( "action_getresturantmenu")

        hotelName= tracker.get_slot("booking_place")
        num_people= tracker.get_slot("num_people")
        area = tracker.get_slot("area")

        if hotelName is not None:
            hotelDB= DatabaseRepository.getHotelDbConnection()
            print("in the action")

            print(hotelName)

            # queryObj = {'name':hotelName ,'area': area, 'available_space' : { '$gte' : int(num_people) } }
            # hotelslistTemp= dbQuery.getMatchingHotelList(queryObj, hotelDB)
               

            # if hotelslistTemp:
            selectedHotelDocument = Utils.searchDocument(hotelSearchList,"name",hotelName)

            if selectedHotelDocument is not None:
                menuUrl = selectedHotelDocument.get("menu")
                logging.info("action_getresturantmenu : selectedHotelDocument found in the hotelSearchList - From Filtered results" )
                
            else:
                queryObj = {'name':hotelName ,'area': area, 'available_space' : { '$gte' : int(num_people) } }
                hotelslistTemp= dbQuery.getMatchingHotelList(queryObj, hotelDB)
                selectedHotelDocument = Utils.searchDocument(hotelslistTemp,"name",hotelName)    
                
                if selectedHotelDocument is None:
                    logging.error("action_getresturantmenu :  selectedHotelDocument NOT FOUND in the DB")
                
                logging.info("action_getresturantmenu : selectedHotelDocument FOUND in the DB")
                menuUrl = selectedHotelDocument.get("menu")
            
            print(menuUrl)
            
            
            dispatcher.utter_message(text= "tadaa...!!!")
            dispatcher.utter_message(image= menuUrl)

        else: 
            dispatcher.utter_message(text=" you haven't selected a resturant yet. Please select a resturant First")

        return [] 
    
# to check the recomendations Using a Behaviour Tracker
class SlotService(Action):

    def name(self) -> Text:
        return "check_recomendations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        result =[]
        # cuisin_value = 'trans'
        num_people_value = 8

        print("Check Recomendations executed...")
        dispatcher.utter_message(text = "Hi, User check_recomendations executed!")

        # get the slot and check if null
        # if tracker.get_slot("cuisine") is None:
        #     # Not working withoout returning the slotset
        #     result.append(SlotSet("cuisine", cuisin_value))
        #     print("cuisine SlotSet executed...")
        #     dispatcher.utter_message(text = "Hi, User cuisine SlotSet executed!")
        
        # if tracker.get_slot("num_people") is None:
        #     result.append(SlotSet("num_people", num_people_value))
        #     print("num_people SlotSet executed...")
        #     dispatcher.utter_message(text = "Hi, User num_people SlotSet executed!")

        # Not working withoout returning the slotset

        

        # it is a must to return slotset values 
        return result





