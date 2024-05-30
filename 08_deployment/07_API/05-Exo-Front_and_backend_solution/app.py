import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List
from fastapi import FastAPI

description = """
Human Resources API helps you learn more about you're companies employee. 
The goal of this api is to serve data that help managers understand how the company is organized and make better decisions to 
keep the top talents. 

## Preview

Where you can: 
* `/preview` a few rows of your dataset
* get `/unique-values` of a given column in your dataset

## Categorical

Where you can: 
* `/groupby` a given column and chose an aggregation metric 
* `/filter-by` one of several categories within your dataset 

## Numerical 

Where you can: 
* Get a subset of your data given a certain `/quantile` 


Check out documentation for more information on each endpoint. 
"""

tags_metadata = [
    {
        "name": "Categorical",
        "description": "Endpoints that deal with categorical data",
    },

    {
        "name": "Numerical",
        "description": "Endpoints that deal with numerical data"
    },

    {
        "name": "Preview",
        "description": "Endpoints that quickly explore dataset"
    }
]

app = FastAPI(
    title="👨‍💼 HR API",
    description=description,
    version="0.1",
    contact={
        "name": "HR API - by Jedha",
        "url": "https://jedha.co",
    },
    openapi_tags=tags_metadata
)

class GroupBy(BaseModel):
    column: str
    by_method: Literal["mean", "median", "max", "min", "sum", "count"] = "mean"

class FilterBy(BaseModel):
    column: str
    by_category: List[str]= None



@app.get("/preview", tags=["Preview"])
async def random_employees(rows: int=10):
    """
    Get a sample of your whole dataset. 
    You can specify how many rows you want by specifying a value for `rows`, default is `10`
    """
    df = pd.read_excel("data/ibm_hr_attrition.xlsx")
    sample = df.sample(rows)
    return sample.to_json()


@app.get("/unique-values", tags=["Preview"])
async def unique_values(column: str):
    """
    Get unique values from a given column 
    """
    df = pd.read_excel("data/ibm_hr_attrition.xlsx")
    df = pd.Series(df[column].unique())

    return df.to_json()

@app.get("/quantile", tags=["Numerical"])
async def quantile(column: str , percent: float = 0.1, top: bool = True):
    """
    Get a values of HR dataset according above or below a given quantile. 
    *i.e* with this dataset, you can have the top 10% values of the dataset given a certain column
    
    You can choose whether you want the top quantile or the bottom quantile by specify `top=True` or `top=False`. Default value is `top=True`
    Accepted values for percentage is a float between `0.01` and `0.99`, default is `0.1`
    """

    df = pd.read_excel("data/ibm_hr_attrition.xlsx")

    if percent > 0.99 or percent <0.01:
        msg = "percentage value is not accepted"
        return msg
    else:
        if top:
            df =    df[ df[column] > df[column].quantile(1-percent)]
        else:
            df = df[ df[column] < df[column].quantile(percent)]

        return df.to_json()

@app.post("/groupby", tags=["Categorical"])
async def group_by(groupBy: GroupBy):
    """
    Get data grouped by a given column. Accepted columns are:

    * `["Attrition","BusinessTravel", "Department", "EducationField", "Gender", "JobRole", "MaritalStatus", "Over18", "OverTime"]`

    You can use different method to group by category which are:

    * `mean`
    * `median`
    * `min`
    * `max`
    * `sum`
    * `count`
    """
    
    df = pd.read_excel("data/ibm_hr_attrition.xlsx")

    method = groupBy.by_method

    if method=="mean":
        df = df.groupby(groupBy.column).mean()
    if method=="median":
        df = df.groupby(groupBy.column).median()
    if method=="min":
        df = df.groupby(groupBy.column).min()
    if method=="max":
        df = df.groupby(groupBy.column).max()
    if method=="sum":
        df = df.groupby(groupBy.column).sum()
    if method=="count":
        df = df.groupby(groupBy.column).count()

    return df.to_json()

@app.post("/filter-by", tags=["Categorical"])
async def filter_by(filterBy: FilterBy):

    """
    Filter by one or more categories in a given column. Columns possible values are:

    * `["Attrition","BusinessTravel", "Department", "EducationField", "Gender", "JobRole", "MaritalStatus", "Over18", "OverTime"]`

    Check values within dataset to know what kind of `categories` you can filter by. You can use `/unique-values` path to check them out.
    `categories` must be `list` format.
    """

    df = pd.read_excel("data/ibm_hr_attrition.xlsx")

    if filterBy.by_category != None:
        df = df[df[filterBy.column].isin(filterBy.by_category)]
        return df.to_json()
    else:
        msg = "Please chose a column to filter by"
        return msg


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)