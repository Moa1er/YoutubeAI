from dotenv import dotenv_values # pip3 instlal python-dotenv
import openai #pip3 install openai

secrets = dotenv_values(".env")
openai.api_key = secrets['CHATGPT_API_KEY']

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

    chat = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo", messages=messages 
    ) 
    reply = chat.choices[0].message.content 
    print(f"ChatGPT reply: {reply}") 
    
    return reply

def get_impression_and_title(vid_title, vid_comments, vid_duration):
    # takes 3 seconds of every 5 seconds increments in the video
    # max_impression_duration = vid_duration - (1 * vid_duration // 3)
    # print("max_impression_duration: ", max_impression_duration)

    # or fidn the max duration of the impression
    max_impression_duration = 4

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
                + "' give me an impression of the video (2 sentences)."
                + " Give me only the impression and nothing else. DO NOT use sentences with commas."
                + " At 180 words per minute, the impression should be less time than "
                + str(max_impression_duration) + " seconds (make sure to calculate the time it takes with the impression you give me, "
                + "if it is more than the time I just gave you, start again)."}, 
    )
    print("User request: " + messages[len(messages)-1]["content"])

    chat = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo", messages=messages 
    ) 
    impression = chat.choices[0].message.content 
    print(f"ChatGPT impression: {impression}")

    messages.append( 
        {
            "role": "user", 
            "content": 
                "In one short phrase, knowing that the impression of the video is: '"
                + impression
                + "' give me a short title for the video."}, 
    )
    print("User request: " + messages[len(messages)-1]["content"])

    chat = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo", messages=messages 
    ) 
    vid_title = chat.choices[0].message.content 
    print(f"ChatGPT new title for vid: {vid_title}")

    return impression, vid_title


def get_vid_tags(vid_title, vid_impression, vid_comments):
    messages = [ {"role": "system", "content":  
                "You are a intelligent assistant that gives me tags for youtube videos."} ] 

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
                + "', give me a list of tags for the video seperated by a comma. The output has to be less than 450 characters."
                + "Give me only this list of tags and nothing else."
        }, 
    )
    print("User request: " + messages[len(messages)-1]["content"])

    chat = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo", messages=messages 
    ) 
    tags = chat.choices[0].message.content
    print(f"ChatGPT impression: {tags}")

    return tags.split(",")

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

    chat = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo", messages=messages 
    ) 
    cat_id = chat.choices[0].message.content
    print(f"ChatGPT impression: {cat_id}")

    return cat_id
