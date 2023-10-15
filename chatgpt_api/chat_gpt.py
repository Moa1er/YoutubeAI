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

def get_impression_and_title(vod_title, vod_comments):
    messages = [ {"role": "system", "content":  
                "You are a intelligent assistant that creates impression on tiktok videos."} ] 

    messages.append( 
        {
            "role": "user", 
            "content": 
                "In one phrase, knowing that the title of the video is: '" 
                + vod_title 
                + "' and the comments are: '" 
                + vod_comments 
                + "' give me an impression of the video (2 sentences)."
                + " Give me only the impression and nothing else."}, 
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