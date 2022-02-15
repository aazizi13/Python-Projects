
# importing required libraries
from geopy.geocoders import Nominatim
from colorama import Fore
from colorama import Style
from colorama import Back
import math
import csv
import os
import sys


#creating the Address class
class Address:
    address=''
    cities=''
    Longitude=0
    Latitude=0
    radius=0

    #declaring all the variables used inside the class
    def __init__(self,address,cities,Longitude,Latitude,radius):
        self.address=address
        self.cities=cities
        self.Longitude=Longitude
        self.Latitude=Latitude
        self.radius=radius

    #creating a method to get address from the user and calculate the latitude and longitude for the address
    @classmethod
    def get_address(self):
        self.address=input('\nPlease enter your address: (e.g. 1234 Street Address, Mountain View, CA 94043): ')
       
        #finding the latitude and longitude for the entered address
        #if there i no latitude and longitude for the address 
        #then displaying a message and redirect to the start of the program
        try:
            geoloc=Nominatim(user_agent="restaurant_finder")
            loc=geoloc.geocode(self.address)
            self.Longitude=loc.longitude
            self.Latitude=loc.latitude
        
        except:
            print('\nWe couldn\'t find the latitude and the longitude coordinates for your address.\n')
            exit()

    @classmethod
    def get_cities(self):
        self.cities=input('\nPlease enter the cities where you want to find a restaurant separated by comma (e.g. Mountain View, Sunnyvale, Cupertino): ')

    #creating a method to filter restuarants according to the given addres
    @classmethod
    def address_filter(self):
        global restaurant_names,restaurant_data

        #earth's radius for calculating distance
        earth_radius=6371

        #to store filtered names
        return_list=[]
        try:
            distance_pref=int(input('\nPlease enter the search area radius in miles (5 or 10): '))
            self.radius=distance_pref
            if distance_pref not in [5,10]:
                print('\n[X] Please enter 5 or 10.')
                return Address.address_filter()
        except:
            print('\n[X] Please enter 5 or 10')
            return Address.address_filter()

        #calculating longitude and latitude
        #and filtering the restuarants
        for rest in restaurant_names:
            longitude_rest=restaurant_data[rest]['longitude']
            latitude_rest=restaurant_data[rest]['latitude']

            delta_longitude=math.radians(longitude_rest)-math.radians(self.Longitude)
            delta_latitude=math.radians(latitude_rest)-math.radians(self.Latitude)

            var1=math.sin(delta_latitude/ 2)**2+math.cos(self.Latitude) *math.cos(latitude_rest)*math.sin(delta_longitude / 2)**2
            var2=2*math.atan2(math.sqrt(var1), math.sqrt(1 - var1))
            distance=earth_radius*var2*0.62
            if distance<=distance_pref:
                return_list.append(rest) 

        return return_list

#creating a class to get diet preferences from the user
class Dietary_Preference:
    #declaring all the variables used inside the class
    diet = ''

    def __init__(self,diet):
        self.diet=diet

    #creating a method to get user diet preference
    @classmethod
    def get_dietary(self):
        print('\nDietary Preferences List')
        print('1 - Vegetarian')
        print('2 - Vegan')
        print('3 - Neither')
        try:
            diet_num=int(input('\nPlease enter your dietary preferences (1/2/3): '))
            if diet_num not in [1,2,3]:
                print('\n[X] Please enter 1, 2 or 3.')
                return Dietary_Preference.get_dietary()
        except:
            print('\n[X] Please enter a valid number.')
            return Dietary_Preference.get_dietary()

        if diet_num==1:
            self.diet='Vegetarian'
        elif diet_num==2:
            self.diet='Vegan'
        elif diet_num==3:
            self.diet='Neither'
        else:
            print('\n[X] You have entered an invalid preference.')
            return Dietary_Preference.get_dietary()
    
    #creating a method to filter restuarants
    @classmethod
    def diet_filter(self):
        global restaurant_names,restaurant_data
        return_list=[]

        for rest in restaurant_names:
            if self.diet==restaurant_data[rest]['diet']:
                return_list.append(rest)
        return return_list

#creating a class to get budget preferences from the user 
class Budget:
    #declaring all the variables used inside the class
    budget = ''

    def __init__(self,budget):
        self.budget=budget

    #creating method to get user's budget preference
    @classmethod
    def get_budget(self):
        self.budget=input('\nPlease enter your budget preferences ($ ranking system): ')
        if self.budget not in ['$','$$','$$$','$$$$','$$$$$']:
            print('\n[X] Please enter it in $ ranking system (e.g. $$$).')
            return Budget.get_budget()

    #creating a method to filter restuarants
    @classmethod
    def budget_filter(self):
        global restaurant_names,restaurant_data
        return_list=[]
        for rest in restaurant_names:
            if self.budget==restaurant_data[rest]['budget']:
                return_list.append(rest)
        return return_list

#creating a class to get rating preferences from the user
class Rating:
    #declaring all the variables used inside the class
    rating = 0

    def __init__(self,rating):
        self.rating=rating

    #creating method to get user's rating preference
    @classmethod
    def get_rating(self):
        try:
            self.rating=int(input('\nPlease enter your rating preferences (1-5 scale): '))
            if self.rating not in [1,2,3,4,5]:
                print('\n[X] Please enter a valid number.')
                return Rating.get_rating() 
        except:
            print('\n[X] Please enter a valid number.')
            return Rating.get_rating()
    
    #creating a method to filter restuarants
    @classmethod
    def rating_filter(self):
        global restaurant_names,restaurant_data
        return_list=[]
        for rest in restaurant_names:
            if self.rating==restaurant_data[rest]['rating']:
                return_list.append(rest)
        return return_list

#creating a class to get food type preferences from the user
class Food_type:
    #declaring all the variables used inside the class
    food_type = ''

    def __init__(self,food_type):
        self.food_type=food_type

    #creating method to get user's food type preference
    @classmethod
    def get_type(self):
        print('\nFood Type Preferences List')
        print('1 - Asian')
        print('2 - Mexican')
        print('3 - Burgers')
        print('4 - Italian')
        print('5 - Greek')
        print('6 - fast food')

        try:
            type_num=int(input('\nPlease enter your food type preference (1/2/3/4/5/6): '))
            if type_num not in [1,2,3,4,5,6]:
                print('\n[X] Please enter a valid number.')
                return Food_type.get_type()
        except:
            print('\n[X] Please enter a valid number.')
            return Food_type.get_type()

        if type_num==1:
            self.food_type='Asian'
        elif type_num==2:
            self.food_type='Mexican'
        elif type_num==3:
            self.food_type='Burgers'
        elif type_num==4:
            self.food_type='Italian'
        elif type_num==5:
            self.food_type='Greek'
        elif type_num==6:
            self.food_type='fast food'
        else:
            print('\nYou have entered an invalid preference.')
            return Food_type.get_type()
    
    #creating a method to filter restuarants
    @classmethod
    def type_filter(self):
        global restaurant_names,restaurant_data
        return_list=[]
        for rest in restaurant_names:
            if self.food_type==restaurant_data[rest]['type']:
                return_list.append(rest)
        return return_list

#creating a class to find recommendations for the user
class Recommendations:
    user_address=Address
    user_dietary_pref=Dietary_Preference
    user_budget=Budget
    user_rating_pref=Rating
    user_food_pref=Food_type

    @classmethod
    def get_user_address(self):
        self.user_address.get_address()

    @classmethod
    def get_search_cities(self):
        self.user_address.get_cities()

    @classmethod
    def get_search_radius(self):
        self.filtered_address=self.user_address.address_filter()

    @classmethod
    def get_user_dietary_pref(self):
        self.user_dietary_pref.get_dietary()
        self.filtered_diets=self.user_dietary_pref.diet_filter()

    @classmethod
    def get_user_budget(self):
        self.user_budget.get_budget()
        self.filtered_budgets=self.user_budget.budget_filter()

    @classmethod
    def get_user_rating_pref(self):
        self.user_rating_pref.get_rating()
        self.filtered_rating=self.user_rating_pref.rating_filter()

    @classmethod
    def get_user_food_pref(self):
        self.user_food_pref.get_type()
        self.filtered_types=self.user_food_pref.type_filter()

    @classmethod
    def get_recommandations(self):
        return_list=[]
        for i in self.filtered_address:
            check_num=0
            if i in self.filtered_budgets:
                if i in self.filtered_diets:
                    if i in self.filtered_rating:
                        if i in self.filtered_types:
                            check_num=1

            if check_num==1:
                return_list.append(i)

        if len(return_list)==0:
            print('\nSorry. There seems to be no matches for your preferences ...')
            choice=input('\nDo you wish to try again? (Y/N): ')
            if choice in ['Y', 'y', 'Yes', 'yes']:
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif choice in ['N', 'n', 'No', 'no']:
                print('\nThank you for using our application.\n')
                exit()
            else:
                print('\nYou have entered an invalid response.')
                print('\nThank you for using our application.\n')
                exit()
        else:
            print('\nHere are our recommandations based on your preferences: ')
            for entity in return_list:
                print('+ ', entity)

            print('\n\nThank you for using our application.')
            print('------------------------------------')
            choice=input('Do you wish to go again? (Y/N): ')
            if choice in ['Y', 'y', 'Yes', 'yes']:
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif choice in ['N', 'n', 'No', 'no']:
                print('\nThank you for using our application.\n')
                exit()
            else:
                print('\nYou have entered an invalid response.')
                print('\nThank you for using our application.\n')
                exit()


if __name__ == "__main__":
    #to store fetch data from the restuarant data csv file
    restaurant_names=[]
    restaurant_data={}

    #reading csv data file and store data in created list and dictionary 
    with open('restuarant data.csv','r') as data_file:
        data = csv.reader(data_file)

        #going through each restuarant in file 
        for row in list(data)[1:]:
            rest_dict={}
            restaurant_names.append(row[0])
            rest_dict['address']=row[1]
            rest_dict['diet']=row[2]
            rest_dict['rating']=int(row[3])
            rest_dict['budget']=row[4]
            rest_dict['type']=row[5]
            rest_dict['latitude']=float(row[6])
            rest_dict['longitude']=float(row[7])
            #include analized data to the dictionary
            restaurant_data[row[0]]=rest_dict

    print('\n       ***Welcome To The Restaurant Recommender***')
    print('\n       #Disclaimer: Designed for Mountain View, CA#')

    while True:
        area=input(Fore.RED + '\nAre you located in Mountain View California? (Y/N): ')
        if area not in ['Y', 'y', 'Yes', 'yes', 'N', 'n', 'No', 'no']:
            print('\n[X] Wrong input.')
            continue            
        else:
            break
        
    if area in ['N', 'n', 'No', 'no']:
        print('\nSorry. This program is only designed for Mountain View California.\n')
        exit(0)

    user=Recommendations

    while True:
        print('\nPlease fill in your preferences:')
        print('--------------------------------')    
        print(Fore.YELLOW + '[1] - Your address: "{:s}"'.format(user.user_address.address))
        print(Fore.GREEN + '[2] - Cities to search: "{:s}"'.format(user.user_address.cities))
        print(Fore.YELLOW + '[3] - Search radius: {:d}'.format(user.user_address.radius))
        print(Fore.GREEN + '[4] - Dietary preferences: "{:s}"'.format(user.user_dietary_pref.diet))
        print(Fore.YELLOW + '[5] - Budget preferences: "{:s}"'.format(user.user_budget.budget))
        print(Fore.GREEN + '[6] - Rating preferences: {:d}'.format(user.user_rating_pref.rating))
        print(Fore.WHITE + '[7] - Food Type Preferences: "{:s}"'.format(user.user_food_pref.food_type))
        print('\n')
        print('[8] - Give me my recommendations!')
        print('[0] - Exit')

        while True:
            try:
                answer=int(input('\nPlease choose a number: '))
                if answer not in [1,2,3,4,5,6,7,8,0]:
                    print('\n[X] Wrong input.')
                    continue            
                else:
                    break
            except ValueError:
                print('\n[X] Wrong input.')
                continue

        if answer==1:
            user.get_user_address()
        elif answer==2:
            user.get_search_cities()
        elif answer==3:
            if(user.user_address.address == ''):    
                print('\n[X] You must enter your address first.')
            else:
                user.get_search_radius()
        elif answer==4:
            user.get_user_dietary_pref()
        elif answer==5:
            user.get_user_budget()
        elif answer==6:
            user.get_user_rating_pref()
        elif answer==7:
            user.get_user_food_pref()
        elif answer==8:
            if( user.user_address.address == '' or user.user_address.cities == '' 
                or user.user_address.radius == 0 or user.user_dietary_pref.diet == '' 
                or user.user_budget.budget == '' or user.user_rating_pref.rating == 0 
                or user.user_food_pref.food_type == ''):
                print('\n[X] You must fill all the preferences.')  
            else: 
                user.get_recommandations()
        elif answer==0:
            exit()
