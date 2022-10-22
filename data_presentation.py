# %% 
import index_data
import ipywidgets as widgets

# %%
period_type = widgets.Dropdown(
    description = 'Period Type:',
    options = ['Months', 'Years'], 
    value = 'Months', 
    style = {'description_width': 'initial'} 
)

period_length = widgets.IntSlider(
    description = 'Length of Period:', 
    min = 1, 
    max = 60, 
    step = 1, 
    value = 1, 
    style = {'description_width': 'initial'} 
)

starting_cash = widgets.BoundedIntText(
    description = 'How much would you like to initially invest?', 
    min = 1, 
    max = 50000, 
    step = 0.1, 
    value = 50, 
    style = {'description_width': 'initial'} 
)

display(period_type, period_length, starting_cash) #type:ignore 

# %% 
if period_type.value == "Months":
    period = str(period_length.value) + "mo"
else:
    period = str(period_length.value) + "y"

# %%
data = index_data.gather_data()
end_money_data = index_data.end_money(starting_cash.value, period, data)
index_data.get_graph(end_money_data, period)

# %%
index_picker = widgets.Dropdown(
    description = 'Index Details:',
    options = [index for index in data],  
    style = {'description_width': 'initial'} 
)

display(index_picker) #type: ignore

#%%
dict_index = end_money_data[index_picker.value]
df = index_data.get_index_details(dict_index, starting_cash.value)

#%%
df
# %%
