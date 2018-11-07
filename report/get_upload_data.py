
def get_sfg_product(data):
    data = data.loc[:,~data.columns.str.contains('^Unnamed')]
    data = data.dropna()
    