import rarbgapi

# Used for searching with the RARBG API module
def rarbg(search_value, chosen_value):
    # To return the following dictionary containing the results
    allLinks = dict()

    # Client is used to connect to the API
    client = rarbgapi.RarbgAPI()

    # Adult wasn't giving any results

    # Depending on the chosen value, it searches in the category
    if chosen_value == "Movie XVID":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_XVID])

    elif chosen_value == "Movie XVID 720p":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_XVID_720P])

    elif chosen_value == "Movie H264":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_H264])    

    elif chosen_value == "Movie H264 1080p":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_H264_1080P])

    elif chosen_value == "Movie H264 720p":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_H264_720P])         

    elif chosen_value == "Movie H264 3D":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_H264_3D])   

    elif chosen_value == "Movie H264 4K":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_H264_4K])    

    elif chosen_value == "Movie H265 1080P":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_H265_1080P])    

    elif chosen_value == "Movie H265 4K":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_H265_4K])    

    elif chosen_value == "Movie H265 4K HDR":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_H265_4K_HDR]) 

    elif chosen_value == "Movie Full BD":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_FULL_BD]) 

    elif chosen_value == "Movie BD Remux":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_BD_REMUX])  

    elif chosen_value == "TV Episodes":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_TV_EPISODES])   

    elif chosen_value == "TV Episodes HD":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_TV_EPISODES_HD])    

    elif chosen_value == "TV Episodes UHD":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_TV_EPISODES_UHD])    

    elif chosen_value == "Music MP3":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MUSIC_MP3])    

    elif chosen_value == "Music FLAC":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_MUSIC_FLAC])    

    elif chosen_value == "Games PC ISO":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_GAMES_PC_ISO])    

    elif chosen_value == "Games PS3":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_GAMES_PS3])    

    elif chosen_value == "Games PS4":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_GAMES_PS4])    

    elif chosen_value == "Games XBOX":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_GAMES_XBOX])    

    elif chosen_value == "Software":
        results = client.search(search_string=search_value, categories=[rarbgapi.RarbgAPI.CATEGORY_SOFTWARE])    

    # Appends the results retrieved to allLinks dictionary
    for result in results:
        allLinks[("default", "RARBG", "https://rarbg.to/", str(result))] = str(result.download)

    return allLinks

