from datetime import datetime, timedelta
import csv
import os
from decimal import *

def get_estimates(path, dict_csv=False):
    estimates = None
    with open(path, 'r') as est_file:
        reader = csv.reader(est_file)
        if dict_csv:
            reader = csv.DictReader(est_file)
        # only one line
        for row in reader:
            estimates = row
            break
    return estimates

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, '../matlab/outputs/EV_estimates.csv')
    estimates = get_estimates(path)
    ev_rep = int(estimates[1])
    ev_dem = int(estimates[2])

    ev_metamargin = Decimal(estimates[12]).quantize(Decimal('0.1'))

    ev_ahead_str = 'D+'
    if ev_metamargin < 0:
        ev_ahead_str = 'R+'

    path = os.path.join(dir_path, '../matlab/outputs/Senate_estimates.csv')
    estimates = get_estimates(path)
    sen_seats_dem = int(estimates[0])
    sen_seats_rep = 100 - sen_seats_dem
    sen_metamargin = Decimal(estimates[-1]).quantize(Decimal('0.1'))

    sen_ahead_str = 'D+'
    if sen_metamargin < 0:
        sen_ahead_str = 'R+'

    path = os.path.join(dir_path, '../scraping/outputs/2020.generic.polls.median.csv')
    estimates = get_estimates(path, dict_csv=True)
    gen_metamargin = (Decimal(estimates['median_margin']) - 3).quantize(Decimal('0.1'))

    gen_ahead_str = 'D+'
    if gen_metamargin < 0:
        gen_ahead_str = 'R+'

    weekday_num = datetime.now().date().weekday()
    past_sunday = datetime.now() + timedelta(days=-weekday_num)
    end_of_week = past_sunday + timedelta(days=6)
    weekstartnum = past_sunday.strftime("%d")
    weekendnum = end_of_week.strftime("%d")

    datestring = ''
    if past_sunday.month != end_of_week.month:
        start_month = past_sunday.strftime("%b")
        end_month = end_of_week.strftime("%b")
        datestring = f'{start_month} {weekstartnum} - {end_month} {weekendnum}, 2020'
    else:
        month = past_sunday.strftime("%b")
        datestring = f'{month} {weekstartnum}-{weekendnum}, 2020'
    
    datestring = datetime.now().strftime("%b %d")

    ev_mm_str = f'{ev_ahead_str}{abs(ev_metamargin)}% from toss-up'
    sen_mm_str = f'{sen_ahead_str}{abs(sen_metamargin)}%'
    gen_mm_str = f'{gen_ahead_str}{abs(gen_metamargin)}%'

    banner = f"""
    <div style="font-weight: 600; width: 970px; color:black ; background-color: #eee ; line-height: 30px; font-family: Helvetica; font-size: 20px">
        <span>{datestring}: Biden {ev_dem} EV ({ev_mm_str}), Senate {sen_seats_dem} D, {sen_seats_rep} R ({sen_mm_str}), House control {gen_mm_str}</span>
        <br>
        <span>Moneyball states: President NV GA AZ, <a href="/election-tracking-2020-u-s-senate/">Senate</a> MT ME IA, <a href="https://secure.actblue.com/donate/pec2020?refcode=thermometer">Legislatures</a> KS TX NC</span>
    </div>
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, 'banner.html')
    with open(path, 'w') as bannerfile:
        bannerfile.write(banner)

if __name__ == "__main__":
    main()
