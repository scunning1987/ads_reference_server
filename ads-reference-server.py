'''
Copyright (c) 2021 Scott Cunningham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Summary: This script is designed to create a linear HLS playlist using VOD content

Original Author: Scott Cunningham
'''

import json
import xmltodict
import time
from xml.sax import saxutils as su

def lambda_handler(event, context):

    default_ad_duration = 30 # Value to use if no duration is sent in the VAST request

    if event['path'] == "/ads":

        vast_req_duration = 0

        if 'queryStringParameters' in event:
            vast_req_params = event['queryStringParameters']

            if vast_req_params != None:
                if 'duration' in vast_req_params:
                    vast_req_duration = int(vast_req_params['duration'])
                else:
                    vast_req_duration = default_ad_duration
            else:
                vast_req_duration = default_ad_duration

        else:
            vast_req_duration = default_ad_duration

        if 'assetid' not in vast_req_params:
            # not a VOD VMAP response

            avaiable_ads = dict()
            avaiable_ads["1"] = {"duration_s":15,"location":"https://d3re4i3vgppvr8.cloudfront.net/Media/Bumpers/AD-caribbean-15-HD.mp4","mediafile_name":"AD-caribbean-15-HD","mediafile_id":"00001"}
            avaiable_ads["2"] = {"duration_s":15,"location":"https://d3re4i3vgppvr8.cloudfront.net/Media/Bumpers/AD-caribbean2-15-HD.mp4","mediafile_name":"AD-caribbean2-15","mediafile_id":"00002"}
            avaiable_ads["3"] = {"duration_s":15,"location":"https://d3re4i3vgppvr8.cloudfront.net/Media/Bumpers/AD-carracing-15-HD.mp4","mediafile_name":"AD-carracing-15","mediafile_id":"00003"}
            avaiable_ads["4"] = {"duration_s":15,"location":"https://d3re4i3vgppvr8.cloudfront.net/Media/Bumpers/AD-music-15-HD.mp4","mediafile_name":"AD-music-15","mediafile_id":"00004"}
            avaiable_ads["5"] = {"duration_s":15,"location":"https://d3re4i3vgppvr8.cloudfront.net/Media/Bumpers/AD-perfume-15-HD.mp4","mediafile_name":"AD-perfume-15","mediafile_id":"00005"}
            avaiable_ads["6"] = {"duration_s":15,"location":"https://d3re4i3vgppvr8.cloudfront.net/Media/Bumpers/AD-polarbear-15-HD.mp4","mediafile_name":"AD-polarbear-15","mediafile_id":"00006"}
            avaiable_ads["7"] = {"duration_s":15,"location":"https://d3re4i3vgppvr8.cloudfront.net/Media/Bumpers/AD-robots-15-HD.mp4","mediafile_name":"AD-robots-15","mediafile_id":"00007"}
            avaiable_ads["8"] = {"duration_s":15,"location":"https://d3re4i3vgppvr8.cloudfront.net/Media/Bumpers/AD-skiing-15-HD.mp4","mediafile_name":"AD-skiing-15","mediafile_id":"00008"}
            avaiable_ads["9"] = {"duration_s":15,"location":"https://d3re4i3vgppvr8.cloudfront.net/Media/Bumpers/AD-sports-15-HD.mp4","mediafile_name":"AD-sports-15","mediafile_id":"00009"}
            avaiable_ads["10"] = {"duration_s":15,"location":"https://d3re4i3vgppvr8.cloudfront.net/Media/Bumpers/AWSElemental_commerical_break_15s-HD.mp4","mediafile_name":"AWSElemental_commerical_break_15","mediafile_id":"00010"}
            avaiable_ads["11"] = {"duration_s":30,"location":"https://d3re4i3vgppvr8.cloudfront.net/Media/Bumpers/rugby-30-HD.mp4","mediafile_name":"rugby-30","mediafile_id":"00011"}

            cumulative_duration = 0
            ad_list = []
            for ad in avaiable_ads:
                sequence_id = ad
                ad_duration = avaiable_ads[ad]['duration_s']
                ad_location = avaiable_ads[ad]['location']
                ad_name = avaiable_ads[ad]['mediafile_name']
                ad_id = avaiable_ads[ad]['mediafile_id']

                cumulative_duration += int(ad_duration)
                if cumulative_duration <= vast_req_duration:
                    ad_dict = dict()
                    ad_dict['@sequence'] = str(sequence_id)
                    ad_dict['InLine'] = {}
                    ad_dict['InLine']['AdSystem'] = "2.0"
                    ad_dict['InLine']['AdTitle'] = ad_name
                    ad_dict['InLine']['Impression'] = {}
                    ad_dict['InLine']['Impression']['#text'] = '<![CDATA[%s]]>' % ('https://n8ljfs0h09.execute-api.us-west-2.amazonaws.com/v1/impression')
                    ad_dict['InLine']['Creatives'] = {}
                    ad_dict['InLine']['Creatives']['Creative'] = {}
                    ad_dict['InLine']['Creatives']['Creative']['Linear'] = {}
                    ad_dict['InLine']['Creatives']['Creative']['Linear']['Duration'] = time.strftime('%H:%M:%S', time.gmtime(int(ad_duration)))
                    ad_dict['InLine']['Creatives']['Creative']['Linear']['MediaFiles'] = {}
                    ad_dict['InLine']['Creatives']['Creative']['Linear']['MediaFiles']['MediaFile'] = {}
                    ad_dict['InLine']['Creatives']['Creative']['Linear']['MediaFiles']['MediaFile']['@id'] = str(ad_id)
                    ad_dict['InLine']['Creatives']['Creative']['Linear']['MediaFiles']['MediaFile']['@delivery'] = "progressive"
                    ad_dict['InLine']['Creatives']['Creative']['Linear']['MediaFiles']['MediaFile']['@type'] = "video/mp4"
                    ad_dict['InLine']['Creatives']['Creative']['Linear']['MediaFiles']['MediaFile']['@width'] = "1280"
                    ad_dict['InLine']['Creatives']['Creative']['Linear']['MediaFiles']['MediaFile']['@height'] = "720"
                    ad_dict['InLine']['Creatives']['Creative']['Linear']['MediaFiles']['MediaFile']['#text'] = '<![CDATA[%s]]>' % (ad_location)

                    ad_list.append(ad_dict)

            # build VAST response
            vast_response = dict()
            vast_response['VAST'] = {}
            vast_response['VAST']['@version'] = "3.0"
            vast_response['VAST']['@xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
            vast_response['VAST']['Ad'] = ad_list

            # convert payload to xml for return
            vast_xml = xmltodict.unparse(vast_response, short_empty_elements=True, pretty=True, encoding='utf-8')
            vast_xml = su.unescape(vast_xml)

        else:
            # This is VOD VMAP

            vmap_breaks = []

            vmap_break_times = [15,60]
            for vmap_break in vmap_break_times:

                vmap_break_dict = dict()
                vmap_break_dict['@timeOffset'] = time.strftime('%H:%M:%S', time.gmtime(int(vmap_break)))
                vmap_break_dict['@breakType'] = "linear"
                vmap_break_dict['@breakId'] = "midroll-%s" % (str(vmap_break))
                vmap_break_dict['vmap:AdSource'] = {}
                vmap_break_dict['vmap:AdSource']['@id'] = "ad-%s" % (str(vmap_break))
                vmap_break_dict['vmap:AdSource']['@allowMultipleAds'] = "true"
                vmap_break_dict['vmap:AdSource']['@followRedirects'] = "true"
                vmap_break_dict['vmap:AdSource']['vmap:AdTagURI'] = {}
                vmap_break_dict['vmap:AdSource']['vmap:AdTagURI']['@templateType'] = "vast3"
                vmap_break_dict['vmap:AdSource']['vmap:AdTagURI']['#text'] = '<![CDATA[%s]]>' % ("https://n8ljfs0h09.execute-api.us-west-2.amazonaws.com/v1/ads?duration=120")

                vmap_breaks.append(vmap_break_dict)

            vmap_response = dict()
            vmap_response['vmap:VMAP'] = {}
            vmap_response['vmap:VMAP']['@version'] = "1.0"
            vmap_response['vmap:VMAP']['@xmlns:vmap'] = "http://www.iab.net/videosuite/vmap"
            vmap_response['vmap:VMAP']['vmap:AdBreak'] = vmap_breaks

            # convert payload to xml for return
            vast_xml = xmltodict.unparse(vmap_response, short_empty_elements=True, pretty=True, encoding='utf-8')
            vast_xml = su.unescape(vast_xml)

        return {
            'statusCode': 200,
            "headers": {
                "Content-Type": "application/xml"
            },
            'body': vast_xml
        }

    else:
        # treat this as impression
        return {
            'statusCode': 200,
            "headers": {
                "Content-Type": "application/xml"
            }
        }
