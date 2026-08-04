from urllib.parse import quote
class TrackingUrlBuilder:
    def build(self,template: str,tracking_number: str)->str:
        if not template.startswith('https://'):return ''
        return template.replace('{tracking}',quote(tracking_number,safe=''))
