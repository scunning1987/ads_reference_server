# ADS Reference Server
## Overview
This is a simple ADS reference server that build a VAST response with ads to fill a desired ad break duration

![](architecture-aws.png?width=80pc&classes=border,shadow)

## Release Notes
| Date       | Version | Update Notes                                                              |
|------------|-----|---------------------------------------------------------------------------|
| 2021-10-21 | 1.0 | Initial release containing support for simple ADS VAST and VMAP responses |
| 2023-04-24 | 1.1 | Added support for adding a wrapped VAST response                          |

## How To Deploy

Use [this](https://raw.githubusercontent.com/scunning1987/ads_reference_server/main/ads-ref-server.yaml) CloudFormation template to deploy the ADS Reference server resources. Once the stack is deployed, you can navigate to the Stack Output tab to see the API endpoint for the ADS server.


## How To Use
There are no required query parameters for this to work. The server can be configured to respond with a default duration if it is missing from the request.

example URL with duration query parameter:
```
https://1234567890.execute-api.us-west-2.amazonaws.com/v1/ads?duration=45
```

The server will return a VAST response like so:

```
<?xml version="1.0" encoding="utf-8"?>
<VAST version="3.0">
	<Ad sequence="1">
		<Inline>
			<AdSystem>2.0</AdSystem>
			<AdTitle>AD-caribbean-15-HD</AdTitle>
			<Impression><![CDATA[https://1234567890.execute-api.us-west-2.amazonaws.com/v1/impression]]></Impression>
			<Creatives>
				<Linear>
					<Duration>00:00:15</Duration>
					<MediaFiles>
						<MediaFile id="00001" delivery="progressive" type="video/mp4" width="1280" height="720"><![CDATA[https://1234567890.cloudfront.net/Media/Bumpers/AD-caribbean-15-HD.mp4]]></MediaFile>
					</MediaFiles>
				</Linear>
			</Creatives>
		</Inline>
	</Ad>
	<Ad sequence="2">
		<Inline>
			<AdSystem>2.0</AdSystem>
			<AdTitle>AD-caribbean2-15</AdTitle>
			<Impression><![CDATA[https://1234567890.execute-api.us-west-2.amazonaws.com/v1/impression]]></Impression>
			<Creatives>
				<Linear>
					<Duration>00:00:15</Duration>
					<MediaFiles>
						<MediaFile id="00002" delivery="progressive" type="video/mp4" width="1280" height="720"><![CDATA[https://1234567890.cloudfront.net/Media/Bumpers/AD-caribbean2-15-HD.mp4]]></MediaFile>
					</MediaFiles>
				</Linear>
			</Creatives>
		</Inline>
	</Ad>
	<Ad sequence="3">
		<Inline>
			<AdSystem>2.0</AdSystem>
			<AdTitle>AD-carracing-15</AdTitle>
			<Impression><![CDATA[https://1234567890.execute-api.us-west-2.amazonaws.com/v1/impression]]></Impression>
			<Creatives>
				<Linear>
					<Duration>00:00:15</Duration>
					<MediaFiles>
						<MediaFile id="00003" delivery="progressive" type="video/mp4" width="1280" height="720"><![CDATA[https://1234567890.cloudfront.net/Media/Bumpers/AD-carracing-15-HD.mp4]]></MediaFile>
					</MediaFiles>
				</Linear>
			</Creatives>
		</Inline>
	</Ad>
</VAST>
```

Once the solution is deployed via CloudFormation, open the "ads_reference_server" Lambda function and modify the `avaiable_ads` dictionary object to use your ad files.

This is an example of what the dictionary object looks like and the type of data you need to populate:

```
{
  "1": {
    "duration_s": 15,
    "location": "https://1234567890.cloudfront.net/Media/Bumpers/AD-caribbean-15-HD.mp4",
    "mediafile_name": "AD-caribbean-15-HD",
    "mediafile_id": "00001"
  },
  "2": {
    "duration_s": 15,
    "location": "https://1234567890.cloudfront.net/Media/Bumpers/AD-caribbean2-15-HD.mp4",
    "mediafile_name": "AD-caribbean2-15",
    "mediafile_id": "00002"
  },
  "3": {
    "duration_s": 15,
    "location": "https://1234567890.cloudfront.net/Media/Bumpers/AD-carracing-15-HD.mp4",
    "mediafile_name": "AD-carracing-15",
    "mediafile_id": "00003"
  },
  "4": {
    "duration_s": 15,
    "location": "https://1234567890.cloudfront.net/Media/Bumpers/AD-music-15-HD.mp4",
    "mediafile_name": "AD-music-15",
    "mediafile_id": "00004"
  }
}
```

On the CloudFormation **Outputs** section, there are 3 examples to show 3 different ADS functions:

* VAST request and response for linear use cases (pass a *duration* query parameter)
* VAST request and VMAP response for VOD use cases (pass a *assetid* query parameter)
* VAST request and wrapper response for Ad request redirects (change the path to `/vastwrapper` and pass query parameter *ads_url*)