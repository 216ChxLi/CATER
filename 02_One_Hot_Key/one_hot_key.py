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

    def save_file(self, one_hot_key_array: list):
        one_hot_key_json = json.dumps(one_hot_key_array)
        with open(output_path, 'w', encoding = 'UTF-8') as output_file:
            output_file.write(one_hot_key_json)
            output_file.close()

class One_hot_key:

    def __init__(self, attributes_value_dict: dict):
        
        self.attributes_value_dict = attributes_value_dict

        self.shape_dict = {'spl': 0,
                           'cone': 1,
                           'sphere': 2,
                           'cylinder': 3,
                           'cube': 4}
        self.color_dict = {'gold': 0,
                           'blue': 1, 
                           'yellow': 2, 
                           'red': 3, 
                           'brown': 4, 
                           'green': 5, 
                           'cyan': 6, 
                           'purple': 7, 
                           'gray': 8}
        self.size_dict = {'small': 0, 
                          'medium': 1,
                          'large': 2}
        self.material_dict = {'metal': 0, 
                              'rubber': 1}

        self.one_hot_key = {}

    def match(self):
        shape = self.attributes_value_dict['shape']
        color = self.attributes_value_dict['color']
        size = self.attributes_value_dict['size']
        material = self.attributes_value_dict['material']

        shape_id = self.shape_dict[shape]
        color_id = self.color_dict[color]
        size_id = self.size_dict[size]
        material_id = self.material_dict[material]

        name = str(shape+'_'+color)
        self.one_hot_key[name] = []
        self.one_hot_key[name].append([shape_id, color_id, size_id, material_id])
        self.one_hot_key[name].append([shape, color, size, material])



if __name__=='__main__':
    
    for i in range(5780, 5781):

        input_path = r'D:\文档\12 Vorlesungen Stuttgart\21WS Practical Course ML & CV for HCI\01_code\02_One_Hot_Key\json_input/CATER_new_00{}.json'.format(str(i))
        output_path = r'D:\文档\12 Vorlesungen Stuttgart\21WS Practical Course ML & CV for HCI\01_code\02_One_Hot_Key\json_output/CATER_new_00{}.json'.format(str(i))

        one_hot_key_array = []

        try:
            file = File(input_path, output_path)
            all_objects_list = file.open_file()

            object_amount = len(all_objects_list)
            for object_id in range(object_amount):
                dataset = Dataset(all_objects_list, object_id)
                dataset.get_attributes()
                attributes_value_dict = dataset.attributes_value_dict
                
                ohk = One_hot_key(attributes_value_dict)
                ohk.match()
                one_hot_key_array.append(ohk.one_hot_key)
            
            print(one_hot_key_array)
            file.save_file(one_hot_key_array)

        except FileNotFoundError:
            pass