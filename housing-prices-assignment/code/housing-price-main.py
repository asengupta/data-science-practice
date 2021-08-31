# # Running the file
# If you wish to use your own copy of the data, use the following command:
#
# ``python housing-price-main.py [{-i |--input=}<train-csv>] [-h | --help]``
#
# Here are some examples:
#
# ``python housing-price-main.py --input=train.csv``
# ``python housing-price-main.py -i train.csv``
# ``python housing-price-main.py``
# ``python housing-price-main.py --help``
#
# All of these arguments are optional. Providing no arguments makes the code read from the default location, i.e. ```./data```.
#
# # Instructions on regenerating this Jupyter Notebook
# The Jupyter notebook can be regenerated by installing P2J, like so:
#
# ``pip install p2j``
#
# and running the following:
#
# ``p2j -o code/housing-price-main.py -t notebook/housing-price-main.ipynb``

# # Library Imports
import getopt
import logging
import sys
import warnings

import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from matplotlib import pyplot as plt
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor

# # Constants
# A bunch of constants are set up so that strings don't clutter the source everywhere.

DEFAULT_DATASET_LOCATION = "../data"
DEFAULT_HOUSING_PRICE_CSV_FILENAME = "train.csv"

METADATA = [{'name': 'MSSubClass', 'meaning': 'Identifies the type of dwelling involved in the sale.', 'values': [{'value': '20', 'meaning': '1-STORY 1946 & NEWER ALL STYLES'}, {'value': '30', 'meaning': '1-STORY 1945 & OLDER'}, {'value': '40', 'meaning': '1-STORY W/FINISHED ATTIC ALL AGES'}, {'value': '45', 'meaning': '1-1/2 STORY - UNFINISHED ALL AGES'}, {'value': '50', 'meaning': '1-1/2 STORY FINISHED ALL AGES'}, {'value': '60', 'meaning': '2-STORY 1946 & NEWER'}, {'value': '70', 'meaning': '2-STORY 1945 & OLDER'}, {'value': '75', 'meaning': '2-1/2 STORY ALL AGES'}, {'value': '80', 'meaning': 'SPLIT OR MULTI-LEVEL'}, {'value': '85', 'meaning': 'SPLIT FOYER'}, {'value': '90', 'meaning': 'DUPLEX - ALL STYLES AND AGES'}, {'value': '120', 'meaning': '1-STORY PUD (Planned Unit Development) - 1946 & NEWER'}, {'value': '150', 'meaning': '1-1/2 STORY PUD - ALL AGES'}, {'value': '160', 'meaning': '2-STORY PUD - 1946 & NEWER'}, {'value': '180', 'meaning': 'PUD - MULTILEVEL - INCL SPLIT LEV/FOYER'}, {'value': '190', 'meaning': '2 FAMILY CONVERSION - ALL STYLES AND AGES'}]}, {'name': 'MSZoning', 'meaning': 'Identifies the general zoning classification of the sale.', 'values': [{'value': 'A', 'meaning': 'Agriculture'}, {'value': 'C', 'meaning': 'Commercial'}, {'value': 'FV', 'meaning': 'Floating Village Residential'}, {'value': 'I', 'meaning': 'Industrial'}, {'value': 'RH', 'meaning': 'Residential High Density'}, {'value': 'RL', 'meaning': 'Residential Low Density'}, {'value': 'RP', 'meaning': 'Residential Low Density Park'}, {'value': 'RM', 'meaning': 'Residential Medium Density'}]}, {'name': 'LotFrontage', 'meaning': 'Linear feet of street connected to property', 'values': []}, {'name': 'LotArea', 'meaning': 'Lot size in square feet', 'values': []}, {'name': 'Street', 'meaning': 'Type of road access to property', 'values': [{'value': 'Grvl', 'meaning': 'Gravel'}, {'value': 'Pave', 'meaning': 'Paved'}]}, {'name': 'Alley', 'meaning': 'Type of alley access to property', 'values': [{'value': 'Grvl', 'meaning': 'Gravel'}, {'value': 'Pave', 'meaning': 'Paved'}, {'value': 'NA', 'meaning': 'No alley access'}]}, {'name': 'LotShape', 'meaning': 'General shape of property', 'values': [{'value': 'Reg', 'meaning': 'Regular'}, {'value': 'IR1', 'meaning': 'Slightly irregular'}, {'value': 'IR2', 'meaning': 'Moderately Irregular'}, {'value': 'IR3', 'meaning': 'Irregular'}]}, {'name': 'LandContour', 'meaning': 'Flatness of the property', 'values': [{'value': 'Lvl', 'meaning': 'Near Flat/Level'}, {'value': 'Bnk', 'meaning': 'Banked - Quick and significant rise from street grade to building'}, {'value': 'HLS', 'meaning': 'Hillside - Significant slope from side to side'}, {'value': 'Low', 'meaning': 'Depression'}]}, {'name': 'Utilities', 'meaning': 'Type of utilities available', 'values': [{'value': 'AllPub', 'meaning': 'All public Utilities (E,G,W,& S)'}, {'value': 'NoSewr', 'meaning': 'Electricity, Gas, and Water (Septic Tank)'}, {'value': 'NoSeWa', 'meaning': 'Electricity and Gas Only'}, {'value': 'ELO', 'meaning': 'Electricity only'}]}, {'name': 'LotConfig', 'meaning': 'Lot configuration', 'values': [{'value': 'Inside', 'meaning': 'Inside lot'}, {'value': 'Corner', 'meaning': 'Corner lot'}, {'value': 'CulDSac', 'meaning': 'Cul-de-sac'}, {'value': 'FR2', 'meaning': 'Frontage on 2 sides of property'}, {'value': 'FR3', 'meaning': 'Frontage on 3 sides of property'}]}, {'name': 'LandSlope', 'meaning': 'Slope of property', 'values': [{'value': 'Gtl', 'meaning': 'Gentle slope'}, {'value': 'Mod', 'meaning': 'Moderate Slope'}, {'value': 'Sev', 'meaning': 'Severe Slope'}]}, {'name': 'Neighborhood', 'meaning': 'Physical locations within Ames city limits', 'values': [{'value': 'Blmngtn', 'meaning': 'Bloomington Heights'}, {'value': 'Blueste', 'meaning': 'Bluestem'}, {'value': 'BrDale', 'meaning': 'Briardale'}, {'value': 'BrkSide', 'meaning': 'Brookside'}, {'value': 'ClearCr', 'meaning': 'Clear Creek'}, {'value': 'CollgCr', 'meaning': 'College Creek'}, {'value': 'Crawfor', 'meaning': 'Crawford'}, {'value': 'Edwards', 'meaning': 'Edwards'}, {'value': 'Gilbert', 'meaning': 'Gilbert'}, {'value': 'IDOTRR', 'meaning': 'Iowa DOT and Rail Road'}, {'value': 'MeadowV', 'meaning': 'Meadow Village'}, {'value': 'Mitchel', 'meaning': 'Mitchell'}, {'value': 'Names', 'meaning': 'North Ames'}, {'value': 'NoRidge', 'meaning': 'Northridge'}, {'value': 'NPkVill', 'meaning': 'Northpark Villa'}, {'value': 'NridgHt', 'meaning': 'Northridge Heights'}, {'value': 'NWAmes', 'meaning': 'Northwest Ames'}, {'value': 'OldTown', 'meaning': 'Old Town'}, {'value': 'SWISU', 'meaning': 'South & West of Iowa State University'}, {'value': 'Sawyer', 'meaning': 'Sawyer'}, {'value': 'SawyerW', 'meaning': 'Sawyer West'}, {'value': 'Somerst', 'meaning': 'Somerset'}, {'value': 'StoneBr', 'meaning': 'Stone Brook'}, {'value': 'Timber', 'meaning': 'Timberland'}, {'value': 'Veenker', 'meaning': 'Veenker'}]}, {'name': 'Condition1', 'meaning': 'Proximity to various conditions', 'values': [{'value': 'Artery', 'meaning': 'Adjacent to arterial street'}, {'value': 'Feedr', 'meaning': 'Adjacent to feeder street'}, {'value': 'Norm', 'meaning': 'Normal'}, {'value': 'RRNn', 'meaning': "Within 200' of North-South Railroad"}, {'value': 'RRAn', 'meaning': 'Adjacent to North-South Railroad'}, {'value': 'PosN', 'meaning': 'Near positive off-site feature--park, greenbelt, etc.'}, {'value': 'PosA', 'meaning': 'Adjacent to postive off-site feature'}, {'value': 'RRNe', 'meaning': "Within 200' of East-West Railroad"}, {'value': 'RRAe', 'meaning': 'Adjacent to East-West Railroad'}]}, {'name': 'Condition2', 'meaning': 'Proximity to various conditions (if more than one is present)', 'values': [{'value': 'Artery', 'meaning': 'Adjacent to arterial street'}, {'value': 'Feedr', 'meaning': 'Adjacent to feeder street'}, {'value': 'Norm', 'meaning': 'Normal'}, {'value': 'RRNn', 'meaning': "Within 200' of North-South Railroad"}, {'value': 'RRAn', 'meaning': 'Adjacent to North-South Railroad'}, {'value': 'PosN', 'meaning': 'Near positive off-site feature--park, greenbelt, etc.'}, {'value': 'PosA', 'meaning': 'Adjacent to postive off-site feature'}, {'value': 'RRNe', 'meaning': "Within 200' of East-West Railroad"}, {'value': 'RRAe', 'meaning': 'Adjacent to East-West Railroad'}]}, {'name': 'BldgType', 'meaning': 'Type of dwelling', 'values': [{'value': '1Fam', 'meaning': 'Single-family Detached'}, {'value': '2FmCon', 'meaning': 'Two-family Conversion; originally built as one-family dwelling'}, {'value': 'Duplx', 'meaning': 'Duplex'}, {'value': 'TwnhsE', 'meaning': 'Townhouse End Unit'}, {'value': 'TwnhsI', 'meaning': 'Townhouse Inside Unit'}]}, {'name': 'HouseStyle', 'meaning': 'Style of dwelling', 'values': [{'value': '1Story', 'meaning': 'One story'}, {'value': '1.5Fin', 'meaning': 'One and one-half story: 2nd level finished'}, {'value': '1.5Unf', 'meaning': 'One and one-half story: 2nd level unfinished'}, {'value': '2Story', 'meaning': 'Two story'}, {'value': '2.5Fin', 'meaning': 'Two and one-half story: 2nd level finished'}, {'value': '2.5Unf', 'meaning': 'Two and one-half story: 2nd level unfinished'}, {'value': 'SFoyer', 'meaning': 'Split Foyer'}, {'value': 'SLvl', 'meaning': 'Split Level'}]}, {'name': 'OverallQual', 'meaning': 'Rates the overall material and finish of the house', 'values': [{'value': '10', 'meaning': 'Very Excellent'}, {'value': '9', 'meaning': 'Excellent'}, {'value': '8', 'meaning': 'Very Good'}, {'value': '7', 'meaning': 'Good'}, {'value': '6', 'meaning': 'Above Average'}, {'value': '5', 'meaning': 'Average'}, {'value': '4', 'meaning': 'Below Average'}, {'value': '3', 'meaning': 'Fair'}, {'value': '2', 'meaning': 'Poor'}, {'value': '1', 'meaning': 'Very Poor'}]}, {'name': 'OverallCond', 'meaning': 'Rates the overall condition of the house', 'values': [{'value': '10', 'meaning': 'Very Excellent'}, {'value': '9', 'meaning': 'Excellent'}, {'value': '8', 'meaning': 'Very Good'}, {'value': '7', 'meaning': 'Good'}, {'value': '6', 'meaning': 'Above Average'}, {'value': '5', 'meaning': 'Average'}, {'value': '4', 'meaning': 'Below Average'}, {'value': '3', 'meaning': 'Fair'}, {'value': '2', 'meaning': 'Poor'}, {'value': '1', 'meaning': 'Very Poor'}]}, {'name': 'YearBuilt', 'meaning': 'Original construction date', 'values': []}, {'name': 'YearRemodAdd', 'meaning': 'Remodel date (same as construction date if no remodeling or additions)', 'values': []}, {'name': 'RoofStyle', 'meaning': 'Type of roof', 'values': [{'value': 'Flat', 'meaning': 'Flat'}, {'value': 'Gable', 'meaning': 'Gable'}, {'value': 'Gambrel', 'meaning': 'Gabrel (Barn)'}, {'value': 'Hip', 'meaning': 'Hip'}, {'value': 'Mansard', 'meaning': 'Mansard'}, {'value': 'Shed', 'meaning': 'Shed'}]}, {'name': 'RoofMatl', 'meaning': 'Roof material', 'values': [{'value': 'ClyTile', 'meaning': 'Clay or Tile'}, {'value': 'CompShg', 'meaning': 'Standard (Composite) Shingle'}, {'value': 'Membran', 'meaning': 'Membrane'}, {'value': 'Metal', 'meaning': 'Metal'}, {'value': 'Roll', 'meaning': 'Roll'}, {'value': 'Tar&Grv', 'meaning': 'Gravel & Tar'}, {'value': 'WdShake', 'meaning': 'Wood Shakes'}, {'value': 'WdShngl', 'meaning': 'Wood Shingles'}]}, {'name': 'Exterior1st', 'meaning': 'Exterior covering on house', 'values': [{'value': 'AsbShng', 'meaning': 'Asbestos Shingles'}, {'value': 'AsphShn', 'meaning': 'Asphalt Shingles'}, {'value': 'BrkComm', 'meaning': 'Brick Common'}, {'value': 'BrkFace', 'meaning': 'Brick Face'}, {'value': 'CBlock', 'meaning': 'Cinder Block'}, {'value': 'CemntBd', 'meaning': 'Cement Board'}, {'value': 'HdBoard', 'meaning': 'Hard Board'}, {'value': 'ImStucc', 'meaning': 'Imitation Stucco'}, {'value': 'MetalSd', 'meaning': 'Metal Siding'}, {'value': 'Other', 'meaning': 'Other'}, {'value': 'Plywood', 'meaning': 'Plywood'}, {'value': 'PreCast', 'meaning': 'PreCast'}, {'value': 'Stone', 'meaning': 'Stone'}, {'value': 'Stucco', 'meaning': 'Stucco'}, {'value': 'VinylSd', 'meaning': 'Vinyl Siding'}, {'value': 'WdSdng', 'meaning': 'Wood Siding'}, {'value': 'WdShing', 'meaning': 'Wood Shingles'}]}, {'name': 'Exterior2nd', 'meaning': 'Exterior covering on house (if more than one material)', 'values': [{'value': 'AsbShng', 'meaning': 'Asbestos Shingles'}, {'value': 'AsphShn', 'meaning': 'Asphalt Shingles'}, {'value': 'BrkComm', 'meaning': 'Brick Common'}, {'value': 'BrkFace', 'meaning': 'Brick Face'}, {'value': 'CBlock', 'meaning': 'Cinder Block'}, {'value': 'CemntBd', 'meaning': 'Cement Board'}, {'value': 'HdBoard', 'meaning': 'Hard Board'}, {'value': 'ImStucc', 'meaning': 'Imitation Stucco'}, {'value': 'MetalSd', 'meaning': 'Metal Siding'}, {'value': 'Other', 'meaning': 'Other'}, {'value': 'Plywood', 'meaning': 'Plywood'}, {'value': 'PreCast', 'meaning': 'PreCast'}, {'value': 'Stone', 'meaning': 'Stone'}, {'value': 'Stucco', 'meaning': 'Stucco'}, {'value': 'VinylSd', 'meaning': 'Vinyl Siding'}, {'value': 'WdSdng', 'meaning': 'Wood Siding'}, {'value': 'WdShing', 'meaning': 'Wood Shingles'}]}, {'name': 'MasVnrType', 'meaning': 'Masonry veneer type', 'values': [{'value': 'BrkCmn', 'meaning': 'Brick Common'}, {'value': 'BrkFace', 'meaning': 'Brick Face'}, {'value': 'CBlock', 'meaning': 'Cinder Block'}, {'value': 'None', 'meaning': 'None'}, {'value': 'Stone', 'meaning': 'Stone'}]}, {'name': 'MasVnrArea', 'meaning': 'Masonry veneer area in square feet', 'values': []}, {'name': 'ExterQual', 'meaning': 'Evaluates the quality of the material on the exterior', 'values': [{'value': 'Ex', 'meaning': 'Excellent'}, {'value': 'Gd', 'meaning': 'Good'}, {'value': 'TA', 'meaning': 'Average/Typical'}, {'value': 'Fa', 'meaning': 'Fair'}, {'value': 'Po', 'meaning': 'Poor'}]}, {'name': 'ExterCond', 'meaning': 'Evaluates the present condition of the material on the exterior', 'values': [{'value': 'Ex', 'meaning': 'Excellent'}, {'value': 'Gd', 'meaning': 'Good'}, {'value': 'TA', 'meaning': 'Average/Typical'}, {'value': 'Fa', 'meaning': 'Fair'}, {'value': 'Po', 'meaning': 'Poor'}]}, {'name': 'Foundation', 'meaning': 'Type of foundation', 'values': [{'value': 'BrkTil', 'meaning': 'Brick & Tile'}, {'value': 'CBlock', 'meaning': 'Cinder Block'}, {'value': 'PConc', 'meaning': 'Poured Contrete'}, {'value': 'Slab', 'meaning': 'Slab'}, {'value': 'Stone', 'meaning': 'Stone'}, {'value': 'Wood', 'meaning': 'Wood'}]}, {'name': 'BsmtQual', 'meaning': 'Evaluates the height of the basement', 'values': [{'value': 'Ex', 'meaning': 'Excellent (100+ inches)'}, {'value': 'Gd', 'meaning': 'Good (90-99 inches)'}, {'value': 'TA', 'meaning': 'Typical (80-89 inches)'}, {'value': 'Fa', 'meaning': 'Fair (70-79 inches)'}, {'value': 'Po', 'meaning': 'Poor (<70 inches'}, {'value': 'NA', 'meaning': 'No Basement'}]}, {'name': 'BsmtCond', 'meaning': 'Evaluates the general condition of the basement', 'values': [{'value': 'Ex', 'meaning': 'Excellent'}, {'value': 'Gd', 'meaning': 'Good'}, {'value': 'TA', 'meaning': 'Typical - slight dampness allowed'}, {'value': 'Fa', 'meaning': 'Fair - dampness or some cracking or settling'}, {'value': 'Po', 'meaning': 'Poor - Severe cracking, settling, or wetness'}, {'value': 'NA', 'meaning': 'No Basement'}]}, {'name': 'BsmtExposure', 'meaning': 'Refers to walkout or garden level walls', 'values': [{'value': 'Gd', 'meaning': 'Good Exposure'}, {'value': 'Av', 'meaning': 'Average Exposure (split levels or foyers typically score average or above)'}, {'value': 'Mn', 'meaning': 'Mimimum Exposure'}, {'value': 'No', 'meaning': 'No Exposure'}, {'value': 'NA', 'meaning': 'No Basement'}]}, {'name': 'BsmtFinType1', 'meaning': 'Rating of basement finished area', 'values': [{'value': 'GLQ', 'meaning': 'Good Living Quarters'}, {'value': 'ALQ', 'meaning': 'Average Living Quarters'}, {'value': 'BLQ', 'meaning': 'Below Average Living Quarters'}, {'value': 'Rec', 'meaning': 'Average Rec Room'}, {'value': 'LwQ', 'meaning': 'Low Quality'}, {'value': 'Unf', 'meaning': 'Unfinshed'}, {'value': 'NA', 'meaning': 'No Basement'}]}, {'name': 'BsmtFinSF1', 'meaning': 'Type 1 finished square feet', 'values': []}, {'name': 'BsmtFinType2', 'meaning': 'Rating of basement finished area (if multiple types)', 'values': [{'value': 'GLQ', 'meaning': 'Good Living Quarters'}, {'value': 'ALQ', 'meaning': 'Average Living Quarters'}, {'value': 'BLQ', 'meaning': 'Below Average Living Quarters'}, {'value': 'Rec', 'meaning': 'Average Rec Room'}, {'value': 'LwQ', 'meaning': 'Low Quality'}, {'value': 'Unf', 'meaning': 'Unfinshed'}, {'value': 'NA', 'meaning': 'No Basement'}]}, {'name': 'BsmtFinSF2', 'meaning': 'Type 2 finished square feet', 'values': []}, {'name': 'BsmtUnfSF', 'meaning': 'Unfinished square feet of basement area', 'values': []}, {'name': 'TotalBsmtSF', 'meaning': 'Total square feet of basement area', 'values': []}, {'name': 'Heating', 'meaning': 'Type of heating', 'values': [{'value': 'Floor', 'meaning': 'Floor Furnace'}, {'value': 'GasA', 'meaning': 'Gas forced warm air furnace'}, {'value': 'GasW', 'meaning': 'Gas hot water or steam heat'}, {'value': 'Grav', 'meaning': 'Gravity furnace'}, {'value': 'OthW', 'meaning': 'Hot water or steam heat other than gas'}, {'value': 'Wall', 'meaning': 'Wall furnace'}]}, {'name': 'HeatingQC', 'meaning': 'Heating quality and condition', 'values': [{'value': 'Ex', 'meaning': 'Excellent'}, {'value': 'Gd', 'meaning': 'Good'}, {'value': 'TA', 'meaning': 'Average/Typical'}, {'value': 'Fa', 'meaning': 'Fair'}, {'value': 'Po', 'meaning': 'Poor'}]}, {'name': 'CentralAir', 'meaning': 'Central air conditioning', 'values': [{'value': 'N', 'meaning': 'No'}, {'value': 'Y', 'meaning': 'Yes'}]}, {'name': 'Electrical', 'meaning': 'Electrical system', 'values': [{'value': 'SBrkr', 'meaning': 'Standard Circuit Breakers & Romex'}, {'value': 'FuseA', 'meaning': 'Fuse Box over 60 AMP and all Romex wiring (Average)'}, {'value': 'FuseF', 'meaning': '60 AMP Fuse Box and mostly Romex wiring (Fair)'}, {'value': 'FuseP', 'meaning': '60 AMP Fuse Box and mostly knob & tube wiring (poor)'}, {'value': 'Mix', 'meaning': 'Mixed'}]}, {'name': '1stFlrSF', 'meaning': 'First Floor square feet', 'values': []}, {'name': '2ndFlrSF', 'meaning': 'Second floor square feet', 'values': []}, {'name': 'LowQualFinSF', 'meaning': 'Low quality finished square feet (all floors)', 'values': []}, {'name': 'GrLivArea', 'meaning': 'Above grade (ground) living area square feet', 'values': []}, {'name': 'BsmtFullBath', 'meaning': 'Basement full bathrooms', 'values': []}, {'name': 'BsmtHalfBath', 'meaning': 'Basement half bathrooms', 'values': []}, {'name': 'FullBath', 'meaning': 'Full bathrooms above grade', 'values': []}, {'name': 'HalfBath', 'meaning': 'Half baths above grade', 'values': []}, {'name': 'BedroomAbvGr', 'meaning': 'Bedrooms above grade (does NOT include basement bedrooms)', 'values': []}, {'name': 'KitchenAbvGr', 'meaning': 'Kitchens above grade', 'values': []}, {'name': 'KitchenQual', 'meaning': 'Kitchen quality', 'values': [{'value': 'Ex', 'meaning': 'Excellent'}, {'value': 'Gd', 'meaning': 'Good'}, {'value': 'TA', 'meaning': 'Typical/Average'}, {'value': 'Fa', 'meaning': 'Fair'}, {'value': 'Po', 'meaning': 'Poor'}]}, {'name': 'TotRmsAbvGrd', 'meaning': 'Total rooms above grade (does not include bathrooms)', 'values': []}, {'name': 'Functional', 'meaning': 'Home functionality (Assume typical unless deductions are warranted)', 'values': [{'value': 'Typ', 'meaning': 'Typical Functionality'}, {'value': 'Min1', 'meaning': 'Minor Deductions 1'}, {'value': 'Min2', 'meaning': 'Minor Deductions 2'}, {'value': 'Mod', 'meaning': 'Moderate Deductions'}, {'value': 'Maj1', 'meaning': 'Major Deductions 1'}, {'value': 'Maj2', 'meaning': 'Major Deductions 2'}, {'value': 'Sev', 'meaning': 'Severely Damaged'}, {'value': 'Sal', 'meaning': 'Salvage only'}]}, {'name': 'Fireplaces', 'meaning': 'Number of fireplaces', 'values': []}, {'name': 'FireplaceQu', 'meaning': 'Fireplace quality', 'values': [{'value': 'Ex', 'meaning': 'Excellent - Exceptional Masonry Fireplace'}, {'value': 'Gd', 'meaning': 'Good - Masonry Fireplace in main level'}, {'value': 'TA', 'meaning': 'Average - Prefabricated Fireplace in main living area or Masonry Fireplace in basement'}, {'value': 'Fa', 'meaning': 'Fair - Prefabricated Fireplace in basement'}, {'value': 'Po', 'meaning': 'Poor - Ben Franklin Stove'}, {'value': 'NA', 'meaning': 'No Fireplace'}]}, {'name': 'GarageType', 'meaning': 'Garage location', 'values': [{'value': '2Types', 'meaning': 'More than one type of garage'}, {'value': 'Attchd', 'meaning': 'Attached to home'}, {'value': 'Basment', 'meaning': 'Basement Garage'}, {'value': 'BuiltIn', 'meaning': 'Built-In (Garage part of house - typically has room above garage)'}, {'value': 'CarPort', 'meaning': 'Car Port'}, {'value': 'Detchd', 'meaning': 'Detached from home'}, {'value': 'NA', 'meaning': 'No Garage'}]}, {'name': 'GarageYrBlt', 'meaning': 'Year garage was built', 'values': []}, {'name': 'GarageFinish', 'meaning': 'Interior finish of the garage', 'values': [{'value': 'Fin', 'meaning': 'Finished'}, {'value': 'RFn', 'meaning': 'Rough Finished'}, {'value': 'Unf', 'meaning': 'Unfinished'}, {'value': 'NA', 'meaning': 'No Garage'}]}, {'name': 'GarageCars', 'meaning': 'Size of garage in car capacity', 'values': []}, {'name': 'GarageArea', 'meaning': 'Size of garage in square feet', 'values': []}, {'name': 'GarageQual', 'meaning': 'Garage quality', 'values': [{'value': 'Ex', 'meaning': 'Excellent'}, {'value': 'Gd', 'meaning': 'Good'}, {'value': 'TA', 'meaning': 'Typical/Average'}, {'value': 'Fa', 'meaning': 'Fair'}, {'value': 'Po', 'meaning': 'Poor'}, {'value': 'NA', 'meaning': 'No Garage'}]}, {'name': 'GarageCond', 'meaning': 'Garage condition', 'values': [{'value': 'Ex', 'meaning': 'Excellent'}, {'value': 'Gd', 'meaning': 'Good'}, {'value': 'TA', 'meaning': 'Typical/Average'}, {'value': 'Fa', 'meaning': 'Fair'}, {'value': 'Po', 'meaning': 'Poor'}, {'value': 'NA', 'meaning': 'No Garage'}]}, {'name': 'PavedDrive', 'meaning': 'Paved driveway', 'values': [{'value': 'Y', 'meaning': 'Paved'}, {'value': 'P', 'meaning': 'Partial Pavement'}, {'value': 'N', 'meaning': 'Dirt/Gravel'}]}, {'name': 'WoodDeckSF', 'meaning': 'Wood deck area in square feet', 'values': []}, {'name': 'OpenPorchSF', 'meaning': 'Open porch area in square feet', 'values': []}, {'name': 'EnclosedPorch', 'meaning': 'Enclosed porch area in square feet', 'values': []}, {'name': '3SsnPorch', 'meaning': 'Three season porch area in square feet', 'values': []}, {'name': 'ScreenPorch', 'meaning': 'Screen porch area in square feet', 'values': []}, {'name': 'PoolArea', 'meaning': 'Pool area in square feet', 'values': []}, {'name': 'PoolQC', 'meaning': 'Pool quality', 'values': [{'value': 'Ex', 'meaning': 'Excellent'}, {'value': 'Gd', 'meaning': 'Good'}, {'value': 'TA', 'meaning': 'Average/Typical'}, {'value': 'Fa', 'meaning': 'Fair'}, {'value': 'NA', 'meaning': 'No Pool'}]}, {'name': 'Fence', 'meaning': 'Fence quality', 'values': [{'value': 'GdPrv', 'meaning': 'Good Privacy'}, {'value': 'MnPrv', 'meaning': 'Minimum Privacy'}, {'value': 'GdWo', 'meaning': 'Good Wood'}, {'value': 'MnWw', 'meaning': 'Minimum Wood/Wire'}, {'value': 'NA', 'meaning': 'No Fence'}]}, {'name': 'MiscFeature', 'meaning': 'Miscellaneous feature not covered in other categories', 'values': [{'value': 'Elev', 'meaning': 'Elevator'}, {'value': 'Gar2', 'meaning': '2nd Garage (if not described in garage section)'}, {'value': 'Othr', 'meaning': 'Other'}, {'value': 'Shed', 'meaning': 'Shed (over 100 SF)'}, {'value': 'TenC', 'meaning': 'Tennis Court'}, {'value': 'NA', 'meaning': 'None'}]}, {'name': 'MiscVal', 'meaning': '$Value of miscellaneous feature', 'values': []}, {'name': 'MoSold', 'meaning': 'Month Sold (MM)', 'values': []}, {'name': 'YrSold', 'meaning': 'Year Sold (YYYY)', 'values': []}, {'name': 'SaleType', 'meaning': 'Type of sale', 'values': [{'value': 'WD', 'meaning': 'Warranty Deed - Conventional'}, {'value': 'CWD', 'meaning': 'Warranty Deed - Cash'}, {'value': 'VWD', 'meaning': 'Warranty Deed - VA Loan'}, {'value': 'New', 'meaning': 'Home just constructed and sold'}, {'value': 'COD', 'meaning': 'Court Officer Deed/Estate'}, {'value': 'Con', 'meaning': 'Contract 15% Down payment regular terms'}, {'value': 'ConLw', 'meaning': 'Contract Low Down payment and low interest'}, {'value': 'ConLI', 'meaning': 'Contract Low Interest'}, {'value': 'ConLD', 'meaning': 'Contract Low Down'}, {'value': 'Oth', 'meaning': 'Other'}]}, {'name': 'SaleCondition', 'meaning': 'Condition of sale', 'values': [{'value': 'Normal', 'meaning': 'Normal Sale'}, {'value': 'Abnorml', 'meaning': 'Abnormal Sale -  trade, foreclosure, short sale'}, {'value': 'AdjLand', 'meaning': 'Adjoining Land Purchase'}, {'value': 'Alloca', 'meaning': 'Allocation - two linked properties with separate deeds, typically condo with a garage unit'}, {'value': 'Family', 'meaning': 'Sale between family members'}, {'value': 'Partial', 'meaning': 'Home was not completed when last assessed (associated with New Homes)'}]}]

class Columns:
    ZONING_TYPE = "MSZoning"
    NEIGHBORHOOD = "Neighborhood"
    BUILDING_TYPE = "BldgType"
    ALLEY = "Alley"
    POOL_QUALITY = "PoolQC"
    MISC_FEATURE = "MiscFeature"
    FENCE = "Fence"
    BASEMENT_QUALITY = "BsmtQual"
    BASEMENT_CONDITION = "BsmtCond"
    BASEMENT_EXPOSURE = "BsmtExposure"
    BASEMENT_FINISHED_AREA_RATING = "BsmtFinType1"
    SECONDARY_BASEMENT_FINISHED_AREA_RATING = "BsmtFinType2"
    ELECTRICAL = "Electrical"
    GARAGE_QUALITY = "GarageQual"
    GARAGE_TYPE = "GarageType"
    GARAGE_CONDITION = "GarageCond"
    GARAGE_FINISH = "GarageFinish"
    GARAGE_YEAR_BUILT = "GarageYrBlt"
    FIREPLACE_QUALITY = "FireplaceQu"
    MASONRY_VENEER_TYPE = "MasVnrType"
    MASONRY_VENEER_AREA = "MasVnrArea"
    LOT_FRONTAGE = "LotFrontage"
    EXTERIOR_FIRST = "Exterior1st"
    EXTERIOR_SECOND = "Exterior2nd"

def with_dummies_builder(categorical_column, category_mapping):
    return lambda dataset: with_dummy_variables(dataset, categorical_column, category_mapping)

# This utility function pretty prints a dataframe for output
def log_df(dataframe_label, dataframe, num_rows=10):
    heading(dataframe_label)
    logging.info(dataframe.head(num_rows).to_string())

# This function actually performs the dummy variable setup
def with_dummy_variables(dataset, categorical_column, category_mapping):
    dummy_columns = pd.get_dummies(dataset.pop(categorical_column), drop_first=True)
    log_df(f"{categorical_column} before Renaming of Dummy Variables", dummy_columns)
    dummy_columns = dummy_columns.rename(columns=category_mapping)
    log_df(f"{categorical_column} after Renaming of Dummy Variables", dummy_columns)
    dataset_with_dummy_columns = pd.concat([dataset, dummy_columns], axis=1)
    return dataset_with_dummy_columns

def dummified(dataset):
    # map_season = with_dummies_builder(Columns.SEASON, SEASON_CATEGORICAL_MAPPING)
    # map_weather = with_dummies_builder(Columns.WEATHER, WEATHER_CATEGORICAL_MAPPING)
    # return map_weather(map_season(with_day(dataset)))
    return dataset

# # Entry Point for CRISPR
#  This function is the entry point for the entire CRISPR process. This is called by `main()`
def analyse(raw_housing_prices):
    pass


def log_mode(columns, housing_prices):
    for column in columns:
        logging.debug(f"Most Common {column}: {housing_prices[column].mode()[0]}")


def log_median(columns, housing_prices):
    for column in columns:
        logging.debug(f"Most Common {column}: {housing_prices[column].median()}")


def impute(categorical_columns, numerical_columns, housing_prices):
    for categorical_column in categorical_columns:
        housing_prices[categorical_column] = housing_prices[categorical_column].fillna(
            housing_prices[categorical_column].mode()[0])
    for categorical_column in numerical_columns:
        housing_prices[categorical_column] = housing_prices[categorical_column].fillna(
            housing_prices[categorical_column].median())

    return housing_prices


def impute_missing(raw_housing_prices):
    NUMERICAL_COLUMNS_WITH_MISSING_VALUES = [Columns.MASONRY_VENEER_AREA, Columns.LOT_FRONTAGE]
    CATEGORICAL_COLUMNS_WITH_MISSING_VALUES = [Columns.ALLEY, Columns.POOL_QUALITY, Columns.MISC_FEATURE, Columns.FENCE,
                                               Columns.BASEMENT_QUALITY,
                                               Columns.BASEMENT_CONDITION, Columns.BASEMENT_EXPOSURE,
                                               Columns.BASEMENT_FINISHED_AREA_RATING,
                                               Columns.SECONDARY_BASEMENT_FINISHED_AREA_RATING,
                                               Columns.ELECTRICAL, Columns.GARAGE_QUALITY, Columns.GARAGE_TYPE,
                                               Columns.GARAGE_CONDITION, Columns.GARAGE_FINISH,
                                               Columns.GARAGE_YEAR_BUILT, Columns.FIREPLACE_QUALITY,
                                               Columns.MASONRY_VENEER_TYPE]
    log_mode(CATEGORICAL_COLUMNS_WITH_MISSING_VALUES,
             raw_housing_prices)
    log_median(NUMERICAL_COLUMNS_WITH_MISSING_VALUES, raw_housing_prices)
    imputed_housing_prices = impute(CATEGORICAL_COLUMNS_WITH_MISSING_VALUES, NUMERICAL_COLUMNS_WITH_MISSING_VALUES,
                                    raw_housing_prices)
    return imputed_housing_prices


def replace(column, valueToReplace, replacingValue, dataset):
    dataset[column] = np.where((dataset[column]==valueToReplace), replacingValue, dataset[column])
    logging.info(dataset[column].unique())
    return dataset

def imputed(raw_housing_prices):
    heading("Null Entries BEFORE")
    null_entry_statistics = raw_housing_prices.isnull().sum() / len(raw_housing_prices.index)
    logging.info(null_entry_statistics.to_string())
    raw_housing_prices = impute_missing(raw_housing_prices)
    heading("Null Entries Statistics AFTER")
    null_entry_statistics = raw_housing_prices.isnull().sum() / len(raw_housing_prices.index)
    logging.info(null_entry_statistics.to_string())

    raw_housing_prices = replace(Columns.EXTERIOR_FIRST, "Wd Sdng", "WdSdng", raw_housing_prices)
    raw_housing_prices = replace(Columns.EXTERIOR_SECOND, "Wd Sdng", "WdSdng", raw_housing_prices)

    return raw_housing_prices


def as_ranked_map(ordered):
    dictionary = {}
    for idx, val in enumerate(ordered):
        dictionary[val]=idx + 1
    return dictionary

def ranked(raw_housing_prices):
    ranked_electricity = as_ranked_map(["ELO", "NoSeWa", "NoSewr", "AllPub"])
    print(ranked_electricity)
    # raw_housing_prices["Utilities"].map({"ELO": 1, })


def verify_data_quality(dataset, metadata):
    heading("DATA DISCREPANCIES")
    for feature in metadata:
        feature_name = feature["name"]
        feature_values = set(map(lambda v: v["value"], feature["values"]))
        if (len(feature["values"]) == 0):
            continue
        actual_values = set(dataset[feature_name].unique())
        discrepancies = actual_values.difference(feature_values)
        if (discrepancies == set()):
            continue
        logging.info(f"Discrepancies for feature [{feature_name}]: {discrepancies}")


def fix_data_quality(dataset):
    dataset = replace(Columns.ZONING_TYPE, "C (all)", "C", dataset)
    dataset = replace(Columns.NEIGHBORHOOD, "NAmes", "Names", dataset)
    dataset = replace(Columns.BUILDING_TYPE, "2fmCon", "2FmCon", dataset)
    dataset = replace(Columns.BUILDING_TYPE, "Duplex", "Duplx", dataset)
    dataset = replace(Columns.BUILDING_TYPE, "Twnhs", "TwnhsE", dataset)
    dataset = replace(Columns.EXTERIOR_SECOND, "Wd Shng", "WdShing", dataset)
    dataset = replace(Columns.EXTERIOR_SECOND, "CmentBd", "CemntBd", dataset)
    dataset = replace(Columns.EXTERIOR_SECOND, "Brk Cmn", "BrkComm", dataset)

    return dataset

def study(raw_housing_prices):
    logging.debug(raw_housing_prices.head().to_string())
    logging.debug(raw_housing_prices.shape)
    logging.debug(raw_housing_prices.columns)
    imputed_housing_prices = imputed(raw_housing_prices)
    # ranked(raw_housing_prices)
    verify_data_quality(raw_housing_prices, METADATA)
    raw_housing_prices = fix_data_quality(raw_housing_prices)
    verify_data_quality(raw_housing_prices, METADATA)
    # explore(imputed_housing_prices)
    # analyse(imputed_housing_prices)

def explore(dataset):
    plt.figure()
    # Please note that generating the pairplot takes a little while due to the number of variables to plot. Please be patient while it does this.
    sns.pairplot(data=dataset)
    plt.show()
    plt.figure()
    sns.heatmap(dataset.corr(), cmap="YlGnBu", annot=True, annot_kws={"size": 5})
    plt.show()


# # Utility Functions
# This function reads command line arguments, one of which can be the input loan data set
def parse_commandline_options(args):
    print(f"args are: {args}")
    loan_csv = f"{DEFAULT_DATASET_LOCATION}/{DEFAULT_HOUSING_PRICE_CSV_FILENAME}"

    try:
        options, arguments = getopt.getopt(args, "i:hf:", ["input=", "help"])
        for option, argument in options:
            if option in ("-h", "--help"):
                print_help_text()
            elif option in ("-i", "--input"):
                loan_csv = argument
            else:
                print(f"{option} was not recognised as a valid option")
                print_help_text()
                print("Allowing to continue since Jupyter notebook passes in other command-line options")
        return loan_csv
    except getopt.GetoptError as e:
        sys.stderr.write("%s: %s\n" % (args[0], e.msg))
        print_help_text()
        exit(2)


# This function prints out the help text if either explicitly requested or in case of wrong input
def print_help_text():
    print("USAGE: python housing-price-main.py [{-i |--input=}<housing-pricing-csv>]")


# This function overrides Jupyter's default logger so that we can output things based on our formatting preferences
def setup_logging():
    warnings.filterwarnings("ignore")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logger = logging.getLogger()
    formatter = logging.Formatter('%(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)


# This function reads the loan data set
def read_csv(loan_csv):
    return pd.read_csv(loan_csv, low_memory=False)


# This utility function pretty prints a heading for output
def heading(heading_text):
    logging.info("-" * 100)
    logging.info(heading_text)
    logging.info("-" * 100)


# # Main Entry Point: main()
# This function is the entry point of the script
def main():
    setup_logging()
    study(read_csv(parse_commandline_options(sys.argv[1:])))


main()
