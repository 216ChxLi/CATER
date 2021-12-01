import json

class Dataset:

    def __init__(self, all_objects_list: list, object_id: int):

        self.all_objects_list = all_objects_list
        self.object_id = object_id

        self.attributes_list = ['instance', 
                  'shape', 
                  'color', 
                  'size',                              
                  'material']
        self.attributes_value_dict = {}

    def get_attributes(self):
        for attribute in self.attributes_list:
            self.attributes_value_dict[attribute] = self.all_objects_list[self.object_id][attribute]

class File:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    def open_file(self):
        with open(input_path, 'r', encoding = 'UTF-8') as input_file:
            dictionary = json.load(input_file)
            input_file.close()
        all_objects_list = dictionary['objects']
        return all_objects_list

if __name__=='__main__':
    
    shape = []
    color = []
    size = []
    material = []

    for i in range(4000, 5781):

        input_path = r'D:\文档\12 Vorlesungen Stuttgart\21WS Practical Course ML & CV for HCI\01_code\02_One_Hot_Key\json_input/CATER_new_00{}.json'.format(str(i))
        output_path = r'D:\文档\12 Vorlesungen Stuttgart\21WS Practical Course ML & CV for HCI\01_code\02_One_Hot_Key\json_input/CATER_new_00{}.json'.format(str(i))

        try:
            file = File(input_path, output_path)
            all_objects_list = file.open_file()

            object_amount = len(all_objects_list)
            for object_id in range(object_amount):
                dataset = Dataset(all_objects_list, object_id)
                dataset.get_attributes()
                attributes_value_dict = dataset.attributes_value_dict
                
                if attributes_value_dict['shape'] not in shape:
                    shape.append(attributes_value_dict['shape'])

                if attributes_value_dict['color'] not in color: 
                    color.append(attributes_value_dict['color'])

                if attributes_value_dict['size'] not in size: 
                    size.append(attributes_value_dict['size'])

                if attributes_value_dict['material'] in material: 
                    pass
                else:
                    material.append(attributes_value_dict['material'])

        except FileNotFoundError:
            pass
    
    print(shape)
    print(color)
    print(size)
    print(material)