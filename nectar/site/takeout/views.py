# coding=utf-8
import json
from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from nectar.template import templated
from nectar import db
from nectar.models import User
from nectar import db
from forms import WifiQueryForm
from jester import Jester
from . import takeout

jester = Jester()

header = [u'SSID', u'BSSID', u'密码', u'加密方式', u'商户id', u'商户名称', u'省份', u'城市', u'经纬度']
security_map = [u'开放网络', u'WEP', u'WPA', u'EAP']

def refine_result(result):
    new = []
    for ap in result:
        tmp = {}
        lon, lat = 0.0, 0.0
        for k, v in ap.items():
            if k == 'ssid':
                tmp[u'SSID'] = v
            elif k == 'bssid':
                tmp[u'BSSID'] = v
            elif k == 'password':
                tmp[u'密码'] = v[:3] + len(v[:3]) * '*' if v else '-'
            elif k == 'security':
                tmp[u'加密方式'] = security_map[int(v)]
            elif k == 'shop_id':
                tmp[u'商户id'] = v if v > 0 else '-'
            elif k == 'shop_name':
                tmp[u'商户名称'] = v if v else '-'
            elif k == 'lon':
                lon = v
            elif k == 'lat':
                lat = v
            elif k == 'province':
                tmp[u'省份'] = v if v else '-'
            elif k == 'city':
                tmp[u'城市'] = v if v else '-'
            else:
                tmp[k] = v
            # 格式化经纬度
            if lon and lat:
                tmp[u'经纬度'] = '({0}, {1})'.format(lon, lat)
            else:
                tmp[u'经纬度'] = '-'
        new.append(tmp)
    return new


@takeout.route('/wifi', methods=['GET', 'POST'])
@templated('takeout/wifi.html')
def wifi():
    form = WifiQueryForm()
    if form.validate_on_submit():
        resp = jester.query(form.ssid.data)
        resultSet = refine_result(resp['result'])
        return dict(form=form, resultSet=resultSet, header=header)
    flash('无效的SSID')
    return dict(form=form)

