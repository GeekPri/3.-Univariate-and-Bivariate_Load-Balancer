import pandas as pd
import numpy as ny
class Univariate():
    import pandas as pd
    def getQuanQual(dataset):
        qual = []
        quan = []
        for col in dataset.columns:
            if dataset[col].dtype == 'O':
                qual.append(col)
            else:
                quan.append(col)
        return quan, qual
     
    
    def getDescriptiveWithUnivariatesValues(dataset, quan): 
        descriptive = pd.DataFrame(index=["Mean", "Median", "Mode", "0%", "1%", 
                                      "Q1:25%", "Q2:50%", "Q3:75%", "99%", 
                                      "Q4:100%","IQR","Lesser_Outliner", 
                                      "Greater_Outliner", "min", "max", "skew", "kurtosis", "variance", "standard_variance" ], columns = quan)
        for eachField in quan:   
            descriptive[eachField]["Mean"] = dataset[eachField].mean()
            descriptive[eachField]["Median"] = dataset[eachField].median()
            descriptive[eachField]["Mode"] = dataset[eachField].mode()[0]
            descriptive[eachField]["0%"] = ny.percentile(dataset[eachField], 0)
            descriptive[eachField]["1%"] = ny.percentile(dataset[eachField], 1)
            descriptive[eachField]["Q1:25%"] = dataset.describe()[eachField]["25%"]
            descriptive[eachField]["Q2:50%"] =dataset.describe()[eachField]['50%']
            descriptive[eachField]["Q3:75%"] = dataset.describe()[eachField]['75%']
            descriptive[eachField]["99%"] = ny.percentile(dataset[eachField], 99)
            descriptive[eachField]["Q4:100%"] = ny.percentile(dataset[eachField], 100)
            # IQR
            descriptive[eachField]["IQR"] =   dataset.describe()[eachField]['75%'] - dataset.describe()[eachField]['25%']
            descriptive[eachField]["Lesser_Outliner"] =  dataset.describe()[eachField]['25%'] - ( 1.5 * (dataset.describe()[eachField]['75%'] - dataset.describe()[eachField]['25%']))
            descriptive[eachField]["Greater_Outliner"] = dataset.describe()[eachField]['75%'] + ( 1.5 * (dataset.describe()[eachField]['75%'] - dataset.describe()[eachField]['25%']))
            descriptive[eachField]["min"] =   dataset[eachField].min()
            descriptive[eachField]["max"] =   dataset[eachField].max()
            descriptive[eachField]["skew"]= dataset[eachField].skew()
            descriptive[eachField]["kurtosis"]= dataset[eachField].kurtosis()
            descriptive[eachField]["variance"]= dataset[eachField].var()
            descriptive[eachField]["standard_variance"]= dataset[eachField].std()
        return descriptive
    
    def findOutlinerFields(descriptive,quan):
        greater= []
        lesser= []
        for columnName in quan:
        # Check if all expected keys exist in the dictionary
            if all(key in descriptive[columnName] for key in ["min", "max", "Lesser_Outliner", "Greater_Outliner"]):

                # Compare against the thresholds
                if descriptive[columnName]["min"] < descriptive[columnName]["Lesser_Outliner"]:
                    lesser.append(columnName)
                if descriptive[columnName]["max"] > descriptive[columnName]["Greater_Outliner"]:
                    greater.append(columnName)
            else:
                print(f"Missing keys in {columnName}, skipping...")
        return greater, lesser

    
    def replaceOutline(outlineFields, dataset, descriptive):
        greaterFildsList = outlineFields[0]
        lesserFildsList = outlineFields[1]    
        for lesserColumn in lesserFildsList:  
                    dataset.loc[dataset[lesserColumn] <= descriptive[lesserColumn]["Lesser_Outliner"],lesserColumn ] = descriptive[lesserColumn]["Lesser_Outliner"] 

        for greaterColumn in greaterFildsList:  
                    dataset.loc[dataset[greaterColumn] >= descriptive[greaterColumn]["Greater_Outliner"],greaterColumn ] = descriptive[greaterColumn]["Greater_Outliner"] 
        return dataset
