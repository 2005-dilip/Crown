import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
csv_file_path = 'watches.csv'

# Read the CSV file into a pandas DataFrame with a different encoding
try:
    df = pd.read_csv(csv_file_path, encoding='utf-8')
except UnicodeDecodeError:
    # If utf-8 encoding fails, try 'latin1' or 'ISO-8859-1'
    df = pd.read_csv(csv_file_path, encoding='latin1')

gender1=[]
budget1=[]
style1=[]
type1=[]
rating1=[]
material1=[]
def budget(parameters):
    budget=parameters['number']
    if len(budget)==1:
        budget1.append(0)
        budget1.append(int(budget[0]))
        fulfillment_message=f"Great! Thanks for sharing your budget. With a budget of ${budget1[-1]}, we have a variety of stylish options for you. Are you interested in a specific style, like sporty, classic, or modern? "
    else:
        int_list = [int(x) for x in budget]
        budget1.extend(int_list)
        fulfillment_message = f"Great! Thanks for sharing your budget. With a budget between (${budget1[-2]} and ${budget1[-1]}), we have a variety of stylish options for you. Are you interested in a specific style, like sporty, classic, or modern? "

    return JSONResponse(content={"fulfillmentText": f"{fulfillment_message}"})
def style(parameters):
    style=parameters['style'][0]
    style1.append(style)
    fulfillment_message = " Are you looking for a women's, men's, or unisex watch?"

    return JSONResponse(content={"fulfillmentText": f"{fulfillment_message}and {style}"})
#from
def gender(parameters):
     gender= parameters['gender']
     gender1.append(gender)
def watch_type(parameters):
    type2=parameters['type']
    type1.append(type2)
def rating(parameters):
    rating = parameters['number']
    if rating[0]==5:
        rating1.append(False)
        rating1.append(int(rating[0]))
    if len(rating) == 1:
        rating1.append(int(rating[0]))
        rating1.append(5)
    else:
        int_list = [int(x) for x in rating]
        rating1.extend(int_list)
def filter(df, budget, style, gender, type1, rating, material):
    global filtered_watches

    filtered_watches = df[(df['Price'] >= budget[-2]) & (df['Price'] <= budget[-1])]
    if rating[-2] == False:
        filtered_watches = filtered_watches[(filtered_watches['Ratings'] == rating[-1])]
    else:
        filtered_watches = filtered_watches[
            (filtered_watches['Ratings'] >= rating[-2]) & (filtered_watches['Ratings'] <= rating[-1])]
    filtered_watches = filtered_watches[(filtered_watches['Style'] == style[-1])]
    filtered_watches = filtered_watches[(filtered_watches['Gender'] == gender[-1])]
    filtered_watches = filtered_watches[(filtered_watches['Type'] == type1[-1])]
    filtered_watches = filtered_watches[(filtered_watches['Material'] == material[-1])]
    return filtered_watches


def material(parameters):
    material = parameters['material']
    material1.append(material)
    filtered_watches=filter(df,budget1,style1,gender1,type1,rating1,material1)
    brand = filtered_watches.groupby('Sub-Brand')['Ratings'].mean().sort_values(ascending=False)
    recommended_brands=list(brand.head().index)
    fulfillment_message = f"Based on your choices and budget, we recommend the following watches: {', '.join(recommended_brands)}. These watches are highly rated and align with your preferences."
    response_data = {
        "fulfillmentText": fulfillment_message
    }

    return JSONResponse(content=response_data)



