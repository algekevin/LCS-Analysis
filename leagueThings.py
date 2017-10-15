import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

class LeagueThings:
    def __init__(self):

        # Adjusting what is seen in the output
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 1000)
        pd.set_option('max_columns', 1000)
        #pd.set_option('expand_frame_repr', True)
        #pd.set_option('max_rows', 1000)

        # Printing this to describe what each column is.
        col_df = pd.read_csv('dataStuff/_Columns.csv')
        print(col_df, '\n')

        league_df = pd.read_csv('dataStuff/_LeagueofLegends.csv')   # This holds data from 2015 up until MSI 2017
        #print league_df, '\n'
        #print league_df[['redADC','blueADC']], '\n'
        #sneaky_df = league_df.set_index('redADC').loc[['Sneaky'], ['goldredADC']].get_values()     # Cannot figure out how to cut the gold intervals from one minute to five minute intervals
        #print sneaky_df.flatten([1])[::8]

        c9_df = self.c9_win_rate(league_df)
        sneaky_df = self.sneaky_champ_info(league_df)


    # Using Sneaky to mess around with
    def sneaky_champ_info(self, league_df):

        sneaky_df_red = league_df.set_index('redADC').loc[['Sneaky'], ['redADCChamp']]
        sneaky_df_blue = league_df.set_index('blueADC').loc[['Sneaky'], ['blueADCChamp']]

        # Displaying number of times sneaky played Sivir on red side and blue side respectively.
        print('Times snacky played Sivir on red side: ', (sneaky_df_red['redADCChamp'] == 'Sivir').sum(), '\n')
        print('Times snacky played Sivir on blue side: ', (sneaky_df_blue['blueADCChamp'] == 'Sivir').sum(), '\n')

        # Grouping the two data frames based on champ
        sneaky_df_red = sneaky_df_red.groupby('redADCChamp').size()
        sneaky_df_blue = sneaky_df_blue.groupby('blueADCChamp').size()

        # Making the data frames have two columns: champ and times played per champ
        sneaky_df_red = pd.DataFrame({'SneakyChamp':sneaky_df_red.index, 'Times played':sneaky_df_red.values})
        sneaky_df_blue = pd.DataFrame({'SneakyChamp':sneaky_df_blue.index, 'Times played':sneaky_df_blue.values})

        # Just sorting the two data frames and printing
        print(sneaky_df_red.sort_values(by='Times played', ascending=False).reset_index(drop=True))
        print(sneaky_df_blue.sort_values(by='Times played', ascending=False).reset_index(drop=True))

        # Finally, combining the red and blue data frames into one while combining times each champ was played
        sneaky_df = pd.concat([sneaky_df_red, sneaky_df_blue]).groupby('SneakyChamp').sum()
        sneaky_df = sneaky_df.sort_values(by='Times played', ascending=False).reset_index()

        print(sneaky_df, '\n')

        # Plotting sneaky's champs played finally
        ax = sns.barplot(x='SneakyChamp', y='Times played', data=sneaky_df)
        ax.set(xlabel='Dad\'s chump', ylabel='Times Played')
        ax.set_title('Daddy Info')

        sns.plt.show()

        return sneaky_df

    # Just getting win rate of Cloud 9 from red and blue sides as well as total win rate
    def c9_win_rate(self, league_df):
        c9_df = league_df[(league_df['blueTeamTag'] == 'C9') | (league_df['redTeamTag'] == 'C9')]
        c9_df_blue = c9_df[c9_df['blueTeamTag'] == 'C9']
        c9_df_red = c9_df[c9_df['redTeamTag'] == 'C9']
        print(c9_df_blue['bResult'].mean())
        print(c9_df_red['rResult'].mean(), '\n')

        # Averaging the win rates from blue and red side to get true win rate.
        c9_wr = (c9_df_blue['bResult'].mean() + c9_df_red['rResult'].mean()) / 2
        print(c9_wr)

        # Printing the league, season, and year that c9 played in.
        print(c9_df[['League','Season','Year']])

        return league_df

LeagueThings()