import os #line:2
import requests #line:3
import time #line:4
import json #line:5
import re #line:6
import subprocess #line:7
import logging #line:8
try :#line:10
    from kafka import KafkaConsumer ,TopicPartition #line:11
except :#line:12
    logging .warning ('you need pip install kafka-python')#line:13
os .environ ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'#line:15
requests .packages .urllib3 .disable_warnings ()#line:16
from airflow .settings import ETL_FILE_PATH ,KETTLE_HOME ,HIVE_HOME ,P_URL ,DATASET_TOKEN ,REFRESH_TOKEN #line:18
from airflow .utils .email import fun_email ,list_email #line:19
from airflow .common .datax import datax_cmdStr #line:20
_OOOOO00OO00O00OO0 =f'{P_URL}/echart/dataset_api/?token={DATASET_TOKEN}&visitor=Airflow&type='#line:23
_O0OO0OO00OO0OO00O =f'{P_URL}/echart/refresh_ds/?token={REFRESH_TOKEN}&type='#line:24
_O00OO00O000O0OOO0 =f'{P_URL}/dm/api/sync_tableQuality/?token={REFRESH_TOKEN}&project='#line:25
class SmartPipError (Exception ):#line:28
    def __init__ (OO0000O0O0OOOO0O0 ,err ='SmartPip Error'):#line:29
        Exception .__init__ (OO0000O0O0OOOO0O0 ,err )#line:30
def smart_upload (OO00OOO00O00O00O0 ):#line:34
    OOO00000OOO00O0O0 ,O00O00OOO0OO0O00O =os .path .split (OO00OOO00O00O00O0 )#line:35
    O00O00OOO0OO0O00O =O00O00OOO0OO0O00O .split ('.')[0 ]#line:36
    O00OO0OOO0OOO0O0O ={"title":O00O00OOO0OO0O00O ,"token":DATASET_TOKEN ,"visitor":"Airflow"}#line:41
    O00O0O00OO0O00000 ={'file':open (OO00OOO00O00O00O0 ,'rb')}#line:42
    OOO000000000OOOO0 =f'''{P_URL}/echart/dataset_api/?type=uploadlog&visitor=Airflow&token={DATASET_TOKEN}&param={{"uptime":"{time.time()}","filename":"{O00O00OOO0OO0O00O}"}}'''#line:43
    O0OO0O000O00O00O0 =60 #line:44
    OO000000O0O00O0OO =requests .post (f'{P_URL}/etl/api/upload_file_api/',files =O00O0O00OO0O00000 ,data =O00OO0OOO0OOO0O0O, verify=False )#line:46
    print (OO000000O0O00O0OO .status_code )#line:47
    if OO000000O0O00O0OO .status_code ==200 :#line:48
        OO000000O0O00O0OO =OO000000O0O00O0OO .json ()#line:49
    elif OO000000O0O00O0OO .status_code ==504 :#line:50
        print ('timeout, try waiting...')#line:51
        OO000000O0O00O0OO ={"result":"error","data":"time out"}#line:52
        for O000O0OOOOOOOO00O in range (20 ):#line:53
            O00O0OOOOO0O0O00O =requests .get (OOO000000000OOOO0, verify=False).json ()#line:54
            print (O00O0OOOOO0O0O00O )#line:55
            O00OO0OOO0OOO0O0O =O00O0OOOOO0O0O00O ['data']#line:56
            if len (O00OO0OOO0OOO0O0O )>1 :#line:57
                OO000000O0O00O0OO ={"result":"success","data":"uploaded"}#line:58
                break #line:59
            time .sleep (O0OO0O000O00O00O0 )#line:60
    else :#line:61
        OO000000O0O00O0OO ={"result":"error","data":"some thing wrong"}#line:62
    print (OO000000O0O00O0OO )#line:63
    if OO000000O0O00O0OO ['result']=='error':#line:64
        raise SmartPipError ('Upload Error')#line:65
def get_dataset (O0OOO000O00OO0OOO, param=None ):#line:68
    ""#line:73
    O0OOO000O00OO0OOO = _OOOOO00OO00O00OO0 +str (O0OOO000O00OO0OOO )
    if param:
        O0OOO000O00OO0OOO = f'{O0OOO000O00OO0OOO}&param={json.dumps(param)}'
    OO0O000OO000OO0OO =requests .get (_OOOOO00OO00O00OO0 +str (O0OOO000O00OO0OOO ),verify =False )#line:74
    OO0O000OO000OO0OO =OO0O000OO000OO0OO .json ()#line:75
    return OO0O000OO000OO0OO #line:76
def dataset (OO00O0O000OOO0OO0 ,OOO0O0OO0O000O0OO ,OO0O0OO0O000OO000 ,tolist =None ):#line:79
    ""#line:86
    O0O0OO00O0O0OOO0O =60 *15 #line:87
    O00OO0000OO000OO0 =3600 *2 #line:88
    OO000000O0O000OO0 =''#line:89
    try :#line:90
        while True :#line:91
            OOO000O0OO0OO0O00 =requests .get (_OOOOO00OO00O00OO0 +OOO0O0OO0O000O0OO ,verify =False )#line:92
            OOO000O0OO0OO0O00 =OOO000O0OO0OO0O00 .json ()#line:93
            O0O0O0OOO000OOO00 =OOO000O0OO0OO0O00 ['result']#line:94
            OOO000O0OO0OO0O00 =OOO000O0OO0OO0O00 ['data']#line:95
            if O0O0O0OOO000OOO00 =='error':#line:96
                raise Exception (f'{OOO000O0OO0OO0O00}')#line:97
            OO000000O0O000OO0 =',\n'.join ([str (O00O0OOO0OOOOO00O )for O00O0OOO0OOOOO00O in OOO000O0OO0OO0O00 ])#line:98
            print (f'Dataset: {OO000000O0O000OO0} ')#line:99
            if OO0O0OO0O000OO000 =='e3':#line:100
                if len (OOO000O0OO0OO0O00 )<2 :#line:101
                    if O00OO0000OO000OO0 <=0 :#line:102
                        raise Exception ('超时且数据为空')#line:103
                    else :#line:104
                        time .sleep (O0O0OO00O0O0OOO0O )#line:105
                        O00OO0000OO000OO0 =O00OO0000OO000OO0 -O0O0OO00O0O0OOO0O #line:106
                else :#line:107
                    break #line:108
            else :#line:109
                if len (OOO000O0OO0OO0O00 )>1 :#line:110
                    if OO0O0OO0O000OO000 =='e1':#line:111
                        raise Exception ('有异常数据')#line:112
                    elif OO0O0OO0O000OO000 =='e2':#line:113
                        list_email (f'Info_{OO00O0O000OOO0OO0}',f'{OO00O0O000OOO0OO0}-Dataset Status',OOO000O0OO0OO0O00 ,to_list =tolist )#line:114
                else :#line:115
                    if OO0O0OO0O000OO000 not in ['info','e1']:#line:116
                        OO000000O0O000OO0 ='数据为空'#line:117
                        raise Exception (OO000000O0O000OO0 )#line:118
                break #line:119
    except Exception as O000OO000OOOOOOO0 :#line:120
        fun_email (f'{OO00O0O000OOO0OO0}-执行Dataset校验出错',OO000000O0O000OO0 ,to_list =tolist )#line:121
        raise SmartPipError (str (O000OO000OOOOOOO0 .args ))#line:122
def refresh_dash (OOOO0OOO0O00O0000 ,O0OO0O0O0O0OOO000 ):#line:125
    ""#line:128
    try :#line:129
        OO0OOOOOOOOO0O00O =requests .get (f'{_O0OO0OO00OO0OO00O}{O0OO0O0O0O0OOO000}',verify =False )#line:130
        OO0OOOOOOOOO0O00O =OO0OOOOOOOOO0O00O .json ()#line:131
        print (OO0OOOOOOOOO0O00O )#line:132
        O0OO00OO00OOO0OOO =OO0OOOOOOOOO0O00O ['status']#line:133
        if O0OO00OO00OOO0OOO !=200 :#line:134
            raise SmartPipError ('refresh_dash')#line:135
    except Exception as OOO0O0OO0O0O00OO0 :#line:136
        fun_email (f'{OOOO0OOO0O00O0000}-执行refresh出错',str (OOO0O0OO0O0O00OO0 .args ))#line:137
        raise SmartPipError (str (OOO0O0OO0O0O00OO0 .args ))#line:138
def refresh_quality (OOO00O0OO0OO0000O ,OOOOOOO0000000O0O ,hours =1 ):#line:140
    ""#line:143
    try :#line:144
        OO00OOO0OO0OO000O =requests .get (f'{_O00OO00O000O0OOO0}{OOOOOOO0000000O0O}&hours={hours}',verify =False )#line:145
        OO00OOO0OO0OO000O =OO00OOO0OO0OO000O .json ()#line:146
        print (OO00OOO0OO0OO000O )#line:147
        OOO0OOO0O000OOOOO =OO00OOO0OO0OO000O ['status']#line:148
        if OOO0OOO0O000OOOOO !=200 :#line:149
            raise SmartPipError ('refresh_quality')#line:150
    except Exception as O0O0OO0O000000O00 :#line:151
        fun_email (f'{OOO00O0OO0OO0000O}-执行refresh_quality出错',str (O0O0OO0O000000O00 .args ))#line:152
        raise SmartPipError (str (O0O0OO0O000000O00 .args ))#line:153
def dash_mail (O000000OOO00O0000 ,OOO000O00OOOO0000 ,O0O00OOOOOO000O0O ):#line:1
    ""#line:5
    if callable (OOO000O00OOOO0000 ):#line:6
        O000OOO00O0O0OOO0 =OOO000O00OOOO0000 ()#line:7
    else :#line:8
        O000OOO00O0O0OOO0 =OOO000O00OOOO0000 #line:9
    print (O000OOO00O0O0OOO0 )#line:10
    if isinstance (O000OOO00O0O0OOO0 ,str ):#line:11
        fun_email (O000000OOO00O0000 ,O000OOO00O0O0OOO0 ,O0O00OOOOOO000O0O )#line:12
    else :#line:13
        fun_email (O000OOO00O0O0OOO0 [0 ],O000OOO00O0O0OOO0 [1 ],O0O00OOOOOO000O0O )#line:14
    print ('发送邮件成功!')
def run_bash (O000OOOOOO0OOO0OO ):#line:157
    OOO0OO0O000O0000O =''#line:158
    O0OO00O0OO0OO0OOO =subprocess .Popen (O000OOOOOO0OOO0OO ,stdout =subprocess .PIPE ,stderr =subprocess .STDOUT ,shell =True ,cwd =ETL_FILE_PATH )#line:159
    print ('PID:',O0OO00O0OO0OO0OOO .pid )#line:160
    for OOO0OOOOO00O0OOO0 in iter (O0OO00O0OO0OO0OOO .stdout .readline ,b''):#line:161
        if O0OO00O0OO0OO0OOO .poll ()and OOO0OOOOO00O0OOO0 ==b'':#line:162
            break #line:163
        OOO0OOOOO00O0OOO0 =OOO0OOOOO00O0OOO0 .decode (encoding ='utf8')#line:164
        print (OOO0OOOOO00O0OOO0 .rstrip ())#line:165
        OOO0OO0O000O0000O =OOO0OO0O000O0000O +OOO0OOOOO00O0OOO0 #line:166
    O0OO00O0OO0OO0OOO .stdout .close ()#line:167
    O00000OOO00O00000 =O0OO00O0OO0OO0OOO .wait ()#line:168
    print ('result code: ',O00000OOO00O00000 )#line:169
    return OOO0OO0O000O0000O ,O00000OOO00O00000 #line:170
def run_python (O0O0OOOO0OO0OO00O ,OOOO0O0O00O0OO00O ,dev =''):#line:173
    O00OO0OOO0OO00OO0 =O0O0OOOO0OO0OO00O .split ('/')#line:174
    _O0OOOOO0O0O0O000O ,OO0O000O000OO0OOO =run_bash ('python %s %s'%(O0O0OOOO0OO0OO00O ,OOOO0O0O00O0OO00O ))#line:175
    if OO0O000O000OO0OOO !=0 :#line:176
        fun_email (f'{O00OO0OOO0OO00OO0[-2]}/{O00OO0OOO0OO00OO0[-1]}出错','python error')#line:177
        raise Exception ('error')#line:178
def run_dataxx (O0O00OOO0000O0000 ,OOO00O00OOOOO0000 ,dev =''):#line:182
    O00O00OO000000O0O =O0O00OOO0000O0000 .split ('/')#line:183
    if OOO00O00OOOOO0000 :#line:184
        OOO0OO0OOO0O00OO0 =[f'-D{O0OO0O0O0OO0O0OOO}:{O000OO00OO000OOO0}'for O0OO0O0O0OO0O0OOO ,O000OO00OO000OOO0 in OOO00O00OOOOO0000 .items ()]#line:185
        O0OOO0O0O00000O00 =' '.join (OOO0OO0OOO0O00OO0 )#line:186
        O0OOO000OOO00O000 =[f'-p"{O0OOO0O0O00000O00}"',O0O00OOO0000O0000 ]#line:187
    else :#line:188
        O0OOO000OOO00O000 =[O0O00OOO0000O0000 ]#line:189
    O0O0O0O0OO0OO00O0 =datax_cmdStr (O0OOO000OOO00O000 )#line:190
    _OO0OOOOO0OO0OO000 ,OOOOO0OOO00O0OOOO =run_bash (O0O0O0O0OO0OO00O0 )#line:191
    if OOOOO0OOO00O0OOOO !=0 :#line:192
        fun_email (f'{O00O00OO000000O0O[-2]}/{O00O00OO000000O0O[-1]}出错','datax error')#line:193
        raise Exception ('error')#line:194
def run_datax (O00OO00OOO0OOO0OO ,O0O0O0OO0O0O0OO0O ,OOOO00OO0OO000000 ,OO00O0OO00OOO000O ,dev =''):#line:197
    with open (O00OO00OOO0OOO0OO ,'r',encoding ='utf8')as OO0000O0O0000OOO0 :#line:198
        OOOO0O0O00O0O000O =readSqlstr (OO0000O0O0000OOO0 .read ().strip (),para_dict =OO00O0OO00OOO000O )#line:199
    OOOO0O0O00O0O000O =OOOO0O0O00O0O000O .split ('##')#line:200
    O00O0O00OO0O00OOO ={}#line:201
    for OOO0OOOO0O0O000O0 in OOOO0O0O00O0O000O :#line:202
        O0O0OOO000OO0O00O =OOO0OOOO0O0O000O0 .find ('=')#line:203
        if O0O0OOO000OO0O00O >0 :#line:204
            O00O0O00OO0O00OOO [OOO0OOOO0O0O000O0 [:O0O0OOO000OO0O00O ].strip ()]=OOO0OOOO0O0O000O0 [O0O0OOO000OO0O00O +1 :].replace ('\n',' ').strip ()#line:205
    O00O0OOOOOO0OO0OO =O00O0O00OO0O00OOO .keys ()#line:206
    OOO0OO00O00OO0O0O =O00O0O00OO0O00OOO .pop ('template')if 'template'in O00O0OOOOOO0OO0OO else 'default'#line:207
    OO0OOOOOOOOO0OOO0 =O00O0O00OO0O00OOO .get ('targetColumn')#line:208
    O0O0OOOOO000OOOOO =None #line:209
    if OOO0OO00O00OO0O0O .endswith ('hdfs'):#line:210
        O0O0OOOOO000OOOOO =O00O0O00OO0O00OOO .pop ('hiveSql')if 'hiveSql'in O00O0OOOOOO0OO0OO else None #line:212
        if not O0O0OOOOO000OOOOO :#line:213
            O0O0OOOOO000OOOOO =O00O0O00OO0O00OOO .pop ('postSql')if 'postSql'in O00O0OOOOOO0OO0OO else None #line:214
        if OO0OOOOOOOOO0OOO0 :#line:216
            OO0OOOOOOOOO0OOO0 =OO0OOOOOOOOO0OOO0 .split (',')#line:217
            OOOO0000OOOO000O0 =[]#line:218
            for OOO0OOOO0O0O000O0 in OO0OOOOOOOOO0OOO0 :#line:219
                if ':'in OOO0OOOO0O0O000O0 :#line:220
                    OOO0OOOO0O0O000O0 =OOO0OOOO0O0O000O0 .split (':')#line:221
                    OOOO0000OOOO000O0 .append ({"name":OOO0OOOO0O0O000O0 [0 ].strip (),"type":OOO0OOOO0O0O000O0 [1 ].strip ()})#line:222
                else :#line:223
                    OOOO0000OOOO000O0 .append ({"name":OOO0OOOO0O0O000O0 .strip (),"type":"STRING"})#line:224
            O00O0O00OO0O00OOO ['targetColumn']=json .dumps (OOOO0000OOOO000O0 )#line:225
    else :#line:226
        if OO0OOOOOOOOO0OOO0 :#line:227
            OO0OOOOOOOOO0OOO0 =[OOO00OOO00000000O .strip ()for OOO00OOO00000000O in OO0OOOOOOOOO0OOO0 .split (',')]#line:228
            O00O0O00OO0O00OOO ['targetColumn']=json .dumps (OO0OOOOOOOOO0OOO0 )#line:229
        else :#line:230
            O00O0O00OO0O00OOO ['targetColumn']='["*"]'#line:231
        if OOO0OO00O00OO0O0O .endswith ('starrocks'):#line:233
            if '.'in O00O0O00OO0O00OOO ['targetTable']:#line:234
                O00O0O00OO0O00OOO ['targetDB'],O00O0O00OO0O00OOO ['targetTable']=O00O0O00OO0O00OOO ['targetTable'].split ('.')#line:235
            else :#line:236
                O00O0O00OO0O00OOO ['targetDB']='Test'#line:237
        else:
            if 'writeMode' not in O00O0OOOOOO0OO0OO:
                O00O0OOOOOO0OO0OO['writeMode'] = 'insert'
    if 'preSql'in O00O0OOOOOO0OO0OO :#line:239
        O00O0O00OO0O00OOO ['preSql']=json .dumps (O00O0O00OO0O00OOO ['preSql'].strip ().split (';'))#line:240
    else :#line:241
        O00O0O00OO0O00OOO ['preSql']=''#line:242
    if 'postSql'in O00O0OOOOOO0OO0OO :#line:243
        O00O0O00OO0O00OOO ['postSql']=json .dumps (O00O0O00OO0O00OOO ['postSql'].strip ().split (';'))#line:244
    else :#line:245
        O00O0O00OO0O00OOO ['postSql']=''#line:246
    OO00O0OO0O0000OO0 =O00OO00OOO0OOO0OO .split ('/')#line:247
    OO00000O00O000O0O =OO00O0OO0O0000OO0 [-1 ].split ('.')[0 ]#line:248
    with open (os .path .join (OOOO00OO0OO000000 ,'datax','templates',OOO0OO00O00OO0O0O ),'r')as OO0000O0O0000OOO0 :#line:249
        OOOOOOOO0000OO000 =OO0000O0O0000OOO0 .read ()#line:250
    O00OO00OOO0OOO0OO =os .path .join (OOOO00OO0OO000000 ,'datax',OO00000O00O000O0O +'.json')#line:251
    with open (O00OO00OOO0OOO0OO ,'w',encoding ='utf8')as OO0000O0O0000OOO0 :#line:252
        OO0000O0O0000OOO0 .write (readSqlstr (OOOOOOOO0000OO000 ,O00O0O00OO0O00OOO ))#line:253
    OOOOO0OOOOO0OO0OO =datax_cmdStr ([O00OO00OOO0OOO0OO ])#line:254
    _OOO0O00OOOO000000 ,OO0000000OO0OO0O0 =run_bash (OOOOO0OOOOO0OO0OO )#line:255
    if OO0000000OO0OO0O0 !=0 :#line:256
        fun_email (f'{OO00O0OO0O0000OO0[-2]}/{OO00O0OO0O0000OO0[-1]}出错','datax error')#line:257
        raise Exception ('error')#line:258
    if O0O0OOOOO000OOOOO :#line:259
        print (_OO000OO0O0O000OO0 (O0O0OOOOO000OOOOO .split (';'),O0O0O0OO0O0O0OO0O ,db_connect ='hive',dev =dev ))#line:260
def readSqlFile (OOOOO0O000O00O0OO ,para_dict =None ):#line:264
    if OOOOO0O000O00O0OO .find ('.sql')<0 :#line:265
        return 'file type error'#line:266
    with open (OOOOO0O000O00O0OO ,'r',encoding ='utf-8')as O000OOOO0OO0OOOOO :#line:267
        O000OO00OO0OOOOOO =O000OOOO0OO0OOOOO .read ()#line:268
    O000O00OO00O0O0O0 =readSqlstr (O000OO00OO0OOOOOO ,para_dict )#line:269
    return O000O00OO00O0O0O0 #line:270
def readSqoopFile (O0OO00OOO0OOOOO0O ,para_dict =None ):#line:273
    if not O0OO00OOO0OOOOO0O .endswith ('.sql'):#line:274
        return 'file type error'#line:275
    with open (O0OO00OOO0OOOOO0O ,'r',encoding ='utf8')as OO0OO0O00OOOOOOO0 :#line:276
        OO0O0OOO000OOO00O =OO0OO0O00OOOOOOO0 .read ().strip ()#line:277
    O000OO0O0O0OOO00O =re .match (r"/\*(.*?)\*/(.+)",OO0O0OOO000OOO00O ,re .M |re .S )#line:278
    OOOO000O0000O00O0 =readSqlstr (O000OO0O0O0OOO00O .group (1 ).strip (),para_dict )#line:279
    O0OO0O00O0000O00O =O000OO0O0O0OOO00O .group (2 ).strip ()#line:280
    return OOOO000O0000O00O0 ,O0OO0O00O0000O00O #line:281
def readSqlstr (O00OO00OO00O00OOO ,para_dict =None ):#line:1
    O0O000O0OOOOOO0O0 =re .sub (r"(\/\*(.|\n)*?\*\/)|--.*",'',O00OO00OO00O00OOO .strip ())#line:2
    if para_dict :#line:3
        for OO0OO000OO0OOOOOO ,O00OO000OO0OOO000 in para_dict .items ():#line:4
            if OO0OO000OO0OOOOOO .isnumeric ():#line:5
                OO00O0O0OOOO0OOO0 =get_dataset (O00OO000OO0OOO000 )['data']#line:6
                print ('dataset:',OO00O0O0OOOO0OOO0 )#line:7
                if len (OO00O0O0OOOO0OOO0 )>1 :#line:8
                    for OOOOOOOO00O0OO0O0 ,O0O00OO0OOOO0O000 in zip (OO00O0O0OOOO0OOO0 [0 ],OO00O0O0OOOO0OOO0 [1 ]):#line:9
                        O0O000O0OOOOOO0O0 =O0O000O0OOOOOO0O0 .replace ('$'+OOOOOOOO00O0OO0O0 ,str (O0O00OO0OOOO0O000 ))#line:10
            elif callable (O00OO000OO0OOO000 ):#line:11
                O000O0OOOOO000OO0 =O00OO000OO0OOO000 ()#line:12
                for OOOOOOOO00O0OO0O0 ,O0O00OO0OOOO0O000 in O000O0OOOOO000OO0 .items ():#line:13
                    O0O000O0OOOOOO0O0 =O0O000O0OOOOOO0O0 .replace ('$'+OOOOOOOO00O0OO0O0 ,str (O0O00OO0OOOO0O000 ))#line:14
            else :#line:15
                O0O000O0OOOOOO0O0 =O0O000O0OOOOOO0O0 .replace ('$'+OO0OO000OO0OOOOOO ,str (O00OO000OO0OOO000 ))#line:16
    return O0O000O0OOOOOO0O0
def run_sql_file (O00OO0OOOOOOOOOOO ,O00000000OOOOOO00 ,db_connect ='starrocks',para_dict =None ,dev =''):#line:292
    O0000O00O0OO0OO00 =O00OO0OOOOOOOOOOO .split ('/')#line:293
    try :#line:294
        OO0O000OO0OO00OO0 =readSqlFile (O00OO0OOOOOOOOOOO ,para_dict ).split (';')#line:295
        OO0O0000O0OOO000O =O00000000OOOOOO00 .get (db_connect )#line:296
        if dev :#line:297
            if f'{db_connect}{dev}'in O00000000OOOOOO00 .keys ():#line:298
                OO0O0000O0OOO000O =O00000000OOOOOO00 .get (f'{db_connect}{dev}')#line:299
        OOOOOOO0O000OOO0O =connect_db_execute ().execute_sql_list (OO0O000OO0OO00OO0 ,db_connect ,connect_dict =OO0O0000O0OOO000O )#line:300
        return OOOOOOO0O000OOO0O #line:301
    except Exception as OO0000O0OOOOO0OOO :#line:302
        fun_email ('{}/{}执行出错'.format (O0000O00O0OO0OO00 [-2 ],O0000O00O0OO0OO00 [-1 ]),str (OO0000O0OOOOO0OOO .args ))#line:303
        print (OO0000O0OOOOO0OOO .args )#line:304
        raise SmartPipError ('Run SQL Error')#line:305
def _OO000OO0O0O000OO0 (O00O0000O00000O00 ,OOOOO0OOO0O0O0O0O ,db_connect ='starrocks',para_dict =None ,dev =''):#line:308
    try :#line:309
        if isinstance (O00O0000O00000O00 ,str ):#line:310
            O00O0000O00000O00 =readSqlstr (O00O0000O00000O00 ,para_dict ).split (';')#line:311
        OO0O0O00000OO0000 =OOOOO0OOO0O0O0O0O .get (db_connect )#line:312
        if dev :#line:313
            if f'{db_connect}{dev}'in OOOOO0OOO0O0O0O0O .keys ():#line:314
                OO0O0O00000OO0000 =OOOOO0OOO0O0O0O0O .get (f'{db_connect}{dev}')#line:315
        O0OOO00O000000OO0 =connect_db_execute ().execute_sql_list (O00O0000O00000O00 ,db_connect ,connect_dict =OO0O0O00000OO0000 )#line:316
        return O0OOO00O000000OO0 #line:317
    except Exception as O0OOO00000OOO00O0 :#line:318
        fun_email ('SQL执行出错',f'{O00O0000O00000O00}{O0OOO00000OOO00O0.args}')#line:319
        print (O0OOO00000OOO00O0 .args )#line:320
        raise SmartPipError ('Run SQL Error')#line:321
def run_sp (O0OOOOOO00O00OOOO ,O0O00000OOO0OOOO0 ,db_connect ='oracle',sp_para =None ,dev =''):#line:1
    try :#line:2
        O0O0OOO0OO0OOOO0O =O0O00000OOO0OOOO0 .get (db_connect )#line:3
        if dev :#line:4
            if f'{db_connect}{dev}'in O0O00000OOO0OOOO0 .keys ():#line:5
                O0O0OOO0OO0OOOO0O =O0O00000OOO0OOOO0 .get (f'{db_connect}{dev}')#line:6
        connect_db_execute ().excute_proc (O0OOOOOO00O00OOOO ,O0O0OOO0OO0OOOO0O ,sp_para )#line:7
    except Exception as O0000O00O0000OO00 :#line:8
        fun_email ('{}执行出错'.format (O0OOOOOO00O00OOOO ),str (O0000O00O0000OO00 .args ))#line:9
        raise O0000O00O0000OO00
def run_kettle (O00000O00O0OOOO0O ,para_str ='',dev =False ):#line:325
    ""#line:332
    O0OOOO00000OOO0OO =O00000O00O0OOOO0O .split ('/')#line:333
    print ('kettle job start')#line:334
    if '.ktr'in O00000O00O0OOOO0O :#line:336
        OOO0000OO000OOO0O =f'{KETTLE_HOME}/pan.sh -level=Basic -file={O00000O00O0OOOO0O}{para_str}'#line:337
    else :#line:338
        OOO0000OO000OOO0O =f'{KETTLE_HOME}/kitchen.sh -level=Basic -file={O00000O00O0OOOO0O}{para_str}'#line:339
    print (OOO0000OO000OOO0O )#line:340
    OOOOOO00O0OO00OOO ,O00OO000OO0OOOOO0 =run_bash (OOO0000OO000OOO0O )#line:344
    if O00OO000OO0OOOOO0 ==0 :#line:345
        print ('{} 完成数据抽取'.format (str (O00000O00O0OOOO0O )))#line:346
    else :#line:347
        print ('{} 执行错误'.format (O00000O00O0OOOO0O ))#line:348
        fun_email ('{}/{}出错'.format (O0OOOO00000OOO0OO [-2 ],O0OOOO00000OOO0OO [-1 ]),str (OOOOOO00O0OO00OOO ))#line:349
        raise SmartPipError ('Run Kettle Error')#line:350
def hdfsStarrocks (O0O0OOO0OO0OO0OOO ,OO0O0O0OO00O0O00O ,para_dict =None ):#line:354
    ""#line:358
    OO00OOOOOOOO0OO0O =O0O0OOO0OO0OO0OOO .split ('/')#line:359
    print ('starrocks load job start')#line:360
    OOOO0OO0OO0OO00OO ,O0OOOOO00O000O0OO =readSqoopFile (O0O0OOO0OO0OO0OOO ,para_dict =para_dict )#line:361
    OOOO0OO0OO0OO00OO =OOOO0OO0OO0OO00OO .split ('\n')#line:362
    OOOO0O00OO000000O ={}#line:363
    OOOO0O00OO000000O ['LABEL']=f'{OO00OOOOOOOO0OO0O[-2]}{OO00OOOOOOOO0OO0O[-1][:-4]}{int(time.time())}'#line:364
    OOOO0O00OO000000O ['HDFS']=HIVE_HOME #line:365
    for O000O0OOOOOO0O0O0 in OOOO0OO0OO0OO00OO :#line:366
        O0O000OO0OOO0O0O0 =O000O0OOOOOO0O0O0 .find ('=')#line:367
        if O0O000OO0OOO0O0O0 >0 :#line:368
            OOOO0O00OO000000O [O000O0OOOOOO0O0O0 [:O0O000OO0OOO0O0O0 ].strip ()]=O000O0OOOOOO0O0O0 [O0O000OO0OOO0O0O0 +1 :].strip ()#line:369
    OO00O00OO0OO0000O =OOOO0O00OO000000O .get ('sleepTime')#line:371
    if OO00O00OO0OO0000O :#line:372
        OO00O00OO0OO0000O =int (OO00O00OO0OO0000O )#line:373
        if OO00O00OO0OO0000O <30 :#line:374
            OO00O00OO0OO0000O =30 #line:375
    else :#line:376
        OO00O00OO0OO0000O =30 #line:377
    OOO00OOOOO00OOO00 =OOOO0O00OO000000O .get ('maxTime')#line:379
    if OOO00OOOOO00OOO00 :#line:380
        OOO00OOOOO00OOO00 =int (OOO00OOOOO00OOO00 )#line:381
        if OOO00OOOOO00OOO00 >3600 :#line:382
            OOO00OOOOO00OOO00 =3600 #line:383
    else :#line:384
        OOO00OOOOO00OOO00 =600 #line:385
    _OO000OO0O0O000OO0 (O0OOOOO00O000O0OO ,OO0O0O0OO00O0O00O ,db_connect ='starrocks',para_dict =OOOO0O00OO000000O )#line:387
    time .sleep (OO00O00OO0OO0000O )#line:388
    OO0O00000O00O0000 =f'''show load from {OOOO0O00OO000000O.get('targetDB')} where label = '{OOOO0O00OO000000O['LABEL']}' order by CreateTime desc limit 1 '''#line:389
    O0OOOO00OOOO000O0 ='start to check label'#line:390
    try :#line:391
        while True :#line:392
            O0OOOO00OOOO000O0 =_OO000OO0O0O000OO0 ([OO0O00000O00O0000 ],OO0O0O0OO00O0O00O ,db_connect ='starrocks')#line:393
            print (O0OOOO00OOOO000O0 )#line:394
            OOOOO0OOOOOO0OOOO =O0OOOO00OOOO000O0 [1 ][2 ]#line:395
            if OOOOO0OOOOOO0OOOO =='CANCELLED':#line:396
                raise Exception (f'Starrocks:{OOOOO0OOOOOO0OOOO}')#line:397
            elif OOOOO0OOOOOO0OOOO =='FINISHED':#line:398
                print ('Load completed')#line:399
                break #line:400
            if OOO00OOOOO00OOO00 <=0 :#line:401
                raise Exception ('超时未完成')#line:402
            else :#line:403
                time .sleep (OO00O00OO0OO0000O )#line:404
                OOO00OOOOO00OOO00 =OOO00OOOOO00OOO00 -OO00O00OO0OO0000O #line:405
    except Exception as O00O0000OO0O0O0O0 :#line:406
        print ('{} 执行错误'.format (O0O0OOO0OO0OO0OOO ))#line:407
        fun_email ('{}/{}执行出错'.format (OO00OOOOOOOO0OO0O [-2 ],OO00OOOOOOOO0OO0O [-1 ]),str (O0OOOO00OOOO000O0 ))#line:408
        raise SmartPipError (str (O00O0000OO0O0O0O0 .args ))#line:409
def kafkaStarrocks (OO00O0OO0OO0OO0OO ,O000OO0OOOOO000OO ,OOO00OOOOO0OO0OOO ,OO0000O0000OOO0OO ,O00OO0OOO0OO0O0O0 ,dev =''):#line:412
    with open (OO00O0OO0OO0OO0OO ,'r',encoding ='utf8')as OOOOO0OO0000OOOO0 :#line:413
        O00O00O00000O0OO0 =readSqlstr (OOOOO0OO0000OOOO0 .read ().strip (),para_dict =O00OO0OOO0OO0O0O0 )#line:414
    O00O00O00000O0OO0 =O00O00O00000O0OO0 .split ('##')#line:415
    O00OO0O00OO0OOO0O ={}#line:416
    for O0O00OOOO0OO000O0 in O00O00O00000O0OO0 :#line:417
        O0000OO0OOO0OOO00 =O0O00OOOO0OO000O0 .find ('=')#line:418
        if O0000OO0OOO0OOO00 >0 :#line:419
            O00O00OO0OO00O0O0 =O0O00OOOO0OO000O0 [O0000OO0OOO0OOO00 +1 :].replace ('\n',' ').strip ()#line:420
            if O00O00OO0OO00O0O0 :#line:421
                O00OO0O00OO0OOO0O [O0O00OOOO0OO000O0 [:O0000OO0OOO0OOO00 ].strip ()]=O00O00OO0OO00O0O0 #line:422
    O000O0000O00O0000 =O00OO0O00OO0OOO0O .pop ('topic')#line:423
    OO000O0O0000OOO00 =O00OO0O00OO0OOO0O .pop ('table')#line:424
    O0O0OO000OOOOOO00 =O00OO0O00OO0OOO0O .keys ()#line:425
    if 'skipError'in O0O0OO000OOOOOO00 :#line:426
        skipError =O00OO0O00OO0OOO0O .pop ('skipError')#line:427
    else :#line:428
        skipError =None #line:429
    if 'kafkaConn'in O0O0OO000OOOOOO00 :#line:430
        O0O0O00OOOO0000O0 =O00OO0O00OO0OOO0O .pop ('kafkaConn')#line:431
    else :#line:432
        O0O0O00OOOO0000O0 ='default'#line:433
    if 'offsets'in O0O0OO000OOOOOO00 :#line:434
        O00O00OO000OOOO00 =json .loads (O00OO0O00OO0OOO0O .pop ('offsets'))#line:435
    else :#line:436
        O00O00OO000OOOO00 =None #line:437
    if 'json_root'in O0O0OO000OOOOOO00 :#line:438
        OO00O0O00O00OO000 =O00OO0O00OO0OOO0O .pop ('json_root')#line:439
    else :#line:440
        OO00O0O00O00OO000 =None #line:441
    if 'jsonpaths'in O0O0OO000OOOOOO00 :#line:442
        O0000000O0O0OOOOO =O00OO0O00OO0OOO0O .get ('jsonpaths')#line:443
        if not O0000000O0O0OOOOO .startswith ('['):#line:444
            O0000000O0O0OOOOO =O0000000O0O0OOOOO .split (',')#line:445
            O0000000O0O0OOOOO =json .dumps (['$.'+OOOOO00O0OO00OO0O .strip ()for OOOOO00O0OO00OO0O in O0000000O0O0OOOOO ])#line:446
            O00OO0O00OO0OOO0O ['jsonpaths']=O0000000O0O0OOOOO #line:447
    OOO0O000O00O0OOO0 =_OO00O0OOO000O00O0 (O000O0000O00O0000 ,O000OO0OOOOO000OO [O0O0O00OOOO0000O0 ],OO0000O0000OOO0OO ,O00O00OO000OOOO00 )#line:448
    def O00O0O00OO00OO0O0 (OOOO0OOOOO00O0OOO ):#line:450
        OO0OOO0O0OOO0OO0O =b''#line:451
        O0OO0OOOO0O0OOOOO =None #line:452
        if 'format'in O0O0OO000OOOOOO00 :#line:453
            for O0OO0OOOO0O0OOOOO in OOOO0OOOOO00O0OOO :#line:454
                O0000OO00OO000OOO =O0OO0OOOO0O0OOOOO .value #line:455
                if OO00O0O00O00OO000 :#line:456
                    O0000OO00OO000OOO =json .loads (O0000OO00OO000OOO .decode ('utf8'))#line:457
                    O0000OO00OO000OOO =json .dumps (O0000OO00OO000OOO [OO00O0O00O00OO000 ]).encode ('utf8')#line:458
                if O0000OO00OO000OOO .startswith (b'['):#line:459
                    OO0OOO0O0OOO0OO0O =OO0OOO0O0OOO0OO0O +b','+O0000OO00OO000OOO [1 :-1 ]#line:460
                else :#line:461
                    OO0OOO0O0OOO0OO0O =OO0OOO0O0OOO0OO0O +b','+O0000OO00OO000OOO #line:462
                if len (OO0OOO0O0OOO0OO0O )>94857600 :#line:463
                    streamStarrocks (OO000O0O0000OOO00 ,OOO00OOOOO0OO0OOO ,O00OO0O00OO0OOO0O ,OO0OOO0O0OOO0OO0O ,skipError )#line:464
                    OOO0O000O00O0OOO0 .write_offset (O0OO0OOOO0O0OOOOO .partition ,O0OO0OOOO0O0OOOOO .offset +1 )#line:465
                    OO0OOO0O0OOO0OO0O =b''#line:466
                if O0OO0OOOO0O0OOOOO .offset ==OOO0O000O00O0OOO0 .end_offset -1 :#line:467
                    break #line:468
        else :#line:469
            for O0OO0OOOO0O0OOOOO in OOOO0OOOOO00O0OOO :#line:470
                O0000OO00OO000OOO =O0OO0OOOO0O0OOOOO .value #line:471
                if OO00O0O00O00OO000 :#line:472
                    O0000OO00OO000OOO =json .loads (O0000OO00OO000OOO .decode ('utf8'))#line:473
                    O0000OO00OO000OOO =json .dumps (O0000OO00OO000OOO [OO00O0O00O00OO000 ]).encode ('utf8')#line:474
                OO0OOO0O0OOO0OO0O =OO0OOO0O0OOO0OO0O +b'\n'+O0000OO00OO000OOO #line:475
                if len (OO0OOO0O0OOO0OO0O )>94857600 :#line:476
                    streamStarrocks (OO000O0O0000OOO00 ,OOO00OOOOO0OO0OOO ,O00OO0O00OO0OOO0O ,OO0OOO0O0OOO0OO0O ,skipError )#line:477
                    OOO0O000O00O0OOO0 .write_offset (O0OO0OOOO0O0OOOOO .partition ,O0OO0OOOO0O0OOOOO .offset +1 )#line:478
                    OO0OOO0O0OOO0OO0O =b''#line:479
                if O0OO0OOOO0O0OOOOO .offset ==OOO0O000O00O0OOO0 .end_offset -1 :#line:480
                    break #line:481
        print (OO0OOO0O0OOO0OO0O [1 :1000 ])#line:482
        if OO0OOO0O0OOO0OO0O :#line:483
            streamStarrocks (OO000O0O0000OOO00 ,OOO00OOOOO0OO0OOO ,O00OO0O00OO0OOO0O ,OO0OOO0O0OOO0OO0O ,skipError )#line:484
        return O0OO0OOOO0O0OOOOO #line:485
    OOO0O000O00O0OOO0 .consumer_topic (O00O0O00OO00OO0O0 )#line:487
def apiStarrocks (O0O0OO0O0OO0000O0 ,O00O0OOO0O0OOO00O ,O0000O00O0000O0OO ,OOO0OO00O0OOOOO00 ):#line:490
    with open (O0O0OO0O0OO0000O0 ,'r',encoding ='utf8')as O0O0OO0O000OO0000 :#line:491
        OO0OO0O0O0000OOOO =readSqlstr (O0O0OO0O000OO0000 .read ().strip (),para_dict =OOO0OO00O0OOOOO00 )#line:492
    OO0OO0O0O0000OOOO =OO0OO0O0O0000OOOO .split ('##')#line:493
    O00O0OO000OO00OOO ={}#line:494
    for O0000000O00OO000O in OO0OO0O0O0000OOOO :#line:495
        O00OOO0OO00000O0O =O0000000O00OO000O .find ('=')#line:496
        if O00OOO0OO00000O0O >0 :#line:497
            O00000O00O0O0O00O =O0000000O00OO000O [O00OOO0OO00000O0O +1 :].replace ('\n',' ').strip ()#line:498
            if O00000O00O0O0O00O :#line:499
                O00O0OO000OO00OOO [O0000000O00OO000O [:O00OOO0OO00000O0O ].strip ()]=O00000O00O0O0O00O #line:500
    OOO00O0000O00OO00 =O00O0OO000OO00OOO .pop ('table')#line:501
    OOOOO0O0O00000000 =O00O0OO000OO00OOO .keys ()#line:502
    if 'param'in OOOOO0O0O00000000 :#line:503
        OOO00O0O00OO0OO0O =O00O0OO000OO00OOO .pop ('param')#line:504
    else :#line:505
        OOO00O0O00OO0OO0O =None #line:506
    if 'apiConn'in OOOOO0O0O00000000 :#line:507
        O0O000000O000OO00 =O00O0OO000OO00OOO .pop ('apiConn')#line:508
    else :#line:509
        O0O000000O000OO00 ='default'#line:510
    if 'skipError'in OOOOO0O0O00000000 :#line:511
        skipError =O00O0OO000OO00OOO .pop ('skipError')#line:512
    else :#line:513
        skipError =None #line:514
    if 'jsonpaths'in OOOOO0O0O00000000 :#line:515
        O0OOO0O000O000000 =O00O0OO000OO00OOO .get ('jsonpaths')#line:516
        if not O0OOO0O000O000000 .startswith ('['):#line:517
            O0OOO0O000O000000 =O0OOO0O000O000000 .split (',')#line:518
            O0OOO0O000O000000 =json .dumps (['$.'+O0OO0O00OO0000O0O .strip ()for O0OO0O00OO0000O0O in O0OOO0O000O000000 ])#line:519
            O00O0OO000OO00OOO ['jsonpaths']=O0OOO0O000O000000 #line:520
    OOOO00O00000OOOOO =O00O0OOO0O0OOO00O [O0O000000O000OO00 ](OOO00O0O00OO0OO0O )#line:521
    if OOOO00O00000OOOOO :#line:522
        streamStarrocks (OOO00O0000O00OO00 ,O0000O00O0000O0OO ,O00O0OO000OO00OOO ,OOOO00O00000OOOOO ,skipError )#line:523
    else :#line:524
        print ('无数据')#line:525
def streamStarrocks (OO0OOO0OOOO00OO0O ,O00O0OO0O0O000OO0 ,O0O0000OOOOOOOOOO ,OO000OO0000O00000 ,skipError =False ):#line:528
    ""#line:531
    import base64 ,uuid #line:532
    O0O0O0O0OOOOOOOO0 ,OO0OOO0OOOO00OO0O =OO0OOO0OOOO00OO0O .split ('.')#line:533
    O00O0OOOOO00O0O00 =str (base64 .b64encode (f'{O00O0OO0O0O000OO0["user"]}:{O00O0OO0O0O000OO0["password"]}'.encode ('utf-8')),'utf-8')#line:534
    OO000OO0000O00000 =OO000OO0000O00000 .strip ()#line:535
    if OO000OO0000O00000 .startswith (b','):#line:536
        O0O0000OOOOOOOOOO ['strip_outer_array']='true'#line:537
        OO000OO0000O00000 =b'['+OO000OO0000O00000 [1 :]+b']'#line:538
    O0OO0OOOO00000O00 ={'Content-Type':'application/json','Authorization':f'Basic {O00O0OOOOO00O0O00}','label':f'{OO0OOO0OOOO00OO0O}{uuid.uuid4()}',**O0O0000OOOOOOOOOO }#line:544
    O0O0O0OOOO00O0O0O =f"{O00O0OO0O0O000OO0['url']}/api/{O0O0O0O0OOOOOOOO0}/{OO0OOO0OOOO00OO0O}/_stream_load"#line:545
    print ('start loading to starrocks....')#line:546
    O0O0O00OO00000OOO =requests .put (O0O0O0OOOO00O0O0O ,headers =O0OO0OOOO00000O00 ,data =OO000OO0000O00000 ).json ()#line:547
    print (O0O0O00OO00000OOO )#line:548
    if O0O0O00OO00000OOO ['Status']=='Fail':#line:549
        if skipError :#line:550
            print (f'Starrocks Load Error, Skip this offset')#line:551
        else :#line:552
            raise Exception ('Starrocks Load Error')#line:553
def routineStarrocks (OOOO0O0O0OO0000O0 ,OO0O0OO00O00O0OOO ,flag =''):#line:556
    O0000OOO0O000O000 =_OO000OO0O0O000OO0 ([f'SHOW ROUTINE LOAD FOR {OO0O0OO00O00O0OOO}'],OOOO0O0O0OO0000O0 ,db_connect ='starrocks')#line:557
    O0000OOO0O000O000 =dict (zip (O0000OOO0O000O000 [0 ],O0000OOO0O000O000 [1 ]))#line:558
    print ('状态:',O0000OOO0O000O000 ['State'])#line:559
    print ('统计:',O0000OOO0O000O000 ['Statistic'])#line:560
    print ('进度:',O0000OOO0O000O000 ['Progress'])#line:561
    if O0000OOO0O000O000 ['State']!='RUNNING':#line:562
        print ('ERROR: ',O0000OOO0O000O000 ['ReasonOfStateChanged'])#line:563
        if not flag :#line:564
            raise Exception ('Starrocks Routin Load')#line:565
from airflow .utils .session import provide_session #line:571
@provide_session #line:572
def point_test (OOO000OOOO0O000OO ,sleeptime ='',maxtime ='',session =None ):#line:573
    ""#line:580
    if sleeptime :#line:581
        sleeptime =int (sleeptime )#line:582
        sleeptime =sleeptime if sleeptime >60 else 60 #line:583
    if maxtime :#line:584
        maxtime =int (maxtime )#line:585
        maxtime =maxtime if maxtime <60 *60 *2 else 60 *60 *2 #line:586
    else :#line:587
        maxtime =0 #line:588
    try :#line:589
        OOO000OO0O0O000OO =f"select start_date,state from dag_run where dag_id ='{OOO000OOOO0O000OO}' ORDER BY id desc LIMIT 1"#line:590
        while True :#line:591
            O0O00OO0OOOO0OOOO =session .execute (OOO000OO0O0O000OO ).fetchall ()#line:592
            if O0O00OO0OOOO0OOOO [0 ][1 ]!='success':#line:593
                if maxtime >0 and O0O00OO0OOOO0OOOO [0 ][1 ]!='failed':#line:594
                    print ('waiting...'+O0O00OO0OOOO0OOOO [0 ][1 ])#line:595
                    time .sleep (sleeptime )#line:596
                    maxtime =maxtime -sleeptime #line:597
                else :#line:598
                    O000OOO00OOO0O000 =O0O00OO0OOOO0OOOO [0 ][0 ].strftime ("%Y-%m-%d %H:%M:%S")#line:599
                    OO0000OO00OOOO0OO ='所依赖的dag:'+OOO000OOOO0O000OO +',状态为'+O0O00OO0OOOO0OOOO [0 ][1 ]+'.其最新的执行时间为'+O000OOO00OOO0O000 #line:600
                    fun_email (OO0000OO00OOOO0OO ,'前置DAG任务未成功')#line:601
                    print (OO0000OO00OOOO0OO )#line:602
                    raise SmartPipError ('Run DAG validate Error')#line:603
            else :#line:604
                print ('success...')#line:605
                break #line:606
    except Exception as O0OO000O0OO0O0O00 :#line:607
        print (O0OO000O0OO0O0O00 .args )#line:608
        raise SmartPipError ('DAG validate Error')#line:609
class connect_db_execute ():#line:614
    def __init__ (O0OO0OO000O000OO0 ,dev =False ,db =''):#line:615
        O0OO0OO000O000OO0 .dev =dev #line:616
    def insert_contents (OOO000OOO00000OO0 ,OO0O00O0O00000O0O ,OO000O0OOO0O0O0O0 ,per_in =1000 ,connect_dict =None ):#line:618
        OO0O0O000OOOO0OOO =time .time ()#line:619
        logging .info ('starting to execute insert contents...')#line:620
        if isinstance (connect_dict ,dict ):#line:621
            O0OO0O0000OO000OO =connect_dict ['dbtype']#line:622
        else :#line:623
            if connect_dict =='':#line:624
                O0OO0O0000OO000OO ='oracle'#line:625
            else :#line:626
                O0OO0O0000OO000OO =connect_dict #line:627
            connect_dict =None #line:628
        O0OO00O0O0000000O =getattr (OOO000OOO00000OO0 ,'insert_contents_'+O0OO0O0000OO000OO )#line:629
        OO0O0OOO0OOO00O0O =O0OO00O0O0000000O (OO0O00O0O00000O0O ,OO000O0OOO0O0O0O0 ,per_in ,connect_dict )#line:630
        logging .info ('execute insert contents time : {}ms'.format (time .time ()-OO0O0O000OOOO0OOO ))#line:631
        return OO0O0OOO0OOO00O0O #line:632
    def impala (OO0OOO0OO00O00OO0 ,OOOO0OO0OOOOO0O00 ,connect_dict =None ):#line:634
        ""#line:635
        from impala .dbapi import connect as impala #line:636
        O000O0O00OOO0OOO0 =impala (user =connect_dict ['user'],password =connect_dict ['password'],host =connect_dict ['host'],port =int (connect_dict ['port']),auth_mechanism ='PLAIN')#line:643
        O0OOO000O00O0O0OO =O000O0O00OOO0OOO0 .cursor ()#line:644
        O00000000000OOO00 =r'^insert\s|^update\s|^truncate\s|^delete\s|^load\s|^refresh\s|^upsert\s'#line:645
        O0O0OOO0O000OOO00 =None #line:646
        for O00OOOOOOO0O0O00O in OOOO0OO0OOOOO0O00 :#line:647
            print (O00OOOOOOO0O0O00O )#line:648
            O00OOOOOOO0O0O00O =O00OOOOOOO0O0O00O .strip ()#line:649
            if not O00OOOOOOO0O0O00O :#line:650
                continue #line:651
            if re .search (O00000000000OOO00 ,O00OOOOOOO0O0O00O ,re .I |re .IGNORECASE ):#line:652
                O0OOO000O00O0O0OO .execute (O00OOOOOOO0O0O00O )#line:653
            else :#line:654
                O0OOO000O00O0O0OO .execute (O00OOOOOOO0O0O00O )#line:655
                try :#line:656
                    O0O0OOO0O000OOO00 =O0OOO000O00O0O0OO .fetchall ()#line:657
                except Exception as O0OOO000OOO00000O :#line:658
                    print (O0OOO000OOO00000O .args )#line:659
        O000O0O00OOO0OOO0 .close ()#line:660
        return O0O0OOO0O000OOO00 #line:661
    def hive (OOO0O00O00OO000O0 ,O0OOOO0OOO00O000O ,connect_dict =None ):#line:663
        ""#line:664
        from impala .dbapi import connect as impala #line:665
        O0OOOOO0O0O0O0O0O =impala (user =connect_dict ['user'],password =connect_dict ['password'],host =connect_dict ['host'],port =int (connect_dict ['port']),auth_mechanism ='PLAIN')#line:672
        OOOO0OO0OO0OOO0OO =O0OOOOO0O0O0O0O0O .cursor ()#line:673
        O00000O0O0000O0O0 =r'^insert\s|^update\s|^truncate\s|^delete\s|^load\s'#line:674
        OO0OOOOO0OOOOOOOO =None #line:675
        for O0O0000OOOOOO0000 in O0OOOO0OOO00O000O :#line:676
            O0O0000OOOOOO0000 =O0O0000OOOOOO0000 .strip ()#line:677
            if not O0O0000OOOOOO0000 :#line:678
                continue #line:679
            print (O0O0000OOOOOO0000 )#line:680
            if O0O0000OOOOOO0000 .startswith ('refresh'):#line:681
                connect_dict ['port']=21050 #line:682
                OOO0O00O00OO000O0 .impala ([O0O0000OOOOOO0000 ],connect_dict =connect_dict )#line:683
            else :#line:684
                if re .search (O00000O0O0000O0O0 ,O0O0000OOOOOO0000 ,re .I |re .IGNORECASE ):#line:685
                    OOOO0OO0OO0OOO0OO .execute (O0O0000OOOOOO0000 )#line:686
                else :#line:687
                    OOOO0OO0OO0OOO0OO .execute (O0O0000OOOOOO0000 )#line:688
                    try :#line:689
                        OO0OOOOO0OOOOOOOO =OOOO0OO0OO0OOO0OO .fetchall ()#line:690
                    except Exception as OOOO00O0OO0O0OOO0 :#line:691
                        print (OOOO00O0OO0O0OOO0 .args )#line:692
        O0OOOOO0O0O0O0O0O .close ()#line:693
        return OO0OOOOO0OOOOOOOO #line:694
    def mysql (O0OOO000000O000O0 ,OOOO0O0O0OO0O000O ,connect_dict =None ):#line:696
        import pymysql #line:697
        OOO00O0O000O0O00O =pymysql .connect (user =connect_dict ['user'],password =connect_dict ['password'],host =connect_dict ['host'],port =connect_dict ['port'],database =connect_dict ['db'])#line:704
        try :#line:705
            O0O000OO00OO0OOOO =OOO00O0O000O0O00O .cursor ()#line:706
            OO0000O0O0OO000O0 =r'^insert\s|^update\s|^truncate\s|^delete\s|^load\s'#line:707
            for O000O0O0OOOO0O000 in OOOO0O0O0OO0O000O :#line:708
                O000O0O0OOOO0O000 =O000O0O0OOOO0O000 .strip ()#line:709
                if not O000O0O0OOOO0O000 :#line:710
                    continue #line:711
                print (O000O0O0OOOO0O000 )#line:712
                if re .search (OO0000O0O0OO000O0 ,O000O0O0OOOO0O000 ,re .I |re .IGNORECASE ):#line:713
                    try :#line:714
                        O0O000OO00OO0OOOO .execute (O000O0O0OOOO0O000 )#line:715
                        OOO00O0O000O0O00O .commit ()#line:716
                    except Exception as OOOOO00OO00000000 :#line:717
                        OOO00O0O000O0O00O .rollback ()#line:718
                        raise OOOOO00OO00000000 #line:719
                else :#line:720
                    O0O000OO00OO0OOOO .execute (O000O0O0OOOO0O000 )#line:721
                    O0O0O000O0000OO00 =O0O000OO00OO0OOOO .fetchall ()#line:722
                    O0O0O000O0000OO00 =[[OO00OOO0000O0OO00 [0 ]for OO00OOO0000O0OO00 in O0O000OO00OO0OOOO .description ]]+list (O0O0O000O0000OO00 )#line:723
                    return O0O0O000O0000OO00 #line:724
        except Exception as O0O000000O0OOOO00 :#line:725
            raise O0O000000O0OOOO00 #line:726
        finally :#line:727
            OOO00O0O000O0O00O .close ()#line:728
    def starrocks (O0OOO000O0O0O0O00 ,OO0O0O0OOO0O000O0 ,connect_dict =None ):#line:730
        return O0OOO000O0O0O0O00 .mysql (OO0O0O0OOO0O000O0 ,connect_dict )#line:731
    def oracle (O00O0OO00O00O0OOO ,OO00O00O00OOO0OO0 ,connect_dict =None ):#line:733
        import cx_Oracle #line:734
        O00OOOO00000O000O ='{}/{}@{}/{}'.format (connect_dict ['user'],connect_dict ['password'],connect_dict ['host'],connect_dict ['db'])#line:739
        O00000OO00O00O000 =cx_Oracle .connect (O00OOOO00000O000O )#line:740
        try :#line:741
            OO0OO0OOO00O00OOO =O00000OO00O00O000 .cursor ()#line:742
            O00O0OOO0000OOO0O =r'^insert\s|^update\s|^truncate\s|^delete\s|^comment\s'#line:743
            for OO0O00OO0000OOOO0 in OO00O00O00OOO0OO0 :#line:744
                OO0O00OO0000OOOO0 =OO0O00OO0000OOOO0 .strip ()#line:745
                if not OO0O00OO0000OOOO0 :#line:746
                    continue #line:747
                if re .search (O00O0OOO0000OOO0O ,OO0O00OO0000OOOO0 ,re .I ):#line:748
                    try :#line:749
                        OO0OO0OOO00O00OOO .execute (OO0O00OO0000OOOO0 )#line:750
                        O00000OO00O00O000 .commit ()#line:751
                    except Exception as O0O000OO0O0OOOO00 :#line:752
                        if OO0O00OO0000OOOO0 .startswith ('comment'):#line:753
                            print ('err:',OO0O00OO0000OOOO0 )#line:754
                            continue #line:755
                        O00000OO00O00O000 .rollback ()#line:756
                        raise O0O000OO0O0OOOO00 #line:757
                else :#line:758
                    OO0OO0OOO00O00OOO .execute (OO0O00OO0000OOOO0 )#line:759
                    O0OO0O000OOOO0000 =OO0OO0OOO00O00OOO .fetchall ()#line:760
                    O0OO0O000OOOO0000 =[[O00OO000O00OO0000 [0 ]for O00OO000O00OO0000 in OO0OO0OOO00O00OOO .description ]]+list (O0OO0O000OOOO0000 )#line:761
                    return O0OO0O000OOOO0000 #line:762
        except Exception as OOO0000OOO0OOO0O0 :#line:763
            raise OOO0000OOO0OOO0O0 #line:764
        finally :#line:765
            O00000OO00O00O000 .close ()#line:766
    def gp (O0OOOO00OO00O00O0 ,O000O00O000OO0OOO ,connect_dict =None ):#line:768
        import psycopg2 #line:769
        O0OO000O00000O0OO =psycopg2 .connect (user =connect_dict ['user'],password =connect_dict ['password'],host =connect_dict ['host'],port =connect_dict ['port'],database =connect_dict ['db'])#line:776
        try :#line:777
            O00O00000000O00O0 =O0OO000O00000O0OO .cursor ()#line:778
            OOOOO0O0OOOOO0O00 =r'^insert\s|^update\s|^truncate\s|^delete\s'#line:779
            for OOO0OO000OOOOO0OO in O000O00O000OO0OOO :#line:780
                OOO0OO000OOOOO0OO =OOO0OO000OOOOO0OO .strip ()#line:781
                if not OOO0OO000OOOOO0OO :#line:782
                    continue #line:783
                if re .search (OOOOO0O0OOOOO0O00 ,OOO0OO000OOOOO0OO ,re .I |re .IGNORECASE ):#line:784
                    try :#line:785
                        O00O00000000O00O0 .execute (OOO0OO000OOOOO0OO )#line:786
                        O0OO000O00000O0OO .commit ()#line:787
                    except Exception as OOO0OOOO0OO0O0000 :#line:788
                        O0OO000O00000O0OO .rollback ()#line:789
                        raise OOO0OOOO0OO0O0000 #line:790
                else :#line:791
                    O00O00000000O00O0 .execute (OOO0OO000OOOOO0OO )#line:792
                    OO0000OOO000O0OO0 =O00O00000000O00O0 .fetchall ()#line:793
                    OO0000OOO000O0OO0 =[[O00O0O00O0O0000O0 [0 ]for O00O0O00O0O0000O0 in O00O00000000O00O0 .description ]]+list (OO0000OOO000O0OO0 )#line:794
                    return OO0000OOO000O0OO0 #line:795
        except Exception as OOO0000000O00O00O :#line:796
            raise OOO0000000O00O00O #line:797
        finally :#line:798
            O0OO000O00000O0OO .close ()#line:799
    def mssql (O0OO00O0000OOO0OO ,O00OO00O000O0OO00 ,connect_dict =None ):#line:801
        import pymssql #line:802
        if connect_dict ['port']:#line:803
            O00OO0OOOO00OOO00 =pymssql .connect (user =connect_dict ['user'],password =connect_dict ['password'],host =connect_dict ['host'],port =int (connect_dict ['port']),database =connect_dict ['db'],charset ="utf8",)#line:811
        else :#line:812
            O00OO0OOOO00OOO00 =pymssql .connect (user =connect_dict ['user'],password =connect_dict ['password'],host =connect_dict ['host'],database =connect_dict ['db'],charset ="utf8",)#line:819
        try :#line:820
            OO00000O00000O0O0 =O00OO0OOOO00OOO00 .cursor ()#line:821
            OO0O0OOOOOO0O0OOO =r'^insert\s|^update\s|^truncate\s|^delete\s'#line:822
            for O0O0OOOOOOO0000OO in O00OO00O000O0OO00 :#line:823
                O0O0OOOOOOO0000OO =O0O0OOOOOOO0000OO .strip ()#line:824
                if not O0O0OOOOOOO0000OO :#line:825
                    continue #line:826
                if re .search (OO0O0OOOOOO0O0OOO ,O0O0OOOOOOO0000OO ,re .I |re .IGNORECASE ):#line:827
                    try :#line:828
                        OO00000O00000O0O0 .execute (O0O0OOOOOOO0000OO )#line:829
                        O00OO0OOOO00OOO00 .commit ()#line:830
                    except Exception as O00O0000OO0O00OO0 :#line:831
                        O00OO0OOOO00OOO00 .rollback ()#line:832
                        raise O00O0000OO0O00OO0 #line:833
                else :#line:834
                    OO00000O00000O0O0 .execute (O0O0OOOOOOO0000OO )#line:835
                    OO0OOOO00OOO00OOO =OO00000O00000O0O0 .fetchall ()#line:836
                    OO0OOOO00OOO00OOO =[[O0O0O00OOOO00O00O [0 ]for O0O0O00OOOO00O00O in OO00000O00000O0O0 .description ]]+list (OO0OOOO00OOO00OOO )#line:837
                    return OO0OOOO00OOO00OOO #line:838
        except Exception as O00OOO0000O000O00 :#line:839
            raise O00OOO0000O000O00 #line:840
        finally :#line:841
            O00OO0OOOO00OOO00 .close ()#line:842
    def execute_sql_list (O0OO000000O00OO0O ,OO000000OO00O0O0O ,db_connect ='',connect_dict =None ):#line:844
        if db_connect =='':db_connect ='oracle'#line:845
        O0OOO00OOOO00OOO0 =getattr (O0OO000000O00OO0O ,db_connect )#line:846
        return O0OOO00OOOO00OOO0 (OO000000OO00O0O0O ,connect_dict =connect_dict )#line:847
    def excute_proc (O0O0O000O000O00OO ,O00OO000OO0OOO000 ,O0O0000O00O0OO0OO ,proc_para =None ):#line:849
        import cx_Oracle #line:850
        OOO0OO0OO0OO0OOOO ='{}/{}@{}/{}'.format (O0O0000O00O0OO0OO ['user'],O0O0000O00O0OO0OO ['password'],O0O0000O00O0OO0OO ['host'],O0O0000O00O0OO0OO ['db'])#line:856
        OOO0OOOO0O0O0O000 =cx_Oracle .connect (OOO0OO0OO0OO0OOOO )#line:857
        try :#line:859
            OO0000O0OOOOO0O0O =OOO0OOOO0O0O0O000 .cursor ()#line:860
            print ("开始执行过程:{}  参数: {}".format (O00OO000OO0OOO000 ,proc_para ))#line:861
            if proc_para is None :#line:862
                OOOO00000O0OO00O0 =OO0000O0OOOOO0O0O .callproc (O00OO000OO0OOO000 )#line:863
                OOO0OOOO0O0O0O000 .commit ()#line:864
            else :#line:865
                OOOO00000O0OO00O0 =OO0000O0OOOOO0O0O .callproc (O00OO000OO0OOO000 ,proc_para )#line:867
                OOO0OOOO0O0O0O000 .commit ()#line:868
            OO0000O0OOOOO0O0O .close ()#line:869
            OOO0OOOO0O0O0O000 .close ()#line:870
            print (OOOO00000O0OO00O0 )#line:871
        except Exception as OOO00O0OOO000O000 :#line:872
            OOO0OOOO0O0O0O000 .rollback ()#line:873
            OOO0OOOO0O0O0O000 .close ()#line:874
            raise OOO00O0OOO000O000 #line:876
        return True #line:877
    def insert_contents_oracle (O0O0000OO00OO0O0O ,OOO0000OO00OOO000 ,OOOOOOO0OOOOO00O0 ,per_in =100 ,connect_dict =None ):#line:879
        import cx_Oracle #line:880
        OO000O00O0OO00OO0 ='{}/{}@{}:{}/{}'.format (connect_dict ['user'],connect_dict ['password'],connect_dict ['host'],connect_dict ['port'],connect_dict ['db'])#line:886
        O0O0OO0OO0O0OOO0O =cx_Oracle .connect (OO000O00O0OO00OO0 )#line:887
        OO0000O0000OO0O00 =O0O0OO0OO0O0OOO0O .cursor ()#line:888
        O00OO0000O00OO00O =' into {} values {}'#line:889
        O0OO00OOOOOOO0000 =''#line:890
        OOO0O000OOOOOOO00 =len (OOO0000OO00OOO000 )#line:891
        logging .info ("total {} records need to insert table {}: ".format (OOO0O000OOOOOOO00 ,OOOOOOO0OOOOO00O0 ))#line:892
        try :#line:893
            for OO0OO0000O0O0OOOO in range (OOO0O000OOOOOOO00 ):#line:894
                O0OO00OOOOOOO0000 =O0OO00OOOOOOO0000 +O00OO0000O00OO00O .format (OOOOOOO0OOOOO00O0 ,tuple (OOO0000OO00OOO000 [OO0OO0000O0O0OOOO ]))+'\n'#line:895
                if (OO0OO0000O0O0OOOO +1 )%per_in ==0 or OO0OO0000O0O0OOOO ==OOO0O000OOOOOOO00 -1 :#line:896
                    OO0O0O00O00OOOOOO ='insert all '+O0OO00OOOOOOO0000 +'select 1 from dual'#line:897
                    logging .debug (OO0O0O00O00OOOOOO )#line:898
                    OO0000O0000OO0O00 .execute (OO0O0O00O00OOOOOO )#line:899
                    O0O0OO0OO0O0OOO0O .commit ()#line:900
                    O0OO00OOOOOOO0000 =''#line:901
            return str (OOO0O000OOOOOOO00 )#line:902
        except Exception as O0O0O0O000OOO0000 :#line:903
            try :#line:904
                O0O0OO0OO0O0OOO0O .rollback ()#line:905
                OO0000O0000OO0O00 .execute ("delete from {} where UPLOADTIME = '{}'".format (OOOOOOO0OOOOO00O0 ,OOO0000OO00OOO000 [0 ][-1 ]))#line:906
                O0O0OO0OO0O0OOO0O .commit ()#line:907
            except Exception :#line:908
                logging .error ('can not delete by uploadtime')#line:909
            finally :#line:910
                raise O0O0O0O000OOO0000 #line:911
        finally :#line:912
            O0O0OO0OO0O0OOO0O .close ()#line:913
class _OO00O0OOO000O00O0 (object ):#line:917
    connect =None #line:918
    def __init__ (OO0OOO00O0O0OOOOO ,O00OOOO00000OO000 ,O00OO0OO00OO0O000 ,OOO00O00O0OOO0000 ,offsets =None ):#line:920
        OO0OOO00O0O0OOOOO .end_offset =None #line:921
        OO0OOO00O0O0OOOOO .db_err_count =0 #line:922
        OO0OOO00O0O0OOOOO .topic =O00OOOO00000OO000 #line:923
        OO0OOO00O0O0OOOOO .kafkaconfig =O00OO0OO00OO0O000 #line:924
        OO0OOO00O0O0OOOOO .offsetDict ={}#line:925
        OO0OOO00O0O0OOOOO .current_dir =OOO00O00O0OOO0000 #line:926
        OO0OOO00O0O0OOOOO .offsets =offsets #line:927
        try :#line:928
            OO0OOO00O0O0OOOOO .consumer =OO0OOO00O0O0OOOOO .connect_kafka_customer ()#line:929
        except Exception as OO00OO0O0OOO0O00O :#line:930
            OO00OO0O0OOO0O00O ='kafka无法连接','ErrLocation：{}\n'.format (O00OOOO00000OO000 )+str (OO00OO0O0OOO0O00O )+',kafka消费者无法创建'#line:931
            raise OO00OO0O0OOO0O00O #line:932
    def get_toggle_or_offset (OO0O0O0OOOO00OO0O ,OO0O000OOOOO00O0O ,O0000OOOOOO0O0O0O ):#line:934
        ""#line:935
        if OO0O0O0OOOO00OO0O .offsets :#line:936
            if isinstance (OO0O0O0OOOO00OO0O .offsets ,int ):#line:937
                return OO0O0O0OOOO00OO0O .offsets #line:938
            else :#line:939
                O0O0O00OOO00OOOOO =OO0O0O0OOOO00OO0O .offsets .get (str (O0000OOOOOO0O0O0O ))#line:940
                if O0O0O00OOO00OOOOO is not None :#line:941
                    return int(O0O0O00OOO00OOOOO) #line:942
        O0O0O00OOO00OOOOO =0 #line:943
        try :#line:944
            OOO0O0000O0O000OO =f"{OO0O0O0OOOO00OO0O.current_dir}/kafka/{OO0O000OOOOO00O0O}_offset_{O0000OOOOOO0O0O0O}.txt"#line:945
            if os .path .exists (OOO0O0000O0O000OO ):#line:946
                O000O0O0O000OOOO0 =open (OOO0O0000O0O000OO ).read ()#line:947
                if O000O0O0O000OOOO0 :#line:948
                    O0O0O00OOO00OOOOO =int (O000O0O0O000OOOO0 )#line:949
            else :#line:950
                with open (OOO0O0000O0O000OO ,encoding ='utf-8',mode ='a')as O0OO0O0OO000O0O0O :#line:951
                    O0OO0O0OO000O0O0O .close ()#line:952
        except Exception as OO000OOOO0OOO0OOO :#line:953
            print (f"读取失败：{OO000OOOO0OOO0OOO}")#line:954
            raise OO000OOOO0OOO0OOO #line:955
        return O0O0O00OOO00OOOOO #line:956
    def write_offset (OOOO0OOO0OOO00000 ,OO0O00OO0O00O00OO ,offset =None ):#line:958
        ""#line:961
        if OOOO0OOO0OOO00000 .topic and offset :#line:962
            OOO0OOO000OO0OO0O =f"{OOOO0OOO0OOO00000.current_dir}/kafka/{OOOO0OOO0OOO00000.topic}_offset_{OO0O00OO0O00O00OO}.txt"#line:964
            try :#line:965
                with open (OOO0OOO000OO0OO0O ,'w')as OO000O000O0O0OOOO :#line:966
                    OO000O000O0O0OOOO .write (str (offset ))#line:967
                    OO000O000O0O0OOOO .close ()#line:968
            except Exception as OO0O000O0OO0O0O0O :#line:969
                print (f"写入offset出错：{OO0O000O0OO0O0O0O}")#line:970
                raise OO0O000O0OO0O0O0O #line:971
    def connect_kafka_customer (O0OOOO00O0O000O00 ):#line:973
        ""#line:974
        OO0OO00O000O0O000 =KafkaConsumer (**O0OOOO00O0O000O00 .kafkaconfig )#line:975
        return OO0OO00O000O0O000 #line:976
    def parse_data (O0OOO000OO0000000 ,OO0000O000O000O0O ):#line:978
        ""#line:983
        return dict ()#line:984
    def gen_sql (OOO00OOO0O0O00OO0 ,O000OO00O000O0OO0 ):#line:986
        ""#line:991
        O0000000OOO0O0000 =[]#line:992
        for O00OOO0O0OO0OO0OO in O000OO00O000O0OO0 :#line:993
            O0000000OOO0O0000 .append (str (tuple (O00OOO0O0OO0OO0OO )))#line:995
        return ','.join (O0000000OOO0O0000 )#line:996
    def dispose_kafka_data (OO000OO0OO0O000OO ,OO00OOO000O0OO0OO ):#line:998
        ""#line:1003
        pass #line:1004
    def get_now_time (OO000OOOO0O0OOO00 ):#line:1006
        ""#line:1010
        O000000O0O0OO0OOO =int (time .time ())#line:1011
        return time .strftime ('%Y-%m-%d %H:%M:%S',time .localtime (O000000O0O0OO0OOO ))#line:1012
    def tran_data (O000OOOO000O0OOOO ,O00OOOOOOO00OOOOO ,OOO00O0OOO0OOOO0O ):#line:1014
        ""#line:1020
        O0OOOO0000OOO0000 =O00OOOOOOO00OOOOO .get (OOO00O0OOO0OOOO0O ,"")#line:1021
        O0OOOO0000OOO0000 =""if O0OOOO0000OOO0000 is None else O0OOOO0000OOO0000 #line:1022
        return str (O0OOOO0000OOO0000 )#line:1023
    def consumer_data (O00OOOOOOO00000O0 ,OOOO0OOOO0OO00O00 ,O0O00000O0O00O00O ,OO0O000O0O0O0OOO0 ):#line:1025
        ""#line:1032
        if O00OOOOOOO00000O0 .consumer :#line:1033
            O00OOOOOOO00000O0 .consumer .assign ([TopicPartition (topic =O00OOOOOOO00000O0 .topic ,partition =OOOO0OOOO0OO00O00 )])#line:1034
            O000O0O00O0O00OOO =TopicPartition (topic =O00OOOOOOO00000O0 .topic ,partition =OOOO0OOOO0OO00O00 )#line:1036
            OOO000O0OO00O0OOO =O00OOOOOOO00000O0 .consumer .beginning_offsets ([O000O0O00O0O00OOO ])#line:1037
            OO0O0OOO0O0OO0O00 =OOO000O0OO00O0OOO .get (O000O0O00O0O00OOO )#line:1038
            O000OOO0O00OOO0O0 =O00OOOOOOO00000O0 .consumer .end_offsets ([O000O0O00O0O00OOO ])#line:1039
            OO0O0OOO00O0000OO =O000OOO0O00OOO0O0 .get (O000O0O00O0O00OOO )#line:1040
            print (f'建立消费者, {OOOO0OOOO0OO00O00}分区, 最小offset:{OO0O0OOO0O0OO0O00}, 最大offset:{OO0O0OOO00O0000OO}')#line:1041
            if O0O00000O0O00O00O == -996:
                O0O00000O0O00O00O = OO0O0OOO00O0000OO - 1
            if O0O00000O0O00O00O <OO0O0OOO0O0OO0O00 :#line:1042
                print (f'Warning: 消费offset：{O0O00000O0O00O00O} 小于最小offset:{OO0O0OOO0O0OO0O00}')#line:1043
                O0O00000O0O00O00O =OO0O0OOO0O0OO0O00 #line:1044
            if O0O00000O0O00O00O >=OO0O0OOO00O0000OO :#line:1045
                print (f'消费offset：{O0O00000O0O00O00O} 大于最大offset:{OO0O0OOO00O0000OO}, 本次不消费')#line:1046
                return #line:1050
            O00OOOOOOO00000O0 .end_offset =OO0O0OOO00O0000OO #line:1051
            O00OOOOOOO00000O0 .consumer .seek (TopicPartition (topic =O00OOOOOOO00000O0 .topic ,partition =OOOO0OOOO0OO00O00 ),offset =O0O00000O0O00O00O )#line:1052
            print (f'消费{OOOO0OOOO0OO00O00}分区, 开始消费offset：{O0O00000O0O00O00O}!')#line:1053
            O0OOOOO0OO0OO00O0 =OO0O000O0O0O0OOO0 (O00OOOOOOO00000O0 .consumer )#line:1054
            O0O00000O0O00O00O =O0OOOOO0OO0OO00O0 .offset +1 #line:1055
            O00OOOOOOO00000O0 .offsetDict [OOOO0OOOO0OO00O00 ]=O0O00000O0O00O00O #line:1058
            O00OOOOOOO00000O0 .write_offset (OOOO0OOOO0OO00O00 ,O0O00000O0O00O00O )#line:1059
            O00OOOOOOO00000O0 .offsetDict [OOOO0OOOO0OO00O00 ]=O0O00000O0O00O00O #line:1062
            O00OOOOOOO00000O0 .write_offset (OOOO0OOOO0OO00O00 ,O0O00000O0O00O00O )#line:1063
    def consumer_topic (OOO00O0OOOO00OOO0 ,OO00O00OOO0000O0O ):#line:1065
        print (f"topic: {OOO00O0OOOO00OOO0.topic}")#line:1066
        print ('开始解析。')#line:1067
        OO0OOOO000O0O00O0 =OOO00O0OOOO00OOO0 .consumer .partitions_for_topic (topic =OOO00O0OOOO00OOO0 .topic )#line:1069
        for OO0OOO00OOOOOO00O in OO0OOOO000O0O00O0 :#line:1070
            O0OOOOOOOO0OOOO0O =OOO00O0OOOO00OOO0 .get_toggle_or_offset (OOO00O0OOOO00OOO0 .topic ,OO0OOO00OOOOOO00O )#line:1071
            O000O0OOO00OO000O =0 if O0OOOOOOOO0OOOO0O <0 else O0OOOOOOOO0OOOO0O #line:1073
            OOO00O0OOOO00OOO0 .consumer_data (OO0OOO00OOOOOO00O ,O000O0OOO00OO000O ,OO00O00OOO0000O0O )#line:1074
    def save_all_offset (O0OOO0OO0O0OO0OOO ):#line:1076
        for OO00O000OO0OOOOO0 ,O00OO0O000O00OO0O in O0OOO0OO0O0OO0OOO .offsetDict :#line:1077
            O0OOO0OO0O0OO0OOO .write_offset (OO00O000OO0OOOOO0 ,O00OO0O000O00OO0O )#line:1078
