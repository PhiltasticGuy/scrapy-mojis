import scrapy
import os
import base64

class UnicodeSpider(scrapy.Spider):
    name = 'unicode'
    path = './emojis'
    pathExtended = path + '/extended'

    def start_requests(self):
        urls = [
            'http://unicode.org/emoji/charts/full-emoji-list.html',
            'http://unicode.org/emoji/charts/full-emoji-modifiers.html'
        ]

        # Loop through the 'urls' array and parse the sites with scrapy.
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

        # Each requests need their own processing callback because of our 
        # current emoji 'id' filtering.
        yield scrapy.Request(url=urls[0], callback=self.parse)
        yield scrapy.Request(url=urls[1], callback=self.parseExtended)

    def parse(self, response):
        # Select all the <tr> elements that contain <td> elements.
        rows = response.xpath('//tr[td]')

        # Return immediately if there's nothing...
        if (len(rows) <= 0):
            return
        
        for row in rows:
            # Skip non-emoji rows (They all have 15 <td> elements.)
            tdCount = row.xpath('count(td)').get()
            if (float(tdCount) < 15.0):
                continue

            # Select the columns for this row.
            cols = row.xpath('td')

            # Pick out the 'id' since we use it as a filter.
            id = int(cols[0].xpath('text()').get())
            isExtended = (id >= 208 and id <= 235)

            # Process the filtered emojis.
            if (id < 98 or isExtended):
                # Load the data into a JSON object.
                emoji = {
                    'id' : id,
                    'name' : cols[14].xpath('text()').get().replace(': ', '-').replace(' ', '-').lower(),
                    'isExtended' : isExtended,
                    'apple' : cols[3].xpath('img/@src').get(),
                    'google' : cols[4].xpath('img/@src').get(),
                    'facebook' : cols[5].xpath('img/@src').get(),
                    'windows' : cols[6].xpath('img/@src').get(),
                    'twitter' : cols[7].xpath('img/@src').get(),
                    'joy' : cols[8].xpath('img/@src').get(),
                    'samsung' : cols[9].xpath('img/@src').get()
                }

                # Print the emoji 'name' for debug purposes.
                print(emoji['name'])

                # Save the images associated with this emoji.
                self.saveImage(emoji, 'apple')
                self.saveImage(emoji, 'google')
                self.saveImage(emoji, 'facebook')
                self.saveImage(emoji, 'windows')
                self.saveImage(emoji, 'twitter')
                self.saveImage(emoji, 'joy')
                self.saveImage(emoji, 'samsung')

    def parseExtended(self, response):
        # Select all the <tr> elements that contain <td> elements.
        rows = response.xpath('//tr[td]')

        # Return immediately if there's nothing...
        if (len(rows) <= 0):
            return
        
        for row in rows:
            # Skip non-emoji rows (They all have 15 <td> elements.)
            tdCount = row.xpath('count(td)').get()
            if (float(tdCount) < 15.0):
                continue

            # Select the columns for this row.
            cols = row.xpath('td')

            # Pick out the 'id' since we use it as a filter.
            id = int(cols[0].xpath('text()').get())
            isExtended = (id >= 196 and id <= 335)

            # Process the filtered emojis.
            if (isExtended):
                # Load the data into a JSON object.
                emoji = {
                    'id' : id,
                    'name' : cols[14].xpath('text()').get().replace(': ', '-').replace(', ', '-').replace(' ', '-').lower(),
                    'isExtended' : isExtended,
                    'apple' : cols[3].xpath('img/@src').get(),
                    'google' : cols[4].xpath('img/@src').get(),
                    'facebook' : cols[5].xpath('img/@src').get(),
                    'windows' : cols[6].xpath('img/@src').get(),
                    'twitter' : cols[7].xpath('img/@src').get(),
                    'joy' : cols[8].xpath('img/@src').get(),
                    'samsung' : cols[9].xpath('img/@src').get()
                }

                # Print the emoji 'name' for debug purposes.
                print(emoji['name'])

                # Save the images associated with this emoji.
                self.saveImage(emoji, 'apple')
                self.saveImage(emoji, 'google')
                self.saveImage(emoji, 'facebook')
                self.saveImage(emoji, 'windows')
                self.saveImage(emoji, 'twitter')
                self.saveImage(emoji, 'joy')
                self.saveImage(emoji, 'samsung')

    def saveImage(self, emoji, emojiType):
        # Ensure output folders exist.
        if (not os.path.exists(self.path)):
            os.makedirs(self.path)

        if (not os.path.exists(self.pathExtended)):
            os.makedirs(self.pathExtended)

        # Only output images with data. (Some types don't have data...)
        if (emoji[emojiType]):
            # Create the filename from the emoji properties.
            filename = f'{emoji["id"]}-{emoji["name"]}-{emojiType}.png'
            
            # Prepend the correct folder to filename.
            if (not emoji['isExtended']):
                filename = f'{self.path}/{filename}'
            else:
                filename = f'{self.pathExtended}/{filename}'

            # Decode the HTML base64 encoding. The format is:
            #   'data:image/png;base64,[...BASE64_ENCODED_IMAGE...]'
            content = base64.b64decode(emoji[emojiType].split(',')[1])
            
            # Write the bytes to the disk.
            with open(filename, 'wb') as outfile:
                outfile.write(content)
        