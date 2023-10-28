from dotenv import dotenv_values # pip3 instlal python-dotenv
import openai #pip3 install openai
import threading

secrets = dotenv_values(".env")
openai.api_key = secrets['CHATGPT_API_KEY']


MAX_RETRIES = 5
TIMEOUT = 20

def call_api(messages, result_container):
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    result_container.append(chat.choices[0].message.content)

def call_api_handle_timeout(messages):
    retries = 0
    while retries < MAX_RETRIES:
        result_container = []
        t = threading.Thread(target=call_api, args=(messages, result_container))
        t.start()
        t.join(timeout=TIMEOUT)  # Wait for the specified timeout

        if result_container:  # If there's a result, break out of the loop
            response = result_container[0]
            print(f"ChatGPT response: {response}")
            return response
        else:  # If the timeout is reached and there's no result, retry
            retries += 1
            print(f"Request timed out. Retry {retries}/{MAX_RETRIES}")

    raise Exception("Failed to get a response after max retries.")

def get_description(vid_title, vid_comments, tags):
    messages = [{
        "role": "system",
        "content": "You are a intelligent assistant that gives me a reaction of less than 100 characters "
                   + "for a youtube video basing yourself heavily on the comments provided (it can be very similar)."
                   + "Don't overdue your reaction it has to sound real like a human."
    }]

    messages.append({
        "role": "user",
        "content": "Knowing that the title of the video is: '"
                   + vid_title
                   + "', the comments are: '"
                   + vid_comments
                   + "' and the tags are: '"
                   + tags + "'."
                   + "Speak at the first person, speaking about your impression."
                   + "The video is not YOURS."
    })

    print("User request: " + messages[len(messages) - 1]["content"])

    return call_api_handle_timeout(messages)

def get_trend_keyword():
    messages = [ {"role": "system", "content":  
                "You are a intelligent assistant that creates impression on tiktok videos."} ] 

    messages.append( 
        {
            "role": "user", 
            "content": 
                "Give me ONE trendy keyword on tiktok videos that could be used to create impression on." 
                + "Don't give me dance challenge as there is a high probability of copyrighted music in it."
                + " Just answer the keyword and nothing else. Always give me a new keyword everytime I ask." 
                + " Don't give the '#' before the keyword. And don't give a dot at the end."}, 
    ) 
    print("User request: " + messages[len(messages)-1]["content"])
    
    return call_api_handle_timeout(messages)

def get_impression(vid_title, vid_comments):
    messages = [ {"role": "system", "content":  
                "You are a intelligent assistant that creates impression on tiktok videos."} ] 

    messages.append( 
        {
            "role": "user", 
            "content": 
                "In one phrase, knowing that the title of the video is: '" 
                + vid_title 
                + "' and the comments are: '" 
                + vid_comments 
                + "' give me an impression of the video."
                + "Give me only the impression and nothing else."
                + "The impression should be maximum 12 words."
                + "Speak at the first person not like everyone agrees with you."
        }, 
    )
    print("User request: " + messages[len(messages)-1]["content"])

    return call_api_handle_timeout(messages)

def get_title(txt_about_vid):
    messages = [ {"role": "system", "content":  
                "You are a intelligent assistant that creates short titles for tiktok videos."} ]

    messages.append( 
        {
            "role": "user", 
            "content": 
                "In one short phrase, knowing that the video is related to this content: '"
                + txt_about_vid
                + "' give me a short title for the video."
                + "The tite should NOT BE more than 5 words. It should be a sentence."
                + "Do not put the character ':' in the answer."
                + "You can add an emoji too but not necessary."
                + "The title should be some kind of interactions with the public"
                + " or something that gives them the want to click on the video. Please sound human !"
                + "It can be a question to the public for example."
        }, 
    )
    print("User request: " + messages[len(messages)-1]["content"])
    
    return call_api_handle_timeout(messages)

def get_vid_tags(vid_title, vid_impression, vid_comments):
    messages = [ {"role": "system", "content":  
                "You are a intelligent assistant that gives me tags (starting by '#' and ending by ',') for youtube videos."} ] 

    messages.append( 
        {
            "role": "user", 
            "content": 
                "In one phrase, knowing that the title of the video is: '" 
                + vid_title 
                + "', the comments are: '" 
                + vid_comments 
                + "' and the impression on the video is: '"
                + vid_impression
                + "', give me a list of tags for the video. The output has to be less than 450 characters."
                + "Give me only this list of tags and nothing else."
        }, 
    )
    print("User request: " + messages[len(messages)-1]["content"])

    return tag_too_long(call_api_handle_timeout(messages).replace(" ", "").split(","))

def tag_too_long(tags):
    # Calculate total characters of all tags combined
    total_chars = sum([len(tag) for tag in tags])

    # While the total number of characters is above the threshold, remove the longest tag
    while total_chars > 350:
        # Find the longest tag
        last_tag = tags[len(tags) - 1]
        tags.remove(last_tag)
        total_chars -= len(last_tag)
    
    return tags

def get_category_id(vid_title, vid_impression, vid_comments):
    possible_cat_id = "2 - Cars & Vehicles, 23 - Comedy, 27 - Education, 24 - Entertainment, 1 - Film & Animation, 20 - Gaming, 26 - How-to & Style, 10 - Music, 25 - News & Politics, 29 - Non-profits & Activism, 22 - People & Blogs, 15 - Pets & Animals, 28 - Science & Technology, 17 - Sport, 19 - Travel & Events"

    messages = [ {"role": "system", "content":  
                "You are a intelligent assistant that gives me categoryId for youtube videos."} ] 

    messages.append( 
        {
            "role": "user", 
            "content": 
                "In one phrase, knowing that the title of the video is: '" 
                + vid_title 
                + "', the comments are: '" 
                + vid_comments 
                + "' and the impression on the video is: '"
                + vid_impression
                + "', give me the category id for this video. Here are the possible category id: '"
                + possible_cat_id 
                + "' Answer me ONLY the id and nothing else."
        }, 
    )
    print("User request: " + messages[len(messages)-1]["content"])

    return call_api_handle_timeout(messages)

# def get_trend_keyword():
#     messages = [ {"role": "system", "content":  
#                 "You are a intelligent assistant that creates impression on tiktok videos."} ] 

#     messages.append( 
#         {
#             "role": "user", 
#             "content": 
#                 "Give me ONE trendy keyword on tiktok videos that could be used to create impression on." 
#                 + "Don't give me dance challenge as there is a high probability of copyrighted music in it."
#                 + " Just answer the keyword and nothing else. Always give me a new keyword everytime I ask." 
#                 + " Don't give the '#' before the keyword. And don't give a dot at the end."}, 
#     ) 
#     print("User request: " + messages[len(messages)-1]["content"])

#     chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)  
#     reply = chat.choices[0].message.content 
#     print(f"ChatGPT reply: {reply}") 
    
#     return reply

# def get_impression(vid_title, vid_comments, vid_duration = 0):
#     # takes 3 seconds of every 5 seconds increments in the video
#     # max_impression_duration = vid_duration - (1 * vid_duration // 3)
#     # print("max_impression_duration: ", max_impression_duration)

#     # or fidn the max duration of the impression
#     max_impression_duration = 4

#     messages = [ {"role": "system", "content":  
#                 "You are a intelligent assistant that creates impression on tiktok videos."} ] 

#     messages.append( 
#         {
#             "role": "user", 
#             "content": 
#                 "In one phrase, knowing that the title of the video is: '" 
#                 + vid_title 
#                 + "' and the comments are: '" 
#                 + vid_comments 
#                 + "' give me an impression of the video."
#                 + "Give me only the impression and nothing else."
#                 + "The impression should be maximum 12 words."
#                 + "Speak at the first person not like everyone agrees with you."
#         }, 
#     )
#     print("User request: " + messages[len(messages)-1]["content"])

#     chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)  
#     impression = chat.choices[0].message.content 
#     print(f"ChatGPT impression: {impression}")

#     return impression

# def get_title(txt_about_vid):
#     messages = [ {"role": "system", "content":  
#                 "You are a intelligent assistant that creates short titles for tiktok videos."} ]

#     messages.append( 
#         {
#             "role": "user", 
#             "content": 
#                 "In one short phrase, knowing that the video is related to this content: '"
#                 + txt_about_vid
#                 + "' give me a short title for the video."
#                 + "The tite should NOT BE more than 5 words. It should be a sentence."
#                 + "Do not put the character ':' in the answer."
#                 + "You can add an emoji too but not necessary."
#                 + "The title should be some kind of interactions with the public"
#                 + " or something that gives them the want to click on the video. Please sound human !"
#                 + "It can be a question to the public for example."
#         }, 
#     )
#     print("User request: " + messages[len(messages)-1]["content"])

#     chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages) 
#     vid_title = chat.choices[0].message.content 
#     print(f"ChatGPT new title for vid: {vid_title}")

#     return vid_title


# def get_vid_tags(vid_title, vid_impression, vid_comments):
#     messages = [ {"role": "system", "content":  
#                 "You are a intelligent assistant that gives me tags (starting by '#' and ending by ',') for youtube videos."} ] 

#     messages.append( 
#         {
#             "role": "user", 
#             "content": 
#                 "In one phrase, knowing that the title of the video is: '" 
#                 + vid_title 
#                 + "', the comments are: '" 
#                 + vid_comments 
#                 + "' and the impression on the video is: '"
#                 + vid_impression
#                 + "', give me a list of tags for the video. The output has to be less than 450 characters."
#                 + "Give me only this list of tags and nothing else."
#         }, 
#     )
#     print("User request: " + messages[len(messages)-1]["content"])

#     chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)  
#     tags = chat.choices[0].message.content
#     print(f"ChatGPT tags: {tags}")

#     return tag_too_long(tags.replace(" ", "").split(","))

# def tag_too_long(tags):
#     # Calculate total characters of all tags combined
#     total_chars = sum([len(tag) for tag in tags])

#     # While the total number of characters is above the threshold, remove the longest tag
#     while total_chars > 350:
#         # Find the longest tag
#         last_tag = tags[len(tags) - 1]
#         tags.remove(last_tag)
#         total_chars -= len(last_tag)
    
#     return tags

# def get_category_id(vid_title, vid_impression, vid_comments):
#     possible_cat_id = "2 - Cars & Vehicles, 23 - Comedy, 27 - Education, 24 - Entertainment, 1 - Film & Animation, 20 - Gaming, 26 - How-to & Style, 10 - Music, 25 - News & Politics, 29 - Non-profits & Activism, 22 - People & Blogs, 15 - Pets & Animals, 28 - Science & Technology, 17 - Sport, 19 - Travel & Events"

#     messages = [ {"role": "system", "content":  
#                 "You are a intelligent assistant that gives me categoryId for youtube videos."} ] 

#     messages.append( 
#         {
#             "role": "user", 
#             "content": 
#                 "In one phrase, knowing that the title of the video is: '" 
#                 + vid_title 
#                 + "', the comments are: '" 
#                 + vid_comments 
#                 + "' and the impression on the video is: '"
#                 + vid_impression
#                 + "', give me the category id for this video. Here are the possible category id: '"
#                 + possible_cat_id 
#                 + "' Answer me ONLY the id and nothing else."
#         }, 
#     )
#     print("User request: " + messages[len(messages)-1]["content"])

#     chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages) 
#     cat_id = chat.choices[0].message.content
#     print(f"ChatGPT cat_id: {cat_id}")

#     return cat_id

# def get_description(vid_title, vid_comments, tags):
#     messages = [ {"role": "system", "content":  
#                 "You are a intelligent assistant that gives me a reaction of less than 100 characters "
#                 + "for a youtube video basing yourself heavily on the comments provided (it can be very similar)."
#                 + "Don't overdue your reaction it has to sound real like a human."
#                 } ] 

#     messages.append( 
#         {
#             "role": "user", 
#             "content": 
#                 "Knowing that the title of the video is: '" 
#                 + vid_title 
#                 + "', the comments are: '" 
#                 + vid_comments 
#                 + "' and the tags are: '"
#                 + tags + "'."
#                 + "Speak at the first person, speaking about your impression."
#                 + "The video is not YOURS."
#         }, 
#     )
#     print("User request: " + messages[len(messages)-1]["content"])

#     chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages) 
#     description = chat.choices[0].message.content
#     print(f"ChatGPT description: {description}")

#     return description
