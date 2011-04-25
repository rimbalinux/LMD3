
def get(request, start):
    if 
        if self.request.get('start'):
            json_data = []
            startid = int(self.request.get('start'));
            persontables = models.Personal().all()
            persontables = persontables.fetch(2, startid)
            for person in persontables:
                json_data.append({
                    'key' : str(person.key()),
                    'lc_id' : str(person.lc_id),
                    'name' : str(person.name),
                    'gender' : str(person.gender),
                    'address' : str(person.address),
                    'village' : getLocationName(self, int(person.village)),
                    'sub_district' : getLocationName(self, int(person.sub_district)),
                    'district' : getLocationName(self, int(person.district)),
                    'member_type' : str(person.member_type)
                    })
            self.response.out.write(json.encode(json_data))
        else:
            self.response.out.write('error')


