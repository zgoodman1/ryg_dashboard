import matplotlib.pyplot as plt
import base64
from io import BytesIO
import pandas as pd
from .models import Green_by_date, Green_by_team, Emot_by_date, Num_check_ins

# gets necessary stats and returns either the data for a chart, or the summary statistics
# based on "summary" argument
def getStats(summary):
    # read in csv and convert it to a df
    df = pd.read_csv('ryg_dashboard/rygs.csv')

    # eliminate duplicate entries
    result_df = df.drop_duplicates(subset=['Timestamp', 'Elaboration', 'Emotion', 'MeetingHours', 'Platform', 'PrivateElaboration', 'Reactions', 'Selection', 'SlackMessageId', 'SlackOrgId', 'SlackUserId'], keep='first')

    # make new date column with human-readable dates
    result_df['Date'] = pd.to_datetime(result_df['Timestamp'], unit='s')
    result_df['Date'] = result_df['Date'].dt.date

    # get statistics for green flags overall by date
    # get unique dates
    unique_dates = sorted(result_df.Date.unique())
    greens_by_date = []
    for date in unique_dates:
        on_date = result_df.loc[result_df.Date == date]
        total = len(on_date.index)
        green_perc = on_date.Selection.value_counts()['green'] / total
        greens_by_date.append((date, green_perc))

    # now get stats for greens based on teams
    unique_teams = result_df.SlackTeamId.unique()
    greens_by_team = []
    for team in unique_teams:
        on_team = result_df.loc[result_df.SlackTeamId == team]
        total = len(on_team.index)
        green_perc = on_team.Selection.value_counts()['green'] / total
        greens_by_team.append((team, green_perc))

    # now get stats for most common emotions each day, specific to each user (not allowing multiple submissions per day)
    # start by filtering dataset so that we only have one entry per user per day
    unique_dates_emot = sorted(result_df.Date.unique())
    emot_by_date = []
    for date in unique_dates_emot:
        # filter data based on date and only get first user entry on that day
        on_date = result_df.loc[result_df.Date == date].drop_duplicates(subset=['SlackUserId'], keep='first')
        total = len(on_date.index)
        try:
            common_emot = on_date.Emotion.value_counts().index[0]
            common_emot_perc = on_date.Emotion.value_counts()[0] / total
            emot_by_date.append((date, common_emot, common_emot_perc))
        except IndexError:
            emot_by_date.append((date, 'none', 0))

    # finally get stats for how many check ins happened on each day
    num_check_ins = []
    for date in unique_dates:
        check_ins = len(result_df[result_df.Date == date])
        num_check_ins.append((date, check_ins))

    if not summary:
        return((greens_by_date, greens_by_team, emot_by_date, num_check_ins))
    else:
        # return summary statistics
        # recent green percentage:
        rec_green_perc = greens_by_date[-1][-1]
        # most green team:
        most_green_team = sorted(greens_by_team, key= lambda x: x[1])[-1][0]
        # most common emotion:
        most_common_emot = emot_by_date[-1][1]
        # number of check ins today/most recent day
        # get most recent day
        rec_date = sorted(result_df.Date.unique())[-1]
        # get check ins on most recent day
        num_check_ins = len(result_df[result_df.Date == rec_date])
        return (rec_green_perc, most_green_team, most_common_emot, num_check_ins)

# wipes local database of prior entries to avoid duplicates
# then adds new entries based on output from getStats()
# each entry is a model which is used as a table to store data
def addData():
    data = getStats(False)

    # retrieve data for input to database
    greens_by_date = data[0]
    greens_by_team = data[1]
    emot_by_date = data[2]
    num_check_ins = data[3]

    # wipe prior entries to avoid duplicates
    Green_by_date.objects.all().delete()
    # create new model and save in database for each element in data
    for green in greens_by_date:
        entry = Green_by_date(date = green[0], percentage = green[1])
        entry.save()
    
    Green_by_team.objects.all().delete()
    for green in greens_by_team:
        entry = Green_by_team(team = green[0], percentage = green[1])
        entry.save()
    
    Emot_by_date.objects.all().delete()
    for emot in emot_by_date:
        entry = Emot_by_date(date = emot[0], emotion = emot[1], percentage = emot[2])
        entry.save()

    Num_check_ins.objects.all().delete()
    for check in num_check_ins:
        entry = Num_check_ins(date = check[0], check_ins = check[1])
        entry.save()

# creates a plot using matplotlib and saves the plot as a png
# this png is later retrieved and used for display on site
# x, y, z, represent input data for a plot
# while num indicates which plot is being generated
def getPlot(x, y, z, num):
    if num == 0:
        plt.switch_backend('AGG')
        plt.figure(figsize=(12, 8))
        plt.title('Overall green light percentage over time')
        x = [str(a) for a in x]
        plt.plot(x, y)
        plt.xticks(x, rotation=45)
        plt.xlabel('Date')
        plt.ylabel('Green lights (%)')
        plt.tight_layout()
        plt.savefig('ryg_dashboard/static/green_by_date.png')
    if num == 1:
        plt.switch_backend('AGG')
        plt.figure(figsize=(12, 8))
        plt.title('Green light percentage by team')
        plt.barh(x, y)
        plt.ylabel('Team')
        plt.xlabel('Green lights (%)')
        plt.tight_layout()
        plt.savefig('ryg_dashboard/static/green_by_team.png')
    if num == 2:
        plt.switch_backend('AGG')
        plt.figure(figsize=(12, 8))
        plt.title('Most Common Emotions in the Last 5 Days')
        x = [str(a) for a in x]
        plt.bar(x, z)
        labels = [str(a[1]) + ": " + str(a[0]) for a in zip(y,x)]
        plt.xticks(x, labels=labels)
        plt.xlabel('Date and Corresponding Common Emotion')
        plt.ylabel('Percentage of Reports of Emotion (%)')
        plt.tight_layout()
        plt.savefig('ryg_dashboard/static/emot_by_date.png')
    if num == 3:
        plt.switch_backend('AGG')
        plt.figure(figsize=(12, 8))
        plt.title('Number of Check Ins Over Time')
        x = [str(a) for a in x]
        plt.bar(x, y)
        plt.xticks(x, rotation=45)
        plt.xlabel('Date')
        plt.ylabel('Number of Check Ins')
        plt.tight_layout()
        plt.savefig('ryg_dashboard/static/num_check_ins.png')
