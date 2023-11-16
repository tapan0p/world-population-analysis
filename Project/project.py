from modify_data import table
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
import pandas as pd
import seaborn as sns
import tkinter as tk


# World population data 
index=[int(row[0]) for row in table ]
countries=[row[1] for row in table ]
population=[int(row[2]) for row in table]
yearlyChange=[float(row[3][0:4]) for row in table[0:100]]
netChange=[int(row[4]) for row in table]
density=[int(row[5]) for row in table]
landArea=[int(row[6]) for row in table]
migrants=[int(row[7]) for row in table]
fartRate=[row[8] for row in table[0:100]]
midAge=[row[9] for row in table[0:100]]



def main():
    
    populationDistribution()
    populationBar()
    fertilityVsPopulationChange()
    fartalityVsMiddleAge()
    # Indian population data
    state, total, rural, urban, male, female, inhabited, uninhabited=import_data()
    population_vs_state(state,total)
    male_vs_female_population(state,male,female)
    village(state,inhabited,uninhabited)



def populationDistribution():
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter_plot = sns.scatterplot(x=index, y=population, palette="viridis", s=100, alpha=0.7)
    ax.set(xlabel="Index", ylabel="Population", title="Population Distribution in the World")
    plt.tight_layout()
    plt.show()

def populationBar():
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_plot = sns.barplot(x=countries[0:10], y=population[0:10], palette="viridis")
    ax.set(xlabel="Country Names", ylabel="Population", title="Top 10 Countries by Population")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    for p in bar_plot.patches:
        bar_plot.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    plt.show()


def fertilityVsPopulationChange():
    sorted_lists = sorted(zip(fartRate, yearlyChange), key=lambda pair: pair[0])
    x_sorted, y_sorted = zip(*sorted_lists)
    x_sorted = np.array(x_sorted, dtype=float)
    y_sorted = np.array(y_sorted)
    coefficients = np.polyfit(x_sorted, y_sorted, 2)
    polynomial = np.poly1d(coefficients)
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.scatter(x_sorted, y_sorted, label='Original Data', color='skyblue', alpha=0.7)
    x_line = np.linspace(min(x_sorted), max(x_sorted), 100)
    plt.plot(x_line, polynomial(x_line), color='red', label='Quadratic Regression')
    plt.axvline(x=2.1, color='green', linestyle='--', label='Sustainable Fertility Rate')
    plt.grid(True)
    plt.xlabel("Fertility Rate")
    plt.ylabel("Yearly Population Change (%)")
    plt.title("Fertility Rate vs Population Change with Quadratic Regression")
    plt.legend()
    plt.tight_layout()
    plt.show()
    print("Estimated Population Growth Rate at Sustainable Fertility Rate:", polynomial(2.1), "%")

def fartalityVsMiddleAge() :
    sorted_lists = sorted(zip(fartRate,midAge), key=lambda pair: pair[0])
    x_sorted, y_sorted = zip(*sorted_lists)
    x_sorted=list(x_sorted)
    y_sorted=list(y_sorted)
    x_sorted = np.array([float(x) for x in x_sorted])
    y_sorted = np.array([float(y) for y in y_sorted])
    coefficients = np.polyfit(x_sorted, y_sorted, 3)
    polynomial = np.poly1d(coefficients)
    # Plot original data
    plt.scatter(x_sorted, y_sorted, label='Original Data')
    # Plot regression line
    plt.plot(x_sorted, polynomial(x_sorted), color='red', label='Linear Regression')
    plt.axvline(x=2.1, color='green', linestyle='--', label='x = 2.1')
    plt.grid(True)
    plt.xlabel("Fatality rate")
    plt.ylabel("Average middle age of the country")
    plt.title("Fertility rate vs Average middle age of the country")
    plt.legend()
    plt.show()
    print("Avarage middle age at sustainable fertility rate ", polynomial(2.1),"%")

def import_data():
    data = pd.read_excel('Indian_data.xlsx')
    data=data[3:]
    state=[]
    total=[]
    rural=[]
    urban=[]
    male=[]
    female=[]
    inhabited=[]
    uninhabited=[]
    for i in range(3,len(data)):
        if str(data.iloc[:,3][i])=='STATE' and str(data.iloc[:,5][i])=='Total' :
            state.append(data.iloc[:,4][i])
            total.append(int(data.iloc[:,10][i]))
            male.append(int(data.iloc[:,11][i]))
            female.append(int(data.iloc[:,12][i]))
            inhabited.append(int(data.iloc[:,6][i]))
            uninhabited.append(int(data.iloc[:,7][i]))

        if str(data.iloc[:,3][i])=='STATE' and str(data.iloc[:,5][i])=='Rural' :
            rural.append(int(data.iloc[:,10][i]))
        if str(data.iloc[:,3][i])=='STATE' and str(data.iloc[:,5][i])=='Urban' :
            urban.append(int(data.iloc[:,10][i]))
    return state, total, rural, urban, male, female, inhabited, uninhabited


def population_vs_state(state,total):
    average_population=sum(total)/len(total)
    sns.barplot(x=state, y=total, color='blue',palette='deep')
    plt.xlabel('State')
    plt.ylabel('Total Population')
    plt.title('Total Population by State')
    plt.axhline(y=average_population, color='red', linestyle='--', label='Average Population', linewidth=2)
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

def male_vs_female_population(state,male,female):
    data = pd.DataFrame({
        'State': state,
        'Male Population': male,
        'Female Population': female
    })
    average_male=sum(male)/len(male)
    average_female=sum(female)/len(female)
    melted_data = pd.melt(data, id_vars=['State'], value_vars=['Male Population', 'Female Population'])
    sns.barplot(x='State', y='value', hue='variable', data=melted_data, palette='deep')
    plt.xlabel('State')
    plt.ylabel('Population')
    plt.title('Male and Female Population by State (Seaborn)')
    plt.axhline(y=average_male, color='g', linestyle='--', label='Average Male', linewidth=1)
    plt.axhline(y=average_female, color='black', linestyle='--', label='Average Female', linewidth=1)
    plt.xticks(rotation=90, ha='right')
    plt.legend(title='Gender', loc='upper right')
    plt.show()


def village(state,inhabited,uninhabited):
    data = pd.DataFrame({
        'State': state,
        'Inhabited': inhabited,
        'Uninhabited': uninhabited
    })
    melted_data = pd.melt(data, id_vars=['State'], value_vars=['Inhabited', 'Uninhabited'])
    sns.barplot(x='State', y='value', hue='variable', data=melted_data, palette='dark')
    plt.xlabel('State')
    plt.ylabel('Village')
    plt.title('Inhabited vs Uninhabited villages in a state')
    plt.xticks(rotation=90, ha='right')
    plt.legend()
    plt.show()

if __name__=="__main__" :
    main()
