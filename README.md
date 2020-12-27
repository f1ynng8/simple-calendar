# simple-calendar
一个简单的日历，基于Python、树莓派、微雪4.2寸 e-Paper墨水屏。
# 功能说明
  * 显示上个月、当前月、下个月、下下个月日历
  * 显示与放假有关的节假日
  * 显示放假日期（方框圈出）
  * 显示调休上班日期（圆形圈出）
  * 显示当前日期（黑底白字）
# 使用说明
  1. 按照[这里](https://www.waveshare.net/wiki/4.2inch_e-Paper_Module)的说明配置硬件和软件运行环境
  2. 将本工程的bin目录放到RaspberryPi_JetsonNano/python/下面
  3. sudo python3 daemon.py查看运行效果
  4. 使用cron设置成每天凌晨运行一次bin/daemon.py
  5. 每年国务院发布节假日放假安排后更新bin/holiday下对应年份的.ini文件
 
