'''
Author: yuweipeng
Date: 2023-04-26 20:38:55
LastEditors: yuweipeng
LastEditTime: 2023-04-26 21:02:27
Description: 主要用于性能测试摸高，并生成统一测试报告
'''
import os
import re
import time
from lazy_testdata.sh_and_os_ext import exec_cmd
from json2html import *
from decimal import Decimal
import operator

run_time_list = []
scene_name_list = []
csvfile_list = []
htmlreport_list = []
SEP = os.sep

def get_jmx_file(dir):
    jmx_files = []
    for root, dirs, files in os.walk(dir):
        for x in files:
            if '.jmx' in x:
                jmx_files.append(x)
    return jmx_files

def get_datetime():
    '''
    获取当前日期时间，格式'20150708085159'
    '''
    return time.strftime(r'%Y%m%d%H%M%S', time.localtime(time.time()))

def combine_cli_cmd(jmx_dir, threads, loops, jmx_files=None, others_args=''):
    parent_path = os.path.dirname(os.path.abspath(__file__))
    csvlog_dir = os.path.join(parent_path, 'csvlog')
    report_dir = os.path.join(parent_path, 'web-report')
    if not os.path.exists(csvlog_dir):
        os.makedirs(csvlog_dir)
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    if not jmx_files:
        jmx_files = get_jmx_file(jmx_dir)
        print(jmx_files)
    cmd_list = []
    for jmx in jmx_files:
        now = get_datetime()
        tmp = f"{jmx}t{threads}Xl{loops}at{now}"
        csv_file_name = f"{csvlog_dir}{SEP}{tmp}.csv"
        web_report = f"{report_dir}{SEP}{tmp}"
        cmd = f"jmeter -Jthreads={threads} -Jloops={loops} {others_args} -n -t {jmx_dir}{SEP}{jmx} -l {csv_file_name} -e -o {web_report}"
        print(cmd)
        cmd_list.append(cmd)
    for cmd in cmd_list:
        exec_cmd(cmd)
        time.sleep(30)

def gen_summary_report(data, report_name='SummaryReport'):
    table = json2html.convert(json=data,escape=False)
    style = """
        <style type="text/css">
        html {
            font-family: sans-serif;tan
            -ms-text-size-adjust: 100%;
            -webkit-text-size-adjust: 100%;
        }
        
        body {
            margin: 10px;
        }
        table {
            border-collapse: collapse;
            border-spacing: 0;
        }
        
        td,th {
            padding: 5;
        }
        
        .pure-table {
            border-collapse: collapse;
            border-spacing: 0;
            empty-cells: show;
            border: 1px solid #cbcbcb;
        }
        
        .pure-table caption {
            color: #000;
            font: italic 85%/1 arial,sans-serif;
            padding: 1em 0;
            text-align: center;
        }
        
        .pure-table td,.pure-table th {
            border-left: 1px solid #cbcbcb;
            border-width: 0 0 0 1px;
            font-size: inherit;
            margin: 0;
            overflow: visible;
            padding: .5em 1em;
        }
        
        .pure-table thead {
            background-color: #e0e0e0;
            color: #000;
            text-align: left;
            vertical-align: bottom;
        }
        
        .pure-table td {
            background-color: transparent;
        }
        
        .pure-table-bordered td {
            border-bottom: 1px solid #cbcbcb;
        }
        
        .pure-table-bordered tbody>tr:last-child>td {
            border-bottom-width: 0;
        }
        </style>
    """
    html = f"""
            <html>
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                    <title>{report_name}</title>
                    {style}
                </head>
                <body><center>{table} </center></body> </html>
            """
    with open(f'{report_name}.html', 'w', encoding='utf-8') as file:
        file.writelines(html)

def filter_error(data):
    error_data = []
    for d in data:
        val = d["error%"].replace('%','')
        if Decimal(val) > 0:
            error_data.append(d)
    return error_data

def collect_jmx_csv_reports(jmx_dir, csv_dir, report_dir):
    jmx_csv_report = []
    for root, dirs, files in os.walk(jmx_dir):
        for name in files:
            if '.jmx' in name:
                tmp_csv_list = []
                tmp_report_list = set()
                for csv_root, csv_dirs, csv_files in os.walk(csv_dir):
                    for csv in csv_files:
                        if name in csv:
                            tmp_csv_list.append(csv)
                            for report_root, report_dirs, report_files in os.walk(report_dir):
                                for report in report_dirs:
                                    if name in report:
                                        tmp_report_list.add(report)
                tmp = {'jmx_file': name, 'csv_files': tmp_csv_list,
                       'report_dirs': list(tmp_report_list)}
                jmx_csv_report.append(tmp)
    return jmx_csv_report

def deal_pt_data(jmx_dir, csv_dir, report_dir):
    data = []
    jmx_csv_report = collect_jmx_csv_reports(jmx_dir, csv_dir, report_dir)
    for rows in jmx_csv_report:
        run_time = '无'
        sci_name = '无'
        jmx_name = rows['jmx_file']
        td_jmx = f'<a href="file:///{jmx_dir}/{jmx_name}" target="_blank">{jmx_name}</a>'
        if not rows['csv_files']:
            data.append({"执行时间":run_time,"场景名":sci_name,"jmx文件":td_jmx,"csvLog":"无","报告详情":"无",
            "平均响应时间（ms）":"0","99th pct":"0","tps（t/s）":"0","接收":"0","发送":"0","error%":"0"})
        else:
            for i in rows['csv_files']:
                run_time = i.split('at')[-1].split('.csv')[0]
                sci_name = i.split('jmx')[-1].split('at')[0]
                jmx_name = rows['jmx_file']
                td_jmx = f'<a href="{jmx_dir}/{jmx_name}" target="_blank">{jmx_name}</a>'
                td_csv = f'<a href="{csv_dir}/{i}" target="_blank">{i}</a>'
                td_report = "无"
                may_be_report_name = i[:-4]
                if may_be_report_name in rows['report_dirs']:
                    report = f"{report_dir}/{may_be_report_name}/index.html"
                    td_report = f'<a href="{report}" target="_blank">查看</a>'
                    js = f"{report_dir}/{may_be_report_name}/content/js/dashboard.js"
                    text = ''
                    with open(js,encoding='utf-8') as f:
                        text = f.read()
                    pat = re.compile(r'''statisticsTable.+\["Total",(.+)\], "isController": false}, "titles":''')
                    detail = re.findall(pat,text)[0].split(',')
                    error = Decimal(detail[2]).quantize(Decimal('0.00'))
                    error_pct = f'{error}%'
                    avg_time = Decimal(detail[3]).quantize(Decimal('0.00'))
                    pct_99th = Decimal(detail[-4]).quantize(Decimal('0.00'))
                    throughput = Decimal(detail[-3]).quantize(Decimal('0.00'))
                    rec = Decimal(detail[-2]).quantize(Decimal('0.00'))
                    sent = Decimal(detail[-1]).quantize(Decimal('0.00'))
                try:
                    data.append({"执行时间":run_time,"场景名":sci_name,"jmx文件":td_jmx,"csvLog":td_csv,"报告详情":td_report,
            "平均响应时间（ms）":avg_time,"99th pct":pct_99th,"tps（t/s）":throughput,"接收":rec,"发送":sent,"error%":error_pct})
                except Exception as err:
                    print(err)
    sort_data = sorted(data, key=operator.itemgetter('执行时间'), reverse=False)
    return sort_data


if __name__ == '__main__':
    pass
