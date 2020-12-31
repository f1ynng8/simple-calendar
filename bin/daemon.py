#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from configparser import ConfigParser

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import calendar
import datetime
from datetime import date
from dateutil.parser import parse
from dateutil.rrule import rrule, DAILY


logging.basicConfig(level=logging.DEBUG)
calendar.setfirstweekday(firstweekday=0)

festivalsDays={}
holiDays={}
workDays={}

def DrawScreen(draw):
    today=datetime.date.today()
    Year = today.strftime('%Y')
    Month = today.strftime('%m')
    Day = today.strftime('%d')

    currentMonth = int(Month)
    currentYear = int(Year)
    position0Month = currentMonth - 1
    position0Year = currentYear
    position2Month = currentMonth + 1
    position2Year = currentYear
    position3Month = currentMonth + 2
    position3Year = currentYear        

    if(position0Month <= 0):
        position0Month = position0Month + 12
        position0Year = currentYear - 1
    if position2Month > 12:
        position2Month = position2Month - 12
        position2Year = position2Year + 1
    if position3Month > 12:
        position3Month = position3Month - 12
        position3Year = position3Year + 1
    SetDayStatus(festivalsDays, holiDays, workDays, str(position0Year))
    SetDayStatus(festivalsDays, holiDays, workDays, str(currentYear))
    SetDayStatus(festivalsDays, holiDays, workDays, str(position2Year))
    SetDayStatus(festivalsDays, holiDays, workDays, str(position3Year))

    DrawMonth(0, position0Year, position0Month)
    DrawMonth(1, currentYear, currentMonth)
    DrawMonth(2, position2Year, position2Month)
    DrawMonth(3, position3Year, position3Month)

def DrawMonth(position,year, month):
    dateMatrix = calendar.monthcalendar(year, month)
    original_x = original_y = 0
    if position == 0:
        original_x = 0
        original_y = 0
    elif position == 1:
        original_x = 200
        original_y = 0 
    elif position == 2:           
        original_x = 0
        original_y = 150
    elif position == 3:
        original_x = 200
        original_y = 150
    font13 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 13)            
    draw.text((original_x + 60, original_y), str(year)+u'年'+str(month)+u'月', font = font13, fill = 0) 
    weekList = [u'一',u'二',u'三',u'四',u'五',u'六',u'日']

    for i in range(0,7):
        draw.text((original_x + 2 + i*28, original_y + 20), weekList[i], font = font13, fill = 0) 
    for row in range(len(dateMatrix)):
        for col in range(len(dateMatrix[row])):
            DrawDate(dateMatrix, row, col,original_x,original_y,year,month)        

def DrawDate(dateMatrix, row, col,original_x,original_y,year,month):
    font13 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 13)
    font9 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)
    today = datetime.date.today()
    currentDay = 0
    monthValue = str(month)
    dayValue = str(dateMatrix[row][col])
    if month < 10:
        monthValue = '0' + str(month)
    if dateMatrix[row][col] < 10:
        dayValue = '0' + str(dateMatrix[row][col])
    keyValue = str(year) + monthValue + dayValue
    if today.strftime('%Y%m%d') == keyValue :
        currentDay = 1
        draw.rectangle((original_x + 2 + col*28, original_y + 42 + row*18, original_x  + col*28 + 15, original_y + 54 + row*18), fill = 0)
    else:
        currentDay = 0

    if  dateMatrix[row][col] == 0:
        return
    if dateMatrix[row][col] < 10:
        draw.text((original_x + 6 + col*28, original_y + 40 + row*18), str(dateMatrix[row][col]), font = font13, fill = currentDay) 
    else:    
        draw.text((original_x + 2 + col*28, original_y + 40 + row*18), str(dateMatrix[row][col]), font = font13, fill = currentDay)   
    #绘制节日名称
    if (keyValue in festivalsDays.keys()):
        draw.text((original_x + 16 + col*28, original_y + 38 + row*18), festivalsDays[keyValue][0], font = font9, fill = 0)  
        draw.text((original_x + 16 + col*28, original_y + 48 + row*18), festivalsDays[keyValue][1], font = font9, fill = 0)  
    #绘制放假标志
    if (keyValue in holiDays.keys()):
        draw.rectangle((original_x + 2 + col*28, original_y + 42 + row*18, original_x  + col*28 + 15, original_y + 54 + row*18), outline = 0)
    #绘制上班标志
    if (keyValue in workDays.keys()):
        draw.arc((original_x + 2 + col*28, original_y + 41 + row*18, original_x  + col*28 + 17, original_y + 56 + row*18), 0, 360, fill = 0)

def SetDayStatus(festivalsDays,holidays, workDays, year):
    cfg = ConfigParser()
    cfg.read('./days/'+year+'.ini')
    for f in cfg['节日日期']:
        dates = cfg.get(u'节日日期',f)
        festivalsDays[year+cfg.get(u'节日日期',f)] = f
    for f in cfg['放假日期']:
        dates = cfg.get(u'放假日期',f)
        if '-' in dates:
            start = int(dates.split('-')[0]) + int(year)*10000
            end = int(dates.split('-')[1])  + int(year)*10000
            for i in rrule(DAILY, dtstart=parse(str(start)), until=parse(str(end))):
                holidays[i.date().strftime('%Y%m%d')] = f
        else:
            holidays[year+cfg.get(u'放假日期',f)] = f
    for f in cfg['调休上班日期']:
        dates = cfg.get(u'调休上班日期',f)
        if dates != '':
            dateList = dates.split(',')
            for d in dateList:
                workDays[year + d] = f
try:
    logging.info("The Calendar daemon starts...")
    epd = epd4in2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    DrawScreen(draw)
    epd.display(epd.getbuffer(Himage))
    time.sleep(1)
    #epd.Clear()
    logging.info("Goto Sleep...")
    epd.sleep()
    time.sleep(3)
    epd.Dev_exit()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()


