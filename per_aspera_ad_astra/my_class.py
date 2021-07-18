from PIL import Image
import requests


class AdAstra:
    # Size of one meridian or parallel in pixels on light pollution map

    # Image size was manually corrected (+120 pixels on the top)
    step_y = 16920 / 141
    # Image size was manually corrected (+118 pixels on the right)
    step_x = 43318 / 361

    def __init__(self, coords, month, time='22:00:00'):
        try:
            self.success = True  # If data was found by api or not
            self.month = month
            self.time = time
            arr = coords.split(', ')
            self.lat = arr[0]
            self.lon = arr[1]
            del arr
            self.timezone = ''
            self.address = ''
            self.av = {}
        except:  # Passing all the exceptions cuz we will catch it in __call__
            pass

    def __call__(self):
        try:
            self.get_json()
            if self.success:
                self.light_pollution()
                result = self.av
                result['timezone'] = self.timezone
                result['lat'] = self.lat
                result['lon'] = self.lon
                result['address'] = self.address
                return result
            result = {}
            self.lat = '0'
            self.lon = '0'
            self.light_pollution()
            return result
        except:
            return {'0': '0'}

    def light_pollution(self):

        Image.MAX_IMAGE_PIXELS = 725760000
        im_showable = Image.open(r'world2016B.png')
        im_dev = Image.open(r'world2016.png')

        # Getting coordinates of pixel where our location is
        dot_x = int(self.step_x * (180 + float(self.lon)))
        dot_y = int(self.step_y * (75 - float(self.lat)))

        # sqm and nelm are astronomical characteristics of visibility of stars.
        # here i make conformity between colour of pixel on the map
        # and sqm/nelm
        sqm = ['22.00-21.99', '21.99-21.93', '21.93-21.89', '21.89-21.81',
               '21.81-21.69', '21.69-21.51', '21.51-21.25', '21.25-20.91',
               '20.91-20.49', '20.49-20.02', '20.02-19.50', '19.50-18.95',
               '18.95-18.38', '18.38-17.80', '<17.80']
        nelm = ['6.6', '6.6', '6.6', '6.6-6.5', '6.5', '6.5-6.4', '6.4-6.3',
                '6.3-6.1', '6.1-5.8', '5.8-5.5', '5.5-5.1', '5.1-4.7',
                '4.7-4.3', '4.3-3.8', '<3.8']

        self.av['light_pol'] = (sqm[im_dev.getpixel((dot_x, dot_y))],
                                nelm[im_dev.getpixel((dot_x, dot_y))])

        # cropping our map. Our location in the center
        img = im_showable.crop((max(dot_x - 100, 0), max(dot_y - 100, 0),
                                min(dot_x + 100, im_showable.size[0]),
                                min(dot_y + 100, im_showable.size[1])))
        img.save('image1.png')

    # weather API

    def get_json(self):
        with open('Token.txt') as tok:
            api = tok.read()
        home_link = "https://weather.visualcrossing.com" \
                    "/VisualCrossingWebServices" \
                    "/rest/services/timeline/"

        params = 'cloudcover,' + 'conditions,' + 'humidity,' + 'visibility'
        if int(self.month) < 10:
            self.month = '0' + str(int(self.month))

        # Average weather characteristics will be counted with data for whole
        # month according to last year
        date = ('2020-' + self.month + '-01', '2020-' + self.month + '-28')

        result_call = home_link + self.lat + ',' + self.lon + '/' + date[
            0] + 'T' + self.time + '/' + date[1] + 'T' + self.time + '/' +\
            '?key=' + api + '&include=obs%2Cfcst%2Cstats%2Calerts%2Ccurrent' \
            '%2Chistfcst&elements=' + params

        data = requests.get(result_call)
        data = data.json()

        # if data wasn't found queryCost == 1
        if data['queryCost'] == 1:
            self.success = False
            self.lat = data['latitude']
            self.lon = data['longitude']
        else:
            self.lat = data['latitude']
            self.lon = data['longitude']
            self.address = data['resolvedAddress']
            self.timezone = data['timezone']
            self.av = {'vis': 0.0, 'cloud': 0.0, 'hum': 0.0}
            conditions = {}

            count = 1

            # counting average numbers
            for i in data['days']:

                if i['conditions'] not in conditions:
                    conditions[i['conditions']] = 0
                conditions[i['conditions']] += 1

                self.av['vis'] *= (count - 1) / count
                self.av['vis'] += i['visibility'] / count

                self.av['cloud'] *= (count - 1) / count
                self.av['cloud'] += i['cloudcover'] / count

                self.av['hum'] *= (count - 1) / count
                self.av['hum'] += i['humidity'] / count

                count += 1
            self.av['vis'] = str(round(self.av['vis'], 4))
            self.av['hum'] = str(round(self.av['hum'], 4))
            self.av['cloud'] = str(round(self.av['cloud'], 4))
