from Functions._settings import *

#imports the currently available used com Ports and return it in a list
def import_comports():
    a = stl.comports()
    ports = []
    for i in a:
        ports.append(i.device)
    if not a:
        messagebox.showinfo("ERROR","Keine COM-Ports gefunden, bitte überprüfen Sie die Verbindung mit Arduino")
        ports.append('COM0')
    return ports

#it Prepares the data Frame for receiving the data and return it back
#takes in a data frame
def vorbereitung(df):
    df.columns = ['sensor', 'time', 'gyrox', 'gyroy', 'gyroz', 'accelx', 'accely', 'accelz', 'a', 'b', 'c', 'd']
    df.dropna(axis=0, how='all', subset=None, inplace=True)
    df = df.drop(columns=['a', 'b', 'c', 'd'])
    return df

#takes a data frame contains angel velocity
#calculates the angel and return the data frame back
def position(sens_df):
    sens_df['time'] = sens_df['time'] / 1000
    sens_df['gyrox'] = sens_df['gyrox'] / 131
    sens_df['gyroy'] = sens_df['gyroy'] / 131
    sens_df['gyroz'] = sens_df['gyroz'] / 131
    ds = pd.Series([])
    ds = sens_df['time'] * sens_df['gyrox']
    sens_df['PositionX'] = ds
    ds = sens_df['time'] * sens_df['gyroy']
    sens_df['PositionY'] = ds
    ds = sens_df['time'] * sens_df['gyroz']
    sens_df['PositionZ'] = ds
    print(sens_df)
    return (sens_df)

#takes a data frame
#resret the index of the data frame and return it back
def reset_index(df):
    df = df.reset_index(drop=True)
    return df

#takes a data frame
#adds the angels in each row with the next row so that at the end we have the total in the last row and return it back
def add_posiotion(df):
    ds = pd.Series([])
    ds1 = pd.Series([])
    ds2 = pd.Series([])
    ds3 = pd.Series([])
    ds1[0] = df['PositionX'][0]
    ds2[0] = df['PositionY'][0]
    ds3[0] = df['PositionZ'][0]
    ds[0] = df['time'][0]
    for i in range(1, df.shape[0]):
        ds1[i] = ds1[i - 1] + df['PositionX'][i]
        ds[i] = ds[i - 1] + df['time'][i]
        ds2[i] = ds2[i - 1] + df['PositionY'][i]
        ds3[i] = ds3[i - 1] + df['PositionZ'][i]
    df['total_posx'] = ds1
    df['total_posy'] = ds2
    df['total_posz'] = ds3
    df['total_time'] = ds
    print(df)
    return (df)

#takes a data frame
#calculate the slope for the angels coloumn and then multiplies it with the time to get the error in angel
#then subtract the error from each row (from angel) and at the end return it back
def slope(df):
    print(df)
    x = (df.shape[0]) - 10
    slopex = (df['total_posx'][x] - df['total_posx'][3]) / ((df['total_time'][x] - df['total_time'][3]))
    slopey = (df['total_posy'][x] - df['total_posy'][3]) / ((df['total_time'][x] - df['total_time'][3]))
    slopez = (df['total_posz'][x] - df['total_posz'][3]) / ((df['total_time'][x] - df['total_time'][3]))
    df['PositionX'] = df['PositionX'] - (slopex * df['time'])
    df['PositionY'] = df['PositionY'] - (slopey * df['time'])
    df['PositionZ'] = df['PositionZ'] - (slopez * df['time'])
    df = add_posiotion(df)
    print(slopex)
    print(slopey)
    print(slopez)
    print(df)
    return (df)

#takes three data frames in
#create plots for the angel over time for each axis for the three data frames that
# represents the upper sensor, the lower sensor, and the spinal movement
def plotting(df1, df2, df3):
    plt.style.use('seaborn')
    fig, (x, y, z) = plt.subplots(nrows=3, ncols=1)
    x.set_title('Bewegungen der Wirbelsäule', fontsize=20)
    x.plot(df1['total_time'], df1['total_posx'], '-g', label='Oberer Sensor')
    x.plot(df2['total_time'], df2['total_posx'], '-b', label='Unterer Sensor')
    x.plot(df3['total_time'], df3['total_posx'], '-r', label='WS')
    x.set_ylabel(' Rotationswinkel [°]', fontsize=14)
    x.legend();
    y.plot(df1['total_time'], df1['total_posy'], '-g', label='Oberer Sensor')
    y.plot(df2['total_time'], df2['total_posy'], '-b', label='Unterer Sensor')
    y.plot(df3['total_time'], df3['total_posy'], '-r', label='WS')
    y.set_ylabel('Vor- und Rückneigungswinkel [°]', fontsize=14)
    z.plot(df1['total_time'], df1['total_posz'], '-g', label='Oberer Sensor')
    z.plot(df2['total_time'], df2['total_posz'], '-b', label='Unterer Sensor')
    z.plot(df3['total_time'], df3['total_posz'], '-r', label='WS')
    z.set_xlabel('Zeit [s]', fontsize=20)
    z.set_ylabel('Seitliche Neigungswinkel [°]', fontsize=14)
    plt.tight_layout()
    plt.show()

#takes two data frames (upper and lower sensor)
#subtract the angels colmns for the upper sensor from the lower and store it in a data frame
#returns the new data frame
def phi(df1, df2):
    ds = pd.DataFrame()
    ds['total_posy'] = df1['total_posy'] - df2['total_posy']
    ds['total_posx'] = df1['total_posx'] - df2['total_posx']
    ds['total_posz'] = df1['total_posz'] - df2['total_posz']
    ds['total_time'] = df2['total_time']
    print(ds)
    return (ds)



#################################################################################################################
###############################################################################  MAIN FUNCTION FOR THIS MODULE
#################################################################################################################

#takes a path to a csv file
#import the data from the csv file to a data frame and the delets all the rows that contain NAN cells
#and then call the other functions to do the calculations and create the plots
def date_cleaning(xp_path):
    try:
        df = pd.read_csv(xp_path, skiprows=10, skipfooter=100,
                         on_bad_lines='skip', header=None, names=range(12))
        df = vorbereitung(df)
        sens1_df = df.loc[df['sensor'] == 1.0]
        sens2_df = df.loc[df['sensor'] == 2.0]
        sens1_df = reset_index(sens1_df)
        sens2_df = reset_index(sens2_df)
        sens1_df = position(sens1_df)
        sens2_df = position(sens2_df)
        sens1_df = add_posiotion(sens1_df)
        sens2_df = add_posiotion(sens2_df)
        sens1_df = slope(sens1_df)
        sens2_df = slope(sens2_df)
        dss = pd.DataFrame()
        dss = phi(sens1_df, sens2_df)
        dss['total_time'] = sens1_df['total_time'][0:len(dss)]
        plotting(sens1_df, sens2_df, dss)
    except:
       messagebox.showinfo("ERROR", "Falsche Dateneingabe")
