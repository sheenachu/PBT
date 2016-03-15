CMSC 122 Winter 2016 Final Project

Chicagoin' Green

by Kevin Bernat, Estelle Ostro, and Sheena Chu

Project set up instructions:
    
    Use the VM image in the flashdrive. Otherwise, this should
    be sufficient:

    As described at http://askubuntu.com/questions/666933/how-to-install-python3-django-in-14-04,

    Install pip package manager:
    sudo apt-get update

    Install pip:
    sudo apt-get install python3-pip

    Install Django:
    sudo pip3 install django
    
    Modules:
        django
        json
        traceback
        io
        sys
        csv
        os
        operator
        meep (local)
        functools
        rankings (local)
        coc_data (local)
        coords_to_block (local)
        utility (local)
        quicksort (local)
        sqlite3
        pprint
        re
        bs4
        math
        urllib.parse
        requests
        random
        statistics
        numpy

    How to use the Website:

        In the Django folder, run python3 manage.py runserver in the terminal. Click on the link. This will open the website in Firefox. You will begin at the homepage. Using the navigation bar, you can go between a Neighborhood Map page,
        a Census Map page, and an About page.

        In the Neighborhood and Census Map pages, select a layer using the button in the upper right-hand corner of the map (electricity or gas) in order to visualize the neighborhoods/census blocks on the map. Hovering of a neighborhood reveals the name of the neighborhoood. Clicking on the neighborhood reveals the name of the neighborhood as well as its ranking when compared to the other neighborhoods. This can likewise be done in the Census Map page. On the Census Map page, you can input an appropriate address and return the census tract. You can even click on the "show on map?" button to get a pin show up on the map to see under which census block the address falls under.

        On the Improvements page, you can choose which device you would like to use less. The number of hours per day in which you would like to not use the device can be inputted. This returns the amount of money that would be saved per month.

Structure of Code:

    Data is collected in csv files and in sqlite3 databases. This data is then organized and analyzed and then used to generated a map of Chicago. This map of Chicago, along with the data generated in sqlite3 databases, are placed in a website which is created with Django.

Project Files:
    Note1: For each file, the following categories will be given based on how much the code is original, modified, or a direct copy:
        Direct Copy - File was unchanged from source.

        Modified - File was changed for the purpose of the project,
        but the original structure is maintained.

        Original - File was written independently or heavily modified from source. 

    Note2: Code that was generated but ended up not being used for the final project will be labelled as "Legacy Code". Code that is needed for the final project will not have this label.       

    Data Files (Kevin Bernat):

        CSV Files:

            census_energy_data_elec.csv: Electricity usage based on     census block.

            census_energy_Data_therms.csv: Gas usage based on census block.

            Energy_Usage_2010.csv: Imported and complete data from City of Chicago website (both electricity and gas).

            Energy_Usage_2010_elec.csv: Electricity data from City of Chicago website.

            Energy_Usage_2010_therms.csv: Gas data from City of Chicago website.

            Energy_Usage_2010_mini.csv: Used to test Python files.

            standby.csv: Data on the standby power that certain electrical appliances use under different conditions.

            gas_improvements.csv: Data on the energy and money saved if certain devices are used less. The information 
            was gotten from the following website: 
            http://www.peoplesgasdelivery.com/home/gas_calculator.aspx

        Sqlite3 Databases:

            coc.db: Legacy Code - Data from City of Chicago Website (Energy Usage 2010). This was created by using "Energy_Usage_2010.csv" and using the following command-line prompt commands:
            .separator "," .import Energy_Usage_2010.csv electricity/therms

            improvements.db: Database with two tables. One called standby which has information on standby power for electrical devices. The other is called therms_improvements which has information on gas energy and money saved for certain appliances. This was created by using "standby.csv" and "gas_improvements.csv" and .separator "," .import csv_filename table in the sqlite3 command line.

        Python Files:

            coc_data.py: Original - Organizes data based on census block and neighborhoods (community areas)

            coords_to_block.py: Original - Converts an address to a census block.

            nrel_data.py: Legacy Code - Modified - Gets information about alternative fuel stations in Chicago. The distance function was retrieved from online (Direct Copy), but the rest is original. This was not implemented into the final build of the website.

            nrel_pv_data.py: Legacy Code - Original - Gets information on energy generated by placing photovoltaic devices at a given location. This works, but was not put in the final build.

            nrel_rates.py: Legacy Code - Original - Gives the electricity rates in $/kwh. This works, but not put in the final build.

            quicksort.py: Modified - Sorts a list from least to greatest using a median of three quicksort algorithm.

            rankings.py: Original - Ranks the neighborhoods or census block based on energy efficiency for any month or for the total for that year. Only the totals were implemented into the final project.

            standby_crawler.py: Legacy Code - Original - Crawls the Standby Power website. This is the website:
            http://standby.lbl.gov/summary-table.html
            While this file works, it was not implemented into the final build.

            utility.py: Direct Copy from pa2-Used to get and read requests from urls.

            All crawling files were of course influenced by the work
            done in pa2.

        
    Django Files:

    Improvements.py (Legacy): Modified - Build search function

    meep.py: Modified - creates output for improvements search


    res (Sheena Chu):
        device.csv - List of devices


    Search Files (Sheena Chu):

        Python Files:
            urls.py: Modified - url paths for this app

            views.py: Modified - Creates a Django form which returns
                the amount of money saved per month based on device and
                hours reduced

        Static:
            background.jpg - Image for website background

            search.css - Modified - css for search app pages

        Templates:

            Search:
                about.html: Original - Displays the about page
                base.html: Original - Base html for all html pages 
                index.html: Original - Displays the home page
                search.html: Original  - Displays the improvements page




    Website (Sheena Chu):
        Python Files:
            settings.py: Modified - settings for Django website

            urls.py: Modified - has url paths for the website

    
    Map Files (Estelle Ostro):

        Python Files:

            rank_neighborhoods.py: Original - Used to add ranking info to 
            geojson properties.

            map/views.py: Modified - Creates a Django form which retrieves 
            the census tract of a submitted address.

            search/views.py: (with Sheena Chu) Modified - Creates a Django form which retrieves the amount saved/month for a given device 
            and number of hours/day

        GEOJSON Files:

            Boundaries - Community Areas (current).geojson: Community area
            boundaries from City of Chicago website

            Boundaries - Neighborhoods.geojson: Neighborhood boundaries from 
            City of Chicago website

            censusRanked.geojson: Census tract boundaries with ranking 
            information added.

            chicagoCensus.geojson: Census tract boundaries from City of 
            Chicago website.

            ranked_neighborhoods2.geojson: Community Area boundaries with
            ranking information added.

        HTML Files:

            energymap.html: (Legacy) Modified - used to experiment with mapmaking techniques

            map/census.html: Modified - To display a choropleth map of census 
            tracts with a census tract lookup by address function using the 
            JS library Leaflet (leafletjs.com)

            map/map.html: Modified - To display a choropleth map of 
            neighborhoods using the JS library Leaflet (leafletjs.com)

        JS Files:

            community-areas.js: Stores community area boundaries in a js
            variable.

            census-tracts.js: Stroes census tract boundaries in a js
            variable.

            maptest1.js: (Legacy) Stores sample map data in a js variable.
            Used to experiment with map making techniques.
